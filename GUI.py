from msilib.schema import Error
import os
import pickle
import tkinter as tk
from tkinter import ttk
import datetime
from tkinter import messagebox
import filetype
from Roslina import Roslina
from RoslinaDoniczkowa import RoslinaDoniczkowa
from RoslinaOgrodowa import RoslinaOgrodowa
from Uzytkownik import Uzytkownik

BG = 'white'    # kolor tła dla widgetów

class TkinterPlantsApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        # ustawiamy tytuł i protokół zamknięcia
        tk.Tk.wm_title(self, "PlantsApp")
        self.protocol("WM_DELETE_WINDOW", self.zapisz_i_zamknij)

        # wczytujemy dotychczasową bazę użytkowników i ich rośliny korzystając z biblioteki pickle
        self.bazaUzytkownikow = []
        with open("uzytkownicy.pkl", "rb") as f:
            while True:
                try:
                    self.bazaUzytkownikow.append(pickle.load(f))
                except EOFError:
                    break

        # tworzymy atrybut okno i wywolujemy fukcje pokaz_okno aby wyświetlić OknoStartowe
        self._okno = None
        self.pokaz_okno(OknoStartowe)
        

    # funkcja odpowiada za wyświetlanie okna podanego w parametrze
    # ustawiamy tło okna (bo okna dziedziczą z tk.Canvas)
    # chcemy żeby okno pokrywało cały dostępny obszar z poprzedniego okna

    def pokaz_okno_zdjecie(self, okno, zdjecie, *args, **kw):
        self._okno = okno(self, *args, **kw)
        self.img = tk.PhotoImage(file = zdjecie)
        self._okno.create_image(50, 50, anchor='nw', image=self.img)
        self._okno.grid(row=0, column=0, sticky="nsew")
        self._okno.grid_propagate(0)

    def pokaz_okno(self, okno, *args, **kw):
        self._okno = okno(self, *args, **kw)
        self.bg = tk.PhotoImage(file = "images/bg3.png")
        self._okno.create_image(0, 0, anchor='nw', image=self.bg)
        self._okno.grid(row=0, column=0, sticky="nsew")
        self._okno.grid_propagate(0)
        
    # funkcja sprawdza czy email z parametru jest w bazie uzytkownikow
    # jesli jest zwraca True, jeśli nie zwraca False
    def czy_email_zajety(self, email):
        for uzytkownik in self.bazaUzytkownikow:
            if uzytkownik.email == email:
                return True
        return False

    # funkcja sprawdza czy login z parametru jest w bazie uzytkownikow
    # jesli jest zwraca True, jeśli nie zwraca False
    def czy_login_zajety(self, login):
        for uzytkownik in self.bazaUzytkownikow:
            if uzytkownik.login == login:
                return True
        return False

    # funkcja sprawdza w bazie użytkowników czy hasło podane w parametrze pasuje do emailu/loginu z parametru
    # jesli pasuje zwraca tego użytkownika, jeśli nie zwraca None
    def walidacja_uzytkownika(self, email_login, haslo):
        for uzytkownik in self.bazaUzytkownikow:
            if uzytkownik.email == email_login or uzytkownik.login == email_login:
                if uzytkownik.haslo == haslo:
                    return uzytkownik
                else:
                    return None
        return None
    
    # funkkcja dodaje użytkownika z parametru do bazy użytkowników
    def dodaj_uzytkownika(self, uzytkownik):
            self.bazaUzytkownikow.append(uzytkownik)

    # funkcja odpowiada za zapisanie bazy użytkowników do pliku przy pomocy biblioteki pickle
    # następnie zamyka okno
    def zapisz_i_zamknij(self):
        self.zapisz()
        self.destroy()

    def zapisz(self):
        with open('uzytkownicy.pkl', 'wb') as f:
            for uzytkownik in self.bazaUzytkownikow:
                pickle.dump(uzytkownik, f)

    def zapisz_i_zamknij_event(self, event):
        self.zapisz_event(event)
        self.destroy()

    def zapisz_event(self, event):
        with open('uzytkownicy.pkl', 'wb') as f:
            for uzytkownik in self.bazaUzytkownikow:
                pickle.dump(uzytkownik, f)

# pierwsze widoczne okno z wyborem logowania lub zakładania konta
class OknoStartowe(tk.Canvas):
    def __init__(self, parent):
        # ustawiamy wielkość okna
        tk.Canvas.__init__(self, parent, height=500, width=600)
        
        # okno bedzie mieć 1 kolumnę
        self.columnconfigure(0, weight=1)

        # tworzymy pasek menu
        self.menu = tk.Menu(parent)
        self.menu.add_command(label="Wyjdź", command=parent.zapisz_i_zamknij, accelerator="Ctrl+Q")
        parent.bind("<Control-q>", parent.zapisz_i_zamknij_event)
        parent.config(menu=self.menu)
        
        # nagłówek powitalny
        label = ttk.Label(self, text="Witaj w PlantsApp!", font=16)
        label.configure(background=BG)
        label.grid(row=0, column=0, pady=(70,20))

        # przycisk który otwiera okno logowania
        button = ttk.Button(self, text="Zaloguj się", padding=5, command=lambda: parent.pokaz_okno(OknoLogowania))
        button.grid(row=1, column=0,pady=10)
        
        # przycisk który otwiera okno tworzenia konta
        button2 = ttk.Button(self, text="Załóż konto", padding=5, command=lambda: parent.pokaz_okno(OknoTworzeniaKonta))
        button2.grid(row=2, column=0,pady=10)

# okno do wpisywania danych logowania
class OknoLogowania(tk.Canvas):
    def __init__(self, parent):
        tk.Canvas.__init__(self, parent)

        # funkcja sprawdza czy email i haslo są poprawne
        # jesli tak to otwiera okno główne, jeśli nie to wyświetla informację o błędzie
        def sprawdz_dane():
            email_login = email_login_entry.get()
            haslo = haslo_entry.get()
            uzytkownik = parent.walidacja_uzytkownika(email_login, haslo)
            if uzytkownik != None:
                self.uzytkownik = uzytkownik
                parent.pokaz_okno(OknoGlowne, uzytkownik)
            else:
                messagebox.showerror("Błąd", "Niepoprawne dane. Spróbuj ponownie.")

        # okno będzie miało 2 kolumny
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)

        # tworzymy pasek menu
        self.menu = tk.Menu(parent)
        self.menu.add_command(label="Wyjdź", command=parent.zapisz_i_zamknij, accelerator="Ctrl+Q")
        parent.bind("<Control-q>", parent.zapisz_i_zamknij_event)
        parent.config(menu=self.menu)
        
        # tworzymy pasek narzędzi i umieszczamy na nim przycisk powrotu do poprzedniego okna (OknoStartowe)
        self.toolbar = tk.Frame(self)
        self.toolbar_images = []
        image = "images/powrot.png"
        image = os.path.join(os.path.dirname(__file__), image)
        image = tk.PhotoImage(file=image)
        self.toolbar_images.append(image)
        button = ttk.Button(self.toolbar, image=image, command=lambda: parent.pokaz_okno(OknoStartowe))
        button.grid(row=0, column=0)
        self.toolbar.grid(row=0, column=0, columnspan=2, sticky=tk.NSEW)

        # umieszczamy nagłówek i pole do wpisania emailu lub loginu
        email_login_label = ttk.Label(self, text="Email lub login: ")
        email_login_label.configure(background=BG)
        email_login_label.grid(column=0, row=1, padx=10, pady=(70,10), sticky='E')
        email_login_entry = ttk.Entry(self, width=40)
        email_login_entry.grid(column=1, row=1, padx=10, pady=(70,10), sticky='W')

        # umieszczamy nagłówek i pole do wpisania hasła
        haslo_label = ttk.Label(self, text="Hasło: ")
        haslo_label.configure(background=BG)
        haslo_label.grid(column=0, row=2, padx=10, pady=10, sticky='E')
        haslo_entry = ttk.Entry(self, width=40, show="*")
        haslo_entry.grid(column=1, row=2, padx=10, pady=10, sticky='W')

        # umieszczamy przycisk do logowania który wywołuje funkcję sprawdz_dane
        zaloguj_button = ttk.Button(self, text='Zaloguj', command=sprawdz_dane)
        zaloguj_button.grid(column=1, row=3, padx=100, pady=10, sticky='W')

# okno do wpisywania danych do założenia konta
class OknoTworzeniaKonta(tk.Canvas):
    def __init__(self, parent):
        tk.Canvas.__init__(self, parent)

        # funkcja sprawdza czy email i haslo są poprawne
        # jesli tak to wyświetla informację o powodzeniu i otwiera okno startowe, jeśli nie to wyświetla informację o błędzie
        def sprawdz_dane():
            email = email_entry.get()
            login = login_entry.get()
            haslo = haslo_entry.get()
            powtorz_haslo = powtorz_haslo_entry.get()

            if akceptacja_warunkow.get() == 1 and przetwarzanie_danych.get() == 1:
                if parent.czy_email_zajety(email):
                    messagebox.showerror("Błąd", "Email ma już konto.")
                elif parent.czy_login_zajety(login):
                    messagebox.showerror("Błąd", "Login jest zajęty.")
                elif haslo != powtorz_haslo:
                    messagebox.showerror("Błąd", "Hasła są rożne.")
                else:
                    try:
                        parent.dodaj_uzytkownika(Uzytkownik(email, login, haslo))
                        messagebox.showinfo("Informacja", "Konto utworzone poprawnie.")
                        parent.pokaz_okno(OknoStartowe)
                    except ValueError as error:
                        messagebox.showerror("Błąd", "{0}".format(error))
            else:
                messagebox.showerror("Błąd", "Musisz zaakceptować warunki i przetwarzanie danych.")

        # okno będzie miało 2 kolumny i 9 wierszy
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=4)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(6, weight=1)
        self.rowconfigure(7, weight=100)
        self.rowconfigure(8, weight=1)

        # tworzymy pasek menu
        self.menu = tk.Menu(parent)
        self.menu.add_command(label="Wyjdź", command=parent.zapisz_i_zamknij, accelerator="Ctrl+Q")
        parent.bind("<Control-q>", parent.zapisz_i_zamknij_event)
        parent.config(menu=self.menu)

        # tworzymy linię statusu
        self.statusbar = tk.Label(self, text="Oczekiwanie...", anchor=tk.W)
        self.statusbar.grid(row=8, column=0, columnspan=2, sticky=tk.EW)
        
        # tworzymy pasek narzędzi i umieszczamy na nim przycisk powrotu do poprzedniego okna (OknoStartowe)
        self.toolbar = tk.Frame(self)
        self.toolbar_images = []
        image = "images/powrot.png"
        image = os.path.join(os.path.dirname(__file__), image)
        image = tk.PhotoImage(file=image)
        self.toolbar_images.append(image)
        button = ttk.Button(self.toolbar, image=image, command=lambda: parent.pokaz_okno(OknoStartowe))
        button.grid(row=0, column=0)
        self.toolbar.grid(row=0, column=0, columnspan=2, sticky=tk.NSEW)

        # umieszczamy nagłówek i pole do wpisania emailu
        email_label = ttk.Label(self, text="Email: ")
        email_label.configure(background=BG)
        email_label.grid(column=0, row=1, padx=10, pady=(50,10), sticky='E')
        email_entry = ttk.Entry(self, width=40)
        email_entry.grid(column=1, row=1, padx=10, pady=(50,10), sticky='W')

        # umieszczamy nagłówek i pole do wpisania loginu
        login_label = ttk.Label(self, text="Login: ")
        login_label.configure(background=BG)
        login_label.grid(column=0, row=2, padx=10, pady=10, sticky='E')
        login_entry = ttk.Entry(self, width=40)
        login_entry.grid(column=1, row=2, padx=10, pady=10, sticky='W')

        # umieszczamy nagłówek i pole do wpisania hasła
        haslo_label = ttk.Label(self, text="Hasło: ")
        haslo_label.configure(background=BG)
        haslo_label.grid(column=0, row=3, padx=10, pady=10, sticky='E')
        haslo_entry = ttk.Entry(self, width=40, show="*")
        haslo_entry.grid(column=1, row=3, padx=10, pady=10, sticky='w')

        # umieszczamy nagłówek i pole do ponownego wpisania hasła
        powtorz_haslo_label = ttk.Label(self, text="Powtórz hasło: ")
        powtorz_haslo_label.configure(background=BG)
        powtorz_haslo_label.grid(column=0, row=4, padx=(60,10), pady=10, sticky='E')
        powtorz_haslo_entry = ttk.Entry(self, width=40, show="*")
        powtorz_haslo_entry.grid(column=1, row=4, padx=10, pady=10, sticky='W')
        
        # umieszczamy przyciski do zaznaczenia akceptacji warunków i zgody na przetwarzanie danych
        akceptacja_warunkow = tk.IntVar()
        warunki_checkbutton = ttk.Checkbutton(self, text='Akceptuję warunki korzystania z aplikacji.', variable=akceptacja_warunkow, 
                                        onvalue=1, offvalue=0)
        warunki_checkbutton.grid(column=1, row=5, padx=10, pady=10, sticky='W')

        przetwarzanie_danych = tk.IntVar()
        dane_checkbutton = ttk.Checkbutton(self, text='Zgadzam się na przetwarzanie moich danych.', variable=przetwarzanie_danych, 
                                        onvalue=1, offvalue=0)
        dane_checkbutton.grid(column=1, row=6, padx=10, pady=10, sticky='W')

        # umieszczamy przycisk tworzenia konta który wywołuje funkcję sprawdz_dane
        zaloz_konto_button = ttk.Button(self, text='Załóż konto', command=sprawdz_dane)
        zaloz_konto_button.grid(column=1, row=7, padx=100, pady=10, sticky='NW')

# okno z lista roślin konkretnego użytkownika    
class OknoGlowne(tk.Canvas):
    def __init__(self, parent, uzytkownik):
        tk.Canvas.__init__(self, parent)

        # ustawiamy uzytkownika okna na uzytkownika podnaego w parametrze
        self.uzytkownik = uzytkownik

        # okno bedzie mialo  2 kolumny
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)

        self.menu = tk.Menu(parent)
        self.fileMenu = tk.Menu(self.menu)
        self.fileMenu.add_command(label="Zapisz", command=parent.zapisz, accelerator="Ctrl+S")
        self.fileMenu.add_command(label="Wyjdź", command=parent.zapisz_i_zamknij, accelerator="Ctrl+Q")
        self.focus_force()
        parent.bind("<Control-s>", parent.zapisz_event)
        parent.bind("<Control-q>", parent.zapisz_i_zamknij_event)
        self.menu.add_cascade(label="Plik", menu=self.fileMenu) 
        parent.config(menu=self.menu)

        self.toolbar = tk.Frame(self)
        self.toolbar_images = []

        # dodajemy do paska narzedzi przycisk plus przekierowujący do okna dodawania nowej rośliny
        image = "images/plus.png"
        image = os.path.join(os.path.dirname(__file__), image)
        image = tk.PhotoImage(file=image)
        self.toolbar_images.append(image)
        button = ttk.Button(self.toolbar, image=image, command=lambda: parent.pokaz_okno(OknoDodawaniaRosliny, self.uzytkownik))
        button.grid(row=0, column=0)

        # dodajemy do paska narzedzi przycisk wyloguj przekierowujący do okna startowego
        image = "images/wyloguj.png"
        image = os.path.join(os.path.dirname(__file__), image)
        image = tk.PhotoImage(file=image)
        self.toolbar_images.append(image)
        button = ttk.Button(self.toolbar, image=image, command=lambda: parent.pokaz_okno(OknoStartowe))
        button.grid(row=0, column=1)

        self.toolbar.grid(row=0, column=0, columnspan=2, sticky=tk.NSEW)

        # umieszczamy nagłówek Twoje rosliny
        naglowek_label = ttk.Label(self, text="Twoje rośliny: ", font=14)
        naglowek_label.configure(background=BG)
        naglowek_label.grid(column=0, row=1, columnspan=2, padx=180, pady=(30,10), sticky='W')

        # w 1 kolumnie umieszczamy nagłówek Rosliny wymagajace opieki
        wymagajace_opieki_label = ttk.Label(self, text="-> Rośliny wymagające opieki: ")
        wymagajace_opieki_label.configure(background=BG)
        wymagajace_opieki_label.grid(column=0, row=2, padx=(20,10), pady=(30,10), sticky='W')

        # w 1 kolumnie umieszczamy przyciski z roslinami wymagającymi opieki (zwraca je funkcja niezadbane_rosliny w Uzytkowniku)
        row = 3
        wymagajace_opieki = self.uzytkownik.niezadbane_rosliny()
        for roslina in wymagajace_opieki:
            button = ttk.Button(self, text=roslina.nazwa, 
                                command=lambda roslina=roslina: parent.pokaz_okno(OknoRosliny, self.uzytkownik, roslina))
            button.grid(column=0, row=row, padx=(70,10), pady=10, sticky='W')
            row += 1

        # w 2 kolumnie umieszczamy nagłówek Rosliny zadbane
        zadbane_label = ttk.Label(self, text="-> Rośliny zadbane: ")
        zadbane_label.configure(background=BG)
        row = 2
        zadbane_label.grid(column=1, row=row, pady=(30,10), sticky='W')
        row += 1
        
        # w 2 kolumnie umieszczamy przyciski z roslinami zadbanymi (zwraca je funkcja zadbane_rosliny w Uzytkowniku)
        zadbane = self.uzytkownik.zadbane_rosliny()
        for roslina in zadbane:
            button = ttk.Button(self, text=roslina.nazwa, 
                                command=lambda roslina=roslina: parent.pokaz_okno(OknoRosliny, self.uzytkownik, roslina))
            button.grid(column=1, row=row, padx=(50,10), pady=10, sticky='W')
            row += 1

# okno do wpisywania danych nowej rosliny użytkownika
class OknoDodawaniaRosliny(tk.Canvas):
    def __init__(self, parent, uzytkownik):
        tk.Canvas.__init__(self, parent)

        # ustawiamy uzytkownika okna na uzytkownika podnaego w parametrze
        self.uzytkownik = uzytkownik

        # tworzymy pasek menu
        self.menu = tk.Menu(parent)
        self.menu.add_command(label="Wyjdź", command=parent.zapisz_i_zamknij, accelerator="Ctrl+Q")
        parent.bind("<Control-q>", parent.zapisz_i_zamknij_event)
        parent.config(menu=self.menu)

        # tworzymy linię statusu
        self.statusbar = tk.Label(self, text="Oczekiwanie...", anchor=tk.W)
        self.statusbar.grid(row=11, column=0, columnspan=2, sticky=tk.EW)

        # funkcja zamienia datę ze stringa na datetime.date i zwraca ją
        # jeśli data jest zła albo z przyszłości to wyświetla informację o błędzie
        def wyciagnijDate(dataStr):
            data = dataStr.split('.')
            if len(data) != 3:
                raise ValueError("Zły format daty.")
            else:
                data = datetime.date(int(data[2]), int(data[1]), int(data[0]))
                if data > datetime.date.today():
                    raise ValueError("Data nie może być z przyszłości.")
                else:
                    return data

        # funkcja sprawdza czy wybrany typ to Roslina doniczkowa czy Roslina ogrodowa
        # dla Rosliny doniczkowej prosi o informacje dotyczące przesadzania
        # dla Rosliny ogrodowej prosi o informacje dotyczące opryskiwania
        # funkcja sprawdza też poprawnośc wprowadzonych danych i w przypadku błędów wyświetla komunikat
        def sprawdz_typ_rosliny(typ):
            try:
                nazwa = nazwa_entry.get()
                czestotliwoscPodlewania = int(czestotliwosc_podlewania_entry.get())
                ostatniePodlewanie = ostatnie_podlewanie_entry.get()
                zdjecie = zdjecie_entry.get()
                try:
                    data = wyciagnijDate(ostatniePodlewanie)
                    ostatniePodlewanie = data
                    czestotliwoscNawozenia = int(czestotliwosc_nawozenia_entry.get())
                    ostatnieNawozenie = ostatnie_nawozenie_entry.get()
                    try:
                        data = wyciagnijDate(ostatnieNawozenie)
                        ostatnieNawozenie = data
                        if os.path.isfile(zdjecie) and filetype.is_image(zdjecie):
                        
                            if typ == "Roślina doniczkowa":
                                
                                # funkcja sprawdza poprawnośc wprowadzonych danych i w przypadku błędów wyświetla komunikat
                                def sprawdz_dane_rosliny_doniczkowej():
                                    srednicaDoniczki = int(srednica_doniczki_entry.get())
                                    ostatniePrzesadzanie = ostatnie_przesadzanie_entry.get()
                                    try:
                                        data = wyciagnijDate(ostatniePrzesadzanie)
                                        ostatniePrzesadzanie = data
                                        try:
                                            roslina = RoslinaDoniczkowa(nazwa, czestotliwoscPodlewania, ostatniePodlewanie, czestotliwoscNawozenia, 
                                                                            ostatnieNawozenie, srednicaDoniczki, ostatniePrzesadzanie, zdjecie)
                                            self.uzytkownik.listaRoslin.append(roslina)
                                            messagebox.showinfo("Informacja", "Roślina dodana poprawnie.")
                                            parent.pokaz_okno(OknoGlowne, self.uzytkownik)
                                        except TypeError as error:
                                            messagebox.showerror("Błąd", "{0}".format(error))

                                    except ValueError as error:
                                        messagebox.showerror("Błąd", "{0}".format(error))
                                
                                # umieszczamy nagłówek i pole do wpisywania średnicy doniczki
                                srednica_doniczki_label = ttk.Label(self, text="Średnica doniczki w cm: ")
                                srednica_doniczki_label.configure(background=BG)
                                srednica_doniczki_label.grid(column=0, row=8, padx=10, pady=10, sticky='E')
                                srednica_doniczki_entry = ttk.Entry(self, width=40)
                                srednica_doniczki_entry.grid(column=1, row=8, padx=10, pady=10, sticky='W')

                                # umieszczamy nagłówek i pole do wpisywania daty ostatniego przesadzania
                                ostatnie_przesadzanie_label = ttk.Label(self, text="Ostatnie przesadzanie <dd.mm.yyyy>: ")
                                ostatnie_przesadzanie_label.configure(background=BG)
                                ostatnie_przesadzanie_label.grid(column=0, row=9, padx=10, pady=10, sticky='E')
                                ostatnie_przesadzanie_entry = ttk.Entry(self, width=40)
                                ostatnie_przesadzanie_entry.grid(column=1, row=9, padx=10, pady=10, sticky='W')

                                # umieszczamy przycisk Dodaj rosline wywolujacy funkcje sprawdz_dane_rosliny_doniczkowej
                                dodaj_rosline_button = ttk.Button(self, text='Dodaj rośline', command=sprawdz_dane_rosliny_doniczkowej)
                                dodaj_rosline_button.grid(column=1, row=10, padx=(100, 10), pady=10, sticky='NW')
                            
                            elif typ == "Roślina ogrodowa":
                                
                                # funkcja sprawdza poprawnośc wprowadzonych danych i w przypadku błędów wyświetla komunikat
                                def sprawdz_dane_rosliny_ogrodowej():
                                    czestotliwoscOpryskiwania = int(czestotliwosc_opryskiwania_entry.get())
                                    ostatnieOpryskiwanie = ostatnie_opryskiwanie_entry.get()
                                    try:
                                        data = wyciagnijDate(ostatnieOpryskiwanie)
                                        ostatnieOpryskiwanie = data
                                        try:
                                            roslina = RoslinaOgrodowa(nazwa, czestotliwoscPodlewania, ostatniePodlewanie, czestotliwoscNawozenia, 
                                                                        ostatnieNawozenie, czestotliwoscOpryskiwania, ostatnieOpryskiwanie, zdjecie)
                                            self.uzytkownik.listaRoslin.append(roslina)
                                            messagebox.showinfo("Informacja", "Roślina dodana poprawnie.")
                                            parent.pokaz_okno(OknoGlowne, self.uzytkownik)
                                        except TypeError as error:
                                            messagebox.showerror("Błąd", "{0}".format(error))
                                    except ValueError as error:
                                        messagebox.showerror("Błąd", "{0}".format(error))
                            
                                # umieszczamy nagłówek i pole do wpisywania czestotliwosci opryskiwania
                                czestotliwosc_opryskiwania_label = ttk.Label(self, text="Czestotliwość opryskiwania w miesiącach: ")
                                czestotliwosc_opryskiwania_label.configure(background=BG)
                                czestotliwosc_opryskiwania_label.grid(column=0, row=8, padx=10, pady=10, sticky='E')
                                czestotliwosc_opryskiwania_entry = ttk.Entry(self, width=40)
                                czestotliwosc_opryskiwania_entry.grid(column=1, row=8, padx=10, pady=10, sticky='W')

                                # umieszczamy nagłówek i pole do wpisywania daty ostatniego opryskiwania
                                ostatnie_opryskiwanie_label = ttk.Label(self, text="Ostatnie opryskiwanie <dd.mm.yyyy>: ")
                                ostatnie_opryskiwanie_label.configure(background=BG)
                                ostatnie_opryskiwanie_label.grid(column=0, row=9, padx=10, pady=10, sticky='E')
                                ostatnie_opryskiwanie_entry = ttk.Entry(self, width=40)
                                ostatnie_opryskiwanie_entry.grid(column=1, row=9, padx=10, pady=10, sticky='W')

                                # umieszczamy przycisk Dodaj rosline wywolujacy funkcje sprawdz_dane_rosliny_ogrodowej
                                dodaj_rosline_button = ttk.Button(self, text='Dodaj roślinę', command=sprawdz_dane_rosliny_ogrodowej)
                                dodaj_rosline_button.grid(column=1, row=10, padx=(100, 10), pady=10, sticky='NW')
                            
                        else:
                            messagebox.showerror("Błąd", "Podano błędną ścieżkę.")

                    except ValueError as error:
                        messagebox.showerror("Błąd", "{0}".format(error))
                
                except ValueError as error:
                    messagebox.showerror("Błąd", "{0}".format(error))
            
            except ValueError as error:
                messagebox.showerror("Błąd", "{0}".format(error))
            except TypeError as error:
                messagebox.showerror("Błąd", "{0}".format(error))

        # okno bedzie mialo 2 kolumny i 12 wierszy
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(6, weight=1)
        self.rowconfigure(7, weight=1)
        self.rowconfigure(8, weight=1)
        self.rowconfigure(9, weight=1)
        self.rowconfigure(10, weight=100)
        self.rowconfigure(11, weight=1)

        # tworzymy pasek narzedzi i dodajemy do niego przycisk powrotu do poprzedniego okna (OknoGlowne uzytkownika)
        self.toolbar = tk.Frame(self)
        self.toolbar_images = []
        image = "images/powrot.png"
        image = os.path.join(os.path.dirname(__file__), image)
        image = tk.PhotoImage(file=image)
        self.toolbar_images.append(image)
        button = ttk.Button(self.toolbar, image=image, command=lambda: parent.pokaz_okno(OknoGlowne,self.uzytkownik))
        button.grid(row=0, column=0)
        self.toolbar.grid(row=0, column=0, columnspan=2, sticky=tk.NSEW)

        # umieszczamy nagłówek i pole do wpisywania nazwy rośliny
        nazwa_label = ttk.Label(self, text="Nazwa rośliny: ")
        nazwa_label.configure(background=BG)
        nazwa_label.grid(column=0, row=1, padx=10, pady=10, sticky='E')
        nazwa_entry = ttk.Entry(self, width=40)
        nazwa_entry.grid(column=1, row=1, padx=10, pady=10, sticky='W')

        # umieszczamy nagłówek i pole do wpisywania ścieżki do zdjęcia rośliny
        zdjecie_label = ttk.Label(self, text="Ścieżka do zdjęcia (opcjonalne): ")
        zdjecie_label.configure(background=BG)
        zdjecie_label.grid(column=0, row=2, padx=10, pady=10, sticky='E')
        zdjecie_entry = ttk.Entry(self, width=40)
        zdjecie_entry.grid(column=1, row=2, padx=10, pady=10, sticky='W')

        # umieszczamy nagłówek i pole do wpisywania czestotliwosci podlewania
        czestotliwosc_podlewania_label = ttk.Label(self, text="Czestotliwość podlewania w dniach: ")
        czestotliwosc_podlewania_label.configure(background=BG)
        czestotliwosc_podlewania_label.grid(column=0, row=3, padx=10, pady=10, sticky='E')
        czestotliwosc_podlewania_entry = ttk.Entry(self, width=40)
        czestotliwosc_podlewania_entry.grid(column=1, row=3, padx=10, pady=10, sticky='W')

        # umieszczamy nagłówek i pole do wpisywania daty ostatniego podlewania
        ostatnie_podlewanie_label = ttk.Label(self, text="Ostatnie podlewanie <dd.mm.yyyy>: ")
        ostatnie_podlewanie_label.configure(background=BG)
        ostatnie_podlewanie_label.grid(column=0, row=4, padx=10, pady=10, sticky='E')
        ostatnie_podlewanie_entry = ttk.Entry(self, width=40)
        ostatnie_podlewanie_entry.grid(column=1, row=4, padx=10, pady=10, sticky='W')

        # umieszczamy nagłówek i pole do wpisywania czestotliwosci nawożenia
        czestotliwosc_nawozenia_label = ttk.Label(self, text="Czestotliwość nawożenia w miesiącach: ")
        czestotliwosc_nawozenia_label.configure(background=BG)
        czestotliwosc_nawozenia_label.grid(column=0, row=5, padx=10, pady=10, sticky='E')
        czestotliwosc_nawozenia_entry = ttk.Entry(self, width=40)
        czestotliwosc_nawozenia_entry.grid(column=1, row=5, padx=10, pady=10, sticky='W')

        # umieszczamy nagłówek i pole do wpisywania daty ostatniego nawożenia
        ostatnie_nawozenie_label = ttk.Label(self, text="Ostatnie nawożenie <dd.mm.yyyy>: ")
        ostatnie_nawozenie_label.configure(background=BG)
        ostatnie_nawozenie_label.grid(column=0, row=6, padx=10, pady=10, sticky='E')
        ostatnie_nawozenie_entry = ttk.Entry(self, width=40)
        ostatnie_nawozenie_entry.grid(column=1, row=6, padx=10, pady=10, sticky='W')

        # umieszczamy nagłówek i listę wyboru typu rośliny
        # po wybraniu typu wywolywana jest funkcja sprawdz_typ_rosliny wyswietlajaca kolejne pola
        typ_label = ttk.Label(self, text="Typ rośliny: ")
        typ_label.configure(background=BG)
        typ_label.grid(column=0, row=7, padx=10, pady=10, sticky='E')
        typy = ["Wybierz typ", "Roślina doniczkowa", "Roślina ogrodowa"]
        wybrany_typ = tk.StringVar()
        menu_opcji = ttk.OptionMenu(self, wybrany_typ , *typy, command=sprawdz_typ_rosliny)
        menu_opcji.config(width=36)
        menu_opcji.grid(column=1, row=7, padx=10, pady=10, sticky='W')

# okno z informacjami o stanie konkretnej rosliny użytkownika i możliwością podlania, nawiezienia i przesadzenia/opryskania
class OknoRosliny(tk.Canvas):
    def __init__(self, parent, uzytkownik, roslina):
        tk.Canvas.__init__(self, parent)
        
        # ustawiamy uzytkownika i rosline okna na uzytkownika i rosline podane w parametrze
        self.uzytkownik = uzytkownik
        self.roslina = roslina

        # okno bedzie miało 4 kolumny
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=3)
        self.columnconfigure(2, weight=2)
        self.columnconfigure(3, weight=3)

        # funkcja wyswietlajaca informacje o oknie rośliny - tłumaczy kiedy należy aktualizować dane
        def pokaz_info():
            informacja = "-> Podlej, nawieź lub przesadź/opryskaj roślinę w aplikacji tego samego dnia, gdy to zrobił*ś.\n-> Jeśli roślina jest ogrodowa, podlej ją w aplikacji, gdy spadł deszcz.\n-> Przesadzanie powinno się wykonywać co roku.\n-> Zalecane jest przesadzanie do doniczki o rozmiar większej."
            messagebox.showinfo("Info", informacja)

        # tworzymy pasek menu
        self.menu = tk.Menu(parent)
        self.menu.add_cascade(label="Pomoc", command=pokaz_info) 
        parent.config(menu=self.menu)
        
        # tworzymy pasek narzedzi
        self.toolbar = tk.Frame(self)
        self.toolbar_images = []
        
        # dodajemy do paska narzedzi przycisk powrotu przekierowujacy do poprzedniego okna (OknoGlowne uzytkownika)
        image = "images/powrot.png"
        image = os.path.join(os.path.dirname(__file__), image)
        image = tk.PhotoImage(file=image)
        self.toolbar_images.append(image)
        button = ttk.Button(self.toolbar, image=image, command=lambda: parent.pokaz_okno(OknoGlowne,self.uzytkownik))
        button.grid(row=0, column=0)

        # funkcja kontrolna - upewniamy się czy osoba na pewno chciała usunąć roślinę
        # jesli tak to usuwamy rosline z listy roslin danego uzytkownika i wracamy do okna głównego
        def usun_rosline():
            czy_na_pewno = messagebox.askyesno("Potwierdź operację", "Czy na pewno chcesz usunąć roślinę?")
            if czy_na_pewno:
                self.uzytkownik.listaRoslin.pop(self.uzytkownik.listaRoslin.index(self.roslina))
                parent.pokaz_okno(OknoGlowne,self.uzytkownik)
           
        # dodajemy do paska narzedzi przycisk kosza wywolujacy funkcję usun_rosline
        image = "images/kosz.png"
        image = os.path.join(os.path.dirname(__file__), image)
        image = tk.PhotoImage(file=image)
        self.toolbar_images.append(image)
        button = ttk.Button(self.toolbar, image=image, command=usun_rosline)
        button.grid(row=0, column=1)

        self.toolbar.grid(row=0, column=0, columnspan=4, sticky=tk.NSEW)

        # umieszczamy nagłówek z nazwą rośliny
        nazwa_label = ttk.Label(self, text=self.roslina.nazwa, font=14)
        nazwa_label.configure(background=BG)
        nazwa_label.grid(column=0, row=1, columnspan=3, padx=10, pady=10)

        # funkcja aktualizująca datę ostatniego podlania rośliny  (po zaktualizowaniu odświeża okno)
        def podlej():
            self.roslina.ostatniePodlewanie = datetime.date.today()
            parent.pokaz_okno(OknoRosliny, self.uzytkownik, self.roslina)

        # funkcja aktualizująca datę ostatniego nawozenia rośliny  (po zaktualizowaniu odświeża okno)
        def nawiez():
            self.roslina.ostatnieNawozenie = datetime.date.today()
            parent.pokaz_okno(OknoRosliny, self.uzytkownik, self.roslina)

        # funkcja aktualizująca datę ostatniego przesadzania rośliny  (po zaktualizowaniu odświeża okno)
        def przesadz():
            def przesadz_ok():
                self.roslina.srednicaDoniczki = int(doniczka_entry.get())
                self.roslina.ostatniePrzesadzanie = datetime.date.today()
                parent.pokaz_okno(OknoRosliny, self.uzytkownik, self.roslina)

            # umieszczamy nagłówek i pole do wprowadzenia nowej średnicy doniczki
            doniczka_label = ttk.Label(self, text='Nowa średnica doniczki:')
            doniczka_label.configure(background=BG)
            doniczka_label.grid(column=1, row=11, padx=10, pady=10, sticky='E')
            doniczka_entry = ttk.Entry(self, width=10)
            doniczka_entry.grid(column=2, row=11, padx=10, pady=10)

            # umieszczamy przycisk OK wywołujący funkcję przesadź_ok
            doniczka_button = ttk.Button(self, text='OK', command=przesadz_ok)
            doniczka_button.grid(column=3, row=11, padx=10, pady=10)

        # funkcja aktualizująca datę ostatniego opryskiwania rośliny  (po zaktualizowaniu odświeża okno)
        def opryskaj():
            self.roslina.ostatnieOpryskiwanie = datetime.date.today()
            parent.pokaz_okno(OknoRosliny, self.uzytkownik, self.roslina)

        # definiujemy paski oznaczające stopień podlania/nawiezienia/przesadzenia/opyskania rosliny
        self.paski_images = [tk.PhotoImage(file=os.path.join(os.path.dirname(__file__), 'images/pasek_czerwony.png')),
                            tk.PhotoImage(file=os.path.join(os.path.dirname(__file__), 'images/pasek_zolty.png')),
                            tk.PhotoImage(file=os.path.join(os.path.dirname(__file__), 'images/pasek_jasnozielony.png')),
                            tk.PhotoImage(file=os.path.join(os.path.dirname(__file__), 'images/pasek_zielony.png'))]

        # umieszczamy nagłówek
        podlewanie_label = ttk.Label(self, text='Podlewanie')
        podlewanie_label.configure(background=BG)
        podlewanie_label.grid(column=0, row=2, padx=10, pady=10, sticky='E')

        # umieszczamy odpowiedni pasek w zaleznosci od stopnia podlania rosliny
        if self.roslina.czy_wymaga_podlania() == 1:
            pasek_label = ttk.Label(self, image=self.paski_images[0])
            pasek_label.configure(background=BG)
            pasek_label.grid(column=1, row=2, padx=10, pady=10, sticky='W')
        elif self.roslina.czy_wymaga_podlania() >= 0.6:
            pasek_label = ttk.Label(self, image=self.paski_images[1])
            pasek_label.configure(background=BG)
            pasek_label.grid(column=1, row=2, padx=10, pady=10, sticky='W')
        elif self.roslina.czy_wymaga_podlania() >= 0.3:
            pasek_label = ttk.Label(self, image=self.paski_images[2])
            pasek_label.configure(background=BG)
            pasek_label.grid(column=1, row=2, padx=10, pady=10, sticky='W')
        else:
            pasek_label = ttk.Label(self, image=self.paski_images[3])
            pasek_label.configure(background=BG)
            pasek_label.grid(column=1, row=2, padx=10, pady=10, sticky='W')

        # umieszczamy przycisk wywołujący funkcję podlej     
        podlewanie_button = ttk.Button(self, text='Podlej', command=podlej)
        podlewanie_button.grid(column=2, row=2, pady=10, sticky='W')

        # umieszczamy informacje o aktualnych danych dotyczących podlewania
        ostatnie_podlewanie_label = podlewanie_label = ttk.Label(self, text='Ostatnie podlewanie: '+ str(self.roslina.ostatniePodlewanie))
        ostatnie_podlewanie_label.configure(background=BG)
        ostatnie_podlewanie_label.grid(column=1, row=3, padx=(30,10), sticky='W')
        czestotliwosc_podlewania_label = podlewanie_label = ttk.Label(self, text='Czestotliwość podlewania: '+ str(self.roslina.czestotliwoscPodlewania) + ' dni')
        czestotliwosc_podlewania_label.configure(background=BG)
        czestotliwosc_podlewania_label.grid(column=1, row=4, padx=(30,10), pady=(0,10), sticky='W')

        # umieszczamy nagłówek
        nazwozenie_label = ttk.Label(self, text='Nawożenie')
        nazwozenie_label.configure(background=BG)
        nazwozenie_label.grid(column=0, row=5, padx=10, pady=10, sticky='E')
        
        # umieszczamy odpowiedni pasek w zaleznosci od stopnia nawiezienia rosliny
        if self.roslina.czy_wymaga_nawozenia() == 1:
            pasek_label = ttk.Label(self, image=self.paski_images[0])
            pasek_label.configure(background=BG)
            pasek_label.grid(column=1, row=5, padx=10, pady=10, sticky='W')
        elif self.roslina.czy_wymaga_nawozenia() >= 0.6:
            pasek_label = ttk.Label(self, image=self.paski_images[1])
            pasek_label.configure(background=BG)
            pasek_label.grid(column=1, row=5, padx=10, pady=10, sticky='W')
        elif self.roslina.czy_wymaga_nawozenia() >= 0.3:
            pasek_label = ttk.Label(self, image=self.paski_images[2])
            pasek_label.configure(background=BG)
            pasek_label.grid(column=1, row=5, padx=10, pady=10, sticky='W')
        else:
            pasek_label = ttk.Label(self, image=self.paski_images[3])
            pasek_label.configure(background=BG)
            pasek_label.grid(column=1, row=5, padx=10, pady=10, sticky='W')
            
        # umieszczamy przycisk wywołujący funkcję nawiez
        nazwozenie_button = ttk.Button(self, text='Nawieź', command=nawiez)
        nazwozenie_button.grid(column=2, row=5, pady=10, sticky='W')

        # umieszczamy informacje o aktualnych danych dotyczących nawozenia
        ostatnie_nawozenie_label = podlewanie_label = ttk.Label(self, text='Ostatnie nawożenie: '+ str(self.roslina.ostatnieNawozenie))
        ostatnie_nawozenie_label.configure(background=BG)
        ostatnie_nawozenie_label.grid(column=1, row=6, padx=(30,10), sticky='W')
        czestotliwosc_nawozenia_label = podlewanie_label = ttk.Label(self, text='Czestotliwość nawożenia: '+ str(self.roslina.czestotliwoscNawozenia) + ' miesiecy')
        czestotliwosc_nawozenia_label.configure(background=BG)
        czestotliwosc_nawozenia_label.grid(column=1, row=7, padx=(30,10), pady=(0,10), sticky='W')

        # jesli roslina jest doniczkowa to analogicznie wyświetlamy dane dotyczące przesadzania
        if isinstance(self.roslina, RoslinaDoniczkowa):
            przesadzanie_label = ttk.Label(self, text='Przesadzanie')
            przesadzanie_label.configure(background=BG)
            przesadzanie_label.grid(column=0, row=8, padx=10, pady=10, sticky='E')
            if self.roslina.czy_wymaga_przesadzenia() == 1:
                pasek_label = ttk.Label(self, image=self.paski_images[0])
                pasek_label.configure(background=BG)
                pasek_label.grid(column=1, row=8, padx=10, pady=10, sticky='W')
            elif self.roslina.czy_wymaga_przesadzenia() >= 0.6:
                pasek_label = ttk.Label(self, image=self.paski_images[1])
                pasek_label.configure(background=BG)
                pasek_label.grid(column=1, row=8, padx=10, pady=10, sticky='W')
            elif self.roslina.czy_wymaga_przesadzenia() >= 0.3:
                pasek_label = ttk.Label(self, image=self.paski_images[2])
                pasek_label.configure(background=BG)
                pasek_label.grid(column=1, row=8, padx=10, pady=10, sticky='W')
            else:
                pasek_label = ttk.Label(self, image=self.paski_images[3])
                pasek_label.configure(background=BG)
                pasek_label.grid(column=1, row=8, padx=10, pady=10, sticky='W')
                
            przesadzanie_button = ttk.Button(self, text='Przesadź', command=przesadz)
            przesadzanie_button.grid(column=2, row=8, pady=10, sticky='W')

            ostatnie_przesadzanie_label = podlewanie_label = ttk.Label(self, text='Ostatnie przesadzanie: '+ str(self.roslina.ostatniePrzesadzanie))
            ostatnie_przesadzanie_label.configure(background=BG)
            ostatnie_przesadzanie_label.grid(column=1, row=9, padx=(30,10), sticky='W')
            srednica_doniczki_label = podlewanie_label = ttk.Label(self, text='Średnica doniczki: '+ str(self.roslina.srednicaDoniczki) + ' cm')
            srednica_doniczki_label.configure(background=BG)
            srednica_doniczki_label.grid(column=1, row=10, padx=(30,10), pady=(0,10), sticky='W')
        
        # jesli roslina jest ogrodowa to analogicznie wyświetlamy dane dotyczące opryskiwania
        else:
            opryskiwanie_label = ttk.Label(self, text='Opryskiwanie')
            opryskiwanie_label.configure(background=BG)
            opryskiwanie_label.grid(column=0, row=8, padx=10, pady=10, sticky='E')
            if self.roslina.czy_wymaga_opryskania() == 1:
                pasek_label = ttk.Label(self, image=self.paski_images[0])
                pasek_label.configure(background=BG)
                pasek_label.grid(column=1, row=8, padx=10, pady=10, sticky='W')
            elif self.roslina.czy_wymaga_opryskania() >= 0.6:
                pasek_label = ttk.Label(self, image=self.paski_images[1])
                pasek_label.configure(background=BG)
                pasek_label.grid(column=1, row=8, padx=10, pady=10, sticky='W')
            elif self.roslina.czy_wymaga_opryskania() >= 0.3:
                pasek_label = ttk.Label(self, image=self.paski_images[2])
                pasek_label.configure(background=BG)
                pasek_label.grid(column=1, row=8, padx=10, pady=10, sticky='W')
            else:
                pasek_label = ttk.Label(self, image=self.paski_images[3])
                pasek_label.configure(background=BG)
                pasek_label.grid(column=1, row=8, padx=10, pady=10, sticky='W')
                
            opryskiwanie_button = ttk.Button(self, text='Opryskaj', command=opryskaj)
            opryskiwanie_button.grid(column=2, row=8, pady=10, sticky='W')

            ostatnie_opryskiwanie_label = podlewanie_label = ttk.Label(self, text='Ostatnie opryskiwanie: '+ str(self.roslina.ostatnieOpryskiwanie))
            ostatnie_opryskiwanie_label.configure(background=BG)
            ostatnie_opryskiwanie_label.grid(column=1, row=9, padx=(30,10), sticky='W')
            czestotliwosc_opryskiwania_label = podlewanie_label = ttk.Label(self, text='Czestotliwość opryskiwania: '+ str(self.roslina.czestotliwoscOpryskiwania) + ' miesiecy')
            czestotliwosc_opryskiwania_label.configure(background=BG)
            czestotliwosc_opryskiwania_label.grid(column=1, row=10, padx=(30,10), pady=(0,10), sticky='W')

        if self.roslina.zdjecie != None:
            zdjecie_button = ttk.Button(self, text='Pokaż zdjęcie', command=lambda: parent.pokaz_okno_zdjecie(OknoZdjeciaRosliny, zdjecie=self.roslina.zdjecie, uzytkownik=self.uzytkownik, roslina=self.roslina))
            zdjecie_button.grid(row=11, columnspan=2, pady=10)

class OknoZdjeciaRosliny(tk.Canvas):
    def __init__(self, parent, uzytkownik, roslina):
        tk.Canvas.__init__(self, parent)
        
        # ustawiamy uzytkownika i rosline okna na uzytkownika i rosline podane w parametrze
        self.uzytkownik = uzytkownik
        self.roslina = roslina

        # tworzymy pasek menu
        self.menu = tk.Menu(parent)
        self.menu.add_command(label="Wyjdź", command=parent.zapisz_i_zamknij, accelerator="Ctrl+Q")
        parent.bind("<Control-q>", parent.zapisz_i_zamknij_event)
        parent.config(menu=self.menu)
        
        # tworzymy pasek narzedzi
        self.toolbar = tk.Frame(self)
        self.toolbar_images = []
        self.toolbar.grid(row=0, column=0, sticky=tk.NSEW)
        
        # dodajemy do paska narzedzi przycisk powrotu przekierowujacy do poprzedniego okna (OknoGlowne uzytkownika)
        image = "images/powrot.png"
        image = os.path.join(os.path.dirname(__file__), image)
        image = tk.PhotoImage(file=image)
        self.toolbar_images.append(image)
        button = ttk.Button(self.toolbar, image=image, command=lambda: parent.pokaz_okno(OknoRosliny,self.uzytkownik, self.roslina))
        button.grid(row=0, column=0)

if __name__ == '__main__':
    app = TkinterPlantsApp()
    app.mainloop()
