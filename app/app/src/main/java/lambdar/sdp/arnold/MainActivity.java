package lambdar.sdp.arnold;

import android.app.Activity;
import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Intent;
import android.os.Build;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.v4.app.NotificationCompat;
import android.support.v4.app.NotificationManagerCompat;
//import android.support.design.widget.BottomNavigationView;
import android.util.Log;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.CompoundButton;
import android.widget.Switch;
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
    boolean alarm_flag=false;
    private NotificationChannel mChannel;
    private NotificationManager mManager;
    private Random prng = new Random(0);
//    private BottomNavigationView.OnNavigationItemSelectedListener mOnNavigationItemSelectedListener
//            =new BottomNavigationView.OnNavigationItemSelectedListener() {
//        @Override
//        public boolean onNavigationItemSelected(@NonNull MenuItem item) {
//            return false;
//        }
//    };
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
        Switch activateSwitch = (Switch)  findViewById(R.id.switch1);
        Switch notificationSwitch = (Switch)  findViewById(R.id.switch2);
        TextView followstatement = findViewById(R.id.manoraut);
        TextView disturbStatement = findViewById(R.id.disturbia);
//        BottomNavigationView navigation =findViewById(R.id.navigation);
//        navigation.setOnNavigationItemSelectedListener(mOnNavigationItemSelectedListener);
        activateSwitch.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                if (isChecked==true){
                 //   Log.i(LOG_TAG,"ON");
                    followstatement.setText("Follow");
                    mHelper.sendMessage("arnold/topics", "START");
                }
                else {
                  //  Log.i(LOG_TAG,"OF");
                    followstatement.setText("Do Not Follow");
                    mHelper.sendMessage("arnold/topics","STOP");
                }
            }
        });

        notificationSwitch.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                if (isChecked==true){
                    //   Log.i(LOG_TAG,"ON");
                    disturbStatement.setText("Out of Range Alarm");
                    alarm_flag=true;

                }
                else {
                    //  Log.i(LOG_TAG,"OF");
                    disturbStatement.setText("No Alarm");
                    alarm_flag=false;
                }
            }
        });
        initMembers();
    }


    private void initMembers()
    {

        makeNotificationChannel();

        this .mHelper = new MQTTHelper(this . getApplicationContext());
        this .mHelper. setCallback(new ArnoldMQTTCallback(this, new MqttCallback()));

   /*     this.fields.put(
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
        );*/


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
        if (message_string.equals("OR")&& alarm_flag) //only give notification if switch is on.
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
