# Restaurant Webshop követelményspecifikáció

## 1. Jelenlegi helyzet
Jelenleg az étterem nem rendelkezik online rendelési felülettel. A rendeléseket telefonon vagy személyesen veszik fel, ami lassú, hibalehetőségekkel teli folyamat. Nincs egységes rendszer az ételek megjelenítésére, a rendelés nyomon követésére vagy az adminisztrációra. A cél egy modern, online rendelőplatform létrehozása, amely egyszerűsíti a rendelési folyamatot mind a vendégek, mind az étterem személyzete számára.

## 2. Vágyálom rendszer
A cél egy letisztult, gyors és könnyen kezelhető online éttermi rendelőfelület létrehozása.
A felhasználók egyszerűen böngészhetik a menüt, kosárba tehetik az ételeket, és leadhatják rendelésüket regisztráció után.
Az adminisztrátorok kezelhetik a termékeket és a beérkezett rendeléseket, míg egy integrált AI chatbot segíti a felhasználókat a rendelésben és az információk megválaszolásában.

## 3. Jelenlegi üzleti folyamatok
A fejlesztés előtt nincs formalizált üzleti folyamat.
A rendeléseket jelenleg manuálisan kezelik.

## 4. Igényelt üzleti feladatok

### 4.1 Felhasználói felület
A rendszer több fő oldalt tartalmaz:  

- **Bejelentkezés / Regisztráció oldal:**  
  A felhasználók új fiókot hozhatnak létre vagy bejelentkezhetnek meglévő adataikkal.  

- **Menü oldal:**  
  Az ételek listázva jelennek meg képpel, névvel, leírással és árral. A felhasználó az ételeket kosárba teheti.  

- **Kosár oldal:**  
  A felhasználó megtekintheti a kosarában lévő tételeket, módosíthatja a mennyiséget, és leadhatja a rendelést.  

- **AI Chat oldal:**  
  Egy beépített chatbot segít a rendelésben, válaszol a gyakori kérdésekre és javaslatot ad ételekre.  

### 4.2 Backend logika
#### **Főbb feladatok és funkciók**
1. **Autentikáció és jogosultságkezelés**
   - Regisztráció (jelszó hash-eléssel)
   - Bejelentkezés
   - Jogosultság-szintek kezelése (felhasználó / admin)
2. **Adatkezelés és API réteg**
   - RESTful API biztosítja a kapcsolatot a frontend és az adatbázis között  
   - CRUD műveletek az entitásokon
   - Minden adat JSON formátumban kerül küldésre/visszaadásra
3. **Rendeléskezelési logika**
   - Kosár tartalmának mentése rendelésként  
   - Teljes ár kiszámítása
   - Rendelés státuszainak kezelése
   - Admin jogosult módosítani a rendelés státuszát
5. **Hibakezelés és biztonság**
   - Minden végpont validálja a bemenő adatokat  
   - Hibák JSON formátumban kerülnek visszaadásra
   - Adatbázis-lekérdezések biztonságos formában történnek
6. **AI Chat modul integráció**
   - Chat kezelése backend oldalon  
   - API használata válaszgeneráláshoz  
   - Ételajánlás az adatbázis adatai alapján

## 5. A rendszerre vonatkozó szabványok és ajánlások
- **Adatbiztonság:** jelszavak biztonságos (hash-elt) tárolása
- **Webes szabványok:** W3C HTML5, CSS3 és ECMAScript szabványok betartása  
- **REST API ajánlások:** JSON formátum, HTTP státuszkódok konzisztens használata

## 6. Követelménylista
- Reszponzív dizájn
- Egyszerű, letisztult és konzisztens UI
- Felhasználói regisztráció és bejelentkezés  
- Menü megjelenítése 
- Ételek kosárba helyezése és rendelés leadása  
- Rendelések megtekintése 
- Admin termék- és rendeléskezelés  
- AI chat funkció

## 7. Fogalomszótár
| Fogalom | Jelentés |
|----------|-----------|
| [Fogalom] | [Definíció] |
| [Fogalom] | [Definíció] |
