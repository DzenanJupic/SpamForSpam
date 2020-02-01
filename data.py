import string
import random
from os import path


def random_str(n=10):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=n))


me = "SpamForSpam876235@gmail.com"
password = "vPO406W*Lp"


subject = f"SPAM FOR SPAM!"
files = 2
file_name = "image.png"
file_size = path.getsize(file_name)
body = \
    "Hey guys,\nhope you like the pictures!" \
    "\n\nSend 'please stop' if you stop spamming. " \
    "Then the email flood  might end.\n\n" \
    "Ups! forgot that there's no email to send to!"
