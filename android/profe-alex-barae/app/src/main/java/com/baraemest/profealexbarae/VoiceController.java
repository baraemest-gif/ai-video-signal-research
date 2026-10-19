package com.baraemest.profealexbarae;

import android.Manifest;
import android.app.Activity;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.media.AudioAttributes;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.speech.RecognitionListener;
import android.speech.RecognizerIntent;
import android.speech.SpeechRecognizer;
import android.speech.tts.TextToSpeech;
import android.speech.tts.UtteranceProgressListener;
import android.webkit.WebView;
import org.json.JSONObject;
import java.util.ArrayList;
import java.util.Locale;

/** A supervised, turn-based voice conversation; microphone stops when app pauses. */
public final class VoiceController {
    static final int MIC_PERMISSION_REQUEST=533;
    private final Activity activity;
    private final WebView web;
    private final Handler handler=new Handler(Looper.getMainLooper());
    private static final String HOST_URL="https://profe-alex.baraemest.workers.dev/";
    private TextToSpeech tts;
    private SpeechRecognizer recognizer;
    private boolean ttsReady=false, ttsFailed=false, conversation=false, listening=false;
    private boolean paused=false, awaitingPermission=false, alive=true, speaking=false;
    private int silenceRetries=0, utteranceCounter=0;
    private String language="es-ES", pendingText=null, pendingLanguage="es-ES";
    private Runnable scheduledRetry;

    VoiceController(Activity activity, WebView web) {
        this.activity=activity;
        this.web=web;
        tts=new TextToSpeech(activity, status->activity.runOnUiThread(()->{
            if(!alive)return;
            ttsReady=status==TextToSpeech.SUCCESS;
            ttsFailed=!ttsReady;
            if(ttsReady){
                tts.setSpeechRate(0.94f);
                tts.setPitch(1.02f);
                tts.setAudioAttributes(new AudioAttributes.Builder()
                    .setUsage(AudioAttributes.USAGE_MEDIA)
                    .setContentType(AudioAttributes.CONTENT_TYPE_SPEECH).build());
                tts.setLanguage(Locale.forLanguageTag("es-ES"));
                tts.setOnUtteranceProgressListener(new UtteranceProgressListener() {
                    @Override public void onStart(String id) {
                        activity.runOnUiThread(()->{if(alive){speaking=true;notifyPage("speaking","🔊 Profe Alex está hablando…");}});
                    }
                    @Override public void onDone(String id) {
                        activity.runOnUiThread(()->{
                            if(!alive)return;
                            speaking=false;
                            if(conversation&&!paused)handler.postDelayed(()->{if(conversation&&!paused)listenInternal();},450);
                            else notifyPage("idle","🎧 Pulsa el micrófono para seguir hablando.");
                        });
                    }
                    @Override public void onError(String id) {
                        activity.runOnUiThread(()->{
                            if(!alive)return;
                            speaking=false;
                            notifyPage("error","El móvil no pudo reproducir la voz. Comprueba el motor de texto a voz.");
                            if(conversation)stopConversation();
                        });
                    }
                });
                if(pendingText!=null){String txt=pendingText,loc=pendingLanguage;pendingText=null;speak(txt,loc);}
                else notifyPage("ready","🔊 Voz de Profe Alex preparada.");
            }else notifyPage("error","Instala o activa Servicios de voz de Google en Android.");
        }));
    }

    private void notifyPage(String state,String message) {
        if(!alive||web.getUrl()==null||!web.getUrl().startsWith(HOST_URL))return;
        web.evaluateJavascript("(function(){var n=window.profeAlexNative;if(n&&n.onStatus)n.onStatus("+JSONObject.quote(state)+","+JSONObject.quote(message)+");})();",null);
    }

    private void recognized(String text) {
        if(!alive||web.getUrl()==null||!web.getUrl().startsWith(HOST_URL))return;
        web.evaluateJavascript("(function(){var n=window.profeAlexNative;if(n&&n.onSpeech)n.onSpeech("+JSONObject.quote(text)+");})();",null);
    }

    public void pageLoaded(){notifyPage("ready",ttsFailed?"⚠️ Revisa el motor de voz de Android.":"🎧 Voz preparada. Pulsa para hablar.");}

    public void speak(String text,String locale) {
        if(!alive||paused)return;
        text=(text==null?"":text).replaceAll("[#*]{1,3}","").trim();
        if(text.isEmpty()){if(conversation)listenInternal();return;}
        if(text.length()>3900)text=text.substring(0,3900);
        if(!ttsReady){
            pendingText=text;pendingLanguage=locale;
            if(ttsFailed)notifyPage("error","No hay voz instalada. Activa el motor de texto a voz del teléfono.");
            return;
        }
        cancelScheduledRetry();
        if(listening&&recognizer!=null){recognizer.cancel();listening=false;}
        String loc="en-GB".equalsIgnoreCase(locale)?"en-GB":"es-ES";
        int support=tts.setLanguage(Locale.forLanguageTag(loc));
        if(support==TextToSpeech.LANG_MISSING_DATA||support==TextToSpeech.LANG_NOT_SUPPORTED)
            tts.setLanguage(Locale.forLanguageTag("es-ES"));
        int result=tts.speak(text,TextToSpeech.QUEUE_FLUSH,null,"alex-barae-"+(++utteranceCounter));
        if(result==TextToSpeech.ERROR)notifyPage("error","Error de audio. Comprueba volumen y motor de voz.");
    }

    public void startConversation(String locale){
        if(!alive||paused)return;
        conversation=true;silenceRetries=0;
        language="en-GB".equalsIgnoreCase(locale)?"en-GB":"es-ES";
        cancelScheduledRetry();
        if(speaking&&tts!=null){tts.stop();speaking=false;}
        requestListen();
    }

    public void startSpeech(String locale){
        if(!alive||paused)return;
        language="en-GB".equalsIgnoreCase(locale)?"en-GB":"es-ES";
        cancelScheduledRetry();
        if(speaking&&tts!=null){tts.stop();speaking=false;}
        requestListen();
    }

    private void requestListen(){
        if(activity.checkSelfPermission(Manifest.permission.RECORD_AUDIO)!=PackageManager.PERMISSION_GRANTED){
            awaitingPermission=true;
            notifyPage("permission","Permite el micrófono para hablar con Profe Alex.");
            activity.requestPermissions(new String[]{Manifest.permission.RECORD_AUDIO},MIC_PERMISSION_REQUEST);
        }else listenInternal();
    }

    public void microphonePermission(boolean granted){
        if(!awaitingPermission)return;
        awaitingPermission=false;
        if(granted)listenInternal();
        else {conversation=false;notifyPage("off","Micrófono sin permiso. Puedes usar el teclado.");}
    }

    private void createRecognizerIfNeeded(){
        if(recognizer!=null)return;
        if(!SpeechRecognizer.isRecognitionAvailable(activity)){
            conversation=false;
            notifyPage("error","Falta reconocimiento de voz. Activa Servicios de voz de Google.");
            return;
        }
        recognizer=SpeechRecognizer.createSpeechRecognizer(activity);
        recognizer.setRecognitionListener(new RecognitionListener(){
            @Override public void onReadyForSpeech(Bundle params){notifyPage("listening","🔴 Te escucho, Barae. Habla ahora.");}
            @Override public void onBeginningOfSpeech(){silenceRetries=0;notifyPage("listening","🎙️ Te estoy escuchando…");}
            @Override public void onRmsChanged(float rms){}
            @Override public void onBufferReceived(byte[] buffer){}
            @Override public void onEndOfSpeech(){notifyPage("thinking","⏳ Estoy entendiendo tu pregunta…");}
            @Override public void onError(int error){
                listening=false;
                if(!conversation){notifyPage("idle","No te he oído. Pulsa el micrófono e inténtalo otra vez.");return;}
                if(error==SpeechRecognizer.ERROR_NO_MATCH||error==SpeechRecognizer.ERROR_SPEECH_TIMEOUT){
                    if(silenceRetries++<1){notifyPage("ready","Prueba a hablar otra vez.");scheduleRetry();}
                    else{conversation=false;notifyPage("off","No he oído nada. Pulsa Hablar para continuar.");}
                }else{
                    conversation=false;
                    notifyPage("error",error==SpeechRecognizer.ERROR_NETWORK?"Sin conexión para reconocer voz.":"El micrófono se ha detenido. Vuelve a pulsar Hablar.");
                }
            }
            @Override public void onResults(Bundle results){
                listening=false;
                ArrayList<String> list=results.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION);
                String text=list!=null&&!list.isEmpty()?list.get(0).trim():"";
                if(text.isEmpty()){
                    if(conversation&&silenceRetries++<1)scheduleRetry();
                    else notifyPage("idle","No he oído palabras. Pulsa para intentarlo.");
                    return;
                }
                silenceRetries=0;
                notifyPage("thinking","⏳ Profe Alex está preparando su respuesta…");
                recognized(text);
            }
            @Override public void onPartialResults(Bundle b){}
            @Override public void onEvent(int event,Bundle b){}
        });
    }

    private void scheduleRetry(){
        cancelScheduledRetry();
        scheduledRetry=()->{scheduledRetry=null;if(conversation&&!paused)listenInternal();};
        handler.postDelayed(scheduledRetry,650);
    }
    private void cancelScheduledRetry(){if(scheduledRetry!=null){handler.removeCallbacks(scheduledRetry);scheduledRetry=null;}}

    private void listenInternal(){
        if(!alive||paused||listening)return;
        if(activity.checkSelfPermission(Manifest.permission.RECORD_AUDIO)!=PackageManager.PERMISSION_GRANTED){requestListen();return;}
        createRecognizerIfNeeded();if(recognizer==null)return;
        if(speaking&&tts!=null){tts.stop();speaking=false;}
        try{
            Intent i=new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
            i.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL,RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);
            i.putExtra(RecognizerIntent.EXTRA_LANGUAGE,language);
            i.putExtra(RecognizerIntent.EXTRA_LANGUAGE_PREFERENCE,language);
            i.putExtra(RecognizerIntent.EXTRA_PARTIAL_RESULTS,false);
            i.putExtra(RecognizerIntent.EXTRA_MAX_RESULTS,1);
            listening=true;recognizer.startListening(i);
            notifyPage("listening","🔴 Te escucho, Barae…");
        }catch(Exception e){
            listening=false;conversation=false;
            notifyPage("error","No se pudo activar el micrófono. Revisa los permisos.");
        }
    }

    public void stopTalking(){
        if(tts!=null)tts.stop();
        speaking=false;
        if(conversation&&!paused)listenInternal();
        else notifyPage("ready","Audio detenido.");
    }

    public void tutorError(){
        if(!alive)return;
        conversation=false;
        if(tts!=null)tts.stop();
        speaking=false;
        notifyPage("error","Sin respuesta del tutor. Comprueba Internet y vuelve a intentar.");
    }

    public void stopConversation(){
        conversation=false;silenceRetries=0;cancelScheduledRetry();
        if(recognizer!=null&&listening){recognizer.cancel();listening=false;}
        if(tts!=null)tts.stop();
        speaking=false;
        notifyPage("off","⏹ Conversación detenida. Toca Hablar cuando quieras continuar.");
    }
    public void pause(){paused=true;stopConversation();}
    public void resume(){paused=false;}
    public void destroy(){
        alive=false;conversation=false;cancelScheduledRetry();
        if(recognizer!=null){recognizer.cancel();recognizer.destroy();recognizer=null;}
        if(tts!=null){tts.stop();tts.shutdown();tts=null;}
    }
}
