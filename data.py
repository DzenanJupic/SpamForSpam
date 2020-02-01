import string
import random

me = "SpamForSpam876235@gmail.com"
password = "vPO406W*Lp"


def random_str(n=10):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=n))


subject = f"SPAM FOR SPAM!\t{random_str()}"
file_name = "image.png"
body = \
    "Hey guys,\nhope you like the pictures!" \
    "\n\nSend 'please stop' if you stop spamming. " \
    "Then the email flood  might end.\n\n" \
    "Ups! forgot that there's no email to send to!"
