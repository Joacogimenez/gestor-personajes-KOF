"""
-----------------------------------------------------------------------------------------------
Título: Personajes KOF
Fecha: 
Autor: Grupo 7
Descripción: 
    Programa que gestiona un diccionario de personajes del juego KOF. 
    Incluye validaciones de entrada, un menú CRUD y reportes.
-----------------------------------------------------------------------------------------------
"""


#----------------------------------------------------------------------------------------------
# DICCIONARIO
#----------------------------------------------------------------------------------------------
# Diccionario de personajes
personajes = {
    "K001": {
        "nombre": "Kyo Kusanagi",
        "nacionalidad": "Japón",
        "estilo": "Kusanagi style",
        "edad": 20,
        "peso": 75,     # Todos los pesos están en kg
        "altura": 180,  # Todas las alturaas están en cm
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
# FUNCIONES DE VALIDACIÓN
#----------------------------------------------------------------------------------------------
def validarNumero(msj, msE, msE2, mini, maxi):
    """ 
    Valida que el número ingresado sea entero y esté dentro de un rango.
    Parámetros:
        msj (str): mensaje de solicitud
        msE (str): mensaje si no es número
        msE2 (str): mensaje si no está en rango
        mini (int): mínimo aceptado
        maxi (int): máximo aceptado
    Retorna:
        int: número validado
    """
    flag = True 
    while flag:
        valor = input(msj)
        if valor.isnumeric():
            if  mini <= int(valor) <= maxi:
                flag = False
            else:
                print(msE2)
        else:
            print(msE)
    return int(valor)

def validarTexto(msj, msE):
    """
    Valida que el texto ingresado no esté vacío ni contenga solo números.
    Parámetros:
        msj (str): mensaje de solicitud
        msE (str): mensaje de error
    Retorna:
        str: texto validado
    """
    while True:
        valor = input(msj).strip()
        if valor.isalpha() or " " in valor: 
            return valor
        else:
            print(msE)

#----------------------------------------------------------------------------------------------
# FUNCIONES
#----------------------------------------------------------------------------------------------
def crear_personaje():
    """ 
    Crea un nuevo personaje y lo agrega al diccionario de personajes. 
    Pide todos los atributos validados por las funciones de validación.
    """
    codigo = input("Ingrese código (ej: K006): ").upper()
    if codigo in personajes:
        print("El código ya existe.")
        return
    nombre = validarTexto("Nombre: ", "Texto inválido.")
    nacionalidad = validarTexto("Nacionalidad: ", "Texto inválido.")
    estilo = validarTexto("Estilo: ", "Texto inválido.")
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
    print(f"\nEl Personaje {nombre} fue creado.")

def leer_personaje():
    """ 
    Muestra la información de un personaje específico, según su código. 
    Si el código no existe, muestra mensaje de error.
    """
    codigo = input("Ingrese código: ").upper()
    if codigo in personajes:
        print(personajes[codigo])
    else:
        print("Personaje no encontrado.")

def listar_personajes():
    """ 
    Lista todos los personajes del diccionario mostrando código, nombre y nacionalidad. 
    """
    print("\nLista de personajes:")
    for codigo, datos in personajes.items():
        print(f"{codigo}: {datos['nombre']} ({datos['nacionalidad']})")

def actualizar_personaje():
    """ 
    Permite actualizar un atributo de un personaje existente. 
    Valida el nuevo valor según tipo de dato.
    """
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
            print("Personaje actualizado.")
        else:
            print("Atributo inválido.")
    else:
        print("Personaje no encontrado.")

def eliminar_personaje():
    """ 
    Elimina un personaje del diccionario según su código. 
    Si no existe, muestra mensaje de error.
    """
    codigo = input("Ingrese código del personaje: ").upper()
    if codigo in personajes:
        del personajes[codigo]
        print("Personaje eliminado.")
    else:
        print("Personaje no encontrado.")

#----------------------------------------------------------------------------------------------
# REPORTES
#----------------------------------------------------------------------------------------------
def reporte_tabla_personajes():
    """ 
Muestra una tabla con los datos principales de todos los personajes. 
Incluye: código, nombre, edad, peso, altura y fuerza.
    """
    print("\nTabla de personajes:")
    # Encabezado
    print(f"{'Código':<6} {'Nombre':<18} {'Edad':<4} {'Peso':<4} {'Altura':<6} {'Fuerza'}")
    print("--------------------------------------")
    # Filas
    for codigo, datos in personajes.items():
        print(f"{codigo:<6} {datos['nombre']:<18} {datos['edad']:<4} {datos['peso']:<4} {datos['altura']:<6} {datos['fuerza']}")


def reporte_por_nacionalidad():
    """ 
    Muestra la cantidad de personajes agrupados por nacionalidad. 
    Utiliza un conjunto para contar cada nacionalidad solo una vez.
    """
    nacionalidades = [datos["nacionalidad"] for datos in personajes.values()]
    conteo = {nac: nacionalidades.count(nac) for nac in set(nacionalidades)} 
    print("\nPersonajes por nacionalidad:")
    for nac, cant in conteo.items():
        print(f"{nac}: {cant}")

#----------------------------------------------------------------------------------------------
# CUERPO PRINCIPAL
#----------------------------------------------------------------------------------------------
def main():
    """
    Función principal que ejecuta el programa.
    """
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
        
       
        # Validación de opción
        valido = False
        while not valido:
            opcion = input("Seleccione una opción: ")
            if opcion in [str(i) for i in range(0, opciones + 1)]:
                valido = True  
            else:
                input("Opción inválida. ENTER para volver.")
        print()

        

        # Ejecución según opción
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


#RUN
if __name__ == "__main__":
    main()
