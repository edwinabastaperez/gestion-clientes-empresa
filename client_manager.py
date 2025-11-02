import os
from datetime import datetime

# --- Configuración y Tabla Hash ---
CLIENT_DIR = 'clientes' # Directorio de almacenamiento
client_index = {}       # Tabla Hash (Diccionario: nombre_cliente -> ruta_archivo)

def load_client_index():
    """Inicializa/Recarga el índice (Tabla Hash) buscando archivos existentes."""
    if not os.path.exists(CLIENT_DIR):
        os.makedirs(CLIENT_DIR)
        print(f"Directorio '{CLIENT_DIR}' creado.")
        return

    client_index.clear()
    for filename in os.listdir(CLIENT_DIR):
        if filename.endswith(".txt"):
            client_name = filename.replace(".txt", "")
            file_path = os.path.join(CLIENT_DIR, filename)
            # Almacenar en la tabla hash: clave en minúsculas para búsqueda rápida
            client_index[client_name.lower()] = file_path
    
    print(f"Índice de clientes cargado. Clientes: {len(client_index)}")

# --- Funciones de Gestión de Archivos ---

def create_client_file(client_name, service_description):
    """Genera un nuevo archivo para un comprador (Nuevo Cliente)."""
    normalized_name = client_name.lower()
    if normalized_name in client_index:
        print(f"\n❌ Error: El cliente '{client_name}' ya existe.")
        return False

    filename = f"{client_name.title()}.txt"
    file_path = os.path.join(CLIENT_DIR, filename)

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"--- Ficha del Cliente: {client_name.title()} ---\n")
            f.write(f"Fecha de Creación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("\n--- Servicio Inicial ---\n")
            f.write(f"Descripción: {service_description}\n")
        
        # Actualizar la Tabla Hash
        client_index[normalized_name] = file_path
        print(f"\n✅ Archivo de cliente '{client_name.title()}' creado con éxito.")
        return True
    except Exception as e:
        print(f"\n❌ Error al crear el archivo: {e}")
        return False

def update_client_request(client_name, new_service_description):
    """Busca el archivo (Tabla Hash) y agrega una nueva solicitud (Cliente Recurrente)."""
    normalized_name = client_name.lower()
    file_path = client_index.get(normalized_name) # Consulta rápida por hash

    if not file_path:
        print(f"\n❌ Error: El cliente '{client_name}' no se encuentra en el índice.")
        return False

    try:
        with open(file_path, 'a', encoding='utf-8') as f: # 'a' para añadir al final
            f.write("\n" + "="*30 + "\n")
            f.write(f"--- Solicitud Recurrente ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) ---\n")
            f.write(f"Descripción: {new_service_description}\n")
            f.write("="*30 + "\n")

        print(f"\n✅ Nueva solicitud añadida al archivo de '{client_name.title()}'.")
        return True
    except Exception as e:
        print(f"\n❌ Error al actualizar el archivo: {e}")
        return False

def read_client_file(client_name):
    """Consulta la información del cliente (acceso por nombre/hash)."""
    normalized_name = client_name.lower()
    file_path = client_index.get(normalized_name)

    if not file_path:
        print(f"\n❌ Error: El cliente '{client_name}' no se encuentra en el índice.")
        return

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            print("\n" + "#"*40)
            print(f"### Contenido del Archivo de Cliente: {client_name.title()} ###")
            print("#"*40)
            print(content)
            print("#"*40 + "\n")
    except Exception as e:
        print(f"\n❌ Error al leer el archivo: {e}")

def delete_client_file(client_name):
    """Elimina el archivo y la entrada de la Tabla Hash."""
    normalized_name = client_name.lower()
    file_path = client_index.get(normalized_name)

    if not file_path:
        print(f"\n❌ Error: El cliente '{client_name}' no se encuentra en el índice.")
        return False

    try:
        os.remove(file_path)
        del client_index[normalized_name] # Eliminar de la Tabla Hash
        print(f"\n✅ Archivo y entrada de '{client_name.title()}' eliminados con éxito.")
        return True
    except Exception as e:
        print(f"\n❌ Error al eliminar el archivo: {e}")
        return False

def list_all_clients():
    """Visualiza una lista de todos los clientes (claves de la Tabla Hash)."""
    if not client_index:
        print("\nℹ️ No hay clientes registrados en el sistema.")
        return
    
    print("\n--- Lista de Clientes Registrados (Índice de Clientes) ---")
    for name in sorted(client_index.keys()):
        print(f"- {name.title()}")
    print("----------------------------------------------------------\n")

# --- Menú Principal ---
def get_client_name(prompt):
    """Función auxiliar para normalizar la entrada."""
    return input(prompt).strip().title()

def main_menu():
    load_client_index()

    while True:
        print("\n=======================================================")
        print("SISTEMA DE GESTIÓN DE CLIENTES - MENU FINAL AUTOMATIZADO")
        print("=======================================================")
        print("1. Registrar Nuevo Cliente")
        print("2. Registrar Nueva Solicitud (Cliente Recurrente)")
        print("3. Consultar Información de Cliente")
        print("4. Mostrar Lista de Todos los Clientes")
        print("5. Eliminar Cliente")
        print("6. Salir")
        print("=======================================================")
        
        choice = input("Seleccione una opción: ")

        if choice == '1':
            name = get_client_name("Nombre del NUEVO cliente: ")
            desc = input("Descripción del servicio inicial: ")
            create_client_file(name, desc)
        
        elif choice == '2':
            name = get_client_name("Nombre del cliente RECURRENTE: ")
            desc = input("Descripción de la nueva solicitud: ")
            update_client_request(name, desc)

        elif choice == '3':
            print("\n--- CONSULTA DE CLIENTE ---")
            print("a) Consultar por Nombre")
            print("b) Ver Lista y Consultar")
            sub_choice = input("Seleccione (a/b): ").lower()
            if sub_choice == 'b':
                list_all_clients()
            
            name = get_client_name("Nombre del cliente a consultar: ")
            read_client_file(name)

        elif choice == '4':
            list_all_clients()
        
        elif choice == '5':
            name = get_client_name("Nombre del cliente a ELIMINAR: ")
            if input(f"¿Seguro que desea ELIMINAR a '{name}'? (s/n): ").lower() == 's':
                delete_client_file(name)
        
        elif choice == '6':
            print("\n👋 ¡Gracias por usar el sistema! Saliendo...")
            break
        
        else:
            print("\n❌ Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main_menu()
