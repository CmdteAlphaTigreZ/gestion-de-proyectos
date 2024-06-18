"""
PROBLEMA

I. Consola de línea de Comando: Este módulo deberá permitir el ingreso de
comandos para ejecutar funciones de los demás módulos a programar. Estos
comandos son: prectangulo, vpiramide, ctiempo, vcubo, regresar(salir del
módulo y regresar al inicio).

II. Perímetro de un rectángulo(prectangulo): Calcular el perímetro de un
rectángulo cuyos datos sean solicitados al usuario.

III. Volumen de una pirámide(vpiramide): Calcular el volumen de una
pirámide cuyos datos sean introducido por el usuario.

IV. Calcular Tiempo(ctiempo): Solicita al usuario una cantidad en horas y
regresa su equivalente días, minutos y segundos.

V. Volumen de un cubo(vcubo): Calcular el volumen de un cubo cuyos
datos sean introducidos por el usuario.

ANÁLISIS

I.

  Datos de entrada:
    * Comando a ejecutar, tipo texto.
    * Todos los demás requeridos por sus módulos.

  Datos de salida:
    * Información de estado para el usuario, tipo texto.
    * Todos los demás provistos por sus módulos.

  Algoritmo base:
    En un ciclo controlado por la comparación de una variable
    que contiene al comando con un dato falso ("regresar"):
      Dar un mensaje de saludo.  Luego si el comando introducido
      es igual a alguno de los disponibles, delegar la ejecución
      del programa al procedimiento correspondiente; de lo contrario,
      indicar un mensaje de error apropiado.

II.

  Datos de entrada:
    * Longitud de la base del rectángulo, tipo real.
    * Altura del rectángulo, tipo real.

  Datos de salida:
    * Perímetro del rectángulo, tipo real.

  Algoritmo base:
    Se suma la longitud de la base del rectángulo con su altura
    y el resultado se multiplica por dos para obtener su perímetro.

III.

  Datos de entrada:
    * Área de la base de la pirámide, tipo real.
    * Altura de la pirámide, tipo real.

  Datos de salida:
    * Volumen de la pirámide, tipo real.

  Algoritmo base:
    Se multiplica el área de la base de la pirámide por su altura
    y se divide entre 3 para obtener su volumen.

IV.

  Datos de entrada:
    * Horas, tipo real.

  Datos de salida:
    * Tiempo equivalente en (juntos):
        * Días, tipo entero.
        * Minutos, tipo entero.
        * Segundos, tipo real.

  Algoritmo base:
    Se calcula la parte entera de la división de las horas entre 24
    para obtener los días; luego se calcula el resto de la división anterior
    y se toma como las horas restantes a convertir.
    Se multiplican las horas restantes por 60 para obtener los minutos
    con decimales.  Luego se calcula el resto de la división de los minutos
    entre 1 para obtener la parte decimal que al multiplicarse luego por 60
    se obtienen los segundos.  Finalmente, se calcula la parte entera
    de la división de los minutos con decimales entre 1 para obtener los
    minutos enteros.

V.

  Datos de entrada:
    * Longitud de la arista del cubo, tipo real.

  Datos de salida:
    * Volumen del cubo, tipo real.

  Algoritmo base:
    Se eleva la longitud de la arista del cubo al cubo (a la potencia de 3)
    para obtener su volumen.
"""

# Descripción POR HACER!!!
#
# Autores: Francisco Román, Francisco Unda y Santiago Pinto
# Fecha: 2024-06-14
# Cambios:
#   v1
#     * Versión inicial

info = dict
info = {
        "prectangulo": {
            "sintaxis": "prectangulo [base altura]",
            "descripcion": "Perímetro de un rectángulo",
            "comando": None
        },
        "vpiramide": {
            "sintaxis": "vpiramide [base altura]",
            "descripcion": "Volumen de una pirámide",
            "comando": None
        },
        "ctiempo": {
            "sintaxis": "ctiempo [horas]",
            "descripcion": "Horas a días, minutos y segundos",
            "comando": None
        },
        "vcubo": {
            "sintaxis": "vcubo [arista]",
            "descripcion": "Volumen de un cubo",
            "comando": None
        },
        "leerconfig": {
            "sintaxis": "leerconfig",
            "descripcion": "Ver el archivo de configuración",
            "comando": None
        },
        "errores": {
            "sintaxis": "errores",
            "descripcion": "Ver el registro de errores",
            "comando": None
        },
        "historial": {
            "sintaxis": "historial",
            "descripcion": "Ver el historial de operaciones",
            "comando": None
        }
       }

# alineacion es la longitud del texto de sintaxis más largo añadiendo unos
# caracteres extra de separación, aquí son 4 de separación.
alineacion = str
alineacion = " " * 29

ruta_errores = "errores.log.txt"
errores = list([ dict(tipo="Tipo de error.",
                      origen="Componente de origen del error.",
                      mensaje="Mensaje de error.") ])
ruta_historial = "historial.log.txt"
historial = list([ list([ str("Línea de comando"), str("Resultado") ]) ])
ruta_configuracion = "calculadora.ini"

def main():
    print("Calculadora científica.",
          "", sep="\n")
    configurar()
    cargar_errores()
    cargar_historial()
#   Lo siguiente es para comprobar errores
#    print(configuracion)
#    print(info)
    consola()
    guardar_historial()

def consola():
    "Procedimiento que implementa la interfaz en línea de comandos."

    # "ayuda = list" , luego "ayuda = str"
    ayuda = ["Comandos disponibles:"]
    for cmd in info.values():
        largo = len(cmd["sintaxis"])
        ayuda.append("".join([ "  ",
                               cmd["sintaxis"],
                               alineacion[largo:],
                               cmd["descripcion"] ]))
    ayuda.append("  regresar" + alineacion[8:] + "Salir de la calculadora\n")
    ayuda = "\n".join(ayuda)
    print(ayuda)
    
    linea_comando = list()
    comando = str
    leer_comando(linea_comando)
    comando = linea_comando[0]
    while comando != "regresar" or len(linea_comando) != 1:
        if comando == "regresar":
            mensaje_e = "Error: Sintaxis inválida: regresar no toma argumentos."
            print(mensaje_e)
            registrar_error("Sintaxis", "Consola", mensaje_e)
        else:
            try:
                # resultado = {"resultado": mensaje, "tipo_error": si_lo_hay}
                resultado = info[comando]["comando"](linea_comando)
                print(resultado["resultado"])
                if resultado["tipo_error"] == "":
                    if comando not in ["leerconfig", "errores", "historial"]:
                        registrar_comando(linea_comando, resultado["resultado"])
                    else:
                        registrar_comando(linea_comando, "Resultado omitido...")
                else:
                    registrar_error(resultado["tipo_error"],
                                    comando,
                                    resultado["resultado"])
            except KeyError as e:
                mensaje_e = "Error: Comando desconocido: " + comando
                print(mensaje_e)
                registrar_error("No implementado", "Consola", mensaje_e)
        linea_comando = []
        leer_comando(linea_comando)
        comando = linea_comando[0]
    print("Saliendo de la calculadora...")

def leer_comando(linea_comando):
    error = bool
    error = True
    while error:
        try:
            linea_comando.extend( input(">> ").split() )
        # Esta excepcion que sigue no debe ser capturada, está mal.
        except EOFError as e:
            pass
        except UnicodeError as e:
            mensaje_e = "Error: Texto de entrada por consola inválido."
            print(mensaje_e)
            registrar_error("Codificación de texto", "Consola", mensaje_e)
        else:
            if len(linea_comando) != 0:
                error = False

def registrar_comando(linea_comando, resultado):
    "Registra los comandos ejecutados y sus resultados internamente."

    global historial
    historial.append( [" ".join(linea_comando), resultado] )

def registrar_error(tipo, origen, mensaje):
    "Registra errores en un archivo de registro de errores e internamente.\
 Acepta tres textos."

    global errores
    errores.append({"tipo": tipo, "origen": origen, "mensaje": mensaje})
    try:
        with open(ruta_errores, "a") as registro:
            contenido = "".join([ "Tipo: ", tipo, "\n",
                                  "Origen: ", origen, "\n",
                                  mensaje, "\n\n" ])
            registro.write(contenido)
    except OSError as e:
        mensaje_e = "Error: No se pudo abrir el registro de errores."
        print(mensaje_e +
              " El error se mantendrá almacenado de manera no permanente.")
        errores.append({"tipo": "Archivo",
                        "origen": "Registro de errores",
                        "mensaje": mensaje_e})

def configurar():
    "Procedimiento que configura la calculadora."

    global ruta_errores, ruta_historial, info
    try:
        configuracion = procesar_ini(ruta_configuracion)
    except OSError as e:
        mensaje_e = "Error: No se pudo abrir el archivo de configuración."
        print(mensaje_e,
              "Info: Se utilizará una configuración predefinida.",
              "", sep="\n")
        registrar_error("Archivo", "Configuración", mensaje_e)
        return
    except UnicodeError as e:
        mensaje_e = "Error: Archivo de configuración con texto inválido."
        print(mensaje_e,
              "Info: Se utilizará una configuración predefinida.",
              "", sep="\n")
        registrar_error("Codificación de texto", "Configuración", mensaje_e)
        return
    except ValueError as e:
        mensaje_e = \
               "Error: El archivo de configuración tiene un formato incorrecto."
        print(mensaje_e,
              "Info: Se utilizará una configuración predefinida.",
              "", sep="\n")
        registrar_error("Sintaxis", "Configuración", mensaje_e)
        return

    if "registros" in configuracion:
        errores = configuracion["registros"].get("errores", "")
        if errores != "":
            ruta_errores = errores
        historial = configuracion["registros"].get("historial", "")
        if historial != "":
            ruta_historial = historial
    if "modulos" in configuracion:
        modulos = []
        for nombre in info:
            modulos.append(nombre)
        for modulo in modulos:
            activar = configuracion["modulos"].get(modulo, "")
            activar = str(activar).lower()
            if activar in ["0", "no", "false"]:
                del info[modulo]
            elif activar not in ["1", "si", "sí", "yes", "true", ""]:
                mensaje_e = \
                    "Error: Valor de módulo inválido en la configuración: " + \
                    modulo + " = " + activar
                print(mensaje_e)
                registrar_error("Sintaxis", "Configuración", mensaje_e)

def procesar_ini(ruta):
    "Procesa un archivo INI y devuelve su contenido como diccionario."

    ini = dict()
    with open(ruta) as archivo:
        seccion = ""
        for linea in archivo:
            linea = linea.strip()
            if linea == "":
                continue
            if linea[0] == ";":
                continue
            if linea[0] == "[" and linea[-1] == "]":
                seccion = linea[1:-1]
                validar_datos_ini(seccion, "seccion")
                seccion = seccion.lower()
                ini[seccion] = {}
                break
            else:
                raise ValueError(
                    "El archivo INI debe comenzar con una sección.")
        for linea in archivo:
            linea = linea.strip()
            if linea == "":
                continue
            if linea[0] == ";":
                continue
            if linea[0] == "[" and linea[-1] == "]":
                seccion = linea[1:-1]
                validar_datos_ini(seccion, "seccion")
                seccion = seccion.lower()
                ini[seccion] = {}
                continue
            par = linea.split("=", 1)
            if len(par) != 2:
                raise ValueError(
                    "Los pares nombre=valor deben separarse con '='.")
            nombre = par[0].strip()
            valor = par[1].strip()
            validar_datos_ini(nombre, "nombre")
            try:
                valor = int(valor)
            except ValueError as e:
                try:
                    valor = a_float(valor)
                except ValueError as e:
                    # No es un número
                    if valor[0] == '"' == valor[-1]:
                        valor = valor[1:-1]
            ini[seccion][nombre.lower()] = valor
    return ini

def validar_datos_ini(dato, tipo):
    "Valida datos de un archivo INI, segun el tipo indicado. Acepta dos textos."

    if not dato.isprintable():
        raise ValueError(
            "No se permiten caracteres no imprimibles en los datos.")
    if tipo == "seccion" or tipo == "nombre":
        for inaceptable in (";", "=", "[", "]"):
            if inaceptable in dato:
                raise ValueError(
                    "No se permite '" + inaceptable + "' en '" + tipo +"' INI.")

def cargar_historial():
    "Procedimiento que carga el historial del archivo al registro interno."

    global historial
    try:
        registro = open(ruta_historial)
        entrada = list(["", ""])
        primera_linea = ""
        for linea in registro:
            if linea != "\n":
                primera_linea = linea
                break
        entrada = [primera_linea, registro.readline()]
        while entrada[0] != "" and entrada[1] != "":
                historial.append(entrada)
                entrada = ["", ""]
                entrada[0] = registro.readline()
                entrada[1] = registro.readline()
                registro.readline()
        registro.close()
    except OSError as e:
        mensaje_e = "Error: No se pudo abrir el historial para cargarlo."
        print(mensaje_e)
        registrar_error("Archivo", "Historial", mensaje_e)
    except UnicodeError as e:
        registro.close()
        mensaje_e = "Error: Archivo de historial con texto inválido."
        print(mensaje_e)
        registrar_error("Codificación de texto", "Historial", mensaje_e)    

def guardar_historial():
    "Procedimiento que guarda el historial del registro interno al archivo."

    try:
        with open(ruta_historial, "a") as registro:
            for i in range(1, len(historial)):
                entrada = historial[i]
                contenido = "\n".join(entrada + ["\n"])
                registro.write(contenido)
    except OSError as e:
        mensaje_e = "Error: No se pudo abrir el historial para guardarlo."
        print(mensaje_e)
        registrar_error("Archivo", "Historial", mensaje_e)

def cargar_errores():
    "Procedimiento que carga los errores del archivo al registro interno."

    global errores
    try:
        registro = open(ruta_errores)
        error = dict(tipo="", origen="", mensaje="")
        for linea in registro:
            if linea == "\n":
                errores.append(error)
                error = dict(tipo="", origen="", mensaje="")
            elif linea[:6] == "Tipo: ":
                error["tipo"] = linea[6:-1]
            elif linea[:8] == "Origen: ":
                error["origen"] = linea[8:-1]
            else:
                error["mensaje"] = linea[:-1]
        registro.close()
    except OSError as e:
        mensaje_e = \
                 "Error: No se pudo abrir el registro de errores para cargarlo."
        print(mensaje_e)
        registrar_error("Archivo", "Registro de errores", mensaje_e)
    except UnicodeError as e:
        registro.close()
        mensaje_e = "Error: Archivo de registro de errores con texto inválido."
        print(mensaje_e)
        registrar_error(\
            "Codificación de texto", "Registro de errores", mensaje_e)

def cmd_prectangulo(linea_comando):
    "Comando prectangulo. Acepta lista de texto y devuelve diccionario de texto."

    base = float
    altura = float
    perimetro = float
    argumentos = list([float])
    try:
        argumentos = leer_argumentos(linea_comando, [
            "Indique la longitud de la base del rectángulo: ",
            "Indique la altura del rectángulo: " ])
    except ValueError as e:
        return {"resultado": e.args[0], "tipo_error": "Valor"}
    except SyntaxError as e:
        return {"resultado": e.args[0], "tipo_error": "Sintaxis"}
    except UnicodeError as e:
        return {"resultado": e.args[0], "tipo_error": "Codificación de texto"}
    base = argumentos[0]
    altura = argumentos[1]
    if base <= 0 or altura <= 0:
        return {"resultado": "Error: Las medidas deben ser positivas.",
                "tipo_error": "Valor"}
    perimetro = prectangulo(base, altura)
    return {"resultado": "El perímetro del rectángulo es: " + str(perimetro),
            "tipo_error": ""}

info["prectangulo"]["comando"] = cmd_prectangulo

def prectangulo(base, altura):
    "Perímetro de un rectángulo."
    return 2 * (base + altura)

def cmd_vpiramide(linea_comando):
    "Comando vpiramide. Acepta lista de texto y devuelve diccionario de texto."

    base = float
    altura = float
    volumen = float
    argumentos = list([float])
    try:
        argumentos = leer_argumentos(linea_comando, [
            "Indique el área de la base de la pirámide: ",
            "Indique la altura de la pirámide: " ])
    except ValueError as e:
        return {"resultado": e.args[0], "tipo_error": "Valor"}
    except SyntaxError as e:
        return {"resultado": e.args[0], "tipo_error": "Sintaxis"}
    except UnicodeError as e:
        return {"resultado": e.args[0], "tipo_error": "Codificación de texto"}
    base = argumentos[0]
    altura = argumentos[1]
    if base <= 0 or altura <= 0:
        return {"resultado": "Error: Las medidas deben ser positivas.",
                "tipo_error": "Valor"}
    volumen = vpiramide(base, altura)
    return {"resultado": "El volumen de la pirámide es: " + str(volumen),
            "tipo_error": ""}

info["vpiramide"]["comando"] = cmd_vpiramide

def vpiramide(base, altura):
    "Volumen de una pirámide."
    return base * altura / 3

def cmd_ctiempo(linea_comando):
    "Comando ctiempo. Acepta lista de texto y devuelve diccionario de texto."

    horas = float
    tiempo = list([int, int, float])
    argumentos = list([float])
    try:
        argumentos = leer_argumentos(linea_comando, [
            "Indique la cantidad de horas: " ])
    except ValueError as e:
        return {"resultado": e.args[0], "tipo_error": "Valor"}
    except SyntaxError as e:
        return {"resultado": e.args[0], "tipo_error": "Sintaxis"}
    except UnicodeError as e:
        return {"resultado": e.args[0], "tipo_error": "Codificación de texto"}
    horas = argumentos[0]
    if horas <= 0:
        return {"resultado": "Error: El tiempo debe ser positivo.",
                "tipo_error": "Valor"}
    tiempo = ctiempo(horas)
    return {"resultado": \
            ("La cantidad de horas es equivalente a " +
            str(tiempo[0]) + " días, " + str(tiempo[1]) + " minutos y " +
            str(tiempo[2]) + " segundos."),
            "tipo_error": ""}

info["ctiempo"]["comando"] = cmd_ctiempo

def ctiempo(horas):
    "\
Conversión de horas a días, minutos y segundos.\
 Devuelve lista de cantidades de días, minutos y segundos."

    # dias y minutos se devuelven como enteros (int)
    dias = float
    minutos = float
    segundos = float
    tiempo = list([int, int, float])

    dias = 0
    minutos = 0
    segundos = 0.0
    tiempo = [dias, minutos, segundos]

    dias = horas // 24
    horas = horas % 24
    minutos = horas * 60
    segundos = (minutos % 1) * 60
    minutos = minutos // 1
    tiempo = [int(dias), int(minutos), segundos]
    return tiempo

def cmd_vcubo(linea_comando):
    "Comando vcubo. Acepta lista de texto y devuelve diccionario de texto."

    arista = float
    volumen = float
    argumentos = list([float])
    try:
        argumentos = leer_argumentos(linea_comando, [
            "Indique la longitud de la arista: " ])
    except ValueError as e:
        return {"resultado": e.args[0], "tipo_error": "Valor"}
    except SyntaxError as e:
        return {"resultado": e.args[0], "tipo_error": "Sintaxis"}
    except UnicodeError as e:
        return {"resultado": e.args[0], "tipo_error": "Codificación de texto"}
    arista = argumentos[0]
    if arista <= 0:
        return {"resultado": "Error: Las medidas deben ser positivas.",
                "tipo_error": "Valor"}
    volumen = vcubo(arista)
    return {"resultado": "El volumen del cubo es: " + str(volumen),
            "tipo_error": ""}

info["vcubo"]["comando"] = cmd_vcubo

def vcubo(arista):
    "Volumen de un cubo."
    return arista ** 3

def cmd_leerconfig(linea_comando):
    "Comando leerconfig. Acepta lista de texto y devuelve diccionario de texto."

    argumentos = list()
    try:
        # Este comando no tiene parámetros, serán rechazados.
        argumentos = leer_argumentos(linea_comando, [])
    except ValueError as e:
        return {"resultado": e.args[0], "tipo_error": "Valor"}
    except SyntaxError as e:
        return {"resultado": e.args[0], "tipo_error": "Sintaxis"}
    except UnicodeError as e:
        return {"resultado": e.args[0], "tipo_error": "Codificación de texto"}
    configuracion = leerconfig()
    return configuracion

info["leerconfig"]["comando"] = cmd_leerconfig

def leerconfig():
    "Devuelve el contenido del archivo de configuración"

    configuracion = str()
    # Realmente es de uno de los tipos de archivo
    archivo = open
    try:
        archivo = open(ruta_configuracion)
        configuracion = archivo.read()
    except OSError as e:
        return {\
            "resultado": "Error: No se pudo abrir el archivo de configuración.",
            "tipo_error": "Archivo"}
    except UnicodeError as e:
        return {\
            "resultado": "Error: Archivo de configuración con texto inválido.",
            "tipo_error": "Codificación de texto"}
    archivo.close()
    return {"resultado": "\n" + configuracion + "\n",
            "tipo_error": ""}

def cmd_errores(linea_comando):
    "Comando errores. Acepta lista de texto y devuelve diccionario de texto."

    argumentos = list()
    try:
        # Este comando no tiene parámetros, serán rechazados.
        argumentos = leer_argumentos(linea_comando, [])
    except ValueError as e:
        return {"resultado": e.args[0], "tipo_error": "Valor"}
    except SyntaxError as e:
        return {"resultado": e.args[0], "tipo_error": "Sintaxis"}
    except UnicodeError as e:
        return {"resultado": e.args[0], "tipo_error": "Codificación de texto"}
    errores = verrores()
    return {"resultado": errores,
            "tipo_error": ""}

info["errores"]["comando"] = cmd_errores

def verrores():
    "Devuelve un listado del registro de errores."

    # "listado = list(str)" , luego "listado = str"
    listado = list()
    for error in errores:
        listado.append("\n".join([ "Tipo: " + error["tipo"],
                                   "Origen: " + error["origen"],
                                   error["mensaje"],
                                   "" ]))
    listado = "\n".join(listado) + "\n"
    return listado

def cmd_historial(linea_comando):
    "Comando historial. Acepta lista de texto y devuelve diccionario de texto."

    argumentos = list()
    try:
        # Este comando no tiene parámetros, serán rechazados.
        argumentos = leer_argumentos(linea_comando, [])
    except ValueError as e:
        return {"resultado": e.args[0], "tipo_error": "Valor"}
    except SyntaxError as e:
        return {"resultado": e.args[0], "tipo_error": "Sintaxis"}
    except UnicodeError as e:
        return {"resultado": e.args[0], "tipo_error": "Codificación de texto"}
    historial = vhistorial()
    return {"resultado": historial,
            "tipo_error": ""}

info["historial"]["comando"] = cmd_historial

def vhistorial():
    "Devuelve un listado del historial."

    # "listado = list(str)" , luego "listado = str"
    listado = list()
    for entrada in historial:
        listado.append("\n".join(entrada) + "\n")
    listado = "\n".join(listado) + "\n"
    return listado

def leer_argumentos(linea_comando, mensajes):
    """\
Lee argumentos de la línea de comandos y del usuario.\
 Acepta dos listas de texto y devuelve una lista de flotantes.

Esta función obtiene los argumentos para un comando
de la línea de comando sólo si todos están en ella,
de lo contrario los solicita al usuario mostrando uno
de los mensajes para cada argumento requerido sólo si
no se proporciona ninguno en la línea de comando;
levanta una excepción de uso inapropiado de no cumplirse
alguna de estas condiciones.  Se considera que la cantidad
de argumentos requeridos por el comando es la cantidad
de mensajes para el usuario que recibe esta función
como parámetro.

Se devuelve una lista de todos los argumentos del comando
en el orden en que se recibieron los mensajes al usuario
para ellos, convertido cada uno en "float".

Debe capturarse desde el comando la excepción ValueError
que puede levantar esta función.
"""

    len_linea_comando = len(linea_comando)
    len_mensajes = len(mensajes)
    # "argumentos = list([str])" , luego "argumentos = list([float])"
    argumentos = [""] * len_mensajes

    if len_linea_comando - 1 == len_mensajes:
        for i in range(len_mensajes):
            argumentos[i] = linea_comando[i + 1]
    elif len_linea_comando == 1:
        try:
            for i in range(len_mensajes):
                argumentos[i] = input(mensajes[i])
        except EOFError as e:
            raise ValueError("Error: No se proporcionó el dato.")\
                  from e
        except UnicodeError as e:
            raise UnicodeError("Error: Texto de entrada por consola inválido.")\
                  from e
    else:
        raise SyntaxError(
            "Error: Sintaxis inválida: " + info[linea_comando[0]]["sintaxis"])
    for i in range(len_mensajes):
        argumentos[i] = a_float(argumentos[i])
    return argumentos

def a_float(valor):
    "Conversion a número de coma flotante."
    inicial = valor
    try:
        if type(valor) == str:
            valor = valor.replace("," , ".")
            if valor.count(".") > 1:
                raise ValueError("\
Error: Los números pueden tener sólo un separador decimal.")
        valor = float(valor)
        return valor
    except ValueError as e:
        if e.args[0][:5] != "Error":
            raise ValueError("Error: Valor numérico inválido: " + str(inicial))\
                  from e
        else:
            raise

main()
