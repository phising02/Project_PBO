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
                if l.strip():  # Hanya pertimbangkan baris yang tidak kosong
                    current_indent = len(l) - len(l.lstrip())
                    if indent is None or current_indent < indent:
                        indent = current_indent
            
            # Menghilangkan indentasi dari setiap baris
            realigned_lines = [l[indent:] for l in lines]
            realigned = '\n'.join(realigned_lines)
            
            # Tambah ke daftar token, sekaligus kompilasi script menjadi object code
            tokens.append((True, compile(realigned, '<template> %s' % realigned[:20], 'exec')))
    
    return tokens

def compile_template(tokens, context=None, **keywrd_args):
    global_context = {}
    
    if context:
        global_context.update(context)
    
    if keywrd_args:
        global_context.update(keywrd_args)
    
    # Tambahkan fungsi untuk output
    result = []
    
    def echo(*args):
        result.extend([str(arg) for arg in args])
    
    def echo_fmt(fmt, *args):
        result.append(fmt % args)
    
    global_context['echo'] = echo
    global_context['echo_fmt'] = echo_fmt
    
    # Jalankan kode atau tampilkan text biasa
    for is_code, token in tokens:
        if is_code:
            exec(token, global_context)
        else:
            result.append(token)
    
    return ''.join(result)
