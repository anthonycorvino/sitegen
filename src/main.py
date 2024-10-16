import os
import shutil
import htmlnode
from delimiter import markdown_to_html_node


def extract_title(markdown):
    # Extract the title from the markdown file
    title = None
    for line in markdown.split("\n"):
        if line.startswith("# "):
            title = line[2:].strip()
            break
    return title

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    # Generate pages recursively from the content directory
    for root, dirs, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith('.md'):
                markdown_path = os.path.join(root, file)
                relative_path = os.path.relpath(markdown_path, dir_path_content)
                dest_path = os.path.join(dest_dir_path, relative_path.replace('.md', '.html'))
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                generate_page(markdown_path, template_path, dest_path)


def generate_page(from_path, template_path, dest_path):
    # Generate a page from a markdown file
    print(f"Generating page {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        markdown = f.read()
    with open(template_path, "r") as t:
        template = t.read()
    html_string = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown) or ""
    html_string = template.replace("{{ Content }}", html_string)
    html_string = html_string.replace("{{ Title }}", title)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as d:
        d.write(html_string)


def copy_files(source, destination):
    # Copy files from source to destination
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

    if os.path.exists("public"):
        shutil.rmtree("public")

    copy_files("static", "public")
    generate_pages_recursive("content", "template.html", "public")


if __name__ == "__main__":
    main()

