import datetime
from Roslina import Roslina

# klasa dziedziczy po Roslinie
class RoslinaOgrodowa(Roslina):

    # obiekty typu RoslinaDoniczkowa oprócz atrybutów Rosliny maja dodatkowo atrybuty: 
    # czestotliwoscOpryskiwania, ostatnieOpryskiwanie
    def __init__(self, nazwa, czestotliwoscPodlewania, ostatniePodlewanie, czestotliwoscNawozenia, ostatnieNawozenie, czestotliwoscOpryskiwania, ostatnieOpryskiwanie, zdjecie):
        super().__init__(nazwa, czestotliwoscPodlewania, ostatniePodlewanie, czestotliwoscNawozenia, ostatnieNawozenie, zdjecie)
        
        if isinstance(czestotliwoscOpryskiwania, int):
            self.czestotliwoscOpryskiwania = czestotliwoscOpryskiwania
        else:
            raise TypeError('Czestotliwosc opryskiwania musi byc typu int.')

        if isinstance(ostatnieOpryskiwanie, datetime.date):
            self.ostatnieOpryskiwanie = ostatnieOpryskiwanie
        else:
            raise TypeError('Ostatnie opryskiwanie musi byc typu date.')
        
    # funkcja zwraca True jeśli roślina jest zadbana (nie wymaga podlewania, nawożenia ani przesadzania), False jeśli nie 
    def czy_zadbana(self):
        if self.czy_wymaga_opryskania() != 1:
            return super().czy_zadbana()
        else:
            return False

    # funkcja zwraca stosunek liczby miesięcy od ostatniego opryskiwania do czestotliwosci opryskiwania
    # jeśli liczba miesięcy jest większa/równa niż częstotliwość (rosline trzeba opryskać) to zwraca 1
    def czy_wymaga_opryskania(self):
        ile_miesiecy_minelo_od_nawozenia = (datetime.date.today() - self.ostatnieOpryskiwanie).days/30

        if ile_miesiecy_minelo_od_nawozenia >= self.czestotliwoscOpryskiwania:
            return 1
        else:
            return ile_miesiecy_minelo_od_nawozenia / self.czestotliwoscOpryskiwania

    # funkcja aktualizuje informacje o roślinie bazując na roślinie podanej w parametrze
    def aktualizuj(self, roslina):
        super().aktualizuj(roslina)
        self.czestotliwoscOpryskiwania = roslina.czestotliwoscOpryskiwania
        self.ostatnieOpryskiwanie = roslina.ostatnieOpryskiwanie