package com.baraemest.profealexbarae;

import android.Manifest;
import android.app.Activity;
import android.content.ActivityNotFoundException;
import android.content.ContentValues;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Color;
import android.net.Uri;
import android.net.http.SslError;
import android.os.Build;
import android.os.Bundle;
import android.provider.MediaStore;
import android.speech.RecognizerIntent;
import android.view.Gravity;
import android.view.View;
import android.webkit.JavascriptInterface;
import android.webkit.PermissionRequest;
import android.webkit.SslErrorHandler;
import android.webkit.ValueCallback;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceError;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Button;
import android.widget.FrameLayout;
import android.widget.LinearLayout;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;
import org.json.JSONObject;
import java.util.ArrayList;

public final class MainActivity extends Activity {
    private static final String HOME = "https://profe-alex.baraemest.workers.dev/";
    private static final String HOST = "profe-alex.baraemest.workers.dev";
    private static final int PICK_IMAGE = 530, VOICE = 531, AUDIO = 532;
    private WebView web;
    private ProgressBar loader;
    private LinearLayout errorView;
    private ValueCallback<Uri[]> fileCallback;
    private Uri cameraUri;
    private PermissionRequest pendingAudio;
    private VoiceController nativeVoice;

    @Override public void onCreate(Bundle state) {
        super.onCreate(state);
        getWindow().setStatusBarColor(Color.rgb(59,36,131));
        getWindow().setNavigationBarColor(Color.rgb(246,242,255));
        getWindow().getDecorView().setSystemUiVisibility(View.SYSTEM_UI_FLAG_LIGHT_NAVIGATION_BAR);
        FrameLayout root = new FrameLayout(this);
        root.setBackgroundColor(Color.rgb(250,247,255));
        web = new WebView(this);
        web.setBackgroundColor(Color.rgb(250,247,255));
        root.addView(web,new FrameLayout.LayoutParams(-1,-1));
        loader = new ProgressBar(this);
        root.addView(loader,new FrameLayout.LayoutParams(80,80,Gravity.CENTER));
        errorView = createErrorView();
        errorView.setVisibility(View.GONE);
        root.addView(errorView,new FrameLayout.LayoutParams(-1,-1));
        setContentView(root);

        WebSettings s = web.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setLoadsImagesAutomatically(true);
        s.setMediaPlaybackRequiresUserGesture(false);
        s.setAllowFileAccess(false);
        s.setAllowContentAccess(true);
        s.setMixedContentMode(WebSettings.MIXED_CONTENT_NEVER_ALLOW);
        s.setSupportZoom(false);
        s.setCacheMode(WebSettings.LOAD_DEFAULT);
        if(Build.VERSION.SDK_INT>=26) s.setSafeBrowsingEnabled(true);
        WebView.setWebContentsDebuggingEnabled(false);
        nativeVoice=new VoiceController(this,web);
        web.addJavascriptInterface(new AndroidFeatures(),"ProfeAlexAndroid");

        web.setWebViewClient(new WebViewClient() {
            @Override public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest req) {
                Uri url = req.getUrl();
                if ("https".equalsIgnoreCase(url.getScheme()) && HOST.equalsIgnoreCase(url.getHost())) return false;
                if ("https".equalsIgnoreCase(url.getScheme())) {
                    try { startActivity(new Intent(Intent.ACTION_VIEW,url)); }
                    catch(Exception e) { Toast.makeText(MainActivity.this,"No se puede abrir el enlace",Toast.LENGTH_SHORT).show(); }
                }
                return true;
            }
            @Override public void onPageFinished(WebView view,String url) {
                loader.setVisibility(View.GONE);
                if(url.startsWith(HOME)) {
                    errorView.setVisibility(View.GONE);
                    nativeVoice.pageLoaded();
                }
            }
            @Override public void onReceivedError(WebView view,WebResourceRequest req,WebResourceError error) {
                if(req.isForMainFrame()) {loader.setVisibility(View.GONE);errorView.setVisibility(View.VISIBLE);}
            }
            @Override public void onReceivedSslError(WebView view,SslErrorHandler handler,SslError error) {
                handler.cancel(); loader.setVisibility(View.GONE);errorView.setVisibility(View.VISIBLE);
            }
        });

        web.setWebChromeClient(new WebChromeClient() {
            @Override public void onPermissionRequest(PermissionRequest request) {
                runOnUiThread(() -> {
                    String origin=request.getOrigin()==null?"":request.getOrigin().toString();
                    if(!origin.equals("https://"+HOST)) {request.deny();return;}
                    boolean audio=false;
                    for(String resource:request.getResources())
                        if(PermissionRequest.RESOURCE_AUDIO_CAPTURE.equals(resource)) audio=true;
                    if(!audio) {request.deny();return;}
                    if(checkSelfPermission(Manifest.permission.RECORD_AUDIO)==PackageManager.PERMISSION_GRANTED)
                        request.grant(new String[]{PermissionRequest.RESOURCE_AUDIO_CAPTURE});
                    else {pendingAudio=request;requestPermissions(new String[]{Manifest.permission.RECORD_AUDIO},AUDIO);}
                });
            }
            @Override public void onPermissionRequestCanceled(PermissionRequest request) {
                if(pendingAudio==request)pendingAudio=null;
            }
            @Override public boolean onShowFileChooser(WebView view,ValueCallback<Uri[]> cb,FileChooserParams params) {
                if(fileCallback!=null)fileCallback.onReceiveValue(null);
                fileCallback=cb;cameraUri=null;
                Intent gallery=new Intent(Intent.ACTION_GET_CONTENT);
                gallery.addCategory(Intent.CATEGORY_OPENABLE);
                gallery.setType("image/*");
                Intent chooser=Intent.createChooser(gallery,"Elegir foto de deberes");
                Intent camera=new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
                if(camera.resolveActivity(getPackageManager())!=null) {
                    try {
                        ContentValues v=new ContentValues();
                        v.put(MediaStore.Images.Media.DISPLAY_NAME,"ProfeAlex_"+System.currentTimeMillis()+".jpg");
                        v.put(MediaStore.Images.Media.MIME_TYPE,"image/jpeg");
                        if(Build.VERSION.SDK_INT>=29) v.put(MediaStore.Images.Media.RELATIVE_PATH,"Pictures/ProfeAlex");
                        cameraUri=getContentResolver().insert(MediaStore.Images.Media.EXTERNAL_CONTENT_URI,v);
                        if(cameraUri!=null) {
                            camera.putExtra(MediaStore.EXTRA_OUTPUT,cameraUri);
                            camera.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION|Intent.FLAG_GRANT_WRITE_URI_PERMISSION);
                            chooser.putExtra(Intent.EXTRA_INITIAL_INTENTS,new Intent[]{camera});
                        }
                    } catch(Exception ignored) {cameraUri=null;}
                }
                try {startActivityForResult(chooser,PICK_IMAGE);}
                catch(ActivityNotFoundException e) {
                    fileCallback.onReceiveValue(null);fileCallback=null;
                    Toast.makeText(MainActivity.this,"No hay galería disponible",Toast.LENGTH_SHORT).show();
                }
                return true;
            }
        });
        web.loadUrl(HOME);
    }

    private LinearLayout createErrorView() {
        LinearLayout outer=new LinearLayout(this);
        outer.setOrientation(LinearLayout.VERTICAL);
        outer.setGravity(Gravity.CENTER);
        outer.setPadding(32,30,32,30);
        outer.setBackgroundColor(Color.rgb(250,247,255));
        TextView title=new TextView(this);
        title.setText("📚 Profe Alex");
        title.setTextColor(Color.rgb(53,35,111));
        title.setTextSize(27);title.setGravity(Gravity.CENTER);outer.addView(title);
        TextView message=new TextView(this);
        message.setText("Para estudiar necesito Internet. Comprueba la conexión y vuelve a intentarlo.");
        message.setTextColor(Color.rgb(59,44,90));
        message.setTextSize(17);message.setGravity(Gravity.CENTER);message.setPadding(0,20,0,20);
        outer.addView(message);
        Button retry=new Button(this);
        retry.setText("VOLVER A CONECTAR");
        retry.setOnClickListener(v->{errorView.setVisibility(View.GONE);loader.setVisibility(View.VISIBLE);web.loadUrl(HOME);});
        outer.addView(retry);
        return outer;
    }

    private final class AndroidFeatures {
        @JavascriptInterface public int voiceVersion() { return 2; }
        @JavascriptInterface public void startSpeech(String lang) {
            runOnUiThread(()->nativeVoice.startSpeech(lang));
        }
        @JavascriptInterface public void startConversation(String lang) {
            runOnUiThread(()->nativeVoice.startConversation(lang));
        }
        @JavascriptInterface public void stopConversation() {
            runOnUiThread(()->nativeVoice.stopConversation());
        }
        @JavascriptInterface public void stopTalking() {
            runOnUiThread(()->nativeVoice.stopTalking());
        }
        @JavascriptInterface public void tutorError() {
            runOnUiThread(()->nativeVoice.tutorError());
        }
        @JavascriptInterface public void speak(String text,String lang) {
            runOnUiThread(()->nativeVoice.speak(text,lang));
        }
    }

    @Override protected void onActivityResult(int req,int result,Intent data) {
        super.onActivityResult(req,result,data);
        if(req==PICK_IMAGE) {
            Uri chosen=(result==RESULT_OK&&data!=null)?data.getData():null;
            Uri[] returned=null;
            if(result==RESULT_OK) {
                if(chosen!=null)returned=new Uri[]{chosen};
                else if(cameraUri!=null)returned=new Uri[]{cameraUri};
            }
            if(cameraUri!=null&&(returned==null||!cameraUri.equals(returned[0]))) {
                try {getContentResolver().delete(cameraUri,null,null);}catch(Exception ignored){}
            }
            if(fileCallback!=null)fileCallback.onReceiveValue(returned);
            fileCallback=null;cameraUri=null;
        } else if(req==VOICE&&result==RESULT_OK&&data!=null) {
            ArrayList<String> results=data.getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS);
            if(results!=null&&!results.isEmpty()) {
                String js="(function(){var x=document.getElementById('input');if(x){x.value="+JSONObject.quote(results.get(0))+";x.dispatchEvent(new Event('input',{bubbles:true}));x.focus();}})();";
                web.evaluateJavascript(js,null);
            }
        }
    }

    @Override public void onRequestPermissionsResult(int req,String[] perms,int[] grants) {
        super.onRequestPermissionsResult(req,perms,grants);
        if(req==VoiceController.MIC_PERMISSION_REQUEST) {
            nativeVoice.microphonePermission(grants.length>0&&grants[0]==PackageManager.PERMISSION_GRANTED);
            return;
        }
        if(req==AUDIO&&pendingAudio!=null) {
            if(grants.length>0&&grants[0]==PackageManager.PERMISSION_GRANTED)
                pendingAudio.grant(new String[]{PermissionRequest.RESOURCE_AUDIO_CAPTURE});
            else pendingAudio.deny();
            pendingAudio=null;
        }
    }

    @Override public void onBackPressed() {
        if(errorView.getVisibility()==View.VISIBLE) {
            errorView.setVisibility(View.GONE);web.loadUrl(HOME);
        } else if(web.canGoBack())web.goBack();
        else super.onBackPressed();
    }

    @Override protected void onPause() {
        if(nativeVoice!=null)nativeVoice.pause();
        super.onPause();
    }
    @Override protected void onResume() {
        super.onResume();
        if(nativeVoice!=null)nativeVoice.resume();
    }
    @Override protected void onDestroy() {
        if(fileCallback!=null){fileCallback.onReceiveValue(null);fileCallback=null;}
        if(nativeVoice!=null)nativeVoice.destroy();
        web.removeJavascriptInterface("ProfeAlexAndroid");
        web.destroy();
        super.onDestroy();
    }
}
