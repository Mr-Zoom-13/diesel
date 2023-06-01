from math import log

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
vixod_gidro_diesel = 100 - vixod_benzina - vixod_gaza
# ----------------

m_merkaptan = 0.062
m_sulfid = 0.125
m_disulfid = 0.0938
m_tiofen = 0.25

G1 = m_merkaptan * seri_merkaptan + m_sulfid * seri_sulfid + m_disulfid * seri_disulfid + (
        seri_tiofen - ost_sod_seri) * m_tiofen

p15_15 = 0.994 * (p20_4 / 100) + 0.0093
t_sr = (n_k + k_k) / 2
K = (1.216 * ((t_sr + 273) ** (1 / 3))) / p15_15
M = 7 * K - 21.5 + (0.76 - 0.04 * K) * t_sr + (0.0003 * K - 0.00245) * (t_sr ** 2)

G2 = 2 * 9 / M

N_A = (M * (A_0 - A_K)) / 13600
V_A = (m_facilities * (1000 / M)) * N_A

G4 = (x_h2 * 2 * 100) / (x_h2 * 2 + (1 - x_h2) * M)

G5 = (xi * 0.01 * 2 * 100) / (p20_4 * 22.4)

G_h2 = G1 + G2 + G3 + G4 + G5 + 0.3

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

# ---------------
V_c = (G_rasxod * 22.4 * z_c * 0.1 * (380 + 273)) / (M * p * 273)
# ---------------


V_kat = G_rasxod / (p20_4 * w * n)

# -----------------
D_p = ((2 * V_kat) / 3.14) ** (1 / 3)
# ----------------

V_g = 111111111111111111111111111
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
N_c = (400 * 238095.24) / 846.6

# -------
t_itog = V_g_r / N_c
# -------

print("Вдт: " + str(vixod_gidro_diesel))
print('Общий расход водорода: ' + str(G_h2))
print('ВдтУточ: ' + str(vixod_gidro_diesel_utoch))
print('Выход сухого газа: ' + str(V_sux_gaz))
# таблица 2.7 и 2.9
# таблица 2.7
table_27 = [
    ['Наименование', '% (масс.)', 'т/год', 'т/сут*', 'кг/час'],
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
    ['Сухой газ** + потери', V_sux_gaz + vixod_gidro_diesel_utoch + G_H2S + vixod_benzina - 100, m_facilities / 100 * (V_sux_gaz + vixod_gidro_diesel_utoch + G_H2S + vixod_benzina - 100), m_facilities / 34500 * (V_sux_gaz + vixod_gidro_diesel_utoch + G_H2S + vixod_benzina - 100), m_facilities / 34500 * (V_sux_gaz + vixod_gidro_diesel_utoch + G_H2S + vixod_benzina - 100) / 24 * 1000],
    ['Бензин', vixod_benzina, m_facilities / 100 * vixod_benzina,
     m_facilities / 34500 * vixod_benzina, m_facilities / 34500 * vixod_benzina / 24 * 1000],
    ['Сумма:', vixod_gidro_diesel_utoch + G_H2S + vixod_benzina + V_sux_gaz + vixod_gidro_diesel_utoch + G_H2S + vixod_benzina - 100,
     m_facilities / 100 * vixod_gidro_diesel_utoch + m_facilities / 100 * G_H2S + m_facilities / 100 * vixod_benzina + m_facilities / 100 * (V_sux_gaz + vixod_gidro_diesel_utoch + G_H2S + vixod_benzina - 100),
     m_facilities * vixod_gidro_diesel_utoch / 34500 + m_facilities / 34500 * G_H2S + m_facilities / 34500 * vixod_benzina + m_facilities / 34500 * (V_sux_gaz + vixod_gidro_diesel_utoch + G_H2S + vixod_benzina - 100),
     m_facilities * vixod_gidro_diesel_utoch / 34500 / 24 * 1000 + m_facilities / 34500 * G_H2S / 24 * 1000 + m_facilities / 34500 * vixod_benzina / 24 * 1000 + m_facilities / 34500 * (V_sux_gaz + vixod_gidro_diesel_utoch + G_H2S + vixod_benzina - 100) / 24 * 1000]
]
for i in range(len(table_27)):
    for j in range(len(table_27[i])):
        table_27[i][j] = str(table_27[i][j])
for i in table_27:
    print('\t'.join(i))

# Таблица 2.9
table_29 = [
    ['Наименование', '% масс.', 'кг/ч'],
    ['Взято:'],
    ['Сырье', 100, m_facilities / 345 / 24 * 1000],
    ['Свежий водородсодержащий газ', G_0_H2, m_facilities / 34500 * (G_0_H2 + 0.1) / 24 * 1000],
    ['Циркулирующий водородсодержащий газ', ],
    ['Сумма'],


]

print('Температура на выходе из реактора: ' + str(t))
print('Vc: ' + str(V_c))
# Таблица 2.11
print('Dp: ' + str(D_p))
print('h(кат): ' + str(h_kat))
print('h(цикл): ' + str(h_cycle))
print('H: ' + str(H))
print('P: ' + str(delta_P))
print('t: ' + str(t_itog))
