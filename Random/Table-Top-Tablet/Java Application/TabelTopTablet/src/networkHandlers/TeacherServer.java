package networkHandlers;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.PrintWriter;
import java.nio.ByteBuffer;
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;

import org.apache.commons.io.FileUtils;

import com.google.gson.Gson;

public class TeacherServer {

	private String serverRoot;
	private String questionsFile;
	private Gson gson;
	private Questions questions;

	public TeacherServer(String serverRoot, String questionsFile) {
		File root = new File(serverRoot);
		if (!root.exists()) {
			boolean madeDir = root.mkdir();
			if (!madeDir) 
				System.out.println("[-] Unable to make root directory in: " + serverRoot);
		}
		this.serverRoot = serverRoot;
		this.questionsFile = questionsFile;
		this.gson = new Gson();
		if (!this.loadQuestions())
			this.questions = new Questions();
	}

	public boolean addQuestion(String title, String folder) {
		boolean createdFolder = new File(serverRoot + folder).mkdir();
		if (createdFolder) {
			questions.addQuestion(title, serverRoot + folder);
			return true;
		} else {
			return false;
		}
	}

	public boolean saveQuestions() {
		try {
			String json = gson.toJson(questions);
			PrintWriter pW = new PrintWriter(new File(serverRoot + this.questionsFile));
			pW.println(json);
			pW.close();
			return true;
		} catch (Exception e) {
			System.out.println("[-] Unable to save questions to: " + serverRoot + this.questionsFile);
			return false;
		}
	}

	private boolean loadQuestions() {
		try {
			String json = readFile(serverRoot + this.questionsFile, Charset.defaultCharset());
			this.questions = gson.fromJson(json, Questions.class);
			return true;
		} catch (Exception e) {
			System.out.println("[-] Unable to load questions from: " + serverRoot + this.questionsFile);
			return false;
		}
	}

	public void setQuestionConfigurationLocation(String location) {
		this.questionsFile = location;
	}

	static String readFile(String path, Charset encoding) throws IOException {
		byte[] encoded = Files.readAllBytes(Paths.get(path));
		return encoding.decode(ByteBuffer.wrap(encoded)).toString();
	}

	public String getQuestions() {
		return questions.toString();
	}
	
	public void cleanServerRoot() throws IOException {
		FileUtils.cleanDirectory(new File(serverRoot));
	}
}
