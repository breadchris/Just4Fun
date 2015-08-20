using TableTopTablet.Common;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.RegularExpressions;
using System.Runtime.InteropServices.WindowsRuntime;
using System.Diagnostics;
using Windows.Foundation;
using Windows.Foundation.Collections;
using Windows.UI.Xaml;
using Windows.UI.Xaml.Controls;
using Windows.UI.Xaml.Controls.Primitives;
using Windows.UI.Xaml.Data;
using Windows.UI.Xaml.Input;
using Windows.UI.Xaml.Media;
using Windows.UI.Xaml.Navigation;

// The Basic Page item template is documented at http://go.microsoft.com/fwlink/?LinkId=234237

namespace TableTopTablet
{
    /// <summary>
    /// A basic page that provides characteristics common to most applications.
    /// </summary>
    public sealed partial class ConnectionSettingsPage : Page
    {

        private NavigationHelper navigationHelper;
        private ObservableDictionary defaultViewModel = new ObservableDictionary();

        /// <summary>
        /// This can be changed to a strongly typed view model.
        /// </summary>
        public ObservableDictionary DefaultViewModel
        {
            get { return this.defaultViewModel; }
        }

        /// <summary>
        /// NavigationHelper is used on each page to aid in navigation and 
        /// process lifetime management
        /// </summary>
        public NavigationHelper NavigationHelper
        {
            get { return this.navigationHelper; }
        }


        public ConnectionSettingsPage()
        {
            this.InitializeComponent();
            this.navigationHelper = new NavigationHelper(this);
            this.navigationHelper.LoadState += navigationHelper_LoadState;
            this.navigationHelper.SaveState += navigationHelper_SaveState;

            ServerIP.Text = App.remoteServerIP;
            ServerPort.Text = App.remoteServerPort;
        }

        /// <summary>
        /// Populates the page with content passed during navigation. Any saved state is also
        /// provided when recreating a page from a prior session.
        /// </summary>
        /// <param name="sender">
        /// The source of the event; typically <see cref="NavigationHelper"/>
        /// </param>
        /// <param name="e">Event data that provides both the navigation parameter passed to
        /// <see cref="Frame.Navigate(Type, Object)"/> when this page was initially requested and
        /// a dictionary of state preserved by this page during an earlier
        /// session. The state will be null the first time a page is visited.</param>
        private void navigationHelper_LoadState(object sender, LoadStateEventArgs e)
        {
        }

        /// <summary>
        /// Preserves state associated with this page in case the application is suspended or the
        /// page is discarded from the navigation cache.  Values must conform to the serialization
        /// requirements of <see cref="SuspensionManager.SessionState"/>.
        /// </summary>
        /// <param name="sender">The source of the event; typically <see cref="NavigationHelper"/></param>
        /// <param name="e">Event data that provides an empty dictionary to be populated with
        /// serializable state.</param>
        private void navigationHelper_SaveState(object sender, SaveStateEventArgs e)
        {
        }

        #region NavigationHelper registration

        /// The methods provided in this section are simply used to allow
        /// NavigationHelper to respond to the page's navigation methods.
        /// 
        /// Page specific logic should be placed in event handlers for the  
        /// <see cref="GridCS.Common.NavigationHelper.LoadState"/>
        /// and <see cref="GridCS.Common.NavigationHelper.SaveState"/>.
        /// The navigation parameter is available in the LoadState method 
        /// in addition to page state preserved during an earlier session.

        protected override void OnNavigatedTo(NavigationEventArgs e)
        {
            navigationHelper.OnNavigatedTo(e);
        }

        protected override void OnNavigatedFrom(NavigationEventArgs e)
        {
            navigationHelper.OnNavigatedFrom(e);
        }

        #endregion

        private async void SaveSettingsButton_Click(object sender, RoutedEventArgs e)
        {
            if (ServerIP.Text != "" && validIP(ServerIP.Text) && ServerPort.Text != "" && validNumber(ServerPort.Text))
            {
                App.remoteServerIP = ServerIP.Text;
                App.remoteServerPort = ServerPort.Text;
                bool connected = await App.networkHandler.SetServer(App.remoteServerIP, App.remoteServerPort);
                string connectedMsg = "but failed to establish connection to server.";
                if (connected)
                {
                    connectedMsg = "and successfully connected to server.";
                }
                var messageDialog = new Windows.UI.Popups.MessageDialog("Settings saved successfully, " + connectedMsg);
                var result = messageDialog.ShowAsync();
            }
            else
            {
                var messageDialog = new Windows.UI.Popups.MessageDialog("The settings you attempted to save are not vaild entries, please check them again.");
                var result = messageDialog.ShowAsync();
            }
        }

        private async void EstablishConnectionButton_Click(object sender, RoutedEventArgs e)
        {
            if (App.remoteServerIP != "" && validIP(App.remoteServerIP) && App.remoteServerPort != "" && validNumber(App.remoteServerPort))
            {
                bool connected = await App.networkHandler.SetServer(App.remoteServerIP, App.remoteServerPort);
                string connectionMsg = "Unable to establish connection to server";
                if (connected)
                    connectionMsg = "Successfully connected to server.";
                var messageDialog = new Windows.UI.Popups.MessageDialog(connectionMsg);
                var result = messageDialog.ShowAsync();
            }
            else
            {
                var messageDialog = new Windows.UI.Popups.MessageDialog("Attempted to establish connection, but given network configuration had invalid parameters.");
                var result = messageDialog.ShowAsync();
            }
        }

        private bool validNumber(string number)
        {
            int n;
            return int.TryParse(ServerPort.Text, out n);
        }

        private bool validIP(string ip)
        {
            string pattern = @"\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b";
            //create our Regular Expression object
            Regex check = new Regex(pattern);
            //boolean variable to hold the status
            bool validIP = false;
            //check to make sure an ip address was provided
            //check to make sure an ip address was provided
            if (ServerIP.Text == "")
            {
                //no address provided so return false
                validIP = false;
            }
            else
            {
                //address provided so use the IsMatch Method
                //of the Regular Expression object
                validIP = check.IsMatch(ip, 0);
            }
            return validIP;
        }
    }
}
