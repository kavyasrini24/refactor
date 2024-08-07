from config import extract_variables
# Extract key-value pairs from a properties file
def extract_properties(file_path):
    properties = {}
    try:
        with open(file_path, 'r') as f:
            for line in f:
                if '=' in line:
                    key, value = line.split('=', 1)
                    properties[key.strip()] = value.strip()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    return properties

# Compare variable names from application.properties with keys in environment.properties
def compare_and_write_differences(app_vars_file, env_props_file, output_file):
    app_vars = extract_variables(app_vars_file)
    env_props = extract_properties(env_props_file)
    
    app_keys = set(app_vars.keys())
    env_keys = set(env_props.keys())

    differences = {}
    
    # Variables in application.properties but not in environment.properties
    missing_in_env = app_keys - env_keys
    for key in missing_in_env:
        differences[key] = 'MISSING (not found in env)'

    # Keys in environment.properties but not in application.properties
    extra_in_env = env_keys - app_keys
    for key in extra_in_env:
        differences[key] = f'{env_props[key]} (not found in app)'

    with open(output_file, 'w') as f:
        for key, value in differences.items():
            f.write(f'{key}={value}\n')
