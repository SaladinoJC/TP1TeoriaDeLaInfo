import sys
import os
from collections import defaultdict, Counter
from itertools import product
import math
import numpy as np

TOL=8e-2



def calculate_entropy2(probabilities):
    """Calcula la entropía en base a probabilidades."""
    entropy = 0
    for prob in probabilities.values():
        if prob > 0:
            entropy -= prob * math.log2(prob)
    return entropy

def calculate_entropy(probabilities):
    """Calcula la entropía en base a probabilidades con formato."""
    entropy = 0
    for prob in probabilities:
        if prob > 0:
            entropy -= prob * math.log2(prob)
    return entropy

def main():
    os.system('cls')
#Validaciones---------------------------------------------------------------------
    if len(sys.argv) < 2:
        print("Error: ejecutar de la siguiente forma: python tp1.py filename.txt [N]")
        sys.exit(1)
    filename = sys.argv[1]
    n = None
    if len(sys.argv) == 3:
        try: 
            n = int(sys.argv[2])
            if n < 0:
                raise ValueError("N debe ser un número natural (mayor o igual a 0).")
        except ValueError as e:
            print(f"Error: {e}")
            sys.exit(1)
    if not os.path.isfile(filename):
        print(f"Error: El archivo '{filename}' no existe.")
        sys.exit(1)
#---------------------------------------------------------------------------------

    # Lee el contenido del archivo y calcula la frecuencia de caracteres y pares de caracteres
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()

            # Cuenta frecuencias de caracteres individuales
            char_frequency = Counter(content)
            total_chars = sum(char_frequency.values())

            # Calcula probabilidades marginales P(A)
            marginal_probabilities = {char: freq / total_chars for char, freq in char_frequency.items()}

            # Cuenta frecuencias de pares de caracteres
            pair_frequency = defaultdict(Counter)
            for i in range(len(content) - 1):
                pair_frequency[content[i]][content[i + 1]] += 1

            # Calcula probabilidades condicionales P(A|B)
            conditional_probabilities = defaultdict(dict)
            for char, following_chars in pair_frequency.items():
                total_occurrences = sum(following_chars.values())
                for following_char, count in following_chars.items():
                    conditional_probabilities[char][following_char] = count / total_occurrences

            # Determina si la fuente es de memoria nula o no nula
            is_memoryless = True
            for char, following_chars in conditional_probabilities.items():
                for following_char, cond_prob in following_chars.items():
                    marginal_prob = marginal_probabilities.get(following_char, 0)
                    if abs(cond_prob - marginal_prob) > TOL: #TOLERANCIA
                        is_memoryless = False
                        break
                if not is_memoryless:  
                    break

            # Muestra frecuencias, probabilidades y conclusión sobre la memoria
            print(f"\nFrecuencia de caracteres en '{filename}':")
            for char in sorted(char_frequency.keys()):
                print(f"'{char}': {char_frequency[char]}")

            print("\nProbabilidades condicionales:")
            for char in sorted(conditional_probabilities.keys()):
                for following_char in sorted(conditional_probabilities[char].keys()):
                    prob = conditional_probabilities[char][following_char]
                    print(f"P('{following_char}'|'{char}') = {prob:.4f}")

            print("\nProbabilidades marginales:")
            for char in sorted(marginal_probabilities.keys()):
                print(f"P('{char}') = {marginal_probabilities[char]:.4f}")

            print("\nConclusión:")
            if  is_memoryless:
                print("La fuente es de memoria nula.")
                
                # Calcula probabilidades de extensión de orden N
                if n is not None:
                    print(f"\nProbabilidades de la extensión de orden {n}:")
                    sequences = product(sorted(marginal_probabilities.keys()), repeat=n)
                    extension_probabilities = []
                    
                    for seq in sequences:
                        prob = 1
                        seq_str = ''.join(seq)
                        for char in seq:
                            prob *= marginal_probabilities[char]
                        extension_probabilities.append(prob)
                        print(f"P('{seq_str}') = {prob:.8f}")
                    
                    # Calcula entropía de la extensión de orden N
                    entropy_n = calculate_entropy(extension_probabilities)
                    print(f"\nEntropía de la extensión de orden {n}: H_{n} = {entropy_n:.4f} bits")
                    entropy_src = calculate_entropy2(marginal_probabilities)
                    print(f"La Entropia de la fuente es: {entropy_src:.4f} bits")
                    
            else:
                print("La fuente es de memoria no nula. \n")
                
                # Calcula el vector estacionario
                chars = sorted(marginal_probabilities.keys())
                transition_matrix = np.zeros((len(chars), len(chars)))

                for i, char in enumerate(chars):
                    for j, following_char in enumerate(chars):
                        transition_matrix[i, j] = conditional_probabilities[char].get(following_char, 0)

                # Resuelve el sistema de ecuaciones lineales para encontrar el vector estacionario
                eigenvalues, eigenvectors = np.linalg.eig(transition_matrix.T)
                stationary_vector = eigenvectors[:, np.isclose(eigenvalues, 1)]

                # Normaliza el vector estacionario para que sus componentes sumen 1
                stationary_vector = stationary_vector / np.sum(stationary_vector)

                # Imprime el vector estacionario y la entropia de la fuente

                print("Vector estacionario:")
                for i, char in enumerate(chars):
                    print(f"π('{char}') = {stationary_vector[i, 0].real:.4f}")
                non_zero_mask = transition_matrix > 0
                log_values = np.zeros_like(transition_matrix)
                log_values[non_zero_mask] = transition_matrix[non_zero_mask] * np.log2(1/transition_matrix[non_zero_mask])
                column_sums = np.sum(log_values, axis=1)
                weighted_sums = np.dot(column_sums, stationary_vector)
                resultado = (weighted_sums[0].real)
                print(f"\nLa Entropia de la fuente es {resultado:.4f} bits")

    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()