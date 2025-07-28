import unicodedata

def limpiar_texto(texto):
    texto = unicodedata.normalize('NFD', texto)
    texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
    return ''.join(c.lower() for c in texto if c.isalpha())

def son_anagramas(palabra1, palabra2):
    return sorted(limpiar_texto(palabra1)) == sorted(limpiar_texto(palabra2))

# Ejemplo de uso
if __name__ == "__main__":
    p1 = input("Ingrese la primera palabra o frase: ")
    p2 = input("Ingrese la segunda palabra o frase: ")

    if son_anagramas(p1, p2):
        print("Son anagramas.")
    else:
        print("No son anagramas.")
