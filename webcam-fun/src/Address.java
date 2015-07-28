
public class Address {
	
	private String hostType;
	private String IPAddress;
	
	public Address(String IPAddress) {
		this.IPAddress = IPAddress;
	}
	
	public void setHostType(String hostType) {
		this.hostType = hostType;
	}
	
	public String getIPAddress() {
		return IPAddress;
	}
	
	public String toString() {
		return "IPAddress: " + IPAddress + "Host type: " + hostType;
	}
	
}
