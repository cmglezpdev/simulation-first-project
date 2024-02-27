
import streamlit as st
import numpy as np
import pandas as pd
from main import start_simulation
import matplotlib.pyplot as plt


servers = [
lambda: np.random.uniform(),
lambda: np.random.exponential(0.2),
lambda: np.random.chisquare(0.1),
lambda: np.random.uniform(0.4),
lambda: np.random.exponential(0.5),
]



# Configuración de la página de Streamlit
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


datos_servidores = start_simulation(1800,servers)
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
