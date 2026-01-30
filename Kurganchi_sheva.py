"""
Toshkent viloyati tumanlarida va asosan
Quyichirchiq tumani Qo'rg'oncha shaharchasida
og'zaki nutqda ishlatiladi.

Dastur fe'llarni rasmiy va sheva shakllarida
avtomatik ravishda tuslantirib beradi.
Tovush uyg'unligi qoidasi qo'shilgan.
"""

import pandas as pd
import os
from pathlib import Path

print(f"Joriy katalog: {os.getcwd()}")

def asosiy_formalar(ozak):
    """
    Fe'l uchun 2 xil asos hosil qiladi:
    - oddiy asos (bil, kel, bor)
    - a-li asos (bila, kela, bora)

    Args:
        ozak (str): Fe'l o'zagi

    Returns:
        dict: oddiy va a-li asoslar
    """

    # e, i, a bilan tugagan fe'llar: ye → yey, o'qi → o'qiy
    if ozak.endswith(("e", "i", "a")):
        return {
            "oddiy": ozak,
            "ali": ozak + "y"
        }

    # r, l bilan tugagan fe'llar: bor → bora, kel → kela
    if ozak.endswith(("r", "l")):
        return {
            "oddiy": ozak,
            "ali": ozak + "a"
        }

    # Qolgan barcha fe'llar: yoz → yoza
    return {
        "oddiy": ozak,
        "ali": ozak + "a"
    }

def tovush_uygunligini_aniqlash(ozak):
    """
    Sheva uchun tovush uyg'unligini aniqlaydi.
    -il, -er, -el, -ör, -et, -ir bilan tugasa → 'e'
    Boshqalari → 'a'

    Args:
        ozak (str): Fe'l o'zagi (sheva varianti)

    Returns:
        str: 'e' yoki 'a'
    """
    # -il, -er, -el, -ör, -et, -ir bilan tugovchi fe'llar
    if ozak.endswith(("il", "er", "el", "ör", "et", "ir")):
        return "e"
    return "a"

# Rasmiy shakllari uchun qoidalar (1-5 shaxslar)
RASMIY_QOIDALAR_1_5 = [
    ("ali", "man"),      # men bilaman
    ("ali", "san"),      # sen bilasan
    ("ali", "di"),       # u biladi
    ("ali", "miz"),      # biz bilamiz
    ("ali", "sizlar"),   # sizlar bilasizlar
]

def sheva_qoidalarini_hosil_qilish(unli):
    """
    Tovush uyg'unligiga qarab sheva qoidalarini hosil qiladi.

    Args:
        unli (str): 'e' yoki 'a'

    Returns:
        list: Sheva uchun qoidalar ro'yxati
    """
    return [
        ("oddiy", f"{unli}m"),         # men bilem / boram
        ("oddiy", f"{unli}sn"),        # sen bilesn / borasn
        ("oddiy", f"{unli}di"),        # u biledi / boradi
        ("oddiy", f"{unli}mz"),        # biz bilemz / boramz
        ("oddiy", f"{unli}sl{unli}r"), # sizlar esler / aslar (TO'G'RILANDI!)
        ("oddiy", f"ish{unli}di")      # ular bilishedi / borishadi
    ]

def felni_toldir_rasmiy(ozak):
    """
    Fe'l o'zagidan rasmiy shakllarni hosil qiladi.
    3-shaxs ko'plik uchun maxsus mantiq qo'llaniladi.

    Args:
        ozak (str): Fe'l o'zagi

    Returns:
        list: 6 ta shaxs-son shakli
    """
    asoslar = asosiy_formalar(ozak)

    # 1-5 shaxslar (oddiy qoida)
    natija = []
    for asos_turi, suffix in RASMIY_QOIDALAR_1_5:
        natija.append(asoslar[asos_turi] + suffix)

    # 3-shaxs ko'plik (maxsus mantiq)
    if ozak.endswith(("e", "i", "a")):
        # Unli bilan tugagan fe'llar
        if ozak in ["de", "ye"]:
            # de → deyishadi, ye → yeyishadi
            natija.append(asoslar["ali"] + "ishadi")
        else:
            # o'qi → o'qishadi, boshla → boshlashadi, so'ra → so'rashadi
            natija.append(ozak + "shadi")
    else:
        # Undosh bilan tugagan fe'llar: bil → bilishadi
        natija.append(ozak + "ishadi")

    return natija

def felni_toldir_sheva(ozak):
    """
    Fe'l o'zagidan sheva shakllarni hosil qiladi.

    QOIDA 1: Agar o'zak UNLI bilan tugasa (-a, -e, -i):
      - 1-5 shaxs: o'zak + y + m/sn/di/mz/sler
      - 3-shaxs ko'plik:
        * -a bilan tugasa: o'zak + shadi
        * -e bilan tugasa: o'zak + shedi
        * -i bilan tugasa: o'zak + shadi
        * MAXSUS di, ji: diyishedi, jiyishedi

    QOIDA 2: Agar o'zak UNDOSH bilan tugasa:
      - Tovush uyg'unligi: -il/-er/-el/-ör/-et/-ir → 'e', qolganlari → 'a'
      - 1-5 shaxs: o'zak + em/esn/edi/emz/esler yoki am/asn/adi/amz/aslar
      - 3-shaxs ko'plik: o'zak + ishedi yoki ishadi

    Args:
        ozak (str): Fe'l o'zagi (sheva varianti)

    Returns:
        list: 6 ta shaxs-son shakli
    """

    # QOIDA 1: Unli bilan tugagan fe'llar
    if ozak.endswith(("a", "e", "i")):
        # 1-5 shaxslar: o'zak + y + m/sn/di/mz/sler
        natija = [
            ozak + "ym",      # 1-sh birlik
            ozak + "ysn",     # 2-sh birlik
            ozak + "ydi",     # 3-sh birlik
            ozak + "ymz",     # 1-sh ko'plik
            ozak + "ysler",   # 2-sh ko'plik
        ]

        # 3-shaxs ko'plik (maxsus qoidalar)
        if ozak in ["di", "ji"]:
            # MAXSUS: di → diyishedi, ji → jiyishedi
            natija.append(ozak + "yishedi")
        elif ozak.endswith("a"):
            # -a bilan tugasa: shadi
            natija.append(ozak + "shadi")
        elif ozak.endswith("e"):
            # -e bilan tugasa: shedi
            natija.append(ozak + "shedi")
        elif ozak.endswith("i"):
            # -i bilan tugasa: shadi
            natija.append(ozak + "shadi")

        return natija

    # QOIDA 2: Undosh bilan tugagan fe'llar
    else:
        # Tovush uyg'unligini aniqlash
        unli = tovush_uygunligini_aniqlash(ozak)

        # Sheva qoidalarini hosil qilish
        sheva_qoidalar = sheva_qoidalarini_hosil_qilish(unli)

        # Shakllarni hosil qilish
        return [
            ozak + suffix
            for asos_turi, suffix in sheva_qoidalar
        ]

def main():
    """Asosiy dastur"""

    # Fayl mavjudligini tekshirish
    kirish_fayl = "fellar.xlsx"
    if not Path(kirish_fayl).exists():
        print(f"❌ Xato: '{kirish_fayl}' fayli topilmadi!")
        print(f"   Iltimos, joriy katalogda '{kirish_fayl}' faylini yarating.")
        return

    try:
        # Excel faylni o'qish
        df = pd.read_excel(kirish_fayl)

        # Kerakli ustunlar borligini tekshirish
        if "rasmiy" not in df.columns or "sheva" not in df.columns:
            print("❌ Xato: Excel faylda 'rasmiy' va 'sheva' ustunlari bo'lishi kerak!")
            return

        print(f"📖 '{kirish_fayl}' faylidan {len(df)} ta fe'l o'qildi.")

    except Exception as e:
        print(f"❌ Xato: Faylni o'qishda muammo: {e}")
        return

    # Natija qatorlarini tayyorlash
    natija_qatorlar = []

    for idx, row in df.iterrows():
        rasmiy = row["rasmiy"]
        sheva = row["sheva"]

        # Bo'sh qatorlarni o'tkazib yuborish
        if pd.isna(rasmiy) or pd.isna(sheva):
            continue

        rasmiy_shakllar = felni_toldir_rasmiy(rasmiy)
        sheva_shakllar = felni_toldir_sheva(sheva)

        natija_qatorlar.append(
            [rasmiy, sheva] + rasmiy_shakllar + sheva_shakllar
        )

    # Ustun nomlari
    ustunlar = (
        ["Rasmiy o'zak", "Sheva o'zak"] +
        ["1-sh birlik", "2-sh birlik", "3-sh birlik",
         "1-sh ko'plik", "2-sh ko'plik", "3-sh ko'plik"] +
        ["Sheva 1-sh birlik", "Sheva 2-sh birlik", "Sheva 3-sh birlik",
         "Sheva 1-sh ko'plik", "Sheva 2-sh ko'plik", "Sheva 3-sh ko'plik"]
    )

    # Yangi DataFrame yaratish
    out_df = pd.DataFrame(natija_qatorlar, columns=ustunlar)

    # Excel faylga yozish
    chiqish_fayl = "natija.xlsx"
    out_df.to_excel(chiqish_fayl, index=False)

    print(f"✅ Tayyor! {len(natija_qatorlar)} ta fe'l qayta ishlandi.")
    print(f"📄 Natija '{chiqish_fayl}' faylida saqlandi.")
    print(f"\n📊 Qoidalar:")
    print(f"   • Rasmiy 3-sh ko'plik: undosh+ishadi, unli+shadi (de, ye dan tashqari)")
    print(f"   • Sheva unli bilan tugasa: o'zak+ym/ysn/ydi/ymz/ysler, 3-sh: -a→shadi, -e→shedi, -i→shadi")
    print(f"   • Sheva undosh bilan tugasa: tovush uyg'unligi (-il/-er/-el/-ör/-et/-ir → 'e', qolganlari → 'a')")
    print(f"   • Sheva 2-sh ko'plik: esler/aslar (bir xil unli)")

if __name__ == "__main__":
    main()
