import os
import re

def process_ttl_files():
    # Obter o diretório atual onde o script está localizado
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Padrões de busca e substituição
    single_multi_pattern = re.compile(r'rdfs:subClassOf\s*:(single|multi)Value')
    single_multi_replacement = r':hasValueCardinality :\1Value'
    
    other_values_pattern = re.compile(r'rdfs:subClassOf\s*:(\w+)Value')
    other_values_replacement = r':hasTypedValue :\1Value'
    
    # Processar cada arquivo .ttl no diretório
    for filename in os.listdir(current_dir):
        if filename.endswith('.ttl'):
            filepath = os.path.join(current_dir, filename)
            
            # Ler o conteúdo do arquivo
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Fazer as substituições
            # Primeiro para single e multi
            new_content = single_multi_pattern.sub(single_multi_replacement, content)
            # Depois para os demais valores
            new_content = other_values_pattern.sub(other_values_replacement, new_content)
            
            # Escrever o conteúdo modificado de volta no arquivo
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(new_content)
            
            print(f"Arquivo processado: {filename}")

if __name__ == "__main__":
    process_ttl_files()
    print("Processamento concluído.")