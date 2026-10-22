package com.baraemest.quranahmedakl.preview;

import android.app.Activity;
import android.os.Bundle;
import android.graphics.Color;
import android.graphics.Typeface;
import android.view.Gravity;
import android.view.View;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.net.Uri;
import android.content.Intent;

public final class MainActivity extends Activity {
    private static final String RECITER_URL = "https://ar.assabile.com/ahmed-akl/quran";
    private static final String ALAA_AQL_URL = "https://way2quran.com/ar/reciters/alaa-aql/hafs-an-asim";
    private static final String QURAN_URL = "https://ar.assabile.com/quran";
    private WebView browser;
    private ProgressBar progress;
    private String currentUrl = RECITER_URL;

    @Override public void onCreate(Bundle state) {
        super.onCreate(state);
        getWindow().setStatusBarColor(Color.rgb(18, 8, 42));
        getWindow().setNavigationBarColor(Color.rgb(18, 8, 42));

        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setBackgroundColor(Color.rgb(18, 8, 42));
        root.setLayoutDirection(View.LAYOUT_DIRECTION_RTL);

        TextView heading = new TextView(this);
        heading.setText("القرآن الكريم");
        heading.setTextSize(25);
        heading.setTypeface(Typeface.DEFAULT, Typeface.BOLD);
        heading.setTextColor(Color.WHITE);
        heading.setGravity(Gravity.CENTER);
        heading.setPadding(12, 20, 12, 4);
        root.addView(heading, new LinearLayout.LayoutParams(-1, -2));

        TextView subtitle = new TextView(this);
        subtitle.setText("أحمد عقل وعلاء عقل · الاستماع عبر الإنترنت");
        subtitle.setTextSize(15);
        subtitle.setTextColor(Color.rgb(240, 201, 135));
        subtitle.setGravity(Gravity.CENTER);
        subtitle.setPadding(12, 0, 12, 14);
        root.addView(subtitle, new LinearLayout.LayoutParams(-1, -2));

        LinearLayout tabs = new LinearLayout(this);
        tabs.setGravity(Gravity.CENTER);
        tabs.setPadding(10, 0, 10, 10);
        Button reader = makeButton("أحمد عقل");
        Button alaa = makeButton("علاء عقل");
        Button complete = makeButton("المصحف");
        tabs.addView(reader, new LinearLayout.LayoutParams(0, dp(54), 1));
        tabs.addView(alaa, new LinearLayout.LayoutParams(0, dp(54), 1));
        tabs.addView(complete, new LinearLayout.LayoutParams(0, dp(54), 1));
        root.addView(tabs);

        TextView hint = new TextView(this);
        hint.setText("إذا بقيت الصفحة بيضاء، اضغط «فتح في المتصفح» أسفل الشاشة");
        hint.setTextColor(Color.WHITE);
        hint.setTextSize(13);
        hint.setGravity(Gravity.CENTER);
        hint.setPadding(dp(10), dp(4), dp(10), dp(8));
        root.addView(hint);

        progress = new ProgressBar(this, null, android.R.attr.progressBarStyleHorizontal);
        progress.setMax(100);
        progress.setProgress(0);
        root.addView(progress, new LinearLayout.LayoutParams(-1, 3));

        browser = new WebView(this);
        browser.setBackgroundColor(Color.WHITE);
        WebSettings settings = browser.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setJavaScriptCanOpenWindowsAutomatically(false);
        settings.setAllowFileAccess(false);
        settings.setAllowContentAccess(false);
        settings.setMediaPlaybackRequiresUserGesture(true);
        settings.setMixedContentMode(WebSettings.MIXED_CONTENT_NEVER_ALLOW);
        browser.setWebChromeClient(new WebChromeClient() {
            @Override public void onProgressChanged(WebView view, int newProgress) {
                progress.setProgress(newProgress);
                progress.setVisibility(newProgress >= 100 ? View.INVISIBLE : View.VISIBLE);
            }
        });
        browser.setWebViewClient(new WebViewClient() {
            @Override public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                Uri uri = request.getUrl();
                if ("https".equalsIgnoreCase(uri.getScheme())) return false;
                try { startActivity(new Intent(Intent.ACTION_VIEW, uri)); } catch (Exception ignored) {}
                return true;
            }
        });
        root.addView(browser, new LinearLayout.LayoutParams(-1, 0, 1));

        Button openExternal = makeButton("فتح التلاوات في المتصفح");
        root.addView(openExternal, new LinearLayout.LayoutParams(-1, dp(54)));
        openExternal.setOnClickListener(v -> {
            try { startActivity(new Intent(Intent.ACTION_VIEW, Uri.parse(currentUrl))); }
            catch (Exception ignored) { hint.setText("لا يوجد متصفح متاح لفتح الصفحة"); }
        });
        setContentView(root);

        reader.setOnClickListener(v -> open(RECITER_URL));
        alaa.setOnClickListener(v -> open(ALAA_AQL_URL));
        complete.setOnClickListener(v -> open(QURAN_URL));
        if (state != null) {
            browser.restoreState(state);
        } else {
            open(RECITER_URL);
        }
    }

    private int dp(int value) {
        return (int) (value * getResources().getDisplayMetrics().density + 0.5f);
    }

    private Button makeButton(String label) {
        Button b = new Button(this);
        b.setText(label);
        b.setTextSize(14);
        b.setAllCaps(false);
        b.setTextColor(Color.WHITE);
        b.setBackgroundTintList(android.content.res.ColorStateList.valueOf(Color.rgb(47, 25, 99)));
        return b;
    }

    private void open(String url) {
        currentUrl = url;
        browser.loadUrl(url);
    }

    @Override protected void onSaveInstanceState(Bundle state) {
        browser.saveState(state);
        super.onSaveInstanceState(state);
    }

    @Override public void onBackPressed() {
        if (browser != null && browser.canGoBack()) browser.goBack();
        else super.onBackPressed();
    }
}
