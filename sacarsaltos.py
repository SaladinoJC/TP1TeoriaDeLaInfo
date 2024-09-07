import string

def filter_and_process_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        # Lee el contenido del archivo
        content = file.read()
        
        # Elimina los saltos de línea y convierte a minúsculas
        content = content.replace('\n', ' ').replace('\r', '').lower()
        
        # Elimina los espacios múltiples
        content = ' '.join(content.split())
        
        # Filtra solo las letras del alfabeto inglés (sin números ni signos de puntuación)
        filtered_content = ''.join(char for char in content if char.isalpha() or char.isspace())
    
    # Escribe el contenido procesado en el archivo de salida
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(filtered_content)

    print(f"Se ha procesado el archivo y el nuevo archivo se guardó como {output_file}.")

if __name__ == "__main__":
    input_file = 'swedish.txt'  # Reemplaza con el nombre de tu archivo de entrada
    output_file = 'filtered_swedish.txt'  # Reemplaza con el nombre que quieras para tu archivo de salida
    filter_and_process_file(input_file, output_file)