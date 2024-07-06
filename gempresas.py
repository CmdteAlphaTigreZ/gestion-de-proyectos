import csv


class Empresa:
    def __init__(
        self,
        id,
        nombre,
        descripcion,
        fecha_creacion,
        direccion,
        telefono,
        correo,
        gerente,
        equipo_contacto,
    ):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_creacion = fecha_creacion
        self.direccion = direccion
        self.telefono = telefono
        self.correo = correo
        self.gerente = gerente
        self.equipo_contacto = equipo_contacto
        self.proyectos = []


class GestionEmpresas:
    def __init__(self):
        self.empresas = []

    def agregar_empresa(self, empresa):
        self.empresas.append(empresa)

    def modificar_empresa_por_id(self, id, nuevos_atributos):
        empresa = self.buscar_empresa_por_id(id)
        if empresa:
            for atributo, valor in nuevos_atributos.items():
                setattr(empresa, atributo, valor)
            print(f"Empresa con ID {id} modificada exitosamente.")
        else:
            print(f"No se encontró ninguna empresa con el ID {id}.")

    def buscar_empresa_por_id(self, id):
        for empresa in self.empresas:
            if empresa.id == id:
                return empresa
        return None

    def eliminar_empresa_por_id(self, id):
        empresa = self.buscar_empresa_por_id(id)
        if empresa:
            self.empresas.remove(empresa)
            print(f"Empresa con ID {id} eliminada correctamente.")
        else:
            print(f"No se encontró ninguna empresa con el ID {id}.")

    def listar_empresas(self):
        for empresa in self.empresas:
            print(f"ID: {empresa.id}, Nombre: {empresa.nombre}")

    def guardar_empresas_en_csv(self, archivo_csv):
        with open(archivo_csv, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(
                [
                    "ID",
                    "Nombre",
                    "Descripción",
                    "Fecha Creación",
                    "Dirección",
                    "Teléfono",
                    "Correo",
                    "Gerente",
                    "Equipo de Contacto",
                ]
            )
            for empresa in self.empresas:
                writer.writerow(
                    [
                        empresa.id,
                        empresa.nombre,
                        empresa.descripcion,
                        empresa.fecha_creacion,
                        empresa.direccion,
                        empresa.telefono,
                        empresa.correo,
                        empresa.gerente,
                        ", ".join(empresa.equipo_contacto),
                    ]
                )
