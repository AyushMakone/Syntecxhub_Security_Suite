Unified Security Tool Suite

Project Type: Standalone Desktop Utility Kit

1. Project Overview and Features

This project serves as a comprehensive demonstration of foundational cybersecurity tools built into a single, cohesive desktop application. It showcases proficiency in network concurrency, secure local storage, and automated enumeration techniques, directly addressing the core tasks of a typical cybersecurity internship curriculum:

Module

Core Task Addressed

Functionality

Technical Focus

TCP Port Scanner

Network Reconnaissance

Identifies open TCP ports on a target host.

Socket Programming, Multi-threading

Encrypted Password Vault

Secure Data Management

Stores credentials encrypted on the local disk.

Symmetric Cryptography (AES), Key Derivation (PBKDF2)

Subdomain Enumerator

DNS Reconnaissance

Brute-forces potential subdomains for a target domain.

HTTP Requests, File I/O

Vulnerability Scanner

Basic Fingerprinting

Retrieves and analyzes host banners and HTTP headers.

Requests, Basic String Analysis

2. Technical Deep Dive: How the Tools Work

The application follows a modern architecture that separates the user interface logic from the core security operations. The crucial use of the threading module ensures the GUI remains responsive while time-consuming network scans are running in the background.

2.1. TCP Port Scanner

This module is designed for efficient network analysis using low-level socket operations, fulfilling the requirements for Project 1 (Port Scanner) from the task list.

Concurrency for Speed: To minimize the duration of the scan, the scanner.py module uses a thread pool (up to 200 threads). All ports to be scanned are loaded into a queue.Queue. Each thread simultaneously pulls a port from the queue, allowing hundreds of checks to occur in parallel.

Non-Blocking Check: Each test employs the socket.connect_ex() function. This method is crucial as it returns an error code (0 for success) for closed ports, which is significantly faster and more stable than using socket.connect() which would raise an exception.

Time Control: A short socket.settimeout(1.0) is applied to the socket connection. This ensures that threads quickly fail on filtered or closed ports, preventing resource waste and maintaining scan speed.

2.2. Encrypted Password Vault

This module ensures secure, persistent storage for sensitive credentials, aligning with the requirements of Project 2 (Password Manager).

Secure Key Generation (PBKDF2): The Master Password is never stored. Instead, it is converted into a robust cryptographic key using the PBKDF2HMAC (Password-Based Key Derivation Function 2) algorithm. This process incorporates a static salt and a high iteration count (e.g., 100,000) to resist brute-force attacks and create a derived key suitable for encryption.

Symmetric Encryption (Fernet/AES): The derived key is then used by the Fernet library (which implements symmetric AES-128 in CBC mode) to encrypt the user's data (usernames, passwords) before it is written to the disk.

Storage & Retrieval: The encrypted data is stored in a binary file (passwords.enc). During retrieval, the user must supply the correct Master Password, which is used to re-derive the exact same key required to decrypt the data successfully.

2.3. Subdomain Enumerator

This tool utilizes a common technique to map the surface area of a target domain.

Brute-Force Method: The enumerator works by iterating through a wordlist (wordlist.txt) containing common subdomain prefixes (e.g., www, mail, api, dev).

DNS Resolution Check: For each prefix, the tool constructs a full URL (e.g., https://mail.targetdomain.com) and attempts an HTTP request. If the request resolves and returns a non-error status code (i.e., the subdomain exists and is active), it is reported as a positive result.

3. Setup and Execution

Prerequisites

Python 3.x

Required libraries: cryptography, requests (as listed in requirements.txt).

Step 1: Clone the Repository & Setup Environment

# Clone the repository (or download the files)
git clone [YOUR_REPO_URL]
cd [PROJECT_FOLDER_NAME]

# Create and activate a virtual environment (highly recommended)
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
│   └── main.py                # The main Tkinter GUI and application entry point
│
├── port_scanner/
│   └── scanner.py             # Implementation of the TCP Port Scanner logic
│
├── password_manager/
│   ├── vault.py               # Implementation of encryption/decryption logic
│   └── passwords.enc          # (Generated) Encrypted vault data file
│
├── subdomain_finder/
│   ├── finder.py              # Implementation of subdomain enumeration
│   └── wordlist.txt           # Default list of common subdomain prefixes
│
├── vuln_scanner/
│   └── vuln_scanner.py        # Implementation of basic banner/header analysis
│
├── requirements.txt           # List of required Python libraries
└── README.md                  # Project documentation (This file)
