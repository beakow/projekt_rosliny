import datetime

class Roslina:

    # obiekty typu Roslina maja atrybuty: 
    # nazwa, czestotliwoscPodlewania, ostatniePodlewanie, czestotliwoscNawozenia, ostatnieNawozenie, zdjecie
    def __init__(self, nazwa, czestotliwoscPodlewania, ostatniePodlewanie, czestotliwoscNawozenia, ostatnieNawozenie, zdjecie):
        if isinstance(nazwa, str):
            self.nazwa = nazwa
        else:
            raise TypeError('Nazwa musi byc typu string.')
        
        if isinstance(czestotliwoscPodlewania, int):
            self.czestotliwoscPodlewania = czestotliwoscPodlewania
        else:
            raise TypeError('Czestotliwosc podlewania musi byc typu int.')
        
        if isinstance(ostatniePodlewanie, datetime.date):
            self.ostatniePodlewanie = ostatniePodlewanie
        else:
            raise TypeError('Ostatnie podlewanie musi byc typu date.')

        if isinstance(czestotliwoscNawozenia, int):
            self.czestotliwoscNawozenia = czestotliwoscNawozenia
        else:
            raise TypeError('Czestotliwosc nawozenia musi byc typu int.')

        if isinstance(ostatnieNawozenie, datetime.date):
            self.ostatnieNawozenie = ostatnieNawozenie
        else:
            raise TypeError('Ostatnie nawozenie musi byc typu date.')

        if zdjecie != "":
            self.zdjecie = zdjecie
        else:
            self.zdjecie = None
        

    # funkcja zwraca True jeśli roślina jest zadbana (nie wymaga podlewania ani nawożenia), False jeśli nie 
    def czy_zadbana(self):
        if self.czy_wymaga_podlania() == 1 or self.czy_wymaga_nawozenia() == 1:
            return False
        else:
            return True

    # funkcja zwraca stosunek liczby dni od ostatniego podlania do czestotliwosci podlewania
    # jeśli liczba dni jest większa/równa niż częstotliwość (rosline trzeba podlac) to zwraca 1
    def czy_wymaga_podlania(self):
        ile_dni_minelo_od_podlania = (datetime.date.today() - self.ostatniePodlewanie).days

        if ile_dni_minelo_od_podlania >= self.czestotliwoscPodlewania:
            return 1
        else:
            return ile_dni_minelo_od_podlania / self.czestotliwoscPodlewania

    # funkcja zwraca stosunek liczby miesięcy od ostatniego nawożenia do czestotliwosci nawożenia
    # jeśli liczba miesięcy jest większa/równa niż częstotliwość (rosline trzeba nawiźć) to zwraca 1
    def czy_wymaga_nawozenia(self):
        ile_miesiecy_minelo_od_nawozenia = (datetime.date.today() - self.ostatnieNawozenie).days/30

        if ile_miesiecy_minelo_od_nawozenia >= self.czestotliwoscNawozenia:
            return 1
        else:
            return ile_miesiecy_minelo_od_nawozenia / self.czestotliwoscNawozenia

    # funkcja aktualizuje informacje o roślinie bazując na roślinie podanej w parametrze
    def aktualizuj(self, roslina):
        self.czestotliwoscPodlewania = roslina.czestotliwoscPodlewania
        self.ostatniePodlewanie = roslina.ostatniePodlewanie
        self.czestotliwoscNawozenia = roslina.czestotliwoscNawozenia
        self.ostatnieNawozenie = roslina.ostatnieNawozenie
