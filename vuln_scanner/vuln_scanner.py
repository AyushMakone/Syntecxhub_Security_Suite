import socket
import requests

def grab_banner(ip, port):
    try:
        s = socket.socket()
        s.settimeout(2)
        s.connect((ip, int(port)))
        banner = s.recv(1024).decode().strip()
        s.close()
        return banner
    except:
        return "No banner found."

def scan_http_headers(url):
    try:
        if not url.startswith("http"):
            url = "http://" + url
        response = requests.get(url, timeout=2)
        return dict(response.headers)
    except Exception as e:
        return {"Error": str(e)}