import uuid
import yaml
import argparse
import os

# Create the argument parser
parser = argparse.ArgumentParser(description="Rename files in a directory to start with a specific prefix.")
parser.add_argument("-d", "--directory_path", required=True, help="Destination directory")
args = parser.parse_args()

def generate_lowercase_uuid():
    # Generate a lowercase UUID similar to `uuidgen | tr "[:upper:]" "[:lower:]"`
    return str(uuid.uuid4())

def process_yaml_files(directory):
    # Traverse the directory and find all YAML files
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(('.yaml', '.yml')):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    lines = f.readlines()

                # Check if 'id' field already exists
                id_exists = any(line.strip().startswith('id:') for line in lines)

                if not id_exists:
                    # Generate a new UUID
                    new_id = generate_lowercase_uuid()
                    # Insert the ID as the second line
                    lines.insert(1, f'id: {new_id}\n')

                    # Write back the updated content to the file
                    with open(file_path, 'w') as f:
                        f.writelines(lines)
                    print(f"Added ID to {file_path}")

if __name__ == "__main__":
    process_yaml_files(args.directory_path)