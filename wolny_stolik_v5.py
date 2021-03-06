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
        action = input("(U)żytkownik\n(K)elner\n(A)dministrator\n(W)wyjście z programu\nTwój wybór: ")
        while (action != "W" and action != "w" and action != "U" and action != "u" and action != "K" and action != "k" and action != "A" and action != "a"):
            print()
            print(linia)
            print("Wprowadzono niepoprawny klawisz")
            print("Wybierz rodzaj konta: ")
            action = input("(U)żytkownik\n(K)elner\n(A)dministrator\n(W)wyjście z programu\nTwój wybór: ")
        if (action == "U" or action == "u"):
            db_user_file = open("db_user.txt", "r")
            db_user_pass = db_user_file.read()
            db_user_file.close()
            start = User(db_user_pass)        
        elif (action == "K" or action == "k"):
            db_waiter_file = open("db_waiter.txt", "r")
            db_waiter_pass = db_waiter_file.read()
            db_waiter_file.close()
            start = Waiter(db_waiter_pass)        
        elif (action == "A" or action == "a"):
            db_admin = input("Wprowadź hasło administratora: ")
            start = Admin(db_admin)              
        else:     
            print()
            print(linia)
            print("Zamknięcie aplikacji. Do zobaczenia")        

class Admin:
    
    # Po wybraniu konta Administrator uruchamiana jest klasa Admin
    
    def __init__(self, password):
        self.password = password
        self.conn = pymysql.connect("localhost", "root", self.password, "wolny_stolik_5",  use_unicode=True, charset="utf8")
        self.c = self.conn.cursor()
        print()
        print(linia)        
        print("Zalogowano jako administrator")
        print("W budowie")

class User:
    
    # Po wybraniu konta Użytkownik uruchamiana jest klasa user
    
    def __init__(self, password):
        self.password = password
        self.conn = pymysql.connect("localhost", "users", self.password, "wolny_stolik_5",  use_unicode=True, charset="utf8")
        self.c = self.conn.cursor()
        self.user_menu()
        
    def user_menu(self):
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
            self.conn.close()
            start = MenuStart()
        
    def user_log(self):
        print()
        print(linia)
        self.user_e_mail = input("Podaj e-mail: ")
        user_pass = input("Podaj hasło: ")
        self.c.execute("select id_user, e_mail, pass from users where e_mail = '" + self.user_e_mail + "';")
        result_user_log = self.c.fetchall()
        self.id_user = result_user_log[0][0]
        while (len(result_user_log) == 0):
            print()
            print("Podany e-mail i/lub hasło są nieprawidłowe")
            action = input("(W)prowadź e-mail i hasło ponownie\n(P)owrót do MENU LOGOWANIA UŻYTKOWNIKA\nTwój wybór: ")
            while (action != "W" and action != "w" and action != "P" and action != "p"):
                print()
                print("Wprowadzono niepoprawny klawisz")  
                action = input("(W)prowadź e-mail i hasło ponownie\n(P)owrót do MENU LOGOWANIA UŻYTKOWNIKA\nTwój wybór: ")
            if (action == "W" or action == "w"):
                self.user_log()
            elif (action == "P" or action =="p"):
                self.user_menu()
        if (self.user_e_mail == result_user_log[0][1]):
            if (user_pass == result_user_log[0][2]):
                self.user_panel()
            else:
                print()
                print("Podany e-mail i/lub hasło są nieprawidłowe")
                action = input("(W)prowadź e-mail i hasło ponownie\n(P)owrót do MENU LOGOWANIA UŻYTKOWNIKA\nTwój wybór: ")
                while (action != "W" and action != "w" and action != "P" and action != "p"):
                    print()
                    print("Wprowadzono niepoprawny klawisz")  
                    action = input("(W)prowadź e-mail i hasło ponownie\n(P)owrót do MENU LOGOWANIA UŻYTKOWNIKA\nTwój wybór: ")
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
            print("Podany adres e-mail jest już zajęty lub podany ciąg znaków nie jest adresem e-mail")
            action = input("(W)prowadz e-mail ponownie\n(P)owrót do MENU LOGOWANIA UŻYTKOWNIKA\nTwój wybór: ")
            while (action != "W" and action != "w" and action != "P" and action != "p"):
                print()
                print("Wprowadzono niepoprawny klawisz")  
                action = input("(W)prowadz e-mail ponownie\n(P)owrót do MENU LOGOWANIA UŻYTKOWNIKA\nTwój wybór: ")
            if (action == "W" or action == "w"):
                self.newuser_reg()
            elif (action == "P" or action =="p"):
                self.user_menu()            
        newuser_pass1 = input("Podaj hasło: ")
        newuser_pass2 = input("Powtórz hasło: ")
        while (newuser_pass1 != newuser_pass2):
            print()
            print("Hasła nie są identyczne")
            action = input("(W)prowadź hasło od początku\n(P)owrót do MENU LOGOWANIA UŻYTKOWNIKA\nTwój wybór: ")
            while (action != "W" and action != "w" and action != "P" and action != "p"):
                print()
                print("Wprowadzono niepoprawny klawisz")
                action = input("(W)prowadź hasło od początku\n(P)owrót do MENU LOGOWANIA UŻYTKOWNIKA\nTwój wybór: ")
            if (action == "W" or action == "w"):
                print()
                newuser_pass1 = input("Podaj hasło: ")
                newuser_pass2 = input("Powtórz hasło: ")
            elif (action == "P" or action =="p"):
                self.user_menu()                
        self.c.execute("select * from cities;")
        result_newuser_cities = self.c.fetchall()
        print()
        print("Czy chcesz do swojego konta dołączyć jedno z ponizszych miast ?")
        print("---------------")
        print("ID  | Miasto")
        print("---------------")
        for v in result_newuser_cities:
            id = v[0]
            city = v[1]
            print("%-4s| %-10s" % (id, city))
        print("---------------")
        action = input("(T)ak\n(N)ie\nTwój wybór: ")
        while (action != "T" and action != "t" and action != "N" and action != "n"):
            print()
            print("Wprowadzono niepoprawny klawisz")
            action = input("(T)ak\n(N)ie\nTwój wybór: ")
        if (action == "T" or action == "t"):
            action = input("Wprowadź numer miasta: (1) - (" + str(len(result_newuser_cities)) + "): ")
            self.c.execute("select * from cities where id_city = '" + action + "';")
            result_newuser_cities_2 = self.c.fetchall()
            while (len(result_newuser_cities_2) == 0):
                print()
                print("Wprowadzono niprawidłowy numer miasta")
                action = input("Wprowadź prawidłowy numer miasta: (1) - (" + str(len(result_newuser_cities)) + "): ")
                self.c.execute("select * from cities where id_city = '" + action + "';")
                result_newuser_cities_2 = self.c.fetchall()
            print()
            print("Wybrałeś miasto: " + result_newuser_cities_2[0][1])
            action = input("Naciśnij ENTER, aby potwierdzić utworzenie użytkownika " + newuser_e_mail + "\n(P)owrót do MENU LOGOWANIA UŻYTKOWNIKA (kasuje dotychczas wprowadzone dane)\nTwój wybór: ")
            while (action != "" and action != "P" and action != "p"):
                print()
                print("Wprowadzono niepoprawny klawisz")             
                action = input("Naciśnij ENTER, aby potwierdzić utworzenie użytkownika " + newuser_e_mail + "\n(P)owrót do MENU LOGOWANIA UŻYTKOWNIKA (kasuje dotychczas wprowadzone dane)\nTwój wybór: ")
            if (action == ""):
                self.c.execute('insert into users (e_mail, pass, id_city, date_login) values ("' + newuser_e_mail + '", "' + newuser_pass1 + '", ' + str(result_newuser_cities_2[0][0]) + ', now());')
                self.conn.commit()
                print()
                print("Konto użytkownika " + newuser_e_mail + " utworzone pomyślnie !")
                action = input("Naciśnij ENTER, aby przejść do menu logowania: ")
                while (action != ""):
                    print()
                    print("Wprowadzono niepoprawny klawisz")
                    action = input("Naciśnij ENTER, aby przejść do menu logowania: ")
                self.user_menu()
            else:
                self.user_menu()
        elif (action == "N" or action =="n"):
            print()
            action = input("Naciśnij ENTER, aby potwierdzić utworzenie użytkownika " + newuser_e_mail + "\n(P)owrót do MENU LOGOWANIA UŻYTKOWNIKA (kasuje dotychczas wprowadzone dane)\nTwój wybór: ")
            while (action != "" and action != "P" and action != "p"):
                print()
                print("Wprowadzono niepoprawny klawisz")            
                action = input("Naciśnij ENTER, aby potwierdzić utworzenie użytkownika " + newuser_e_mail + "\n(P)owrót do MENU LOGOWANIA UŻYTKOWNIKA (kasuje dotychczas wprowadzone dane)\nTwój wybór: ")
            if (action == ""):
                self.c.execute('insert into users (e_mail, pass, date_login) values ("' + newuser_e_mail + '", "' + newuser_pass1 + '", now());')
                self.conn.commit()
                print()
                print("Konto użytkownika " + newuser_e_mail + " utworzone pomyślnie !")
                action = input("Naciśnij ENTER, aby przejść do menu logowania: ")
                while (action != ""):
                    print()
                    print("Wprowadzono niepoprawny klawisz")
                    action = input("Naciśnij ENTER, aby przejść do menu logowania: ")
                self.user_menu()
            else:
                self.user_menu() 
            
    def user_panel(self):
        print()
        print(linia)
        print("Witaj " + self.user_e_mail)
        print(linia)
        print("MENU UŻYTKOWNIKA")
        action = input("(S)zukaj WOLNY STOLIK\n(M)oje rezerwacje\n(W)yloguj\nTwój wybór: ")
        while (action != "S" and action != "s" and action != "M" and action != "m" and action != "U" and action != "u" and action != "W" and action != "w"):
            print()
            print(linia)
            print("Wprowadzono niepoprawny klawisz")        
            action = input("(S)zukaj WOLNY STOLIK\n(M)oje rezerwacje\n(W)yloguj\nTwój wybór: ")
        if (action == "S" or action == "s"):
            self.wolny_stolik()
        elif (action == "M" or action == "m"):
            print()
            print("W budowie")
            action = input("Naciśnij ENTER, aby przejść do MENU UŻYTKOWNIKA: ")
            while (action != ""):
                print()
                print("Wprowadzono niepoprawny klawisz")          
                action = input("Naciśnij ENTER, aby przejść do MENU UŻYTKOWNIKA: ")
            self.user_panel()
        else:
            self.user_menu()
            
    def wolny_stolik(self):
        print()
        print(linia)
        print("MENU WOLNY STOLIK")
        print("Powiedz jak bardzo jesteś głodny: ")
        action = input("(J)uż jestem głodny! Szukaj aktualnie WOLNY STOLIK\n(B)ędę głodny w przyszłości. Dokonaj rezerwacji WOLNY STOLIK z wyprzedzeniem\n(P)owrót do MENU UŻYTKOWNIKA\nTwój wybór: ")
        while (action != "J" and action != "j" and action != "B" and action != "b" and action != "P" and action != "p"):
            print()
            print(linia)
            print("Wprowadzono niepoprawny klawisz")
            print("Powiedz jak bardzo jesteś głodny: ")        
            action = input("(J)uż jestem głodny! Szukaj aktualnie WOLNY STOLIK\n(B)ędę głodny w przyszłości. Dokonaj rezerwacji WOLNY STOLIK z wyprzedzeniem\n(P)owrót do MENU UŻYTKOWNIKA\nTwój wybór: ")       
        if (action == "J" or action == "j"):
            self.wolny_stolik_now()
        elif (action == "B" or action == "b"):
            print()
            print("W budowie")
            action = input("Naciśnij ENTER, aby przejść do MENU WOLNY STOLIK: ")
            while (action != ""):
                print()
                print("Wprowadzono niepoprawny klawisz")          
                action = input("Naciśnij ENTER, aby przejść do MENU WOLNY STOLIK: ")
            self.wolny_stolik()            
        elif (action == "P" or action == "p"):
            self.user_panel()
    
    def wolny_stolik_now(self):
        self.c.execute("select id_rest, rest_name, type_cuisine, round(avg(value_rating),1) as 'Ocena' from restaurants natural left join rating natural left join cities natural right join cuisines where city_name = ((select city_name from cities natural left join users where e_mail = '" + self.user_e_mail + "')) group by rest_name order by city_name desc, Ocena desc;")
        result_search_now_1 = self.c.fetchall()
        i = 1
        list_rest = {}
        napis1 = "ID"
        napis2 = "Restauracja"
        napis3 = "Rodzaj kuchni"
        napis4 = "Ocena"
        napis5 = "Ilość wolnych stolików: "
        print()
        print("Restauracje w mieście przypisanym do Twojego konta, w których aktualnie jest WOLNY STOLIK:")
        print("-"*85)
        print("| %-4s| %-20s| %-15s| %-8s| %-26s |" % (napis1, napis2, napis3, napis4, napis5))
        print("-"*85)         
        for v in result_search_now_1:
            a = int(self.count_all_table_in_rest(v[1]))
            b = int(self.count_occ_and_book_table_in_rest(v[1]))
            c = a - b
            if (a - b > 0):
                id = i
                rest = v[1]
                cuisine = v[2]
                rate = v[3]
                print("| %-4s| %-20s| %-15s| %-8s| %-26s |" % (id, rest, cuisine, rate, napis5 + str(c)))
                print("-"*85)
                list_rest[str(i)] = rest
                i = i + 1
        action = input("Wprowadź numer restauracji w której chcesz ZAKLEPAĆ, na 15 minut, stolik: ")
        while (action not in list_rest):
            print()
            print("Wprowadzono błędny numer restauracji")
            action = input("Wprowadź numer restauracji w której chcesz ZAKLEPAĆ, na 15 minut, stolik: ")
        self.c.execute("select id_table, nr_table, qty_chairs from type_tables natural left join restaurants where rest_name = '" + list_rest[action] + "';")
        result_search_now_2 = self.c.fetchall()
        napis1 = "NR STOLIKA"
        napis2 = "Ilość krzeseł przy stoliku"
        napis3 = "Uwagi"
        list = []
        print()
        print("Który stolik chcesz ZAKLEPAĆ:")
        print("-"*85)
        print("| %-11s| %-27s| %-40s|" % (napis1, napis2, napis3))
        print("-"*85)
        for v in result_search_now_2:
            if (self.check_table_is_occ(v[0]) == 0 and self.check_table_is_book_15_min(v[0]) == 0):
                nr = v[1]
                qty = v[2]
                at = ""
                print("| %-11s| %-27s| %-40s|" % (nr, qty, at))
                print("-"*85)
                list.append(nr)
            #elif (self.check_table_is_occ(v[0]) == 0 and self.check_table_is_book_15_min(v[0]) == 2):
                #nr = v[1]
                #qty = v[2]
                #at = "Stolik zarezerwowany od godziny: "
                #print("| %-11s| %-27s| %-50s|" % (nr, qty, at + self.check_book_start(v[0])))
                #print("-"*95)
                #list.append(nr)                
        while ((self.check_nr_table_is_int() == False) or (self.nr_table not in list)):
            print()
            print("Wprowadzono błędny nr stolik")
        print()
        print("Wybrano stolik: " + str(self.nr_table))
        action = input("Naciśnij ENTER, aby potwierdzić ZAKLEPANIE stolika: " + str(self.nr_table) + "\n(P)owrót do MENU WOLNY STOLIK (kasuje dotychczas wprowadzone dane)\nTwój wybór: ")
        while (action != "" and action != "P" and action != "p"):
            print()
            print("Wprowadzono niepoprawny klawisz")          
            action = input("Naciśnij ENTER, aby potwierdzić ZAKLEPANIE stolika: " + str(self.nr_table) + "\n(P)owrót do MENU WOLNY STOLIK (kasuje dotychczas wprowadzone dane)\nTwój wybór: ")
        if (action == ""):
            self.c.execute("insert into booking_now (id_user, id_table, date_book_now) values (" + str(self.id_user) + ", " + str(self.nr_table) + ", now());")
            self.conn.commit()
            print()
            print("ZAKLEPANO stolik: " + str(self.nr_table) + " , masz 15 minut na dojście do restauracji")
            action = input("Naciśnij ENTER, aby przejść do MENU WOLNY STOLIK: ")
            while (action != ""):
                print()
                print("Wprowadzono niepoprawny klawisz")
                action = input("Naciśnij ENTER, aby przejść do MENU WOLNY STOLIK: ")
            self.wolny_stolik()            
        else:
            self.wolny_stolik()
     
    def count_occ_and_book_table_in_rest(self, rest_name):
        occ_and_book = 0
        self.c.execute("select id_table, nr_table, qty_chairs from type_tables natural left join restaurants where rest_name = '" + rest_name + "';")
        all_table_form = self.c.fetchall()
        for v in all_table_form:
            if (self.check_table_is_occ(v[0]) != 0):
                occ_and_book = occ_and_book + 1
            if (self.check_table_is_book_15_min(v[0]) == 1):
                occ_and_book = occ_and_book + 1   
        return occ_and_book
    
    #def check_book_start(self, id_table):
        #self.c.execute('select date_format(date_book_start, "%H:%i") from booking where timestampdiff(minute, now(), date_book_start) > 0 and timestampdiff(minute, now(), date_book_start) <= 90 and id_table = ' + str(id_table) + ';')
        #date_book_start = self.c.fetchall()
        #return date_book_start[0][0]
    
    def check_table_is_occ(self, id_table):
        self.c.execute("select * from occupancy where id_table = '" + str(id_table) + "';")        
        check_table_occ = self.c.fetchall()
        return len(check_table_occ)
    
    def check_table_is_book_15_min(self, id_table):
        self.c.execute("select case when timestampdiff(minute, now(), date_book_now) > 90 then 3 when timestampdiff(minute, now(), date_book_now) > 0 and timestampdiff(minute, now(), date_book_now) <= 90 then 2 when timestampdiff(minute, now(), date_book_now) <= 0 and timestampdiff(minute, now(), date_book_now) >= -15 then 1 else 0 end from booking_now where id_table = '" + str(id_table) + "';")
        check_table_book = self.c.fetchall()
        if (len(check_table_book) == 0):
            return 0
        else:
            if (check_table_book[0][0] == 0):
                self.c.execute("delete from booking_now where id_table = '" + str(id_table) + "' and timestampdiff(minute, now(), date_book_now) < -15;")
                self.conn.commit()
                return 0
            elif (check_table_book[0][0] == 1):
                return 1
            #elif (check_table_book[0][0] == 2):
                #return 2 
            #elif (check_table_book[0][0] == 3):
                #return 0
    
    def count_all_table_in_rest(self, rest_name):
        self.c.execute("select count(nr_table) from type_tables natural left join restaurants where rest_name = '" + rest_name + "' group by id_rest;")
        all_table_in_rest = self.c.fetchall()
        return all_table_in_rest[0][0]     
            
    def check_nr_table_is_int(self): # sprawdza czy wprowadzona wartość przez użytkownika jest integer w celu dokonania zaklepania stolika
        while(True):
            try:
                self.nr_table = int(input("Wybierz NR STOLIKA, aby ZAKLEPAĆ go na 15 minut: "))
                test = True
                break
            except:
                print()
                print("Wprowadzono błędny nr stolik")
        return test     
    
    def check_e_mail_correct(self, e_mail): # sprawdza czy podany przez użytkownika login jest już zajęty lub jeżeli nie jest to czy podany ciąg znaków jest adresem e-mail (czy zawiera symbol "@") 
        i = 0
        test = 0
        self.c.execute("select e_mail, pass from users where e_mail = '" + e_mail + "';")
        result = self.c.fetchall()        
        if (len(result) !=0):
            test = 0
        else:
            while (i < len(e_mail)):
                if (e_mail[i] == '@'):
                    test = 1
                i = i + 1
        return test   
    
class Waiter:
    
    # Po wybraniu konta Kelner uruchamiana jest klasa Waiter    
    
    def __init__(self, password):
        self.password = password
        self.conn = pymysql.connect("localhost", "waiters", self.password, "wolny_stolik_5",  use_unicode=True, charset="utf8")
        self.c = self.conn.cursor() 
        self.waiter_menu()        
        
    def waiter_menu(self):
        print()
        print(linia)        
        print("MENU LOGOWANIA KELNERA")
        print("Stworzenie nowego użytkownika typu kelner wymaga kontaktu z administratorem")
        action = input("(L)ogowanie kelnera\n(P)owrót do MENU START\nTwój wybór: ")
        while (action != "P" and action != "p" and action != "L" and action != "l"):
            print()
            print("Wprowadzono niepoprawny klawisz")            
            action = input("(L)ogowanie kelnera\n(P)owrót do MENU START\nTwój wybór: ")
        if (action == "L" or action == "l"):
            self.waiter_log()
        else:
            self.conn.close()
            start = MenuStart()   
                
    def waiter_log(self):
        print()
        print(linia)
        self.waiter_login = input("Podaj login: ")
        waiter_pass = input("Podaj hasło: ")
        self.c.execute("select login, pass, rest_name from waiters natural left join restaurants where login = '" + self.waiter_login + "';")
        result_waiter_log = self.c.fetchall()
        while (len(result_waiter_log) == 0):
            print()
            print("Podany login i/lub hasło są nieprawidłowe")
            action = input("(W)prowadź login i hasło ponownie\n(P)owrót do MENU LOGOWANIA KELNERA\nTwój wybór: ")
            while (action != "W" and action != "w" and action != "P" and action != "p"):
                print()
                print("Wprowadzono niepoprawny klawisz")  
                action = input("(W)prowadź e-mail i hasło ponownie\n(P)owrót do MENU LOGOWANIA KELNERA\nTwój wybór: ")
            if (action == "W" or action == "w"):
                self.waiter_log()
            else:
                self.waiter_menu()
        if (self.waiter_login == result_waiter_log[0][0]):
            if (waiter_pass == result_waiter_log[0][1]):
                self.waiter_rest = result_waiter_log[0][2]
                self.waiter_panel()
            else:
                print()
                print("Podany login i/lub hasło są nieprawidłowe")
                action = input("(W)prowadź login i hasło ponownie\n(P)owrót do MENU LOGOWANIA UŻYTKOWNIKA\nTwój wybór: ")
                while (action != "W" and action != "w" and action != "P" and action != "p"):
                    print()
                    print("Wprowadzono niepoprawny klawisz")  
                    action = input("(W)prowadź e-mail i hasło ponownie\n(P)owrót do MENU LOGOWANIA UŻYTKOWNIKA\nTwój wybór: ")
                if (action == "W" or action == "w"):
                    self.waiter_log()
                else:
                    self.waiter_menu()  
                    
    def waiter_panel(self):
        print()
        print(linia)
        print("Kelner: " + self.waiter_login + " | Restauracja: " + self.waiter_rest)
        print(linia)
        print("MENU KELNERA")
        action = input("(O)twórz nowy rachunek\n(Z)amknij bieżący rachunek\n(S)prawdź rezerwacje\n(W)yloguj\nTwój wybór: ")       
        while (action != "O" and action != "o" and action != "Z" and action != "z" and action != "S" and action != "s" and action != "H" and action != "h" and action != "W" and action != "w"):
            print()
            print(linia)
            print("Wprowadzono niepoprawny klawisz")        
            action = input("(O)twórz nowy rachunek\n(Z)amknij bieżący rachunek\n(S)prawdź rezerwacje\n(H)istoria konta\n(W)yloguj\nTwój wybór: ")
        if (action == "O" or action == "o"):
            self.count_table_occ_start()
        elif (action == "Z" or action == "z"):
            self.count_table_occ_stop()
        elif (action == "S" or action == "s"):
            print()
            print("W budowie")
            action = input("Naciśnij ENTER, aby przejść do MENU KELNERA: ")
            while (action != ""):
                print()
                print("Wprowadzono niepoprawny klawisz")          
                action = input("Naciśnij ENTER, aby przejść do MENU KELNERA: ")
            self.waiter_panel()            
        else:
            self.waiter_menu() 
    
    def count_table_occ_start(self):
        self.c.execute("select count(nr_table) from type_tables natural left join restaurants where rest_name = '" + self.waiter_rest + "' group by id_rest;")
        result_qty_table_in_rest = self.c.fetchall()
        self.c.execute("select count(nr_table) from occupancy natural left join restaurants natural left join type_tables where rest_name = '" + self.waiter_rest + "' group by id_rest;")
        result_qty_table_occ = self.c.fetchall()
        if (len(result_qty_table_occ) == 0):
            self.occupancy_start()
        elif (result_qty_table_occ[0][0] == result_qty_table_in_rest[0][0]):
            print()
            print("Brak wolnych stolików")
            action = input("Naciśnij ENTER, aby wrócić do MENU KELNERA: ")
            while (action != ""):
                print()
                print("Wprowadzono niepoprawny klawisz")
                action = input("Naciśnij ENTER, aby wrócić do MENU KELNERA: ")
            self.waiter_panel()
        else:
            self.occupancy_start()
            
    def occupancy_start(self):
        self.c.execute("select nr_table, qty_chairs from type_tables natural left join restaurants where rest_name = '" + self.waiter_rest + "';")
        result_search_now = self.c.fetchall() 
        napis1 = "NR STOLIKA"
        napis2 = "Ilość krzeseł przy stoliku"
        napis3 = "Status"
        print()
        print("Aktualny status stolików:")
        print("-"*100)
        print("| %-11s| %-27s| %-54s |" % (napis1, napis2, napis3))
        print("-"*100)
        i = 1
        list = []
        for v in result_search_now:
            self.c.execute("delete from booking_now where id_table = '" + str(i) + "' and timestampdiff(minute, now(), date_book_now) < -15;")
            self.conn.commit()               
            self.c.execute("select rest_name, nr_table, login, qty_chairs, time_occ_start from occupancy natural join type_tables natural join restaurants natural left join waiters where rest_name = '" + self.waiter_rest + "' and nr_table = '" + str(i) + "';")
            result_is_it_occ = self.c.fetchall()
            self.c.execute("select rest_name, id_table, nr_table, qty_chairs, e_mail, date_book_now from restaurants natural join type_tables natural join users natural join booking_now where id_table = '" + str(i) + "';")
            result_is_it_book = self.c.fetchall()           
            if (len(result_is_it_occ) == 0 and len(result_is_it_book) == 0):
                nr = v[0]
                qty = v[1]
                stat = "WOLNY"
                print("| %-11s| %-27s| %-54s |" % (nr, qty,stat))
                print("-"*100)
                list.append(nr)
            elif (len(result_is_it_occ) == 0 and len(result_is_it_book) != 0):
                nr = v[0]
                qty = v[1]
                stat = "ZAKLEPANY przez użtykownika: " + result_is_it_book[0][4]
                print("| %-11s| %-27s| %-54s |" % (nr, qty,stat))
                print("-"*100)
                list.append(nr)                
            else:
                nr = v[0]
                qty = v[1]
                stat = "ZAJĘTY przez: " + result_is_it_occ[0][2]
                print("| %-11s| %-27s| %-54s |" % (nr, qty,stat,))
                print("-"*100)           
            i = i + 1
        while ((self.check_nr_table_occ_start() == False) or (self.nr_table not in list)):
            print()
            print("Wprowadzono błędny nr stolik lub stolik jest już zajęty")
        print()
        print("Wybrano stolik: " + str(self.nr_table))
        action = input("Naciśnij ENTER, aby potwierdzić otwarcie rachunku dla stolika: " + str(self.nr_table) + "\n(P)owrót do MENU KELNERA (kasuje dotychczas wprowadzone dane)\nTwój wybór: ")        
        while (action != "" and action != "P" and action != "p"):
            print()
            print("Wprowadzono niepoprawny klawisz")             
            action = input("Naciśnij ENTER, aby potwierdzić otwarcie rachunku dla stolika: " + str(self.nr_table) + "\n(P)owrót do MENU KELNERA (kasuje dotychczas wprowadzone dane)\nTwój wybór: ")
        if(action == ""):
            self.c.execute("select id_wait login, pass from waiters where login = '" + self.waiter_login + "';")
            result_waiter_log = self.c.fetchall()
            self.c.execute("select id_table, nr_table, rest_name from type_tables natural left join restaurants where nr_table = '" + str(self.nr_table) + "' and rest_name = '" + self.waiter_rest + "';")
            result_id_table = self.c.fetchall()
            self.c.execute("delete from booking_now where id_table = '" + str(result_id_table[0][0]) + "' and timestampdiff(minute, now(), date_book_now) <= 0;")
            self.conn.commit()            
            self.c.execute('insert into occupancy (id_table, id_wait, time_occ_start) values (' + str(result_id_table[0][0]) + ', ' + str(result_waiter_log[0][0]) + ', now());')
            self.conn.commit()
            print()
            print("Otworzono rachunek dla stolika: " + str(self.nr_table))
            action = input("Naciśnij ENTER, aby przejść do MENU KELNERA: ")
            while (action != ""):
                print()
                print("Wprowadzono niepoprawny klawisz")
                action = input("Naciśnij ENTER, aby przejść do MENU KELNERA: ")
            self.waiter_panel() 
        else:
            self.waiter_panel()        
            
    def check_nr_table_occ_start(self): # sprawdza czy wprowadzona wartość przez kelnera jest integer w celu dokonania zajętości stolika
        while(True):
            try:
                self.nr_table = int(input("Wybierz NR wolnego STOLIKA, aby otworzyć rachunek (dokonać zajętości stolika): "))
                test = True
                break
            except:
                print()
                print("Wprowadzono błędny nr stolik lub stolik jest już zajęty")
        return test        
        
    def count_table_occ_stop(self):
        self.c.execute("select nr_table, qty_chairs from occupancy natural left join type_tables natural left join waiters where login = '" + self.waiter_login + "' order by nr_table;")
        result_waiter_occ = self.c.fetchall()
        if (len(result_waiter_occ) == 0):
            print()
            print("Brak otwartych rachunków na Twoim koncie")
            action = input("Naciśnij ENTER, aby wrócić do MENU KELNERA: ")
            while (action != ""):
                print()
                print("Wprowadzono niepoprawny klawisz")
                action = input("Naciśnij ENTER, aby wrócić do MENU KELNERA: ")
            self.waiter_panel()
        else:
            self.occupancy_stop()
    
    def occupancy_stop(self):
        self.c.execute("select nr_table, qty_chairs from occupancy natural left join type_tables natural left join waiters where login = '" + self.waiter_login + "' order by nr_table;")
        result_waiter_occ = self.c.fetchall()
        napis1 = "NR STOLIKA"
        napis2 = "Ilość krzeseł przy stoliku"
        print()
        print("Obsługiwane przez Ciebie stoliki:")  
        print("-"*43)
        print("| %-11s| %-27s|" % (napis1, napis2))
        print("-"*43) 
        list = []
        for v in result_waiter_occ:
            nr = v[0]
            qty = v[1]
            print("| %-11s| %-27s|" % (nr, qty))
            print("-"*43)
            list.append(nr)
        while ((self.check_nr_table_occ_stop() == False) or (self.nr_table not in list)):
            print()
            print("Wprowadzono błędny nr stolik")
        print()
        print("Wybrano stolik: " + str(self.nr_table))
        action = input("Naciśnij ENTER, aby potwierdzić zamknięcie rachunku dla stolika (zwolnić stolik): " + str(self.nr_table) + "\n(P)owrót do MENU KELNERA (kasuje dotychczas wprowadzone dane)\nTwój wybór: ")
        while (action != "" and action != "P" and action != "p"):
            print()
            print("Wprowadzono niepoprawny klawisz")          
            action = input("Naciśnij ENTER, aby potwierdzić zamknięcie rachunku dla stolika (zwolnić stolik): " + str(self.nr_table) + "\n(P)owrót do MENU KELNERA (kasuje dotychczas wprowadzone dane)\nTwój wybór: ")
        if (action == ""):
            self.c.execute("select id_table, nr_table, rest_name from type_tables natural left join restaurants where nr_table = '" + str(self.nr_table) + "' and rest_name = '" + self.waiter_rest + "';")
            result_id_table = self.c.fetchall()    
            self.c.execute("delete from occupancy where id_table = '" + str(result_id_table[0][0]) + "';")
            self.conn.commit()
            print()
            print("Zamknięto rachunek dla stolika (zwolniono stolik): " + str(self.nr_table))
            action = input("Naciśnij ENTER, aby przejść do MENU KELNERA: ")
            while (action != ""):
                print()
                print("Wprowadzono niepoprawny klawisz")
                action = input("Naciśnij ENTER, aby przejść do MENU KELNERA: ")
            self.waiter_panel()            
        else:
            self.waiter_panel() 
            
    def check_nr_table_occ_stop(self): # sprawdza czy wprowadzona wartość przez kelnera jest integer w celu dokonania zwolnienia stolika
        while(True):
            try:
                self.nr_table = int(input("Wybierz NR STOLIKA, aby zamknąć rachunek (zwolnić stolik): "))
                test = True
                break
            except:
                print()
                print("Wprowadzono błędny nr stolik")
        return test           

# Logo aplikacji

linia = "=========================================="

print(linia)
print('Witaj w aplikacji "Wolny Stolik"')
print(linia)
print("Wersja beta | (c) Tomasz Prysak")
print(linia)
print("|    W W W   OOO   L      N   N  Y   Y   |")
print("|    W W W  O   O  L      N   N  Y   Y   |")
print("|    W W W  O   O  L      NN  N   Y Y    |")
print("|    W W W  O   O  L      N N N    Y     |")
print("|    W W W  O   O  L      N  NN    Y     |")
print("|    W W W  O   O  L      N   N    Y     |")
print("|     W W    OOO   LLLLL  N   N    Y     |")
print("|                                        |")
print("|                                        |")
print("|   SSS   TTTTT   OOO   L      I  K   K  |")
print("|  S   S    T    O   O  L      I  K  K   |")
print("|  S        T    O   O  L      I  K K    |")
print("|   SSS     T    O   O  L      I  KK     |")
print("|      S    T    O   O  L      I  K K    |")
print("|  S   S    T    O   O  L      I  K  K   |")
print("|   SSS     T     OOO   LLLLL  I  K   K  |")
print(linia)
next = input("Naciśnij ENTER aby kontynuować: ")

while (next != ""):
    print()
    print(linia)
    print("Wprowadzono niepoprawny kawisz")
    next = input("Naciśnij ENTER aby kontynuować: ")
    
start = MenuStart()