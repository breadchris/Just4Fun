#!/bin/bash

echo "Content-type: text/html"
echo ""

echo '<html>'
echo '<head>'
echo '<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">'
echo '<title>IT LOGIN</title>'
echo '</head>'
echo '<body>'

  echo '<h1>IT LOGIN</h1>'
  echo "<form method=GET action=\"${SCRIPT}\">"\
       '<table nowrap>'\
          '<tr><td>Username</TD><TD><input type="text" name="user" size=12></td></tr>'\
          '<tr><td>Password</td><td><input type="text" name="pass" size=12 value=""></td>'\
          '</tr></table>'

  echo '<br><input type="submit" value="Login">'\
       '<input type="reset" value="Reset"></form>'

  # Make sure we have been invoked properly.

  if [ "$REQUEST_METHOD" != "GET" ]; then
        echo "<hr>Script Error:"\
             "<br>Usage error, cannot complete request, REQUEST_METHOD!=GET."\
             "<br>Check your FORM declaration and be sure to use METHOD=\"GET\".<hr>"
        exit 1
  fi

  # If no search arguments, exit gracefully now.

  if [ -z "$QUERY_STRING" ]; then
        exit 0
  else
     # No looping this time, just extract the data you are looking for with sed:
     USER=`echo "$QUERY_STRING" | sed -n 's/^.*user=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"`
     PASS=`echo "$QUERY_STRING" | sed -n 's/^.*pass=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"`
     if [ "$USER" != "itadmin" -o "$PASS" != "0ct0pusW4lruuus" ]; then
        echo '<marquee><h1>SIKE THOSE ARE THE WRONG CREDS</h1></marquee>'
        exit 1
     else
        echo "<h3>Welcome! " $USER "</h3>"
    echo '<br>'
        echo '<a href="http://52.2.178.68/files/capture-2015-11-9.pcap">capture-2015-11-9.pcap</a><br />'
     fi
  fi
echo '</body>'
echo '</html>'

exit 0
