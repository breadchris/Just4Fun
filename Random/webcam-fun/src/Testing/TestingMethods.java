package Testing;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import org.apache.commons.codec.binary.Base64;

public class TestingMethods {

    public static void main(String[] args) {
    	ipSplitting();
    }
    
    private static void ipSplitting() {
    	String ip = "172.23.123.23";
    	String[] splitIP = ip.split("\\.");
    	for (int i = 0; i < splitIP.length; i++) {
    		System.out.println("[" + i + "] = " + splitIP[i]);
    	}
    }
    
    private static void httpAuth() {
        try {
            URL url = new URL ("http://172.26.13.25/now.jpg");
            byte[] encoding = Base64.encodeBase64("root:****246".getBytes());
            String encodingString = new String(encoding);

            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("POST");
            connection.setDoOutput(true);
            connection.setRequestProperty  ("Authorization", "Basic " + encodingString);
            InputStream content = (InputStream)connection.getInputStream();
            BufferedReader in   = 
                new BufferedReader (new InputStreamReader (content));
            String line;
            while ((line = in.readLine()) != null) {
                System.out.println(line);
            }
        } catch(Exception e) {
            e.printStackTrace();
        }
    }
}
