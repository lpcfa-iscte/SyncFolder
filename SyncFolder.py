import os
import hashlib
import argparse
import time
from datetime import datetime

def get_file_hash(file_path):
    """Calculate MD5 hash of a file."""
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hasher.update(chunk)
    return hasher.hexdigest()

def copy_file(source_path, replica_path, file_name):
    """Copy a file from source to replica."""
    with open(os.path.join(source_path, file_name), 'rb') as src_file:
        with open(os.path.join(replica_path, file_name), 'wb') as dest_file:
            dest_file.write(src_file.read())

def delete_file(replica_path, file_name):
    """Delete a file from replica."""
    os.remove(os.path.join(replica_path, file_name))

def sync_folders(source_path, replica_path, log_file):
    """Synchronize source folder to replica folder."""
    # Ensure replica folder exists
    if not os.path.exists(replica_path):
        os.makedirs(replica_path)

    # Get list of files in source folder
    source_files = set(os.listdir(source_path))

    # Get list of files in replica folder
    replica_files = set(os.listdir(replica_path))

    # Files to be copied or updated
    to_copy = source_files - replica_files

    # Files to be deleted
    to_delete = replica_files - source_files

    # Copy or update files
    for file_name in to_copy:
        copy_file(source_path, replica_path, file_name)
        log_message = f"{datetime.now()} - Copied: {file_name}\n"
        print(log_message)
        log_file.write(log_message)

    # Delete files
    for file_name in to_delete:
        delete_file(replica_path, file_name)
        log_message = f"{datetime.now()} - Deleted: {file_name}\n"
        print(log_message)
        log_file.write(log_message)

def main():
    parser = argparse.ArgumentParser(description="Synchronize two folders.")
    parser.add_argument("source", help="Path to source folder")
    parser.add_argument("replica", help="Path to replica folder")
    parser.add_argument("interval", type=int, help="Synchronization interval in seconds")
    parser.add_argument("log", help="Path to log file")

    args = parser.parse_args()

    while True:
        with open(args.log, 'a') as log_file:
            sync_folders(args.source, args.replica, log_file)
        time.sleep(args.interval)

if __name__ == "__main__":
    main()
