"""
-----------------------------------------------------------------------------------------------
Título: Personajes KOF
Fecha: 
Autor: Grupo 7
Descripción: 
    Programa que gestiona un diccionario de personajes del juego KOF. 
    Incluye validaciones de entrada, un menú CRUD, reportes y persistencia en CSV.
-----------------------------------------------------------------------------------------------
"""
#----------------------------------------------------------------------------------------------
# MÓDULOS
#----------------------------------------------------------------------------------------------

import pandas as pd  # para guardar y cargar datos en CSV

#----------------------------------------------------------------------------------------------
# DICCIONARIO
#----------------------------------------------------------------------------------------------
personajes = {
    "K001": {
        "nombre": "Kyo Kusanagi",
        "nacionalidad": "Japón",
        "estilo": "Kusanagi style",
        "edad": 20,
        "peso": 75,
        "altura": 180,
        "fuerza": 88
    },
    "K002": {
        "nombre": "Terry Bogard",
        "nacionalidad": "EEUU",
        "estilo": "Martial arts",
        "edad": 24,
        "peso": 82,
        "altura": 182,
        "fuerza": 90
    },
    "K003": {
        "nombre": "Robert Garcia",
        "nacionalidad": "Italia",
        "estilo": "Kyokugenryu Karate",
        "edad": 23,
        "peso": 85,
        "altura": 180,
        "fuerza": 84
    },
    "K004": {
        "nombre": "Ramón",
        "nacionalidad": "México",
        "estilo": "Lucha Libre",
        "edad": 25,
        "peso": 80,
        "altura": 170,
        "fuerza": 86
    },
    "K005": {
        "nombre": "Chin Gentsai",
        "nacionalidad": "China",
        "estilo": "Kung-fu",
        "edad": 70,
        "peso": 68,
        "altura": 168,
        "fuerza": 78
    }
}

#----------------------------------------------------------------------------------------------
# PERSISTENCIA DE DATOS
#----------------------------------------------------------------------------------------------
def guardar_personajes_csv():
    """
    Guarda los personajes actuales en un archivo CSV usando pandas.
    El archivo se llama 'personajes.csv' y sobrescribe los datos anteriores.
    """
    df = pd.DataFrame.from_dict(personajes, orient='index')
    df.index.name = 'codigo'
    df.to_csv('personajes.csv', index=True)
    print("Datos guardados en 'personajes.csv'.")

def cargar_personajes_csv():
    """
    Carga los personajes desde 'personajes.csv' si el archivo existe.
    Si no se encuentra o hay error, mantiene el diccionario inicial.
    """
    global personajes
    try:
        df = pd.read_csv('personajes.csv', index_col='codigo')
        personajes = df.to_dict(orient='index')
        print("Datos cargados desde 'personajes.csv'.")
    except FileNotFoundError:
        print("Archivo 'personajes.csv' no encontrado. Se usará el diccionario inicial.")
    except Exception as e:
        print(f"Error al cargar los personajes: {e}")
        print("Se usará el diccionario inicial.")

#----------------------------------------------------------------------------------------------
# FUNCIONES DE VALIDACIÓN
#----------------------------------------------------------------------------------------------
def validarNumero(msj, msE, msE2, mini, maxi):
    flag = True 
    while flag:
        valor = input(msj)
        if valor.isnumeric():
            if mini <= int(valor) <= maxi:
                flag = False
            else:
                print(msE2)
        else:
            print(msE)
    return int(valor)

def validarTexto(msj, msE):
    while True:
        valor = input(msj).strip()
        if valor.isalpha() or " " in valor: 
            return valor
        else:
            print(msE)

#----------------------------------------------------------------------------------------------
# FUNCIONES CRUD
#----------------------------------------------------------------------------------------------
def crear_personaje():
    codigo = input("Ingrese código (ej: K006): ").upper()
    if codigo in personajes:
        print("El código ya existe.")
        return
    nombre = validarTexto("Nombre: ", "Texto inválido.")
    nacionalidad = validarTexto("Nacionalidad: ", "Texto inválido.")
    estilo = validarTexto("Estilo: ", "Texto inválido.")
    edad = validarNumero("Edad: ", "No es número.", "Edad fuera de rango.", 10, 80) #tupla de argumentos
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
    guardar_personajes_csv()
    print(f"\nEl personaje {nombre} fue creado y guardado en CSV.")

def leer_personaje():
    codigo = input("Ingrese código: ").upper()
    if codigo in personajes:
        print(personajes[codigo])
    else:
        print("Personaje no encontrado.")

def listar_personajes():
    print("\nLista de personajes:")
    for codigo, datos in personajes.items():
        print(f"{codigo}: {datos['nombre']} ({datos['nacionalidad']})")

def actualizar_personaje():
    codigo = input("Ingrese código del personaje: ").upper()
    if codigo in personajes:
        print("Datos actuales:", personajes[codigo])
        campo = input("Atributo a modificar (nombre, nacionalidad, estilo, edad, peso, altura, fuerza): ").lower()
        if campo in personajes[codigo]:
            if campo in ["edad", "peso", "altura", "fuerza"]:
                nuevo_valor = validarNumero("Nuevo valor: ", "No es número.", "Fuera de rango.", 0, 200)
            else:
                nuevo_valor = validarTexto("Nuevo valor: ", "Texto inválido.")
            personajes[codigo][campo] = nuevo_valor
            guardar_personajes_csv()
            print("Personaje actualizado y guardado en CSV.")
        else:
            print("Atributo inválido.")
    else:
        print("Personaje no encontrado.")

def eliminar_personaje():
    codigo = input("Ingrese código del personaje: ").upper()
    if codigo in personajes:
        del personajes[codigo]
        guardar_personajes_csv()
        print("Personaje eliminado y cambios guardados en CSV.")
    else:
        print("Personaje no encontrado.")

#----------------------------------------------------------------------------------------------
# REPORTES
#----------------------------------------------------------------------------------------------
def reporte_tabla_personajes():
    print("\nTabla de personajes:")
    print(f"{'Código':<6} {'Nombre':<18} {'Edad':<4} {'Peso':<4} {'Altura':<6} {'Fuerza'}")
    print("-------------------------------------------------")
    for codigo, datos in personajes.items():
        print(f"{codigo:<6} {datos['nombre']:<18} {datos['edad']:<4} {datos['peso']:<4} {datos['altura']:<6} {datos['fuerza']}")

def reporte_por_nacionalidad():
    nacionalidades = [datos["nacionalidad"] for datos in personajes.values()] #Lista por comprension
    conteo = {nac: nacionalidades.count(nac) for nac in set(nacionalidades)} 
    print("\nPersonajes por nacionalidad:")
    for nac, cant in conteo.items():
        print(f"{nac}: {cant}")

#----------------------------------------------------------------------------------------------
# MAIN
#----------------------------------------------------------------------------------------------
def main():
    cargar_personajes_csv()  #carga automática antes del menú

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
            crear_personaje()
        elif opcion == "2":
            leer_personaje()
        elif opcion == "3":
            listar_personajes()
        elif opcion == "4":
            actualizar_personaje()
        elif opcion == "5":
            eliminar_personaje()
        elif opcion == "6":
            reporte_tabla_personajes()
        elif opcion == "7":
            reporte_por_nacionalidad()

        input("\nPresione ENTER para volver al menú.")
        print("\n\n")

# RUN
if __name__ == "__main__":
    main()
