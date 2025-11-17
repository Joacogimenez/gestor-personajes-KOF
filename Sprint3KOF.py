"""
-----------------------------------------------------------------------------------------------
Título: Personajes KOF
Fecha: 
Autor: Grupo 7
Descripción: 
    Programa que gestiona un diccionario de personajes del juego KOF. 
    Incluye validaciones de entrada, un menú CRUD, reportes y persistencia en CSV y JSON.
-----------------------------------------------------------------------------------------------
"""

# Nota: No hay una variable activa con datos por defecto; el programa
# intentará cargar JSON -> CSV y, si no hay archivos, trabajará con un diccionario vacío.

#----------------------------------------------------------------------------------------------
# DICCIONARIO 
#----------------------------------------------------------------------------------------------
# personajes = {
#     "K001": {
#         "nombre": "Kyo Kusanagi",
#         "nacionalidad": "Japón",
#         "estilo": "Kusanagi style",
#         "edad": 20,
#         "peso": 75,
#         "altura": 180,
#         "fuerza": 88
#     },
#     "K002": {
#         "nombre": "Terry Bogard",
#         "nacionalidad": "EEUU",
#         "estilo": "Martial arts",
#         "edad": 24,
#         "peso": 82,
#         "altura": 182,
#         "fuerza": 90
#     },
#     "K003": {
#         "nombre": "Robert Garcia",
#         "nacionalidad": "Italia",
#         "estilo": "Kyokugenryu Karate",
#         "edad": 23,
#         "peso": 85,
#         "altura": 180,
#         "fuerza": 84
#     },
#     "K004": {
#         "nombre": "Ramón",
#         "nacionalidad": "México",
#         "estilo": "Lucha Libre",
#         "edad": 25,
#         "peso": 80,
#         "altura": 170,
#         "fuerza": 86
#     },
#     "K005": {
#         "nombre": "Chin Gentsai",
#         "nacionalidad": "China",
#         "estilo": "Kung-fu",
#         "edad": 70,
#         "peso": 68,
#         "altura": 168,
#         "fuerza": 78
#     }
# }

#----------------------------------------------------------------------------------------------
# MÓDULOS
#----------------------------------------------------------------------------------------------
import pandas as pd  # para mostrar tablas y guardar CSV (persistencia CSV)
import json          # persistencia JSON
import tempfile
import os
import re            # REGEX

#----------------------------------------------------------------------------------------------
# PERSISTENCIA DE DATOS (CSV y JSON)
#----------------------------------------------------------------------------------------------
ARCHIVO_CSV = "personajes.csv"
ARCHIVO_JSON = "personajes_kof.json"


def guardar_personajes_csv(personajes):
    """
    Guarda el diccionario `personajes` en 'personajes.csv' (sobrescribe).
    Recibe: personajes (dict)
    Retorna: None
    """
    try:
        # Persistencia en CSV (se usa pandas DataFrame -> to_csv)
        df = pd.DataFrame.from_dict(personajes, orient='index')
        df.index.name = 'codigo'
        df.to_csv(ARCHIVO_CSV, index=True)
        print("Datos guardados en 'personajes.csv'.")
    except (OSError, pd.errors.ParserError) as e:
        print("Error al guardar 'personajes.csv':", e)


def cargar_personajes_csv():
    """
    Intenta cargar personajes desde 'personajes.csv'.
    Retorna: dict con personajes si tuvo éxito, o None si no pudo.
    """
    try:
        # manejo de excepciones: captura FileNotFoundError y errores de pandas
        df = pd.read_csv(ARCHIVO_CSV, index_col='codigo')
        data = df.to_dict(orient='index')
        # Normalizar campos numéricos
        for k, v in data.items():
            for campo in ("edad", "peso", "altura", "fuerza"):
                if campo in v:
                    try:
                        v[campo] = int(v[campo])
                    except (ValueError, TypeError):
                        # si no es convertible, dejamos tal cual
                        pass
        print("Datos cargados desde 'personajes.csv'.")
        return data
    except FileNotFoundError:
        print("Archivo 'personajes.csv' no encontrado.")
        return None
    except (pd.errors.EmptyDataError, pd.errors.ParserError, OSError) as e:
        print(f"Error al cargar los personajes desde CSV: {e}")
        return None


def guardar_personajes_json(personajes):
    """
    Guarda el diccionario `personajes` en 'personajes_kof.json' de forma atómica.
    Recibe: personajes (dict)
    Retorna: None

    Usamos json.dumps primero para validar la serialización y luego escribimos
    el string al archivo de forma segura (archivo temporal -> replace).
    """
    try:
        # VALIDACIÓN: intentar serializar a string JSON
        json_text = json.dumps(personajes, ensure_ascii=False, indent=4)
    except (TypeError, OverflowError) as e:
        print("No se pudo serializar a JSON (datos inválidos):", e)
        return

    try:
        # Escritura atómica: escribimos el string en archivo temporal y reemplazamos
        with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as tmp:
            tmp.write(json_text)
            tmp_name = tmp.name
        os.replace(tmp_name, ARCHIVO_JSON)
        print(f"Datos guardados en '{ARCHIVO_JSON}'.")
    except OSError as e:
        # manejo de excepciones de I/O
        print("Error al guardar JSON en disco:", e)


def cargar_personajes_json():
    """
    Intenta cargar personajes desde 'personajes_kof.json'.
    Retorna: dict con personajes si tuvo éxito, o None si no pudo.
    Utiliza json.loads sobre el contenido leído para que podamos capturar
    errores de parseo y dar mensajes claros.
    """
    try:
        with open(ARCHIVO_JSON, "r", encoding="utf-8") as f:
            text = f.read()
        # parsear con loads para poder atrapar JSONDecodeError
        data = json.loads(text)
        # Normalizar tipos numéricos
        for k, v in data.items():
            for campo in ("edad", "peso", "altura", "fuerza"):
                if campo in v:
                    try:
                        v[campo] = int(v[campo])
                    except (ValueError, TypeError):
                        pass
        print(f"Datos cargados desde '{ARCHIVO_JSON}'.")
        return data
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        print(f"El archivo '{ARCHIVO_JSON}' está corrupto o tiene formato inválido.")
        return None
    except OSError as e:
        print("Error al leer JSON desde disco:", e)
        return None

#----------------------------------------------------------------------------------------------
# FUNCIONES DE VALIDACIÓN
#----------------------------------------------------------------------------------------------
def validarNumero(msj, msE, msE2, mini, maxi):
    """
    Solicita y valida un entero dentro del rango [mini, maxi].
    Retorna el entero validado.

    Manejo de excepción simple: usamos try/except ValueError en la conversión a int.
    """
    while True:
        valor = input(msj).strip()
        try:
            n = int(valor)
        except ValueError:
            print(msE)
            continue
        if mini <= n <= maxi:
            return n
        else:
            print(msE2)


def validarTexto(msj, msE):
    """
    Solicita y valida texto básico (letras o espacios).
    Retorna el string validado.
    """
    while True:
        valor = input(msj).strip()
        if valor == "":
            print(msE)
            continue
        # aceptamos texto que contenga letras y espacios
        if all(ch.isalpha() or ch.isspace() for ch in valor):
            return valor
        else:
            print(msE)

#----------------------------------------------------------------------------------------------
# FUNCIONES CRUD (reciben/retornan el diccionario personajes)
#----------------------------------------------------------------------------------------------
def crear_personaje(personajes):
    """
    Crea un nuevo personaje en el diccionario `personajes` (parámetro)
    y retorna el diccionario actualizado.

    REGEXs usados:
    - código: ^K\d{3}$  (ya existente)
    - nombre: acepta letras, espacios y acentos (2-30 chars)
      patrón: ^[A-Za-zÁÉÍÓÚáéíóúÑñ ]{2,30}$
    - estilo: letras, espacios y guiones (3-30 chars)
      patrón: ^[A-Za-zÁÉÍÓÚáéíóúÑñ\s\-]{3,30}$
    """
    # validación del código con regex: 'K' + 3 dígitos
    # REGEX usado aquí: ^K\d{3}$  (ver línea)
    while True:
        codigo = input("Ingrese código (ej: K006): ").upper().strip()
        if not re.fullmatch(r"^K\d{3}$", codigo):  # REGEX 1
            print("Código inválido. Debe tener formato 'K' seguido de 3 dígitos (ej: K001).")
            continue
        if codigo in personajes:
            print("El código ya existe.")
            return personajes
        break

    # Nombre: validamos también con regex 
    while True:
        nombre = validarTexto("Nombre: ", "Texto inválido.")
        # permitir acentos y Ñ; regex que acepta letras y espacios, entre 2 y 30 chars
        if re.fullmatch(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ ]{2,30}$", nombre):
            break
        else:
            print("Nombre inválido. Use solo letras y espacios (2-30 caracteres).")

    nacionalidad = validarTexto("Nacionalidad: ", "Texto inválido.")

    # Estilo: validación simple con regex (letras, espacios y guiones)
    while True:
        estilo = validarTexto("Estilo: ", "Texto inválido.")
        if re.fullmatch(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ\s\-]{3,30}$", estilo):
            break
        else:
            print("Estilo inválido. Use letras, espacios o guiones (3-30 caracteres).")

    edad = validarNumero("Edad: ", "No es número.", "Edad fuera de rango.", 10, 80)
    peso = validarNumero("Peso (kg): ", "No es número.", "Peso fuera de rango.", 30, 200)
    altura = validarNumero("Altura (cm): ", "No es número.", "Altura fuera de rango.", 100, 250)
    fuerza = validarNumero("Fuerza (0-100): ", "No es número.", "Rango inválido.", 0, 100)

    personajes[codigo] = {
        "nombre": nombre,
        "nacionalidad": nacionalidad,
        "estilo": estilo,
        "edad": edad,
        "peso": peso,
        "altura": altura,
        "fuerza": fuerza
    }
    # Guardar persistencia (CSV y JSON)
    guardar_personajes_csv(personajes)   # persistencia en CSV
    guardar_personajes_json(personajes)  # persistencia en JSON
    print(f"\nEl personaje {nombre} fue creado y guardado en CSV y JSON.")
    return personajes


def leer_personaje(personajes):
    """
    Muestra la información de un personaje específico en forma alineada.
    Corrige el desacomodo del título 'Código' para que quede bien sobre la columna.
    """
    codigo = input("Ingrese código: ").upper().strip()
    if codigo in personajes:
        datos = personajes[codigo]
        nombre = datos.get("nombre", "N/A")
        edad = datos.get("edad", "N/D")
        peso = datos.get("peso", "N/D")
        altura = datos.get("altura", "N/D")
        fuerza = datos.get("fuerza", "N/D")

        
        print("\nPersonaje encontrado:\n")
        print(f"{'Código':<6} {'Nombre':<18} {'Edad':<4} {'Peso':<5} {'Altura':<7} {'Fuerza':<6}")
        print("-----------------------------------------------------------")
        print(f"{codigo:<6} {str(nombre):<18} {str(edad):<4} {str(peso):<5} {str(altura):<7} {str(fuerza):<6}")
    else:
        print("Personaje no encontrado.")


def listar_personajes(personajes):
    """
    Muestra todos los personajes en formato simple:
    Nombre - Nacionalidad (sin tabla ni código)
    """
    if not personajes:
        print("No hay personajes para listar.")
        return
    print("\nLista de personajes (Nombre - Nacionalidad):\n")
    for datos in personajes.values():
        nombre = datos.get("nombre", "N/A")
        nacionalidad = datos.get("nacionalidad", "N/D")
        print(f"{nombre} - {nacionalidad}")


def actualizar_personaje(personajes):
    """
    Actualiza un atributo de un personaje. Retorna el diccionario actualizado.
    """
    codigo = input("Ingrese código del personaje: ").upper().strip()
    if codigo in personajes:
        print("Datos actuales:", personajes[codigo])
        campo = input("Atributo a modificar (nombre, nacionalidad, estilo, edad, peso, altura, fuerza): ").lower()
        if campo in personajes[codigo]:
            if campo in ["edad", "peso", "altura", "fuerza"]:
                nuevo_valor = validarNumero("Nuevo valor: ", "No es número.", "Fuera de rango.", 0, 200)
            else:
                # si actualiza nombre o estilo aplicamos regex válida como en creación
                if campo == "nombre":
                    while True:
                        nv = validarTexto("Nuevo nombre: ", "Texto inválido.")
                        if re.fullmatch(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ ]{2,30}$", nv):
                            nuevo_valor = nv
                            break
                        else:
                            print("Nombre inválido. Use solo letras y espacios (2-30 caracteres).")
                elif campo == "estilo":
                    while True:
                        nv = validarTexto("Nuevo estilo: ", "Texto inválido.")
                        if re.fullmatch(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ\s\-]{3,30}$", nv):
                            nuevo_valor = nv
                            break
                        else:
                            print("Estilo inválido. Use letras, espacios o guiones (3-30 caracteres).")
                else:
                    nuevo_valor = validarTexto("Nuevo valor: ", "Texto inválido.")
            personajes[codigo][campo] = nuevo_valor
            guardar_personajes_csv(personajes)
            guardar_personajes_json(personajes)
            print("Personaje actualizado y guardado en CSV y JSON.")
            return personajes
        else:
            print("Atributo inválido.")
            return personajes
    else:
        print("Personaje no encontrado.")
        return personajes


def eliminar_personaje(personajes):
    """
    Elimina un personaje del diccionario. Retorna el diccionario actualizado.
    """
    codigo = input("Ingrese código del personaje: ").upper().strip()
    if codigo in personajes:
        nombre = personajes[codigo].get("nombre", codigo)
        del personajes[codigo]
        guardar_personajes_csv(personajes)
        guardar_personajes_json(personajes)
        print(f"Personaje {nombre} eliminado y cambios guardados en CSV y JSON.")
        return personajes
    else:
        print("Personaje no encontrado.")
        return personajes

#----------------------------------------------------------------------------------------------
# REPORTES
#----------------------------------------------------------------------------------------------
def reporte_tabla_personajes(personajes):
    """
    Muestra un resumen de los personajes (tabla).
    Ajusta anchos para que los títulos queden alineados.
    """
    if not personajes:
        print("No hay personajes para mostrar.")
        return
    # Usamos DataFrame solo para ordenar columnas; imprimimos con formateo manual
    df = pd.DataFrame.from_dict(personajes, orient='index')
    df.index.name = 'codigo'
    cols = ["nombre", "edad", "peso", "altura", "fuerza"]
    cols_presentes = [c for c in cols if c in df.columns]

    print("\nResumen de personajes:\n")
    # Encabezado con los mismos anchos que en leer_personaje
    print(f"{'Código':<6} {'Nombre':<18} {'Edad':<4} {'Peso':<5} {'Altura':<7} {'Fuerza':<6}")
    print("----------------------------------------------------")
    for codigo, row in df[cols_presentes].iterrows():
        nombre = row.get("nombre", "N/A")
        edad = row.get("edad", "N/D")
        peso = row.get("peso", "N/D")
        altura = row.get("altura", "N/D")
        fuerza = row.get("fuerza", "N/D")
        print(f"{codigo:<6} {str(nombre):<18} {str(edad):<4} {str(peso):<5} {str(altura):<7} {str(fuerza):<6}")


def reporte_por_nacionalidad(personajes):
    """
    Muestra la cantidad de personajes agrupados por nacionalidad.
    Ejemplo de uso de conjunto (set) para identificar nacionalidades únicas:
    nacionalidades_set = set(nacionalidades)  # <-- uso de set
    """
    nacionalidades = [datos.get("nacionalidad", "") for datos in personajes.values()]
    # Uso de conjunto para contar solo una vez cada nacionalidad (tupla o set)
    conteo = {nac: nacionalidades.count(nac) for nac in set(nacionalidades)}
    print("\nPersonajes por nacionalidad:")
    for nac, cant in conteo.items():
        print(f"{nac}: {cant}")

#----------------------------------------------------------------------------------------------
# MAIN
#----------------------------------------------------------------------------------------------
def main():
    # Cargamos datos: JSON -> CSV -> vacío (si no hay archivos)
    personajes = {}  # empezamos vacío; cargamos si hay archivos
    cargado = cargar_personajes_json()  # manejo de excepciones dentro de la función
    if cargado is not None:
        personajes = cargado
    else:
        cargado = cargar_personajes_csv()  # manejo de excepciones dentro de la función
        if cargado is not None:
            personajes = cargado
        else:
            print("No se encontraron archivos de datos. Se iniciará con un diccionario vacío.")

    while True:
        opciones = 7
        print()
        print("---------------------------")
        print("MENÚ CRUD PERSONAJES KOF")
        print("---------------------------")
        print("[1] Crear personaje")
        print("[2] Leer personaje")
        print("[3] Listar todos")
        print("[4] Actualizar personaje")
        print("[5] Eliminar personaje")
        print("[6] Reporte: Tabla de personajes")
        print("[7] Reporte: Por nacionalidad")
        print("---------------------------")
        print("[0] Salir del programa")
        print("---------------------------")
        print()

        valido = False
        while not valido:
            opcion = input("Seleccione una opción: ")
            if opcion in [str(i) for i in range(0, opciones + 1)]:
                valido = True
            else:
                input("Opción inválida. ENTER para volver.")
        print()

        if opcion == "0":
            exit()
        elif opcion == "1":
            personajes = crear_personaje(personajes)
        elif opcion == "2":
            leer_personaje(personajes)
        elif opcion == "3":
            listar_personajes(personajes)
        elif opcion == "4":
            personajes = actualizar_personaje(personajes)
        elif opcion == "5":
            personajes = eliminar_personaje(personajes)
        elif opcion == "6":
            reporte_tabla_personajes(personajes)
        elif opcion == "7":
            reporte_por_nacionalidad(personajes)

        input("\nPresione ENTER para volver al menú.")
        print("\n\n")


# RUN
if __name__ == "__main__":
    main()
