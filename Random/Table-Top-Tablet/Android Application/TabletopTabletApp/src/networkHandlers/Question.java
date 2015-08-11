package networkHandlers;
import java.util.ArrayList;

public class Question {
	
	String question;
	String type;
	ArrayList<String> options;
	int userAnswer;
	int answer;
	int[] answers;
	
	public Question(String question, ArrayList<String> options, String type) {
		this.question = question;
		this.options = options;
		this.type = type;
	}
	
	public Question(String question, ArrayList<String> options, int correctAnswerIndex, String type) {
		this.question = question;
		this.options = options;
		this.answer = correctAnswerIndex;
		this.type = type;
	}
	
	public Question(String question, ArrayList<String> options, int[] correctAnswers, String type) {
		this.question = question;
		this.options = options;
		this.answers = correctAnswers;
		this.type = type;
	}

	public int getUserAnswer() {
		return userAnswer;
	}

	public void setUserAnswer(int userAnswer) {
		this.userAnswer = userAnswer;
	}

	public String getquestion() {
		return question;
	}

	public ArrayList<String> getOptions() {
		return options;
	}

	public int getCorrectAnswer() {
		return answer;
	}
	
	

}
