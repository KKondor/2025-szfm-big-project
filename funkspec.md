# Restaurant Webshop funkcionális specifikáció

## 1. Bevezetés
A dokumentum célja, hogy részletesen bemutassa a rendszer működését, funkcióit, felhasználói interakcióit és az adatáramlást.  
A leírás a fejlesztés alapjául szolgál, a követelményspecifikációban megfogalmazott igények alapján.

---

## 2. A rendszer célja

A rendszer célja egy modern, könnyen használható online éttermi rendelőplatform létrehozása, amely megkönnyíti a rendelési folyamatot mind a felhasználók, mind az étterem dolgozói számára.  
A webes alkalmazás lehetővé teszi az ételek böngészését, a kosárba helyezést és a rendelés leadását, miközben az adminisztrátorok kezelhetik a termékeket és a rendeléseket.  
A rendszer része egy AI alapú chatfelület is, amely segíti a felhasználót a rendelésben, információt ad az ételekről, és válaszol a gyakori kérdésekre.

---

## 3. Rendszeráttekintés
[Magas szintű leírás a rendszer fő komponenseiről és működéséről – például frontend, backend, adatbázis, külső szolgáltatások.]

**Fő modulok:**
- [Felhasználói modul]
- [Admin modul]
- [Adatkezelő modul]
- [Statisztikai vagy AI modul, ha van]

---

## 4. Rendszerszereplők
| Szereplő | Leírás |
|-----------|--------|
| [Felhasználó] | [Pl. böngészheti az adatokat, használhat funkciókat] |
| [Admin] | [Pl. adatokat kezelhet, módosíthat] |
| [Vendég] | [Pl. regisztráció nélkül megtekinthet bizonyos oldalakat] |

---

## 5. Rendszerhasználati esetek (Use Case-ek)

### 5.1 Használati esetek áttekintése
[Listázd a fő funkciókat, amelyeket a rendszernek teljesítenie kell.]

| ID | Név | Szereplő | Rövid leírás |
|----|-----|-----------|---------------|
| UC1 | Regisztráció | Felhasználó | Új fiók létrehozása |
| UC2 | Bejelentkezés | Felhasználó | Bejelentkezés a rendszerbe meglévő adatokkal |


### 5.2 Használati eset részletes leírása
#### UC1 – Regisztráció
- **Szereplő:** Felhasználó 
- **Cél:** Új fiók létrehozása
- **Előfeltétel:** Felhasználó nem rendelkezik regisztrált fiókkal, érvényes e-mail cím és jelszó rendelkezésre áll.
- **Lépések:**
  1. Felhasználó megnyitja a regisztrációs oldalt  
  2. Adatok megadása (név, e-mail, jelszó)  
  3. Backend validálja az adatokat
  4. Jelszó hash-elése, adatok mentése az adatbázisba
  5. Visszaigazolás a felhasználónak
- **Utófeltétel:** Felhasználó fiókja létrejön, be tud lépni a rendszerbe.
- **Alternatív folyamatok:**
  - Ha a megadott e-mail már regisztrált, hibaüzenet jelenik meg.  
  - Ha a jelszó nem elég erős, felhasználót figyelmezteti a rendszer.  
  - Hibás adatbevitel esetén a rendszer újra kéri a helyes adatokat.
 
#### UC2 – Bejelentkezés
- **Szereplő:** Felhasználó  
- **Cél:** A felhasználó bejelentkezik a rendszerbe.  
- **Előfeltétel:** A felhasználó korábban regisztrált, rendelkezik érvényes e-mail címmel és jelszóval.  
- **Lépések:**
  1. Felhasználó megnyitja a bejelentkezési oldalt  
  2. Megadja az e-mail címét és jelszavát  
  3. Backend ellenőrzi az adatokat az adatbázisban  
  4. Sikeres hitelesítés esetén a felhasználó átirányításra kerül a főoldalra
- **Utófeltétel:** A felhasználó be van jelentkezve, hozzáfér a saját fiókjához.  
- **Alternatív folyamatok:**  
  - Hibás e-mail vagy jelszó esetén hibaüzenet jelenik meg.  
  - Ha a backend nem elérhető, a rendszer értesíti a felhasználót.
---

## 6. Funkcionális követelmények
[A rendszer mit tudjon – részletesen funkciónként.]

| Azonosító | Funkció | Leírás | Prioritás |
|------------|----------|---------|------------|
| F1 | [Regisztráció] | [Felhasználó regisztrálhat új fiókot] | Magas |
| F2 | [Bejelentkezés] | [Felhasználó hitelesítése, token kezelése] | Magas |
| F3 | [Adatlekérés] | [Adatok megjelenítése a felhasználó számára] | Közepes |
| F4 | [Admin funkciók] | [Adatok szerkesztése, törlése] | Magas |

---

## 7. Nem-funkcionális követelmények
| Típus | Leírás |
|--------|--------|
| Teljesítmény | [Pl. válaszidő < 2 másodperc] |
| Biztonság | [Hash-elt jelszavak, HTTPS kommunikáció] |
| Megbízhatóság | [Rendszer működjön 99% rendelkezésre állással] |
| Felhasználói élmény | [Reszponzív, mobilbarát felület] |

---

## 8. Adatkezelés és adatáramlás
[Írd le, milyen adatokat kezel a rendszer, honnan jönnek, hová mennek.]

**Fő adatok:**
- [Felhasználói adatok]
- [Rendelések, bejegyzések stb.]
- [Logok, statisztikák]

**Adatáramlás:**
1. [Felhasználó kérés → Frontend → Backend → Adatbázis]
2. [Backend válasz → Frontend → Felhasználó megjelenítés]

---

## 9. Felhasználói felület (UI)
[Röviden írd le a fő oldalakat, képernyőket, és azok funkcióit.]

| Oldal | Leírás | Funkciók |
|--------|--------|-----------|
| Főoldal | [Rövid leírás] | [Gombok, linkek, űrlapok] |
| Admin oldal | [Leírás] | [CRUD műveletek] |
| Profil oldal | [Leírás] | [Felhasználói adatok kezelése] |

---

## 10. Hibakezelés és kivételek
- [Mit csinál a rendszer, ha hiba történik pl. adatbázis-hiba, üres input, 404, 500 stb.]  
- [Felhasználónak visszajelzés: pl. hibaüzenet megjelenítése.]  
- [Logolás a backend oldalon.]

---

## 11. Tesztelési javaslatok
- **Egységtesztek:** [Egyes funkciók működésének ellenőrzése]
- **Integrációs tesztek:** [Frontend–backend adatkapcsolat]
- **Felhasználói tesztek:** [Használhatósági és UX tesztelés]
- **Hibakezelés tesztelése:** [Hibás inputok és kivételes helyzetek vizsgálata]

---

## 12. Függőségek és feltételek
- [Milyen külső könyvtárakat, API-kat, adatbázist használ a rendszer.]
- [Pl. Flask, React, MySQL, OpenAI API stb.]

---

## 13. Korlátozások
- [Hardver vagy szoftver korlátozások]
- [Időkeret, projekt hatókörének korlátai]

---

## 14. Összefoglalás
A dokumentum meghatározza a rendszer működésének logikai alapját, a funkciókat, és a felhasználói interakciók részletes leírását, amelyek alapján a fejlesztés megkezdhető.
