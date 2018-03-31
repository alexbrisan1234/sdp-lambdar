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
    boolean alarm_flag = false;
    boolean theft_flag = false;
    private NotificationChannel mChannel;
    private NotificationManager mManager;
    private Button stopAlarm;
    private Switch theftie;
    private Random prng = new Random(0);

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
        theftie = (Switch) findViewById(R.id.theftie);

        TextView followstatement = findViewById(R.id.manoraut);
        TextView disturbStatement = findViewById(R.id.disturbia);

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
                alarm_flag = isChecked;
                if (isChecked){
                    //   Log.i(LOG_TAG,"ON");
                    disturbStatement.setText("Out of Range Alarm");

                }
                else {
                    //  Log.i(LOG_TAG,"OF");
                    disturbStatement.setText("No Alarm");
                }
            }
        });

        theftie.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener()
        {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked)
            {
                theft_flag = isChecked;
                if (isChecked)
                {
                    mHelper.sendMessage("arnold/test", "LOCK");
                }
                else
                {
                    mHelper.sendMessage("arnold/test", "UNLOCK");
                }

            }
        });


        initMembers();
    }


    private void initMembers()
    {

        this .mHelper = new MQTTHelper(this . getApplicationContext());
        this .mHelper. setCallback(new ArnoldMQTTCallback(this, new MqttCallback()));

        this . stopAlarm = (Button) findViewById(R.id.button);
        this . stopAlarm . setVisibility(Button.INVISIBLE);


    }

    public void messageReceived(MqttMessage message)
    {
        Log.i(LOG_TAG, message.toString());

        String message_string = message.toString();

        Log.i(LOG_TAG, "Checking if to send notification");

        if (message_string.equals("OR") && alarm_flag) //only give notification if switch is on.
        {
            Log.i(LOG_TAG, "Sending notification");
            NotificationHelper.sendNotification(
                    this,
                    "Out of Range Alarm",
                    "Your Arnold is out of range. Go find it!",
                    MainActivity.class
            );
        }
        else if (message_string.equals("AL") && theft_flag)
        {
            this . stopAlarm . setVisibility(Button.VISIBLE);
            this . theftie . setClickable(false);
            NotificationHelper.sendNotification(
                    this,
                    "Anti-Theft Alarm",
                    "Your Arnold lid has been opened. Someone might be trying to steal your belongings",
                    this.getClass()
            );
        }

    }

    public void stopAlarm(View view)
    {
        this . mHelper . sendMessage("arnold/test", "ASTOP");
        this . stopAlarm . setVisibility(Button.INVISIBLE);
        this . theftie . setClickable(true);
    }
}
