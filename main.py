import sqlite3 
from sqlite3 import Error
import time
import re
import string
import bcrypt
import datetime
from cryptography.fernet import Fernet
import os
import random
import secrets
import requests



# Killing the process to prevent database lock
try:
	os.system('fuser -k pass.db && fuser -k welcome.db')
except:
	pass

now = datetime.datetime.now()
date_logs = now.strftime("[" + "%d-%m-%Y|%H:%M:%S" + "]")

#view_entry_log = " [ViewEntry] "
#search_item_log = " [SearchItem] "
#new_entry_log = " [NewEntry] "
#update_entry_log = " [UpdateEntry] "
#delete_entry_log = " [DeleteEntry] "



connection = sqlite3.connect("pass.db") # CHANGE THIS
# print("\n[+] Successfully connected to database")
cursor = connection.cursor()
# print("[+] Cursor set up successfully")


connection_log = sqlite3.connect("log.db") # CHANGE THIS
	
cursor_log = connection_log.cursor()


# Create database:

def create_db():

	try:

		table = cursor.execute(""" CREATE TABLE passwords (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			service CHAR(30),
			url_website CHAR(50),
			email CHAR(30),
			password CHAR(50),
			note CHAR(50),
			date_added DATE
		);
		""")

		print("Table added successfully")

	except Error as e:
		print(f"Went wrong - {e}")

# Uncomment this to create DB
# create_db() 

# 1
def fetch_data():

	print("---------------")
	print("- All entries -")
	print("---------------\n")

	cursor.execute("SELECT service, url_website, email, password, note, date_added FROM passwords")
	table = cursor.fetchall()

	for i in table:

		print("[|] " + i[0] + "\n")
		print("URL: " + i[1])
		print("Email: " + i[2])
		print("Password: " + str(i[3]))
		print("Note: " + str(i[4]))
		print("Date added: " + i[5])
		print("\n----------------------------------\n")


	time.sleep(1.5)


	entry_date = date_logs
	category_log = " [ViewEntry] "
	message_log = "-- Searched for all entries."

	cursor_log.execute("INSERT INTO logs (date_added, category, log_message) VALUES (?, ?, ?)", (entry_date, category_log, message_log))
	connection_log.commit()

	continue_search = input("\n\nTo continue, press enter: ")

	if len(continue_search) != 0 or len(continue_search) == 0:
		main_menu()

	else:
		main_menu()


# 2
def search_for_data():

	print("----------")
	print("- Search -")
	print("----------\n")

	keyword_input = input(str("Enter keyword: "))

	time.sleep(1)
	print("\nResults: \n")
	time.sleep(0.5)

	cursor.execute("SELECT * FROM passwords WHERE service like ?", ('%'+keyword_input+'%',))
	table = cursor.fetchall()

	if len(table) == 0:
		cursor.execute("SELECT * FROM passwords WHERE email like ?", ('%'+keyword_input+'%',))
		table = cursor.fetchall()
		
		# print("\n[-] No result yielded")

	index = 0

	for i in table:

		print("[|] " + str(i[1]) + "\n")
		print("URL: " + i[2])
		print("Email: " + i[3])
		print("Password: " + str(i[4]))
		print("Note: " + str(i[5]))
		print("Date added: " + str(i[6]))
		print("\n----------------------------------\n")

		index += 1

	time.sleep(1.5)

	entry_date = date_logs
	category_log = " [SearchItem] "
	message_log = "-- Searched for " + "{ " + keyword_input + " }" + " which yielded " + str(index) + " result(s)."

	cursor_log.execute("INSERT INTO logs (date_added, category, log_message) VALUES (?, ?, ?)", (entry_date, category_log, message_log))
	connection_log.commit()

	continue_search = input("\n\nTo continue, press enter: ")

	if len(continue_search) != 0 or len(continue_search) == 0:

		main_menu()

	else:
		main_menu()


# Enter email and password
# 3
def enter_details():

	print("-------------")
	print("- Add entry -")
	print("-------------\n")

	print("Enter your details below:\n\n")

	service_input = input("Service: ")

	url_input = input("Website's URL: ")

	email_input = input("Email: ")

	# Hash password
	password_input = input("Password: ")
	password_input = password_input.encode('utf-8')
	hashedPassword = bcrypt.hashpw(password_input, bcrypt.gensalt())

	note_input = input("Note: ")

	date_input = now.strftime("%d-%m-%Y")

	confirm = input("\nIs all information correct? [Y/n]: ")

	if confirm == "Y" or confirm == "y":
		cursor.execute("INSERT INTO passwords (service, url_website, email, password, note, date_added) VALUES (?, ?, ?, ?, ?, ?)", (service_input, url_input, email_input, hashedPassword, note_input, date_input))
		connection.commit()
		print("\n")

		entry_date = date_logs
		category_log = " [NewEntry] "
		message_log = "-- Added entry " + "{ " + service_input + " }" + " with email " + "{ " + email_input + " }" + "."

		cursor_log.execute("INSERT INTO logs (date_added, category, log_message) VALUES (?, ?, ?)", (entry_date, category_log, message_log))
		connection_log.commit()

	elif confirm == "N" or confirm == "n":
		print("\nAlright. Nothing has been done.\n")
		time.sleep(1.5)
		main_menu()

	else:
		print("\nUnknown command.\n")
		time.sleep(2)
		main_menu()


# 4
# Update data
def update_data():
	pass

# 5
# Delete data
def delete_data():
	
	delete_input = input("[?] Which service/email would you like to delete? (type 'all' for a list): ")
	print("\n")

	if delete_input == "all":
		cursor.execute("SELECT service from passwords")
		table = cursor.fetchall()

		for i in table:
			print("[|] " + str(i[0]))

	else:
		print("\n[-] Unknown command.\n")
		delete_data()

	cursor.execute("SELECT service FROM passwords WHERE service like ?", ('%'+delete_input+'%',))
	table = cursor.fetchall()

	if len(table) == 0:
		cursor.execute("SELECT * FROM passwords WHERE email like ?", ('%'+delete_input+'%',))
		table = cursor.fetchall()

	

	for i in table:

		if i[0] == int:
			print("1" + str(type(i)))

			print("\n[|] " + str(i[0]) + "")

		elif type(i) != int:
			print("2" + str(type(i)))

			print("\n[|] " + str(i[0]) + "")

	delete_input2 = input("\nConfirm the service to be deleted: ")	

	delete_confirm = input("\n[?] Are you sure you want to delete " + ">>[ " + delete_input2 + " ]<<? [Y/n]: ")

	cursor.execute("DELETE FROM passwords WHERE service like ?", ('%'+delete_input2+'%',))

	if delete_confirm == "Y" or delete_confirm == "y":
		connection.commit()

		entry_date = date_logs
		category_log = " [DeleteEntry] "
		message_log = "-- Deleted entry " + "{ " + delete_input2 + " }" + "."

		cursor_log.execute("INSERT INTO logs (date_added, category, log_message) VALUES (?, ?, ?)", (entry_date, category_log, message_log))
		connection_log.commit()

		print("\n\n[...] Deleting...")
		time.sleep(1.5)
		print("\n[+] Entry deleted!\n\n")
		time.sleep(1)
		main_menu()

	elif delete_confirm == "n" or delete_confirm == "N":
		print("\nNothing done.\n")

		time.sleep(1)

		main_menu()

	else: 
		print("\n[-] Unknown command.")


# 6
# Extra material

def password_generator():

	entry_date = date_logs
	category_log = " [GeneratePass] "

	print("\n----------------------")
	print("- Password Generator -")
	print("----------------------\n")

	print("Generatea a strong password.\n")

	pass_length = input("[?] How long do you want your password to be? (max 50): ")

	if int(pass_length) > 50:
		time.sleep(1)
		print("\n[...] Sorry. Too long..")
		time.sleep(0.5)
		print("[...] Back to the genereator..")
		time.sleep(2)
		password_generator()

	punctuation_input = input("[?] Do you want punctuation included? [Y/n]: ")


	if punctuation_input == "Y" or punctuation_input == "y":

		# Create random string based on length
		res = ''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation) 
			for x in range(int(pass_length))) 

		print("\n[|] Your password: \n\n" + res)
		print("-" * len(res))

		
		message_log = "-- Generated a password of " + "{ " + pass_length + " }" + "characters with punctuation."

		cursor_log.execute("INSERT INTO logs (date_added, category, log_message) VALUES (?, ?, ?)", (entry_date, category_log, message_log))
		connection_log.commit()

	elif punctuation_input == "N" or punctuation_input == "n":

		# Create random string based on length
		res = ''.join(secrets.choice(string.ascii_letters + string.digits) 
			for x in range(int(pass_length))) 

		print("\n[|] Your password: \n\n" + res)
		print("-" * len(res))

		message_log = "-- Generated a password of " + "{ " + pass_length + " }" + " characters without punctuation."

		cursor_log.execute("INSERT INTO logs (date_added, category, log_message) VALUES (?, ?, ?)", (entry_date, category_log, message_log))
		connection_log.commit()



	time.sleep(4)

	continue_input = input("\nDo you want to continue? [Y/n]: ")

	if continue_input == "Y" or continue_input == "y":
		password_generator()

	elif continue_input == "N" or continue_input == "n":

		print("\n[...] Returning to Main Menu\n")
		time.sleep(1)
		main_menu()




# Secure notes
def secure_notes():

	connection = sqlite3.connect("secnot.db") # CHANGE THIS
	
	cursor = connection.cursor()
	
	# id, header, message, date_added

	
	print("\n----------------")
	print("- Secure notes -")
	print("----------------\n")

	print("Add a secure note below.\n\n")

	print("1. View all \n2. Add new note \n3. Return to main menu\n\n")

	choice = input(">>Choice: ")
	print("\n")

	if choice == "1":
		
		cursor.execute("SELECT header, message, date_added FROM secure_notes")
		table = cursor.fetchall()

		index = 1

		for i in table:

			print("[" + str(index) + "] " + str(i[0]) + "")
			length_line = len(str(i[0]))

			print("-" * length_line + "----")
			time.sleep(0.5)

			index += 1

		choice_2 = input("\n[?] Which note do you want to read: ")

		cursor.execute("SELECT header, message, date_added FROM secure_notes WHERE header like ?", ('%'+choice_2+'%',))
		table = cursor.fetchall()

		for i in table:
			print("\n\n[|] " + str(i[0]))
			print("|" + ("-" * len(str(i[1]))) + "|")
			print("|" + str(i[1]) + "|")
			print("|" + ("-" * len(str(i[1]))) + "|")
			print("\nAdded: " + str(i[2]))

			time.sleep(2)

			continue_input = input("\n\n[...] Press enter to continue.. \n")

			if continue_input != 0:
				secure_notes()



	elif choice == "2":

		header = input("Enter header: ")
		message = input("\nEnter message: ")
		date_input= now.strftime("%d-%m-%Y")

		cursor.execute("INSERT INTO secure_notes (header, message, date_added) VALUES (?, ?, ?)", (header, message, date_input))
		connection.commit()
		time.sleep(1)
		print("\n[...] Adding entry..")
		time.sleep(1)
		print("[+] Entry added!\n")
		time.sleep(1.5)

		secure_notes()

	elif choice == "3":

		print("\n[...] Returning to Main Menu..")
		time.sleep(1)
		main_menu()

	else:
		print("[-] Unknown command.")
		secure_notes()


def password_strength():

	print("\n---------------------")
	print("- Password Strength -")
	print("---------------------\n")


	password_input = input("Enter your password: ")


	if (len(password_input)<8):
		print("\n[-] Password too short.")
		time.sleep(2)
		password_strength()

	if not re.search("[a-z]", password_input):
		print("\n[-] Add some letters to the password.")
		time.sleep(2)
		password_strength()

	if not re.search("[A-Z]", password_input):
		print("\n[-] Add some capital letters.")
		time.sleep(2)
		password_strength()

	if not re.search("[0-9]", password_input):
		print("\n[-] Add some numbers.")
		time.sleep(2)
		password_strength()

	if not re.search("[_@$]", password_input):
		print("\n[-] Add some special characters")
		time.sleep(2)
		password_strength()

	if re.search("\s", password_input):
		print("\n[-] ??")
		time.sleep(2)
		password_strength()

	else:
		print("\n[+] Strong password.")
		time.sleep(2)
		password_strength()


def extra_material():

	print("---------")
	print("- Extra -")
	print("---------\n")

	print("1. Password Generator \n2. Secure Notes \n3. Password Strength Checker \n4. Back to Main Menu\n")

	choice = input(">>Choice: ")

	if choice == "1":
		password_generator()

	elif choice == "2":
		secure_notes()

	elif choice == "3":
		password_strength()

	elif choice == "4":
		main_menu()


def log_proram():

	connection = sqlite3.connect("log.db") # CHANGE THIS
	
	cursor = connection.cursor()

	'''
	CREATE TABLE logs (
	id INTEGER PRIMARY KEY AUTOINCREMENT, date_added DATE NOT NULL, 
	category CHAR(30) NOT NULL, log_message CHAR(200) NOT NULL
	);
	'''

	print("\n----------")
	print("- Logger -")
	print("----------\n")

	print("Welcome to the logger. \nChoose an option below:")

	print("\n1. View all logs \n2. Search \n3. Delete logs \n4. Return to Main Menu")

	choice = input("\n>>Choice: ")

	date = now.strftime("[" + "%d-%m-%Y|%H:%M:%S" + "]")

	if choice == "1":

		cursor.execute("SELECT date_added, category, log_message FROM logs")
		table = cursor.fetchall()

		for i in table:

			print("\n" + str(i[0]) + " " +  str(i[1]) + " " + str(i[2]))

		time.sleep(1)

		continue_search = input("\n\nTo continue, press enter: ")

		if len(continue_search) != 0 or len(continue_search) == 0:
			log_proram()

		else:
			log_proram()

	if choice == "2":

		print("\n1. Search by category \n2. Search by date or time\n")
		choice2 = input(">>Choice: ")

		if choice2 == "1":

			print("\n")
			category_input = input("Choose a category: ")

			cursor.execute("SELECT date_added, category, log_message FROM logs WHERE category LIKE ?", ('%'+category_input+'%',))
			table = cursor.fetchall()

			for i in table:

				print("\n" + str(i[0]) + " " +  str(i[1]) + " " + str(i[2]))
				
			time.sleep(1)

			continue_search = input("\n\nTo continue, press enter: ")

			if len(continue_search) != 0 or len(continue_search) == 0:
				log_proram()

			else:
				log_proram()

		elif choice2 == "2":

			print("\n")
			category_input = input("Choose a date or time (dd-mm-yy or h:m): ")

			cursor.execute("SELECT date_added, category, log_message FROM logs WHERE date_added LIKE ?", ('%'+category_input+'%',))
			table = cursor.fetchall()

			for i in table:

				print("\n" + str(i[0]) + " " +  str(i[1]) + " " + str(i[2]))
				
			time.sleep(1)

			continue_search = input("\n\nTo continue, press enter: ")

			if len(continue_search) != 0 or len(continue_search) == 0:
				log_proram()

			else:
				log_proram()







# Main Menu
def main_menu():

	print("\nEnter your choice below:\n\n")
	print("1. View all entries \n2. Search for item \n3. New entry \n4. Update entry \n5. Delete entry \n6. Extra \n7. Exit \n\nL. Log\n\n")
	choice = input(">>Choice: ")
	print("\n")

	if choice == "1":
		fetch_data()

	elif choice == "2":
		search_for_data()

	elif choice == "3":
		enter_details()
		print("[+] Thank you! - Entry added\n")

		time.sleep(2)

		main_menu()

	elif choice == "4":
		update_data()


	elif choice == "5":
		delete_data()


	elif choice == "6":

		extra_material()
		

	elif choice == "7":

		print("\n[...] Exiting. Thanks for using Pettersen's Password Manager!")
		time.sleep(2)
		exit()

	elif choice == "L":
		log_proram()

	else:
		time.sleep(1)

		print("[-] Command not recognized")

		time.sleep(2)
		main_menu()


# Welcome
def welcome():

	#key = open("secret.key", "rb").read()

	connection_welcome = sqlite3.connect("welcome.db") # CHANGE THIS
	
	cursor_welcome = connection_welcome.cursor()

	print("\n\n               |---------------|")
	print("        |-----------------------------|")
	print("|----------------------------------------------|")
	print("  ------ Pettersen's Password Manager ------")
	print("|----------------------------------------------|")
	print("        |-----------------------------|")
	print("               |---------------|\n\n")

	password = input("\t\tEnter password: ")

	#encodedMessage = password.encode()
	#f = Fernet(key)
	#encrypted_message = f.encrypt(encodedMessage)

	#print(encrypted_message)

	#cursor_welcome.execute("INSERT INTO access (password) VALUES (?)", (encMessage,))
	#connection.commit()

	cursor_welcome.execute("SELECT password from access")
	table = cursor_welcome.fetchall()

	for i in table:
		correct_pass = str(i[0])

	if password == correct_pass:
		main_menu()

	else:
		print("\n[-] Wrong password.\n")
		time.sleep(2)
		welcome()



	


# Run program
welcome()


cursor.close()
connection.commit()
connection.close()