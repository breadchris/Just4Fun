package com.example.sandvich;

import java.io.BufferedWriter;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;
import com.example.sandvich.R;
import com.example.sandvich.MakeSandwich;
import com.example.sandvich.Drive;
import android.os.Bundle;
import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.Toast;

public class MainActivity extends Activity {
	
	public static String ipAddress = "192.168.1.4";
	public static String port = "55555";

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
		
		Button makeSandwichButton = (Button) findViewById(R.id.makeSandwichButton);
		Button deliverFoodButton = (Button) findViewById(R.id.deliverFoodButton);
		
		makeSandwichButton.setOnClickListener(new Button.OnClickListener() {
			@Override
			public void onClick(View arg0) {
	        	Intent intent = new Intent(MainActivity.this, MakeSandwich.class);
	            startActivity(intent);
			}
		});
		
		deliverFoodButton.setOnClickListener(new Button.OnClickListener() {
			@Override
			public void onClick(View arg0) {
	        	Intent intent = new Intent(MainActivity.this, Drive.class);
	            startActivity(intent);
			}
		});
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.main, menu);
		return true;
	}
	
	@Override
	public boolean onOptionsItemSelected(MenuItem item) {
	    switch (item.getItemId()) {
	        case R.id.action_settings:
	        	Intent intent = new Intent(this, Settings.class);
	            startActivity(intent);
	            return true;    
	    }
		return true;
	}

}
