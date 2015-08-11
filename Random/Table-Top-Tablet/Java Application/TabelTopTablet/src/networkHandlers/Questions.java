package networkHandlers;

import java.io.File;
import java.util.ArrayList;

public class Questions {
	public ArrayList<Question> questions;

	public Questions() {
		questions = new ArrayList<Question>();
	}
	
	public void addQuestion(String title, String location) {
		questions.add(new Question(title, location));
	}

	public String toString() {
		String output = "";
		for (int i = 0; i < questions.size(); i++) {
			Question question = questions.get(i);
			output += "Index: [" + i + "], Title: " + question.getTitle() + ", Location: " + question.getLocation() + "\n";
		}
		return output;
	}
	
	public class Question {
		private String title;
		private String location;
		
		public Question(String title, String folder) {
			this.title = title;
			this.location = folder;
		}
		
		public String getTitle() {
			return title;
		}
		
		public String getLocation() {
			return location;
		}
		
	}
}


