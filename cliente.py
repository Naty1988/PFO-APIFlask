import requests

API_URL = "http://localhost:5000"

def menu():
    print("\n--- Sistema de Gestión de Tareas ---")
    print("1. Registrarse")
    print("2. Iniciar sesión")
    print("3. Salir")

def registrarse():
    usuario = input("Ingrese su nombre de usuario: ")
    contraseña = input("Ingrese su contraseña: ")
    datos = {"usuario": usuario, "contraseña": contraseña}
    respuesta = requests.post(f"{API_URL}/registro", json=datos)
    print(respuesta.json())

def login():
    usuario = input("Usuario: ")
    contraseña = input("Contraseña: ")
    datos = {"usuario": usuario, "contraseña": contraseña}
    respuesta = requests.post(f"{API_URL}/login", json=datos)
    print(respuesta.json())
    
    if respuesta.status_code == 200:
        # Si login correcto, accede a /tareas
        tareas = requests.get(f"{API_URL}/tareas")
        print("\n=== Página de tareas ===")
        print(tareas.text)

def main():
    while True:
        menu()
        opcion = input("Elija una opción: ")
        if opcion == "1":
            registrarse()
        elif opcion == "2":
            login()
        elif opcion == "3":
            print("Saliendo...")
            break
        else:
            print("Opción inválida")

if __name__ == '__main__':
    main()
