//package com.example.keyzoomv2;
//
//import android.os.Bundle;
//import android.app.Activity;
//import android.view.Menu;
//
//public class ChangePort extends Activity {
//
//	@Override
//	protected void onCreate(Bundle savedInstanceState) {
//		super.onCreate(savedInstanceState);
//		setContentView(R.layout.activity_change_port);
//	}
//
//	@Override
//	public boolean onCreateOptionsMenu(Menu menu) {
//		// Inflate the menu; this adds items to the action bar if it is present.
//		getMenuInflater().inflate(R.menu.activity_change_port, menu);
//		return true;
//	}
//
//}

package com.example.keyzoomv2;

import android.os.Bundle;
import android.app.Activity;
import android.content.Context;
import android.view.Menu;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

public class ChangePort extends Activity {

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_change_port);
		
		EditText editText = (EditText) findViewById(R.id.editText1);
		editText.setText(MainActivity.Port + "");
		
		Button buttonOne = (Button) findViewById(R.id.button2);
		buttonOne.setOnClickListener(new Button.OnClickListener() {
			@Override
			public void onClick(View arg0) {
				EditText editText = (EditText) findViewById(R.id.editText1);
				String IP3 = editText.getText().toString();
				try{
				MainActivity.Port = Integer.parseInt(IP3);
				MainActivity.s = new Server(MainActivity.IP,MainActivity.Port);
				finish();
				}catch(Exception e)
				{
					Context context = getApplicationContext();
					CharSequence text = "Invalid number, try again";
					int duration = Toast.LENGTH_SHORT;

					Toast toast = Toast.makeText(context, text, duration);
					toast.show();
				}
			}
		});
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.activity_change_port, menu);
		return true;
	}

}
