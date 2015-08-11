package networkHandlers;
import java.io.*;
import java.util.HashMap;

public class ServerMessage implements Serializable {

	protected static final long serialVersionUID = 1112122200L;
	
	private HashMap<String, Object> data;
	
	ServerMessage() {
	}
	
	ServerMessage(HashMap<String, Object> data) {
		this.data = data;
	}
	
	HashMap<String, Object> getData() {
		return data;
	}
	
	void setData(HashMap<String, Object> data) {
		this.data = data;
	}
}

