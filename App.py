

pip install influxdb-client pandas matplotlib

import pandas as pd
from influxdb_client import InfluxDBClient
import matplotlib.pyplot as plt
import altair as alt

# --- Parámetros de conexión ---
INFLUXDB_URL = "https://us-east-1-1.aws.cloud2.influxdata.com"
INFLUXDB_TOKEN = "JcKXoXE30JQvV9Ggb4-zv6sQc0Zh6B6Haz5eMRW0FrJEduG2KcFJN9-7RoYvVORcFgtrHR-Q_ly-52pD7IC6JQ=="
INFLUXDB_ORG = "0925ccf91ab36478"
INFLUXDB_BUCKET = "EXTREME_MANUFACTURING"

# --- Inicializar cliente ---
client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
query_api = client.query_api()

# --- Consulta de datos DHT22 ---
query_dht22 = '''
from(bucket: "EXTREME_MANUFACTURING")
  |> range(start: -3d)
  |> filter(fn: (r) => r._measurement == "studio-dht22")
  |> filter(fn: (r) => r._field == "humedad" or r._field == "temperatura" or r._field == "sensacion_termica")
'''

tables_dht22 = query_api.query(org=INFLUXDB_ORG, query=query_dht22)
data_dht22 = []
for table in tables_dht22:
    for record in table.records:
        data_dht22.append((record.get_time(), record.get_field(), record.get_value()))
st.sidebar.header("Filtros")
days = st.sidebar.slider("Rango de tiempo (días)", 1, 30, 3)

st.title(" Tablero de Monitoreo Industrial")
st.write("Datos de sensores DHT22 y MPU6050")

df_dht22 = pd.DataFrame(data_dht22, columns=["time", "field", "value"])
df_dht22 = df_dht22.pivot(index="time", columns="field", values="value")
df_dht22.plot(subplots=True, figsize=(10,6), title="Variables DHT22")
plt.show()

def query_data(measurement, fields):
    fields_filter = " or ".join([f'r._field == "{f}"' for f in fields])
    query = f'''
    from(bucket: "{INFLUXDB_BUCKET}")
      |> range(start: -{days}d)
      |> filter(fn: (r) => r._measurement == "{measurement}")
      |> filter(fn: (r) => {fields_filter})
    '''
    tables = query_api.query(org=INFLUXDB_ORG, query=query)

    data = []
    for table in tables:
        for record in table.records:
            data.append((record.get_time(), record.get_field(), record.get_value()))

    if len(data) == 0:
        return pd.DataFrame()

    df = pd.DataFrame(data, columns=["time", "field", "value"])
    df = df.pivot(index="time", columns="field", values="value")
    df.index = pd.to_datetime(df.index)
    return df
st.subheader(" Sensor DHT22 (Temperatura y Humedad)")
fields_dht = ["temperatura", "humedad", "sensacion_termica"]
df_dht = query_data("studio-dht22", fields_dht)

if not df_dht.empty:
    st.line_chart(df_dht)
    
    st.write("Métricas DHT22")
    st.write(df_dht.describe().T[["mean", "min", "max"]])

else:
    st.warning("No hay datos para mostrar")

# --- Consulta de datos MPU6050 ---
query_mpu = '''
from(bucket: "EXTREME_MANUFACTURING")
  |> range(start: -3d)
  |> filter(fn: (r) => r._measurement == "mpu6050")
  |> filter(fn: (r) =>
      r._field == "accel_x" or r._field == "accel_y" or r._field == "accel_z" or
      r._field == "gyro_x" or r._field == "gyro_y" or r._field == "gyro_z" or
      r._field == "temperature")
'''
st.subheader(" Sensor MPU6050 (Vibraciones y Aceleración)")
fields_mpu = ["accel_x", "accel_y", "accel_z"]
df_mpu = query_data("mpu6050", fields_mpu)

if not df_mpu.empty:
    st.line_chart(df_mpu)

    st.write("Métricas MPU6050")
    st.write(df_mpu.describe().T[["mean", "min", "max"]])

else:
    st.warning("No hay datos para mostrar")

tables_mpu = query_api.query(org=INFLUXDB_ORG, query=query_mpu)
data_mpu = []
for table in tables_mpu:
    for record in table.records:
        data_mpu.append((record.get_time(), record.get_field(), record.get_value()))

df_mpu = pd.DataFrame(data_mpu, columns=["time", "field", "value"])
df_mpu = df_mpu.pivot(index="time", columns="field", values="value")
df_mpu.plot(subplots=True, figsize=(10,8), title="Variables MPU6050")
plt.show()# --- Visualización de datos DHT22 ---
df_dht22 = pd.DataFrame(data_dht22, columns=["time", "field", "value"])
df_dht22 = df_dht22.pivot(index="time", columns="field", values="value")
df_dht22.plot(subplots=True, figsize=(10,6), title="Variables DHT22")
plt.show()

# --- Visualización de datos MPU6050 ---
df_mpu = pd.DataFrame(data_mpu, columns=["time", "field", "value"])
df_mpu = df_mpu.pivot(index="time", columns="field", values="value")
df_mpu.plot(subplots=True, figsize=(10,8), title="Variables MPU6050")
plt.show()
