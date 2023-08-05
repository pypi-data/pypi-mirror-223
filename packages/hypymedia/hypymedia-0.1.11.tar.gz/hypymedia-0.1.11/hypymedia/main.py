from hypymedia.html_list import tags


def create_element(
    tag: str,
    content: list | str = None,
    attributes: dict = None,
    end_tag: bool = True,
):
    attributes_str = " ".join(
        f'{k}="{v}"' if v is not True else k for k, v in (attributes or {}).items()
    )
    tag = tag[:-1] if tag.endswith("_") else tag
    start_tag = f"<{tag} {attributes_str}".strip() + ">"
    content_str = "".join(content) if isinstance(content, list) else content or ""
    end_tag_str = f"</{tag}>" if end_tag else ""

    return f"{start_tag}{content_str}{end_tag_str}"


def create_tag_function(tag_name: str, end_tag: bool = True):
    return lambda content=None, attributes=None: create_element(
        tag_name, content, attributes, end_tag
    )


for tag in tags:
    tag_name = tag[0]
    end_tag = tag[1]
    globals()[tag_name] = create_tag_function(tag_name, end_tag=end_tag)
