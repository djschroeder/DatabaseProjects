def display_tweet_details(tweet, indent=0, parent_is_list=False):
    indent_str = ' ' * indent

    if isinstance(tweet, dict):
        for key, value in tweet.items():
            # Check if value is a dictionary or a list for recursive call
            if isinstance(value, dict) or isinstance(value, list):
                print(f"{indent_str}{key}:")
                display_tweet_details(value, indent + 4)
            else:
                print(f"{indent_str}{key}: {value}")

    elif isinstance(tweet, list):
        for index, item in enumerate(tweet):
            # Handling the list items
            if isinstance(item, (dict, list)):
                print(f"{indent_str}[{index}]")
                display_tweet_details(item, indent + 4, parent_is_list=True)
            else:
                print(f"{indent_str}- {item}")

    else:
        # For non-dict and non-list values
        if parent_is_list:
            print(f"{indent_str}- {tweet}")
        else:
            print(f"{indent_str}{tweet}")