# Rendszerterv

## 1. A rendszer célja

A rendszer célja egy modern, felhasználóbarát online éttermi rendelőplatform létrehozása, amely lehetővé teszi a felhasználók számára az ételek böngészését, kiválasztását és online történő megrendelését.  
A rendszer támogatja az étterem dolgozóit is azáltal, hogy egyszerű és átlátható felületen kezelhetik a rendeléseket, az ételeket és a rendelés státuszokat.

### Amit a rendszer meg akar oldani
- Teljesen online rendelési folyamat biztosítása: regisztráció, bejelentkezés, kosárkezelés, rendelés leadása.
- Adminisztrációs felület biztosítása az étterem számára: rendelés kezelés, ételek szerkesztése, státuszfrissítés.
- AI alapú chatbot integrálása a felhasználói élmény javítására: ajánlások, gyakori kérdések megválaszolása.
- Valós idejű rendeléskövetés a felhasználók számára.

### Amit a rendszer **nem** csinál
- Nem kezeli offline rendeléseket (telefonon vagy személyesen leadott rendeléseket).
- Nem biztosít fizikai szállítási logisztikát vagy készletkezelést az étterem részére.
- Nem helyettesíti a teljes éttermi ügyviteli rendszert (pl. könyvelés, munkaidő-nyilvántartás).

## 2. Projekt terv

### 2.1. Projektszerepkörök, felelősségek
| Szerepkör | Felelősség |
|-----------|------------|
| Frontend UI/UX fejlesztő | HTML és CSS alapú felhasználói felületek tervezése és implementálása |
| Frontend JavaScript fejlesztő | JavaScript alapú interaktív funkciók fejlesztése, API hívások kezelése |
| Backend fejlesztő | Szerveroldali logika, API-k, adatfeldolgozás és üzleti logika megvalósítása |
| Adatbázis fejlesztő | Adatbázis tervezése, táblák létrehozása, kapcsolatok és lekérdezések biztosítása |

### 2.2. Projektmunkások és felelősségeik

| Név | Szerepkör | Főbb feladatok |
|-----|-----------|----------------|
| Kondor Kristóf | Frontend UI | Felhasználói felület HTML/CSS tervezése és implementációja |
| Nyiri László | Frontend JS | Kosárkezelés, rendelés leadás, interaktív UI elemek, AI chatbot integráció |
| Sebestyén Bence | Backend fejlesztő | API-k készítése, rendeléskezelés, felhasználói autentikáció, backend logika |
| Kacsó Melinda | Adatbázis | Adatbázis struktúra, táblák létrehozása, SQL lekérdezések, adatbiztonság |

## 3. Üzleti folyamatok modellje

### 3.1. Üzleti szereplők

| Szereplő | Leírás | Fő cél |
|-----------|---------|--------|
| **Felhasználó (vásárló)** | Regisztrált vagy vendégként böngésző látogató, aki ételeket keres és rendel. | Ételek kiválasztása és online rendelés leadása. |
| **Adminisztrátor / Étterem dolgozó** | Az étterem munkatársa, aki az online rendeléseket kezeli. | Rendelések megtekintése, státuszfrissítés, étlap karbantartása. |
| **Rendszer (backend)** | A központi szerver és adatbázis, amely a rendeléseket, felhasználókat és ételeket kezeli. | Adatok tárolása, API biztosítása, logika működtetése. |

---

### 3.2. Üzleti folyamatok

| Folyamat | Leírás | Szereplők | Eredmény |
|-----------|---------|------------|-----------|
| **Regisztráció / Bejelentkezés** | A felhasználó fiókot hoz létre, vagy meglévő adataival bejelentkezik. | Felhasználó, Rendszer | Személyes fiók létrejön vagy aktívvá válik. |
| **Étlap böngészése** | A felhasználó áttekinti a kínálatot, szűrhet és kereshet. | Felhasználó, Rendszer | A felhasználó megtalálja a kívánt ételeket. |
| **Kosárkezelés és rendelés leadása** | A felhasználó kosárba teszi az ételeket, majd leadja a rendelést. | Felhasználó, Rendszer | Új rendelés rögzítve az adatbázisban. |
| **Rendelés feldolgozása** | Az adminisztrátor látja az új rendelést, és frissíti annak státuszát (pl. „Elkészítés alatt”, „Kiszállítva”). | Adminisztrátor, Rendszer | A rendelés státusza frissül. |
| **Rendeléskövetés** | A felhasználó valós időben látja a rendelés aktuális állapotát. | Felhasználó, Rendszer | Felhasználó értesül a státuszváltozásról. |

---

### 3.3. Üzleti entitások

| Entitás | Leírás | Fő attribútumok |
|----------|----------|----------------|
| **Felhasználó** | Az alkalmazás regisztrált használója. | felhasználó_id, név, email, jelszó, cím |
| **Étel** | Az étterem által kínált termék. | étel_id, név, leírás, ár, kategória, kép_url |
| **Rendelés** | Egy felhasználó által leadott rendelés. | rendelés_id, felhasználó_id, dátum, összeg, státusz |
| **Rendelés_tétel** | Egy rendeléshez tartozó konkrét étel és mennyiség. | rendelés_tétel_id, rendelés_id, étel_id, mennyiség |


## 4. Követelmények

### 4.1. Funkcionális követelmények

A rendszer funkcionális követelményei azokra a működési képességekre vonatkoznak, amelyeket a felhasználók közvetlenül érzékelnek vagy használnak.

| Azonosító | Követelmény | Leírás |
|------------|--------------|--------|
| F1 | **Regisztráció és bejelentkezés** | A felhasználó létrehozhat fiókot vagy bejelentkezhet meglévő adataival. |
| F2 | **Felhasználói adatok kezelése** | A felhasználó módosíthatja profiladatait (név, cím, jelszó). |
| F3 | **Étlap böngészése** | A rendszer megjeleníti az étterem aktuális kínálatát kategóriák szerint. |
| F4 | **Keresés és szűrés** | A felhasználó név, ár vagy kategória alapján kereshet az ételek között. |
| F5 | **Kosárkezelés** | A felhasználó hozzáadhat, eltávolíthat vagy módosíthat tételeket a kosárban. |
| F6 | **Rendelés leadása** | A felhasználó megerősítheti a kosár tartalmát, és rendelést adhat le. |
| F7 | **Rendelés státusz megtekintése** | A felhasználó valós időben láthatja a rendelése állapotát. |
| F8 | **Adminisztrációs felület** | Az étterem dolgozói új ételeket vehetnek fel, rendeléseket kezelhetnek, státuszokat frissíthetnek. |

---

### 4.2. Nemfunkcionális követelmények

Ezek a követelmények a rendszer **minőségi jellemzőit** határozzák meg: teljesítmény, biztonság, használhatóság stb.

| Azonosító | Követelmény | Leírás |
|------------|--------------|--------|
| N1 | **Használhatóság** | A felhasználói felület legyen intuitív, reszponzív és könnyen kezelhető. |
| N2 | **Megbízhatóság** | A rendszer képes legyen hibatűrő működésre és adatvesztés elkerülésére. |
| N3 | **Teljesítmény** | A rendszer átlagos válaszideje ne haladja meg az 1 másodpercet API-hívások esetén. |
| N4 | **Biztonság** | Az adatok titkosítva legyenek (pl. jelszavak hash-elése, HTTPS kapcsolat). |
| N5 | **Skálázhatóság** | A rendszer képes legyen több felhasználót kiszolgálni párhuzamosan. |
| N6 | **Karbantarthatóság** | A kód legyen moduláris, jól dokumentált, könnyen bővíthető. |
| N7 | **Kompatibilitás** | A rendszer működjön modern böngészőkön (Chrome, Firefox, Edge, Safari). |
| N8 | **Elérhetőség** | A rendszer legalább 99% rendelkezésre állással működjön. |

---

## 5. Funkcionális terv
### 5.1. Rendszerszereplők
### 5.2. Rendszerhasználati esetek és lefutásaik
### 5.3. Határosztályok
### 5.4. Menü-hierarchiák
### 5.5. Képernyőtervek

## 6. Fizikai környezet
### 6.1. Vásárolt szoftverkomponensek és külső rendszerek
### 6.2. Hardver és hálózati topológia
### 6.3. Fizikai alrendszerek
### 6.4. Fejlesztő eszközök
### 6.5. Keretrendszer (pl. Spring)
Flask

## 7. Absztrakt domain modell
### 7.1. Domain specifikáció, fogalmak
### 7.2. Absztrakt komponensek, ezek kapcsolatai

## 8. Architekturális terv
### 8.1. Architekturális tervezési minta (pl. MVC, 3-rétegű alkalmazás, …)
### 8.2. Az alkalmazás rétegei, fő komponensei, ezek kapcsolatai
### 8.3. Változások kezelése
### 8.4. Rendszer bővíthetősége
### 8.5. Biztonsági funkciók

## 9. Adatbázis terv
### 9.1. Logikai adatmodell
### 9.2. Tárolt eljárások
### 9.3. Fizikai adatmodellt legeneráló SQL szkript

## 10. Implementációs terv
### 10.1. Perzisztencia-osztályok
### 10.2. Üzleti logika osztályai
### 10.3. Kliensoldal osztályai

## 11. Tesztterv

## 12. Telepítési terv

## 13. Karbantartási terv
