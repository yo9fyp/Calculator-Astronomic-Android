import math
from datetime import datetime, timedelta

def calculeaza_eveniment_astronomic(an, tip):
    M = (an - 2000) / 1000.0

    coeficienti = {
        'primavara': (2451623.80984, 365242.37404,  0.05169, -0.00411, -0.00057),
        'vara':      (2451716.56767, 365241.62603,  0.00325,  0.00888, -0.00030),
        'toamna':    (2451810.21715, 365242.01767, -0.11575,  0.00337,  0.00078),
        'iarna':     (2451900.05952, 365242.74049, -0.06223, -0.00823,  0.00032)
    }

    c0, c1, c2, c3, c4 = coeficienti[tip]
    jde0 = c0 + c1 * M + c2 * (M ** 2) + c3 * (M ** 3) + c4 * (M ** 4)

    T = (jde0 - 2451545.0) / 36525.0
    W = 35999.373 * T - 2.47
    delta_lambda = 1 + 0.0334 * math.cos(math.radians(W)) + 0.0007 * math.cos(math.radians(2 * W))

    termeni = [
        (485, 324.96, 1934.136), (203, 337.23, 32964.467), (199, 342.08, 20.186),
        (182, 27.85, 445267.112), (156, 73.14, 45036.886), (136, 171.52, 22518.443),
        (77, 222.54, 65928.934), (74, 296.72, 3034.906), (70, 243.58, 9037.513),
        (58, 119.81, 33718.147), (52, 297.17, 150.678), (50, 21.02, 2281.226),
        (45, 247.54, 29929.562), (44, 325.15, 31555.956), (29, 60.93, 4443.417),
        (18, 155.12, 67555.328), (17, 288.79, 4562.452), (16, 198.04, 62894.029),
        (14, 199.76, 31436.921), (12, 95.39, 14577.848), (12, 287.11, 31931.756),
        (12, 320.81, 34777.259), (9, 227.73, 1222.114), (8, 15.45, 16859.074)
    ]

    S = sum(A * math.cos(math.radians(B + C * T)) for A, B, C in termeni)
    jde = jde0 + (0.00001 * S) / delta_lambda

    t_sec = (an - 2000) / 100.0
    delta_t = 62.92 + 32.217 * t_sec + 55.89 * (t_sec ** 2)
    jd_utc = jde - (delta_t / 86400.0)

    zile_de_la_2000 = jd_utc - 2451545.0
    data_utc = datetime(2000, 1, 1, 12, 0, 0) + timedelta(days=zile_de_la_2000)

    if tip in ['vara', 'toamna']:
        fus_orar = 3
        eticheta_ora = "EEST / Ora de vară"
    else:
        fus_orar = 2
        eticheta_ora = "EET / Ora de iarnă"

    data_romania = data_utc + timedelta(hours=fus_orar)
    return data_romania, eticheta_ora

def formateaza_data_ro(dt):
    zile_ro = ["Luni", "Marți", "Miercuri", "Joi", "Vineri", "Sâmbătă", "Duminică"]
    luni_ro = {
        1: "Ianuarie", 2: "Februarie", 3: "Martie", 4: "Aprilie",
        5: "Mai", 6: "Iunie", 7: "Iulie", 8: "August",
        9: "Septembrie", 10: "Octombrie", 11: "Noiembrie", 12: "Decembrie"
    }
    zi_sapt = zile_ro[dt.weekday()]
    return f"{zi_sapt}, {dt.day:02d} {luni_ro[dt.month]} {dt.year}, ora {dt.strftime('%H:%M:%S')}"

