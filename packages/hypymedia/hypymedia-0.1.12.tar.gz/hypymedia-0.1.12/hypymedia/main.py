from hypymedia.html_list import tags


# def create_element(
#     tag: str,
#     content: list | str = None,
#     attributes: dict = None,
#     end_tag: bool = True,
# ):
#     attributes_str = " ".join(
#         f'{k}="{v}"' if v is not True else k for k, v in (attributes or {}).items()
#     )
#     tag = tag[:-1] if tag.endswith("_") else tag
#     start_tag = f"<{tag} {attributes_str}".strip() + ">"
#     content_str = "".join(content) if isinstance(content, list) else content or ""
#     end_tag_str = f"</{tag}>" if end_tag else ""

#     return f"{start_tag}{content_str}{end_tag_str}"


# def create_tag_function(tag_name: str, end_tag: bool = True):
#     return lambda content=None, attributes=None: create_element(
#         tag_name, content, attributes, end_tag
#     )


# for tag in tags:
#     tag_name = tag[0]
#     end_tag = tag[1]
#     globals()[tag_name] = create_tag_function(tag_name, end_tag=end_tag)


# Function to create element functions
def create_tag_function(tag_name: str, end_tag: bool = True):
    # Function to create an HTML element
    def element(content=None, attributes=None):
        # Convert attributes dictionary to attribute string
        attributes_str = " ".join(
            f'{k}="{v}"' if v is not True else k for k, v in (attributes or {}).items()
        )

        # Remove trailing underscore from the tag if present
        tag = tag_name[:-1] if tag_name.endswith("_") else tag_name

        # Build the start tag
        start_tag = f"<{tag} {attributes_str}>"

        # Build the end tag if required
        end_tag_str = f"</{tag}>" if end_tag else ""

        # Combine start tag, content, and end tag to form the complete element
        return f"{start_tag}{content}{end_tag_str}"

    # Return the element function
    return element


# Dynamically create element functions based on the tags list
for tag_name, end_tag in tags:
    # Create the element function using the create_tag_function
    globals()[tag_name] = create_tag_function(tag_name, end_tag=end_tag)
