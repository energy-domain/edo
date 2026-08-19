from runpy import run_path

# Preserve the connection-interface refinement and then extend the generated
# object-relations ontology with the material-specification model.
run_path("tools/_add_connection_interface_specification_impl.py", run_name="__main__")
run_path("tools/add_material_specification_relations.py", run_name="__main__")
