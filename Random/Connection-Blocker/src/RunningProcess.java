
public class RunningProcess {
	
	public String ipAddress;
	public int port;
	public String protocol;
	public String status;
	public int pid;
	
	public RunningProcess (String protocol, String ipAddress, int port, String status, int pid) {
		this.protocol = protocol;
		this.ipAddress = ipAddress;
		this.port = port;
		this.status = status;
		this.pid = pid;
	}
	
	public String toString() {
		return "Protocol: " + protocol + " | IP Address: " + ipAddress + " | Port: " + port + " | Status: " + status + " | PID: " + pid;
	}

}
