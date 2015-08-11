package networkHandlers;

import java.net.*;
import java.io.*;
import java.util.*;

public class ServerHandler {
	public static String SERVER_ROOT;

	public static ArrayList<Student> connectedClients = new ArrayList<Student>();
	
	public ServerHandler(String serverRoot) {
		ServerHandler.SERVER_ROOT = serverRoot;
	}
	
	public void handleNewClient(Socket socket) {
		new transferFile(socket);
	}

	public static void main(String args[]) throws Exception {
		SERVER_ROOT = "ServerFiles//";
		ServerSocket soc = new ServerSocket(5217);
		System.out.println("FTP Server Started on Port Number 5217");
		while (true) {
			System.out.println("Waiting for Connection ...");
			new transferFile(soc.accept());
		}
	}
}

class transferFile extends Thread {
	Socket ClientSoc;
	DataInputStream din;
	DataOutputStream dout;
	int connectionId;

	transferFile(Socket soc) {
		try {
			ClientSoc = soc;
			din = new DataInputStream(ClientSoc.getInputStream());
			dout = new DataOutputStream(ClientSoc.getOutputStream());
			addToServerList();
			System.out.println("FTP Client Connected ...");
			start();
		} catch (Exception ex) {
		}
	}

	void SendFile() throws Exception {
		String filename = din.readUTF();
		System.out.println(ServerHandler.SERVER_ROOT + filename);
		File f = new File(ServerHandler.SERVER_ROOT + filename);
		if (!f.exists()) {
			dout.writeUTF("File Not Found");
			return;
		} else {
			dout.writeUTF("READY");
			FileInputStream fin = new FileInputStream(f);
			int ch;
			do {
				ch = fin.read();
				dout.writeUTF(String.valueOf(ch));
			} while (ch != -1);
			fin.close();
			dout.writeUTF("File Receive Successfully");
		}
	}

	void ReceiveFile() throws Exception {
		String filename = din.readUTF();
		if (filename.compareTo("File not found") == 0) {
			return;
		}
		File f = new File(ServerHandler.SERVER_ROOT + filename);
		String option;

		if (f.exists()) {
			dout.writeUTF("File Already Exists");
			option = din.readUTF();
		} else {
			dout.writeUTF("SendFile");
			option = "Y";
		}

		if (option.compareTo("Y") == 0) {
			FileOutputStream fout = new FileOutputStream(f);
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
			dout.writeUTF("File Send Successfully");
		} else {
			return;
		}

	}

	public synchronized void addToServerList() {
		if (ServerHandler.connectedClients.add(new Student(ClientSoc.getInetAddress().toString(), "Default Student", -1))) {
			connectionId = ServerHandler.connectedClients.size() - 1;
		}
		System.out.println(ServerHandler.connectedClients);
	}

	public synchronized void removeFromServerList() {
		ServerHandler.connectedClients.remove(connectionId);
	}

	public void run() {
		while (true) {
			try {
				System.out.println("Waiting for Command ...");
				String Command = din.readUTF();
				if (Command.compareTo("GET") == 0) {
					System.out.println("\tGET Command Received ...");
					SendFile();
					continue;
				} else if (Command.compareTo("SEND") == 0) {
					System.out.println("\tSEND Command Receiced ...");
					ReceiveFile();
					continue;
				} else if (Command.compareTo("DISCONNECT") == 0) {
					System.out.println("\tDisconnect Command Received ...");
					System.exit(1);
				}
			} catch (Exception ex) {
				System.err.println(ex);
				System.out.println("[-] Client disconnected abruptly");
				break;
			}
		}
		removeFromServerList();
	}
}