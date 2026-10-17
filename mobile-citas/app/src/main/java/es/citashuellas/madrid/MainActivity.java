package es.citashuellas.madrid;
import android.Manifest;
import android.app.Activity;
import android.content.ActivityNotFoundException;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Color;
import android.graphics.Typeface;
import android.graphics.drawable.GradientDrawable;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;
import android.widget.Toast;
public class MainActivity extends Activity {
  private static final String URL="https://icp.administracionelectronica.gob.es/icpplus/index.html";
  private static final int NAVY=Color.rgb(18,42,78);
  private static final int BLUE=Color.rgb(28,78,155);
  private LinearLayout content;
  private TextView status;
  @Override public void onCreate(Bundle b){
    super.onCreate(b);
    getWindow().setStatusBarColor(NAVY);
    getWindow().setNavigationBarColor(NAVY);
    ReminderReceiver.createChannel(this);
    build();
    updateStatus();
  }
  private int dp(float n){ return (int)(n*getResources().getDisplayMetrics().density+0.5f); }
  private GradientDrawable bg(int color){ GradientDrawable d=new GradientDrawable(); d.setColor(color); d.setCornerRadius(dp(14)); return d; }
  private TextView text(String value,int size,int color,boolean bold){
    TextView v=new TextView(this);
    v.setText(value); v.setTextSize(size); v.setTextColor(color);
    if(bold) v.setTypeface(Typeface.DEFAULT,Typeface.BOLD);
    v.setLineSpacing(dp(3),1f);
    return v;
  }
  private void line(String value,int size,boolean bold,int margin){
    TextView v=text(value,size,NAVY,bold);
    LinearLayout.LayoutParams p=new LinearLayout.LayoutParams(-1,-2);
    p.bottomMargin=dp(margin);
    content.addView(v,p);
  }
  private void button(String value,int background,int foreground,Runnable callback){
    Button b=new Button(this); b.setText(value); b.setAllCaps(false);
    b.setTextSize(19); b.setTextColor(foreground);
    b.setTypeface(Typeface.DEFAULT,Typeface.BOLD);
    b.setBackground(bg(background));
    b.setOnClickListener(v->callback.run());
    LinearLayout.LayoutParams p=new LinearLayout.LayoutParams(-1,dp(68));
    p.bottomMargin=dp(14);
    content.addView(b,p);
  }
  private void build(){
    ScrollView scroll=new ScrollView(this); scroll.setFillViewport(true);
    scroll.setBackgroundColor(Color.rgb(238,244,253));
    content=new LinearLayout(this); content.setOrientation(LinearLayout.VERTICAL);
    content.setPadding(dp(24),dp(35),dp(24),dp(27));
    scroll.addView(content); setContentView(scroll);
    line("CITAS DE HUELLAS",29,true,10);
    line("Madrid · Aluche · Tarjeta TIE",20,true,25);
    line("Consulta las citas en la web oficial",22,true,12);
    line("Para pedir una cita: elige MADRID y el trámite «POLICÍA – TOMA DE HUELLA».",19,false,20);
    button("ABRIR CITA OFICIAL ↗",BLUE,Color.WHITE,this::openOfficial);
    status=text("",19,NAVY,true);
    status.setPadding(dp(18),dp(20),dp(18),dp(20)); status.setBackground(bg(Color.WHITE));
    LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(-1,-2);
    lp.bottomMargin=dp(17); content.addView(status,lp);
    button("ACTIVAR RECORDATORIOS",NAVY,Color.WHITE,this::activate);
    button("DETENER RECORDATORIOS",Color.rgb(215,226,244),NAVY,()->{
      ReminderScheduler.stop(this); updateStatus();
      Toast.makeText(this,"Recordatorios detenidos",Toast.LENGTH_LONG).show();
    });
    line("CÓMO FUNCIONA",22,true,12);
    line("1. Abre la página oficial y consulta las citas.\n\n2. Activa recordatorios para volver a mirar.\n\n3. Cuando aparezca una hora, reserva tú mismo.",18,false,22);
    line("AVISO IMPORTANTE",20,true,8);
    line("La aplicación NO consulta plazas automáticamente, NO reserva citas y NO evita CAPTCHA. Los avisos son recordatorios, no confirmaciones de disponibilidad. Android puede retrasarlos.",17,false,16);
  }
  private void updateStatus() {
    status.setText(ReminderScheduler.enabled(this) ? "🔔 AVISOS ACTIVADOS\nCada 20 minutos aproximadamente, de 06:00 a 22:00." : "🔕 AVISOS DETENIDOS\nPulsa Activar recordatorios para recibir avisos de consulta.");
  }
  private void activate(){
    ReminderScheduler.start(this); updateStatus();
    if(Build.VERSION.SDK_INT>=33 && checkSelfPermission(Manifest.permission.POST_NOTIFICATIONS)!=PackageManager.PERMISSION_GRANTED)
      requestPermissions(new String[]{Manifest.permission.POST_NOTIFICATIONS},200);
    else Toast.makeText(this,"Avisos activados. Android puede retrasarlos.",Toast.LENGTH_LONG).show();
  }
  private void openOfficial(){
    Intent i=new Intent(Intent.ACTION_VIEW,Uri.parse(URL)); i.addCategory(Intent.CATEGORY_BROWSABLE);
    try {startActivity(i);} catch(ActivityNotFoundException e){Toast.makeText(this,"Instala un navegador para continuar.",Toast.LENGTH_LONG).show();}
  }
  @Override public void onRequestPermissionsResult(int code,String[] permissions,int[] grant){
    super.onRequestPermissionsResult(code,permissions,grant);
    if(code==200){
      if(grant.length==0 || grant[0]!=PackageManager.PERMISSION_GRANTED){
        ReminderScheduler.stop(this);
        Toast.makeText(this,"Permite las notificaciones para activar avisos.",Toast.LENGTH_LONG).show();
      }
      updateStatus();
    }
  }
}
