package es.citas.madrid.fondo;

import android.Manifest;
import android.app.Activity;
import android.app.AlarmManager;
import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Color;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.PowerManager;
import android.view.Gravity;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;
import android.widget.Toast;
import java.net.HttpURLConnection;
import java.net.URL;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

/*
 * App complementaria para el agente V17.
 * Comprueba solamente accesibilidad HTTPS con pantalla bloqueada.
 * HTTP 200 NO significa plazas; no autentica, no rellena ni reserva.
 */
public class MainActivity extends Activity {
  private TextView estado;
  private static final int NAVY=Color.rgb(20,44,81);
  private static final String OFFICIAL="https://icp.administracionelectronica.gob.es/icpplus/index.html";

  @Override public void onCreate(Bundle b) {
    super.onCreate(b);
    getWindow().setStatusBarColor(NAVY);
    getWindow().setNavigationBarColor(NAVY);
    ui();
    checkNotificationPermission();
  }
  private void ui(){
    ScrollView sc=new ScrollView(this);sc.setFillViewport(true);sc.setBackgroundColor(Color.rgb(239,245,252));
    LinearLayout l=new LinearLayout(this);l.setOrientation(LinearLayout.VERTICAL);l.setPadding(36,42,36,36);
    sc.addView(l);setContentView(sc);
    add(l,"CITAS TIE · MADRID",28,NAVY,true);
    add(l,"Comprobación técnica en segundo plano",20,NAVY,true);
    add(l,"Funciona con la pantalla bloqueada para consultar si la sede oficial responde. No consulta plazas disponibles ni puede reservar citas automáticamente.",17,Color.DKGRAY,false);
    estado=new TextView(this);estado.setTextSize(19);estado.setTextColor(NAVY);estado.setPadding(15,26,15,28);
    l.addView(estado);refresh();
    btn(l,"ACTIVAR · CADA 15 MINUTOS",()->{
      Engine.start(this);refresh();checkNotificationPermission();
      Toast.makeText(this,"Comprobaciones activadas (Android puede retrasarlas)",Toast.LENGTH_LONG).show();
    });
    btn(l,"COMPROBAR CONEXIÓN AHORA",()->{
      if(!Engine.active(this))Engine.start(this);
      sendBroadcast(new Intent(this,CheckReceiverPublic.class).setAction("es.citas.madrid.fondo.CHECK"));
      Toast.makeText(this,"Comprobación técnica solicitada",Toast.LENGTH_SHORT).show();
    });
    btn(l,"ABRIR TRÁMITE OFICIAL",()->{
      startActivity(new Intent(Intent.ACTION_VIEW,Uri.parse(OFFICIAL)).addCategory(Intent.CATEGORY_BROWSABLE));
    });
    btn(l,"ACTUALIZAR ESTADO",this::refresh);
    btn(l,"DETENER COMPROBACIONES",()->{Engine.stop(this);refresh();});
    add(l,"LÍMITES IMPORTANTES",20,NAVY,true);
    add(l,"• Respuesta HTTP 200 ≠ cita disponible.\n• Android puede retrasar alarmas en modo ahorro de energía.\n• No se accede a certificados, Cl@ve ni CAPTCHA.\n• Para completar citas en Chrome, desbloquea el teléfono y utiliza el agente V17 de Termux.\n• La vigilancia finaliza el 27 de octubre de 2026.",16,Color.DKGRAY,false);
  }
  private void add(LinearLayout l,String t,int s,int color,boolean bold){
    TextView v=new TextView(this);v.setText(t);v.setTextSize(s);v.setTextColor(color);
    if(bold)v.setTypeface(null,1);v.setPadding(0,0,0,24);l.addView(v);
  }
  private void btn(LinearLayout l,String t,Runnable on){
    Button v=new Button(this);v.setText(t);v.setTextSize(16);v.setAllCaps(false);
    v.setTextColor(Color.WHITE);v.setBackgroundTintList(android.content.res.ColorStateList.valueOf(NAVY));
    LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(-1,-2);lp.bottomMargin=12;
    l.addView(v,lp);v.setOnClickListener(x->on.run());
  }
  private void refresh(){
    if(estado==null)return;
    long last=Engine.prefs(this).getLong("last",0L);
    String when=last>0?new SimpleDateFormat("dd/MM/yyyy HH:mm",new Locale("es","ES")).format(new Date(last)):"Sin ejecutar";
    String state=Engine.prefs(this).getString("result","Aún no hay resultado técnico");
    estado.setText((Engine.active(this)?"● ACTIVA":"○ DETENIDA")+
      "\nPróximas comprobaciones: aproximadamente cada 15 minutos"+
      "\nÚltima: "+when+"\n"+state+
      "\n\nPlazas: NO VERIFICADAS");
  }
  @Override protected void onResume(){super.onResume();refresh();}
  private void checkNotificationPermission(){
    if(Build.VERSION.SDK_INT>=33 &&
      checkSelfPermission(Manifest.permission.POST_NOTIFICATIONS)!=PackageManager.PERMISSION_GRANTED){
      requestPermissions(new String[]{Manifest.permission.POST_NOTIFICATIONS},203);
    }
  }
}

final class Engine {
  static final String PREF="estado_fondo";
  static final long INTERVAL=15*60*1000L;
  static final long DEADLINE=1793141940000L; // 27 Oct 2026, 23:59 Europe/Madrid
  static android.content.SharedPreferences prefs(Context c){return c.getSharedPreferences(PREF,Context.MODE_PRIVATE);}
  static boolean active(Context c){return prefs(c).getBoolean("active",false);}
  static void note(Context c,String result){prefs(c).edit().putString("result",result).putLong("last",System.currentTimeMillis()).apply();}
  static PendingIntent pending(Context c){
    Intent intent=new Intent(c,CheckReceiverPublic.class).setAction("es.citas.madrid.fondo.CHECK");
    return PendingIntent.getBroadcast(c,19,intent,PendingIntent.FLAG_UPDATE_CURRENT|PendingIntent.FLAG_IMMUTABLE);
  }
  static void start(Context c){prefs(c).edit().putBoolean("active",true).apply();schedule(c);}
  static void stop(Context c){
    prefs(c).edit().putBoolean("active",false).apply();
    AlarmManager a=(AlarmManager)c.getSystemService(Context.ALARM_SERVICE);
    if(a!=null)a.cancel(pending(c));
  }
  static void schedule(Context c){
    if(!active(c))return;
    long next=System.currentTimeMillis()+INTERVAL;
    if(next>=DEADLINE){stop(c);note(c,"Finalizado: se alcanzó el 27/10/2026.");return;}
    AlarmManager a=(AlarmManager)c.getSystemService(Context.ALARM_SERVICE);
    if(a!=null)a.setAndAllowWhileIdle(AlarmManager.RTC_WAKEUP,next,pending(c));
  }
}
class CheckReceiver extends BroadcastReceiver {
  private static final String CHANNEL="fallos_portal_v2";
  private static final ExecutorService pool=Executors.newSingleThreadExecutor();
  @Override public void onReceive(Context c,Intent i){
    if(!Engine.active(c))return;
    Engine.schedule(c);
    final PendingResult finish=goAsync();final Context app=c.getApplicationContext();
    pool.execute(()->{
      PowerManager.WakeLock wake=null;HttpURLConnection conn=null;
      try{
        PowerManager pm=(PowerManager)app.getSystemService(Context.POWER_SERVICE);
        if(pm!=null){wake=pm.newWakeLock(PowerManager.PARTIAL_WAKE_LOCK,"CitasMadrid:ConsultaTecnica");wake.acquire(13000L);}
        conn=(HttpURLConnection)new URL("https://icp.administracionelectronica.gob.es/icpplus/index.html").openConnection();
        conn.setRequestMethod("GET");conn.setConnectTimeout(4500);conn.setReadTimeout(4500);
        conn.setInstanceFollowRedirects(false);
        int code=conn.getResponseCode();
        Engine.note(app,(code>=200&&code<400?"Portal oficial accesible":"Portal respondió sin acceso normal")+
          " (HTTP "+code+"). Plazas no verificadas.");
      }catch(Exception ex){
        Engine.note(app,"No se pudo verificar la conexión a la sede. No informa de plazas.");notifyFailure(app);
      }finally{
        if(conn!=null)conn.disconnect();
        if(wake!=null&&wake.isHeld())wake.release();
        finish.finish();
      }
    });
  }
  private void notifyFailure(Context c){
    long now=System.currentTimeMillis();
    if(now-Engine.prefs(c).getLong("lastAlert",0L)<6*60*60*1000L)return;
    Engine.prefs(c).edit().putLong("lastAlert",now).apply();
    if(Build.VERSION.SDK_INT>=33 && c.checkSelfPermission(Manifest.permission.POST_NOTIFICATIONS)!=PackageManager.PERMISSION_GRANTED)return;
    NotificationManager nm=(NotificationManager)c.getSystemService(Context.NOTIFICATION_SERVICE);
    if(nm==null)return;
    nm.createNotificationChannel(new NotificationChannel(CHANNEL,"Estado técnico del portal",NotificationManager.IMPORTANCE_DEFAULT));
    Intent it=new Intent(c,MainActivity.class);it.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK|Intent.FLAG_ACTIVITY_CLEAR_TOP);
    PendingIntent pi=PendingIntent.getActivity(c,20,it,PendingIntent.FLAG_UPDATE_CURRENT|PendingIntent.FLAG_IMMUTABLE);
    Notification n=new Notification.Builder(c,CHANNEL)
      .setSmallIcon(android.R.drawable.ic_dialog_info)
      .setContentTitle("Citas Madrid: comprobar conexión")
      .setContentText("No se pudo verificar el portal. No indica plazas disponibles.")
      .setContentIntent(pi).setAutoCancel(true).build();
    nm.notify(20,n);
  }
}
class BootReceiver extends BroadcastReceiver {
  @Override public void onReceive(Context c,Intent i){
    if(Intent.ACTION_BOOT_COMPLETED.equals(i.getAction())&&Engine.active(c))Engine.schedule(c);
  }
}
