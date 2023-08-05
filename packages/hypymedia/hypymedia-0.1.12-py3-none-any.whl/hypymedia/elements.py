# curryhtml/elements.py
from html_list import tags


def element(tag_name, end_tag=True):
    def inner(*args):
        attributes = args[0] if args and isinstance(args[0], dict) else None
        content_args = args if not attributes else args[1:]
        content = "".join(map(str, content_args))

        attributes_str = (
            " ".join(
                f'{k}="{v}"' if v is not True else k
                for k, v in (attributes or {}).items()
            )
            if attributes
            else ""
        )

        end_tag_str = f"</{tag_name}>" if end_tag else ""

        return f'<{tag_name}{" " + attributes_str if attributes_str else ""}>{content}{end_tag_str or ""}'  # noqa: E501

    return inner


for tag in tags:
    function_name = f"{tag[0]}"
    tag_name = tag[0][:-1]
    end_tag = tag[1]

    globals()[function_name] = element(tag_name, end_tag)
