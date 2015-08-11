package com.example.keyzoomv2;


import android.graphics.RectF;

public class Key {
	
	private String sLetter;
	private RectF sRect;
	
	public Key(String letter, RectF bounds)
	{
		sLetter = letter;
		sRect = bounds;
	}
	
	public Key()
	{
		
	}
	
	public boolean contains(float x, float y)
	{
		return sRect.contains(x, y);
	}
	

	public String getsLetter() {
		return sLetter;
	}

	public void setsLetter(String sLetter) {
		this.sLetter = sLetter;
	}

	public RectF getsRect() {
		return sRect;
	}

	public void setsRect(RectF sRect) {
		this.sRect = sRect;
	}
	
	@Override
	public String toString()
	{
		return sLetter;
	}


}
