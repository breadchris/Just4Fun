package networkHandlers;
public class Student {
	int id;
	public String name;
	public String ip;
	String hostname;

	public Student(String ip, String name, int id) {
		this.name = name;
		this.ip = ip;
		this.hostname = hostname;
		this.id = id;
	}
}
