import os
import pprint
from faker import Faker
import sqlite3
# CREATING THE DATABASE
def create_names_table(): #[4 This is a function that creates the database]
	db_connection = sqlite3.connect('morbius.db')
	cursor = db_connection.cursor()
	cursor.execute('''CREATE TABLE names(
	name_id INTEGER PRIMARY KEY AUTOINCREMENT,
	first_name TEXT,
	last_name TEXT);
	''')
	db_connection.commit()
	db_connection.close()

def create_card_table():
	db_connection = sqlite3.connect('morbius.db')
	cursor = db_connection.cursor()
	cursor.execute('''CREATE TABLE card_info(
	card_id INTEGER PRIMARY KEY AUTOINCREMENT,
	number TEXT,
	cvc TEXT,
	card_expire TEXT,
	card_provider TEXT);
	''') 
	db_connection.commit()
	db_connection.close()
	

def create_connector_table():
	db_connection = sqlite3.connect('morbius.db')
	cursor = db_connection.cursor()
	cursor.execute('''CREATE TABLE name_card( 
	name_id INTEGER,
	card_id INTEGER);
	''') 
	db_connection.commit()
	db_connection.close()


	
def create_db():	#[!!!!!!!THIS USES  REFERENCED FUNCTIONS TO SAVE TIME AND CREATE ENTIRE DATABASE IN ONE GO !!!!!!!!]
	create_names_table()
	create_card_table()
	create_connector_table()

	
	# INSERTING INTO THE DATABASE
	
def insert_person(): #[A Creating this table adds several rows ]
	first = input("What is your person's first name?")
	last = input("What is your person's last name?") #[2 This user input stores the last name so it can be placed in the database]
	db_connection = sqlite3.connect('morbius.db')
	cursor = db_connection.cursor()
	cursor.execute('INSERT INTO names(first_name, last_name) VALUES(?,?);',[first,last])
	cursor.execute('SELECT * FROM names;')
	dit = {}
	for current in cursor.fetchall():
		dit['name_id'] = current[0]
		dit['first_name'] = current[1]
		dit['last_name'] = current[2]
	pprint.pprint(dit)
	db_connection.commit()
	cursor.execute('INSERT INTO card_info (number, cvc, card_expire,card_provider) VALUES (?, ?, ?, ?);',[ Faker('en_US').credit_card_number(),Faker('en_US').credit_card_security_code(),Faker('en_US').credit_card_expire(),Faker('en_US').credit_card_provider()])
	cursor.execute('SELECT * FROM card_info;')
	db_connection.commit()

	cursor.execute('SELECT max(name_id),max(card_id) FROM names INNER JOIN card_info ON names.name_id = card_info.card_id;')
	lst = []
	for current in cursor.fetchall():
		for cur in current:
			lst.append(cur) #[DATA STORAGE] #[1 FOR LOOP THAT PULLS THE INFORMATION FROM THE SQL QUERY SO THAT IT CAN BE INPUT AS A STRING]


	
	cursor.execute('INSERT INTO name_card(name_id,card_id)VALUES(?,?);',[lst[0], lst[1]])
	db_connection.commit()
	db_connection.close()
	





# SQL SELECT QUERIES

def find_all_info(): #[C, D, and E THIS FUNCTION TAKES THE DATA OUT OF ALL 3 TABLES IN THE DATABASE]
	db_connection = sqlite3.connect('morbius.db')
	cur = db_connection.cursor()
	cur.execute('SELECT * FROM names;')
	print('names')
	dit = {}
	for current in cur.fetchall():
		dit['name_id'] = current[0]
		dit['first_name'] = current[1]
		dit['last_name'] = current[2]
		pprint.pprint(dit)
	cur.execute('SELECT * FROM card_info')
	print('card information')
	dit = {}
	for current in cur.fetchall():
		
		dit['card_id'] = current[0]
		dit['card_holder_name'] = current[1]
		dit['card_number'] = current[2]
		dit['CVV'] = current[3]
		dit['expire_date'] = current[4]
		dit['card_provider'] = current[5]
		print(dit)
	print('connector table')
	cur.execute('SELECT * FROM name_card;')
	dit = {}
	for current in cur.fetchall():
		dit['name_id'] = current[0]
		dit['card_id'] = current[1]
		print(dit)

def find_specific_person(): #[F THIS FUNCTION ASKS FOR A CREDIT CARD NUMBER, AND PRINTS THE NAME OF THE PERSON THAT OWNS THE CARD]
	credit_numba = input("what is your person's credit card number?")
	db_connection = sqlite3.connect('morbius.db')
	cursor = db_connection.cursor()
	try: #[!!!! THIS IS A TRY / EXCEPT STATEMENT IT CHECKS IF THE INPUT GIVEN WORKS WITH THE PROGRAM!!!!!!]
		cursor.execute('SELECT * FROM names INNER JOIN card_info ON names.name_id = card_info.card_id WHERE number = ?;',[int(credit_numba)])
		dit = {}
		for current in cursor.fetchall():
			dit['name_id'] = current[0]
			dit['first_name'] = current[1]
			dit['last_name'] = current[2]
		pprint.pprint(dit)
	except:
		print('Please enter a valid number.') #[!!!!!!!!!THIS USES INPUT VALIDATION AS IT CHECKS IF THE INPUT NUMBER IS VALID AND WORKS WITH THE DATABASE!!!!!!!!]


def specific_row(): #[G THIS FUNCTION ASKS FOR A NAME ID, AND THEN PROVIDES THEIR FIRST AND LAST NAME BASED ON THE ID GIVEN]
	name = input('What is the id of your person?')
	db = sqlite3.connect("morbius.db")
	cursor = db.cursor()
	cursor.execute("SELECT * FROM names WHERE name_id = ?;",[name])
	dit = {}
	for current in cursor.fetchall():
		dit['name_id'] = current[0]
		dit['first_name'] = current[1]
		dit['last_name'] = current[2]
	pprint.pprint(dit)

  
def using_a_join(): #[H THIS FUNCTION INNER JOINS FIRST NAMES ON CARD INFO]
	db = sqlite3.connect("morbius.db")
	cursor = db.cursor()
	cursor.execute("SELECT first_name, number FROM names INNER JOIN card_info ON card_info.card_id = names.name_id ;")
	dit = {}
	for current in cursor.fetchall():
		dit['name'] = current[0]
		dit['card_number'] = current[1]
	pprint.pprint(dit)

def update_rows1(): #[I THIS FUNCTION UPDATES CARD INFO IF YOUR NAME ON CARD STARTS WITH SETH]
	db = sqlite3.connect("morbius.db")
	nameoncard = input('What is the name on the card you would like to change?')
	setnumber = input('What number would you like to set the card to?')
	cursor = db.cursor()
	cursor.execute('SELECT name_id FROM names WHERE first_name = ?',[nameoncard])
	nameoncard = cursor.fetchall()
	print(int(str(nameoncard)[2: -3]))
	cursor.execute("UPDATE card_info SET number = ? WHERE card_id = ?;", [setnumber, nameoncard])
	cursor.execute("SELECT number FROM card_info WHERE number = ?;",[setnumber])
	print('new card number set to '+ setnumber +' successfully!')
	db.commit()
def update_rows2(): #[J I THIS FUNCTION UPDATES CARD INFO IF YOUR NAME ON CARD STARTS WITH JOHN]
	db = sqlite3.connect("morbius.db")
	nameoncard = input('What is the name on the card you would like to change?')
	newcvv = input('What is the new cvv you would like to set for your card?')
	cursor = db.cursor()
	cursor.execute('SELECT name_id FROM names WHERE name =?',[nameoncard])
	nameoncard = cursor.fetchall()
	cursor.execute("UPDATE card_info SET cvc = ? WHERE name_on_card = ?;",[newcvv, nameoncard])
	print('new cvv set to '+ newcvv +' successfully!')
	db.commit()

def remove_specific_rows_from_a_table(): #[K THIS FUNCTION REMOVES ANY SPECIFIC ROWS WITH THE NAMES MICHAEL ATTATCHED IN NAMES]
	namessss = input('What is the name of the person you would like to remove?')
	db = sqlite3.connect("morbius.db")
	cursor = db.cursor()
	cursor.execute("DELETE FROM names WHERE first_name = ?;",[namessss])
	db.commit() 

def create_until_michael(): #[B ADDS UP TO 100 PEOPLE]
	os.remove('morbius.db')
	create_db()
	db = sqlite3.connect('morbius.db')
	cursor = db.cursor()
	numba = 0

	try:
		for cur in range(0,100):
			if numba == 0:
				insert_person()
				cursor.execute('SELECT first_name FROM names ORDER BY name_id DESC LIMIT 1;')
				current_name = cursor.fetchall()
				current_name = str(current_name)[3:-4] #[!!!!!!!!!!!!!This converts the given data to a string!!!!!!!!!!!!]
				print(current_name)
				if current_name.lower() == 'michael': #[3!!!!!!!!!!This checks if the name set is michael in order to give due punishment.!1!!!]
					print('MICHAEL DETECTED: YOU FAIL.')
					numba = 1
					os.remove('morbius.db')
	except:
		print('do better next time.')
