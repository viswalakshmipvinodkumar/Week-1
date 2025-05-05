def fibonacci(n):
    a, b = 0, 1
    sequence = []
    for _ in range(n):
        sequence.append(a)
        a, b = b, a + b
    return sequence

n_terms = int(input("Enter the number of terms: "))
print("Fibonacci sequence:", fibonacci(n_terms))
