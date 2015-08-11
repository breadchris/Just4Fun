package com.example.keyzoomv2;

import java.util.*;
import android.graphics.RectF;

public class Keys {
	
	private ArrayList<Key> keys;
	
	public Keys(int screenWidth, int screenHeight)
	{
		keys = new ArrayList<Key>();
		String[] letters = {"0","1", "2", "3", "4", "5", "6", "7", "8", "9", "Q", "W", "E", "R", "T", "Y", "U", "I"
				, "O", "P", "A", "S", "D", "F", "G", "H", "J", "K", "L", "del", "Z", "X", "C", "V", "B", "N", "M", "."
				, ",", "?", "up", "space", "enter", "'"};
		int[] startX = new int[10];
		int[] endX = new int[10];
		int[] startY = new int[5];
		int[] endY = new int[5];
		
		int cellWidthDistance = screenWidth / 10;
		int cellHeightDistance = screenHeight / 5;
		double percentToStartX = .05;
		double percentToEndX = .95;
		double percentToStartY = .1;
		double percentToEndY = .90;
		int extraStartX = (int) (cellWidthDistance * percentToStartX);
		int extraEndX = (int) (cellWidthDistance * percentToEndX);
		int extraStartY = (int) (cellHeightDistance * percentToStartY);
		int extraEndY = (int) (cellHeightDistance * percentToEndY);
		
		for(int i = 0; i < startX.length; i++)
		{
			startX[i] = i*cellWidthDistance + extraStartX;
		}
		
		for(int i = 0; i < endX.length; i++)
		{
			endX[i] = i*cellWidthDistance + extraEndX;
		}
		
		for(int i = 0; i < startY.length; i++)
		{
			startY[i] = i*cellHeightDistance + extraStartY;
		}
		
		for(int i = 0; i < endY.length; i++)
		{
			endY[i] = i*cellHeightDistance + extraEndY;
		}
		
		int i = 0;
		for(int r = 0; r < 4; r++)
		{
			for(int c = 0; c < 10; c++)
			{
				keys.add(new Key(letters[i], new RectF(startX[c], startY[r], endX[c], endY[r])));
				i++;
			}
		}
											//Startx		StartY		EndX		EndY
		keys.add (new Key("enter", 	new RectF(startX[7],	startY[4],	endX[8],	endY[4])));
		keys.add (new Key("'", 		new RectF(startX[9],	startY[4],	endX[9],	endY[4])));
		keys.add (new Key("space", 	new RectF(startX[1],	startY[4],	endX[6],	endY[4])));
		keys.add (new Key("up", 	new RectF(startX[0],	startY[4],	endX[0],	endY[4])));

	}

	public ArrayList<Key> getKeys()
    {
    	return keys;
    }
    
    public String getKeyPressed(float x, float y)
    {
    	Key k;
    	for(int i = 0; i < keys.size(); i++)
    	{
    		k = keys.get(i);
    		if(k.getsRect().contains(x,y)){
    			return k.getsLetter();
    		}
    	}
    	
		return null;
    }

}
