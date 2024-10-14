from template_engine import parse_template, compile_template

with open('dokumen/template.html', 'r') as fl:
    template_text = fl.read()

data_parameter = {
    'nama': 'Eko Heri',
    'buah': ['Apel', 'Pisang', 'Nanas']
}

# Kompilasi template
tokens = parse_template(template_text)
output = compile_template(tokens, data_parameter)
print(output)
