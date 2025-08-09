import os
import re

def process_ttl_files():
    # Obter o diretório atual onde o script está localizado
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Listar todos os arquivos .ttl no diretório
    ttl_files = [f for f in os.listdir(script_dir) if f.endswith('.ttl')]
    
    if not ttl_files:
        print("Nenhum arquivo TTL encontrado na pasta do script.")
        return
    
    for ttl_file in ttl_files:
        file_path = os.path.join(script_dir, ttl_file)
        print(f"Processando arquivo: {ttl_file}")
        
        # Ler o conteúdo do arquivo
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        # Processar cada linha
        processed_lines = []
        for line in lines:
            # Contar o número de aspas na linha
            quote_count = line.count('"')
            
            if quote_count > 2:
                # Encontrar todas as aspas
                chars = list(line)
                in_quotes = False
                quote_positions = []
                
                for i, char in enumerate(chars):
                    if char == '"':
                        quote_positions.append(i)
                
                # Manter a primeira e última aspas, escapar as do meio
                for pos in quote_positions[1:-1]:
                    # Verificar se a aspa já não está escapada
                    if pos > 0 and chars[pos-1] != '\\':
                        chars.insert(pos, '\\')
                        # Atualizar as posições depois da inserção
                        quote_positions = [p+1 if p >= pos else p for p in quote_positions]
                
                line = ''.join(chars)
            
            processed_lines.append(line)
        
        # Escrever o conteúdo processado de volta no arquivo
        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(processed_lines)
        
        print(f"Arquivo {ttl_file} processado com sucesso.")

if __name__ == "__main__":
    process_ttl_files()