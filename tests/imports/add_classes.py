import os
import re

def process_ttl_files():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    for filename in os.listdir(script_dir):
        if filename.endswith('.ttl'):
            filepath = os.path.join(script_dir, filename)
            process_ttl_file(filepath)

def process_ttl_file(filepath):
    lines_to_add = []  # Agora usamos uma lista para manter a ordem
    processed_strings = set()
    
    with open(filepath, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line.startswith(':'):
                match = re.match(r'^(:[^\s]+)', line)
                if match:
                    stringA = match.group(1)
                    if stringA not in processed_strings:
                        processed_strings.add(stringA)
                        # Adiciona na ordem correta: type primeiro, subClassOf depois
                        lines_to_add.append(f"{stringA} rdf:type owl:Class .")
                        lines_to_add.append(f"{stringA} rdfs:subClassOf :DomainAttribute .")
    
    if lines_to_add:
        with open(filepath, 'a', encoding='utf-8') as file:
            file.write('\n' + '\n'.join(lines_to_add) + '\n')
        print(f"Arquivo {os.path.basename(filepath)} atualizado com {len(lines_to_add)} novas linhas.")
    else:
        print(f"Nenhuma atualização necessária para {os.path.basename(filepath)}.")

if __name__ == "__main__":
    process_ttl_files()