# encoding:utf8

import socket
import zbx2db
import datetime
import json
import time


zbx2db = "/opt/mozbx/zbx2db.py"
if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('0.0.0.0', 7788))
    sock.listen(5)
    while True:
        connection, address = sock.accept()
        try:
            connection.settimeout(5)
            buf = connection.recv(1024)
            if buf == 'update':
                f = file(zbx2db, "wb")
                connection.send("start receiving")
                while True:
                    data = connection.recv(4096)
                    if data == 'file_send_done':break
                f.write(data)
                f.close()
                print datetime.datetime.now(), "get warnning info success!"
            else:
                request = zbx.get_request(buf)
                request_json = json.dumps(request)
                connection.send(request_json)
                print datetime.datetime.now(), "get " + buf + "info success!"
        except socket.timeout:
            print 'time out'
        connection.close()
