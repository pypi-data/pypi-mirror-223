import socket

class utils(object):

    @classmethod
    def local_ip(cls):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        except Exception as e:
            ip = '127.0.0.1'
        finally:
            s.close()
        return ip