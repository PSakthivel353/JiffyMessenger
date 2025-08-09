
import smtplib
import mysql.connector as sql
from datetime import datetime
import random




#Authentication - Captcha ---->
def generate_random_number():
    number = random.randint(10000, 99999)
    return number


def generate_random_character():
    characters = ['!*&', '@!@.', '#s$h', '%s%^', '&``*']
    chosen_character = random.choice(characters)
    return chosen_character


def generate_captcha(number):
    number_str = str(number)
    result = ""
    for i in number_str:
        result += i + generate_random_character()
    return result

def captcha_manager():
    random_number = generate_random_number()
    
    captcha = generate_captcha(random_number)
    print('Captcha: ', captcha)
    captcha_input = str(input("Enter the correct numbers from the captcha: "))
    if captcha_input == str(random_number):
        return True
    else:
        return False
# <----


#Authentication - app password ---->
def app_login():
    global app_password
    pd = str(input('Enter the app password: '))
    return pd
# <----


#greeting the user ---->
def greet_user():
    print('''Welcome to Jiffy Messenger.
Talk nineteen to the dozen.''')
# <----


# mail sending functions ---->
def get_user_input():
    sender_email = input("Enter your email address: ")
    receiver_email = input("Enter the recipient's email address: ")
    message = input("Enter your message: ")
    return sender_email, receiver_email, message


def mailsender(sender_email, receiver_email, message):
    password = input("Enter the password: ") #bylw gifb suxx rnol

    server = smtplib.SMTP('smtp.gmail.com', 587) #variable_object to send mail
    server.starttls() #start the server. TLS - Transport layer security
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)
    
    print('Mail Sent')
# <-----

# Storing records ---->
def data_storage(sender_email, receiver_email, message):
    mycon = sql.connect(host = "localhost", user = "root", passwd = "Root", database = "jiffymessenger")
    cursor = mycon.cursor()
    
    current_datetime = datetime.now()
    current_date = current_datetime.date()
    current_time = current_datetime.strftime('%H:%M:%S')
    

    query = "INSERT INTO data(sender_email, receiver_email, date, time) VALUES (%s, %s, %s, %s)" # %s are parameters
    values = (sender_email, receiver_email, current_date, current_time) #sno auto increment
    cursor.execute(query, values)

    mycon.commit()
    mycon.close()


def display_database():
    mycon = sql.connect(host = "localhost", user = "root", passwd = "Root", database = "jiffymessenger")
    cursor = mycon.cursor(dictionary = True)
    query = "SELECT * FROM data"
    cursor.execute(query)
    data = cursor.fetchall()
    print('History:- ')
    for rec in data:
        print(rec)
    mycon.close()

# <-----


app_password = "12345"
pd = app_login()
captcha = captcha_manager() # returns true or false

# main ---->
if pd == app_password and captcha == True:
    greet_user()
    sender_email, receiver_email, message = get_user_input()
    #mailsender(sender_email, receiver_email, message)
    data_storage(sender_email, receiver_email, message)

    view_data = input("Do you want to view the history? (yes/no): ").lower()
    if view_data == "yes":
        display_database()
    
else:
    print('Incorrect password or captcha. Try again.')
    pd1 = str(input('Enter the correct app password: '))
    recaptcha = captcha_manager()
    
    if pd1 == app_password and recaptcha == True:
        greet_user()
        sender_email, receiver_email, message = get_user_input()
        #mailsender(sender_email, receiver_email, message)
        data_storage(sender_email, receiver_email, message)

        view_data = input("Do you want to view the History? (yes/no): ").lower()
        if view_data == "yes":
            display_database()
        
    else:
        print('Incorrect password or captcha. Try after some time.')
# <----


def clear_all_records():
    mycon = sql.connect(host = "localhost", user = "root", passwd = "Root", database = "jiffymessenger")
    cursor = mycon.cursor()
    query = "delete from data"
    cursor.execute(query)
    mycon.commit()
    mycon.close()


def clear_particular_record(rec):
    mycon = sql.connect(host = "localhost", user = "root", passwd = "Root", database = "jiffymessenger")
    cursor = mycon.cursor()
    query = "DELETE FROM data WHERE sno = %s"
    cursor.execute(query, (sno,)) #tuple containing actual values that will replace the parameter.
    #comma after tuple --> single element tuple.
    #sno is treated as a tuple and passed as a parameter to the execute method.
    mycon.commit()
    mycon.close()

    
choice = str(input('Do you want to clear history? (yes/no)'))
if choice.lower() == 'yes':
    print("""The options:
1. Clear all records
2. Clear particular record. """)
    ch = int(input('Enter 1/2:'))
    if ch == 1:
        clear_all_records()
        print('Records cleared.')
    elif ch == 2:
        rec = int(input('Enter record number: '))
        clear_particular_record(rec)
        print('Record cleared.')
    else:
        print('Invalid input')
    print('Thank you for using our application.')

elif choice.lower() == 'no':
    print('Thank you for using our application.')

else:
    print('Invalid input')





