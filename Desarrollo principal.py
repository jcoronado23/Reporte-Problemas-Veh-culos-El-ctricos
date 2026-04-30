# Fundamentos de Python
# Proyecto de Reportes de Vehículos Eléctricos
# Profesor: Andrés Mena Abarca
# Nombre: Jairon Martinez Coronado

# NHTSA – Datos abiertos sobre fallas y problemas en vehículos eléctricos

import os
import pandas as pd
import matplotlib.pyplot as plt
import textwrap
from contexto import resumen
plt.style.use("seaborn-v0_8-whitegrid")

ARCHIVO = "Vehículos_Eléctricos.csv"


def cargar_datos():
    df = pd.read_csv(
        ARCHIVO,
        encoding="utf-8-sig",
        quotechar='"'
    )
    
    df.columns = df.columns.str.strip()

    columnas_texto = ["id_documento", "marca", "modelo", "problemas"]

    for col in columnas_texto:
        df[col] = df[col].astype(str).str.strip()

    # Convertir año_modelo a número
    df["año_modelo"] = pd.to_numeric(df["año_modelo"], errors="coerce")

    # Quitar filas sin año válido
    df = df.dropna(subset=["año_modelo"])

    # Convertir a entero
    df["año_modelo"] = df["año_modelo"].astype(int)

    return df

# cargar datos una sola vez
df = cargar_datos()
data = df

def guardar_datos(df):
    df.to_csv(ARCHIVO, index=False, encoding="utf-8-sig")


def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")


def pausar():
    input("\nPresione Enter para volver al menú...")


import textwrap

# Buscar por número de ID
def buscar_por_id(data):
    # Selecciona la primer fila del ID
    id_buscar = input("Ingrese el ID del reporte: ").strip()
    
    resultado = data[data["id_documento"].astype(str).str.strip() == id_buscar]

    if resultado.empty:
        print("\n⚠ No se encontró ningún reporte con ese ID.")
        return

    fila = resultado.iloc[0]

    print("\n" + "=" * 65)
    print("        REPORTE DE PROBLEMA EN VEHÍCULO ELÉCTRICO")
    print("=" * 65)
    print(f"ID del reporte : {fila['id_documento']}")
    print(f"Marca          : {fila['marca']}")
    print(f"Modelo         : {fila['modelo']}")
    print(f"Año modelo     : {fila['año_modelo']}")
    print("-" * 65)

    problema = str(fila["problemas"])

    #Traducciones simples
    problema = problema.replace("Symptoms with driver", "Síntomas con la")
    problema = problema.replace("central display", "pantalla central")
    problema = problema.replace("driver display", "pantalla del conductor")
    problema = problema.replace("Under analysis", "Bajo análisis")
    problema = problema.replace("Remedy", "Solución")
    problema = problema.replace("Cause", "Causa")
    problema = problema.replace("Please do not replace any parts",
                                "No reemplazar piezas inmediatamente")
    problema = problema.replace("software release",
                                "actualización de software")

    partes = problema.split("NOTE:")
    descripcion = partes[0]

    descripcion = descripcion.replace("Queja", "")
    descripcion = descripcion.replace("Cause", "\nCausa:")
    descripcion = descripcion.replace("Remedy", "\nSolución:")

    print("\nDESCRIPCIÓN RESUMIDA")
    print("-" * 65)

    for linea in descripcion.split("\n"):
        for parte in textwrap.wrap(linea.strip(), width=65):
            print(parte)

    print("\nACCIONES RECOMENDADAS")
    print("-" * 65)
    print("1. Revisar actualización de software.")
    print("2. Revisar pantalla del conductor y pantalla central.")
    print("3. Revisar cableado eléctrico y línea de video.")
    print("4. Documentar resultados técnicos del vehículo.")

    print("\nNOTAS TÉCNICAS")
    print("-" * 65)
    print("• No reemplazar piezas inmediatamente.")
    print("• Documentar la queja original del cliente.")
    print("• Crear caso técnico si el problema continúa.")

    print("=" * 65)

# Crear gráfica de barras por marca de vehículo con mayor reporte
def grafica_marcas(data):
    conteo = data["marca"].value_counts()

    top_10 = conteo.head(10)
    otras = conteo[10:].sum()

    if otras > 0:
        top_10["Otras"] = otras

    plt.figure(figsize=(12, 6))
    ax = top_10.plot(kind="bar")
    # Cambiar colores de barras, y barra más alta a destacar con color gold
    colores = ["green"] * len(top_10) 
    colores[0] = "red"
    colores[10] = "blue"

    ax = top_10.plot(kind="bar", color=colores)

    plt.title("Cantidad de reportes por marca")
    plt.xlabel("Marca")
    plt.xlabel("[ MARCA VEHÍCULO ELÉCTRICO ]\n \nEl gráfico presenta la cantidad de reportes por marca de vehículos eléctricos, permitiendo identificar cuáles concentran más fallas y facilitando su análisis visual.")
    plt.ylabel("Cantidad de reportes")
    plt.xticks(rotation=45, ha="right")
    
    # Mostrar valores encima de cada barra
    for i, valor in enumerate(top_10):
        ax.text(i, valor, str(int(valor)), ha='center', va='bottom')
        
    plt.tight_layout()
    plt.show()
    

# Crear gráfica de lineas de años con mayor reportes del 2020 al 2026
def grafica_reportes_anio(data):
    datos = data.copy()

    datos["año_modelo"] = pd.to_numeric(datos["año_modelo"], errors="coerce")
    datos = datos.dropna(subset=["año_modelo"])
    datos["año_modelo"] = datos["año_modelo"].astype(int)

    datos = datos[
        (datos["año_modelo"] >= 2020) &
        (datos["año_modelo"] <= 2026)
    ]

    reportes = datos["año_modelo"].value_counts().sort_index()

    if reportes.empty:
        print("\n⚠ No hay reportes entre los años 2020 y 2026.")
        return

    crecimiento = reportes.diff().fillna(0)
    porcentaje = reportes.pct_change().fillna(0) * 100

    plt.figure(figsize=(12, 6))

    plt.plot(reportes.index, reportes.values, marker="o", label="Reportes")
    plt.plot(crecimiento.index, crecimiento.values, marker="s", linestyle="--", label="Crecimiento")

    for x, y in zip(reportes.index, reportes.values):
        plt.text(x, y + 2, str(int(y)), ha="center")
        plt.text(x, y + 200, str(int(y)), ha="center")

    for x, y, p in zip(crecimiento.index, crecimiento.values, porcentaje.values):
        plt.text(x, y - 4, f"{int(y)} / {p:.1f}%", ha="center")
        plt.text(x, y + 200, f"{int(y)} / {p:.1f}%", ha="center")

    plt.title("Reportes, crecimiento y porcentaje 2020-2026")
    plt.xlabel("Año del modelo")
    plt.xlabel("[ AÑO DEL MODELO ] \n \n El gráfico muestra la evolución de los reportes de fallas por año del modelo, permitiendo identificar tendencias a lo largo del tiempo.")
    plt.ylabel("Cantidad")
    plt.xticks(reportes.index)
    plt.legend()
    plt.tight_layout()
    plt.show()

    print("\nResumen:")
    print("Total reportes:", int(reportes.sum()))
    print("Año con más reportes:", int(reportes.idxmax()))

# Registrar un vehículo nuevo en la base de datos CSV
def registrar_vehiculo(data):
    print("\n=== Registrar vehículo nuevo ===")
    print("Escriba M para volver al menú.")

    id_documento = input("ID del vehículo: ").strip()

    if id_documento.upper() == "M":
        return data

    if id_documento == "":
        print("⚠ El ID no puede estar vacío.")
        return data

    existe = data[data["id_documento"].astype(str) == id_documento]

    if not existe.empty:
        print("⚠ Ese ID ya existe.")
        return data

    marca = input("Marca: ").strip()
    modelo = input("Modelo: ").strip()
    anio = input("Año modelo: ").strip()
    problema = input("Problema reportado: ").strip()

    if marca == "" or modelo == "" or anio == "" or problema == "":
        print("⚠ No se permiten campos vacíos.")
        return data

    if not anio.isdigit():
        print("⚠ El año debe ser numérico.")
        return data

    anio = int(anio)

    if anio < 1886 or anio > 2026:
        print("⚠ Año fuera de rango.")
        return data

    nuevo = pd.DataFrame([{
        "id_documento": id_documento,
        "marca": marca,
        "modelo": modelo,
        "año_modelo": anio,
        "problemas": problema
    }])

    data = pd.concat([data, nuevo], ignore_index=True)
    guardar_datos(data)

    print("\n✅ Vehículo registrado correctamente.")
    return data

# Editar vehículo de la base de datos CSV
def editar_vehiculo(data):
    print("\n=== Editar vehículo existente ===")

    id_buscar = input("Ingrese el ID del vehículo a editar: ").strip()

    resultado = data[data["id_documento"].astype(str) == id_buscar]

    if resultado.empty:
        print("⚠ No existe un vehículo con ese ID.")
        return data

    indice = resultado.index[0]

    print("\nVehículo encontrado:")
    print(data.loc[[indice]].to_string(index=False))

    print("\nDeje en blanco lo que no desea cambiar.")

    nueva_marca = input("Nueva marca: ").strip()
    nuevo_modelo = input("Nuevo modelo: ").strip()
    nuevo_anio = input("Nuevo año modelo: ").strip()
    nuevo_problema = input("Nuevo problema reportado: ").strip()

    if nueva_marca != "":
        data.loc[indice, "marca"] = nueva_marca

    if nuevo_modelo != "":
        data.loc[indice, "modelo"] = nuevo_modelo

    if nuevo_anio != "":
        if nuevo_anio.isdigit():
            nuevo_anio = int(nuevo_anio)

            if 1886 <= nuevo_anio <= 2026:
                data.loc[indice, "año_modelo"] = nuevo_anio
            else:
                print("⚠ Año fuera de rango. No se modificó.")
        else:
            print("⚠ Año inválido. No se modificó.")

    if nuevo_problema != "":
        data.loc[indice, "problemas"] = nuevo_problema

    guardar_datos(data)

    print("\n✅ Vehículo actualizado correctamente.")
    return data

# Eliminar vehículo de la base de datos CSV
def eliminar_vehiculo(data):
    print("\n=== Eliminar vehículo existente ===")

    id_buscar = input("Ingrese el ID del vehículo a eliminar: ").strip()

    resultado = data[data["id_documento"].astype(str) == id_buscar]

    if resultado.empty:
        print("⚠ No existe un vehículo con ese ID.")
        return data

    print("\nVehículo encontrado:")
    print(resultado.to_string(index=False))

    confirmar = input("\n¿Seguro que desea eliminarlo? (s/n): ").strip().lower()

    if confirmar == "s":
        data = data[data["id_documento"].astype(str) != id_buscar]
        guardar_datos(data)

        print("\n✅ Vehículo eliminado correctamente.")
    else:
        print("\nOperación cancelada.")

    return data

# Mostrar menú principal
def mostrar_menu():
    data = cargar_datos()

    while True:
        limpiar_pantalla()
        
        print("====================================================================================================")
        print("                     Sistema de Análisis de Problemas en Vehículos Eléctricos 🚗⚡")
        print("====================================================================================================")
        print('🔋')
        print(resumen)
        print('🪫')
        print("1. Buscar problema por ID")
        print("2. Gráfica de reportes por marca")
        print("3. Gráfica de reportes por año 2020-2026")
        print("4. Registrar vehículo nuevo")
        print("5. Editar vehículo existente")
        print("6. Eliminar vehículo existente")
        print("7. Salir")

        opcion = input("\n🔘Ingrese una opción: ").strip()

        if opcion == "1":
            buscar_por_id(data)

        elif opcion == "2":
            grafica_marcas(data)

        elif opcion == "3":
            grafica_reportes_anio(data)

        elif opcion == "4":
            data = registrar_vehiculo(data)

        elif opcion == "5":
            data = editar_vehiculo(data)

        elif opcion == "6":
            data = eliminar_vehiculo(data)

        elif opcion == "7":
            print("\nGracias por usar nuestro sistema de Autos Electricos. ¡Hasta luego!👋")
            break

        else:
            print("\n⚠️ Opción inválida. Ingrese un número del 1 al 7.")

        pausar()


if __name__ == "__main__":
    mostrar_menu()
