package networkHandlers;

import java.io.*;
import java.util.HashMap;
/*
 * This class defines the different type of messages that will be exchanged between the
 * Clients and the Server. 
 * When talking from a Java Client to a Java Server a lot easier to pass Java objects, no 
 * need to count bytes or to wait for a line feed at the end of the frame
 */
public class ClientMessage implements Serializable {

	protected static final long serialVersionUID = 1112122200L;
	
	private HashMap<String, Object> data;

	public static enum Action {
		LOGIN, LOGOUT, REGISTER, MESSAGE, UPDATE_QUESTIONS, WHOISIN, PICTURE
	}
	private Action action;
	static final int WHOISIN = 0, MESSAGE = 1, LOGOUT = 2;
	private int type;
	private String message;
	
	// constructor
	ClientMessage(int type, String message) {
		this.type = type;
		this.message = message;
	}
	
	ClientMessage(Action action, HashMap<String, Object> data) {
		this.action = action;
		this.data = data;
	}
	
	Action getAction() {
		return action;
	}
	String getMessage() {
		return message;
	}
	
	HashMap<String, Object> getData() {
		return data;
	}
}

