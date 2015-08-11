package com.example.sandvich;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.Random;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.Point;
import android.graphics.Rect;
import android.util.AttributeSet;
import android.util.Log;
import android.util.SparseArray;
import android.view.Display;
import android.view.MotionEvent;
import android.view.View;
import android.view.WindowManager;
import android.widget.Toast;

public class CirclesDrawingView extends View {

    private static final String TAG = "CirclesDrawingView";

    /** Main bitmap */
    private Bitmap mBitmap = null;

    private Rect mMeasuredRect;

    /** Stores data about single circle */
    private static class CircleArea {
        int radius;
        int centerX;
        int centerY;

        CircleArea(int centerX, int centerY, int radius) {
            this.radius = radius;
            this.centerX = centerX;
            this.centerY = centerY;
        }

        @Override
        public String toString() {
            return "Circle[" + centerX + ", " + centerY + ", " + radius + "]";
        }
    }

    /** Paint to draw circles */
    private Context context;
    
    private Paint mCirclePaint;
    
    private Paint mRectPaintLeft;
    
    private Paint mRectPaintRight;
    
    private String previousLeftSpeed = "";
    
    private String previousRightSpeed = "";

    private final Random mRadiusGenerator = new Random();
    // Radius limit in pixels
    private final static int RADIUS_LIMIT = 100;

    private static final int CIRCLES_LIMIT = 2;
    
    private static float SCREEN_WIDTH;
    
    private static float SCREEN_HEIGHT;

    /** All available circles */
    private HashSet<CircleArea> mCircles = new HashSet<CircleArea>(CIRCLES_LIMIT);
    private SparseArray<CircleArea> mCirclePointer = new SparseArray<CircleArea>(CIRCLES_LIMIT);

    /**
     * Default constructor
     *
     * @param ct {@link android.content.Context}
     */
    public CirclesDrawingView(final Context ct) {
        super(ct);

        init(ct);
    }

    public CirclesDrawingView(final Context ct, final AttributeSet attrs) {
        super(ct, attrs);

        init(ct);
    }

    public CirclesDrawingView(final Context ct, final AttributeSet attrs, final int defStyle) {
        super(ct, attrs, defStyle);

        init(ct);
    }

    private void init(final Context ct) {
        // Generate bitmap used for background
        // mBitmap = BitmapFactory.decodeResource(ct.getResources(), R.drawable.up_image);
    	
    	context = ct;
    	
        mCirclePaint = new Paint();

        mCirclePaint.setColor(Color.BLUE);
        mCirclePaint.setStrokeWidth(40);
        mCirclePaint.setStyle(Paint.Style.FILL);
        
        
        mRectPaintLeft = new Paint();
        mRectPaintLeft.setColor(Color.GREEN);
        mRectPaintLeft.setStrokeWidth(40);
        mRectPaintLeft.setStyle(Paint.Style.FILL);
        
        
        mRectPaintRight = new Paint();
        mRectPaintRight.setColor(Color.RED);
        mRectPaintRight.setStrokeWidth(40);
        mRectPaintRight.setStyle(Paint.Style.FILL);
        
        WindowManager wm = (WindowManager) ct.getSystemService(Context.WINDOW_SERVICE);
        Display display = wm.getDefaultDisplay();
        Point size = new Point();
        display.getSize(size);
        SCREEN_WIDTH = size.x;
        SCREEN_HEIGHT = size.y;
        
       CircleArea leftCircle = new CircleArea((int) (SCREEN_WIDTH / 4), (int) (SCREEN_HEIGHT / 2), RADIUS_LIMIT);
       CircleArea rightCircle = new CircleArea((int) (3 * SCREEN_WIDTH / 4), (int) (SCREEN_HEIGHT / 2), RADIUS_LIMIT);
       mCircles.add(leftCircle);
       mCircles.add(rightCircle);
    }

    @Override
    public void onDraw(final Canvas canv) {
        // background bitmap to cover all area
        // canv.drawBitmap(mBitmap, null, mMeasuredRect, null);
        canv.drawRect((SCREEN_WIDTH / 4) - 120, 0, (SCREEN_WIDTH / 4) + 120, SCREEN_HEIGHT, mRectPaintLeft);
        canv.drawRect((3 * SCREEN_WIDTH / 4) - 120, 0, (3 * SCREEN_WIDTH / 4) + 120, SCREEN_HEIGHT, mRectPaintRight);
        
        for (CircleArea circle : mCircles) {
            canv.drawCircle(circle.centerX, circle.centerY, circle.radius, mCirclePaint);
        }
        
        updateSpeed();

    }

    @Override
    public boolean onTouchEvent(final MotionEvent event) {
        boolean handled = false;

        CircleArea touchedCircle;
        int xTouch;
        int yTouch;
        int pointerId;
        int actionIndex = event.getActionIndex();

        // get touch event coordinates and make transparent circle from it
        switch (event.getActionMasked()) {
            case MotionEvent.ACTION_DOWN:
                // it's the first pointer, so clear all existing pointers data
                clearCirclePointer();

                xTouch = (int) event.getX(0);
                yTouch = (int) event.getY(0);

                // check if we've touched inside some circle
                touchedCircle = obtainTouchedCircle(xTouch, yTouch);
                if(touchedCircle != null) {
	                //touchedCircle.centerX = xTouch;
	                touchedCircle.centerY = yTouch;
	                mCirclePointer.put(event.getPointerId(0), touchedCircle);
                }

                invalidate();
                handled = true;
                break;

            case MotionEvent.ACTION_POINTER_DOWN:
                Log.w(TAG, "Pointer down");
                // It secondary pointers, so obtain their ids and check circles
                pointerId = event.getPointerId(actionIndex);

                xTouch = (int) event.getX(actionIndex);
                yTouch = (int) event.getY(actionIndex);

                // check if we've touched inside some circle
                touchedCircle = obtainTouchedCircle(xTouch, yTouch);
                
                if (touchedCircle != null) {
	                mCirclePointer.put(pointerId, touchedCircle);
	                //touchedCircle.centerX = xTouch;
	                touchedCircle.centerY = yTouch;
                }
                invalidate();
                handled = true;
                break;

            case MotionEvent.ACTION_MOVE:
                final int pointerCount = event.getPointerCount();

                Log.w(TAG, "Move");

                for (actionIndex = 0; actionIndex < pointerCount; actionIndex++) {
                    // Some pointer has moved, search it by pointer id
                    pointerId = event.getPointerId(actionIndex);

                    xTouch = (int) event.getX(actionIndex);
                    yTouch = (int) event.getY(actionIndex);

                    touchedCircle = mCirclePointer.get(pointerId);

                    if (null != touchedCircle) {
                        //touchedCircle.centerX = xTouch;
                        touchedCircle.centerY = yTouch;
                    }
                }
                invalidate();
                handled = true;
                break;

            case MotionEvent.ACTION_UP:
                clearCirclePointer();
                invalidate();
                handled = true;
                break;

            case MotionEvent.ACTION_POINTER_UP:
                // not general pointer was up
                pointerId = event.getPointerId(actionIndex);

                mCirclePointer.remove(pointerId);
                invalidate();
                handled = true;
                break;

            case MotionEvent.ACTION_CANCEL:
                handled = true;
                break;

            default:
                // do nothing
                break;
        }

        return super.onTouchEvent(event) || handled;
    }

    /**
     * Clears all CircleArea - pointer id relations
     */
    private void clearCirclePointer() {
        Log.w(TAG, "clearCirclePointer");

        mCirclePointer.clear();
    }

    /**
     * Search and creates new (if needed) circle based on touch area
     *
     * @param xTouch int x of touch
     * @param yTouch int y of touch
     *
     * @return obtained {@link CircleArea}
     */
    private CircleArea obtainTouchedCircle(final int xTouch, final int yTouch) {
        CircleArea touchedCircle = getTouchedCircle(xTouch, yTouch);

        /*
        if (null == touchedCircle) {
            touchedCircle = new CircleArea(xTouch, yTouch, RADIUS_LIMIT);

            if (mCircles.size() == CIRCLES_LIMIT) {
                Log.w(TAG, "Clear all circles, size is " + mCircles.size());
                // remove first circle
                mCircles.clear();
            }

            Log.w(TAG, "Added circle " + touchedCircle);
            mCircles.add(touchedCircle);
        }
        */

        return touchedCircle;
    }

    /**
     * Determines touched circle
     *
     * @param xTouch int x touch coordinate
     * @param yTouch int y touch coordinate
     *
     * @return {@link CircleArea} touched circle or null if no circle has been touched
     */
    private CircleArea getTouchedCircle(final int xTouch, final int yTouch) {
        CircleArea touched = null;

        for (CircleArea circle : mCircles) {
            if ((circle.centerX - xTouch) * (circle.centerX - xTouch) + (circle.centerY - yTouch) * (circle.centerY - yTouch) <= circle.radius * circle.radius) {
                touched = circle;
                break;
            }
        }

        return touched;
    }

    @Override
    protected void onMeasure(final int widthMeasureSpec, final int heightMeasureSpec) {
        super.onMeasure(widthMeasureSpec, heightMeasureSpec);

        mMeasuredRect = new Rect(0, 0, getMeasuredWidth(), getMeasuredHeight());
    }
    
    private void updateSpeed() {
    	CircleArea[] circles = mCircles.toArray(new CircleArea[mCircles.size()]);
    	String leftSpeed = circlePosToBits(circles[0].centerY);
    	String rightSpeed = circlePosToBits(circles[1].centerY);
    	boolean sendData = false;
    	
		if (!leftSpeed.equals(previousLeftSpeed)) {
			sendData = true;
			previousLeftSpeed = leftSpeed;
		}
		
		if (!rightSpeed.equals(previousRightSpeed)) {
			sendData = true;
			previousRightSpeed = rightSpeed;
		}
		
		if (sendData) {
			sendSpeedData (leftSpeed, rightSpeed);
		}
    }
    
    private void sendSpeedData(String leftData, String rightData) {
    	String data = "11" + leftData + rightData;
    	Log.v("Speed Update", data);
    	if (MainActivity.ipAddress.equals("") || MainActivity.port.equals("")) {
			// Tell user ip and/or port are invalid
			Toast.makeText(context, "The network configuration is not properly set", Toast.LENGTH_SHORT).show();
    	} else {
			Client client = new Client(MainActivity.ipAddress, Integer.parseInt(MainActivity.port));
			client.sendCommand(data);
    	}
    }
    
    private String circlePosToBits(float posY) {
    	int convertedPos = (int) (Math.floor(Math.abs( ( posY + (SCREEN_HEIGHT / 7) ) / (SCREEN_HEIGHT / 7))));
    	
    	switch (convertedPos) {
    	case 0:
    		return "111";
    	case 1:
    		return "111";
    	case 2:
    		return "110";
    	case 3:
    		return "101";
    	case 4:
    		return "100";
    	case 5:
    		return "011";
    	case 6:
    		return "010";
    	case 7:
    		return "001";
    	}
    	
    	return "000";
    }
}