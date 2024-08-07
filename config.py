import os
import re
import xml.etree.ElementTree as ET
from collections import defaultdict

# Define dynamic file paths
def get_dynamic_file_paths():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    test_data_dir = os.path.join(base_dir, 'test_data')
    application_properties_file = os.path.join(test_data_dir, 'application.properties')
    environment_properties_file = os.path.join(test_data_dir, 'environment.properties')
    output_properties_file = os.path.join(base_dir, 'output_properties.properties')
    missing_properties_file = os.path.join(base_dir, 'missing_properties.properties')
    environment_op_properties_file = os.path.join(base_dir, 'environment_op.properties')
    return (application_properties_file, environment_properties_file, output_properties_file, 
            missing_properties_file, environment_op_properties_file, test_data_dir)

# Extract variable names from application.properties
def extract_variables(file_path):
    variables = defaultdict(set)
    try:
        with open(file_path, 'r') as f:
            for line in f:
                match = re.match(r'.*=\${(\w+)}', line)
                if match:
                    key = match.group(1)
                    variables[key] = set()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    return variables

# Search for variable values in XML files
def search_in_xml(file_path, variables):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        for prop in root.findall('.//property'):
            name_elem = prop.find('name')
            value_elem = prop.find('value')
            if name_elem is not None and value_elem is not None:
                name = name_elem.text
                value = value_elem.text
                if name in variables:
                    variables[name].add(value)
    except Exception as e:
        print(f"Error processing XML file {file_path}: {e}")
    return variables

# Search for variable values in properties files
def search_in_properties(file_path, variables):
    try:
        with open(file_path, 'r') as f:
            for line in f:
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    if key in variables:
                        variables[key].add(value)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    return variables
