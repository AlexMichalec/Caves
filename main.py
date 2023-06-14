import time
import random
import os
from msvcrt import getch

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
    if j == 9:
        return " @ "

    if j in range(11, 20):
        return f"({j % 10})"


def laduj(poziom=4, proc=0):
    os.system("cls")
    print("\n" * 12)
    temp = f"Poziom {poziom}."
    print(f"{temp:^120}")
    if proc != 0:
        temp = "|" + "-" * proc + " " * (30 - proc) + "|"
        print(f"{temp:^120}")
    print("\n" * 8)
    time.sleep(random.random() / 2)
    if proc < 30:
        newproc = min(30, proc + random.randint(1, 8))
        laduj(poziom, newproc)
    else:
        wiad(poziom)


def wiad(level=1, czy_koniec=False, czy_inne=False, wiadomosc=""):
    text = ""
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
    if czy_koniec:
        text = "Dzięki za wspólną wędrówkę, do zobaczenia następnym razem ^^"
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
    if czy_koniec:
        temp = "<kliknij [enter] aby wyjść>"
        input(f"{temp:^120}")


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
        self.ekwipunek = {"Worek na monety": [1, 0]}
        self.ekwipunek_lista = ["Worek na monety"]
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
            if s not in "wasd1234":
                continue
            if s == "w":
                new_pos[0] -= 1
            if s == "s":
                new_pos[0] += 1
            if s == "a":
                new_pos[1] -= 1
            if s == "d":
                new_pos[1] += 1

            if s in "123":
                if int(s) < len(self.ekwipunek_lista):
                    self.action(int(s))
            if s == "4":
                os.system("cls")
                print(self.gra.interfejs(czy_ekwipunek=True))
                q = input("")
                while not (q.isnumeric() or q == "x"):
                    q = input("Podaj nr przedmiotu, który chesz użyć albo 'x' aby wyjść")
                if q == "x":
                    continue
                qq = int(q)
                if qq < len(self.ekwipunek_lista):
                    self.action(qq)

            m = mapa.tab[new_pos[0]][new_pos[1]]
            if m == 1:
                continue
            if m == 5:
                artefakt = random.choice(ARTFEFACTS)
                wiad(1, False, czy_inne=True, wiadomosc=f"Brawo udało Ci się znaleźć: {artefakt}")
                self.ostatnio_zebrane.append(artefakt)
                self.punkty += 20
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
        self.new_level()

    def graj_intro(self):
        print(teksty.intro)
        time.sleep(2.5)
        wiad(1, False, True, wiadomosc="Witaj w Świecie Jaskiń Młody Podróżniku!")
        wiad(1, False, True, wiadomosc="Podaj proszę swoje imię!")
        self.gracz.imie = input("?: ")
        wiad(1, False, True, wiadomosc=f"Miło Cię poznać {self.gracz.imie}!")
        wiad(1, False, True, wiadomosc="Czy to Twój pierwszy raz w tej grze?")
        temp = input("(1 - Tak, O - Nie) ?: ")
        while temp not in ["1", "0"]:
            temp = input("(1 - Tak, O - Nie) ?: ")
        if temp == "0":
            wiad(1, False, True, wiadomosc="W takim razie zapraszamy do gry, miłej zabawy :D")
            return
        wiad(1, False, True, wiadomosc="Czy chiałbyś przejrzeć instrukcję przed rozpoczęciem rozgrywki?")
        temp = input("(1 - Tak, O - Nie) ?: ")
        while temp not in ["1", "0"]:
            temp = input("(1 - Tak, O - Nie) ?: ")
        if temp == "0":
            wiad(1, False, True, wiadomosc="W takim razie zapraszamy do gry, miłej zabawy :D")
            return
        wiad(1, False, True, wiadomosc="Przykro nam instrukcja jeszcze nie gotowa, ale na pewno sobie poradzisz ^^")

    def graj_intro_old(self):
        print("\n")
        print("Witaj poszukiwaczu przygód! :D")
        time.sleep(1)
        x = input("\nCzy jesteś gotów rozpocząć podróż? :3\n"
                  "1 - Tak jestem!\n"
                  "0 - Nie potrzebuję najpierw Instrukcji\n\n"
                  "?: ")
        while x not in ["1", "0"]:
            x = input("\nWybierz 1 lub 0\n?: ")
        if x == "1":
            return
        if x == "0":
            os.system("cls")
            print("""\n\n\nHej, witaj młody eksploratorze jaskiń!
Twoim zadaniem będzie poszukiwanie złotych monet,
kluczy oraz innych cennych artefaktów w coraz
głębszych jaskiniach. Aby sterować swoją
postacią wpisuj komendy [w][a][s][d] bez przecinków,
możesz wpisać ile chcesz kroków, Twoja postać
ruszy z miejsca dopiero po kliknięciu [enter]

Legenda mapy:
 X  - Ty, a raczej Twoja postać ^^
[ ] - ściana, tutaj nie wejdziesz
(k) - klucz, zbierz je wszystkie by przejść dalej
 @  - wyjście, pojawi się gdy już zbierzesz wszystkie klucze
(1) - moneta, mogą mieć różne wartości, warto je zbierać
(A) - artefakt, czekają na odkrycie w najgłebszych jaskiniach
\n\n""")
            x = input("Czy wszystko jasne? (1-Tak, 0-Nie)\n?: ")
            while x != "1":
                x = input("\nOk, bez pośpiechu :p (1-gotów)\n?: ")

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

        self.gracz.ranga = "Tester Junior"
        if p >= 10:
            self.gracz.ranga = "Tester"
        if p >= 50:
            self.gracz.ranga = "Tester Senior"
        if p >= 100:
            self.gracz.ranga = "Poszukiwacz Przygód"
        if p >= 200:
            self.gracz.ranga = "Profesjonalny Grotołaz"
        if p >= 666:
            self.gracz.ranga = "Dziecko Szatana"

    def new_level(self):
        self.level += 1
        x = 4 + self.level * 3
        y = 4 + self.level * 4
        m = 0 + self.level * 2
        k = min((3 if self.level <= 5 else 5), self.level)
        a = random.choice(
            [0] * 3 + [1] * max(0, self.level - 3) + [2] * max(0, self.level - 5) + [3] * max(0, self.level - 7))
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
            laduj(self.gracz.level)
        self.mig_mig()
        while True:
            os.system("cls")
            # temp = input(self.interfejs())
            print(self.interfejs(), end="")
            temp = str(getch())[2]
            if "x" in temp:
                wiad(1, True)
                break
            if self.gracz.ruch(self.mapa, temp):
                self.new_level()
                if not czy_pominac_ladowanie:
                    laduj(self.gracz.level)
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

        temp += f"{'Wpisz nr przedmiotu, który chcesz użyć':^45}" + "\n"
        temp += f"{'lub x aby wrócić do gry + kliknij enter':^45}" + "\n"
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
        temp[15] = temp[15] + f"123 - użyj ekwipunku" + " " * 10 + \
                   (f">> {self.gracz.ostatnio_zebrane[len(self.gracz.ostatnio_zebrane) - 1]}" if len(
                       self.gracz.ostatnio_zebrane) >= 1 else "")
        temp[16] = temp[16] + f" 4 - pokaż ekwipunek" + " " * 10 + (
            f">> {self.gracz.ostatnio_zebrane[len(self.gracz.ostatnio_zebrane) - 2]}" if len(
                self.gracz.ostatnio_zebrane) >= 2 else "")
        temp[17] = temp[17] + f" x - zakończ grę" + " " * 14 + (
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


if __name__ == '__main__':
    getch = _Getch()
    G = Gra()
    """
    bdb = ekwipunek.ButyDoBiegania(G)
    G.gracz.add_ekwipunek(bdb)
  #  bf = ekwipunek.ButyFlasha(G)
 #   G.gracz.add_ekwipunek(bf)
  #  for i in range(80):
  #      k = ekwipunek.Kufer(G,ekwipunek.AllItems())
 #       G.gracz.add_ekwipunek(k.zawartosc)
    #G.gracz.ruch(G.mapa,"4")"""
    G.graj(True)
