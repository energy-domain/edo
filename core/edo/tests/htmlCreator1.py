import os
from rdflib import Graph, URIRef, RDF, RDFS, OWL

def generate_html(ontology_file):
    # Carrega a ontologia
    g = Graph()
    g.parse(ontology_file, format="turtle")
    
    # Define namespaces específicos para sua ontologia
    BASE = URIRef("https://w3id.org/energy-domain/edo#")
    HAS_ATTRIBUTE = URIRef("https://w3id.org/energy-domain/edo#hasAttribute")
    
    # Encontra todas as classes que são subclasses de :DomainObject
    domain_object = BASE + "DomainObject"
    classes_hierarchy = {}
    
    # Função para construir a hierarquia de classes
    def build_hierarchy(class_uri, hierarchy):
        subclasses = []
        for s in g.subjects(predicate=RDFS.subClassOf, object=class_uri):
            if isinstance(s, URIRef):
                subclasses.append(s)
        
        for subclass in subclasses:
            hierarchy[subclass] = {}
            build_hierarchy(subclass, hierarchy[subclass])
    
    build_hierarchy(domain_object, classes_hierarchy)
    
    # Função para gerar a árvore HTML
    def generate_tree_html(hierarchy, level=0):
        html = ""
        for class_uri, sub_hierarchy in hierarchy.items():
            class_name = class_uri.split("#")[-1]
            indent = "  " * level
            html += f'{indent}<li>\n'
            html += f'{indent}  <span class="caret" onclick="selectClass(\'{class_name}\', \'{class_uri}\')">{class_name}</span>\n'
            
            if sub_hierarchy:
                html += f'{indent}  <ul class="nested">\n'
                html += generate_tree_html(sub_hierarchy, level + 2)
                html += f'{indent}  </ul>\n'
            
            html += f'{indent}</li>\n'
        return html
    
    # Função para coletar todas as superclasses de uma classe
    def get_superclasses(class_uri):
        superclasses = []
        for superclass in g.objects(subject=class_uri, predicate=RDFS.subClassOf):
            if isinstance(superclass, URIRef):
                superclasses.append(superclass)
                superclasses.extend(get_superclasses(superclass))
        return superclasses
    
    # Função para coletar todos os atributos de uma classe e suas superclasses
    def get_attributes(class_uri):
        attributes = set()
        
        # Pega os atributos da classe atual
        for attr in g.objects(subject=class_uri, predicate=HAS_ATTRIBUTE):
            if isinstance(attr, URIRef):
                attributes.add(attr.split("#")[-1])
            else:
                attributes.add(str(attr))
        
        # Pega os atributos de todas as superclasses
        for superclass in get_superclasses(class_uri):
            for attr in g.objects(subject=superclass, predicate=HAS_ATTRIBUTE):
                if isinstance(attr, URIRef):
                    attributes.add(attr.split("#")[-1])
                else:
                    attributes.add(str(attr))
        
        return sorted(attributes)
    
    # Gera dados JavaScript com os atributos de todas as classes
    def generate_attributes_data():
        data = {}
        # Processa todas as classes na hierarquia
        def process_hierarchy(hierarchy):
            for class_uri, sub_hierarchy in hierarchy.items():
                class_name = class_uri.split("#")[-1]
                data[class_uri] = {
                    'name': class_name,
                    'attributes': get_attributes(class_uri)
                }
                process_hierarchy(sub_hierarchy)
        
        process_hierarchy(classes_hierarchy)
        return data
    
    attributes_data = generate_attributes_data()
    
    # Gera a parte JavaScript dos dados das classes
    def generate_js_data():
        js_lines = []
        for class_uri, data in attributes_data.items():
            js_line = f'"{class_uri}": {{\n'
            js_line += f'    "name": "{data["name"]}",\n'
            js_line += f'    "attributes": {data["attributes"]}\n'
            js_line += '}'
            js_lines.append(js_line)
        return ',\n'.join(js_lines)
    
    js_data = generate_js_data()
    
    # Gera o HTML completo
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Energy Domain Ontology Browser</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
        }}
        
        /* Tree styling */
        ul, #tree {{
            list-style-type: none;
            padding-left: 20px;
        }}
        
        .caret {{
            cursor: pointer;
            user-select: none;
        }}
        
        .caret::before {{
            content: "\\25B6";
            color: black;
            display: inline-block;
            margin-right: 6px;
        }}
        
        .caret-down::before {{
            transform: rotate(90deg);
        }}
        
        .nested {{
            display: none;
        }}
        
        .active {{
            display: block;
        }}
        
        /* Modal styling */
        .modal {{
            display: none;
            position: fixed;
            z-index: 1;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            overflow: auto;
            background-color: rgba(0,0,0,0.4);
        }}
        
        .modal-content {{
            background-color: #fefefe;
            margin: 15% auto;
            padding: 20px;
            border: 1px solid #888;
            width: 80%;
            max-width: 600px;
        }}
        
        .close {{
            color: #aaa;
            float: right;
            font-size: 28px;
            font-weight: bold;
            cursor: pointer;
        }}
        
        .close:hover {{
            color: black;
        }}
        
        .attribute-list {{
            margin-top: 10px;
        }}
        
        .attribute-item {{
            margin-bottom: 5px;
            padding: 5px;
            background-color: #f0f0f0;
            border-radius: 3px;
        }}
    </style>
</head>
<body>
    <h1>Energy Domain Ontology Browser</h1>
    
    <h2>Class Taxonomy</h2>
    <ul id="tree">
        {generate_tree_html(classes_hierarchy)}
    </ul>
    
    <!-- The Modal -->
    <div id="classModal" class="modal">
        <div class="modal-content">
            <span class="close">&times;</span>
            <h2 id="modalTitle">Class Attributes</h2>
            <div id="attributesContainer" class="attribute-list"></div>
        </div>
    </div>
    
    <script>
        // Dados das classes e atributos
        const classesData = {{
            {js_data}
        }};
        
        // Tree collapsible functionality
        var toggler = document.getElementsByClassName("caret");
        for (var i = 0; i < toggler.length; i++) {{
            toggler[i].addEventListener("click", function() {{
                this.parentElement.querySelector(".nested").classList.toggle("active");
                this.classList.toggle("caret-down");
            }});
        }}
        
        // Modal functionality
        var modal = document.getElementById("classModal");
        var span = document.getElementsByClassName("close")[0];
        
        span.onclick = function() {{
            modal.style.display = "none";
        }}
        
        window.onclick = function(event) {{
            if (event.target == modal) {{
                modal.style.display = "none";
            }}
        }}
        
        // Function to handle class selection
        function selectClass(className, classUri) {{
            // Get class data
            const classData = classesData[classUri];
            
            // Update modal title
            document.getElementById("modalTitle").innerText = "Attributes for: " + className;
            
            // Clear previous attributes
            const container = document.getElementById("attributesContainer");
            container.innerHTML = "";
            
            // Add attributes to the modal
            if (classData.attributes.length > 0) {{
                classData.attributes.forEach(attr => {{
                    const div = document.createElement("div");
                    div.className = "attribute-item";
                    div.textContent = attr;
                    container.appendChild(div);
                }});
            }} else {{
                const div = document.createElement("div");
                div.textContent = "No attributes found for this class.";
                container.appendChild(div);
            }}
            
            // Show the modal
            modal.style.display = "block";
        }}
    </script>
</body>
</html>
"""
    
    # Salva o arquivo HTML
    output_file = os.path.splitext(ontology_file)[0] + ".html"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"HTML file generated: {output_file}")

if __name__ == "__main__":
    ontology_file = "energy-domain-ontology.ttl"  # Nome do seu arquivo TTL
    if os.path.exists(ontology_file):
        generate_html(ontology_file)
    else:
        print(f"Error: File '{ontology_file}' not found in the current directory.")