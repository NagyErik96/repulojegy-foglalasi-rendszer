from abc import ABC, abstractmethod
from datetime import datetime
import random
import string


# ─────────────────────────────────────────────
#  Absztrakt alap: Járat
# ─────────────────────────────────────────────
class Jarat(ABC):
    def __init__(self, jaratszam: str, celallomas: str, jegyar: float):
        self.__jaratszam  = jaratszam
        self.__celallomas = celallomas
        self.__jegyar     = jegyar

    # ── getterek / setterek ──────────────────
    @property
    def jaratszam(self) -> str:
        return self.__jaratszam

    @property
    def celallomas(self) -> str:
        return self.__celallomas

    @property
    def jegyar(self) -> float:
        return self.__jegyar

    @jegyar.setter
    def jegyar(self, ertek: float):
        if ertek <= 0:
            raise ValueError("A jegyár csak pozitív szám lehet!")
        self.__jegyar = ertek

    @abstractmethod
    def jarat_tipus(self) -> str:
        pass

    def __str__(self) -> str:
        return (f"[{self.jarat_tipus()}] {self.__jaratszam} | "
                f"Cél: {self.__celallomas} | Ár: {self.__jegyar:.0f} Ft")


# ─────────────────────────────────────────────
#  BelföldiJarat
# ─────────────────────────────────────────────
class BelföldiJarat(Jarat):
    def __init__(self, jaratszam: str, celallomas: str, jegyar: float, repülési_idő_perc: int):
        super().__init__(jaratszam, celallomas, jegyar)
        self.__repülési_idő_perc = repülési_idő_perc

    @property
    def repülési_idő_perc(self) -> int:
        return self.__repülési_idő_perc

    def jarat_tipus(self) -> str:
        return "Belföldi"

    def __str__(self) -> str:
        return super().__str__() + f" | Repülési idő: {self.__repülési_idő_perc} perc"


# ─────────────────────────────────────────────
#  NemzetköziJarat
# ─────────────────────────────────────────────
class NemzetköziJarat(Jarat):
    def __init__(self, jaratszam: str, celallomas: str, jegyar: float, uticel_orszag: str):
        super().__init__(jaratszam, celallomas, jegyar)
        self.__uticel_orszag = uticel_orszag

    @property
    def uticel_orszag(self) -> str:
        return self.__uticel_orszag

    def jarat_tipus(self) -> str:
        return "Nemzetközi"

    def __str__(self) -> str:
        return super().__str__() + f" | Ország: {self.__uticel_orszag}"


# ─────────────────────────────────────────────
#  JegyFoglalás
# ─────────────────────────────────────────────
class JegyFoglalás:
    def __init__(self, utas_neve: str, jarat: Jarat, foglalás_dátuma: datetime):
        if not isinstance(jarat, Jarat):
            raise TypeError("Érvénytelen járat objektum!")
        if foglalás_dátuma > datetime.now():
            raise ValueError("A foglalás dátuma nem lehet jövőbeli időpont!")

        self.__foglalás_azonosító = self.__azonosito_generálás()
        self.__utas_neve          = utas_neve
        self.__jarat              = jarat
        self.__foglalás_dátuma    = foglalás_dátuma

    @staticmethod
    def __azonosito_generálás() -> str:
        return "FOG-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=6))

    # ── getterek ─────────────────────────────
    @property
    def foglalás_azonosító(self) -> str:
        return self.__foglalás_azonosító

    @property
    def utas_neve(self) -> str:
        return self.__utas_neve

    @property
    def jarat(self) -> Jarat:
        return self.__jarat

    @property
    def foglalás_dátuma(self) -> datetime:
        return self.__foglalás_dátuma

    def __str__(self) -> str:
        return (f"Azonosító: {self.__foglalás_azonosító} | "
                f"Utas: {self.__utas_neve} | "
                f"Járat: {self.__jarat.jaratszam} → {self.__jarat.celallomas} | "
                f"Ár: {self.__jarat.jegyar:.0f} Ft | "
                f"Foglalás dátuma: {self.__foglalás_dátuma.strftime('%Y-%m-%d %H:%M')}")


# ─────────────────────────────────────────────
#  LégiTársaság
# ─────────────────────────────────────────────
class LégiTársaság:
    def __init__(self, nev: str):
        self.__nev      = nev
        self.__jaratok  = []      # list[Jarat]
        self.__foglalasok = []    # list[JegyFoglalás]

    # ── getterek / setterek ──────────────────
    @property
    def nev(self) -> str:
        return self.__nev

    @nev.setter
    def nev(self, ertek: str):
        if not ertek.strip():
            raise ValueError("A légitársaság neve nem lehet üres!")
        self.__nev = ertek

    # ── Járat kezelés ────────────────────────
    def jarat_hozzaadasa(self, jarat: Jarat):
        if not isinstance(jarat, Jarat):
            raise TypeError("Csak Jarat típusú objektum adható hozzá!")
        # Egyedi járatszám ellenőrzés
        for j in self.__jaratok:
            if j.jaratszam == jarat.jaratszam:
                raise ValueError(f"A(z) {jarat.jaratszam} járatszám már létezik!")
        self.__jaratok.append(jarat)

    def jaratok_listazasa(self):
        if not self.__jaratok:
            print("  Nincsenek elérhető járatok.")
            return
        for jarat in self.__jaratok:
            print(f"  {jarat}")

    def jarat_keresese(self, jaratszam: str) -> Jarat:
        for jarat in self.__jaratok:
            if jarat.jaratszam == jaratszam:
                return jarat
        return None

    # ── Foglalás ─────────────────────────────
    def jegy_foglalasa(self, utas_neve: str, jaratszam: str) -> JegyFoglalás:
        if not utas_neve.strip():
            raise ValueError("Az utas neve nem lehet üres!")

        jarat = self.jarat_keresese(jaratszam)
        if jarat is None:
            raise ValueError(f"Nem létezik ilyen járat: {jaratszam}")

        foglalás = JegyFoglalás(utas_neve.strip(), jarat, datetime.now())
        self.__foglalasok.append(foglalás)
        return foglalás

    def foglalas_lemondasa(self, foglalás_azonosító: str) -> bool:
        for foglalas in self.__foglalasok:
            if foglalas.foglalás_azonosító == foglalás_azonosító:
                self.__foglalasok.remove(foglalas)
                return True
        raise ValueError(f"Nem található ilyen foglalás: {foglalás_azonosító}")

    def foglalasok_listazasa(self):
        if not self.__foglalasok:
            print("  Jelenleg nincsenek aktív foglalások.")
            return
        for foglalas in self.__foglalasok:
            print(f"  {foglalas}")


# ─────────────────────────────────────────────
#  Előre betöltött adatok
# ─────────────────────────────────────────────
def adatok_betöltése() -> LégiTársaság:
    legitarsasag = LégiTársaság("Magyar SkyLines")

    # 3 járat
    j1 = BelföldiJarat("MA101", "Debrecen",       15_000, 55)
    j2 = BelföldiJarat("MA202", "Pécs",            12_000, 45)
    j3 = NemzetköziJarat("MA303", "London Heathrow", 85_000, "Egyesült Királyság")

    for j in (j1, j2, j3):
        legitarsasag.jarat_hozzaadasa(j)

    # 6 előre betöltött foglalás
    elozetes = [
        ("Kovács Anna",   "MA101"),
        ("Nagy Béla",     "MA101"),
        ("Tóth Csilla",   "MA202"),
        ("Varga Dániel",  "MA202"),
        ("Horváth Éva",   "MA303"),
        ("Szabó Ferenc",  "MA303"),
    ]
    for nev, jszam in elozetes:
        legitarsasag.jegy_foglalasa(nev, jszam)

    return legitarsasag


# ─────────────────────────────────────────────
#  Menürendszer
# ─────────────────────────────────────────────
SZEPARATOR = "=" * 60

def fejlec(cim: str):
    print(f"\n{SZEPARATOR}")
    print(f"  {cim}")
    print(SZEPARATOR)


def menu(legitarsasag: LégiTársaság):
    while True:
        fejlec(f"✈  {legitarsasag.nev} – Foglalási Rendszer")
        print("  1) Elérhető járatok megtekintése")
        print("  2) Jegy foglalása")
        print("  3) Foglalás lemondása")
        print("  4) Összes foglalás listázása")
        print("  0) Kilépés")
        print(SZEPARATOR)

        valasztas = input("  Válasszon: ").strip()

        # ── 1: Járatok ────────────────────────
        if valasztas == "1":
            fejlec("Elérhető járatok")
            legitarsasag.jaratok_listazasa()

        # ── 2: Foglalás ───────────────────────
        elif valasztas == "2":
            fejlec("Jegy foglalása")
            legitarsasag.jaratok_listazasa()
            print()
            try:
                jaratszam = input("  Adja meg a járatszámot: ").strip().upper()
                utas_neve = input("  Adja meg az utas nevét: ").strip()
                foglalas  = legitarsasag.jegy_foglalasa(utas_neve, jaratszam)
                print(f"\n  ✔ Sikeres foglalás!")
                print(f"  Foglalás azonosítója: {foglalas.foglalás_azonosító}")
                print(f"  Fizetendő összeg:     {foglalas.jarat.jegyar:.0f} Ft")
            except ValueError as e:
                print(f"\n  ✘ Hiba: {e}")
            except TypeError as e:
                print(f"\n  ✘ Típushiba: {e}")

        # ── 3: Lemondás ───────────────────────
        elif valasztas == "3":
            fejlec("Foglalás lemondása")
            legitarsasag.foglalasok_listazasa()
            print()
            try:
                azonosito = input("  Adja meg a lemondandó foglalás azonosítóját: ").strip().upper()
                legitarsasag.foglalas_lemondasa(azonosito)
                print(f"\n  ✔ A(z) {azonosito} foglalás sikeresen lemondva.")
            except ValueError as e:
                print(f"\n  ✘ Hiba: {e}")

        # ── 4: Listázás ───────────────────────
        elif valasztas == "4":
            fejlec("Aktív foglalások")
            legitarsasag.foglalasok_listazasa()

        # ── 0: Kilépés ────────────────────────
        elif valasztas == "0":
            print("\n  Viszontlátásra! ✈\n")
            break

        else:
            print("\n  ✘ Érvénytelen választás, kérjük próbálja újra!")

        input("\n  [Enter] a folytatáshoz...")


# ─────────────────────────────────────────────
#  Belépési pont
# ─────────────────────────────────────────────
if __name__ == "__main__":
    legitarsasag = adatok_betöltése()
    menu(legitarsasag)
