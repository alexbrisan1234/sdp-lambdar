package helpers;


import android.util.Log;
import static helpers.Constants.LOG_TAG;

import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallbackExtended;
import org.eclipse.paho.client.mqttv3.MqttMessage;

import java.util.function.Consumer;

public class ArnoldMQTTCallback implements MqttCallbackExtended
{
    private Consumer<MqttMessage> responseCallback;

    public ArnoldMQTTCallback() {}
    public ArnoldMQTTCallback(Consumer<MqttMessage> callback)
    {
        this . responseCallback = callback;
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
        Log.i(LOG_TAG, message.toString());
        if (responseCallback != null)
        {
            this . responseCallback . accept(message);
        }
    }

    @Override
    public void deliveryComplete(IMqttDeliveryToken token)
    {

    }
}
