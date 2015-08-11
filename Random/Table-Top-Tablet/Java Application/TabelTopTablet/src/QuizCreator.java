import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;

import networkHandlers.Question;

import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

import com.google.gson.Gson;


public class QuizCreator {
	
	ArrayList<Question> questions;
	
	public QuizCreator() {
		questions = new ArrayList<Question>();
	}
	
	private String convertQuizToJSON() {
		Gson gson = new Gson();
		return gson.toJson(this);
	}
	
	private void saveQuizJSONToFile() {
		String json = convertQuizToJSON();
		File file = new File("TestQuiz.json");
		PrintWriter printWriter;
		try {
			printWriter = new PrintWriter(file);
			printWriter.println(json);
			printWriter.close();
		} catch (FileNotFoundException e) {
			System.out.println("[-] Unable to save Quiz JSON to file: " + file.toString());
			e.printStackTrace();
		}
	}
	
	public Question getQuestion(int index) {
		return questions.get(index);
	}
	
	public String[] getQuestionNames() {
		String[] questionNames = new String[questions.size()];
		
		for(int i = 0; i < questions.size(); i++) {
			questionNames[i] = questions.get(i).getquestion();
		}
		
		return questionNames;
		
	}
	
	public String toString() {
		return questions.toString();
	}
}
