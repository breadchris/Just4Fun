import java.awt.*;

import javax.swing.*;
import javax.swing.border.EmptyBorder;
import javax.swing.filechooser.FileNameExtensionFilter;

import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Scanner;
import java.util.Timer;
import java.util.TimerTask;

import javax.swing.GroupLayout.Alignment;
import javax.swing.LayoutStyle.ComponentPlacement;
import javax.swing.UIManager.LookAndFeelInfo;


public class ConnectionBlockerGUI extends JFrame {

	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	private JPanel contentPane;
	private String filename;
	private static NetStatChecker checker = new NetStatChecker();
	private static ArrayList<RunningProcess> checkerOutput = new ArrayList<RunningProcess>();
	public static ArrayList<String> ipExceptions = new ArrayList<String>(); 
	private JTextField txtProcessName;
	private final static JList list = new JList();
	private static boolean showTrusted = true;

	/**
	 * Launch the application.
	 */
	public static void main(String[] args) {
		try {
		    for (LookAndFeelInfo info : UIManager.getInstalledLookAndFeels()) {
		        if ("Nimbus".equals(info.getName())) {
		            UIManager.setLookAndFeel(info.getClassName());
		            break;
		        }
		    }
		} catch (Exception e) {
		    // If Nimbus is not available, you can set the GUI to another look and feel.
		}
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					ConnectionBlockerGUI frame = new ConnectionBlockerGUI();
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
	@SuppressWarnings({ "unchecked", "serial" })
	public ConnectionBlockerGUI() {		
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setBounds(100, 100, 571, 692);
		
		JMenuBar menuBar = new JMenuBar();
		setJMenuBar(menuBar);
		
		JMenu mnFile = new JMenu("File");
		menuBar.add(mnFile);
		
		JScrollPane scrollPane = new JScrollPane();
		list.setCellRenderer(new DefaultListCellRenderer() {
			public Component getListCellRendererComponent (JList list, Object value, int index, boolean isSelected, boolean cellHasFocus) {
				JLabel label = (JLabel) super.getListCellRendererComponent(list, value, index, isSelected, cellHasFocus);
				if (isSelected) {
					txtProcessName.setText(checker.getProcessName(checkerOutput.get(index).pid));
					label.setForeground(Color.BLUE);
				}
				
                for (int i = 0; i < ipExceptions.size(); i++) {
                	if (((String) value).contains(ipExceptions.get(i))) {
                		label.setBackground(Color.GREEN);
                		return label;
                	}
                }
				label.setBackground(Color.YELLOW);
				return label;
			}
		});
		scrollPane.setViewportView(list);
		
		JMenuItem loadExceptionsMenuItem = new JMenuItem("Load Exceptions");
		loadExceptionsMenuItem.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				JFileChooser chooser = new JFileChooser();
			    FileNameExtensionFilter filter = new FileNameExtensionFilter(
			        "Config Files", "conf");
			    chooser.setFileFilter(filter);
			    int returnVal = chooser.showOpenDialog(getParent());
			    if(returnVal == JFileChooser.APPROVE_OPTION) {
			    	filename = chooser.getSelectedFile().getName();
			    	loadIPExceptions();
			    }
			}
		});
		loadExceptionsMenuItem.setAccelerator(KeyStroke.getKeyStroke('O', Toolkit.getDefaultToolkit().getMenuShortcutKeyMask(), false));
		mnFile.add(loadExceptionsMenuItem);
		
		JMenuItem refreshMenuItem = new JMenuItem("Refresh");
		refreshMenuItem.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				refreshList();
			}
		});
		refreshMenuItem.setAccelerator(KeyStroke.getKeyStroke('R', Toolkit.getDefaultToolkit().getMenuShortcutKeyMask(), false));
		mnFile.add(refreshMenuItem);
		
		JMenuItem mntmTimedRefresh = new JMenuItem("Timed Refresh");
		mntmTimedRefresh.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				Timer uploadCheckerTimer = new Timer(true);
				uploadCheckerTimer.scheduleAtFixedRate(
				    new TimerTask() {
				      public void run() { refreshList(); }
				    }, 0, 1000);
			}
		});
		mnFile.add(mntmTimedRefresh);
		
		JMenu mnEdit = new JMenu("Edit");
		menuBar.add(mnEdit);
		
		JMenuItem mntmRemoveDuplicates = new JMenuItem("Remove Duplicates");
		mntmRemoveDuplicates.setAccelerator(KeyStroke.getKeyStroke('D', Toolkit.getDefaultToolkit().getMenuShortcutKeyMask(), false));
		mntmRemoveDuplicates.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				ArrayList<String> deDupedArray = new ArrayList<String>();
				@SuppressWarnings("rawtypes")
				DefaultListModel listModel = new DefaultListModel();
				for (RunningProcess s : checkerOutput) {
					String val = s.toString();
					if (!deDupedArray.contains(val)) {
						listModel.addElement(val);
						deDupedArray.add(val);
					}
				}
				list.setModel(listModel);
			}
		});
		mnEdit.add(mntmRemoveDuplicates);
		
		JMenuItem mntmHideTrusted = new JMenuItem("Show/Hide Trusted");
		mntmHideTrusted.setAccelerator(KeyStroke.getKeyStroke('H', Toolkit.getDefaultToolkit().getMenuShortcutKeyMask(), false));
		mntmHideTrusted.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				showTrusted = false;
				refreshList();
			}
		});
		mnEdit.add(mntmHideTrusted);
		contentPane = new JPanel();
		contentPane.setBorder(new EmptyBorder(5, 5, 5, 5));
		setContentPane(contentPane);
		
		JButton btnNewButton_2 = new JButton("Block Selected");
		btnNewButton_2.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				int selected = list.getSelectedIndex();
				if (selected != -1) {
					RunningProcess selectedElement = checkerOutput.get(selected);
					checker.blockIP(selectedElement.ipAddress, "BlockedAttacker", selectedElement.protocol, selectedElement.port);
				}
			}
		});
		
		JButton button = new JButton("Trust Selected");
		button.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				int selected = list.getSelectedIndex();
				if (selected != -1) {
					RunningProcess selectedElement = checkerOutput.get(selected);
					addIPException(selectedElement.ipAddress);
					ipExceptions.add(selectedElement.ipAddress);
				}
			}
		});
		
		txtProcessName = new JTextField();
		txtProcessName.setEditable(false);
		txtProcessName.setText("Process Name");
		txtProcessName.setColumns(10);
		GroupLayout gl_contentPane = new GroupLayout(contentPane);
		gl_contentPane.setHorizontalGroup(
			gl_contentPane.createParallelGroup(Alignment.LEADING)
				.addGroup(gl_contentPane.createSequentialGroup()
					.addContainerGap()
					.addComponent(btnNewButton_2)
					.addPreferredGap(ComponentPlacement.RELATED)
					.addComponent(button, GroupLayout.PREFERRED_SIZE, 117, GroupLayout.PREFERRED_SIZE)
					.addPreferredGap(ComponentPlacement.RELATED, 220, Short.MAX_VALUE)
					.addComponent(txtProcessName, GroupLayout.PREFERRED_SIZE, 101, GroupLayout.PREFERRED_SIZE))
				.addComponent(scrollPane, GroupLayout.DEFAULT_SIZE, 545, Short.MAX_VALUE)
		);
		gl_contentPane.setVerticalGroup(
			gl_contentPane.createParallelGroup(Alignment.TRAILING)
				.addGroup(Alignment.LEADING, gl_contentPane.createSequentialGroup()
					.addGap(9)
					.addGroup(gl_contentPane.createParallelGroup(Alignment.LEADING)
						.addGroup(gl_contentPane.createParallelGroup(Alignment.BASELINE)
							.addComponent(button, GroupLayout.PREFERRED_SIZE, 33, GroupLayout.PREFERRED_SIZE)
							.addComponent(btnNewButton_2, GroupLayout.PREFERRED_SIZE, 33, GroupLayout.PREFERRED_SIZE))
						.addComponent(txtProcessName, GroupLayout.PREFERRED_SIZE, 27, GroupLayout.PREFERRED_SIZE))
					.addGap(18)
					.addComponent(scrollPane, GroupLayout.DEFAULT_SIZE, 563, Short.MAX_VALUE))
		);
		contentPane.setLayout(gl_contentPane);
	}
	
	public static void refreshList() {
		checkerOutput = checker.getConnections();
		@SuppressWarnings("rawtypes")
		DefaultListModel listModel = new DefaultListModel();
		if (!showTrusted) {
			for (RunningProcess s : checkerOutput) {
				if (!ipExceptions.contains(s.ipAddress)) {
					listModel.addElement(s.toString());
				}
			}
		} else {
			for (RunningProcess s : checkerOutput) {
				listModel.addElement(s.toString());
			}
		}
		list.setModel(listModel);
	}

	private void loadIPExceptions() {
		File file = new File(filename);
        try {
            Scanner scanner = new Scanner(file);
            ipExceptions.clear();
            while (scanner.hasNextLine()) {
                String line = scanner.nextLine();
                ipExceptions.add(line);
            }
            scanner.close();
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
	}
	
	private void addIPException(String ipAddress) {
		try {
		    PrintWriter out = new PrintWriter(new BufferedWriter(new FileWriter(filename, true)));
		    out.print("\n"+ipAddress);
		    out.close();
		} catch (IOException e) {
		    System.out.println("Could not append to file");
		}
	}
}
