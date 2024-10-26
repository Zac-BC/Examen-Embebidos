cadena = "Hola Mundo"

for pos, char in enumerate(cadena):
    if char == 'H':
        print(f"Encontré una H en la posición {pos}!")
    else:
        print(f"No es una H en la posición {pos}")
