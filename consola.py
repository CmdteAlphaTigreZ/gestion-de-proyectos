# Módulo de interfaz en línea de comandos para el programa de
# gestión de proyectos
# Autor: Francisco Román, Francisco Unda y Santiago Pinto
# Fecha: 2024-06-15
# Cambios:
#   v1
#     * Versión inicial


import utilidades as util
funcion_t = util.funcion_t


class Comando:
    """
    Comando de consola que llama a una función con los argumentos de consola

    'ayuda' debe estar en la cadena de documentación de la función y sirve
      como pista para el usuario acerca de la funcionalidad del comando
    'sintaxis' es un texto que muestra la sintaxis válida con que se puede
      llamar al comando
    'descripción' es un texto de ayuda más extenso que describe toda la
      funcionalidad del comando
    'funcion' es una función que recibirá los argumentos de la línea de
      comandos, tomará el control de la consola, y luego *debe devolver su
      resultado como un objeto 'Resultado'*, no se debe mostrar en la consola
    """

    def __init__(self, funcion, sintaxis, descripcion=""):
        util.comprobar_tipos(
            ("ayuda", "sintaxis", "descripcion", "funcion"),
            (funcion.__doc__, sintaxis, descripcion, funcion),
            (str, str, str, funcion_t)
        )
        self.ayuda = funcion.__doc__
        self.sintaxis = sintaxis
        self.descripcion = descripcion
        self.funcion = funcion

    def __call__(self, linea_comando):
        resultado = self.funcion(linea_comando)
        util.comprobar_tipos(("resultado",), (resultado,), (Resultado))
        return resultado

    def __str__(self):
        "Devuelve la sintaxis del comando"
        return self.sintaxis


class Resultado:
    "Resultado de Comando"

    def __init__(self, resultado, origen, tipo_error=None):
        util.comprobar_tipos(("resultado",), (resultado,), (str,))
        if tipo_error is not None:
            util.comprobar_tipos(("tipo_error",), (tipo_error,), (str,))
        self.resultado = resultado
        self.origen = origen
        self.tipo_error = tipo_error


class Consola:
    "Interfaz en línea de comandos"

    def __init__(self, comandos):
        # ¿Algo que añadir aquí?
        util.comprobar_tipos(("comandos",), (comandos,), (dict,))
        util.comprobar_tipos(("comando",) * len(comandos),
                             tuple(comandos.values()),
                             (Comando,) * len(comandos))

        self.comandos = comandos.copy()  # Es público pero mejor no modificar
                                         # arbitrariamente
        self.comandos["ayuda"] = self.ayuda
        self.comandos["salir"] = lambda: None
        #self.historial = None
        #self.errores = None

    def consola(self):
        "Procedimiento que implementa la interfaz en línea de comandos."

        self.ayuda()
        
        linea_comando = list()
        leer_comando(linea_comando)
        comando = linea_comando[0]
        while True:
            if comando == "salir":
                if len(linea_comando) != 1:                    
                    mensaje_e = "Error: Sintaxis inválida: salir no toma argumentos."
                    print(mensaje_e)
                    registrar_error("Sintaxis", "Consola", mensaje_e)
                elif self.salir():
                    break
            else:
                try:
                    resultado = self.comandos[comando](linea_comando)
                    print(resultado.resultado)
##                    if resultado.tipo_error is None:
##                        if comando not in ["leerconfig", "errores", "historial"]:
##                            registrar_comando(linea_comando, resultado.resultado)
##                        else:
##                            registrar_comando(linea_comando, "Resultado omitido...")
##                    else:
##                        registrar_error(resultado.tipo_error,
##                                        comando,
##                                        resultado.resultado)
                except KeyError as e:
                    mensaje_e = "Error: Comando desconocido: " + comando
                    print(mensaje_e)
                    registrar_error("No implementado", "Consola", mensaje_e)
                except KeyboardInterrupt:
                    break
            linea_comando = []
            leer_comando(linea_comando)
            comando = linea_comando[0]
        print("Saliendo de la calculadora...")

    def leer_comando(linea_comando):
        "Lee una línea de comando de la entrada. linea_comando debe ser '[]'"
        continuar = True
        while continuar:
            try:
                linea_comando.extend( input(">> ").split() )
            # Esta excepcion que sigue no debe ser capturada, está mal.
            #except EOFError as e:
            #    pass
            except UnicodeError as e:
                mensaje_e = "Error: Texto de entrada por consola inválido."
                print(mensaje_e)
                registrar_error("Codificación de texto", "Consola", mensaje_e)
            else:
                if len(linea_comando) != 0:
                    continuar = False

    def ayuda(self, linea_comando=None):
        # POR HACER!!!
        # Implementar ayuda con argumentos para ver la descripción de un comando
        ayuda = ["Comandos disponibles:"]
        for cmd in self.comandos.values():
            ayuda.append("""  {}
                                {}""".format(cmd.sintaxis, cmd.ayuda) )
        #ayuda.append("  regresar" + alineacion[8:] + "Salir de la calculadora\n")
        ayuda = "\n".join(ayuda)
        return Resultado(ayuda, self)

    def salir(self):
        confirmacion = input("Seguro que desea salir (S/N): ")
        if confirmacion in ("S", "s"):
            return True
        print("Cierre cancelado")
        return False

    def leer_argumentos(linea_comando, mensajes):
        """
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

##    def registrar_comando(linea_comando, resultado):
##        "Registra los comandos ejecutados y sus resultados internamente."
##
##        self.historial.append( [" ".join(linea_comando), resultado] )

##    def registrar_error(tipo, origen, mensaje):
##        "Registra errores en un archivo de registro de errores e internamente.\
##     Acepta tres textos."
##
##        self.errores.append({"tipo": tipo, "origen": origen, "mensaje": mensaje})
##        try:
##            with open(ruta_errores, "a") as registro:
##                contenido = "".join([ "Tipo: ", tipo, "\n",
##                                      "Origen: ", origen, "\n",
##                                      mensaje, "\n\n" ])
##                registro.write(contenido)
##        except OSError as e:
##            mensaje_e = "Error: No se pudo abrir el registro de errores."
##            print(mensaje_e +
##                  " El error se mantendrá almacenado de manera no permanente.")
##            self.errores.append({"tipo": "Archivo",
##                            "origen": "Registro de errores",
##                            "mensaje": mensaje_e})

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
