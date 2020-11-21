op = {">": "op_rel", "<": "op_rel",
      "=": "op_rel",  "+": "op_ad", "-": "op_ad", "*": "op_mul", "/": "op_mul", "<=": "op_rel",  ">=": "op_rel", "<>": "op_rel", ":=": "op_atrib"}
''
simbolos = {",": "simb", ";": "simb", ":": "simb", "(": "simb", ")": "simb"}

reservadas = {"begin": "reserv", "int": "reserv",
              "end": "reserv", "proc": "reserv", "func": "reserv",
              "read": "reserv", "until": "reserv", "write": "reserv", "to": "reserv", "do": "reserv", "if": "reserv", "fi": "reserv", "else": "reserv"}


token = ""


listaDeTokens = []


def addToken(e):
    global token
    estado = {
        1: 'op',
        2: 'simb',
        3: 'num',
        4: 'ident',
    }
    aux = [token, estado.get(e), "", ""]

    if e == 4:
        aux[2] = "reserv" if reservadas.get(token, False) else "id"

    elif e == 1:
        aux[2] = op.get(token)

    listaDeTokens.append(aux)
    token = ""


def charValido(ch):
    if 97 <= ord(ch) <= 119:
        return True
    return False


def erro():
    print("erro lexico")
    exit()


def espacamento(char, estadoAnterior):
    estadoAtual = 0
    global token
    if estadoAnterior != 0 and estadoAnterior != -1:
        addToken(estadoAnterior)

    if char == " " or char == "\t" or char == "\n" or char == "":
        if char == '':
            return
        return espacamento(file.read(1), estadoAtual)

    token = token + char

    if op.get(char, False):
        operador(file.read(1), estadoAtual)

    elif simbolos.get(char, False):
        simbolo(file.read(1), estadoAtual)

    elif char.isdigit():
        numero(file.read(1), estadoAtual)

    elif charValido(char):
        identificador(file.read(1), estadoAtual)

    else:
        erro()


def operador(char, estadoAnterior):
    estadoAtual = 1
    global token
    if char == " " or char == "\t" or char == "\n" or char == "":
        return espacamento(file.read(1), estadoAtual)

    if char.isdigit() or charValido(char):
        addToken(estadoAtual)
        token = token + char
        if char.isdigit():
            return numero(file.read(1), estadoAtual)
        return identificador(file.read(1), estadoAtual)

    token = token + char

    if op.get(token, False):
        operador(file.read(1), estadoAtual)

    else:
        erro()


def simbolo(char, estadoAnterior):

    estadoAtual = 2
    if char == " " or char == "\t" or char == "\n" or char == "":
        return espacamento(file.read(1), estadoAtual)

    else:
        erro()


def numero(char, estadoAnterior):
    estadoAtual = 3
    global token
    if char == " " or char == "\t" or char == "\n" or char == "":
        return espacamento(file.read(1), estadoAtual)

    if op.get(char, False):
        addToken(estadoAtual)
        token = token + char
        return operador(file.read(1), estadoAtual)

    token = token + char
    if char.isdigit():
        numero(file.read(1), estadoAtual)

    else:
        erro()


def identificador(char, estadoAnterior):
    estadoAtual = 4
    global token
    if char == " " or char == "\t" or char == "\n" or char == "":
        return espacamento(file.read(1), estadoAtual)

    if op.get(char, False):
        addToken(estadoAtual)
        token = token + char
        return operador(file.read(1), estadoAtual)

    token = token + char

    if charValido(char) or char.isdigit():
        identificador(file.read(1), estadoAtual)

    else:
        erro()


file = open("programa_pam.pam", "r")
espacamento(file.readline(1), -1)
output = open("tabela_de_tokens.pam", "w")
output.write(str(listaDeTokens))
