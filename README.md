# ✈ Repülőjegy Foglalási Rendszer

Objektumorientált programozás – kötelező project feladat  
Nyelv: **Python 3.8+**

---

## Futtatás

```bash
python repulojegy_rendszer.py
```

Nincs külső függőség, csak a Python standard könyvtár szükséges.

---

## Osztálystruktúra

```
Jarat (ABC – absztrakt)
├── BelföldiJarat
└── NemzetköziJarat

LégiTársaság
└── tartalmaz: Jarat[], JegyFoglalás[]

JegyFoglalás
└── hivatkozik: Jarat
```

### Főbb osztályok

| Osztály | Leírás |
|---|---|
| `Jarat` | Absztrakt alap – járatszám, célállomás, jegyár |
| `BelföldiJarat` | Belföldi járat + repülési idő percben |
| `NemzetköziJarat` | Nemzetközi járat + célország |
| `JegyFoglalás` | Egy utas egy járatra szóló foglalása |
| `LégiTársaság` | Járatok és foglalások kezelése |

---

## Funkciók

- **Jegy foglalása** – járatszám és utas neve alapján, visszaadja az árat és az azonosítót  
- **Foglalás lemondása** – azonosító alapján törli a foglalást  
- **Foglalások listázása** – az összes aktív foglalás megjelenítése  
- **Járatok listázása** – elérhető járatok típussal, árral, részletekkel  

---

## Előre betöltött adatok

Induláskor automatikusan betöltődik:

- **1 légitársaság**: Magyar SkyLines  
- **3 járat**: MA101 (Debrecen), MA202 (Pécs), MA303 (London)  
- **6 foglalás**: 2 foglalás minden járatra  

---

## OOP elvek alkalmazása

- **Absztrakt osztály** (`ABC`, `@abstractmethod`) – `Jarat`  
- **Öröklés** – `BelföldiJarat`, `NemzetköziJarat`  
- **Egységbezárás** – minden attribútum `private` (`__`), getter/setter `@property`  
- **Hibakezelés** – `ValueError`, `TypeError` kivételek  
- **Adatvalidáció** – üres név, nem létező járat, duplikált járatszám ellenőrzése  
