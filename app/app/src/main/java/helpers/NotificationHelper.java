package helpers;

import android.app.Notification;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.app.Service;
import android.content.Context;
import android.content.Intent;
import android.util.Log;

import lambdar.sdp.arnold.R;

import static helpers.Constants.LOG_TAG;


public class NotificationHelper
{
    public static void sendNotification(Context ctxt, String title, String message, Class<?> target)
    {
        Log.i(LOG_TAG, "Received command to send notification");
        NotificationManager notificationManager = (NotificationManager) ctxt.getSystemService(
                Service.NOTIFICATION_SERVICE
        );

        Intent intent = new Intent(ctxt, target);

        PendingIntent pendingIntent = PendingIntent.getActivity(
                ctxt,
                0,
                intent,
                0
        );


        Notification.Builder builder = new Notification.Builder(ctxt)
                .setContentTitle(title)
                .setContentText(message)
                .setSmallIcon(R.mipmap.ic_launcher)
                .setContentIntent(pendingIntent)
                .setDefaults(Notification.DEFAULT_ALL)
                .setPriority(Notification.PRIORITY_MAX);


        Notification not = builder.build();

        notificationManager.notify(0, not);
    }
}
