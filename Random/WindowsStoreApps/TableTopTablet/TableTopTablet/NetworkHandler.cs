using System;
using Windows.Networking;
using Windows.Networking.Sockets;
using Windows.Networking.Connectivity;
using Windows.Storage.Streams;
using System.Threading;
using System.Text;
using System.Diagnostics;
using System.IO;
using System.Net;
using System.Threading.Tasks;
using System.Collections.Generic;

namespace TableTopTablet
{
    // State object for receiving data from remote device.
    public class NetworkHandler
    {
        private StreamSocket socket;
        private Boolean socketConnected;
        private DataReader reader;
        private DataWriter writer;

        private string serverUrl;
        public NetworkHandler()
        {
        }

        public async Task<bool> SetServer(string ServerIP, string ServerPort)
        {
            bool socketSetup = await setupSocket(ServerIP, ServerPort);
            try
            {
                bool ftpSetup = await setupFTPClient(ServerIP);
            }
            catch (Exception e)
            {
                Debug.WriteLine("Lol what, ftp errors?: " + e.Message);
            }

            return socketSetup;
        }

        private async Task<bool> setupFTPClient(string serverIP)
        {
            try
            {
                string serverUriStr = "ftp://tabletoptablet@" + serverIP;
                Debug.WriteLine(serverUriStr);
                IEnumerable<FTPFileSystem> items = await FTPDownloadManager.Instance.ListFtpContentAsync(serverUriStr, null);
                FTPFileDataSource source = new FTPFileDataSource(items);
                return true;
            }
            catch (Exception e)
            {
                Debug.WriteLine("Error with FTP: " + e.Message);
                return false;
            }
        }

        private async Task<bool> setupSocket(string serverIP, string serverPort)
        {
            if (reader != null)
            {
                reader.DetachStream();
                reader.Dispose();
            }
            
            if (writer != null)
            {
                writer.DetachStream();
                writer.Dispose();
            }

            if (socket != null)
            {
                socket.Dispose();
            }

            socket = new StreamSocket();
            HostName hostname = null;
            try
            {
                hostname = new HostName(serverIP);
            }
            catch (ArgumentException)
            {
                Debug.WriteLine("[-] Invalid host name");
                return false;
            }

            try
            {
                await socket.ConnectAsync(hostname, serverPort, SocketProtectionLevel.PlainSocket);
                socketConnected = true;
                Debug.WriteLine("Connected to remote server: " + serverIP);
            }
            catch (Exception exception)
            {
                if (SocketError.GetStatus(exception.HResult) == SocketErrorStatus.Unknown)
                {
                    throw;
                }

                Debug.WriteLine("Connection failed with error: " + exception.Message);
                return false;
            }

            reader = new DataReader(socket.InputStream);
            writer = new DataWriter(socket.OutputStream);
            return true;
        }

        public async Task<bool> Login(string username, string password)
        {
            if (socketConnected)
            {
                Debug.WriteLine("Attempting to log into server");
                sendData("LOGIN " + username + " " + password);

                string receivedData = null;
                uint count = 0;
                reader.InputStreamOptions = InputStreamOptions.Partial;
                try
                {
                    count = (uint) await reader.LoadAsync(512);
                }
                catch (Exception e)
                {
                    Debug.WriteLine("Unable to write to socket: " + e.Message);
                    var messageDialog = new Windows.UI.Popups.MessageDialog("Unable to establish a connection to the remote server, please check your connectivity settings and try again.");
                    var result = messageDialog.ShowAsync();
                    return false;
                }

                if (count > 0)
                    receivedData = reader.ReadString(count);

                Debug.WriteLine(receivedData);
                if (receivedData != null && receivedData.Equals("LOGGED IN"))
                {
                    // Alert the user they were logged in and redirect page to question list
                    return true;
                }
                else
                {
                    // Alert the user they could not be logged in
                    var messageDialog = new Windows.UI.Popups.MessageDialog("You were unable to be logged into your account, please make sure you have the correct credentials.");
                    var result = messageDialog.ShowAsync();
                    return false;
                }
            }
            else
            {
                var messageDialog = new Windows.UI.Popups.MessageDialog("Unable to establish a connection to the remote server, please check your connectivity settings and try again.");
                var result = messageDialog.ShowAsync();
                return false;
            }
        }

        public async Task<bool> Register(string username, string password)
        {
            if (socketConnected)
            {
                sendData("REGISTER " + username + " " + password);

                string receivedData = null;
                uint count = 0;
                reader.InputStreamOptions = InputStreamOptions.Partial;
                try
                {
                    count = (uint)await reader.LoadAsync(512);
                }
                catch (Exception e)
                {
                    Debug.WriteLine("Unable to write to socket: " + e.Message);
                    var messageDialog = new Windows.UI.Popups.MessageDialog("Unable to establish a connection to the remote server, please check your connectivity settings and try again.");
                    var result = messageDialog.ShowAsync();
                    return false;
                }
                
                if (count > 0)
                    receivedData = reader.ReadString(count);

                if (receivedData.Equals("REGISTERED"))
                {
                    // Alert the user saying that they can now login
                    return true;
                }
                else
                {
                    // Alert the user saying that they could not be registered
                    return false;
                }
            }
            else
            {
                var messageDialog = new Windows.UI.Popups.MessageDialog("Unable to establish a connection to the remote server, please check your connectivity settings and try again.");
                var result = messageDialog.ShowAsync();
                return false;
            }
        }

        public async Task<bool> UpdateQuestions()
        {
            if (socketConnected)
            {
                sendData("UPDATE");

                string receivedData = null;
                uint count = 0;
                reader.InputStreamOptions = InputStreamOptions.Partial;
                try
                {
                    count = (uint)await reader.LoadAsync(512);
                }
                catch (Exception e)
                {
                    Debug.WriteLine("Unable to write to socket: " + e.Message);
                    var messageDialog = new Windows.UI.Popups.MessageDialog("Unable to establish a connection to the remote server, please check your connectivity settings and try again.");
                    var result = messageDialog.ShowAsync();
                    return false;
                }
                
                if (count > 0)
                    receivedData = reader.ReadString(count);
                // RecievedData has JSON of the questions
                return true;
            }
            else
            {
                var messageDialog = new Windows.UI.Popups.MessageDialog("Unable to establish a connection to the remote server, please check your connectivity settings and try again.");
                var result = messageDialog.ShowAsync();
                return false;
            }
        }

        private async void sendData(string msg)
        {
            var length = writer.MeasureString(msg);
            // writer.WriteInt32((int)length);
            writer.WriteString(msg);
            var ret = await writer.StoreAsync();
        }

    }
}