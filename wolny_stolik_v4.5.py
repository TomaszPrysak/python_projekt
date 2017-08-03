# -*- coding: utf-8 -*-

import pymysql

class MenuStart:
    
    # Użytkownik obsługujący aplikację dokonuje wyboru rodzju konta z którego będzie korzystać
    # Wybór konta powoduje zalogowanie się przez odpowiedni profil do bazy danych
    # Są trzy profile:
    # A - administrator, pełne uprawnienia do bazy danych
    # U - użytkownik, uprawnienia do dodawania rekordów i ich kasowania w tabelach booking oraz users
    # K - kelner, uprawnienia dostępu do dodawania rekordów i ich kasowania w tabelach restaurants, occupancy, type_tables, waiters, booking
    
    def __init__(self):
        print()
        print(linia)
        print("MENU START")
        print("Wybierz rodzaj konta: ")
        type_user = input("(U)żytkownik\n(K)elner\n(A)dministrator\n(W)wyjście z programu\nTwój wybór: ")
        while (type_user != "W" and type_user != "w" and type_user != "U" and type_user != "u" and type_user != "K" and type_user != "k" and type_user != "A" and type_user != "a"):
            print()
            print(linia)
            print("Wprowadzono niepoprawny klawisz")
            print("Wybierz rodzaj konta: ")
            type_user = input("(U)żytkownik\n(K)elner\n(A)dministrator\n(W)wyjście z programu\nTwój wybór: ")
        if (type_user == "U" or type_user == "u"):
            database_user_open_file = open("database_user.txt", "r")
            database_user_text = database_user_open_file.read()
            database_user_open_file.close()
            start = User(database_user_text)        
        elif (type_user == "K" or type_user == "k"):
            database_waiter_open_file = open("database_waiter.txt", "r")
            database_waiter_text = database_waiter_open_file.read()
            database_waiter_open_file.close()
            start = Waiter(database_waiter_text)        
        elif (type_user == "A" or type_user == "a"):
            database_admin = input("Wprowadź hasło administratora: ")
            start = Admin(database_admin)        
        else:
            print()
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
        self.user_start()
        
    def user_start(self):
        print()
        print(linia)        
        print("MENU LOGOWANIA UŻYTKOWNIKA")
        action = input("(L)ogowanie istniejącego użytkownika\n(R)ejestracja nowego użytkownika\n(P)owrót do MENU START\nTwój wybór: ")
        while (action != "P" and action != "p" and action != "R" and action != "r" and action != "L" and action != "l"):
            print()
            print("Wprowadzono niepoprawny klawisz")            
            action = input("(L)ogowanie istniejącego użytkownika\n(R)ejestracja nowego użytkownika\n(P)owrót do MENU START\nTwój wybór: ")
        if (action == "L" or action == "l"):
            self.user_log()
        elif (action == "R" or action == "r"):
            self.newuser_reg()
        elif (action == "P" or action == "p"):
            start = MenuStart()
        
    def user_log(self):
        print()
        print(linia)
        e_mail_user = input("Podaj e-mail: ")
        pass_user = input("Podaj hasło: ")
        self.c.execute("select e_mail, pass from users where e_mail = '" + e_mail_user + "';")
        result_user_log = self.c.fetchall()
        while (len(result_user_log) == 0):
            print()
            print("Podany e-mail i/lub hasło są nieprawidłowe")
            action = input("(W)prowadź e-mail i hasło ponownie\n(P)owrót do Strefy użytkownika\nTwój wybór: ")
            while (action != "W" and action != "w" and action != "P" and action != "p"):
                print()
                print("Wprowadzono niepoprawny klawisz")  
                action = input("(W)prowadź e-mail i hasło ponownie\n(P)owrót do Strefy użytkownika\nTwój wybór: ")
            if (action == "W" or action == "w"):
                self.user_log()
            elif (action == "P" or action =="p"):
                self.user_start()
        if (e_mail_user == result_user_log[0][0]):
            if (pass_user == result_user_log[0][1]):
                self.user_panel()
            else:
                print()
                print("Podany e-mail i/lub hasło są nieprawidłowe")
                action = input("(W)prowadź e-mail i hasło ponownie\n(P)owrót do Strefy użytkownika\nTwój wybór: ")
                while (action != "W" and action != "w" and action != "P" and action != "p"):
                    print()
                    print("Wprowadzono niepoprawny klawisz")  
                    action = input("(W)prowadź e-mail i hasło ponownie\n(P)owrót do Strefy użytkownika\nTwój wybór: ")
                if (action == "W" or action == "w"):
                    self.user_log()
                elif (action == "P" or action =="p"):
                    self.user_start()
    def newuser_reg(self):
        print()
        print(linia)
        print("Rejestracja nowego użytkownika")
        
    def user_panel(self):
        print()
        print(linia)
        print("Witaj w panelu użytkownika")
    
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
    print()
    print(linia)
    print("Wprowadzono niepoprawny kawisz")
    next = input("Naciśnij ENTER aby kontynuować: ")

start = MenuStart()