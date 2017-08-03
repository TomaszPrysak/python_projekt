# -*- coding: utf-8 -*-

import pymysql

class Start:
    
    # Użytkownik obsługujący aplikację dokonuje wyboru rodzju konta z którego będzie korzystać
    # Wybór konta powoduje zalogowanie się przez odpowiedni profil do bazy danych
    # Są trzy profile:
    # A - administrator, pełne uprawnienia do bazy danych
    # U - użytkownik, uprawnienia do dodawania rekordów i ich kasowania w tabelach booking oraz users
    # K - kelner, uprawnienia dostępu do dodawania rekordów i ich kasowania w tabelach restaurants, occupancy, type_tables, waiters, booking
    
    def __init__(self):
        print()
        print(linia)
        print("MENU STARTOWE")
        print("Wybierz rodzaj konta: ")
        type_user = input("(U)żytkownik - (K)elner - (A)dministrator || (W)wyjście: ")
        while (type_user != "W" and type_user != "w" and type_user != "U" and type_user != "u" and type_user != "K" and type_user != "k" and type_user != "A" and type_user != "a"):
            print("Wprowadzono niepoprawny klawisz")
            type_user = input("(U)żytkownik - (K)elner - (A)dministrator || (W)wyjście: ")
        if (type_user == "U" or type_user == "u"):
            database_user_open_file = open("database_user.txt", "r")
            database_user_text = database_user_open_file.read()
            database_user_open_file.close()
            start1 = User(database_user_text)        
        elif (type_user == "K" or type_user == "k"):
            database_waiter_open_file = open("database_waiter.txt", "r")
            database_waiter_text = database_waiter_open_file.read()
            database_waiter_open_file.close()
            start1 = Waiter(database_waiter_text)        
        elif (type_user == "A" or type_user == "a"):
            database_admin = input("Wprowadź hasło administratora: ")
            start1 = Admin(database_admin)        
        else:
            print(linia)
            print("Zamknięcie aplikacji. Do zobaczenia")        


class Admin:
    
    # Po wybraniu konta Administrator uruchamiana jest klasa Admin
    
    def __init__(self, password):
        self.password = password
        self.conn = pymysql.connect("localhost", "root", self.password, "wolny_stolik")
        self.c = self.conn.cursor()
        print()
        print(linia)        
        print("Zalogowano jako administrator")

class User:
    
    # Po wybraniu konta Użytkownik uruchamiana jest klasa user
    
    def __init__(self, password):
        self.password = password
        self.conn = pymysql.connect("localhost", "users", self.password, "wolny_stolik")
        self.c = self.conn.cursor()  
        print()
        print(linia)        
        print("Strefa użytkownika")
        action = ""
        while (action != "P" and action != "p"):
            action = input("(L)ogowanie istniejącego użytkownika - (R)ejestracja nowego użytkownika || (P)owrót do MENU START: ")
            if (action == "L" or action == "l"):
                self.log_user()
            elif (action == "R" or action == "r"):
                self.register_new_user()
        start2 = Start()
    def log_user(self):
        print()
        print(linia)
        e_mail_user = input("Podaj e-mail: ")
        self.c.execute("select e_mail from users where e_mail = '" + e_mail_user + "';") # zwraca zapytanie w postaci tablicy w tablicy, w tym wypadku w tablicy w indeksie 0 wartość na indeksie 0
        result_e_mail_user = self.c.fetchall()
        while (len(result_e_mail_user) == 0):
            print("Podany adres e-mail jest niepoprawny")
            e_mail_user = input("Podaj e-mail: ")
            self.c.execute("select e_mail, pass from users where e_mail = '" + e_mail_user + "';")
            result_e_mail_user = self.c.fetchall()
        if (e_mail_user == result_e_mail_user[0][0]):
            pass_user = input("Podaj hasło: ")
            self.c.execute("select pass from users where e_mail = '" + e_mail_user + "';")
            result_pass_user = self.c.fetchall()
            print(pass_user)
            print(result_pass_user[0][0])
            if (pass_user == result_pass_user[0][0]):
                print("Zalogowano poprawnie")
            
        
        
        
        #print(self.c.fetchall())
        #print(wynik[0][0]) wyświetla element z tablicy na indeksie 0 i wartości 0
    
class Waiter:
    
    # Po wybraniu konta Kelner uruchamiana jest klasa Waiter    
    
    def __init__(self, password):
        self.password = password
        self.conn = pymysql.connect("localhost", "waiters", self.password, "wolny_stolik")
        self.c = self.conn.cursor()   
        print()
        print(linia)        
        print("Strefa kelnera")

# Logo aplikacji

linia = "======================================="

print(linia)
print('Witaj w aplikacji "Wolny Stolik"')
print(linia)
print("|    W W W   OOO   L      N   N  Y   Y")
print("|    W W W  O   O  L      N   N  Y   Y")
print("|    W W W  O   O  L      NN  N   Y Y ")
print("|    W W W  O   O  L      N N N    Y  ")
print("|    W W W  O   O  L      N  NN    Y  ")
print("|    W W W  O   O  L      N   N    Y  ")
print("|     W W    OOO   LLLLL  N   N    Y  ")
print("|")
print("|")
print("|   SSS   TTTTT   OOO   L      I  K   K")
print("|  S   S    T    O   O  L      I  K  K ")
print("|  S        T    O   O  L      I  K K  ")
print("|   SSS     T    O   O  L      I  KK   ")
print("|      S    T    O   O  L      I  K K  ")
print("|  S   S    T    O   O  L      I  K  K ")
print("|   SSS     T     OOO   LLLLL  I  K   K")
print(linia)
next = input("Naciśnij ENTER aby kontynuować: ")
print(linia)

while (next != ""):
    print("Wprowadzono niepoprawny kawisz")
    next = input("Naciśnij ENTER aby kontynuować: ")

start1 = Start()



