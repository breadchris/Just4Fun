import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;

import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

import com.google.gson.Gson;


public class TestingClass {
	
	public static void main(String args[]) {
		QuizCreator qc = makeQuizFromFile("TestQuiz.ttq");
		System.out.println(qc);
	}
	
	private static QuizCreator makeQuizFromFile(String file) {
		Gson gson = new Gson();
		JSONParser jsonParser = new JSONParser();
		FileReader fileReader = null;
		try {
			fileReader = new FileReader(file);
		} catch (FileNotFoundException e) {
			System.out.println("[-] Unable to read file: " + file);
			e.printStackTrace();
		}
		
		JSONObject jsonObject = null;
		
		try {
			jsonObject = (JSONObject) jsonParser.parse(fileReader);
		} catch (IOException e) {
			System.out.println("[-] Unable to read file while parsing: " + file);
			e.printStackTrace();
		} catch (ParseException e) {
			System.out.println("[-] Unable to parse json file: " + file);
			e.printStackTrace();
		}
		
		return gson.fromJson(jsonObject.toString(), QuizCreator.class);
	}

}
