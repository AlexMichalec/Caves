import os
import random
import abc


class Kufer():
    def __init__(self, gra, allItems):
        self.gra = gra
        self.zawartosc = random.choices(allItems.items, allItems.probability, k=1)[0](gra)

    def open(self):
        przedmiot = self.zawartosc
        os.system("cls")
        print(self.gra.interfejs(czy_znaleziono_przedmiot=True, przedmiot=przedmiot))


class AllItems():
    def __init__(self):
        self.items = [WorekZlota, UniwersalnyKlucz, MalaSwieczka, Swieczka, DuzaSwieczka, Pochodnia, ButyDoBiegania,
                      MiksturaPredkosci, MiksturaMidasa, ButyFlasha, WorekNaMonety]
        self.probability = [0.4, 0.3, 0.3, 0.2, 0.1, 0.1, 0, 0.2, 0.2, 0,0]
        self.price = [-1, 40, 5, 10, 20, 50, 200, 30, 70, 999, 0]

    def add(self, item, prob, price):
        self.items.append(item)
        self.probability.append(prob)
        self.price.append((price))


class Ekwipunek():
    @abc.abstractmethod
    def __init__(self, gra):
        self.gra = gra
        self.name = "Przedmiot"
        self.description = "Pole na wpisanie właściwości przedmiotu"
        self.value = "2137"  # wartość przedmiotu (do sprzedania)
        self.price = self.value  # cena przedmiotu w sklepie
        self.czy_do_kupienia = True  # Czy możnak kupić w sklepie
        self.czy_mozna_uzyc = False  # Czy można użyć podczas rozgrywki
        self.czy_jednorazowy = True
        self.czy_uzywa_sie_automatycznie = False
        self.czy_zachowac_po_auto = False

    @abc.abstractmethod
    def use(self):
        pass


class WorekZlota(Ekwipunek):
    def __init__(self, gra, wartosc=0):
        super(WorekZlota, self).__init__(gra)
        self.name = "Worek złota"
        if wartosc:
            self.value = wartosc
        else:
            self.value = random.randint(5, 20)
        self.description = f"Mały woreczek zawierający: {self.value} złotych monet. "
        self.czy_do_kupienia = False
        self.czy_uzywa_sie_automatycznie = True
        self.czy_zachowac_po_auto = False

    def use(self):
        self.gra.gracz.coinbag += self.value


class Swieczka(Ekwipunek):
    def __init__(self, gra):
        super(Swieczka, self).__init__(gra)
        self.name = "Świeczka"
        self.description = "Pozwala rozjaśnic mroki jaskiń"
        self.value = 10
        self.price = 10
        self.czy_do_kupienia = True
        self.czy_mozna_uzyc = True
        self.czy_uzywa_sie_automatycznie = False
        self.moc = 2

    def use(self):
        self.gra.gracz.dodatkowe_swiatlo += self.moc


class MalaSwieczka(Swieczka):
    def __init__(self, gra):
        super(MalaSwieczka, self).__init__(gra)
        self.name = "Mała Świeczka"
        self.moc = 1
        self.value = 5
        self.price = 5


class DuzaSwieczka(Swieczka):
    def __init__(self, gra):
        super(DuzaSwieczka, self).__init__(gra)
        self.name = "Duża Świeczka"
        self.moc = 3
        self.value = 15
        self.price = 15


class Pochodnia(Swieczka):
    def __init__(self, gra):
        super(Pochodnia, self).__init__(gra)
        self.name = "Pochodnia"
        self.description = "Rozjaśnia jaskinie znacznie skuteczniej niż świeczki"
        self.moc = 5
        self.value = 50


class UniwersalnyKlucz(Ekwipunek):
    def __init__(self, gra):
        super(UniwersalnyKlucz, self).__init__(gra)
        self.name = "Klucz Uniwersalny"
        self.description = "Mały srebrny klucz, pomaga przy otwarciu drzwi do następnego poziomu. Zastępuje jeden zwykły klucz."
        self.value = 40
        self.price = 45
        self.czy_jednorazowy = True
        self.czy_mozna_uzyc = True
        self.czy_do_kupienia = True
        self.czy_uzywa_sie_automatycznie = False

    def use(self):
        self.gra.gracz.klucze_zebrane += 1


class ButyDoBiegania(Ekwipunek):
    def __init__(self, gra):
        super(ButyDoBiegania, self).__init__(gra)
        self.name = "Buty do Biegania"
        self.description = "Niepozorna para butów pozwalająca pokonywać podziemne korytarze szybciej niż normalnie. (Przedmiot wielokrotnego użytku, użyj akcji ponownie by dezaktywować.)"
        self.value = 200
        self.czy_jednorazowy = False
        self.czy_do_kupienia = True
        self.czy_uzywa_sie_automatycznie = False
        self.czy_mozna_uzyc = True
        self.moc = 1

    def use(self):
        if (self, -1) in self.gra.gracz.aktywne:
            self.gra.gracz.dodatkowe_kroki -= self.moc
            self.gra.gracz.aktywne.remove((self, -1))
        else:
            self.gra.gracz.dodatkowe_kroki += self.moc
            self.gra.gracz.aktywne.append((self, -1))


class ButyFlasha(ButyDoBiegania):
    def __init__(self, gra):
        super(ButyFlasha, self).__init__(gra)
        self.name = "Buty Flasha"
        self.description = "Super nowoczesne buciki do śmiagania z prędkością światła, niezbyt praktyczne, ale kto co lubi"
        self.moc = 20


class Mikstura(Ekwipunek):
    def __init__(self, gra):
        super(Mikstura, self).__init__(gra)
        self.name = "Mikstura"
        self.czy_jednorazowy = True
        self.czy_mozna_uzyc = True
        self.czy_do_kupienia = True
        self.czy_uzywa_sie_automatycznie = False
        self.ile_rund = 10

    def use(self):
        self.gra.gracz.aktywne.append([self, self.ile_rund])

    def deactivate(self):
        pass


class MiksturaPredkosci(Mikstura):
    def __init__(self, gra):
        super(MiksturaPredkosci, self).__init__(gra)
        self.name = self.name + " Prędkości"
        self.description = f"Mikstura pozwalająca biegać szybciej niż normalnie przez całe {self.ile_rund} rund."
        self.value = 30
        self.moc = 3

    def use(self):
        super(MiksturaPredkosci, self).use()
        self.gra.gracz.dodatkowe_kroki += self.moc

    def deactivate(self):
        super(MiksturaPredkosci, self).deactivate()
        self.gra.gracz.dodatkowe_kroki -= self.moc


class MiksturaMidasa(Mikstura):
    def __init__(self, gra):
        super(MiksturaMidasa, self).__init__(gra)
        self.name = "Mikstura Midasa"
        self.description = f"Mikstura pozwalająca na zebranie 2x większej liczby monet niż normalnie, działa {self.ile_rund} tur."
        self.value = 120
        self.moc = 1

    def use(self):
        super(MiksturaMidasa, self).use()
        self.gra.gracz.mnoznik_monet *= 2

    def deactivate(self):
        super(MiksturaMidasa, self).deactivate()
        self.gra.gracz.mnoznik_monet //= 2

class WorekNaMonety(Ekwipunek):
    def __init__(self,gra):
        super(WorekNaMonety, self).__init__(gra)
        self.name = "Worek na Monety"
