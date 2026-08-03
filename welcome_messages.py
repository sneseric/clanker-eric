import random

JOIN_MESSAGES = [
    # --- Roasts & Sarcasm ---
    "Oh look {username}’s here. Average server IQ just dropped 10 points.",
    "Welcome {username}! We were having a nice quiet day until you showed up.",
    "Great, {username} joined. Time to mute the server.",
    "Look everybody! {username} is here to contribute absolutely nothing.",
    "{username} has arrived. Lower your expectations accordingly.",
    "Oh brilliant, {username} joined. Did the server security filters fail?",
    "Welcome {username}. Try not to spill anything on the carpet.",
    "Warning: {username} has entered the room. Conceal all valuable brain cells.",
    "{username} joined! Is this a server update or a massive downgrade?",

    # --- General Greetings ---
    "A wild {username} appeared! Quick, throw a Pokéball.",
    "Welcome to the server, {username}! Grab a drink and settle in.",
    "Everyone act normal, {username} just walked in.",
    "Welcome {username}! Make sure to check out the channels and say hi.",
    "Look who decided to grace us with their presence: {username}!",
    "{username} has spawned into the server.",
    "System Alert: {username} has successfully joined the building.",
    "Welcome aboard {username}! Glad to have you here."
]


def get_random_welcome_message(username: str) -> str:
    template = random.choice(JOIN_MESSAGES)
    return template.format(username=username)