import textwrap


def display_user_details(user, indent=0, parent_is_list=False):
    prefix = " " * indent
    bullet = '* ' if indent == 0 else '- ' if indent == 4 else '→ '

    if indent == 0:
        print(f"{prefix}{'=' * 80}")  # Top level separation line

    for key, value in user.items():
        formatted_key = f"{prefix}{bullet}{key.capitalize()}" if not parent_is_list else prefix.strip()

        if isinstance(value, dict):
            print(f"\n{formatted_key}:")
            display_user_details(value, indent + 4)
        elif isinstance(value, list):
            print(f"\n{formatted_key}:")
            for index, item in enumerate(value):
                print(f"{prefix}    [{index + 1}]:")
                display_user_details(item, indent + 8, parent_is_list=True)
        else:
            # Format specific data types here if needed
            wrapped_text = textwrap.fill(str(value), initial_indent=formatted_key + ": ",
                                         subsequent_indent=' ' * (indent + 4), width=80)
            print(wrapped_text)

    if indent == 0:
        print(f"{prefix}{'=' * 80}\n")  # Bottom level separation line
