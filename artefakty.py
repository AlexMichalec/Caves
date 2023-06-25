import random

class Artefakty():
    def __init__(self):
        self.posiadane = []
        self.do_zdobycia = self.build_from_ENTRY()
        self.kategorie = {}
        for a in self.do_zdobycia:
            if a[1] in self.kategorie:
                self.kategorie[a[1]][0] += 1
                self.kategorie[a[1]].append(a[0])
            else:
                self.kategorie[a[1]] = [1,0, a[0]]

    def find(self):
        if len(self.do_zdobycia) == 0:
            return (0,0)
        temp = random.choice(self.do_zdobycia)
        self.do_zdobycia.remove(temp)
        self.posiadane.append(temp)
        self.kategorie[temp[1]][1] +=1
        return temp


    def build_from_ENTRY(self):
        temp = ENTRY.split("\n")
        r = ""
        tab = []
        for t in temp:
            if len(t) <= 3:
                continue
            if t[0] == " ":
                tab.append((t[1:], r))
                continue
            r = t
            if r[len(r) - 1] == ":":
                r = r[:-1]
        return tab




ENTRY = """
Kamienie szlachetne:
 Diament
 Szmaragd
 Rubin
 Szafir
 Topaz
 Jadeit
 Opal

Dzieła Sztuki:
 Upadła Madonna z Wielkim Cycem
 Le Pigeon Aux Petit Pois
 Sędziowie Sprawiedliwi
 Portret Młodzieńca
 Burza na jeziorze galilejskim
 

Nie-Do-Znalezienia:
 Perpetum Mobile
 Kwadratura Koła
 Sens Życia
 Kamień Filozoficzny
 Godność 
 
Skamieliny:
 Skamieniała wiewiórka
 Skamieniały Nos
 Skamieniałe Udko Kurczaka
 Skamieniałe Tofu

Kości:
 Kość dinozaura
 Kość Mamuta
 Kość niezgody
 Kość K12
 Kość, która została rzucona
 Czaszka neandertalczyka
 Kość ptaka, chyba

Księgi
 Biblia po Hiszpańsku
 Wiersze i Fraszki z XII wieku
 
Zabawki:
 Średniowieczne Dildo
 Mały Drewniany Piesek
 Grzechotka z kości

Różności:
 Fragment mozaiki
 Stare skarpety
 Poszukiwacz przygód nr 31201
 Koziołek Lednicki
 Fragment Bursztynowej Komnaty
 Połamany kijek

Bronie
 Kolczasta maczuga
 Hełm z rogami
 Łuk i trzy strzały
 Tarcza helleńska
 Eskalibur
 
Arki
 Arka Przymierza
 Arka Noego
 """
