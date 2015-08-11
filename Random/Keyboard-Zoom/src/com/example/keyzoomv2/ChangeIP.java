package com.example.keyzoomv2;

import java.util.MissingFormatArgumentException;
import android.os.Bundle;
import android.app.Activity;
import android.content.Intent;
import android.view.Menu;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

public class ChangeIP extends Activity {

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_change_ip);
		
		EditText editText = (EditText) findViewById(R.id.IPText);
		editText.setText(MainActivity.IP);
		
		Button buttonOne = (Button) findViewById(R.id.button1);
		
		buttonOne.setOnClickListener(new Button.OnClickListener() {
			@Override
			public void onClick(View arg0) {
				EditText editText = (EditText) findViewById(R.id.IPText);
				String IP2 = editText.getText().toString();
				MainActivity.IP = IP2;
				MainActivity.s = new Server(MainActivity.IP,MainActivity.Port);
				finish();
			}
		});
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.activity_change_ip, menu);
		return true;
	}

}
