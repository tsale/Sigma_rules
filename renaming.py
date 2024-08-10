import os
import sys
import argparse
import os

# Create the argument parser
parser = argparse.ArgumentParser(description="Rename files in a directory to start with a specific prefix.")
parser.add_argument("-d", "--destination_dir", required=True, help="Destination directory")
parser.add_argument("-p", "--prefix", required=True, help="Prefix")
args = parser.parse_args()

def rename_files(destination_dir, prefix):
    print(f"Renaming files in directory: {destination_dir} with prefix: {prefix}")
    for root, _, files in os.walk(destination_dir):
        for file in files:
            # Get the current file name
            current_name = os.path.join(root, file)
            print(f"Current file: {current_name}")

            # Create the new file name
            new_name = os.path.join(root, prefix + file)
            print(f"New file name: {new_name}")

            # Rename the file
            os.rename(current_name, new_name)
            print(f"Renamed {current_name} to {new_name}")

if __name__ == "__main__":
    # Call the function to rename the directories
    rename_files(args.destination_dir, args.prefix)