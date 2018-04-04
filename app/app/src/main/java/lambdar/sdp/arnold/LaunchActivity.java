package lambdar.sdp.arnold;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;

public class LaunchActivity extends Activity
{

    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_launch);
    }

    public void featuresClicked(View view)
    {
        Intent move_to_features = new Intent(this, MainActivity.class);
        startActivity(move_to_features);
    }

    public void storyClicked(View view)
    {
        Intent move_to_features = new Intent(this, StoryActivity.class);
        startActivity(move_to_features);
    }

    public void instructionsClicked(View view)
    {
        Intent move_to_features = new Intent(this, InstructionsActivity.class);
        startActivity(move_to_features);
    }
}
