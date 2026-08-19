# Magyar munkanapok (Hungarian workdays)

![Magyar munkanapok](icon.png)

A **Magyar munkanapok** egy egyedi Home Assistant integráció, amellyel egyszerűen és megbízhatóan nyomon követheted a magyarországi munkanapokat, munkaszüneti napokat, fix és vándorló ünnepnapokat, valamint az áthelyezett munkanapokat.

---

## Fő jellemzők

* ⚙️ **Nincs YAML konfiguráció:** Teljesen a Home Assistant felhasználói felületén (UI) keresztül állítható be és kezelhető.
* ✝️ **Vándorló ünnepnapok automatikus számítása:** A Nagypéntek, Húsvéthétfő és Pünkösdhétfő pontos dátumát a rendszer automatikusan kiszámítja minden évre.
* 🇭🇺 **Beépített nemzeti ünnepek:** Tartalmazza az összes fix magyar állami ünnepnapot.
* ✏️ **Egyedi napok megadása megjegyzéssel:** Saját céges munkaszüneti napokat (pl. *Semmelweis-nap*) vagy egyedi munkanapokat is hozzáadhatsz egyszerű formátumban (`ÉÉÉÉ-HH-NN:Megjegyzés`).
* 🏷️ **Részletes attribútumok:** Az entitás `ok` attribútuma mindig pontosan kiírja, hogy az adott nap miért munkanap vagy pihenőnap (pl. *Március 15.*, *Hétvége*, *Egyedi munkanap*).

---

## Telepítés

### Telepítés HACS-on keresztül (Ajánlott)

1. Nyisd meg a **HACS**-ot a Home Assistantban.
2. A jobb felső sarokban válaszd az **Egyedi repók** menüpontot.
3. Add hozzá ezt a tárhelyet: `https://github.com/Lecso1977/magyar-munkanapok`
   * **Típus:** Integráció
4. Kattints a **Letöltés** gombra.
5. Indítsd újra a Home Assistantot.

### Beállítás

1. Menj a **Beállítások** $\rightarrow$ **Ezközök és szolgáltatások** menüpontba.
2. Kattints az **Integráció hozzáadása** gombra.
3. Keresd meg a **Magyar munkanapok** integrációt.
4. Kattints a hozzáadásra!

---

## Egyedi napok beállítása

Az integráció kártyáján a **Konfigurálás** gombra kattintva bármikor hozzáadhatsz saját napokat:

* **Formátum:** `ÉÉÉÉ-HH-NN` vagy `ÉÉÉÉ-HH-NN:Megjegyzés`
* **Példa egyedi munkaszüneti napra:** `2026-07-01:Semmelweis-nap`
* **Példa egyedi munkanapra:** `2026-08-08:Céges munkanap`

Több dátumot vesszővel vagy új sorral elválasztva is beírhatsz.

---

## Licenc

Ez a projekt az MIT licenc alatt áll.
