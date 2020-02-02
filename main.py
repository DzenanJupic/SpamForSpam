from smtplib import SMTP
from email.message import EmailMessage

from email_list import *
from data import *

MAX_ERR = 10


def get_int(min_value=0, max_value=1, input_msg=None, default=None):
    while True:
        try:
            ans = input(input_msg)
            if ans == "":
                return default
            else:
                ans = int(ans)

            if min_value < ans < max_value:
                return ans
            else:
                print(f"input needs to be between {min_value} and {max_value}")
        except KeyboardInterrupt:
            exit()
        except:
            print("please input a number")


addresses = get_int(
    0,
    len(to),
    f"How many addresses do you want to send mails to?:\n[min: 0, max: {len(to)}, default: {len(to)}]\n",
    len(to)
)
if addresses == 0:
    exit()
to = to[:addresses]

rounds = get_int(
    0,
    1000,
    "How many times do you want to send the mail?:\n[min: 0, max: 1000, default: 1]\n",
    1
)
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
    "\n\tbody: " + body.rstrip('\n').rstrip('\t') +
    f"\n\tfile: {files} x {round(file_size/1024/1024)}MB ({file_name})"
)

# send message
print("\n\n\n\nstart sending\n\n")
err_count = 0
i = 1
r = 1
while err_count < MAX_ERR:
    try:
        with SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(me, password)

            for i in range(i, rounds+1):
                print(f"start round {i}/{rounds}")
                for r, receiver in zip(range(r, len(to)+1), to):
                    print(f"\tsend email to: {receiver}")
                    server.sendmail(me, receiver, message)
            break

    except KeyboardInterrupt:
        break
    except:
        err_count += 1

if err_count == MAX_ERR:
    print("something went wrong!")
    exit()

print(
    "\n\nfinished sending mails successfully!"
    f"\ntotal send mails:\t{(len(to)*(i-1)) + r}"
    f"\ntotal send data:\t{round( (file_size* ((len(to)*(i-1)) + r) ) /1024/1024 , 2)}MB"
)
