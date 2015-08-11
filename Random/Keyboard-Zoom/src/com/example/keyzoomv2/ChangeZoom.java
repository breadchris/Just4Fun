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
import android.graphics.Matrix;
import android.view.Menu;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.Toast;

public class ChangeZoom extends Activity {
	
	private boolean zoomed;

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_change_zoom);
		
		EditText editText = (EditText) findViewById(R.id.editText3);
		editText.setText(MainActivity.zoom + "");
		
		final Matrix matrix = MainActivity.matrix;
		final ImageView view = (ImageView) findViewById(R.id.zoomImage);
		view.setScaleType(ImageView.ScaleType.MATRIX);
		view.setImageMatrix(matrix);
		
		Button buttonOne = (Button) findViewById(R.id.button4);
		buttonOne.setOnClickListener(new Button.OnClickListener() {
			@Override
			public void onClick(View arg0) {
				EditText editText = (EditText) findViewById(R.id.editText3);
				String zM = editText.getText().toString();
				try{
						MainActivity.zoom = Float.parseFloat(zM);
						matrix.setScale(MainActivity.zoom, MainActivity.zoom);
						view.setImageMatrix(matrix);
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
		
		Button buttonTwo = (Button) findViewById(R.id.button5);
		buttonTwo.setOnClickListener(new Button.OnClickListener() {
			@Override
			public void onClick(View arg0) {
				finish();
			}
		});
		
		
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.activity_change_zoom, menu);
		return true;
	}

}
