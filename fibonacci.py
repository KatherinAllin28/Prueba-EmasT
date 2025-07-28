def fibonacci(n):
    """Genera los primeros n números de la secuencia de Fibonacci."""
    if n <= 0:
        return []
    elif n == 1:
        return [0]

    fib_seq = [0, 1]
    while len(fib_seq) < n:
        fib_seq.append(fib_seq[-1] + fib_seq[-2])
    return fib_seq

# Ejemplo de uso
if __name__ == "__main__":
    n = int(input("Ingrese la cantidad de números de Fibonacci a generar: "))
    print(f"Secuencia Fibonacci ({n} términos): {fibonacci(n)}")
