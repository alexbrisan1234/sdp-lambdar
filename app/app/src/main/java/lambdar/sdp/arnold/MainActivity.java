package lambdar.sdp.arnold;

import android.app.Activity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;

import org.eclipse.paho.client.mqttv3.MqttMessage;

import helpers.ArnoldMQTTCallback;
import helpers.MQTTHelper;

import static helpers.Constants.LOG_TAG;

public class MainActivity extends Activity
{

    private Button m_test_button;
    private MQTTHelper helper;

    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        initMembers();

    }


    private void initMembers()
    {
        this . m_test_button = findViewById(R.id.test_button);
        this . m_test_button . setOnClickListener(this::onTestButtonClicked);

        this . helper = new MQTTHelper(this . getApplicationContext());
        this . helper . setCallback(new ArnoldMQTTCallback(this::messageReceived));
    }

    public void onTestButtonClicked(View view)
    {

    }

    public void messageReceived(MqttMessage message)
    {
        Log.w(LOG_TAG, message.toString());
    }
}
