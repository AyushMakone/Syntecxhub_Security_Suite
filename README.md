Security Suite
Project Theme: Desktop Cybersecurity Utility Kit

1. Project Overview and Features:
This project is a standalone, multi-module desktop application built using Python and the Tkinter framework. It integrates core security tools to demonstrate proficiency in network concurrency, secure local storage, and automated enumeration techniques.

The suite includes three primary functional modules:
Module
Purpose
Core Technology
Key Functionality
TCP Port Scanner
Network reconnaissance
Sockets & Multi-threading
Identifies open ports on a target host.
Encrypted Password Vault
Secure data management
Symmetric Cryptography (AES)
Stores credentials encrypted on the local disk.
Subdomain Enumerator
DNS reconnaissance
HTTP Requests & Wordlists
Brute-forces potential subdomains for a target URL.

2. Technical Deep Dive: How the Tools Work
The application is structured to separate the Graphical User Interface (GUI) from the core security logic, utilizing Python's threading capabilities to ensure the UI remains responsive even during lengthy network operations.

2.1. TCP Port Scanner
This module is designed for rapid, efficient network analysis, adhering to best practices for concurrent socket operations.

Concurrency for Speed: To minimize scan time, the tool employs a thread pool (up to 200 threads). Ports are loaded into a queue.Queue, and each thread simultaneously pulls a port from the queue to test it.

Non-Blocking Check: Each test uses the socket.connect_ex() function. This is preferred over standard connect() because it immediately returns an error code (0 for success) rather than raising an exception for closed ports, which is much faster and cleaner to handle.

Time Control: A short socket.settimeout(1.0) is set on each socket, ensuring threads quickly abandon connection attempts to closed or filtered ports, maintaining scan speed.

2.2. Encrypted Password Vault
This module provides a critical demonstration of secure local data management by ensuring credentials are never stored in plain text.

Key Generation (PBKDF2): The Master Password entered by the user is not used directly. Instead, it is passed through a PBKDF2HMAC (Password-Based Key Derivation Function 2) algorithm with a static salt and 100,000 iterations. This process securely derives a robust 32-byte cryptographic key from the user's input.

Symmetric Encryption (Fernet): The derived key is then used by the Fernet library (which implements symmetric AES-128 in CBC mode) to encrypt the user's data (usernames, passwords).

Secure Storage: The encrypted JSON data is written to a binary file (passwords.enc).

Security Principle: The data can only be decrypted if the user provides the correct Master Password, allowing the exact same key to be re-derived. Any mismatch results in a decryption failure and prevents access, safeguarding the vault.

2.3. Subdomain Enumerator
This tool uses a common reconnaissance technique to discover hidden subdomains of a target domain.

Brute-Force Attack: The tool iterates through a predefined list of common subdomain prefixes (the wordlist), combining each prefix with the target domain (e.g., www.example.com, mail.example.com, api.example.com).

Resolution Check: For each generated URL, the tool sends an HTTP GET request. If the request returns a successful status code (less than 400), it means the subdomain is active and resolving, and is reported as found.

3. Setup and Execution
Prerequisites

Python 3.x
Required libraries listed in requirements.txt (cryptography, requests).

Step 1: Prepare the Environment
# Clone the repository (or download the files)
git clone [YOUR_REPO_URL]
cd [PROJECT_FOLDER_NAME]

# Create and activate a virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate

Step 2: Install Dependencies
pip install -r requirements.txt

Step 3: Run the Application
python gui/main.py

4. Project Structure 

[PROJECT_FOLDER_NAME]/
│
├── gui/
│   └── main.py                # The main Tkinter GUI (View/Controller)
│
├── port_scanner/
│   └── scanner.py             # Core socket and threading logic
│
├── password_manager/
│   ├── vault.py               # Encryption/Decryption logic
│   └── passwords.enc          # (Generated) Encrypted vault data
│
├── subdomain_finder/
│   ├── finder.py              # Logic for brute-forcing subdomains
│   └── wordlist.txt           # Default list of common subdomains
│
├── vuln_scanner/
│   └── vuln_scanner.py        # (Bonus) Basic banner grabbing & header analysis
│
├── requirements.txt           # Project dependencies
├── .gitignore                 # Specifies files to ignore by Git
└── README.md                  # Project documentation (This file)
