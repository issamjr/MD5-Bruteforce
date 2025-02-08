import hashlib
import argparse
import logging
import threading
from tqdm import tqdm
from colorama import Fore
import os
import sys

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Global flag to indicate when the hash is found
found_flag = threading.Event()

# Function to hash a word with the specified algorithm
def hash_word(word, algorithm):
    if algorithm == 'md5':
        return hashlib.md5(word.encode('utf-8')).hexdigest()
    elif algorithm == 'sha1':
        return hashlib.sha1(word.encode('utf-8')).hexdigest()
    elif algorithm == 'sha256':
        return hashlib.sha256(word.encode('utf-8')).hexdigest()
    else:
        raise ValueError(f"Unsupported algorithm: {algorithm}")

# Function to crack the hash using brute force
def crack_hash(hash_to_crack, wordlist, algorithm, thread_id, lock, total_lines):
    print(f"{Fore.CYAN}[Thread-{thread_id}] Starting...\n")
    with open(wordlist, "r", encoding="utf-8", errors="ignore") as f:
        # Initialize the progress bar
        progress_bar = tqdm(total=total_lines, desc=f"Thread-{thread_id} Progress", ncols=100)
        for line in f:
            if found_flag.is_set():
                return  # Exit thread early if hash is found

            word = line.strip()
            hashed_word = hash_word(word, algorithm)
            progress_bar.update(1)
            if hashed_word == hash_to_crack:
                with lock:
                    print(f"\n\n{Fore.GREEN}[+] Found: {word} -> {hashed_word}{Fore.REST}\n")
                    #logging.info(f"Found: {word} -> {hashed_word}")
                    found_flag.set()  # Set the flag to stop all threads
                    sys.exit()  # Exit the program
        progress_bar.close()
    print(f"{Fore.YELLOW}[Thread-{thread_id}] Completed scanning the wordlist.\n")

# Function to divide the wordlist into chunks for threading
def divide_wordlist(wordlist, num_threads):
    with open(wordlist, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    chunk_size = len(lines) // num_threads
    chunks = [lines[i:i + chunk_size] for i in range(0, len(lines), chunk_size)]

    # Write each chunk to a temporary file to pass to threads
    chunk_files = []
    for i, chunk in enumerate(chunks):
        chunk_file = f"chunk_{i}.txt"
        with open(chunk_file, "w", encoding="utf-8") as f:
            f.writelines(chunk)
        chunk_files.append(chunk_file)

    return chunk_files

# Main function to execute the brute force attack
def main():
    print(r"""
    __  _____               __      
   /  |/  / /_  _______  __/ /____  
  / /|_/ / __ \/ ___/ / / / __/ _ \ 
 / /  / / /_/ / /  / /_/ / /_/  __/ 
/_/  /_/_.___/_/   \__,_/\__/\___/  
            @Code By issam Junior
    """)

    parser = argparse.ArgumentParser(description="MD5 Brute Force Cracker")
    parser.add_argument('hash', type=str, help="The MD5 hash to crack")
    parser.add_argument('-a', '--algorithm', choices=['md5', 'sha1', 'sha256'], default='md5', help="Hashing algorithm to use (default: md5)")
    parser.add_argument('wordlist', type=str, help="Path to the wordlist file")
    parser.add_argument('-t', '--threads', type=int, default=4, help="Number of threads to use (default: 4)")

    args = parser.parse_args()

    # Validate wordlist path
    if not os.path.exists(args.wordlist):
        print(f"{Fore.RED}[!] Wordlist file not found at: {args.wordlist}")
        exit(1)

    # Read wordlist to determine total lines
    with open(args.wordlist, "r", encoding="utf-8", errors="ignore") as f:
        total_lines = len(f.readlines())

    # Setup lock for thread synchronization
    lock = threading.Lock()

    # Divide wordlist into chunks and get temporary files
    chunk_files = divide_wordlist(args.wordlist, args.threads)

    # Start threads
    threads = []
    for i, chunk_file in enumerate(chunk_files):
        thread = threading.Thread(target=crack_hash, args=(args.hash, chunk_file, args.algorithm, i + 1, lock, total_lines))
        threads.append(thread)
        thread.start()

    # Join threads
    for thread in threads:
        thread.join()

    # Clean up temporary chunk files
    for chunk_file in chunk_files:
        os.remove(chunk_file)

    print(f"{Fore.GREEN}[+] Finished cracking process.")

if __name__ == '__main__':
    main()
