from smtplib import SMTP
from email.message import EmailMessage
from num2words import num2words

from email_list import *
from data import *


def get_int(min_value=0, max_value=1, input_msg=None):
    while True:
        try:
            ans = int(input(input_msg))
            if ans < min_value or ans > max_value:
                print(f"input needs to be between {min_value} and {max_value}")
                continue
            break
        except KeyboardInterrupt:
            exit()
        except:
            print("please input a number")

    return ans


addresses = get_int(0, len(to), "How many addresses do you want to send mails to?:\n")
if addresses == 0:
    exit()
to = to[:addresses]
rounds = get_int(0, 1000, "How many times do you want to send the mail?:\n")
if rounds == 0:
    exit()

# basic message
print("\n\ncreate mail", end="\t")
msg = EmailMessage()
msg['Subject'] = subject
msg.set_content(body)
print("finished")

# picture attachment
print("attach pictures", end="\t")
with open(file_name, "rb") as image:
    picture = image.read()
for i in range(0, files):
    msg.add_attachment(picture, maintype='image', subtype='png', filename=random_str())
print(f"finished ({files} x {round(file_size/1024/1024, 2)}MB)")

# convert message to string
message = msg.as_string()

print(
    "\n\nSummary:"
    f"\n\tsubject: {subject}"
    f"\n\tbody: {body}"
    f"\n\tfile: {files} x {round(file_size/1024/1024)}MB ({file_name})"
)

# send message
print("\n\n\n\nstart sending\n\n")
with SMTP("smtp.gmail.com", 587) as server:
    server.starttls()
    server.login(me, password)

    for i in range(1, rounds+1):
        print(f"start round {i}/{rounds}")

        for receiver in to:
            print(f"\tsend email to: {receiver}")
            server.sendmail(me, receiver, message)

print(
    "\n\nfinished sending mails "
    f"{num2words(rounds)} {'times' if rounds>1 else 'time'} "
    f"to {num2words(len(to))} {'receivers' if len(to)>1 else 'receiver'} "
    "successfully!"
    f"\ntotal send data: {round((file_size*rounds*len(to))/1024/1024, 2)}MB"
)
