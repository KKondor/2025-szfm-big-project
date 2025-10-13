# Restaurant Webshop funkcionális specifikáció

## 1. Bevezetés
A dokumentum célja, hogy részletesen bemutassa a rendszer működését, funkcióit, felhasználói interakcióit és az adatáramlást.  
A leírás a fejlesztés alapjául szolgál, a követelményspecifikációban megfogalmazott igények alapján.

---

## 2.1 Jelenlegi helyzet leírása
Az étterem rendeléseit jelenleg telefonon és személyesen fogadják.  
A folyamat papíron történik, ami lassú, hibalehetőségekkel jár és nem átlátható.  
Nincs egységes digitális rendszer a rendelések és a felhasználói adatok nyilvántartására.

## 2.2 Vágyálomrendszer

A rendszer célja egy modern, könnyen használható online éttermi rendelőplatform létrehozása, amely megkönnyíti a rendelési folyamatot mind a felhasználók, mind az étterem dolgozói számára.  
A webes alkalmazás lehetővé teszi az ételek böngészését, a kosárba helyezést és a rendelés leadását, miközben az adminisztrátorok kezelhetik a termékeket és a rendeléseket.  
A rendszer része egy AI alapú chatfelület is, amely segíti a felhasználót a rendelésben, információt ad az ételekről, és válaszol a gyakori kérdésekre.

---

## 3.1 Jelenlegi üzleti folyamatok modellje
Az étterem jelenleg manuálisan kezeli a rendeléseket.  
A vendégek telefonon vagy személyesen adják le rendelésüket, amelyet az alkalmazottak kézzel rögzítenek.  
A folyamat során gyakoriak a félreértések, hibás adatok és késedelmek, mivel nincs központi digitális rendszer a rendelési adatok tárolására és kezelésére.  
A rendelések státuszának követése nehézkes, a visszajelzések pedig csak szóban vagy telefonon történnek.

## 3.2 Igényelt üzleti folyamatok modellje
A fejlesztendő rendszer célja, hogy a rendelési folyamat teljesen online, automatizált módon működjön.  

**Folyamatleírás:**
1. A felhasználó regisztrál és bejelentkezik a webalkalmazásba.  
2. A menüoldalon böngészi az ételeket, majd a kiválasztott tételeket a kosárba helyezi.  
3. A kosárban ellenőrzi és véglegesíti a rendelést.  
4. A backend rendszer eltárolja a rendelést és kiszámolja a végösszeget.  
5. Az adminisztrátor a kezelőfelületen megtekinti az új rendeléseket és módosíthatja azok státuszát (pl. „Folyamatban”, „Kiszállítva”).  
6. A felhasználó a profiloldalán követheti a rendelése státuszát, és AI chatbot segítségével kérhet információt vagy ajánlást.

Ez a folyamat gyorsabb, pontosabb és átláthatóbb rendeléskezelést biztosít mindkét fél számára.

---

## 4. Rendszerhasználati esetek (Use Case-ek)

### 4.1 Használati esetek áttekintése
[Listázd a fő funkciókat, amelyeket a rendszernek teljesítenie kell.]

| ID | Név | Szereplő | Rövid leírás |
|----|-----|-----------|---------------|
| UC1 | Regisztráció | Felhasználó | Új fiók létrehozása |
| UC2 | Bejelentkezés | Felhasználó | Bejelentkezés a rendszerbe meglévő adatokkal |


### 4.2 Használati eset részletes leírása
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

## 5. Funkcionális követelmények
[A rendszer mit tudjon – részletesen funkciónként.]

| Azonosító | Funkció | Leírás | Prioritás |
|------------|----------|---------|------------|
| F1 | [Regisztráció] | [Felhasználó regisztrálhat új fiókot] | Magas |
| F2 | [Bejelentkezés] | [Felhasználó hitelesítése, token kezelése] | Magas |
| F3 | [Adatlekérés] | [Adatok megjelenítése a felhasználó számára] | Közepes |
| F4 | [Admin funkciók] | [Adatok szerkesztése, törlése] | Magas |

---

## 6. Nem-funkcionális követelmények
| Típus | Leírás |
|--------|--------|
| Teljesítmény | [Pl. válaszidő < 2 másodperc] |
| Biztonság | [Hash-elt jelszavak, HTTPS kommunikáció] |
| Megbízhatóság | [Rendszer működjön 99% rendelkezésre állással] |
| Felhasználói élmény | [Reszponzív, mobilbarát felület] |

---

## 7. Funkció – követelmény megfeleltetés
| Funkció | Kapcsolódó követelmény |
|----------|-----------------------|
| Regisztráció | Felhasználói fiók létrehozása (K1) |
| Bejelentkezés | Felhasználói azonosítás (K2) |

## 8. Felhasználói felület (UI)
[Röviden írd le a fő oldalakat, képernyőket, és azok funkcióit.]

| Oldal | Leírás | Funkciók |
|--------|--------|-----------|
| Főoldal | [Rövid leírás] | [Gombok, linkek, űrlapok] |
| Admin oldal | [Leírás] | [CRUD műveletek] |
| Profil oldal | [Leírás] | [Felhasználói adatok kezelése] |

---

## 9. Hibakezelés és kivételek
- [Mit csinál a rendszer, ha hiba történik pl. adatbázis-hiba, üres input, 404, 500 stb.]  
- [Felhasználónak visszajelzés: pl. hibaüzenet megjelenítése.]  
- [Logolás a backend oldalon.]

---

## 10. Tesztelési javaslatok
- **Egységtesztek:** [Egyes funkciók működésének ellenőrzése]
- **Integrációs tesztek:** [Frontend–backend adatkapcsolat]
- **Felhasználói tesztek:** [Használhatósági és UX tesztelés]
- **Hibakezelés tesztelése:** [Hibás inputok és kivételes helyzetek vizsgálata]

---

## 11. Függőségek és feltételek
- [Milyen külső könyvtárakat, API-kat, adatbázist használ a rendszer.]
- Backend: Python Flask keretrendszer használatával, pytest a teszteléshez

---

## 12. Összefoglalás
A dokumentum meghatározza a rendszer működésének logikai alapját, a funkciókat, és a felhasználói interakciók részletes leírását, amelyek alapján a fejlesztés megkezdhető.
