import ipaddress
import re
import socket
import threading
import time
from clear import clear

CYAN = "\033[1;36m"

def dolphin_thread(host,subnet=False):
    global host_list
    if not subnet:
        try:
            tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp_socket.settimeout(15)
            tcp_socket.connect((host,80))
            tcp_socket.close()

        except socket.gaierror:
            return False

        except OSError as error:
            if error.errno == 113:
                return False

        except (ConnectionRefusedError, TimeoutError):
            pass

        return True

    else:
        try:
            tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp_socket.settimeout(15)
            tcp_socket.connect((host,80))
            tcp_socket.close()

        except socket.gaierror:
            return False

        except OSError as error:
            if error.errno == 113:
                return False

        except (ConnectionRefusedError, TimeoutError):
            pass

        host_list.append(host)

def dolphin_scanner(host,delay=0,scans=256):
    global host_list
    clear()
    print(CYAN + "dolphin is scanning")
    host_list = []
    host = host.replace("https://", "")
    host = host.replace("http://", "")
    if not re.search("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{2}", host):
        return dolphin_thread(host)

    elif re.search("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{2}", host):
        ip_range = []
        for ip in ipaddress.IPv4Network(host, strict=False):
            ip_range.append(ip)

        thread_tracker = 0
        thread_list = []
        start = time.time()
        for ip in ip_range:
            time.sleep(delay)
            thread_tracker += 1
            my_thread = threading.Thread(target=dolphin_thread, args=(str(ip),True))
            my_thread.start()
            thread_list.append(my_thread)
            if thread_tracker == scans:
                thread_tracker = 0
                for thread in thread_list:
                    thread.join()

                thread_list = []

        end = time.time()
        print(str(end - start) + " seconds")
        host_list = list(set(host_list[:]))
        host_list.sort()
        return host_list
