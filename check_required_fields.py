import yaml
import uuid
from yaml.scanner import ScannerError
import csv
import argparse
import os

# Create the argument parser
parser = argparse.ArgumentParser(description="Rename files in a directory to start with a specific prefix.")
parser.add_argument("-d", "--directory_path", required=True, help="Destination directory")
args = parser.parse_args()

# Define the required fields
required_fields = {
    "title": True,
    "id": True,
    "status": True,
    "description": True,
    "references": True,
    "author": True,
    "date": True,
    "tags": True,
    "logsource": {
        "category": False,
        "product": False,
        "service": False,
        "definition": False,
    },
    "detection": {
        "condition": True,
    },
    "falsepositives": True,
    "level": True,
}

def generate_lowercase_uuid():
    # Generate a lowercase UUID
    return str(uuid.uuid4())

def check_required_fields(yaml_content, required_fields, parent_key=""):
    missing_fields = []
    for key, required in required_fields.items():
        full_key = f"{parent_key}.{key}" if parent_key else key
        if isinstance(required, dict):
            # Nested dictionary, check recursively
            if key in yaml_content:
                missing_fields.extend(check_required_fields(yaml_content[key], required, full_key))
            else:
                missing_fields.append(full_key)
        else:
            if required and key not in yaml_content:
                missing_fields.append(full_key)
    return missing_fields

def process_yaml_files(directory):
    missing_data = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(('.yaml', '.yml')):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r') as f:
                        lines = f.readlines()
                    yaml_content = yaml.safe_load(''.join(lines))

                    # Check if 'id' field exists and add if missing
                    if 'id' not in yaml_content:
                        new_id = generate_lowercase_uuid()
                        lines.insert(1, f'id: {new_id}\n')
                        with open(file_path, 'w') as f:
                            f.writelines(lines)
                        print(f"Added ID to {file_path}")
                        yaml_content['id'] = new_id  # Update the yaml_content with the new ID

                    # Check for missing required fields
                    missing_fields = check_required_fields(yaml_content, required_fields)

                    if missing_fields:
                        missing_data.append({
                            "file": file_path,
                            "missing_fields": ", ".join(missing_fields),
                            "error": "None"
                        })
                        print(f"File: {file_path} is missing fields: {', '.join(missing_fields)}")

                except ScannerError as e:
                    # Handle YAML parsing errors
                    missing_data.append({
                        "file": file_path,
                        "missing_fields": "N/A",
                        "error": f"ScannerError: {str(e)}"
                    })
                    print(f"Error in file {file_path}: ScannerError: {str(e)}")
                except Exception as e:
                    # Handle other unexpected errors
                    missing_data.append({
                        "file": file_path,
                        "missing_fields": "N/A",
                        "error": f"Error: {str(e)}"
                    })
                    print(f"Unexpected error in file {file_path}: {str(e)}")

    return missing_data

def save_to_csv(missing_data, output_file):
    with open(output_file, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["file", "missing_fields", "error"])
        writer.writeheader()
        for data in missing_data:
            writer.writerow(data)

if __name__ == "__main__":
    output_csv = "missing_fields_report.csv"
    
    missing_data = process_yaml_files(args.directory_path)
    
    if missing_data:
        save_to_csv(missing_data, output_csv)
        print(f"Missing fields and error report saved to {output_csv}")
    else:
        print("All YAML files contain the required fields.")