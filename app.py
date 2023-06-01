from math import log, ceil
from tabulate import tabulate

m_facilities = float(input(('Производительность установки по сырью, кг/ год: ')))
print('Пределы выкипания, °C')
n_k = float(input('Н.К.: '))
k_k = float(input('К.К.: '))
sod_seri_t_ch = float(input('Содержание серы, % масс., в т.ч: '))
seri_merkaptan = float(input('Меркаптановой: '))
seri_sulfid = float(input('Сульфидной: '))
seri_disulfid = float(input('Дисульфидной: '))
seri_tiofen = float(input('Тиофеновой: '))
p20_4 = float(input('Относительная плотность при 20 °C ,г/см3: '))
ost_sod_seri = float(input('Остаточное содержание серы, % масс:'))

p = float(input('Давление, МПа: '))
t_c = float(input('Температура, °C'))
w = float(input('Объёмная скорость подачи сырья, ч–1: '))
xi = float(input('Кратность циркуляции ВСГ к сырью, нм3/м3: '))

print('Содержание ароматических углеводородов, % масс.')
A_0 = float(input('Сырьё: '))
A_K = float(input('Гидрогенизат: '))

# CONSTANTS
G3 = 0.222
x_h2 = 0.024
y_h2 = 0.72
G = 118.78
q_a = 214
q_h = 126
C_h = 10
delta_A = A_0 - A_K
t_0 = 350
tepl_merkaptan = 2100
tepl_sulfid = 3500
tepl_disulfid = 5060
tepl_tiofen = 8700
z_c = 0.2
n = 1
M_g = 7.2
ee = 0.504
uu = 2 * (10 ** -5)
u = 0.191
d = 2.5
g = 9.81
M_c = 7.6

# Таблица 2.4
m_H2 = 29.4
m_CH4 = 19.4
m_C2H6 = 26
m_C3H8 = 15.2
m_C4H10 = 10

# Таблица 2.6 Состав ЦВСГ
m_y_H2 = 0.192
m_y_CH4 = 0.427
m_y_C2H6 = 0.201
m_y_C3H8 = 0.103
m_y_C4H10 = 0.077

# Таблица 2.10 Теплоёмкость индивидуальных компонентов
tepl_H2 = 14.57
tepl_CH4 = 3.35
tepl_C2H6 = 3.29
tepl_C3H8 = 3.23
tepl_C4H10 = 3.18

S = sod_seri_t_ch - ost_sod_seri
vixod_benzina = sod_seri_t_ch - ost_sod_seri
vixod_gaza = 0.3 * vixod_benzina

# ----------------
vixod_gidro_diesel = 100 - vixod_benzina - vixod_gaza - S
# ----------------

m_merkaptan = 0.062
m_sulfid = 0.125
m_disulfid = 0.0938
m_tiofen = 0.25

G1 = m_merkaptan * seri_merkaptan + m_sulfid * seri_sulfid + m_disulfid * seri_disulfid + (
        seri_tiofen - ost_sod_seri) * m_tiofen

p15_15 = 0.994 * (p20_4 / 1000) + 0.0093
t_sr = (n_k + k_k) / 2
K = (1.216 * ((t_sr + 273) ** (1 / 3))) / p15_15
M = 7 * K - 21.5 + (0.76 - 0.04 * K) * t_sr + (0.0003 * K - 0.00245) * (t_sr ** 2)

G2 = 2 * 9 / M

N_A = (M * (A_0 - A_K)) / 13600
V_A = (m_facilities * (1000 / M)) * N_A

G4 = (x_h2 * 2 * 100) / (x_h2 * 2 + (1 - x_h2) * M)

G5 = (xi * 0.01 * 2 * 100) / (p20_4 * 22.4)

G_h2 = G1 + G2 + G3 + G4 + G5 + 0.3

G_C = (100 * xi * M_c) / (p20_4 * 22.4)

B_H2S = S * (34 / 32)
G_H2S = B_H2S - S
G_prod = G1 + G2 + G3 - G_H2S

vixod_gidro_diesel_utoch = vixod_gidro_diesel + G_prod

G_0_H2 = G_h2 / 0.294

V_sux_gaz = G_0_H2 * (1 - 0.294) + vixod_gaza + G4

C_c = tepl_H2 * m_y_H2 + tepl_CH4 * m_y_CH4 + tepl_C2H6 * m_y_C2H6 + tepl_C3H8 * m_y_C3H8 + tepl_C4H10 * m_y_C4H10

I_p = (129.58 + 0.134 * (t_0 + 273) + 0.00059 * (t_0 + 273) ** 2) * (4 - p15_15) - 308.99
t_kr = 10 ** (0.634 * log(t_sr + 273, 10) + 1.214) - 150
t_pr = (t_0 + 273) / t_kr
p_kr = 0.1 * K * (t_kr / M)
p_pr = p / p_kr
delta_I = (4.4 * p_pr * t_kr) / ((t_pr ** 3) * M)
I_350_c = I_p - delta_I
G_c = I_350_c / (t_0 + 273)
c_l = (G_c * 100 + C_c * (G - 100)) / G
q_s = seri_merkaptan * tepl_merkaptan + seri_sulfid * tepl_sulfid + seri_disulfid * tepl_disulfid + seri_tiofen * tepl_tiofen

# -----------------------
t = ((t_0 + (S * q_s + C_h * q_h + delta_A * q_a)) / G) * c_l
# -----------------------


G_rasxod = 238095.24

t_sr_vixod_t_c = (t_c + t) / 2
# ---------------
V_c = (G_rasxod * 22.4 * z_c * 0.1 * (t_sr_vixod_t_c + 273)) / (M * p * 273)
# ---------------


V_kat = G_rasxod / (p20_4 * w * n)

# -----------------
D_p = ceil(((2 * V_kat) / 3.14) ** (1 / 3))
# ----------------

fresh_vsg = m_facilities / 34500 * (G_0_H2 + 0.1) / 24 * 1000
cvsg = m_facilities / 34500 * (G_c + 0.1) / 24 * 1000
smes = fresh_vsg + cvsg
V_g = (smes * 22.4 * 0.1 * 1.0 * (t_sr_vixod_t_c + 273)) / (M_g * p * 273)
V_sm = V_c + V_g
U = (4 * V_sm) / (3600 * 3.14 * (D_p ** 2))
F = V_sm / (U * 3600)

# ----------------------
h_kat = V_kat / F
# ----------------------

# ------------
h_cycle = (3 * h_kat) / 2
# ------------

# ------------
H = h_cycle + D_p
# ------------

checki = (150 * ((1 - ee) ** 2) * uu * (u ** 2)) / ((ee ** 3) * ((d * (10 ** -3)) ** 2) * g)
checki2 = (1.75 * (1 - ee) * 32.8 * (u ** 2)) / ((ee ** 3) * ((d * (10 ** -3)) ** 2) * g)

# ------------
delta_P = (checki + checki2) * h_kat
# ------------

V_g_r = 70.3 * 550 * 0.085 * 307.78 * (22.4 / 28)
N_c = (xi * (m_facilities / 345 / 24 * 1000)) / p20_4

# -------
t_itog = V_g_r / N_c
# -------

print("Вдт: " + str(vixod_gidro_diesel))
print('Общий расход водорода: ' + str(G_h2))
print('ВдтУточ: ' + str(vixod_gidro_diesel_utoch))
print('Выход сухого газа: ' + str(V_sux_gaz))
# таблица 2.7 и 2.9
# таблица 2.7
print(
    '-------------------------------------------------Материальный баланс ГИДРООЧИСТКИ-------------------------------------------------')
table_27 = [
    ['Взято: '],
    ['Дизельная фракция', 100, m_facilities, m_facilities / 345,
     m_facilities / 345 / 24 * 1000],
    ['Водородсодержащий газ', G_0_H2, m_facilities / 100 * (G_0_H2 + 0.1),
     m_facilities / 34500 * (G_0_H2 + 0.1), m_facilities / 34500 * (G_0_H2 + 0.1) / 24 * 1000],
    ['в т.ч. 100% водорода', G_h2, m_facilities / 100 * G_h2, m_facilities / 34500 * G_h2,
     m_facilities / 34500 * G_h2 / 24 * 1000],
    ['Сумма:', 100 + G_0_H2, m_facilities + m_facilities / 100 * (G_0_H2 + 0.1),
     m_facilities / 345 + m_facilities / 34500 * (G_0_H2 + 0.1),
     m_facilities / 345 / 24 * 1000 + m_facilities / 34500 * (G_0_H2 + 0.1) / 24 * 1000],
    ['Получено: '],
    ['Дизельное топливо', vixod_gidro_diesel_utoch,
     m_facilities / 100 * vixod_gidro_diesel_utoch,
     m_facilities * vixod_gidro_diesel_utoch / 34500,
     m_facilities * vixod_gidro_diesel_utoch / 34500 / 24 * 1000],
    ['Сероводород', G_H2S, m_facilities / 100 * G_H2S, m_facilities / 34500 * G_H2S,
     m_facilities / 34500 * G_H2S / 24 * 1000],
    ['Сухой газ** + потери',
     V_sux_gaz + vixod_gidro_diesel_utoch + G_H2S + vixod_benzina - 100,
     m_facilities / 100 * (V_sux_gaz + vixod_gidro_diesel_utoch + G_H2S + vixod_benzina - 100),
     m_facilities / 34500 * (
                 V_sux_gaz + vixod_gidro_diesel_utoch + G_H2S + vixod_benzina - 100),
     m_facilities / 34500 * (
                 V_sux_gaz + vixod_gidro_diesel_utoch + G_H2S + vixod_benzina - 100) / 24 * 1000],
    ['Бензин', vixod_benzina, m_facilities / 100 * vixod_benzina,
     m_facilities / 34500 * vixod_benzina, m_facilities / 34500 * vixod_benzina / 24 * 1000],
    ['Сумма:',
     vixod_gidro_diesel_utoch + G_H2S + vixod_benzina + V_sux_gaz + vixod_gidro_diesel_utoch + G_H2S + vixod_benzina - 100,
     m_facilities / 100 * vixod_gidro_diesel_utoch + m_facilities / 100 * G_H2S + m_facilities / 100 * vixod_benzina + m_facilities / 100 * (
                 V_sux_gaz + vixod_gidro_diesel_utoch + G_H2S + vixod_benzina - 100),
     m_facilities * vixod_gidro_diesel_utoch / 34500 + m_facilities / 34500 * G_H2S + m_facilities / 34500 * vixod_benzina + m_facilities / 34500 * (
                 V_sux_gaz + vixod_gidro_diesel_utoch + G_H2S + vixod_benzina - 100),
     m_facilities * vixod_gidro_diesel_utoch / 34500 / 24 * 1000 + m_facilities / 34500 * G_H2S / 24 * 1000 + m_facilities / 34500 * vixod_benzina / 24 * 1000 + m_facilities / 34500 * (
                 V_sux_gaz + vixod_gidro_diesel_utoch + G_H2S + vixod_benzina - 100) / 24 * 1000]
]
print(tabulate(table_27, headers=['Наименование', '% (масс.)', 'т/год', 'т/сут*', 'кг/час']))

# Таблица 2.9
print(
    '-------------------------------------------------Материальный баланс РЕАКТОРА ГИДРООЧИСТКИ-------------------------------------------------')
table_29 = [
    ['Взято:'],
    ['Сырье', 100, m_facilities / 345 / 24 * 1000],
    ['Свежий водородсодержащий газ', G_0_H2,
     m_facilities / 34500 * (G_0_H2 + 0.1) / 24 * 1000],
    ['Циркулирующий водородсодержащий газ', G_C,
     m_facilities / 34500 * (G_C + 0.1) / 24 * 1000],
    ['Сумма', 100 + G_0_H2 + G_C, m_facilities / 345 / 24 * 1000 + m_facilities / 34500 * (
                G_0_H2 + 0.1) / 24 * 1000 + m_facilities / 34500 * (G_C + 0.1) / 24 * 1000],
    ['Получено'],
    ['Дизельное топливо', vixod_gidro_diesel_utoch,
     m_facilities * vixod_gidro_diesel_utoch / 34500 / 24 * 1000],
    ['Сероводород', G_H2S, m_facilities / 34500 * G_H2S / 24 * 1000],
    ['Сухой газ** + потери',
     V_sux_gaz + vixod_gidro_diesel_utoch + G_H2S + vixod_benzina - 100,
     m_facilities / 34500 * (
                 V_sux_gaz + vixod_gidro_diesel_utoch + G_H2S + vixod_benzina - 100) / 24 * 1000],
    ['Бензин', vixod_benzina, m_facilities / 34500 * vixod_benzina / 24 * 1000],
    ['Циркулирующий водородсодержащий газ', G_C,
     m_facilities / 34500 * (G_C + 0.1) / 24 * 1000],
    ['Сумма:',
     vixod_gidro_diesel_utoch + G_H2S + V_sux_gaz + vixod_gidro_diesel_utoch + G_H2S + vixod_benzina - 100 + vixod_benzina + G_c,
     m_facilities * vixod_gidro_diesel_utoch / 34500 / 24 * 1000 + m_facilities / 34500 * G_H2S / 24 * 1000 + m_facilities / 34500 * (
                 V_sux_gaz + vixod_gidro_diesel_utoch + G_H2S + vixod_benzina - 100) / 24 * 1000 + m_facilities / 34500 * vixod_benzina / 24 * 1000 + m_facilities / 34500 * (
                 G_C + 0.1) / 24 * 1000]
]
print(tabulate(table_29, headers=['Наименование', '% масс.', 'кг/ч']))

print('Температура на выходе из реактора: ' + str(t))
print('Vc: ' + str(V_c))

# Таблица 2.11
print(
    '-------------------------------------------------Расчет молекулярной массы смеси (свежего и циркулирующего) водородсодержащего газа-------------------------------------------------')
table_11 = [

    ['Свежий ВСГ ' + str(fresh_vsg) + ' кг/ч', '% мас.', m_H2, m_CH4, m_C2H6, m_y_C3H8,
     m_C4H10],
    ['Свежий ВСГ ' + str(fresh_vsg) + ' кг/ч', 'кг/ч', fresh_vsg / 100 * m_H2,
     fresh_vsg / 100 * m_CH4, fresh_vsg / 100 * m_C2H6, fresh_vsg / 100 * m_C3H8,
     fresh_vsg / 100 * m_C4H10],
    ['ЦВСГ ' + str(cvsg) + ' кг/ч', '% мас.', m_y_H2 * 100, m_y_CH4 * 100, m_y_C2H6 * 100,
     m_y_C3H8 * 100, m_y_C4H10 * 100],
    ['ЦВСГ ' + str(cvsg) + ' кг/ч', 'кг/ч', cvsg * m_y_H2, cvsg * m_y_CH4, cvsg * m_y_C2H6,
     cvsg * m_y_C3H8, cvsg * m_y_C4H10],
    ['Смесь ' + str(smes) + ' кг/ч', '% мас.',
     (fresh_vsg / 100 * m_H2 + cvsg * m_y_H2) * 100 / smes,
     (fresh_vsg / 100 * m_CH4 + cvsg * m_y_CH4) * 100 / smes,
     (fresh_vsg / 100 * m_C2H6 + cvsg * m_y_C2H6) * 100 / smes,
     (fresh_vsg / 100 * m_C2H6 + cvsg * m_y_C2H6) * 100 / smes,
     (fresh_vsg / 100 * m_C3H8 + cvsg * m_y_C3H8) * 100 / smes,
     (fresh_vsg / 100 * m_C4H10 + cvsg * m_y_C4H10) * 100 / smes],
    ['Смесь ' + str(smes) + ' кг/ч', 'кг/ч', fresh_vsg / 100 * m_H2 + cvsg * m_y_H2,
     fresh_vsg / 100 * m_CH4 + cvsg * m_y_CH4, fresh_vsg / 100 * m_C2H6 + cvsg * m_y_C2H6,
     fresh_vsg / 100 * m_C3H8 + cvsg * m_y_C3H8, fresh_vsg / 100 * m_C4H10 + cvsg * m_y_C4H10]
]
print(tabulate(table_11,
               headers=['Состав газа', 'Ед. изм.', 'Н2', 'СН4', 'С2Н6', 'С3Н8', 'С4Н10']))

print('Dp: ' + str(D_p))
print('h(кат): ' + str(h_kat))
print('h(цикл): ' + str(h_cycle))
print('H: ' + str(H))
print('P: ' + str(delta_P))
print('t: ' + str(t_itog))
input()