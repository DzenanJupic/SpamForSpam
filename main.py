from smtplib import SMTP
from email.message import EmailMessage
from email_list import *
from data import *

rounds = int(input("How many times do you want to send the emails?:\n"))

# basic message
print("\n\ncreate Email", end="\t")
msg = EmailMessage()
msg['Subject'] = subject
msg.set_content(body)
print("finished")

# picture attachment
print("attach pictures", end="\t")
with open(file_name, "rb") as image:
    picture = image.read()
msg.add_attachment(picture, maintype='image', subtype='png', filename=random_str())
msg.add_attachment(picture, maintype='image', subtype='png', filename=random_str())
print("finished")

# convert message to string
message = msg.as_string()

# send message
print("\nstart sending\n\n")
with SMTP("smtp.gmail.com", 587) as server:
    server.starttls()
    server.login(me, password)

    for i in range(1, rounds+1):
        print(f"start round {i}/{rounds}")

        for receiver in to:
            print(f"\tsend email to: {receiver}")
            server.sendmail(me, receiver, message)

print(f"\n\nfinished sending mail {rounds} times to {len(to)} receivers successfully!")
