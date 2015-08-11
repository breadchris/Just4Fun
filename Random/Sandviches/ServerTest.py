from socket import *
from time import sleep
import threading
import thread
import signal
import sys
import serial

ser = serial.Serial('/dev/ttyACM0', 9600)
ardubusy = False;
def handler(clientsock, addr):
    while 1:
        data = readline(clientsock);
        if not data:
            break
        print "Data Sent: " +  data
        print "[*] Sending data to Arduino..."
        ser.write(data)
        print "[+] Data sent :3"
        sleep(0.75);
        while (ser.inWaiting() > 0):
            sleep(0.75)
            line = ser.readline().replace("\n","");
            print line;

    clientsock.close()

def signal_handler(signal, frame):
    print '[-] Server closing down...'
    sys.exit(0)

def readline(sock):
    ret = ''
    while 1:
        c = sock.recv(1);
        if c == '\n' or c == '':
            break
        else:
            ret += c
    return ret


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    print "[+] Server starting up... Press Ctrl + C to exit"
    PORT = 55555
    BUFSIZ = 1024
    ADDR = ('', PORT)
    serversock = socket(AF_INET, SOCK_STREAM)
    serversock.bind(ADDR)
    serversock.listen(2)
    
    ser.flushInput();
    while 1:
        print '[*] Waiting for connection...'
        clientsock, addr = serversock.accept()
        print '[+] Connection established with: '
        print addr
        thread.start_new_thread(handler, (clientsock, addr));
