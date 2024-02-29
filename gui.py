
import streamlit as st
import numpy as np
import pandas as pd
from main import start_simulation
import matplotlib.pyplot as plt


servers = [
lambda: np.random.uniform(5.6),
lambda: np.random.exponential(7.6),
lambda: np.random.chisquare(4.9),
lambda: np.random.uniform(3.5),
lambda: np.random.exponential(11.4),
]

datos_servidores = start_simulation(1800,servers)[0]
# Calcular estadísticas por servidor
medias_servidores = [np.mean(servidor) for servidor in datos_servidores]
varianzas_servidores = [np.var(servidor) for servidor in datos_servidores]
desviaciones_estandar_servidores = [np.std(servidor) for servidor in datos_servidores]

# Calcular estadísticas globales
media_global = np.mean(np.concatenate(datos_servidores))
varianza_global = np.var(np.concatenate(datos_servidores))
desviacion_estandar_global = np.std(np.concatenate(datos_servidores))


# Crear DataFrame para mostrar en Streamlit
df_servidores = pd.DataFrame({
    'Servidor': range(1, len(datos_servidores)+1),
    'Media': medias_servidores,
    'Varianza': varianzas_servidores,
    'Desviación Estándar': desviaciones_estandar_servidores
})

# Mostrar tabla de estadísticas por servidor
st.title('Estadísticas por Servidor')
st.table(df_servidores)

# Mostrar estadísticas globales
st.title('Estadísticas Globales')
st.write(f'Media Global: {media_global}')
st.write(f'Varianza Global: {varianza_global}')
st.write(f'Desviación Estándar Global: {desviacion_estandar_global}')

# Gráficos de barras por servidor
fig, axs = plt.subplots(3, figsize=(10, 12))

axs[0].bar(df_servidores['Servidor'], df_servidores['Media'])
axs[0].set_title('Media por Servidor')

axs[1].bar(df_servidores['Servidor'], df_servidores['Varianza'])
axs[1].set_title('Varianza por Servidor')

axs[2].bar(df_servidores['Servidor'], df_servidores['Desviación Estándar'])
axs[2].set_title('Desviación Estándar por Servidor')

st.pyplot(fig)

# Gráfico de pastel para estadísticas globales
fig_pie, ax_pie = plt.subplots()
sizes = [media_global]+medias_servidores
labels = ['Representacion del valor medio de tiempo por servidor'] + ['Servidor: '+str(i) for i in range(1, len(datos_servidores)+1)]
ax_pie.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
ax_pie.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

st.pyplot(fig_pie)

# x = 0

# datos_servidores_total = []
# while x < 18000:
#     x += 1
#     datos_servidores = start_simulation(1800, servers)[1]
    
#     if x == 1:
#         datos_servidores_total = datos_servidores
#     else:
#         for i, j in zip(datos_servidores,datos_servidores_total):
#             j.extend(i)


# medias_servidores = [np.mean(servidor) for servidor in datos_servidores_total]
# varianzas_servidores = [np.var(servidor) for servidor in datos_servidores_total]
# desviaciones_estandar_servidores = [np.std(servidor) for servidor in datos_servidores_total]


# media_global = np.mean(np.concatenate(datos_servidores_total))
# varianza_global = np.var(np.concatenate(datos_servidores_total))
# desviacion_estandar_global = np.std(np.concatenate(datos_servidores_total))

# print("media por servidor:", medias_servidores)
# print('varianza por servidor:', varianzas_servidores)
# print('desviacion por servidor:', desviaciones_estandar_servidores)

# print('==================================')

# print("media global:", media_global)
# print('varianza global:', varianza_global)
# print('desviacion global:', desviacion_estandar_global)

