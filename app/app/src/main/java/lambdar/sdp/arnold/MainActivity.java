package lambdar.sdp.arnold;

import android.app.Activity;
import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Intent;
import android.os.Build;
import android.os.Bundle;
import android.support.v4.app.NotificationCompat;
import android.support.v4.app.NotificationManagerCompat;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;


import org.eclipse.paho.client.mqttv3.MqttMessage;

import java.util.HashMap;
import java.util.Map;
import java.util.Random;

import helpers.ArnoldMQTTCallback;
import helpers.Callback;
import helpers.MQTTHelper;
import helpers.NotificationHelper;

import static helpers.Constants.LOG_TAG;

public class MainActivity extends Activity
{

    private Button m_test_button;
    private MQTTHelper mHelper;
    private NotificationChannel mChannel;
    private NotificationManager mManager;
    private Random prng = new Random(0);
    Map<String, TextView> fields = new HashMap<>();
    TextView previousView;

    private class MqttCallback implements Callback<MainActivity, MqttMessage>
    {
        public void accept(MainActivity activity, MqttMessage message)
        {
            activity.messageReceived(message);
        }
    }


    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        initMembers();
    }


    private void initMembers()
    {

        makeNotificationChannel();

        this .mHelper = new MQTTHelper(this . getApplicationContext());
        this .mHelper. setCallback(new ArnoldMQTTCallback(this, new MqttCallback()));

        this.fields.put(
                "KEY_UP_PRESSED",
                (TextView) findViewById(R.id.up)
        );

        this.fields.put(
                "KEY_DOWN_PRESSED",
                (TextView) findViewById(R.id.down)
        );

        this.fields.put(
                "KEY_LEFT_PRESSED",
                (TextView) findViewById(R.id.left)
        );

        this.fields.put(
                "KEY_RIGHT_PRESSED",
                (TextView) findViewById(R.id.right)
        );


    }

    public void onTestButtonClicked(View view)
    {
        this .mHelper. sendMessage("arnold/topics", "STOP");
    }

    public void messageReceived(MqttMessage message)
    {
        Log.i(LOG_TAG, message.toString());

        String message_string = message.toString();

        Log.i(LOG_TAG, "Checking if to send notification");
        if (message_string.equals("OR"))
        {
            Log.i(LOG_TAG, "Sending notification");
            NotificationHelper.sendNotification(
                    this,
                    "Out of Range Alarm",
                    "Your Arnold is out of range. Go find it!",
                    MainActivity.class
            );
        }

    }

    public void makeNotificationChannel()
    {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O)
        {
            String name = "Arnold";
            String description = "Notification Channel for Arnold Companion App";
            int importance = NotificationManager.IMPORTANCE_HIGH;
            this . mChannel  = new NotificationChannel(name, description, importance);
            registerChannel();
        }
    }

    public void registerChannel()
    {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O)
        {
            this . mManager = this . getSystemService(NotificationManager.class);
            if (this . mManager == null)
            {
                return;
            }
            this . mManager . createNotificationChannel(this . mChannel);
        }
    }

    public void greenPressed(View view)
    {
        this . mHelper . sendMessage("arnold/test", "GREEN");
    }

    public void redPressed(View view)
    {
        this . mHelper . sendMessage("arnold/test", "RED");
    }
}
