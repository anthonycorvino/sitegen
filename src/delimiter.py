import re
from textnode import TextNode, TextType
from htmlnode import LeafNode, ParentNode, HTMLNode

def block_to_block_type(block):
    # Find the type of block and return it as a string
    # If there is no match, return "paragraph"
    lines = block.splitlines()

    if len(lines) > 0:
        heading_level = 0
        while heading_level < 6 and lines[0][heading_level] == "#":
            heading_level += 1
        if heading_level > 0 and len(lines[0]) > heading_level and lines[0][heading_level] == " ":
            return "heading"

    if block.startswith("```") and block.endswith("```"):
        return "code"

    if all(line.startswith(">") for line in lines):
        return "quote"

    if all(line.startswith("- ") or line.startswith("* ") for line in lines):
        return "unordered list"

    if len(lines) > 0 and lines[0].strip().startswith("1. "):
        for i in range(len(lines)):
            expected = i + 1
            line = lines[i].strip()
            if not line.startswith(f"{expected}. "):
                return "paragraph"
        return "ordered list"

    return "paragraph"

def text_to_textnodes(text):
    # Split the text into text nodes based on markdown delimiters

    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    # Split the text nodes based on the delimiter and return the new nodes

    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT.value:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text):
    # Extract the images from the text and return them as a list of tuples

    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    # Extract the links from the text and return them as a list of tuples

    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def split_nodes_image(old_nodes):
    # Split the text nodes based on the image markdown and return the new nodes

    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT.value:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    # Split the text nodes based on the link markdown and return the new nodes

    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT.value:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def markdown_to_blocks(markdown):
    # Split the markdown into blocks and return them as a list

    blocks = markdown.split("\n\n")
    filtered_blocks = []

    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def markdown_to_html_node(markdown):
    # Convert markdown to an HTML node

    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == "heading":
            level = block.count("#")
            content = block[level:].strip()
            nodes.append(ParentNode(f"h{level}", text_to_textnodes(content)))
        elif block_type == "code":
            code_content = block[3:-3].strip()
            code_node = LeafNode("code", code_content)
            pre_node = ParentNode("pre", [code_node])
            nodes.append(pre_node)
        elif block_type == "quote":
            quote_content = block[1:].strip()
            nodes.append(ParentNode("blockquote", text_to_textnodes(quote_content)))
        elif block_type == "unordered list":
            lines = block.splitlines()
            children = [ParentNode("li", text_to_textnodes(line[2:])) for line in lines]
            nodes.append(ParentNode("ul", children))
        elif block_type == "ordered list":
            lines = block.splitlines()
            children = []
            for line in lines:
                line_content = line[line.index('.') + 2:]
                children.append(ParentNode("li", text_to_textnodes(line_content)))
            nodes.append(ParentNode("ol", children))
        elif block_type == "paragraph":
            nodes.append(ParentNode("p", text_to_textnodes(block)))
    return ParentNode("div", nodes)
