package com.example.sandvich;

import android.os.Bundle;
import android.app.Activity;
import android.content.Intent;
import android.util.Log;
import android.view.Menu;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.RadioButton;
import android.widget.RadioGroup;
import android.widget.Toast;

public class MakeSandwich extends Activity {
	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_make_sandwich);
		
		RadioGroup breadGroup = (RadioGroup) findViewById(R.id.breadGroup);
		final RadioButton whiteButton = (RadioButton) findViewById(R.id.whiteButton);
		final RadioButton ryeButton = (RadioButton) findViewById(R.id.ryeButton);
		final RadioButton wheatButton = (RadioButton) findViewById(R.id.wheatButton);
		final CheckBox roastBeefButton = (CheckBox) findViewById(R.id.roastBeefButton);
		final CheckBox veggieBurgerButton = (CheckBox) findViewById(R.id.veggieBurgerButton);
		final CheckBox turkeyButton = (CheckBox) findViewById(R.id.turkeyButton);
		final CheckBox lettuceButton = (CheckBox) findViewById(R.id.lettuceButton);
		final CheckBox tomatoButton = (CheckBox) findViewById(R.id.tomatoButton);
		Button submitButton = (Button) findViewById(R.id.submitButton);
		
		submitButton.setOnClickListener(new Button.OnClickListener() {
			@Override
			public void onClick(View arg0) {
				int[] data = new int[8];
				data[0] = 0;
				if(whiteButton.isChecked()) {
					data[1] = 0;
					data[2] = 1;
				} else if(wheatButton.isChecked()) {
					data[1] = 1;
					data[2] = 0;
				} else if(ryeButton.isChecked()) {
					data[1] = 1;
					data[2] = 1;
				} else {
					Log.v("Error", "A type of bread must be picked");
				}
					
				if(roastBeefButton.isChecked())
					data[3] = 1;
				else
					data[3] = 0;
				
				if(veggieBurgerButton.isChecked())
					data[4] = 1;
				else
					data[4] = 0;
				
				if(turkeyButton.isChecked())
					data[5] = 1;
				else
					data[5] = 0;
				
				if(lettuceButton.isChecked())
					data[6] = 1;
				else
					data[6] = 0;
				
				if(tomatoButton.isChecked())
					data[7] = 1;
				else
					data[7] = 0;
				
				String dataString = "";
				for(int value: data) {
					dataString += value;
				}
				
				Log.v("Data value", dataString);
				
				if (MainActivity.ipAddress.equals("") || MainActivity.port.equals("")) {
					// Tell user ip and/or port are invalid
					Toast.makeText(getApplicationContext(), "The network configuration is not properly set", Toast.LENGTH_SHORT).show();
				} else {
					Client client = new Client(MainActivity.ipAddress, Integer.parseInt(MainActivity.port));
					client.sendCommand(dataString);
					Toast.makeText(getApplicationContext(), "Your order was placed successfully", Toast.LENGTH_SHORT).show();
				}
			}
		});
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.make_sandwich, menu);
		return true;
	}

}
