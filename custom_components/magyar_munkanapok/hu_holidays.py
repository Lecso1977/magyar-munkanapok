"""Hungarian holidays logic for Magyar munkanapok integration."""
from __future__ import annotations

from datetime import date


class HungarianHolidays:
    """Class to manage Hungarian official holidays and workday swaps."""

    def get_easter_sunday(self, year: int) -> date:
        """Húsvétvasárnap kiszámítása (Meeus/Jones/Butcher algoritmus)."""
        a = year % 19
        b = year // 100
        c = year % 100
        d = b // 4
        e = b % 4
        f = (b + 8) // 25
        g = (b - f + 1) // 3
        h = (19 * a + b - d - g + 15) % 30
        i = c // 4
        k = c % 4
        l = (32 + 2 * e + 2 * i - h - k) % 7
        m = (a + 11 * h + 22 * l) // 451
        month = (h + l - 7 * m + 114) // 31
        day = ((h + l - 7 * m + 114) % 31) + 1
        return date(year, month, day)

    def is_workday(self, check_date: date) -> bool:
        """Megadja, hogy az adott nap munkanap-e."""
        # Szombat (5) és Vasárnap (6) alapból hétvége
        if check_date.weekday() in (5, 6):
            return False

        # Állandó munkaszüneti napok
        year = check_date.year
        fixed_holidays = [
            date(year, 1, 1),    # Újév
            date(year, 3, 15),   # Nemzeti ünnep
            date(year, 5, 1),    # A munka ünnepe
            date(year, 8, 20),   # Államalapítás
            date(year, 10, 23),  # 1956-os forradalom
            date(year, 11, 1),   # Mindenszentek
            date(year, 12, 25),  # Karácsony 1. napja
            date(year, 12, 26),  # Karácsony 2. napja
        ]

        if check_date in fixed_holidays:
            return False

        # Mozgóünnepek (Húsvét, Pünkösd)
        easter_sunday = self.get_easter_sunday(year)
        good_friday = easter_sunday - date.resolution * 2
        easter_monday = easter_sunday + date.resolution * 1
        whit_monday = easter_sunday + date.resolution * 50

        movable_holidays = [good_friday, easter_monday, whit_monday]

        if check_date in movable_holidays:
            return False

        return True

    def get_holiday_name(self, check_date: date) -> str:
        """Visszaadja az ünnepnap nevét, ha az adott nap ünnep."""
        year = check_date.year
        fixed_names = {
            date(year, 1, 1): "Újév",
            date(year, 3, 15): "Nemzeti ünnep",
            date(year, 5, 1): "A munka ünnepe",
            date(year, 8, 20): "Szent István ünnepe",
            date(year, 10, 23): "1956-os forradalom",
            date(year, 11, 1): "Mindenszentek",
            date(year, 12, 25): "Karácsony",
            date(year, 12, 26): "Karácsony",
        }

        if check_date in fixed_names:
            return fixed_names[check_date]

        easter_sunday = self.get_easter_sunday(year)
        if check_date == easter_sunday - date.resolution * 2:
            return "Nagypéntek"
        if check_date == easter_sunday + date.resolution * 1:
            return "Húsvéthétfő"
        if check_date == easter_sunday + date.resolution * 50:
            return "Pünkösdhétfő"

        if check_date.weekday() in (5, 6):
            return "Hétvége"

        return ""
