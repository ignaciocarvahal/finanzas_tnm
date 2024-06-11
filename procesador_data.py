import pandas as pd

# Leer datos desde un archivo Excel
df_finanzas = pd.read_excel('archivos/RegistroConsumoEstanqueTNM.xlsx', header=1)
df_sitrack = pd.read_excel('archivos/validarCargaCombustible.xlsx', header=2)

# Verificar la lectura de los archivos
print("df_finanzas shape:", df_finanzas.shape)
print("df_sitrack shape:", df_sitrack.shape)

# Renombrar columnas para que coincidan
df_finanzas.rename(columns={'Patente': 'Dominio', 'Litros Carga\n(lt)': 'Litros'}, inplace=True)
df_sitrack.rename(columns={'Dominio': 'Dominio', 'Litros': 'Litros'}, inplace=True)

# Verificar las columnas renombradas
print("df_finanzas columns:", df_finanzas.columns)
print("df_sitrack columns:", df_sitrack.columns)

# Eliminar filas con NaN
df_finanzas.dropna(subset=['Dominio', 'Fecha', 'Litros'], inplace=True)
df_sitrack.dropna(subset=['Dominio', 'Fecha', 'Litros'], inplace=True)

# Verificar la eliminación de filas con NaN
print("df_finanzas shape after dropna:", df_finanzas.shape)
print("df_sitrack shape after dropna:", df_sitrack.shape)

# Unificar formato de fecha usando formato mixto
df_finanzas['Fecha'] = pd.to_datetime(df_finanzas['Fecha'], errors='coerce').dt.strftime('%Y-%m-%d')
df_sitrack['Fecha'] = pd.to_datetime(df_sitrack['Fecha'], errors='coerce').dt.strftime('%Y-%m-%d')

# Unificar formatos numéricos en 'Litros'
df_finanzas['Litros'] = pd.to_numeric(df_finanzas['Litros'], errors='coerce')
df_sitrack['Litros'] = pd.to_numeric(df_sitrack['Litros'], errors='coerce')

# Concatenar DataFrames
df_unificado = pd.concat([df_sitrack, df_finanzas])
df_unificado.reset_index(drop=True, inplace=True)

# Verificar la concatenación de los DataFrames
print("df_unificado shape:", df_unificado.shape)
print("Unique Dominio values in df_unificado:", df_unificado['Dominio'].unique())

# Guardar el DataFrame unificado en un archivo Excel
df_unificado.to_excel('df_unificado.xlsx', index=False)

# Asegurar que las fechas son datetime
df_unificado['Fecha'] = pd.to_datetime(df_unificado['Fecha'], errors='coerce')

# Extraer año y mes
df_unificado['AñoMes'] = df_unificado['Fecha'].dt.to_period('M')

# Agrupar por Dominio y AñoMes y sumar los Litros
df_agrupado = df_unificado.groupby(['Dominio', 'AñoMes'])['Litros'].sum().reset_index()

# Verificar el agrupamiento y sumas
print("Unique Dominio values in df_agrupado:", df_agrupado['Dominio'].unique())

# Guardar el DataFrame agrupado en un archivo Excel
df_agrupado.to_excel('df_agrupado.xlsx', index=False)

print("DataFrame agrupado guardado en 'df_agrupado.xlsx'")
