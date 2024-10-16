import os
import shutil

def copy_files(source, destination):
    os.makedirs(destination, exist_ok=True)

    for root, dirs, files in os.walk(source):
        for file in files:
            if '.git' in root:
                continue
            source_file = os.path.join(root, file)

            relative_path = os.path.relpath(source_file, source)
            destination_file = os.path.join(destination, relative_path)

            os.makedirs(os.path.dirname(destination_file), exist_ok=True)

            shutil.copy(source_file, destination_file)
            print(f"Moved {source_file} to {destination_file}")

def main():

    copy_files("static", "public")



if __name__ == "__main__":
    main()

