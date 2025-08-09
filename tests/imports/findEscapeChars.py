import os
import re

def find_unescaped_specials_in_quotes(line):
    """Versão que VOCÊ VALIDOU como funcionando corretamente"""
    pattern = re.compile(r'^.*?"(.*)".*?$', re.DOTALL)
    match = pattern.search(line)
    
    if not match:
        return None
    
    content = match.group(1)
    if re.search(r'(?<!\\)([\\"\n\t\r])', content):
        return content
    return None

def escape_content(content):
    """Escapa os caracteres problemáticos no conteúdo"""
    return re.sub(r'(?<!\\)([\\"\n\t\r])', r'\\\1', content)

def process_ttl_files():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ttl_files = [f for f in os.listdir(script_dir) if f.endswith('.ttl')]
    
    if not ttl_files:
        print("Nenhum arquivo TTL encontrado.")
        return
    
    report = []
    
    for ttl_file in ttl_files:
        file_path = os.path.join(script_dir, ttl_file)
        with open(file_path, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                problematic_content = find_unescaped_specials_in_quotes(line)
                
                if problematic_content:
                    # Corrige APENAS o conteúdo entre aspas
                    corrected_content = escape_content(problematic_content)
                    corrected_line = line.replace(problematic_content, corrected_content)
                    
                    report.append(
                        f"\n=== {ttl_file} (Linha {line_num}) ===\n"
                        f"ORIGINAL: {line}\n"
                        f"CORRIGIDO: {corrected_line}\n"
                        f"{'-'*50}"
                    )
    
    with open(os.path.join(script_dir, 'escapeReport.txt'), 'w', encoding='utf-8') as out_file:
        if report:
            out_file.write("RELATÓRIO DE LINHAS COM PROBLEMAS E CORREÇÕES:\n\n")
            out_file.write("\n".join(report))
            print("Relatório gerado com sucesso em escapeReport.txt")
        else:
            out_file.write("✅ Nenhum problema encontrado nos arquivos TTL.")

if __name__ == "__main__":
    process_ttl_files()