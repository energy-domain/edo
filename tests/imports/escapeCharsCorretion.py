import os
import re

def escape_ttl_literal(text):
    # Padrão para encontrar strings entre aspas
    pattern = re.compile(r'(")((?:\\.|[^\\"])*?)(")')
    
    def escape_special_chars(match):
        opening_quote = match.group(1)
        content = match.group(2)
        closing_quote = match.group(3)
        
        # Escapa: \, ", quebras de linha e tabs não escapados
        content_escaped = re.sub(
            r'(?<!\\)([\\"\n\t\r])',
            lambda m: f'\\{m.group(1)}',
            content
        )
        
        return f'{opening_quote}{content_escaped}{closing_quote}'
    
    return pattern.sub(escape_special_chars, text)

def process_ttl_files():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ttl_files = [f for f in os.listdir(script_dir) if f.endswith('.ttl')]
    
    if not ttl_files:
        print("Nenhum arquivo TTL encontrado na pasta do script.")
        return
    
    for ttl_file in ttl_files:
        file_path = os.path.join(script_dir, ttl_file)
        print(f"Processando: {ttl_file}")
        
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        processed_content = escape_ttl_literal(content)
        
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(processed_content)
        
        print(f"Concluído: {ttl_file}")

if __name__ == "__main__":
    process_ttl_files()