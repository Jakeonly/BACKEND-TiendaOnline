"""
Si tu contraseña de Neon tiene caracteres especiales (# @ & ? etc.),
codifícala para usarla en DATABASE_URL.

Uso: python scripts/codificar_password.py
Luego pega la contraseña cuando te la pida y copia el resultado
en la URL de .env (reemplaza la parte de la contraseña).
"""
import urllib.parse

if __name__ == "__main__":
    print("Pega la contraseña de Neon (solo la contraseña) y pulsa Enter:")
    password = input().strip()
    if not password:
        print("No se ingresó nada.")
    else:
        encoded = urllib.parse.quote(password, safe="")
        print("\nContraseña codificada para la URL:")
        print(encoded)
        print("\nEn tu DATABASE_URL reemplaza la contraseña por lo de arriba.")
        print("Ejemplo: postgresql://usuario:ESTE_VALOR@host/db?sslmode=require")


#Por ahora no hizo nada