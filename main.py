import time
import random
import os
import json
from msvcrt import getch

import artefakty
import teksty
import ekwipunek


ARTFEFACTS = ["Średniowieczne Dildo", "Upadła Madonna z Wielkim Cycem", "Fragment Mozaiki", "Skamnieniały Nos",
              "Skamieniała Wiewiórka", "Stare Skarpety", "Stopa z Wyspy Wielkanocnej", "Biblia po hiszpańsku",
              "Drewniana Zabawka Piesek", "Powód do Życia", "Rubin", "Szmaragd", "Kamień Filozoficzny",
              "Perpetum Mobile"]


class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""

    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self):
        return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


def znak(j, czy_mig_mig=False):
    if j == 0:
        return "   "
    if j == 1:
        return "[ ]"
    if j == 2:
        return " . "
    if j == 3:
        if czy_mig_mig:
            return "   "
        return " X "
    if j == 4:
        return "(k)"
    if j == 5:
        return "(A)"  # <- Artefakt
    if j == 6:
        return "(E)"  # <- Ekwipunek
    if j == 7:
        return " $ "
    if j == 8:
        return " * "
    if j == 9:
        return " @ "

    if j in range(11, 20):
        return f"({j % 10})"







class Mapa:
    def __init__(self, szerokosc, dlugosc):
        self.sz = szerokosc
        self.dl = dlugosc
        self.tab = [[1] + [0] * szerokosc + [1] for i in range(dlugosc)]
        self.tab = [[1] * (szerokosc + 2)] + self.tab + [[1] * (szerokosc + 2)]
        self.wyjscie_x = 0
        self.wyjscie_y = 0
        self.wejscie_x = random.randint(1, dlugosc)
        self.wejscie_y = random.randint(1, szerokosc)
        self.tab[self.wejscie_x][self.wejscie_y] = 3

    def __str__(self):
        temp = ""
        for ii, i in enumerate(self.tab):
            for ij, j in enumerate(i):
                if self.czy_mozna_pominac(j, ii, ij):
                    temp += "   "
                else:
                    temp = temp + znak(j)
            temp += "\n"
        return temp

    def pokaz_mape(self, czy_mig_mig=False):
        temp = ""
        for ii, i in enumerate(self.tab):
            for ij, j in enumerate(i):
                if self.czy_mozna_pominac(j, ii, ij):
                    temp += "   "
                else:
                    temp = temp + znak(j, czy_mig_mig)
            temp += "\n"
        return temp

    def czy_mozna_pominac(self, j, ii, ij):
        if j != 1:
            return False
        for index in range(9):
            a = (index % 3) - 1
            b = (index // 3) - 1
            if ii + a in range(0, self.dl + 1) and ij + b in range(0, self.sz + 1):
                if self.tab[ii + a][ij + b] != 1:
                    return False
        return True

    def add_monety(self, n=2):
        t = 0
        while t < n:
            x = random.randint(1, self.dl)
            y = random.randint(1, self.sz)
            if self.tab[x][y] == 0:
                self.tab[x][y] = 10 + random.choice([1] * 25 + [2] * 12 + [3] * 10 + [4, 5, 6] * 2 + [7, 8, 9])
                t += 1

    def add_wyjscie(self):
        t = 0
        while t < 1:
            x = random.randint(1, self.dl)
            y = random.randint(1, self.sz)
            if self.tab[x][y] == 0:
                self.tab[x][y] = 9
                self.wyjscie_x = x
                self.wyjscie_y = y
                t += 1

    def rysuj_test(self, n=5, r=5, klucze=3, artefakty=1, ekwipunek=1):
        #    print("Rys\n",self,sep="")
        self.add_monety(n + r + klucze + artefakty + ekwipunek)
        self.add_wyjscie()
        c = 0
        while c < self.dl * self.sz // 3:
            #         print(f"Rys {c}\n", self, sep="")
            x = random.randint(1, self.dl)
            y = random.randint(1, self.sz)
            if self.tab[x][y] == 0:
                if self.czy_do_przejscia(x, y):
                    self.tab[x][y] = 1
                    c += 1
        while artefakty > 0:
            x = random.randint(1, self.dl)
            y = random.randint(1, self.sz)
            if self.tab[x][y] in range(11, 20):
                self.tab[x][y] = 5
                artefakty = artefakty - 1

        while ekwipunek > 0:
            x = random.randint(1, self.dl)
            y = random.randint(1, self.sz)
            if self.tab[x][y] in range(11, 20):
                self.tab[x][y] = 6
                ekwipunek = ekwipunek - 1

        while klucze > 0:
            x = random.randint(1, self.dl)
            y = random.randint(1, self.sz)
            if self.tab[x][y] in range(11, 20):
                self.tab[x][y] = 4
                klucze = klucze - 1

        while r > 0:
            x = random.randint(1, self.dl)
            y = random.randint(1, self.sz)
            if self.tab[x][y] in range(11, 20):
                self.tab[x][y] = 0
                r = r - 1
        self.tab[self.wyjscie_x][self.wyjscie_y] = 0

    def pokaz_wyjscie(self):
        self.tab[self.wyjscie_x][self.wyjscie_y] = 9

    def czy_do_przejscia(self, a, b):
        self.tab[a][b] = 40
        x = self.wejscie_x
        y = self.wejscie_y
        wazne = (0, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19)
        kolejka = [(x, y)]
        while len(kolejka) > 0:
            temp = kolejka.pop(0)
            if self.tab[temp[0] + 1][temp[1]] in wazne:
                self.tab[temp[0] + 1][temp[1]] += 40
                kolejka.append((temp[0] + 1, temp[1]))
            if self.tab[temp[0] - 1][temp[1]] in wazne:
                self.tab[temp[0] - 1][temp[1]] += 40
                kolejka.append((temp[0] - 1, temp[1]))
            if self.tab[temp[0]][temp[1] + 1] in wazne:
                self.tab[temp[0]][temp[1] + 1] += 40
                kolejka.append((temp[0], temp[1] + 1))
            if self.tab[temp[0]][temp[1] - 1] in wazne:
                self.tab[temp[0]][temp[1] - 1] += 40
                kolejka.append((temp[0], temp[1] - 1))
        czyOk = True
        wazne = (9, 11, 12, 13, 14, 15, 16, 17, 18, 19)
        for i in self.tab:
            for j in i:
                if j in wazne:
                    czyOk = False

        for i, x in enumerate(self.tab):
            for j, y in enumerate(x):
                if y >= 40:
                    self.tab[i][j] -= 40
        return czyOk


class Gracz:
    def __init__(self, gra, x, y):
        self.gra = gra
        self.imie = "Mizu"
        self.ranga = "Kot"
        self.x = x
        self.y = y
        self.punkty = 0
        self.level = 1
        self.klucze_zebrane = 0
        self.klucze_do_zebrania = 1
        self.monety_do_zebrania = 1
        self.monety_zebrane = 0
        self.coinbag = 0
        self.ostatnio_zebrane = []
        self.dodatkowe_swiatlo = 0
        self.ekwipunek = {"Worek na monety": [1, ekwipunek.WorekNaMonety(self.gra)]}
        self.ekwipunek_lista = ["Worek na monety"]
        self.artefakty = artefakty.Artefakty()
        self.czy_buty_zalozone = False
        self.aktywne = []
        self.dodatkowe_kroki = 0
        self.mnoznik_monet = 1

    def get_aktywne(self):
        if len(self.aktywne) == 0:
            return ""
        temp = " Aktywne: "
        for i, x in enumerate(self.aktywne):
            if i != 0:
                temp = temp + ", "
            temp = temp + x[0].name
            if x[0].czy_jednorazowy:
                temp = temp + "(" + str(x[1]) + ")"
        return temp

    def add_ekwipunek(self, przedmiot):
        if przedmiot.name in self.ekwipunek_lista:
            self.ekwipunek[przedmiot.name][0] += 1
        else:
            self.ekwipunek[przedmiot.name] = [1, przedmiot]
            self.ekwipunek_lista.append(przedmiot.name)

    def action(self, k):
        name = self.ekwipunek_lista[k]
        przedmiot = self.ekwipunek[name][1]
        przedmiot.use()
        if not przedmiot.czy_jednorazowy:
            return
        self.ekwipunek[name][0] -= 1
        if self.ekwipunek[name][0] == 0:
            self.ekwipunek_lista.remove(name)

    def ruch(self, mapa, szlak):
        if self.klucze_zebrane >= self.klucze_do_zebrania:
            mapa.pokaz_wyjscie()
        if szlak in "wasd" and len(self.aktywne) > 0:
            for x in self.aktywne:
                if x[0].czy_jednorazowy:
                    x[1] -= 1
                    if x[1] == 0:
                        x[0].deactivate()
            self.aktywne = [x for x in self.aktywne if x[1] != 0]
            szlak = szlak + szlak * self.dodatkowe_kroki
        for s in szlak:
            new_pos = [self.x, self.y]
            if s not in "wasd1234zc":
                continue
            if s == "w":
                new_pos[0] -= 1
            if s == "s":
                new_pos[0] += 1
            if s == "a":
                new_pos[1] -= 1
            if s == "d":
                new_pos[1] += 1

            if s == "z":
                self.gra.save()
                print("Zapisano")
                time.sleep(1)
                continue
            if s == "c":
                self.gra.open()
                time.sleep(1)
                continue
            if s in "123":
                if int(s) < len(self.ekwipunek_lista):
                    self.action(int(s))
            if s == "4":
                os.system("cls")
                print(self.gra.interfejs(czy_ekwipunek=True))
                q = getch()
                q = str(q)[2]
                if q.isnumeric():
                    if int(q) not in range(1, len(self.ekwipunek_lista)):
                        q = "l"
                while not (q.isnumeric() or q == "x"):
                    print("Podaj nr przedmiotu, który chesz użyć albo 'x', aby wyjść")
                    q = str(getch())[2]
                    if q.isnumeric():
                        if int(q) not in range(1,len(self.ekwipunek_lista)):
                            q="l"
                if q == "x":
                    continue
                qq = int(q)
                if qq < len(self.ekwipunek_lista):
                    self.action(qq)

            m = mapa.tab[new_pos[0]][new_pos[1]]
            if m == 1:
                continue
            if m == 5:
                artefakt = self.artefakty.find()
                self.gra.wiad(False, czy_inne=True, wiadomosc=f"Brawo udało Ci się znaleźć: {artefakt[0]}")
                self.ostatnio_zebrane.append(artefakt[0])
                self.punkty += 20
                if len(self.artefakty.do_zdobycia):
                    self.gra.wiad(czy_inne=True, wiadomosc="Gratulacje! Udało Ci się zebrać wszystkie artefakty :D")
            if m == 6:
                kufer = ekwipunek.Kufer(self.gra, ekwipunek.AllItems())
                kufer.open()
                if kufer.zawartosc.czy_uzywa_sie_automatycznie:
                    kufer.zawartosc.use()
                    getch()
                    if kufer.zawartosc.czy_zachowac_po_auto:
                        self.add_ekwipunek(kufer.zawartosc)
                else:
                    ch = str(getch())[2]
                    while ch not in ['1', '0']:
                        ch = str(getch())[2]
                    if ch == '1':
                        kufer.zawartosc.use()
                    else:
                        self.add_ekwipunek(kufer.zawartosc)
                if kufer.zawartosc.name == ekwipunek.WorekZlota(self.gra).name:
                    self.ostatnio_zebrane.append(kufer.zawartosc.name + " (" + str(kufer.zawartosc.value) + ")")
                else:
                    self.ostatnio_zebrane.append(kufer.zawartosc.name)
                self.punkty += 10
            if m == 9:
                self.punkty += 10
                return True
            if m in range(11, 20):
                self.punkty += 2
                self.coinbag += (m - 10) * self.mnoznik_monet
                self.ostatnio_zebrane.append(f"Złota moneta ({(m - 10) * self.mnoznik_monet})")
                self.monety_zebrane += 1
            if m == 4:
                self.punkty += 1
                self.klucze_zebrane += 1
                if self.klucze_zebrane >= self.klucze_do_zebrania:
                    mapa.pokaz_wyjscie()
                self.ostatnio_zebrane.append(f"Klucz")
            mapa.tab[self.x][self.y] = 2
            self.x = new_pos[0]
            self.y = new_pos[1]
            mapa.tab[self.x][self.y] = 3
        return False


class Gra:
    def __init__(self, w=6, l=6, level=0):
        self.mapa = Mapa(w, l)
        self.gracz = Gracz(self, l, (w + 1) // 2)
        self.gracz.level = level
        self.level = level
        self.mapa.tab[self.gracz.x][self.gracz.y] = 3
        self.monety_do_zebrania = 2
        self.monety_zebrane = 0
        # self.mapa.add_monety(self.ilosc_monet)
        self.mapa.rysuj_test(2)
        self.gracz.monety_do_zebrania = 2
        self.autozapis = False
        self.new_level()


    def intro_animation(self):
        ""
        for t in teksty.intros:
            print(t)
            time.sleep(0.3)
            os.system("cls")

        temp = teksty.intros.pop()
        teksty.intros.reverse()
        for t in teksty.intros:
            print(t)
            time.sleep(0.3)
            os.system("cls")
        teksty.intros.reverse()
        teksty.intros.append(temp)
        print(teksty.intro)
        time.sleep(1.5)
        """
        m = 110
        a = 8
        for i in range(m-a):
            temp = teksty.intro.split(sep="\n")
            temp = [" " * i + x[i:i+a] for x in temp]
            temp = "\n".join(temp)
            print(temp)
            time.sleep(0.01)
            os.system("cls")

        for i in range(m-a,0,-1):
            temp = teksty.intro.split(sep="\n")
            temp = [" " * i + x[i:i+a] for x in temp]
            temp = "\n".join(temp)
            print(temp)
            time.sleep(0.01)
            os.system("cls")"""


    def graj_intro(self):
        self.intro_animation()
        self.wiad(False, True, wiadomosc="Witaj w Świecie Jaskiń Młody Podróżniku!")
        if os.path.isfile("save.data"):
            self.wiad(False, True, wiadomosc="Czy chcesz wczytać zapisaną grę?")
            print("(1 - Tak, O - Nie) ?: ")
            ch = str(getch())[2]
            if ch == "1":
                self.open()
                return
        self.wiad(False, True, wiadomosc="Podaj proszę swoje imię!")
        self.gracz.imie = input("?: ")
        self.wiad(False, True, wiadomosc=f"Miło Cię poznać {self.gracz.imie}!")
        self.wiad(False, True, wiadomosc="Czy to Twój pierwszy raz w tej grze?")
        temp = input("(1 - Tak, 0 - Nie) ?: ")
        while temp not in ["1", "0"]:
            temp = input("(1 - Tak, 0 - Nie) ?: ")
        if temp == "0":
            self.wiad(False, True, wiadomosc="W takim razie zapraszamy do gry, miłej zabawy :D")
            return
        self.wiad(False, True, wiadomosc="Czy chiałbyś przejrzeć instrukcję przed rozpoczęciem rozgrywki?")
        temp = input("(1 - Tak, 0 - Nie) ?: ")
        while temp not in ["1", "0"]:
            temp = input("(1 - Tak, 0 - Nie) ?: ")
        if temp == "0":
            self.wiad(False, True, wiadomosc="W takim razie zapraszamy do gry, miłej zabawy :D")
            return
        os.system("cls")
        print(f"""
        
                                            Instrukcja:
                                            
        Masz na imię {self.gracz.imie}. Budzisz się w małym spokojnym miasteczku gdzieś na skraju 
        cywilizacji. Przy sobie znajdujesz parę starych map, plecak oraz mały woreczek na monety 
        (na razie pusty). Twoim wielkim marzeniem jest zostać światowej klasy poszukiwaczem przygód, 
        jednak by tego dokonać musisz znaleźć odpowiednich sponsorów (tak niestety kapitalizm dotarł 
        również tutaj). Powoli podnosisz się na skraj łóżka i przecierasz oczy, na szafce nocnej
        zauważasz list od lokalnego muzeum. Proszą Cię o pomoc w powiększeniu swojej kolekcji,
        podobno wiele cennych przedmiotów można znaleźć w tutejszych jaskiniach. Wiesz o tym dobrze
        w końcu twój ojciec był archeologiem, a matka spędziła pół życia w kopalni. Wyglądasz za 
        okno i czujesz, że to właśnie ten dzień, zakładasz szybko resztę ubrań i czym prędzej 
        ruszasz na swoją pierwszą wielką przygodę.
        
        Po jaskiniach możesz poruszać się za pomocą klawiszy [w][s][a][d], aby zejść na niższy poziom
        potrzebujesz zebrać odpowiednią liczbę kluczy(k), dodatkowo na ziemii pełno jest złotych monet
        (1-9) za które możesz póżniej kupić użyteczne przedmioty w lokalnym sklepie. Im niżej będziesz 
        schodzić tym większa szansa na znalezienie drogocennych artefaktów(A), które z pewnością
        przyciągną sponsorów do muzeum, a zatem również do Ciebie. Musisz mieć jednak na uwadze,
        że im głębiej będziesz schodzić tym ciemniejsze będzie Twoje otoczenie, pamiętaj by zabrać
        ze sobą odpowiedni ekwipunek(E). Jeśli poczujesz, że masz już dość eksploracji na ten dzień
        możesz zapisać grę, pamiętaj tylko, że po wczytaniu zaczniesz od poziomu 1. (nie będziesz
        przecież spać pod ziemią!) 
        
                    Nie trać już więcej czasu i ruszaj na wyprawę w głąb ziemii!
        
                            <kliknij dowolny klawisz by rozpocząć>
        """)
        getch()

    def ciemnosc(self, a=5, czy_mig_mig=False):
        a += self.gracz.dodatkowe_swiatlo
        x1 = max(0, self.gracz.x - min(a, 8))
        x2 = min(self.mapa.dl + 1, self.gracz.x + min(a, 8))
        y1 = max(0, self.gracz.y - min(a, 7))
        y2 = min(self.mapa.sz + 1, self.gracz.y + min(a, 7))
        temp = ""
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                r_x = abs(self.gracz.x - x)
                r_y = abs(self.gracz.y - y)
                q = self.mapa.tab[x][y]
                if r_x + r_y < a:
                    if self.gracz.x == x and r_y == a - 1 \
                            or self.gracz.y == y and r_x == a - 1:
                        temp += " ? "
                    else:
                        if r_x == 8 or r_y == 7:
                            temp += " ? "
                        else:
                            temp += znak(q, czy_mig_mig)
                else:
                    if r_x + r_y == a:
                        if self.gracz.x == x and abs(self.gracz.y - y) == a \
                                or self.gracz.y == y and r_x == a:
                            temp += "   "
                        else:
                            temp += " ? "
                    else:
                        temp += "   "
            temp += "\n"
        return temp

    def aktualizuj_range(self):
        p = self.gracz.punkty

        self.gracz.ranga = "Baby"
        if p >= 10:
            self.gracz.ranga = "Początkujący"
        if p >= 50:
            self.gracz.ranga = "Mały Jaskiniowiec"
        if p >= 100:
            self.gracz.ranga = "Młody Eksplorator"
        if p >= 200:
            self.gracz.ranga = "Grotołaz"
        if p >= 500:
            self.gracz.ranga = "Poszukiwacz Przygód"
        if p == 666:
            self.gracz.ranga = "Dziecko Szatana"
        if p >= 1000:
            self.gracz.ranga = "Znawca Jaskiń"
        if p >= 2000:
            self.gracz.ranga = "Jaskiniowa Dora"
        if p >= 1500:
            self.gracz.ranga = "Indiana Jones Junior"
        if p >= 2000:
            self.gracz.ranga = "Nowa Lara Croft"
        if p >= 2500:
            self.gracz.ranga = "Profesjonalny Grotołaz"
        if p >= 5000:
            self.gracz.ranga = "Złoty Kapelusz"
        if p >= 10000:
            self.gracz.ranga = "no-life"

    def new_level(self):
        self.level += 1
        x = 4 + self.level * 3
        y = 4 + self.level * 4
        m = 0 + self.level * 2
        k = min((3 if self.level <= 5 else 5), self.level)
        a = random.choice(
            [0] * 3 + [1] * max(0, self.level - 3) + [2] * max(0, self.level - 5) + [3] * max(0, self.level - 7))
        a = min(a,len(self.gracz.artefakty.do_zdobycia))
        e = random.choice(
            [0] * 1 + [1] * max(0, self.level) + [2] * max(0, self.level - 3) + [3] * max(0, self.level - 5) + [
                4] * max(0, self.level - 7))
        self.mapa = Mapa(x, y)
        self.gracz.x = self.mapa.wejscie_x
        self.gracz.y = self.mapa.wejscie_y
        self.gracz.monety_do_zebrania = m
        self.gracz.monety_zebrane = 0
        self.gracz.klucze_zebrane = 0
        self.gracz.klucze_do_zebrania = k
        self.gracz.level = self.level
        self.aktualizuj_range()
        self.monety_do_zebrania = m
        self.monety_zebrane = 0
        self.gracz.dodatkowe_swiatlo = 0
        self.mapa.rysuj_test(m, klucze=k, artefakty=a, ekwipunek=e)
        for i, z in enumerate(self.gracz.ostatnio_zebrane):
            if z == "Klucz":
                self.gracz.ostatnio_zebrane[i] = "Klucz (zużyty)"

    def graj(self, czy_pominac_intro=False, czy_pominac_ladowanie=False):
        if not czy_pominac_intro:
            self.graj_intro()
        if not czy_pominac_ladowanie:
            self.laduj(self.gracz.level)
        self.mig_mig()
        while True:
            os.system("cls")
            # temp = input(self.interfejs())
            print(self.interfejs(), end="")
            temp = str(getch())[2]
            if temp == "x":
                if self.wiad( True):
                    return
            if temp == "p":
                self.laduj(czy_na_powierzchnie=True)
                if self.town():
                    return
                else:
                    self.gracz.level = 0
                    self.level = 0
                    self.new_level()
                    if not czy_pominac_ladowanie:
                        self.laduj(self.gracz.level)
                    self.mig_mig()
                    continue
            if temp == "m":
                if self.menu():
                    return
            if self.gracz.ruch(self.mapa, temp):
                if self.autozapis:
                    self.save()
                self.new_level()
                if not czy_pominac_ladowanie:
                    self.laduj(self.gracz.level)
                self.mig_mig()

    def pokaz(self):
        # if self.gracz.level < 4:
        print(self.wyswietl())

    def wyswietl(self, wys=16, szer=21, czy_mig_mig=False):
        S = str(self.mapa.pokaz_mape(czy_mig_mig)).split(sep="\n")
        result = str(self.mapa.pokaz_mape(czy_mig_mig))
        if self.level >= 3:
            S = self.ciemnosc(max(3, 16 - self.level * 2), czy_mig_mig=czy_mig_mig).split(sep="\n")
        w = "   "
        if len(S[0]) < szer * 3:
            r = szer - len(S[0]) // 3
            for i, s in enumerate(S):
                S[i] = w * (r // 2 + r % 2) + s + w * (r // 2)
            S[len(S) - 1] = ""

        if len(S) < wys:
            wiersz = w * (len(S[0]) // 3)
            r = wys - len(S)
            S[len(S) - 1] = wiersz
            S = [wiersz] * (r // 2 + r % 2) + S + [wiersz] * (r // 2)
            S.append("")
        result = "\n".join(S)

        return result

    def ekran(self, wys, szer, czp=False, przedmiot=0, ce=False, cmm=False):
        if not czp and not ce:
            return self.wyswietl(18, 15, cmm)
        if czp:
            return self.znalezionoPrzedmiotEkran(przedmiot)
        if ce:
            return self.ekwipunekEkran()

    def znalezionoPrzedmiotEkran(self, przedmiot):
        temp = ""
        temp += (" " * 45 + "\n") * 7
        temp += f"{'Znaleziono: ' + przedmiot.name:^45}\n"
        temp += (" " * 45 + "\n") * 2
        temp += f"{przedmiot.description[0:40]:^45}\n"
        temp += f"{przedmiot.description[40:80]:^45}\n"
        temp += f"{przedmiot.description[80:120]:^45}\n"
        temp += (" " * 45 + "\n") * 3
        if przedmiot.czy_uzywa_sie_automatycznie:
            temp += f"{'Kliknij dowolny przycisk by kontynować :D':^45}\n"
        else:
            temp += f"{'[1] - użyj teraz [0] - zachowaj na później :D':^45}\n"
        temp += (" " * 45 + "\n")
        return temp

    def ekwipunekEkran(self):
        a = 3
        temp = ""
        temp += " " * 45 + "\n"
        temp += " " * a + f"{' Twój ekwipunek:':^42}\n".upper()
        temp += " " * 45 + "\n"
        for i, e in enumerate(self.gracz.ekwipunek_lista):
            if i == 0:
                temp += " " * a + " " * 3 + f"{e + '(' + str(self.gracz.coinbag) + ')':<39}\n"
            else:
                temp += " " * a + f"{str(i) + '.':<3}" + f"{e + ' x' + str(self.gracz.ekwipunek[e][0]):<39}" + "\n"

        for i in range(12 - len(self.gracz.ekwipunek_lista)):
            temp += " " * 45 + "\n"

        temp += f"{'Wybierz nr przedmiotu, którego chcesz użyć':^45}" + "\n"
        temp += f"{'lub x, aby wrócić do gry':^45}" + "\n"
        return temp

    def interfejs(self, wys=18, szer=45, czy_znaleziono_przedmiot=False, przedmiot=0, czy_ekwipunek=False,
                  czy_mig_mig=False):
        e = self.ekran(wys, szer, czy_znaleziono_przedmiot, przedmiot, czy_ekwipunek, czy_mig_mig)
        temp = e.split("\n")
        for i, t in enumerate(temp):
            temp[i] = "  " + t + "         "
        temp = [""] + temp
        temp[2] = temp[2] + f"Poziom: {self.level:<2}" + " " * 20 + f"Gracz: {self.gracz.imie:<20}"
        temp[3] = temp[3] + " " * 30 + f"Ranga: {self.gracz.ranga}"
        temp[4] = temp[
                      4] + f"Klucze: {self.gracz.klucze_zebrane}/{self.gracz.klucze_do_zebrania}" + " " * 19 + f"Punkty: {self.gracz.punkty}"
        temp[5] = temp[
                      5] + f"Monety:{self.gracz.monety_zebrane:>2}/{self.gracz.monety_do_zebrania:<2}" + " " * 18 + f"Zebrane monety ({self.gracz.coinbag})"
        temp[6] = temp[6] + f"Artefakty: 0/??" + " " * 15
        temp[7] = temp[7] + self.kompas(1) + " " * 25
        temp[8] = temp[8] + self.kompas(2) + " " * 25 + f"  Ekwipunek:"
        temp[9] = temp[9] + self.kompas(
            3) + " " * 25 + f"{('1. ' + self.gracz.ekwipunek_lista[1] + ' x' + str(self.gracz.ekwipunek[self.gracz.ekwipunek_lista[1]][0])) if len(self.gracz.ekwipunek_lista) > 1 else ''} "
        temp[10] = temp[
                       10] + f"  Sterowanie:" + " " * 17 + f"{('2. ' + self.gracz.ekwipunek_lista[2] + ' x' + str(self.gracz.ekwipunek[self.gracz.ekwipunek_lista[2]][0])) if len(self.gracz.ekwipunek_lista) > 2 else ''} "
        temp[11] = temp[11] + f" w - krok w górę " + chr(
            24) + " " * 12 + f"{('3. ' + self.gracz.ekwipunek_lista[3] + ' x' + str(self.gracz.ekwipunek[self.gracz.ekwipunek_lista[3]][0])) if len(self.gracz.ekwipunek_lista) > 3 else ''} "
        temp[12] = temp[12] + f" s - krok w dół " + chr(25) + " " * 13 + (
            "4. ..." if len(self.gracz.ekwipunek_lista) > 4 else "")
        temp[13] = temp[13] + f" a - krok w lewo " + chr(17)
        temp[14] = temp[14] + f" d - krok w prawo " + chr(16) + " " * 13 + f"Ostatnio zebrane:"
        temp[15] = temp[15] + f"123 - użyj przedmiotu" + " " * 10 + \
                   (f">> {self.gracz.ostatnio_zebrane[len(self.gracz.ostatnio_zebrane) - 1]}" if len(
                       self.gracz.ostatnio_zebrane) >= 1 else "")
        temp[16] = temp[16] + f" 4 - ekwipunek" + " " * 17 + (
            f">> {self.gracz.ostatnio_zebrane[len(self.gracz.ostatnio_zebrane) - 2]}" if len(
                self.gracz.ostatnio_zebrane) >= 2 else "")
        temp[17] = temp[17] + f" m - pokaż menu" + " " * 16 + (
            f">> {self.gracz.ostatnio_zebrane[len(self.gracz.ostatnio_zebrane) - 3]}" if len(
                self.gracz.ostatnio_zebrane) >= 3 else "")
        temp[18] = temp[18] + " " * 30 + ("..." if len(self.gracz.ostatnio_zebrane) > 3 else "")
        temp = [""] * 3 + temp
        temp.append(self.gracz.get_aktywne())
        temp.append("")
        temp.append("")
        temp.append("?: ")
        result = "\n".join(temp)
        return result

    def kompas(self, part):
        if self.gracz.klucze_do_zebrania > self.gracz.klucze_zebrane:
            if part == 2:
                return "  ?  "
            else:
                return "     "
        r_x = self.gracz.x - self.mapa.wyjscie_x
        r_y = self.gracz.y - self.mapa.wyjscie_y
        prog2 = 1
        prog3 = 6
        if part == 0:
            if r_x > prog3:
                return f"  ^  "
            else:
                return "     "
        if part == 1:
            if r_x > prog2:
                return f"  ^  "
            else:
                return "     "
        if part == 2:
            temp = ""
            if r_y > prog3:
                temp += "<"
            else:
                temp += " "
            if r_y > prog2:
                temp += "<"
            else:
                temp += " "
            if abs(r_x) > abs(r_y):
                if r_x > 0:
                    temp += "^"
                else:
                    temp += "v"
            else:
                if r_y > 0:
                    temp += "<"
                else:
                    temp += ">"

            if r_y < -prog2:
                temp += ">"
            else:
                temp += " "
            if r_y < -prog3:
                temp += ">"
            else:
                temp += " "

            return temp
        if part == 3:
            if r_x < -prog2:
                return f"  v  "
            else:
                return "     "

        if part == 4:
            if r_x < -prog3:
                return f"  v  "
            else:
                return "     "

    def mig_mig(self):
        for i in range(5):
            time.sleep(0.15)
            os.system("cls")
            if i % 2:
                print(self.interfejs(czy_mig_mig=True))
            else:
                print(self.interfejs())

    def save(self):
        with open("save.data", "w") as myFile:
            myFile.write(self.gracz.imie)
            myFile.write("\n")
            myFile.write(str(self.gracz.punkty))
            myFile.write("\n")
            myFile.write(str(self.gracz.coinbag))
            myFile.write("\n")
            temp = [(x[0], x[1].name) for x in list(self.gracz.ekwipunek.values())]
            myFile.write(str(temp))
            myFile.write("\n")
            myFile.write(str(self.gracz.artefakty.posiadane))
            myFile.write("\n")

    def open(self):
        if not os.path.isfile("save.data"):
            return False
        with open("save.data") as myFile:
            self.gracz.imie = myFile.readline().rstrip()
            self.gracz.punkty = int(myFile.readline())
            self.aktualizuj_range()
            self.gracz.coinbag = int(myFile.readline())
            temp = myFile.readline()
            temp = temp[2:-3].split("), (")
            temp = [(x.split(", ")[0], x.split(", ")[1]) for x in temp]
            temp = [(int(x[0]), x[1][1:-1]) for x in temp]
            slownik = ekwipunek.AllItems().items
            slownik = {x(G).name: x for x in slownik}
            temp = [(x[0], slownik[x[1]](self)) for x in temp]
            self.gracz.ekwipunek_lista = []
            self.gracz.ekwipunek = {}
            for t in temp:
                self.gracz.add_ekwipunek(t[1])
                self.gracz.ekwipunek[t[1].name][0] = t[0]
            self.gracz.level = 1
            temp = myFile.readline()
            if "(" not in temp:
                return
            temp = temp[3:-4].split("'), ('")
            temp = [(x.split("', '")[0], x.split("', '")[1]) for x in temp]
            self.gracz.artefakty = artefakty.Artefakty()
            self.gracz.artefakty.load_from_save(temp)


    def wiad(self, czy_koniec=False, czy_inne=False, wiadomosc=""):
        if czy_koniec:
            os.system("cls")
            print("\n" * 13)
            print("Czy chesz zapisać swój postęp przed wyjściem?".center(118))
            print("[1] Tak   [0] Nie   [x] Anuluj\n".center(118))
            print("\n" * 7)
            ch = str(getch())[2]
            while ch not in "10x":
                ch = str(getch())[2]
            if ch == "1":
                self.save()
                self.wiad(czy_inne=True, wiadomosc="Gra została pomyślnie zapisana ^^")
                self.wiad(czy_inne=True, wiadomosc="Dzięki za wspólną wędrówkę, do zobaczenia następnym razem ^^")
                return True
            if ch == "0":
                self.wiad(czy_inne=True, wiadomosc="Dzięki za wspólną wędrówkę, do zobaczenia następnym razem ^^")
                return True
            if ch == "x":
                return False

        text = ""
        level = self.gracz.level
        match level:
            case 1:
                text = "Uważaj na głowę podczas swoich eksploracji!"
            case 2:
                text = "Pamiętaj, żeby zebrać wszystkie monety przed przejściem dalej!"
            case 3:
                text = "Za zebrane monety możesz kupić pomocne przedmioty w sklepie ^^"
            case 4:
                text = "Uważaj, jaskinie stają się coraz większe i ciemniejsze..."
            case 5:
                text = "Im głębsze jaskinie tym większa szansa na znalezienie cennych artefaktów."
            case 6:
                text = "Prawdziwy z Ciebie poszukiwacz przygód, byle tak dalej! :D"
            case 7:
                text = "W mrokach podziemii świeczki i pochodnie są bardzo przydatne ^^"
            case 8:
                text = "Większość przedmiotów działa tylko raz, ale są i takie których można używać wielokrotnie"
        if czy_inne:
            text = wiadomosc
        if text == "":
            return
        temp = ""
        for w in text.split():
            os.system("cls")
            print("\n" * 13)
            temp = temp + " " + w
            print(f"{temp:^120}")
            print("\n" * 8)
            time.sleep(0.3)
        time.sleep(0.5)



    def laduj(self,poziom=4, proc=0, czy_na_powierzchnie = False):
        os.system("cls")
        print("\n" * 12)
        temp = f"Poziom {poziom}."
        if czy_na_powierzchnie:
            temp = "Na powierzchnię..."
        print(f"{temp:^120}")
        if proc != 0:
            temp = "|" + "-" * proc + " " * (30 - proc) + "|"
            print(f"{temp:^120}")
        print("\n" * 8)
        time.sleep(random.random() / 2)
        if proc < 30:
            newproc = min(30, proc + random.randint(1, 8))
            self.laduj(poziom, newproc, czy_na_powierzchnie)
        else:
            if not czy_na_powierzchnie:
                self.wiad()


    def town(self):
        budynek = []
        budynek.append("""    1. Do Jaskiń    
                    
        [][][]      
      []      []    
    []          []  
  []              []
  []    [][][]    []
  []    []  []    []
  """)

        budynek.append("""    2. Sklep    
                
  [][][][][][][]
  []          []
  []  []  []  []
  []          []
  []  []  []  []
  []          []
  []  []  []  []
  []          []
  []  []  []  []
  []          []
  []  []  []  []
  []          []
  []  [][][]  []
  []  []  []  []
          """)

        budynek.append("""       3. Muzeum      
                      
  [][][][][][][][][][]
   []              [] 
  []   []      []   []
   []              [] 
  []   []      []   []
   []              [] 
  []     [][][]     []
  []     []  []     []
           """)

        budynek.append("""    4. Wyjście
                
  [][][][][][][]
  [] ->   EXIT[]
  [] EXIT ->  []
  []->  EXIT  []
  [][][][][][][]
    []      []
    []      []
        """)

        pp = "        "
        temp2 = ["      " for i in range(23)]
        temp2[2] = "   Gdzie chcesz się teraz udać? (1-4)"
        for i in range(0, len(budynek)):
            q = budynek[i].split("\n")
            c = max(len(q[len(q) - 2]), len(q[len(q) - 3]))
            while len(q) < len(temp2):
                q = [" " * c] + q

            for i in range(len(temp2)):
                temp2[i] = temp2[i] + q[i] + pp
        temp2.pop()
        temp2.append("  " + "[]" * 58)
        temp2.append("  " + "  " * 58)
        temp2.append("  " + "[]" * 58)
        temp2.append("  " + "  " * 58)
        temp2.append("  " + "  " * 58)
        temp2.append("?:")

        temp2 = "\n".join(temp2)
        while True:
            os.system("cls")
            print(temp2, end="")
            x = str(getch())[2]
            while x not in "1234":
                print(f"{x}\nKliknij [1], [2], [3] lub [4]\n?:", end="")
                x = str(getch())[2]
            if x == "4":
                if self.wiad( True):
                    return True
            if x == "1":
                return False
            if x == "2":
                self.shop()
            if x == "3":
                self.museum()


    def shop(self):
        A = ekwipunek.AllItems()
        temp = zip(A.items,A.price)
        temp = list(filter(lambda x: x[0](self).czy_do_kupienia,temp))
        temp.sort(key=lambda x:x[1])
        chosen = 0
        while (True):
            temp = list(filter(lambda x: x[0](self).czy_jednorazowy or (not x[0](self).name in self.gracz.ekwipunek_lista and not x[0](self).czy_jednorazowy),temp))
            os.system("cls")
            print(f"\n\n\t\tWitamy w naszym sklepie, co checesz kupić?                                      Twoje monety: {self.gracz.coinbag}\n")
            print(f" Sklep: {'Twój Ekwipunek:':>90}")
            for i, t in enumerate(temp):
                print(f"{' >> ' if chosen==i else '    '}{str(i+1)}. {t[0](self).name:.<30}{str(t[1]):.>4}", end="")
                if i >= len(self.gracz.ekwipunek_lista):
                    print("")
                else:
                    print(f"{' '*39}{str(i+1):>2}. { self.gracz.ekwipunek_lista[i]:.<25}{'x'+str(self.gracz.ekwipunek[self.gracz.ekwipunek_lista[i]][0]) } ")
            if len(self.gracz.ekwipunek_lista) > len(temp):
                for i in range(len(temp),len(self.gracz.ekwipunek_lista)):
                    print(
                        f"{' ' * 80}{str(i + 1):>2}. {self.gracz.ekwipunek_lista[i]:.<25}{'x' + str(self.gracz.ekwipunek[self.gracz.ekwipunek_lista[i]][0])} ")

            print(f"\n\n\n{'Opis:':^118}")
            print(f"{temp[chosen][0](self).description[:80]:^118}")
            print(f"{temp[chosen][0](self).description[80:]:^118}")
            print("\n\n\n")
            print(f"{'Sterowanie: [w] '+chr(24) +'   [s] '+chr(25)+'   [enter] kup    [x] wyjście':^118}")
            print(f"{'Możesz też używać klawiszy [1-'+ str(len(temp))+'] do szybszego kupowania':^118}")

            g = getch()
            ch = str(g)[2]
            if ch == "x":
                return
            if ch == "w":
                chosen = (chosen-1)%len(temp)
            if ch == "s":
                chosen = (chosen + 1) % len(temp)
            if ch.isnumeric():
                if int(ch) > 0 and int(ch) <= len(temp):
                    if self.gracz.coinbag >= temp[int(ch)-1][1]:
                        self.gracz.add_ekwipunek(temp[int(ch)-1][0](self))
                        self.gracz.coinbag -= temp[int(ch)-1][1]
                        if chosen == len(temp)-1:
                            chosen -=1
                    else:
                        self.wiad(czy_inne=True,wiadomosc="Nie masz wystarczająco monet na ten przedmiot :c")
            if str(g) == "b'\\r'":
                if self.gracz.coinbag >= temp[chosen][1]:
                    self.gracz.add_ekwipunek(temp[chosen][0](self))
                    self.gracz.coinbag -= temp[chosen][1]
                    if chosen == len(temp) - 1:
                        chosen -= 1
                else:
                    self.wiad(czy_inne=True, wiadomosc="Nie masz wystarczająco monet na ten przedmiot :c")



    def museum(self):
        A = self.gracz.artefakty
        temp_list = []
        temp = ""

        os.system("cls")
        for k in A.kategorie.keys():
            if temp.count("\n") + A.kategorie[k][0] > 30:
                temp_list.append(temp)
                temp = ""
            temp+=" "*39 + "\n"
            if A.kategorie[k][1]>0:
                temp+=f"{k:^39}".upper()+"\n"
            else:
                temp += " "*39 + "\n"
            for i, a in enumerate(A.kategorie[k]):
                if i <= 1:
                    continue
                if (a,k) in A.posiadane:
                    temp +=f"{str(i-1)+'. '+a:^39}" + "\n"
                    continue
                temp += " "*39 + "\n"




        #print(temp_list)
        if len(temp_list[0]) > len(temp_list[1]):
            temp_list[1] += f"\n{'Kliknij dowolny klawisz, aby wyjść':^39}\n"
        else:
            temp_list[0] += f"\n{'Kliknij dowolny klawisz, aby wyjść':^39}\n"
        new = ""
        while temp.count("\n") < 14:
            temp = " "*39 + "\n" +temp

        temp = f"{'M U Z E U M':^39}\n"+" "*39 +f"\n{'M U Z E U M':^39}\n" + " "*39 + f"\n{'M U Z E U M':^39}\n" + \
                " "*39 + f"\n{str(len(A.posiadane)) + '/' + str(len(A.posiadane)+len(A.do_zdobycia)):^39}\n"+temp

        while temp.count("\n") < 28:
            temp = " "*39 + "\n" +temp



        for i in range(30):
            new += (temp_list[0].split("\n")[i] if len(temp_list[0].split("\n"))>i else " "*39)+ \
                   (temp.split("\n")[i] if len(temp.split("\n")) > i else " "*39)+ \
                   (temp_list[1].split("\n")[i] if len(temp_list[1].split("\n")) > i else " " * 39) + "\n"
        new = new.rstrip()
      #  new.removesuffix("\n")
        print(new)
        getch()

    def menu(self):
        chosen = 0
        menu_texts = ["Powrót do Gry", "Zapisz Grę", "Wczytaj Grę", "Ekwipunek", "Wróć na Powierzchnię", "Zamknij Grę"]
        while True:

            os.system("cls")
            print("\n"*7)
            print("MENU".center(118))
            print("")
            for i, t in enumerate(menu_texts):
                temp = (">> " if chosen == i else "") + str(i+1) + ". " + t + (" <<" if chosen == i else "")
                print(temp.center(118))
            print("\n"*12)
            print(f"Sterowanie: [w] {chr(24)}   [s] {chr(25)}  [enter] wybór".center(118))
            print(f"Możesz też wybierać za pomocą klawiszy [1-6]".center(118))
            g = str(getch())
            ch = g[2]
            if ch == "w":
                chosen = (chosen-1)%len(menu_texts)
            if ch == "s":
                chosen = (chosen+1)%len(menu_texts)

            if g == "b'\\r'" and chosen == 0 or ch == "1": #BACK TO THE GAME
                return False
            if g == "b'\\r'" and chosen == 1 or ch == "2": #SAVE
                self.save()
                self.wiad(czy_inne=True,wiadomosc="Gra została pomyślnie zapisana :D")
            if g == "b'\\r'" and chosen == 2 or ch == "3": #LOAD
                self.open()
                self.wiad(czy_inne=True, wiadomosc="Gra została wczytana ^^")
                ch = "5"
            if g == "b'\\r'" and chosen == 3 or ch == "4": #EQUIPMENT
                self.gracz.ruch(self.mapa,"4")
                return False
                pass
            if g == "b'\\r'" and chosen == 4 or ch == "5": #BACK TO THE SURFACE
                self.laduj(czy_na_powierzchnie=True)
                if self.town():
                    return True
                else:
                    self.gracz.level = 0
                    self.level = 0
                    self.new_level()
                    self.laduj(self.gracz.level)
                    self.mig_mig()
                    return False
            if g == "b'\\r'" and chosen == 5 or ch == 6: #EXIT
                if self.wiad(czy_koniec=True):
                    return True





if __name__ == '__main__':
    getch = _Getch()
    G = Gra()
    """""
    bdb = ekwipunek.ButyDoBiegania(G)
  #  G.gracz.add_ekwipunek(bdb)
    bf = ekwipunek.ButyFlasha(G)
 #   G.gracz.add_ekwipunek(bf)
    for i in range(20):
        k = ekwipunek.Kufer(G,ekwipunek.AllItems())
        G.gracz.add_ekwipunek(k.zawartosc)
    #G.gracz.ruch(G.mapa,"4")"""
 #   G.open()
  #  G.menu()
    G.gracz.punkty = 5555
    G.graj()

