import os
import random
import abc
import time
from msvcrt import getch


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
                      MiksturaPredkosci, MiksturaMidasa, ButyFlasha, WorekNaMonety, NicAriadny, Drogowskaz, Dynamit]
        self.probability = [0.4, 0.3, 0.3, 0.2, 0.1, 0.1, 0, 0.2, 0.2, 0,0, 0.0, 0.1, 0.05]
        self.price = [-1, 40, 10, 20, 25, 50, 200, 30, 70, 999, 0, 2999, 140, 110]

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
        self.czy_do_kupienia = False
        self.czy_mozna_uzyc = True
        self.czy_uzywa_sie_automatycznie = False
        self.moc = 2

    def use(self):
        self.gra.gracz.dodatkowe_swiatlo += self.moc


class MalaSwieczka(Swieczka):
    def __init__(self, gra):
        super(MalaSwieczka, self).__init__(gra)
        self.name = "Mała Świeczka"
        self.description = "Pozwala nieco zwiększyć krąg widzenia."
        self.moc = 1
        self.value = 5
        self.price = 5
        self.czy_do_kupienia = True


class DuzaSwieczka(Swieczka):
    def __init__(self, gra):
        super(DuzaSwieczka, self).__init__(gra)
        self.name = "Duża Świeczka"
        self.description = "Pozwala rozjaśnić ciemniejsze jaskinie i groty."
        self.moc = 3
        self.value = 15
        self.price = 15
        self.czy_do_kupienia = True


class Pochodnia(Swieczka):
    def __init__(self, gra):
        super(Pochodnia, self).__init__(gra)
        self.name = "Pochodnia"
        self.description = "Rozjaśnia jaskinie znacznie skuteczniej niż świeczki"
        self.moc = 5
        self.value = 50
        self.czy_do_kupienia = False

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
        self.description = "Niepozorna para butów pozwalająca pokonywać podziemne korytarze szybciej niż normalnie. (Przedmiot wielokrotnego użytku, użyj ponownie by dezaktywować.)"
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
        self.description = "Super nowoczesne buciki do śmigania z prędkością światła (Przedmiot wielokrotnego użytku, użyj ponownie aby dezaktywować"
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
        self.description = "To tutaj nosisz wszystkie swoje monety."
        self.czy_do_kupienia = False


class NicAriadny(Ekwipunek):
    def __init__(self,gra):
        super(NicAriadny, self).__init__(gra)
        self.name = "Nić Ariadny"
        self.description = "Wbrew pozorom to nie artefakt, pozwala znaleźć szybką drogę do wyjścia jeśli masz już wszystkie klucze. (Przedmiot wielokrotnego użytku)"
        self.czy_do_kupienia = True
        self.czy_mozna_uzyc = True
        self.czy_jednorazowy = False
        self.czy_uzywa_sie_automatycznie = False
        self.value = 2999
        self.price = 2999

    def use(self):
        if self.gra.gracz.klucze_zebrane < self.gra.gracz.klucze_do_zebrania:
            return False
        x = self.gra.gracz.x
        y = self.gra.gracz.y
        wazne = (0, 2, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19)
        kolejka = [(x, y,[])]
        nms = []
        while len(kolejka) > 0:
            temp = kolejka.pop(0)
            if self.gra.mapa.wyjscie_x == temp[0] and self.gra.mapa.wyjscie_y == temp[1]:
                nms = temp[2]
                break

            if self.gra.mapa.tab[temp[0] + 1][temp[1]] in wazne:
                self.gra.mapa.tab[temp[0] + 1][temp[1]] += 40
                kolejka.append((temp[0] + 1, temp[1],temp[2]+[(temp[0],temp[1])]))
            if self.gra.mapa.tab[temp[0] - 1][temp[1]] in wazne:
                self.gra.mapa.tab[temp[0] - 1][temp[1]] += 40
                kolejka.append((temp[0] - 1, temp[1],temp[2]+[(temp[0],temp[1])]))
            if self.gra.mapa.tab[temp[0]][temp[1] + 1] in wazne:
                self.gra.mapa.tab[temp[0]][temp[1] + 1] += 40
                kolejka.append((temp[0], temp[1] + 1,temp[2]+[(temp[0],temp[1])]))
            if self.gra.mapa.tab[temp[0]][temp[1] - 1] in wazne:
                self.gra.mapa.tab[temp[0]][temp[1] - 1] += 40
                kolejka.append((temp[0], temp[1] - 1,temp[2]+[(temp[0],temp[1])]))

        for i, x in enumerate(self.gra.mapa.tab):
            for j, y in enumerate(x):
                if y >= 40:
                    self.gra.mapa.tab[i][j] -= 40


        for q in nms:
            if self.gra.mapa.tab[q[0]][q[1]] in (0,2):
                self.gra.mapa.tab[q[0]][q[1]] = 8

class Drogowskaz(NicAriadny):
    def __init__(self,gra):
        super(Drogowskaz, self).__init__(gra)
        self.name = "Drogowskaz"
        self.description = "Sprytny przedmiot pozwalający na znalezienie drogi do wyjścia po zebraniu wszystkich kluczy."
        self.czy_jednorazowy = True
        self.value = 140
        self.price = 140

class Dynamit(Ekwipunek):
    def __init__(self, gra):
        super(Dynamit, self).__init__(gra)
        self.name = "Dynamit"
        self.description = "Pozwala usunąć z planszy jeden skalny blok i na chwilę rozjaśnia jaskinię"
        self.czy_jednorazowy = True
        self.czy_mozna_uzyc = True
        self.czy_do_kupienia = True
        self.czy_uzywa_sie_automatycznie = False

    def use(self):
        print("Który blok chcesz spróbować wysadzić?")
        temp = str(getch())[2]
        while temp not in "wasd":
            print("Kliknij [w], [a], [s] lub [d]")
            temp = str(getch())[2]
        x = -1 if temp == "w" else 1 if temp == "s" else 0
        y = -1 if temp == "a" else 1 if temp == "d" else 0
        xd = self.gra.gracz.x + x
        yd = self.gra.gracz.y + y
        if self.gra.mapa.dl < xd or xd<=0 or yd<=0 or self.gra.mapa.sz <yd or self.gra.mapa.tab[xd][yd] != 1:
            print("Nie możesz tego wysadzić :c")
            time.sleep(1)
            self.gra.gracz.add_ekwipunek(Dynamit(self.gra))
            return False

        self.gra.mapa.tab[xd][yd] = 8

        self.gra.gracz.dodatkowe_swiatlo += 10
        os.system("cls")
        print(self.gra.interfejs())
        print("BOOOOOOM!!!")
        time.sleep(2)
        self.gra.gracz.dodatkowe_swiatlo -= 10
        self.gra.mapa.tab[xd][yd] = random.choices((0,5,6),(0.7,0.1,0.2),k=1)[0] #(empty, artefacts, equipment)
