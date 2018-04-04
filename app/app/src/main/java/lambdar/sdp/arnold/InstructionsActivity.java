package lambdar.sdp.arnold;

import android.app.Activity;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import java.util.ArrayList;
import java.util.List;

public class InstructionsActivity extends Activity
{

    private RecyclerView wordlistView;
    private RecyclerView.Adapter wAdapter;
    private RecyclerView.LayoutManager wLayoutManager;


    static class Instructions
    {
        String title;
        String content;

        public Instructions(String title, String content)
        {
            this.title = title;
            this.content = content;
        }
    }

    private static class WordlistAdapter extends RecyclerView.Adapter<WordlistAdapter.ViewHolder>
    {

        private List<Instructions> dataset;

        class ViewHolder extends RecyclerView.ViewHolder
        {
            String string;
            TextView instructionName;
            TextView instruction;

            ViewHolder(View v)
            {
                super(v);
                this . instructionName = v . findViewById(R . id . instruction_category);
                this . instruction = v . findViewById(R . id . instruction_text);
            }

            void setInstructionName(String text)
            {
                this . instructionName . setText(text);
            }

            void setContent(String text)
            {
                this . instruction . setText(text);
            }
        }

        public WordlistAdapter(List<Instructions> gw)
        {
            this . dataset = gw;
        }

        @Override
        public WordlistAdapter.ViewHolder onCreateViewHolder(ViewGroup parent, int viewType)
        {
            View v = LayoutInflater.from(parent.getContext())
                    .inflate(R.layout.instructions_card, parent, false);
            return new ViewHolder(v);
        }

        @Override
        public void onBindViewHolder(final WordlistAdapter.ViewHolder holder, int position)
        {
            Instructions card_at_position = this . dataset . get(position);

            holder.setInstructionName(card_at_position.title);
            holder.setContent(card_at_position.content);

        }

        @Override
        public int getItemCount()
        {
            return this . dataset . size();
        }
    }

    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_instructions);

        List<Instructions> options = new ArrayList<>();


        options.add(new Instructions(
                "Follow",
                "Turns on Arnold. This enables both the following and avoiding obstacles features. To make the robot stop simply disable the function."
        ));

        options.add(new Instructions(
                "Out Of Range",
                "Enable the out of range alarm. An alarm goes off and you receive a notification whenever Arnold loses the signal."
        ));

        options.add(new Instructions(
                "Lock",
                "Enable the anti-theft system. An alarm goes off and you receive a notification whenever Arnold’s lid is open."
        ));

        options.add(new Instructions(
                "Notifications",
                "Enable/disable receiving notifications for the previous two features. This option does not affect the functionality of the alarm on the robot."
        ));

        wordlistView = (RecyclerView) findViewById(R.id.instructions_recycler_view);
        wordlistView . setHasFixedSize(true);

        wLayoutManager = new LinearLayoutManager(this);
        wordlistView.setLayoutManager(wLayoutManager);

        wAdapter = new WordlistAdapter(options);
        wordlistView . setAdapter(wAdapter);
    }
}
