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
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.CompoundButton;
import android.widget.Switch;
import android.widget.TextView;


import org.eclipse.paho.client.mqttv3.MqttMessage;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
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
    private TextView poweredBy;
    private Random prng = new Random(0);
    private boolean notifications_flag = false;

    private RecyclerView wordlistView;
    private RecyclerView.Adapter wAdapter;
    private RecyclerView.LayoutManager wLayoutManager;

    static class SwitchButton
    {
        CompoundButton.OnCheckedChangeListener mListener;
        String label;

        SwitchButton(String label, CompoundButton.OnCheckedChangeListener listener)
        {
            this.label = label;
            this.mListener = listener;
        }
    }


    private static class WordlistAdapter extends RecyclerView.Adapter<WordlistAdapter.ViewHolder>
    {

        private List<SwitchButton> dataset;

        class ViewHolder extends RecyclerView.ViewHolder
        {
            String string;
            TextView categoryName;
            Switch mSwitch;

            ViewHolder(View v)
            {
                super(v);
                this . categoryName = v . findViewById(R . id . categoryName);
                this . mSwitch = v . findViewById(R . id . categorySwitch);
            }

            void setText(String text)
            {
                this . categoryName . setText(text);
            }

            void setListener(CompoundButton.OnCheckedChangeListener listener)
            {
                this . mSwitch . setOnCheckedChangeListener(listener);
            }
        }

        public WordlistAdapter(List<SwitchButton> gw)
        {
            this . dataset = gw;
        }

        @Override
        public WordlistAdapter.ViewHolder onCreateViewHolder(ViewGroup parent, int viewType)
        {
            View v = LayoutInflater.from(parent.getContext())
                    .inflate(R.layout.optioncard, parent, false);
            return new ViewHolder(v);
        }

        @Override
        public void onBindViewHolder(final WordlistAdapter.ViewHolder holder, int position)
        {
            SwitchButton card_at_position = this . dataset . get(position);

            holder . setText(card_at_position . label);

            holder . setListener(card_at_position . mListener);


        }

        @Override
        public int getItemCount()
        {
            return this . dataset . size();
        }
    }

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

        this .mHelper = new MQTTHelper(this . getApplicationContext());
        this .mHelper. setCallback(new ArnoldMQTTCallback(this, new MqttCallback()));

        List<SwitchButton> options = new ArrayList<>();

        options.add(new SwitchButton(
                "Follow",
                new CompoundButton.OnCheckedChangeListener() {
                    public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                        if (isChecked){
                            //   Log.i(LOG_TAG,"ON");
                            mHelper.sendMessage("arnold/topics", "START");
                        }
                        else {
                            //  Log.i(LOG_TAG,"OF");
                            mHelper.sendMessage("arnold/topics","STOP");
                        }
                    }
                }
        ));

        options.add(new SwitchButton(
                "Out of Range",
                new CompoundButton.OnCheckedChangeListener() {
                    public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                        alarm_flag = isChecked;
                    }
                }
        ));

        options.add(new SwitchButton(
                "Lock",
                new CompoundButton.OnCheckedChangeListener()
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
                }
        ));

        options.add(new SwitchButton(
                "Notifications",
                new CompoundButton.OnCheckedChangeListener()
                {
                    @Override
                    public void onCheckedChanged(CompoundButton buttonView, boolean isChecked)
                    {
                        notifications_flag = isChecked;
                    }
                }
        ));


        wordlistView = (RecyclerView) findViewById(R.id.wordlist_recycler_view);
        wordlistView . setHasFixedSize(true);

        wLayoutManager = new LinearLayoutManager(this);
        wordlistView.setLayoutManager(wLayoutManager);

        wAdapter = new WordlistAdapter(options);
        wordlistView . setAdapter(wAdapter);

    }

    public void messageReceived(MqttMessage message)
    {
        if (!this.notifications_flag)
        {
            return;
        }
        Log.i(LOG_TAG, message.toString());

        String message_string = message.toString();

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
            Log.i(LOG_TAG, "Sending notification");
            NotificationHelper.sendNotification(
                    this,
                    "Anti-Theft Alarm",
                    "Your Arnold lid has been opened. Someone might be trying to steal your belongings",
                    this.getClass()
            );
        }

    }
}
