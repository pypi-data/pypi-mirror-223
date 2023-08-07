import socket

def dolphin_scanner(host,delay=0):
    port_list = []
    host = host.replace("https://", "")
    host = host.replace("http://", "")
    try:
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.settimeout(15)
        tcp_socket.connect((host,80))
        tcp_socket.close()

    except socket.gaierror:
        return "host is down or doesn't exist"

    except OSError as error:
        if error.errno == 113:
            return "host is down or doesn't exist"

    except (ConnectionRefusedError, TimeoutError):
        pass

    return "host is up"
