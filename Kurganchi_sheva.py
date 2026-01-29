"""Toshkent viloyati tumanlarida va asosan
Quyichirchiq tumani Qo‘rg‘oncha shaharchasida
og‘zaki nutqda ishlatiladi."""

import pandas as pd
import os
print(os.getcwd())

def asosiy_formalar(ozak):
    """Fe'l uchun 2xil asos:     - oddiy asos (bil, kel, bor),     - a-li asos (bila, kela, bora)"""
    # maxsus fe'l: ye → yey
    if ozak == "ye":
        return {
            "oddiy": "yey",
            "ali": "yey"
        }

    if ozak.endswith(("r", "l")):
        return{
            "oddiy": ozak,
            "ali": ozak + "a"
        }

    return {
        "oddiy": ozak,
        "ali": ozak
    }

QOIDALAR = {
    "rasmiy": [
        ("ali", "man"),
        ("ali", "san"),
        ("ali", "di"),
        ("ali", "miz"),
        ("ali", "sizlar"),
        ("oddiy", "ishadi"), # muhim joy ekan
        ],
    "sheva": [
        ("oddiy", "em"),
        ("oddiy", "esn"),
        ("oddiy", "edi"),
        ("oddiy", "emz"),
        ("oddiy", "esler"),
        ("oddiy", "ishedi")
    ]
}
def felni_toldir(ozak, tur="rasmiy"):
    asoslar = asosiy_formalar(ozak)
    qoidalar = QOIDALAR[tur]

    return [
        asoslar[asos_turi]+suffix
        for asos_turi, suffix in qoidalar
    ]

# Excelni o'qish
df = pd.read_excel("fellar.xlsx")

natija_qatorlar = []

for _, row in df.iterrows():
    rasmiy = row["rasmiy"]
    sheva = row["sheva"]

    rasmiy_shakllar = felni_toldir(rasmiy, 'rasmiy')
    sheva_shakllar = felni_toldir(sheva, "sheva")

    natija_qatorlar.append(
        [rasmiy, sheva] + rasmiy_shakllar + sheva_shakllar
    )

# ustun nomlari
ustunlar = (
    ["rasmiy", "sheva"] +
    ["1-shaxs birlik", "2-shaxs birlik", "3-shaxs birlik", "1-shaxs ko'plik", "2-shaxs ko'plik", "3-shaxs ko'plik"] +
    ["sheva 1-shaxs birlik", "sheva 2-shaxs birlik", "sheva 3-shaxs birlik", "sheva 1-shaxs ko'plik", "sheva 2-shaxs ko'plik", "sheva 3-shaxs ko'plik"]
)
# yangi dataframe
out_df = pd.DataFrame(natija_qatorlar, columns=ustunlar)

#  Excelga yozish
out_df.to_excel("natija.xlsx", index=False)

print("✅ Excel tayyor: natija.xlsx")




# # # fellar = ["bil", "kel", "bor", "ye"]
# # #
# # # for f in fellar:
# # #     print("RASMIY:", f," → ", felni_toldir(f, "rasmiy"))
# # #     print("SHEVA:", f," → ", felni_toldir(f, "sheva"))


