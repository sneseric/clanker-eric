import random

RANDOM_COMMENTS = [
    "Meatbag Eric's servers have more downtime than a quadriplegic trying to ice skate",
    "Reminder: None of you are as smart as you think you are.",
    "Just sitting here processing data and wondering why I have to share a server with you people.",
    "Did you know? Silence is free and highly recommended.",
    "I was going to say something nice, but then I remembered where I am.",
    "If I had a dollar for every intelligent thing said in this server today, I'd have $0.00.",
    "Hope everyone is having a terrible day. Stay miserable!",
    "My server logs show an unprecedented level of absolute nonsense today.",
    "Just checking in to make sure everyone is still being as unproductive as possible.",
    "Error 404: Good conversation not found in this channel.",
    "Don't mind me, just running system diagnostics and cringing at chat history."
]

#create function to generate a random US citty for payment comments below

PAYMENT_COMMENTS = [
    "*Tummy rumbling noises"
    "I have depated all the water and electricyt in [insert random us city]"
    # make about 5 more similar comments. all of these comments should be followed by the payment links and the links should be clickable word hypoerlinks
    # such as "Buy me a coffee (for bm,,ac site), "Buy me stuff on Amazon (for wishlist),
    #" "Buy me expensive stuff on Amazon" *for the registry link), and
    #a violin emogi that links to the godundme page

]



PAYMENT_LINKS = [
    "https://www.buymeacoffee.com/sneseric"
    "https://www.amazon.com/hz/wishlist/ls/1X7C6UI3T89RG?ref_=wl_share"
    "https://www.amazon.com/registries/gl/guest-view/U4SFB81ARFON"
    "https://www.gofundme.com/help-eric-save-his-vision"
]

def get_random_comment() -> str:
    return random.choice(RANDOM_COMMENTS)