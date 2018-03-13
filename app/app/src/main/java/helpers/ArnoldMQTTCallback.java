package helpers;


import android.util.Log;
import static helpers.Constants.LOG_TAG;

import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallbackExtended;
import org.eclipse.paho.client.mqttv3.MqttMessage;

import java.util.function.Consumer;

import lambdar.sdp.arnold.MainActivity;

public class ArnoldMQTTCallback<T> implements MqttCallbackExtended
{
    private Consumer<MqttMessage> responseCallback;
    private Callback<T,MqttMessage> java7Callback;
    private T object;

    public ArnoldMQTTCallback() {}
    public ArnoldMQTTCallback(Consumer<MqttMessage> callback)
    {
        this . responseCallback = callback;
    }

    public ArnoldMQTTCallback(T object, Callback<T, MqttMessage> callback)
    {
        this.object = object;
        this . java7Callback = callback;
    }

    @Override
    public void connectComplete(boolean reconnect, String serverURI)
    {
        Log.i(LOG_TAG, serverURI);
    }

    @Override
    public void connectionLost(Throwable cause)
    {
        Log.e(LOG_TAG, "Connection to MQTT Service Lost");
    }

    @Override
    public void messageArrived(String topic, MqttMessage message) throws Exception
    {
        // Log.i(LOG_TAG, message.toString());
        /*if (responseCallback != null)
        {
            this . responseCallback . accept(message);
        }
        */
        if (this.java7Callback != null)
        {
            this.java7Callback.accept(this.object, message);
        }
    }

    @Override
    public void deliveryComplete(IMqttDeliveryToken token)
    {

    }
}
