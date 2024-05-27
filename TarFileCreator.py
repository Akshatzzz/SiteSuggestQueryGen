import os

# Define the directory and file names
directory_name = 'finalTar'
file_name = 'create_tar_xz.py'
file_path = os.path.join(directory_name, file_name)

# Ensure the directory exists
os.makedirs(directory_name, exist_ok=True)

# Define the content of the Python script
script_content = """import os
import tarfile

def create_tar_xz(source_folder, output_filename):
    with tarfile.open(output_filename, "w:xz") as tar:
        for root, _, files in os.walk(source_folder):
            for file in files:
                file_path = os.path.join(root, file)
                tar.add(file_path, arcname=file)

if __name__ == "__main__":
    # Specify the source folder and the output file name
    source_folder = '/Users/apple/PycharmProjects/pythonDb/EvaluatedAssets'
    output_filename = 'smart_suggestions_affiliate_ads_resources-en.tar.xz'

    # Create the tar.xz archive
    create_tar_xz(source_folder, output_filename)
    print(f"All files in {{source_folder}} have been compressed into {{output_filename}}")
"""

# Write the script content to the file
with open(file_path, 'w') as file:
    file.write(script_content)

print(f"Script has been created and saved to {file_path}")
