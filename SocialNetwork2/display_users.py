def display_users(users):
    for i, user in enumerate(users, start=1):
        print(f"{i}. Username: @{user.get('username', 'N/A')}")
        print(f"   Display Name: {user.get('displayname', 'N/A')}")
        print(f"   Location: {user.get('location', 'N/A')}\n")
        print("-" * 100)
