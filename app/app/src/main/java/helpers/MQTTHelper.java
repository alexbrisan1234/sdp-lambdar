package helpers;

import android.content.Context;
import android.util.Log;

import org.eclipse.paho.android.service.MqttAndroidClient;
import org.eclipse.paho.client.mqttv3.DisconnectedBufferOptions;
import org.eclipse.paho.client.mqttv3.IMqttActionListener;
import org.eclipse.paho.client.mqttv3.IMqttToken;
import org.eclipse.paho.client.mqttv3.MqttCallbackExtended;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;

import static helpers.Constants.LOG_TAG;


public class MQTTHelper
{
    final String serverURI = "tcp://m12.cloudmqtt.com:19634";
    final String subscriptionTopic = "arnold/+";
    final String clientID = "arnoldApp";
    final String username = "gdsszota";
    final String password = "F6am0LwBcGBG";

    private MqttAndroidClient mqttAndroidClient;

    public MQTTHelper(Context ctxt)
    {
        mqttAndroidClient = new MqttAndroidClient(ctxt, serverURI, clientID);
        mqttAndroidClient.setCallback(new ArnoldMQTTCallback());

        connect();
    }

    public void setCallback(MqttCallbackExtended callback)
    {
        mqttAndroidClient.setCallback(callback);
    }

    private void connect()
    {
        MqttConnectOptions mqttConnectOptions = new MqttConnectOptions();
        mqttConnectOptions.setAutomaticReconnect(true);
        mqttConnectOptions.setCleanSession(false);
        mqttConnectOptions.setUserName(this.username);
        mqttConnectOptions.setPassword(this.password.toCharArray());

        try
        {
            this.mqttAndroidClient.connect(
                    mqttConnectOptions,
                    null,
                    new IMqttActionListener()
                    {
                        @Override
                        public void onSuccess(IMqttToken asyncActionToken)
                        {
                            DisconnectedBufferOptions disconnectedBufferOptions = new DisconnectedBufferOptions();
                            disconnectedBufferOptions.setBufferEnabled(true);
                            disconnectedBufferOptions.setBufferSize(100);
                            disconnectedBufferOptions.setPersistBuffer(false);
                            disconnectedBufferOptions.setDeleteOldestMessages(false);
                            mqttAndroidClient.setBufferOpts(disconnectedBufferOptions);
                            subscribeToTopic();
                        }

                        @Override
                        public void onFailure(IMqttToken asyncActionToken, Throwable exception)
                        {
                            Log.e(LOG_TAG, "Failed to connect to: " + serverURI + exception.toString());

                        }
                    }
            );
        } catch (MqttException exc)
        {
            exc.printStackTrace();
        }
    }

    public void subscribeToTopic()
    {
        try
        {
            mqttAndroidClient.subscribe(subscriptionTopic, 0, null, new IMqttActionListener()
            {
                @Override
                public void onSuccess(IMqttToken asyncActionToken)
                {
                    Log.i("Mqtt", "Subscribed!");
                }

                @Override
                public void onFailure(IMqttToken asyncActionToken, Throwable exception)
                {
                    Log.e("Mqtt", "Subscribed fail!");
                }
            });

        }
        catch (MqttException ex)
        {
            ex.printStackTrace();
        }
    }

    public void sendMessage(String topic, String message)
    {
        MqttMessage t_to_send = new MqttMessage(message.getBytes());
        try
        {
            this . mqttAndroidClient . publish(topic, t_to_send);
        }
        catch (MqttException exc)
        {
            Log.e(LOG_TAG, exc.toString());
        }
    }

}
