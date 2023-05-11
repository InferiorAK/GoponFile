#! /usr/bin/python3

# Author        :    InferiorAK
# GoponFile     :    File Encryption Tool
# Version       :    1.0
# Lisence       :    GPL 3.0
# Github        :    github.com/InferiorAK
# facebook      :    fb.com/InferiorAK
# Youtbe	:    youtube.com/@InferiorAk
# twitter	:    twitter.com/@InferiorAk
## 1st Release: 11th May 2023

# -------- Copyright (C) 2023 InferiorAK ------

from cryptography.fernet import *
from cryptography.fernet import Fernet as F
from argparse import ArgumentParser
from multiprocessing import (
	Process,
	cpu_count
)
import platform
from time import perf_counter as pc
import base64
import os
from getpass import getpass
from colorama import (
	init,
	Fore,
	Back,
	Style
)

init(autoreset=True)
bt = Style.BRIGHT
# foreground color
w = Fore.WHITE
r = Fore.RED
g = Fore.GREEN
y = Fore.YELLOW
p = Fore.MAGENTA
lr = Fore.LIGHTRED_EX
# background color
bgr = Back.RED
bgg = Back.GREEN
bgy = Back.YELLOW
bgp = Back.MAGENTA
bglr = Back.LIGHTRED_EX


# Arguments
parser = ArgumentParser(usage="%(prog)s [options]",
						description="Private File Encryption tool by InferiorAK"
)
parser.add_argument(
	"-f", "--file",
	type=str,
	nargs="+",
	help="Target Files"
)
parser.add_argument(
	"-c", "--enc",
	action="store_true",
	help="Specifiy Encryption"
)
parser.add_argument(
	"-d", "--dec",
	action="store_true",
	help="Specifiy Decryption"
)

args = parser.parse_args()


if cpu_count() < 2 or platform.architecture()[0] != "64bit":
	print(f"{bgy + bt + r} !This tool may impact on your Device Hardcore ")
else:
	pass


restricted = [os.path.basename(__file__)]

# functions
def encrypt(file, fernet):
	f = open(file, "rb")
	mal = f.read()
	try:
		encrypted = fernet.encrypt(mal)
		with open(file, "wb") as out:
			out.write(encrypted)
			out.close()
		print(f"{bt + g} {file} Locked Successfully! ")
	except KeyboardInterrupt:
		print(f"{bgy + bt + r} Process Stopped!")
		os._exit(1)
	except Exception as err:
		print(f"{bt + r} {err} ")



def decrypt(file, fernet):
	f = open(file, "rb")
	mal = f.read()
	try:
		decrypted = fernet.decrypt(mal)
		with open(file, "wb") as out:
			out.write(decrypted)
			out.close()
		print(f"{bt + g} {file} Unolcked Successfully! ")
	except KeyboardInterrupt:
		print(f"{bgy + bt + r} Process Stopped!")
		os._exit(1)
	except InvalidToken:
		print(f"{bgr + bt + w} Wrong Passphrase! ")
	except Exception as err:
		print(f"{bt + r} {err} ")

# runner code
if __name__ == "__main__":
	if args.file is not None:
		if args.enc:
			while True:
				key = getpass("Enter your Passphrase: ").encode("utf-8")
				key_re = getpass("Re-Enter your Passphrase: ").encode("utf-8")
				if key_re == key:
					if 32 >= len(key) and not len(key) > 32:
						f_key = key + b'\x00' * (32 - len(key))
						key_b64 = base64.urlsafe_b64encode(f_key)
						fernet = F(key_b64)
					else:
						print(f"{bgy + bt + r} !Your Password Length can't be greater than 32 Characters ")
						continue
				else:
					print(f"{bt + r} !Passphrase did't Matched with Before one ")
					continue
				break

			s = pc()
			files = []
			for file in args.file:
				if os.path.isfile(file):
					if file not in restricted:
						checked = open(file, "rb").read()
						if not checked.startswith(b'gAAAAAB'):
							files.append(file)
						else:
							print(f"{bt + y} {file} is already Locked! ")
					else:
						print(f"{bt + y} !VIP Files can't be Locked ")
				else:
					print(f"{bgr + bt + w} {file} not found!")

			tasks = []
			for file in files:
				ps = Process(target=encrypt, args=[file, fernet])
				ps.start()
				tasks.append(ps)
			for ps in tasks:
				ps.join()
				# encrypt(file)

			e = pc()
			print(f" Time Taken: {e-s} sec ")

		elif args.dec:
			while True:
				key = getpass("Enter your Passphrase: ").encode("utf-8")
				if 32 >= len(key) and not len(key) > 32:
					f_key = key + b'\x00' * (32 - len(key))
					key_b64 = base64.urlsafe_b64encode(f_key)
					fernet = F(key_b64)
				else:
					print(f"{bgy + bt + r} !Your Password Length wasn't greater than 32 Characters ")
					continue
				break

			s = pc()
			files = []
			for file in args.file:
				if os.path.isfile(file):
					checked = open(file, "rb").read()
					if checked.startswith(b'gAAAAAB'):
						files.append(file)
					else:
						print(f"{bt + y} {file} isn't Locked yet! ")
				else:
					print(f"{bgr + bt + w} {file} not found!")

			tasks = []
			for file in files:
				ps = Process(target=decrypt, args=[file, fernet])
				ps.start()
				tasks.append(ps)
			for ps in tasks:
				ps.join()
				# decrypt(file)

			e = pc()
			print(f" Time Taken: {e-s} sec ")

		else:
			print("Select a Method. Encrypt or Decrypt?")
	else:
		print("No file was Given!")
