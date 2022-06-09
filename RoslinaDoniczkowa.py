import datetime
from Roslina import Roslina

# klasa dziedziczy po Roslinie
class RoslinaDoniczkowa(Roslina):
    
    # obiekty typu RoslinaDoniczkowa oprócz atrybutów Rosliny maja dodatkowo atrybuty: 
    # srednicaDoniczki, ostatniePrzesadzanie
    def __init__(self, nazwa, czestotliwoscPodlewania, ostatniePodlewanie, czestotliwoscNawozenia, ostatnieNawozenie, srednicaDoniczki, ostatniePrzesadzanie, zdjecie):
        super().__init__(nazwa, czestotliwoscPodlewania, ostatniePodlewanie, czestotliwoscNawozenia, ostatnieNawozenie, zdjecie)
        
        if isinstance(srednicaDoniczki, int):
            self.srednicaDoniczki = srednicaDoniczki
        else:
            raise TypeError('Srednica doniczki musi byc typu int.')

        if isinstance(ostatniePrzesadzanie, datetime.date):
            self.ostatniePrzesadzanie = ostatniePrzesadzanie
        else:
            raise TypeError('Ostatnie przesadzanie musi byc typu date.')

    # funkcja zwraca True jeśli roślina jest zadbana (nie wymaga podlewania, nawożenia ani przesadzania), False jeśli nie 
    def czy_zadbana(self):
        if self.czy_wymaga_przesadzenia() != 1:
            return super().czy_zadbana()
        else:
            return False

    # funkcja zwraca stosunek liczby dni od ostatniego przesadzania do czestotliwosci przesadzania
    # jeśli liczba dni jest większa/równa niż 365 (minal rok - rosline trzeba przesadzić) to zwraca 1
    def czy_wymaga_przesadzenia(self):
        dni_od_przesadzania = (datetime.date.today() - self.ostatniePrzesadzanie).days
        if dni_od_przesadzania >= 365:
            return 1
        else:
            return dni_od_przesadzania / 365

    # funkcja aktualizuje informacje o roślinie bazując na roślinie podanej w parametrze
    def aktualizuj(self, roslina):
        super().aktualizuj(roslina)
        self.srednicaDoniczki = roslina.srednicaDoniczki
        self.ostatniePrzesadzanie = roslina.ostatniePrzesadzanie
