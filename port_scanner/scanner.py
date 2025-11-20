import socket
import threading
from queue import Queue

def check_port(target, port, result_list):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.0)
        result = s.connect_ex((target, port))
        if result == 0:
            result_list.append(port)
        s.close()
    except:
        pass

def scan_range(target, start, end, threads=100):
    open_ports = []
    q = Queue()
    
    # Populate queue
    for port in range(start, end + 1):
        q.put(port)

    def worker():
        while not q.empty():
            port = q.get()
            check_port(target, port, open_ports)
            q.task_done()

    # Start threads
    thread_list = []
    num_threads = min(threads, (end - start) + 1)
    
    for _ in range(num_threads):
        t = threading.Thread(target=worker)
        t.daemon = True
        t.start()
        thread_list.append(t)

    for t in thread_list:
        t.join()

    return sorted(open_ports)

def scan_list(target, port_list):
    open_ports = []
    threads_list = []

    for port in port_list:
        t = threading.Thread(target=check_port, args=(target, port, open_ports))
        t.daemon = True
        t.start()
        threads_list.append(t)

    for t in threads_list:
        t.join()

    return sorted(open_ports)