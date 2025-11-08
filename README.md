# Tablero de Monitoreo Industrial

Este proyecto implementa un **dashboard interactivo** desarrollado con **Streamlit** para visualizar datos de sensores industriales almacenados en **InfluxDB**.  
Los sensores utilizados son:

- **DHT22** → mide **temperatura**, **humedad** y **sensación térmica**.  
- **MPU6050** → registra **vibraciones** y **aceleraciones** en tres ejes (X, Y, Z).

El tablero permite consultar datos históricos, visualizar tendencias mediante gráficas dinámicas y calcular métricas estadísticas clave.

---

## Características principales

- Conexión directa a **InfluxDB Cloud** mediante API.
- Gráficas interactivas con **Plotly Express**.
- Control de rango temporal mediante **slider** en la barra lateral.
- Tablas de métricas con valores promedio, mínimos y máximos.
- Interfaz web sencilla e intuitiva.

---

## Estructura del proyecto

│
├── App.py # Código principal de la aplicación Streamlit
├── requirements.txt # Lista de dependencias (paquetes de Python)
├── .streamlit/
│ └── secrets.toml # Credenciales privadas (InfluxDB)
├── README.md # Documentación del proyecto
└── assets/ # (Opcional) Imágenes, íconos o archivos adicionales
