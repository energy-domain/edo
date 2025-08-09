import pandas as pd
import requests
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, RDFS, OWL
import datetime
import os
import sys

# --- Configuração ---
ONTOLOGY_URL = "https://raw.githubusercontent.com/energy-domain/ontologies/main/tests/core/src/energy-domain-ontology.ttl"
LOCAL_ONTOLOGY_FILE = "energy-domain-ontology.ttl"
EXCEL_FILE = "dataImport.xlsx"
EXCEL_SHEET = "triples"

PREFIX_MAP = {
    "owl": OWL,
    "rdf": RDF,
    "rdfs": RDFS,
}

def string_to_term(value_str, default_ns):
    if not isinstance(value_str, str) or not value_str.strip():
        return None
    
    value_str = value_str.strip()

    if value_str.startswith(':'):
        return default_ns[value_str[1:]]
    
    if ":" in value_str:
        prefix, local_name = value_str.split(":", 1)
        if prefix in PREFIX_MAP:
            return PREFIX_MAP[prefix][local_name]
        else:
            print(f"AVISO: Prefixo desconhecido '{prefix}' em '{value_str}'. Ignorando termo.")
            return None
    
    return default_ns[value_str]

def main():
    print("Iniciando o processo de atualização da ontologia...")

    g_orig = Graph()
    try:
        try:
            response = requests.get(ONTOLOGY_URL, timeout=10)
            response.raise_for_status()
            g_orig.parse(data=response.text, format="turtle")
            print("-> Sucesso: Ontologia carregada da internet.")
        except requests.exceptions.RequestException as e:
            print(f"-> AVISO: Falha ao acessar a ontologia na internet. Tentando arquivo local... ({e})")
            if not os.path.exists(LOCAL_ONTOLOGY_FILE):
                raise FileNotFoundError(f"Arquivo local '{LOCAL_ONTOLOGY_FILE}' também não foi encontrado.")
            g_orig.parse(location=LOCAL_ONTOLOGY_FILE, format="turtle")
            print("-> Sucesso: Ontologia carregada do arquivo local.")
    except Exception as e:
        print(f"ERRO FATAL: Não foi possível carregar a ontologia base. Detalhe: {e}")
        sys.exit(1)

    # ****** CORREÇÃO DO ATTRIBUTEERROR AQUI ******
    # A forma correta de encontrar o namespace do prefixo padrão (':')
    # é iterando sobre os namespaces conhecidos pelo grafo.
    base_ns_uri = None
    for prefix, namespace in g_orig.namespace_manager.namespaces():
        # O prefixo padrão (:) é representado por uma string vazia ''
        if prefix == '':
            base_ns_uri = namespace
            break  # Encontramos, podemos parar o loop

    if base_ns_uri:
        EDO = Namespace(base_ns_uri)
        print(f"-> Namespace base da ontologia detectado com sucesso: {base_ns_uri}")
    else:
        print("ERRO FATAL: Não foi possível encontrar o namespace base (prefixo ':') na ontologia carregada.")
        sys.exit(1)

    try:
        print(f"\nLendo a planilha '{EXCEL_FILE}'...")
        df = pd.read_excel(EXCEL_FILE, sheet_name=EXCEL_SHEET, dtype=str).fillna('')
        print("Planilha lida com sucesso.")
    except FileNotFoundError:
        print(f"ERRO: Arquivo da planilha '{EXCEL_FILE}' não encontrado.")
        sys.exit(1)

    g_new = Graph()
    g_new.bind("", EDO)
    g_new.bind("owl", OWL)
    g_new.bind("rdf", RDF)
    g_new.bind("rdfs", RDFS)

    print("\nIniciando varredura das linhas da planilha para encontrar APENAS novas triplas...")
    for index, row in df.iterrows():
        s_str = str(row.get('subject', '')).strip()
        st_str = str(row.get('subjectType', '')).strip()
        v_str = str(row.get('verb', '')).strip()
        o_str = str(row.get('object', '')).strip()

        # Pula linhas que não formam uma tripla principal completa
        if not s_str or not v_str or not o_str:
            continue
            
        subject = string_to_term(s_str, default_ns=EDO)
        verb = string_to_term(v_str, default_ns=EDO)
        object_term = string_to_term(o_str, default_ns=EDO)

        if not all([subject, verb, object_term]):
            continue

        main_triple = (subject, verb, object_term)
        
        if main_triple not in g_orig:
            g_new.add(main_triple)
            print(f"  [NOVA TRIPLA] Adicionada: {s_str} {v_str} {o_str}")

        if st_str:
            subject_type = string_to_term(st_str, default_ns=EDO)
            if subject_type:
                type_triple = (subject, RDF.type, subject_type)
                if type_triple not in g_orig:
                    g_new.add(type_triple)
                    print(f"  [NOVO TIPO] Adicionado: {s_str} a {st_str}")

    # --- Geração do Arquivo Final ---
    if len(g_new) > 0:
        data_atual = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        output_filename = f"new_additions_{data_atual}.ttl"
        
        print(f"\nProcessamento concluído. Gerando arquivo de saída...")
        g_new.serialize(destination=output_filename, format="turtle")
        print(f"Arquivo '{output_filename}' criado com sucesso.")
    else:
        print("\nProcessamento concluído. Nenhuma nova informação foi encontrada para ser adicionada.")

if __name__ == "__main__":
    main()