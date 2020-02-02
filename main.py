from smtplib import SMTP
from email.message import EmailMessage
from time import sleep, time
import math

from email_list import *
from data import *

MAX_ERR = 17


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    name = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, name)
    s = round(size_bytes / p, 2)
    return f"{s}{size_name[name]}"


def convert_time(sec_time):
    if sec_time == 0:
        return "0s"
    time_name = ("s", "min", "h")
    name = int(math.floor(math.log(sec_time, 60)))
    p = math.pow(60, name)
    s = round(sec_time / p, 2)
    return f"{s}{time_name[name]}"


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
msg['From'] = "SpamForSpam"
msg['Bcc'] = ', '.join(to)
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
    "\n\tbody: " + body.replace('\n', ' ').replace('\t', ' ') +
    f"\n\tfile: {files} x {round(file_size/1024/1024)}MB ({file_name})"
)

# send message
print("\n\n\n\nstart sending")
err_count = 0
counter = 0
i = 1
t_start = time()
while err_count < MAX_ERR:
    try:
        with SMTP(server, port) as smtp:
            print(f"\n\nstart tls:\t{smtp.starttls()}")
            print(f"login:\t\t{smtp.login(me, password)}\n")

            for i in range(i, rounds+1):
                data = file_size * files * len(to)
                print(f"\nround {i}/{rounds}:")
                t1 = time()
                response = smtp.sendmail(me, to, message)
                t2 = time()
                print(
                    f"\ttime:\t{convert_time(t2 - t1)}"
                    f"\n\tmails:\t{len(to)}"
                    f"\n\tdata:\t{convert_size(data)}"
                    f"\t({convert_size(data/(t2-t1))}/s)"
                    f"\n\tresponse:\t{response}",
                    end=""
                )
                counter += len(to)
            break

    except KeyboardInterrupt:
        break
    except:
        print("\tfailed")
        if err_count < MAX_ERR:
            for _ in range(0, 2**err_count):
                sleep(1)
        err_count += 1
t_end = time()

if err_count == MAX_ERR:
    print("\nsomething went wrong!")
    exit()

data = file_size*files*counter
print(
    "\n\nfinished sending mails successfully!"
    f"\ntotal time:\t{convert_time(t_end-t_start)}"
    f"\ntotal rounds:\t{rounds}"
    f"\ntotal mails:\t{counter}"
    f"\ntotal data:\t{convert_size(data)}"
    f"\t({convert_size(data/(t_end-t_start))}/s)\n\n"
)
