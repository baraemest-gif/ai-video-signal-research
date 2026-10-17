package es.citashuellas.madrid;
import android.app.AlarmManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import java.util.Calendar;
public final class ReminderScheduler {
  private ReminderScheduler(){}
  static final String PREF = "citas_huellas";
  static final String ACTIVE = "active";
  static boolean enabled(Context ctx) {return ctx.getSharedPreferences(PREF,Context.MODE_PRIVATE).getBoolean(ACTIVE,false);}
  private static PendingIntent intent(Context ctx) {
    Intent i = new Intent(ctx,ReminderReceiver.class).setAction("es.citashuellas.madrid.REVIEW");
    return PendingIntent.getBroadcast(ctx,100,i,PendingIntent.FLAG_UPDATE_CURRENT|PendingIntent.FLAG_IMMUTABLE);
  }
  static void start(Context ctx){
    ctx.getSharedPreferences(PREF,Context.MODE_PRIVATE).edit().putBoolean(ACTIVE,true).apply();
    scheduleNext(ctx);
  }
  static void stop(Context ctx){
    ctx.getSharedPreferences(PREF,Context.MODE_PRIVATE).edit().putBoolean(ACTIVE,false).apply();
    AlarmManager am=(AlarmManager)ctx.getSystemService(Context.ALARM_SERVICE);
    if(am!=null) am.cancel(intent(ctx));
  }
  static void scheduleNext(Context ctx) {
    if(!enabled(ctx)) return;
    Calendar next=Calendar.getInstance();
    next.add(Calendar.MINUTE,20);
    int hour=next.get(Calendar.HOUR_OF_DAY);
    if(hour>=22 || hour<6){
      if(hour>=22) next.add(Calendar.DATE,1);
      next.set(Calendar.HOUR_OF_DAY,6);
      next.set(Calendar.MINUTE,0);
      next.set(Calendar.SECOND,0);
      next.set(Calendar.MILLISECOND,0);
    }
    AlarmManager am=(AlarmManager)ctx.getSystemService(Context.ALARM_SERVICE);
    if(am!=null) am.setAndAllowWhileIdle(AlarmManager.RTC_WAKEUP,next.getTimeInMillis(),intent(ctx));
  }
}
