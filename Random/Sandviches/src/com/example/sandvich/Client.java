package com.example.sandvich;

import java.io.BufferedWriter;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.InetAddress;
import java.net.Socket;
import android.os.Handler;
import android.util.Log;

public class Client {

    private String serverIpAddress = "";
    
    private int myPort;

    private boolean connected = false;

    private Handler handler = new Handler();

    public Client(String ip, int port)
    {
    	serverIpAddress = ip;
    	myPort = port;
    }
    
    public void sendCommand(String command)
    {
        Thread cThread = new Thread(new ClientThread(command));
        cThread.start();
    }

    public class ClientThread implements Runnable {
    	
    	private String command;
    	
    	public ClientThread(String command)
    	{
    		this.command = command;
    	}

        @Override
		public void run() {
            try {
                InetAddress serverAddr = InetAddress.getByName(serverIpAddress);
                Log.d("ClientActivity", "C: Connecting...");
                Socket socket = new Socket(serverAddr, myPort);
                try {
                    Log.d("ClientActivity", "C: Sending command.");
                    PrintWriter out = new PrintWriter(new BufferedWriter(new OutputStreamWriter(socket
                                .getOutputStream())), true);
                        out.println(this.command);
                        Log.d("ClientActivity", "C: Sent: " + command);
                } catch (Exception e) {
                    Log.e("ClientActivity", "S: Error", e);
                }
                socket.close();
                Log.d("ClientActivity", "C: Closed.");
            } catch (Exception e) {
                Log.e("ClientActivity", "C: Error", e);
                connected = false;
            }
        }
    }
}