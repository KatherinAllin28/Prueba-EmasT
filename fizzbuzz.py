def fizzbuzz(n):
    for i in range(1, n + 1):
        resultado = ''
        if i % 3 == 0:
            resultado += 'Fizz'
        if i % 5 == 0:
            resultado += 'Buzz'
        print(resultado or i)

# Ejemplo de uso
if __name__ == "__main__":
    n = int(input("Ingrese un número entero positivo: "))
    fizzbuzz(n)
