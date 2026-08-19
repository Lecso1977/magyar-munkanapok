"""Constants for the Magyar munkanapok integration."""

DOMAIN = "magyar_munkanapok"
NAME = "Magyar munkanapok"

# Konfigurációs opciók kulcsai
CONF_CUSTOM_WORKDAYS = "custom_workdays"
CONF_CUSTOM_HOLIDAYS = "custom_holidays"

# Alapértelmezett beállítások
DEFAULT_NAME = "Magyar munkanapok"

# --- HIVATALOS FIX ÁLLAMI ÜNNEPNAPOK ---
FIX_HOLIDAYS = {
    (1, 1): "Újév",
    (3, 15): "Az 1848-as forradalom ünnepe",
    (5, 1): "A munka ünnepe",
    (8, 20): "Szent István napja (Államalapítás)",
    (10, 23): "Az 1956-os forradalom ünnepe",
    (11, 1): "Mindenszentek",
    (12, 25): "Karácsony első napja",
    (12, 26): "Karácsony másnapja",
}

# --- ÉVENTE VÁLTOZÓ ÉS ÁTHELYEZETT NAPOK (Kézzel frissítendő) ---
# Dátum formátum: "ÉÉÉÉ-HH-NN"
OFFICIAL_SHIFTED_WORKDAYS = {
    # Példa a fejlesztéshez:
    # "2026-05-09": "Áthelyezett munkanap",
}

OFFICIAL_SHIFTED_HOLIDAYS = {
    # Példa a fejlesztéshez:
    # "2026-12-24": "Áthelyezett pihenőnap",
}
