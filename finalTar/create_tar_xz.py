import os
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
