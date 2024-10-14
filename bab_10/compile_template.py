import re

def parse_template(text):
    delimiter = re.compile(r'{%(.*?)%}', re.DOTALL)
    tokens = []
    for index, token in enumerate(delimiter.split(text)):
        if index % 2 == 0:
            # Kelompok text bukan program (HTML biasa).
            if token:
                tokens.append((False, token.replace('%}', '%}').replace('{%', '{%')))
        else:
            # Kelompok Text program
            lines = token.replace('{%', '{%').replace('%}', '%}').splitlines()
            # Menentukan indentasi minimum
            indent = None
            for l in lines:
                if l.strip():
                    current_indent = len(l) - len(l.lstrip())
                    if indent is None or current_indent < indent:
                        indent = current_indent
            # Menghilangkan indentasi dari setiap baris
            realigned_lines = []
            for l in lines:
                # Pastikan ada indentasi minimal
                if indent is not None:
                    realigned_lines.append(l[indent:])
                else:
                    realigned_lines.append(l)
            realigned = '\n'.join(realigned_lines)
            # Tambah ke daftar token, sekaligus kompilasi script menjadi object code
            tokens.append((True, compile(realigned, '<template> %s' % realigned[:20], 'exec')))
    return tokens
