import unicodedata
import string

def es_palindromo(texto):
    """Verifica si una palabra o frase es un palíndromo."""
    texto = unicodedata.normalize('NFD', texto)
    texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')  # Elimina tildes
    texto = texto.lower()
    texto_limpio = ''.join(c for c in texto if c.isalnum())
    return texto_limpio == texto_limpio[::-1]

# Ejemplo de uso
if __name__ == "__main__":
    frase = input("Ingrese una palabra o frase: ")
    if es_palindromo(frase):
        print("Es un palíndromo.")
    else:
        print("No es un palíndromo.")
