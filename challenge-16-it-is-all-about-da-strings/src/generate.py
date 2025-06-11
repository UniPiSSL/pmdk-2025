#! /usr/bin/env python3
import os

# File paths
template_file = "binary.template.c"
flag_file = "flag.txt"
output_file = "binary.c"

def escape_c_string(flag):
    """
    Escapes invalid characters in the flag to make it safe for C strings.
    """
    escaped_flag = (
        flag.replace("\\", "\\\\")  # Escape backslashes
            .replace("\"", "\\\"")  # Escape double quotes
            .replace("\n", "\\n")   # Escape newlines
            .replace("\t", "\\t")   # Escape tabs
    )
    return escaped_flag

try:
    # Read the flag value
    with open(flag_file, "r") as f:
        flag = f.read().strip()

    # Escape invalid characters in the flag
    safe_flag = escape_c_string(flag)

    # Read the template content
    with open(template_file, "r") as f:
        template_content = f.read()

    # Replace the placeholder with the escaped flag
    updated_content = template_content.replace("{{FLAG}}", f'{safe_flag}')

    # Write the updated content to the output file
    with open(output_file, "w") as f:
        f.write(updated_content)

    print(f"Successfully created {output_file} with the embedded flag.")
except FileNotFoundError as e:
    print(f"Error: {e}. Please ensure the file exists.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
