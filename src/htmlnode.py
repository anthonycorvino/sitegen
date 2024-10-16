class HTMLNode:
    # Represents an HTML node
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        if self.tag is None:
            return self.value or ""
        
        attrs = ""
        if self.props:
            attrs = " ".join(f'{key}="{value}"' for key, value in self.props.items())
            attrs = " " + attrs if attrs else ""
        
        if self.children:
            children_html = "".join(child.to_html() for child in self.children)
            return f"<{self.tag}{attrs}>{children_html}</{self.tag}>"
        elif self.value:
            return f"<{self.tag}{attrs}>{self.value}</{self.tag}>"
        else:
            return f"<{self.tag}{attrs}></{self.tag}>"
    def props_to_html(self):
        if self.props is None:
            return ""
        props_html = ""
        for prop in self.props:
            props_html += f' {prop}="{self.props[prop]}"'
        return props_html

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False
        return(
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
        )


class LeafNode(HTMLNode):
    # Represents a leaf node in the HTML tree
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Invalid HTML: no value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

    def __eq__(self, other):
        return(
                isinstance(other, LeafNode) and
                self.tag == other.tag and
                self.value == other.value and
                self.props == other.props
        )


class ParentNode(HTMLNode):
    # Represents a parent node in the HTML tree
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Invalid HTML: no tag")
        if self.children is None:
            raise ValueError("Invalid HTML: no children")
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"

    def __eq__(self, other):
        return (
            isinstance(other, ParentNode)
            and self.tag == other.tag
            and self.children == other.children
            and self.props == other.props
        )
