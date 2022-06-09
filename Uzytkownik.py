class Uzytkownik:

    # obiekty typu Uzytkownik maja atrybuty: 
    # email, login, haslo, listaRoslin
    def __init__(self, email, login, haslo):
        self.email = email
        self.login = login
        self.haslo = haslo
        self.listaRoslin = []

    @property
    def email(self):
        return self._email
    @email.setter
    def email(self, value):
        # email musi składać się z nazwy i domeny połączonych symbolem @
        if isinstance(value, str):
            email_splitted = value.split("@")
            if len(email_splitted) == 2:
                domain = email_splitted[1].split(".")
                if len(domain) >= 2:
                    self._email = value
                else:
                    raise ValueError('Niepoprawny email.')
            else:
                raise ValueError('Niepoprawny email.')
            
        else:
            raise TypeError('Email musi byc typu string.')

    @property
    def login(self):
        return self._login
    @login.setter
    def login(self, value):
        # login nie może mieć znaków specjalnych
        if isinstance(value, str):
            if value.isalnum():
                self._login = value
            else:
                raise ValueError('Login może składać się tylko z liter i cyfr.')
        else:
            raise TypeError('Login musi byc typu string.')

    @property
    def haslo(self):
        return self._haslo
    @haslo.setter
    def haslo(self, value):
        
        # funkcja sprawdza czy podany ciąg znaków zawiera cyfrę
        def has_number(value):
            for character in value:
                if character.isdigit():
                    return True
            return False

        # funkcja sprawdza czy podany ciąg znaków zawiera wielką literę
        def has_capital_letter(value):
            for character in value:
                if character.isalpha() and character.capitalize() == character:
                    return True
            return False

        # haslo musi mieć co najmniej 8 znaków, 1 wielką literę i 1 cyfrę
        if isinstance(value, str):
            if len(value) < 8:
                raise ValueError('Hasło musi mieć co najmniej 8 znaków.')
            elif not has_capital_letter(value):
                raise ValueError('Hasło musi mieć co najmniej 1 wielką literę.')
            elif not has_number(value):
                raise ValueError('Hasło musi mieć co najmniej 1 cyfrę.')
            else:
                self._haslo = value
        else:    
            raise TypeError('Haslo musi byc typu string.')

    # funkcja zwraca listę roślin użytkownika, które są zadbane
    def zadbane_rosliny(self):
        zadbane_rosliny = []
        for roslina in self.listaRoslin:
            if roslina.czy_zadbana():
                zadbane_rosliny.append(roslina)
        return zadbane_rosliny
    
    # funkcja zwraca listę roślin użytkownika, które nie są zadbane
    def niezadbane_rosliny(self):
        niezadbane_rosliny = []
        for roslina in self.listaRoslin:
            if not roslina.czy_zadbana():
                niezadbane_rosliny.append(roslina)
        return niezadbane_rosliny