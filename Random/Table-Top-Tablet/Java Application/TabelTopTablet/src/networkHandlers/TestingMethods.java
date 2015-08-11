package networkHandlers;

import java.io.IOException;


public class TestingMethods {
	
	public static void main(String[] args) {
		TeacherServer tS = new TeacherServer("ServerFiles\\", "questions.conf");
		System.out.println(tS.getQuestions().toString());
	}

}
