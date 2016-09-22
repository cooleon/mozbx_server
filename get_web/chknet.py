# encoding:utf8
import socket


def main():
    # locale = "10.10.6.4"
    locale = "127.0.0.1"
    port = 7788
    print connect_chk(locale, port)


def connect_chk(host, port):
    try:
        s = socket.create_connection((host, port), 5)
        connected = 1
        s.close()
        return connected
    except:
        unconnected = 0
        return unconnected

if __name__ == '__main__':
    main()
