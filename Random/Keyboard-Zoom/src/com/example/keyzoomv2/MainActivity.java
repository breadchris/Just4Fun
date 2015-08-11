package com.example.keyzoomv2;

import java.io.BufferedWriter;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;

import android.app.Activity;
import android.content.Intent;
import android.content.pm.ActivityInfo;
import android.gesture.GestureOverlayView;
import android.graphics.*;
import android.media.AudioManager;
import android.media.SoundPool;
import android.media.SoundPool.OnLoadCompleteListener;
import android.os.Bundle;
import android.util.*;
import android.view.*;
import android.view.animation.Animation;
import android.view.animation.AnimationUtils;
import android.widget.ImageView;

public class MainActivity extends Activity implements
		android.view.GestureDetector.OnGestureListener {
	private static final String TAG = "Touch";
	@SuppressWarnings("unused")
	private static final float MIN_ZOOM = 1f, MAX_ZOOM = 1f;

	// These matrices will be used to scale points of the image
	public static Matrix matrix = new Matrix();
	Matrix savedMatrix = new Matrix();

	// The 3 states (events) which the user is trying to perform
	static final int NONE = 0;
	static final int DRAG = 1;
	static final int ZOOM = 2;
	int mode = NONE;

	private GestureDetector gestureScanner;
	private Keys keys;
	public static Server s;
	public static String IP;
	public static int Port;
	public static float zoom;
	private boolean zoomed;

	private int boundaryLeft = 0;
	private int boundaryRight = 0;
	private int boundaryTop = 0;
	private int boundaryBottom = 0;

	// these PointF objects are used to record the point(s) the user is touching
	PointF start = new PointF();
	PointF mid = new PointF();
	float oldDist = 1f;
	private RectF displayRect;
	private SoundPool soundPool;
	private boolean loaded;
	private int soundID;

	/** Called when the activity is first created. */

	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		this.requestWindowFeature(Window.FEATURE_NO_TITLE);
		
		// Setting up Server and Keys
		IP = "10.0.0.10";
		Port = 11113;
		s = new Server(IP, Port);
		
		//Setting Gesture Detector
		gestureScanner = new GestureDetector(this);

		// Formatting the screen
		this.getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN,
				WindowManager.LayoutParams.FLAG_FULLSCREEN);
		this.setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE);
		setContentView(R.layout.activity_main);
		//Getting imageView
		ImageView view = (ImageView) findViewById(R.id.imageView);
		view.setScaleType(ImageView.ScaleType.MATRIX);
		
		setUp();
		view.setImageMatrix(matrix);
		
		final Animation animRotate = AnimationUtils.loadAnimation(this, R.anim.start);
		view.startAnimation(animRotate);
		
		displayRect = new RectF();
		displayRect.set(0, 0, boundaryRight, boundaryBottom);
		
	    this.setVolumeControlStream(AudioManager.STREAM_MUSIC);
	    // Load the sound
	    soundPool = new SoundPool(10, AudioManager.STREAM_MUSIC, 0);
	    soundPool.setOnLoadCompleteListener(new OnLoadCompleteListener() {
	     

		@Override
	      public void onLoadComplete(SoundPool soundPool, int sampleId,
	          int status) {
	        loaded = true;
	      }
	    });
	    soundID = soundPool.load(this, R.raw.click, 1);
		
		
	}
	
	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
	    MenuInflater inflater = getMenuInflater();
	    inflater.inflate(R.menu.activity_menu, menu);
	    return true;
	}
	
	@Override
	public boolean onOptionsItemSelected(MenuItem item) {
	    switch (item.getItemId()) {
	        case R.id.Change_IP:
	        	Intent intent = new Intent(this, ChangeIP.class);
	            startActivity(intent);
	            return true;
	        case R.id.Change_Port:
	        	Intent intent2 = new Intent(this, ChangePort.class);
	            startActivity(intent2);
	            return true;
	        case R.id.ChangeZoom:
	        	Intent intent3 = new Intent(this, ChangeZoom.class);
	            startActivity(intent3);
	            return true;    
	        
	        case R.id.EndServer:
			
			try {
				Socket socket = new Socket(IP,Port);
				PrintWriter out = new PrintWriter(new BufferedWriter(new OutputStreamWriter(socket.getOutputStream())), true);
				out.println("en");
				return true;
			} catch (UnknownHostException e) {
				return false;
			} catch (IOException e) {
				return false;
			}
	            
	            
	    }
		return true;
	}

	private void setUp() {
		DisplayMetrics displaymetrics = new DisplayMetrics();
		getWindowManager().getDefaultDisplay().getMetrics(displaymetrics);

		boundaryBottom = displaymetrics.heightPixels;
		boundaryRight = displaymetrics.widthPixels;
		
		zoom = 3f;
		
		Log.d("Info", boundaryRight + ", " + boundaryBottom);
		
		keys = new Keys(boundaryRight, boundaryBottom);
		matrix.postScale(1f, 1f);

	}

	@Override
	public boolean onTouchEvent(MotionEvent me) {
		return gestureScanner.onTouchEvent(me);
	}

	public boolean checkKey(float x, float y) throws UnknownHostException, IOException {

		final String key = keys.getKeyPressed(x, y);
		if (key != null) {
			Log.d("ClientActiviy", key);
			sendKey(key);
			click();
    		ImageView view = (ImageView) findViewById(R.id.imageView);
    		view.setScaleType(ImageView.ScaleType.MATRIX);
    		matrix.setScale(1f, 1f);
    		view.setImageMatrix(matrix);
    		zoomed = false;
		}

		return false;
	}
	
	private void sendKey(final String key)
	{
		Thread send = new Thread(new Runnable(){
		    @Override
		    public void run()
		    {
				
					try {
						Socket socket = new Socket(IP,Port);
						PrintWriter out = new PrintWriter(new BufferedWriter(new OutputStreamWriter(socket.getOutputStream())), true);
						 out.println(key);
					} catch (UnknownHostException e) {
						// TODO Auto-generated catch block
						e.printStackTrace();
					} catch (IOException e) {
						// TODO Auto-generated catch block
						e.printStackTrace();
					}
	           
		    }
		});

		send.start();
	}
	
	private void click()
	{
	      AudioManager audioManager = (AudioManager) getSystemService(AUDIO_SERVICE);
	      float actualVolume = audioManager
	          .getStreamVolume(AudioManager.STREAM_MUSIC);
	      float maxVolume = audioManager
	          .getStreamMaxVolume(AudioManager.STREAM_MUSIC);
	      float volume = actualVolume / maxVolume;
	      // Is the sound loaded already?
	      if (loaded) {
	        soundPool.play(soundID, volume, volume, 1, 0, 1f);
	        Log.e("Test", "Played sound");
	      }
		Log.d("Info", "click");

	}

	private void adjustPan() {
		float[] matrixValues = new float[9];
		matrix.getValues(matrixValues);
		float currentY = matrixValues[Matrix.MTRANS_Y];
		float currentX = matrixValues[Matrix.MTRANS_X];
		float currentScale = matrixValues[Matrix.MSCALE_X];
		float currentHeight = boundaryBottom * currentScale;
		float currentWidth = boundaryRight * currentScale;
		float newX = currentX;
		float newY = currentY;

		RectF drawingRect = new RectF(newX, newY, newX + currentWidth, newY
				+ currentHeight);
		float diffUp = Math.min(displayRect.bottom - drawingRect.bottom,
				displayRect.top - drawingRect.top);
		float diffDown = Math.max(displayRect.bottom - drawingRect.bottom,
				displayRect.top - drawingRect.top);
		float diffLeft = Math.min(displayRect.left - drawingRect.left,
				displayRect.right - drawingRect.right);
		float diffRight = Math.max(displayRect.left - drawingRect.left,
				displayRect.right - drawingRect.right);

		float x = 0, y = 0;

		if (diffUp > 0)
			y += diffUp;
		if (diffDown < 0)
			y += diffDown;
		if (diffLeft > 0)
			x += diffLeft;
		if (diffRight < 0)
			x += diffRight;

		if (currentWidth < displayRect.width())
			x = -currentX + (displayRect.width() - currentWidth) / 2;
		if (currentHeight < displayRect.height())
			y = -currentY + (displayRect.height() - currentHeight) / 2;

		matrix.postTranslate(x, y);
	}

	private float spacing(MotionEvent event) {
		float x = event.getX(0) - event.getX(1);
		float y = event.getY(0) - event.getY(1);
		return FloatMath.sqrt(x * x + y * y);
	}

	private void midPoint(PointF point, MotionEvent event) {
		float x = event.getX(0) + event.getX(1);
		float y = event.getY(0) + event.getY(1);
		point.set(x / 2, y / 2);
	}

	public void onGesture(GestureOverlayView overlay, MotionEvent event) {
		// TODO Auto-generated method stub

	}

	public void onGestureCancelled(GestureOverlayView overlay, MotionEvent event) {
		// TODO Auto-generated method stub

	}

	public void onGestureEnded(GestureOverlayView overlay, MotionEvent event) {
		// TODO Auto-generated method stub

	}

	public void onGestureStarted(GestureOverlayView overlay, MotionEvent event) {
		// TODO Auto-generated method stub

	}

	@Override
	public boolean onDown(MotionEvent event) {

		return false;
	}

	@Override
	public boolean onFling(MotionEvent e1, MotionEvent e2, float velocityX,
			float velocityY) {
		
		return false;
	}

	@Override
	public void onLongPress(MotionEvent event) {
		ImageView image = (ImageView) findViewById(R.id.imageView);
		Log.d("Info", "Long Press");
		
		matrix.set(savedMatrix);

		float[] values = new float[9];
		matrix.getValues(values);

		if (!zoomed)
		{
			matrix.postScale(zoom,zoom, event.getX(), event.getY());
			zoomed = true;
		}
		else
		{
			matrix.setScale(1f, 1f);
			zoomed = false;
		}
		
		image.setImageMatrix(matrix);
		

	}

	@Override
	public boolean onScroll(MotionEvent e1, MotionEvent e2, float distanceX,
			float distanceY) {
		if(zoomed)
		{
		ImageView image = (ImageView) findViewById(R.id.imageView);
		matrix.postTranslate(-distanceX,  -distanceY);
		adjustPan();
		image.setImageMatrix(matrix);
		}
		return false;
	}

	@Override
	public void onShowPress(MotionEvent e) {
		// TODO Auto-generated method stub

	}

	@Override
	public boolean onSingleTapUp(MotionEvent event) {
		try {
            float[] matrixValues = new float[9];
            matrix.getValues(matrixValues);
            float currentY = event.getY();
            float currentX = event.getX();
            float cornerY = matrixValues[Matrix.MTRANS_Y];
            float cornerX = matrixValues[Matrix.MTRANS_X];
            float currentScale = matrixValues[Matrix.MSCALE_X];
            checkKey(((currentX - cornerX)/ currentScale), ((currentY-cornerY)/currentScale));
		} catch (UnknownHostException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		} catch (IOException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}
		return true;
	}

}