import java.awt.EventQueue;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.ArrayList;

import javax.swing.DefaultListModel;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JList;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;
import javax.swing.JPanel;
import javax.swing.SpringLayout;
import javax.swing.UIManager;
import javax.swing.border.EmptyBorder;
import javax.swing.event.ListSelectionEvent;
import javax.swing.event.ListSelectionListener;

import networkHandlers.Question;
import networkHandlers.ServerHandler;
import networkHandlers.Student;


public class QuizCreatorGUI extends JFrame {

	private JPanel contentPane;
	private QuizCreator quizCreator;
	private String fileName = "TestQuiz.ttq";
	private ServerSocket redSock; 
	private ArrayList<Student> students = new ArrayList<Student>();
	private JList<String> connectedStudentsList;
	private DefaultListModel<String> studentList = new DefaultListModel<String>();
	
	/**
	 * Launch the application.
	 */
	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
					QuizCreatorGUI frame = new QuizCreatorGUI();
					frame.setVisible(true);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}

	/**
	 * Create the frame.
	 */
	public QuizCreatorGUI() {
		loadQuiz();
		new Thread(new Runnable() {
			@Override
			public void run() {
                ServerSocket soc;
				try {
					soc = new ServerSocket(5217);
                    System.out.println("FTP Server Started on Port Number 5217");
                    ServerHandler server = new ServerHandler("ServerFiles//");
                    while (true) {
                        System.out.println("Waiting for Connection ...");
                        server.handleNewClient(soc.accept());
                        studentList.addElement(ServerHandler.connectedClients.get(ServerHandler.connectedClients.size() - 1).ip);
                    }
				} catch (IOException e) {
					e.printStackTrace();
				}
			}
		}).start();
		
		setTitle("Quiz Creator");
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setBounds(100, 100, 832, 527);
		
		JMenuBar menuBar = new JMenuBar();
		setJMenuBar(menuBar);
		contentPane = new JPanel();
		contentPane.setBorder(new EmptyBorder(5, 5, 5, 5));
		setContentPane(contentPane);
		SpringLayout sl_contentPane = new SpringLayout();
		contentPane.setLayout(sl_contentPane);
		
		final JList questionList = new JList(quizCreator.getQuestionNames());
		questionList.addListSelectionListener(new ListSelectionListener() {
			public void valueChanged(ListSelectionEvent arg0) {
				Question question = quizCreator.getQuestion(questionList.getSelectedIndex());
				
			}
		});
		sl_contentPane.putConstraint(SpringLayout.NORTH, questionList, -20, SpringLayout.SOUTH, menuBar);
		
		JMenu fileMenu = new JMenu("File");
		menuBar.add(fileMenu);
		
		JMenuItem openQuizMenuItem = new JMenuItem("Open Quiz...");
		fileMenu.add(openQuizMenuItem);
		
		JMenuItem saveQuizAsMenuItem = new JMenuItem("Save Quiz as...");
		fileMenu.add(saveQuizAsMenuItem);
		
		JMenuItem saveQuizMenuItem = new JMenuItem("Save Quiz");
		fileMenu.add(saveQuizMenuItem);
		sl_contentPane.putConstraint(SpringLayout.WEST, questionList, 5, SpringLayout.WEST, contentPane);
		sl_contentPane.putConstraint(SpringLayout.SOUTH, questionList, -50, SpringLayout.SOUTH, contentPane);
		contentPane.add(questionList);
		
		JButton addQuestionButton = new JButton("Add a question");
		sl_contentPane.putConstraint(SpringLayout.NORTH, addQuestionButton, 5, SpringLayout.SOUTH, questionList);
		sl_contentPane.putConstraint(SpringLayout.WEST, addQuestionButton, 5, SpringLayout.WEST, contentPane);
		sl_contentPane.putConstraint(SpringLayout.SOUTH, addQuestionButton, 0, SpringLayout.SOUTH, contentPane);
		sl_contentPane.putConstraint(SpringLayout.EAST, addQuestionButton, 0, SpringLayout.EAST, questionList);
		contentPane.add(addQuestionButton);
		
		JButton showOnScreensButton = new JButton("Send question to students");
		sl_contentPane.putConstraint(SpringLayout.NORTH, showOnScreensButton, 0, SpringLayout.NORTH, addQuestionButton);
		sl_contentPane.putConstraint(SpringLayout.WEST, showOnScreensButton, 97, SpringLayout.EAST, addQuestionButton);
		sl_contentPane.putConstraint(SpringLayout.SOUTH, showOnScreensButton, 0, SpringLayout.SOUTH, addQuestionButton);
		contentPane.add(showOnScreensButton);
		
		connectedStudentsList = new JList<String>(studentList);
		sl_contentPane.putConstraint(SpringLayout.WEST, connectedStudentsList, 450, SpringLayout.EAST, questionList);
		sl_contentPane.putConstraint(SpringLayout.EAST, questionList, -625, SpringLayout.EAST, connectedStudentsList);
		sl_contentPane.putConstraint(SpringLayout.NORTH, connectedStudentsList, -20, SpringLayout.SOUTH, menuBar);
		sl_contentPane.putConstraint(SpringLayout.SOUTH, connectedStudentsList, 0, SpringLayout.SOUTH, questionList);
		sl_contentPane.putConstraint(SpringLayout.EAST, connectedStudentsList, -5, SpringLayout.EAST, contentPane);
		contentPane.add(connectedStudentsList);
		
		JButton manageConnectedStudentsButton = new JButton("Manage Connected Students");
		sl_contentPane.putConstraint(SpringLayout.EAST, showOnScreensButton, -100, SpringLayout.WEST, manageConnectedStudentsButton);
		sl_contentPane.putConstraint(SpringLayout.NORTH, manageConnectedStudentsButton, 5, SpringLayout.SOUTH, connectedStudentsList);
		sl_contentPane.putConstraint(SpringLayout.WEST, manageConnectedStudentsButton, 0, SpringLayout.WEST, connectedStudentsList);
		sl_contentPane.putConstraint(SpringLayout.SOUTH, manageConnectedStudentsButton, 0, SpringLayout.SOUTH, contentPane);
		sl_contentPane.putConstraint(SpringLayout.EAST, manageConnectedStudentsButton, 0, SpringLayout.EAST, connectedStudentsList);
		contentPane.add(manageConnectedStudentsButton);
	}
	
	private void displayEditableQuestion(Question question) {
		// Add question to the window
	}

	private void loadQuiz() {
		quizCreator = QuizMethods.makeQuizFromFile(fileName);
		
		
	}
}
