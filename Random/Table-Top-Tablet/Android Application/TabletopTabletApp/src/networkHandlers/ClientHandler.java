package networkHandlers;

import java.net.*;
import java.io.*;
import java.util.*;

import android.content.Context;
import android.os.Environment;
import android.util.Log;

public class ClientHandler {
	Socket ClientSoc;
	DataInputStream din;
	DataOutputStream dout;
	BufferedReader br;

	public static void main(String[] args) throws Exception {
		ClientHandler fc = new ClientHandler(new Socket("127.0.0.1", 5217));
	}

	public ClientHandler(Socket soc) {
		try {
			ClientSoc = soc;
			din = new DataInputStream(ClientSoc.getInputStream());
			dout = new DataOutputStream(ClientSoc.getOutputStream());
			br = new BufferedReader(new InputStreamReader(System.in));
		} catch (Exception ex) {
		}
	}

	public void sendFile(String filename) throws Exception {
		dout.writeUTF("SEND");
		File f = new File(filename);
		if (!f.exists()) {
			System.out.println("File does not exist...");
			dout.writeUTF("File not found");
			return;
		}
		System.out.println(filename);
		dout.writeUTF(filename);

		String msgFromServer = din.readUTF();
		if (msgFromServer.compareTo("File Already Exists") == 0) {
			// TODO Add Android verification that we can overwrite file
			String Option = "Y";
			if (Option == "Y") {
				dout.writeUTF("Y");
			} else {
				dout.writeUTF("N");
				return;
			}
		}

		System.out.println("Sending File ...");
		FileInputStream fin = new FileInputStream(f);
		int ch;
		do {
			ch = fin.read();
			dout.writeUTF(String.valueOf(ch));
		} while (ch != -1);
		fin.close();
		System.out.println(din.readUTF());

	}

	public void receiveFile(String filename, Context context) {
		try {
			dout.writeUTF("GET");
            dout.writeUTF(filename);
            String msgFromServer = din.readUTF();
            if (msgFromServer.compareTo("File Not Found") == 0) {
                System.out.println("File not found on Server ...");
                return;
            } else if (msgFromServer.compareTo("READY") == 0) {
                System.out.println("Receiving File ...");
                File directory = new File("//sdcard//com.example.drawingfun//files//");
                directory.mkdirs();
                File f = new File("//sdcard//com.example.drawingfun//files//test.png");
                f.createNewFile();
                if (f.exists()) {
                    // TODO Add Android verification that we can overwrite file				
                    String Option = "Y";
                    if (Option == "N") {
                        dout.flush();
                        return;
                    }
                }
                FileOutputStream fout = new FileOutputStream("/sdcard/com.example.drawingfun/files/test.png");
                int ch;
                String temp;
                do {
                    temp = din.readUTF();
                    ch = Integer.parseInt(temp);
                    if (ch != -1) {
                        fout.write(ch);
                    }
                } while (ch != -1);
                fout.close();
                Log.d("Info", "Saved picture");
                System.out.println(din.readUTF());
            }
		} catch (IOException e) {
			e.printStackTrace();
			Log.d("Info", e.getMessage());
		}

	}
	
	public void disconnect() throws Exception {
		dout.writeUTF("DISCONNECT");
		System.exit(1);
	}
}