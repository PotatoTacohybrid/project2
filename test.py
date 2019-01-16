chats = {
    "room": {
        "users": ["mark", "dave"],
        "messages": ["haha", "funny story dave"]
    },
    "room1": {
        "users": ["mark1", "dave1"],
        "messages": ["hahaha", "funny story daveeeeee"]
    }

}

room = input()
zipped = zip(chats[room]['users'], chats[room]['messages'])

for user, message in zipped:
    print(f"User {user} said '{message}'")
