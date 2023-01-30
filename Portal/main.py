import socket
import threading
import time
from flask import Flask, render_template
from unidecode import unidecode
import sys
import os


port_num = 2000 + int(sys.argv[1])
messages = []

for i in range(2000, port_num):
    messages.append("")

def udp_listener(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', port))
    while True:
        data = sock.recvfrom(1024)
        messages[port - 2000] = unidecode(data[0].decode('utf-8'))  

if __name__ == '__main__':
    time.sleep(1)
    for i in range(2000, port_num):
        t = threading.Thread(target=udp_listener, args=(i,))
        t.start()
        print("Started thread for port %s" % i)
        time.sleep(0.5)

def webserver():
    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_template('index.html', port_num=port_num, messages=messages)
    
    if __name__ == '__main__':
        app.run(debug=False, host='0.0.0.0')
webt = threading.Thread(target=webserver)
webt.start()
print("Started webserver")
