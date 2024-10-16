from htmlnode import LeafNode
from enum import Enum


class TextType(Enum):
    # Represents the type of text node
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    # Represents a text node in the markdown tree
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type.value
        self.url = url

    def __eq__(self, other):
        return (
            self.text_type == other.text_type
            and self.text == other.text
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

    def to_html(self):
        if self.text_type == "text":
            return self.text
        elif self.text_type == "bold":
            return f"<b>{self.text}</b>"
        elif self.text_type == "italic":
            return f"<i>{self.text}</i>"
        elif self.text_type == "code":
            return f"<code>{self.text}</code>"
        elif self.text_type == "link":
            return f'<a href="{self.url}">{self.text}</a>'
        elif self.text_type == "image":
            return f'<img src="{self.url}" alt="{self.text}">'
        else:
            raise ValueError(f"Invalid text_type: {self.text_type}")

def text_node_to_html_node(text_node):
    # Convert a text node to an HTML node
    if text_node.text_type == TextType.TEXT.value:
        return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.BOLD.value:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.ITALIC.value:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.CODE.value:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.LINK.value:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == TextType.IMAGE.value:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    raise ValueError(f"Invalid text type: {text_node.text_type}")
