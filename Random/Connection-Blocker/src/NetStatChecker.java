import java.io.*;
import java.util.ArrayList;
import java.util.Iterator;
import ch.ethz.ssh2.*;

public class NetStatChecker {
        /**
         * OVERVIEW: A class to execute programs from the command line and return
         *                       useful information
         */
	
		// Main
		public static void main(String[] args) {
			NetStatChecker checker = new NetStatChecker();
			ArrayList<RunningProcess> output = checker.getConnectionsLinux();
			for (RunningProcess s : output) {
				System.out.println(s);
			}
			
		}

        // CONSTRUCTOR
        public NetStatChecker() {
        }

        public ArrayList<RunningProcess> getConnections() {
                /**
                 * EFFECTS: Gets the active processes with ports open and returns a list of them
                 */
                ArrayList<String[]> netstat = new ArrayList<String[]>();
                try {
                        String line;
                        // execute the netstat command
                        java.lang.Process p = Runtime.getRuntime().exec("netstat -o -n");
                        // capture the output of netstat
                        BufferedReader input = new BufferedReader(new InputStreamReader(p.getInputStream()));
                        while ((line = input.readLine()) != null) {
                                netstat.add(line.split("\\s+"));
                        }
                        input.close();
                } catch (Exception err) {
                        err.printStackTrace();
                }
                
                // Parsing output of netstat
                ArrayList<RunningProcess> arl = new ArrayList<RunningProcess>();
                
                // Removing headers from netstat command
                netstat.remove(0); netstat.remove(0); netstat.remove(0); netstat.remove(0);
                
                int j = 0;
                for (String[] line : netstat) {
                	String[] parsedIP = line[3].split(":");
                	try {
                	arl.add(new RunningProcess (line[1], parsedIP[0], 
                			Integer.parseInt(parsedIP[1]), line[4], Integer.parseInt(line[5])));
                	} catch (Exception e) {
                		System.out.println("TIME_WAIT Connection: " + line[2]);
                	}
                }
 
                return arl;
        }
        
        public ArrayList<RunningProcess> getConnectionsLinux() {
        	/* *
        	 * Insert SSH setup here
        	 */
        	ArrayList<String[]> netstat = new ArrayList<String[]>();
            try {
                    String line;
                    // execute the netstat command
                    java.lang.Process p = Runtime.getRuntime().exec("netstat -tulpn");
                    // capture the output of netstat
                    BufferedReader input = new BufferedReader(new InputStreamReader(p.getInputStream()));
                    while ((line = input.readLine()) != null) {
                            netstat.add(line.split("\\s+"));
                    }
                    input.close();
            } catch (Exception err) {
                    err.printStackTrace();
            }
            
            // Parsing output of netstat
            ArrayList<RunningProcess> arl = new ArrayList<RunningProcess>();
            
            // Removing headers from netstat command
            netstat.remove(0); netstat.remove(0); netstat.remove(0); netstat.remove(0);
            
            int j = 0;
            for (String[] line : netstat) {
            	String[] parsedIP = line[3].split(":");
            	for (int i = 0; i < line.length; i++) {
            		System.out.println(j + " | " + i + " | " + line[i]);
            	}
            	j++;
            	try {
            	arl.add(new RunningProcess (line[1], parsedIP[0], 
            			Integer.parseInt(parsedIP[1]), line[4], Integer.parseInt(line[5])));
            	} catch (Exception e) {
            		System.out.println("TIME_WAIT Connection: " + line[2]);
            	}
            }

            return arl;
        }

        public String getProcessName(int PID) {
                /**
                 * EFFECTS: Returns the process's name based on its PID
                 */
                String tasklist = new String();
                String processName = new String();
                try {
                        String line;
                        // execute tasklist filtering by PID
                        java.lang.Process p = Runtime.getRuntime().exec("tasklist /FI \"PID eq " + PID + "\"");
                        // capture the output
                        BufferedReader input = new BufferedReader(new InputStreamReader(p.getInputStream()));
                        while ((line = input.readLine()) != null) {
                                tasklist = tasklist + "\n" + line;
                        }
                        input.close();
                } catch (Exception err) {
                        err.printStackTrace();
                }

                if (tasklist.equals("INFO: No tasks running with the specified criteria."))
                        return " ";

                // parse it
                processName = tasklist.substring(tasklist.lastIndexOf("=") + 2,
                                tasklist.indexOf("   ", tasklist.lastIndexOf("=")));
                return processName;
        }

        public static void blockIP(String ipAddress, String name, String protocol, int port) {
            String line = new String();
            try {
                    // execute hostname
                    java.lang.Process p = Runtime.getRuntime().exec("netsh advfirewall add rule name=\""+name+"\" protocol="
                    		+protocol+" localport="+port+" action=block dir=IN remoteip="+ipAddress);
            } catch (Exception err) {
                    err.printStackTrace();
            }
        }
        
        public static void blockIPLinux(String ipAddress) {
        	/* *
        	 * Enter SSH code here
        	 */
        	try {
        		java.lang.Process p = Runtime.getRuntime().exec("iptables -A INPUT -s " + ipAddress + " -j DROP");
        	} catch (Exception err) {
        		err.printStackTrace();
        	}
        }
}