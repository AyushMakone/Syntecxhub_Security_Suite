import requests
import os

DEFAULT_WORDLIST = os.path.join(os.path.dirname(__file__), 'wordlist.txt')

def find_subdomains(domain, wordlist_path=None):
    if not wordlist_path:
        wordlist_path = DEFAULT_WORDLIST
        
    if not os.path.exists(wordlist_path):
        return ["Error: Wordlist file not found."]

    found = []
    try:
        with open(wordlist_path, 'r') as f:
            subs = [line.strip() for line in f if line.strip()]
    except Exception as e:
        return [f"Error reading wordlist: {e}"]

    # Small optimization: use a session
    session = requests.Session()
    
    # Limit for demo purposes if wordlist is huge
    # In a real tool, you'd want to run this threaded
    for sub in subs:
        url = f"http://{sub}.{domain}"
        try:
            resp = session.get(url, timeout=1.0)
            if resp.status_code < 400:
                found.append(f"[+] Found: {url} ({resp.status_code})")
        except requests.ConnectionError:
            pass
        except:
            pass
            
    if not found:
        return ["No subdomains found with current wordlist."]
        
    return found