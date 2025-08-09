import openpyxl

# Carrega a planilha e a aba especificada
workbook = openpyxl.load_workbook('dataImport.xlsx')
sheet = workbook['classMetadata']

# Abre o arquivo de saída
with open('output.ttl', 'w', encoding='utf-8') as file:
    # Pula a primeira linha (header) e começa da segunda
    for n, row in enumerate(sheet.iter_rows(min_row=2), start=2):
        # Verifica se a célula A está vazia (condição de parada)
        if row[0].value is None:
            break
        
        objectName = ':' + str(row[0].value)  # : + célula An
        
        # Loop das colunas A até H (índices 0 a 7)
        for col_idx in range(8):  # A=0, B=1, ..., H=7
            header = sheet.cell(row=1, column=col_idx + 1).value  # Pega o header da coluna (linha 1)
            cell_value = row[col_idx].value
            
            # Se a célula estiver vazia, pula para a próxima coluna
            if cell_value is None or str(cell_value).strip() == "":
                continue
            
            # Formata a string conforme o idioma do header
            if header.endswith("@en"):
                h = header.replace(" @en", "")
                line = f"{objectName} {h} \"{cell_value}\"@en .\n"
            elif header.endswith("@pt-BR"):
                h = header.replace(" @pt-BR", "")
                line = f"{objectName} {h} \"{cell_value}\"@pt-BR .\n"
            else:
                line = f"{objectName} {header} \"{cell_value}\" .\n"
            
            file.write(line)
        
        # Verifica a célula I (índice 8) para skos:altLabel
        if row[8].value is not None:  # Se a célula In não estiver vazia
            parts = str(row[8].value).split('; ')  # Split pelo separador
            for part in parts:
                if part.strip():  # Só escreve se a parte não for vazia
                    alt_label_line = f"{objectName} skos:altLabel \"{part}\"@en .\n"
                    file.write(alt_label_line)

print("Processamento concluído. Resultados salvos em output.ttl.")