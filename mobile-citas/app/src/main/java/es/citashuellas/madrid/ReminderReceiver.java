package es.citashuellas.madrid;
import android.Manifest;
import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.os.Build;
public class ReminderReceiver extends BroadcastReceiver {
  static final String CHANNEL="recordatorios_huellas";
  static void createChannel(Context ctx){
    NotificationManager nm=(NotificationManager)ctx.getSystemService(Context.NOTIFICATION_SERVICE);
    if(nm!=null) {
      NotificationChannel ch=new NotificationChannel(CHANNEL,"Recordatorios citas de huellas",NotificationManager.IMPORTANCE_DEFAULT);
      ch.setDescription("Avisos para consultar el sitio oficial");
      nm.createNotificationChannel(ch);
    }
  }
  @Override public void onReceive(Context ctx,Intent incoming) {
    if(!ReminderScheduler.enabled(ctx)) return;
    createChannel(ctx);
    boolean permitted=Build.VERSION.SDK_INT<33 || ctx.checkSelfPermission(Manifest.permission.POST_NOTIFICATIONS)==PackageManager.PERMISSION_GRANTED;
    if(permitted){
      NotificationManager nm=(NotificationManager)ctx.getSystemService(Context.NOTIFICATION_SERVICE);
      Intent i=new Intent(ctx,MainActivity.class).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK|Intent.FLAG_ACTIVITY_CLEAR_TOP);
      PendingIntent pi=PendingIntent.getActivity(ctx,101,i,PendingIntent.FLAG_UPDATE_CURRENT|PendingIntent.FLAG_IMMUTABLE);
      Notification n=new Notification.Builder(ctx,CHANNEL)
        .setSmallIcon(R.drawable.ic_notification)
        .setContentTitle("Revisa las citas de huellas")
        .setContentText("Madrid / Aluche: consulta la web oficial. No indica disponibilidad.")
        .setStyle(new Notification.BigTextStyle().bigText("Es un recordatorio. Comprueba en la web oficial si hay citas para TIE. Este aviso NO indica plazas disponibles."))
        .setContentIntent(pi).setAutoCancel(true).build();
      if(nm!=null) nm.notify(1001,n);
    }
    ReminderScheduler.scheduleNext(ctx);
  }
}
