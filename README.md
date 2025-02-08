# MD5 Brute Force Cracker Tool
    
    This is a Python-based brute force tool designed to crack MD5 hashes. It supports multi-threading and allows the use of various hashing algorithms (MD5, SHA1, SHA256). It reads a wordlist, hashes each word, and compares it against the provided hash until a match is found.
    
    ## Features:
    - Multi-threading support for faster cracking
    - Supports MD5, SHA1, and SHA256 hashing algorithms
    - Uses tqdm for progress bar visualization
    - Can handle large wordlists efficiently by chunking them for thread processing
    
    ## Requirements:
    - Python 3.x
    - `tqdm` and `colorama` libraries
    
    You can install the required libraries with:
    
    ```bash
    pip install tqdm colorama
    ```
    
    ## Usage:
    
    To use the tool, simply run the following command:
    
    ```bash
    python brute-force.py <hash_to_crack> -a <algorithm> <wordlist_path> -t <number_of_threads>
    ```
    
    Example:
    
    ```bash
    python brute-force.py e0f8bfa154ce04d853acffd6feeeed94 -a md5 /usr/share/wordlists/rockyou.txt -t 4
    ```
    
    ## Parameters:
    - `hash_to_crack`: The hash that you want to crack.
    - `-a, --algorithm`: The hash algorithm to use (`md5`, `sha1`, `sha256`).
    - `wordlist_path`: Path to the wordlist file (e.g., `rockyou.txt`).
    - `-t, --threads`: The number of threads to use for the brute force attack (default is 4).
    
    ## Example Output:
    
    ```bash
    [Thread-1] Starting...
    Thread-1 Progress:  25%|███████▌                      | 3586098/14344392 [01:04<03:13, 55501.67it/s]
    [Thread-1] Completed scanning the wordlist.           | 3412457/14344392 [01:04<03:39, 49869.28it/s]
    [Thread-2] Starting...
    [Thread-2] Completed scanning the wordlist.
    [Thread-3] Starting...
    [Thread-3] Completed scanning the wordlist.
    [Thread-4] Starting...
    [Thread-4] Completed scanning the wordlist.
    [+] Finished cracking process.
    ```
    
    ## License:
    This tool is for educational and personal use only. Please do not use it for illegal activities.
    
