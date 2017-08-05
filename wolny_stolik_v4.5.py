# -*- coding: utf-8 -*-

import pymysql

class MenuStart:
    
    # Użytkownik obsługujący aplikację dokonuje wyboru rodzju konta z którego będzie korzystać
    # Wybór konta powoduje zalogowanie się przez odpowiedni profil do bazy danych
    # Są trzy profile:
    # A - administrator, pełne uprawnienia do bazy danych
    # U - użytkownik, uprawnienia do dodawania, kasowania oraz uaktualniania rekordów w tabelach booking oraz users
    # K - kelner, uprawnienia dostępu do dodawania, kasowania oraz uaktualniania rekordów w tabelach restaurants, occupancy, type_tables, waiters, booking
    
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
            close = Close()        


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
        self.user_menu()
        
    def user_menu(self):
        print()
        print(linia)        
        print("MENU LOGOWANIA")
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
        user_e_mail = input("Podaj e-mail: ")
        user_pass = input("Podaj hasło: ")
        self.c.execute("select e_mail, pass from users where e_mail = '" + user_e_mail + "';")
        result_user_log = self.c.fetchall()
        while (len(result_user_log) == 0):
            print()
            print("Podany e-mail i/lub hasło są nieprawidłowe")
            action = input("(W)prowadź e-mail i hasło ponownie\n(P)owrót do MENU LOGOWANIA\nTwój wybór: ")
            while (action != "W" and action != "w" and action != "P" and action != "p"):
                print()
                print("Wprowadzono niepoprawny klawisz")  
                action = input("(W)prowadź e-mail i hasło ponownie\n(P)owrót do MENU LOGOWANIA\nTwój wybór: ")
            if (action == "W" or action == "w"):
                self.user_log()
            elif (action == "P" or action =="p"):
                self.user_menu()
        if (user_e_mail == result_user_log[0][0]):
            if (user_pass == result_user_log[0][1]):
                self.user_panel(user_e_mail)
            else:
                print()
                print("Podany e-mail i/lub hasło są nieprawidłowe")
                action = input("(W)prowadź e-mail i hasło ponownie\n(P)owrót do MENU LOGOWANIA\nTwój wybór: ")
                while (action != "W" and action != "w" and action != "P" and action != "p"):
                    print()
                    print("Wprowadzono niepoprawny klawisz")  
                    action = input("(W)prowadź e-mail i hasło ponownie\n(P)owrót do MENU LOGOWANIA\nTwój wybór: ")
                if (action == "W" or action == "w"):
                    self.user_log()
                elif (action == "P" or action =="p"):
                    self.user_menu()
                    
    def newuser_reg(self):
        print()
        print(linia)
        print("Rejestracja nowego użytkownika")
        newuser_e_mail = input("Podaj adres e-mail (bedzie wykorzystywany do logowania): ")
        while (self.check_e_mail_correct(newuser_e_mail) != 1):
            print()
            print("Podany ciąg nie jest adresem e-mail")
            action = input("(W)prowadz e-mail ponownie\n(P)owrót do MENU LOGOWANIA\nTwój wybór: ")
            while (action != "W" and action != "w" and action != "P" and action != "p"):
                print()
                print("Wprowadzono niepoprawny klawisz")  
                action = input("(W)prowadz e-mail ponownie\n(P)owrót do MENU LOGOWANIA\nTwój wybór: ")
            if (action == "W" or action == "w"):
                self.newuser_reg()
            elif (action == "P" or action =="p"):
                self.user_menu()            
        newuser_pass1 = input("Podaj hasło: ")
        newuser_pass2 = input("Powtórz hasło: ")
        while (newuser_pass1 != newuser_pass2):
            print()
            print("Hasła nie są identyczne")
            action = input("(W)prowadź hasło od początku\n(P)owrót do MENU LOGOWANIA\nTwój wybór: ")
            while (action != "W" and action != "w" and action != "P" and action != "p"):
                print()
                print("Wprowadzono niepoprawny klawisz")
                action = input("(W)prowadź hasło od początku\n(P)owrót do MENU LOGOWANIA\nTwój wybór: ")
            if (action == "W" or action == "w"):
                print()
                newuser_pass1 = input("Podaj hasło: ")
                newuser_pass2 = input("Powtórz hasło: ")
            elif (action == "P" or action =="p"):
                self.user_menu()                
        self.c.execute("select * from cities;")
        result_newuser_cities = self.c.fetchall()
        print()
        print("Dodaj miasto do swojego konta")
        print("Które z pośród podanych miast chcesz przypisać do swojego konta:")
        print("ID", " Miasto")
        for v in result_newuser_cities:
            id = v[0]
            city = v[1]
            print("%-4s%-10s" % (id, city))
        print()
        action = input("Wprowadź numer miasta: (1) - (" + str(len(result_newuser_cities)) + ")\n(N)nie chcę dodać miasta do mojego konta\nTwój wybór: ")
                
    def user_panel(self, name):
        self.name = name
        print()
        print(linia)
        print("Witaj " + name)
        print(linia)
        print("MENU UŻYTKOWNIKA")
    
    def check_e_mail_correct(self, e_mail): # sprawdza czy podany przez użytkownika ciąg jest adresem e-mail
        i = 0
        test = 0
        while (i < len(e_mail)):
            if (e_mail[i] == '@'):
                test = 1
            i = i + 1
        return test   
    
class Waiter:
    
    # Po wybraniu konta Kelner uruchamiana jest klasa Waiter    
    
    def __init__(self, password):
        self.password = password
        self.conn = pymysql.connect("localhost", "waiters", self.password, "wolny_stolik")
        self.c = self.conn.cursor()   
        print()
        print(linia)        
        print("Strefa kelnera")
class Close:
    
    # Osobna klasa do zamykania aplikacji. 
    
    def __init__(self):
        print()
        print(linia)
        print("Zamknięcie aplikacji. Do zobaczenia") 

# Logo aplikacji

linia = "======================================="

print(linia)
print('Witaj w aplikacji "Wolny Stolik"')
print(linia)
print("Wersja bera | (c) Tomasz Prysak")
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