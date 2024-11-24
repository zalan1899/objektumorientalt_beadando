from abc import ABC, abstractmethod


class Jarat(ABC):
    def __init__(self, jaratszam, celallomas, jegyar):
        self.jaratszam = jaratszam
        self.celallomas = celallomas
        self.jegyar = jegyar
        self.foglalva = False  # Kezdetben a járat nincs lefoglalva

    @abstractmethod
    def informacio(self):
        pass


class BelfoldiJarat(Jarat):
    def informacio(self):
        return f"Belföldi járat: {self.jaratszam}, Célállomás: {self.celallomas}, Jegyár: {self.jegyar} Ft"


class NemzetkoziJarat(Jarat):
    def informacio(self):
        return f"Nemzetközi járat: {self.jaratszam}, Célállomás: {self.celallomas}, Jegyár: {self.jegyar} Ft"


class Légitársaság:
    def __init__(self, nev):
        self.nev = nev
        self.jaratok = []
        self.foglalasok = []

    def hozzaad_jaratot(self, jarat):
        self.jaratok.append(jarat)

    def foglalas(self, jarat_index):
        jarat = self.jaratok[jarat_index]
        if not jarat.foglalva:
            jarat.foglalva = True
            self.foglalasok.append(jarat)
            return jarat.jegyar
        else:
            raise Exception("A járat már le van foglalva!")

    def lemondas(self, jarat_index):
        if 0 <= jarat_index < len(self.foglalasok):
            jarat = self.foglalasok[jarat_index]
            jarat.foglalva = False
            del self.foglalasok[jarat_index]
        else:
            raise Exception("Érvénytelen foglalás index!")

    def listaz_foglalasok(self):
        return [jarat.informacio() for jarat in self.foglalasok]


class JegyFoglalasRendszer:
    def __init__(self):
        self.airline = Légitársaság("MALÉV")
        self.init_jaratok()

    def init_jaratok(self):
        # Hozzáadjuk az előre megadott járatokat
        self.airline.hozzaad_jaratot(BelfoldiJarat("ABC123", "Debrecen", 40000))
        self.airline.hozzaad_jaratot(BelfoldiJarat("DE456", "Pécs", 30000))
        self.airline.hozzaad_jaratot(NemzetkoziJarat("FG789", "Berlin", 70000))

        # Hozzáadunk 6 előre megadott foglalást
        self.airline.foglalas(0)
        self.airline.foglalas(1)
        self.airline.foglalas(2)

    def menu(self):
        while True:
            print("\n1. Jegy foglalása")
            print("2. Foglalás lemondása")
            print("3. Foglalások listázása")
            print("4. Kilépés")

            valasztas = input("Válasszon egy opciót: ")

            if valasztas == "1":
                for i, jarat in enumerate(self.airline.jaratok):
                    print(f"{i}. {jarat.informacio()}")
                jarat_index = int(input("Kérem, válasszon egy járat indexét a foglaláshoz: "))
                try:
                    ar = self.airline.foglalas(jarat_index)
                    print(f"Sikeres foglalás! A jegy ára: {ar} Ft")
                except Exception as e:
                    print(e)

            elif valasztas == "2":
                self.airline.listaz_foglalasok()
                jarat_index = int(input("Kérem, válasszon egy foglalás indexét a lemondáshoz: "))
                try:
                    self.airline.lemondas(jarat_index)
                    print("A foglalás sikeresen lemondva.")
                except Exception as e:
                    print(e)

            elif valasztas == "3":
                foglalasok = self.airline.listaz_foglalasok()
                if foglalasok:
                    print("Aktuális foglalások:")
                    for idx, info in enumerate(foglalasok):
                        print(f"{idx}. {info}")
                else:
                    print("Nincs aktív foglalás.")

            elif valasztas == "4":
                print("Kilépés a rendszerből.")
                break
            else:
                print("Érvénytelen opció! Kérlek próbáld újra.")


if __name__ == "__main__":
    rendszer = JegyFoglalasRendszer()
    rendszer.menu()