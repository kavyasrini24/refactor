import os
from config import get_dynamic_file_paths, extract_variables, search_in_xml, search_in_properties
from utils import extract_properties, compare_and_write_differences

# Main logic
def main():
    (application_properties_file, environment_properties_file, output_properties_file, 
     missing_properties_file, environment_op_properties_file, test_data_dir) = get_dynamic_file_paths()

    variables = extract_variables(application_properties_file)

    # Search for variable values in all XML files
    for file_name in os.listdir(test_data_dir):
        if file_name.endswith('.xml'):
            file_path = os.path.join(test_data_dir, file_name)
            variables = search_in_xml(file_path, variables)

    # Search for variable values in environment.properties
    variables = search_in_properties(environment_properties_file, variables)

    # Write found variables to output_properties.properties
    with open(output_properties_file, 'w') as f:
        for key, values in variables.items():
            for value in values:
                f.write(f'{key}={value}\n')

    # Get all the missing variables and write to missing_properties.properties
    with open(missing_properties_file, 'w') as f:
        for key, values in variables.items():
            if not values:
                f.write(f'{key}=MISSING\n')

    # Compare application.properties variables with environment.properties keys and write differences to environment_op.properties
    compare_and_write_differences(application_properties_file, environment_properties_file, environment_op_properties_file)
