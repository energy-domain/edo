import re
import os

def substituir_prefixos_ttl(arquivo_entrada, arquivo_saida):
    """
    Lê um arquivo TTL, substitui todas as ocorrências do prefixo padrão ':'
    pelo prefixo 'edo:' e atualiza a declaração do prefixo.
    """
    try:
        # Verifica se o arquivo de entrada existe
        if not os.path.exists(arquivo_entrada):
            print(f"Erro: O arquivo '{arquivo_entrada}' não foi encontrado.")
            return False
        
        # Lê o conteúdo do arquivo
        with open(arquivo_entrada, 'r', encoding='utf-8') as f:
            linhas = f.readlines()
        
        novo_conteudo = []
        for linha in linhas:
            # Substitui a declaração do prefixo
            if re.search(r'@prefix\s*:\s*<https://w3id\.org/energy-domain/edo#>\.', linha):
                linha = '@prefix edo: <https://w3id.org/energy-domain/edo#>.\n'
            
            # Substitui referências do prefixo padrão que não são parte de outros prefixos
            # Usa lookbehind negativo para evitar substituir partes de outros prefixos
            linha = re.sub(r'(?<![A-Za-z0-9_]):([A-Za-z_][A-Za-z0-9_]*)', r'edo:\1', linha)
            
            novo_conteudo.append(linha)
        
        # Escreve o novo conteúdo no arquivo de saída
        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            f.writelines(novo_conteudo)
        
        print(f"Sucesso: Arquivo '{arquivo_saida}' criado com as substituições.")
        return True
        
    except Exception as e:
        print(f"Erro durante o processamento: {str(e)}")
        return False

if __name__ == "__main__":
    # Nomes dos arquivos
    arquivo_entrada = "prefix_update.ttl"
    arquivo_saida = "prefix_updated.ttl"
    
    # Executa a substituição
    print(f"Processando arquivo: {arquivo_entrada}")
    sucesso = substituir_prefixos_ttl(arquivo_entrada, arquivo_saida)
    
    if sucesso:
        print("Processamento concluído!")
    else:
        print("Falha no processamento.")