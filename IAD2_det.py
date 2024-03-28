import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('ggplot') #Style
# Creating Dataframes a partir dos dados obtidos por DataThief
df_em = pd.read_csv('EJ200-1.txt', header=1, delimiter=',') # emissor
df_det = pd.read_csv('PDE4.txt', header=1, delimiter=',')   # detetor

em_x  = df_em.iloc[:, 0].values.tolist()  #nº do evento
em_x  = [val + 380 for val in em_x] # o eixo xx do DataThief inicia em 0
em_y  = df_em.iloc[:, 1].values.tolist()  #tempo unix em s

det_x = df_det.iloc[:, 0].values.tolist()  #nº do evento
det_y = df_det.iloc[:, 1].values.tolist()  #tempo unix em s

"""
O eixo xx do DataThief inicia em 0 e removemos os valores que estão fora
do range do (gráfico) do emissor.
"""
rem = []
for lamb in range(len(det_x)):
    if det_x[lamb] > 100 and det_x[lamb] < 200:
        det_x[lamb] = det_x[lamb] + 300
        det_y[lamb] = det_y[lamb]/100
    else:
        rem.append(lamb)

rem.reverse() # reverse para evitar erros de indíces
for ind in rem:
    det_x.pop(ind)
    det_y.pop(ind)

# print(min(em_x)) # 397.6481 = 398 valor máximo
# print(max(em_x)) # 499.9981 = 500 valor mínimo
# print(len(em_x)) # 206 bins
# 500-398/206 = 0,5 valor/bin

"""
Os dados provenientes do Data Thief não vêem com a mesma escala,
Assim, para os analisarmos decidimos recorrer a uma forma de tornar
arredondar a números interiros dividir por 2 obtendo assim o valor
por bin estimado acima.

Depois procedemos realizámos uma medida para a normalização dos fotões emitidos
"""
em_x  = [(round(2*val)/2) for val in em_x]
det_x = [(round(2*val)/2) for val in det_x]
integ_em = 0
for ind in range(1,len(em_x)):
    integ_em += em_y[ind]*(em_x[ind]-em_x[ind-1])
print(integ_em)

#plt.scatter(em_x,em_y, label = "hist e plot")
#plt.scatter(det_x,det_y, label = "hist e plot")
#plt.show(block=False)

"""
Utilizámos um set (estrutura de dados que elimina as repetições) para
eliminarmos os valores que não aparecessem na escala com menor resolução
de bins, e caso houvesse uma repetição dos valores iremos fazer uma
média aritmética.
Multiplicámos as curvas, obtivemos o integral e depois normalizámos
"""
set_det = {val for val in det_x}


mult_x = []
mult_y = []
for ind in range(len(em_x)):
    if em_x[ind] in set_det:
        mult_x.append(em_x[ind])
        temp_mult_y = em_y[ind]
        i2 = 1
        while em_x[ind] == em_x[ind+i2]:
            temp_mult_y += em_y[ind]
            i2 += 1
        mult_y.append((temp_mult_y/i2)*det_y[det_x.index(em_x[ind])])

integ_mult = 0
for ind in range(1,len(mult_x)):
    integ_mult += mult_y[ind]*(mult_x[ind]-mult_x[ind-1])
print(integ_mult)
print(integ_mult/integ_em*100) # 39,34 %
# 0.3934261625894686

plt.scatter(mult_x,mult_y, label = "hist e plot")
plt.show(block=True)

# Assim sendo assumimos que o número de fotões "detetáveis" será:
N_det = 20000*0.3934261625894686
print(N_det)