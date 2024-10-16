import unittest
from delimiter import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_link,
    split_nodes_image,
    text_to_textnodes,
    markdown_to_blocks,
    block_to_block_type,
    markdown_to_html_node,
)

from textnode import TextNode, TextType
from htmlnode import HTMLNode, ParentNode, LeafNode

class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        self.assertEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev)"
        )
        self.assertListEqual(
            [
                ("link", "https://boot.dev"),
                ("another link", "https://blog.boot.dev"),
            ],
            matches,
        )

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://blog.boot.dev"),
                TextNode(" with text that follows", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        nodes = text_to_textnodes(
            "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        )

        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )


class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_block_to_block_type(self):
        block = "This is **bolded** paragraph"
        self.assertEqual(block_to_block_type(block), "paragraph")

        block = "> This is a quote"
        self.assertEqual(block_to_block_type(block), "quote")

        block = "- This is a list"
        self.assertEqual(block_to_block_type(block), "unordered list")

        block = "1. This is a list"
        self.assertEqual(block_to_block_type(block), "ordered list")

        block = "```python\nprint('hello')\n```"
        self.assertEqual(block_to_block_type(block), "code")
    
    def test_markdown_to_html_node(self):
        test_cases = [
            # Test for headings
            {
                "input": "# Heading",
                "expected": HTMLNode("div", [ParentNode("h1", text_to_textnodes("# Heading"))])
            },
            {
                "input": "## Subheading",
                "expected": HTMLNode("div", [ParentNode("h2", text_to_textnodes("## Subheading"))])
            },
            {
                "input": "### Another Heading",
                "expected": HTMLNode("div", [ParentNode("h3", text_to_textnodes("### Another Heading"))])
            },
            # Test for code blocks
            {
                "input": "```\nprint('Hello World')\n```",
                "expected": HTMLNode("div", [ParentNode("pre", [LeafNode("code", "print('Hello World')")])])
            },
            # Test for quote blocks
            {
                "input": "> This is a quote\n> Another line of the quote",
                "expected": HTMLNode("div", [ParentNode("blockquote", text_to_textnodes("> This is a quote\n> Another line of the quote"))])
            },
            # Test for unordered lists
            {
                "input": "- Item 1\n- Item 2\n- Item 3",
                "expected": HTMLNode("div", [
                    ParentNode("ul", [
                        ParentNode("li", text_to_textnodes("Item 1")),
                        ParentNode("li", text_to_textnodes("Item 2")),
                        ParentNode("li", text_to_textnodes("Item 3")),
                    ])
                ])
            },
            {
                "input": "* Item A\n* Item B",
                "expected": HTMLNode("div", [
                    ParentNode("ul", [
                        ParentNode("li", text_to_textnodes("Item A")),
                        ParentNode("li", text_to_textnodes("Item B")),
                    ])
                ])
            },
            # Test for ordered lists
            {
                "input": "1. First item\n2. Second item\n3. Third item",
                "expected": HTMLNode("div", [
                    ParentNode("ol", [
                        ParentNode("li", text_to_textnodes("First item")),
                        ParentNode("li", text_to_textnodes("Second item")),
                        ParentNode("li", text_to_textnodes("Third item")),
                    ])
                ])
            },
            # Test for paragraphs
            {
                "input": "This is a simple paragraph.",
                "expected": HTMLNode("div", [ParentNode("p", text_to_textnodes("This is a simple paragraph."))])
            },
            {
                "input": "No special formatting here.",
                "expected": HTMLNode("div", [ParentNode("p", text_to_textnodes("No special formatting here."))])
            },
            # Test for invalid ordered list
            {
                "input": "1. First item\n3. Second item",
                "expected": HTMLNode("div", [ParentNode("p", text_to_textnodes("1. First item\n3. Second item"))])  # treated as paragraph
            },
            # Test for empty input
            {
                "input": "",
                "expected": HTMLNode("div", [])  # Empty div for empty input
            },
        ]

        for i, case in enumerate(test_cases):
            result = markdown_to_html_node(case["input"])
            if result != case["expected"]:
                print(f"Test case {i + 1} failed")
                print(f"Expected: {case['expected']}")
                print(f"Got: {result}")
            self.assertEqual(result, case["expected"], f"Test case {i + 1} failed")


if __name__ == "__main__":
    unittest.main()

