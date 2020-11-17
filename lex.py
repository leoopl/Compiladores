op = {">": "op", "<": "op",
      "=": "op",  "+": "op", "-": "op", "*": "op", "/": "op"}

op_composto = {"<=": "comp",  ">=": "comp", "<>": "comp"}

simbolos = {",": "simb", ";": "simb", ":": "simb", "(": "simb", ")": "simb"}

reservadas = {"begin": "reserv", "int": "reserv", "end": "reserv"}


token = ""


listaDeTokens = []


def addToken(e):
    global token
    estado = {
        1: 'op_simples',
        2: 'simb',
        3: 'num',
        4: 'ident',
        5: 'op_comp',
        6: 'reserv',
    }
    listaDeTokens.append([token, estado.get(e)])
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

    token = token + char
    if op.get(char, False):
        operadorComposto(file.read(1), estadoAtual)

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

    token = token + char

    if charValido(char) or char.isdigit():
        if reservadas.get(token, False):
            return reservada(file.read(1), estadoAtual)
        identificador(file.read(1), estadoAtual)

    else:
        erro()


def operadorComposto(char, estadoAnterior):

    estadoAtual = 5

    if not op_composto.get(token, False):
        print("operador invalido!")
        exit()

    if char == " " or char == "\t" or char == "\n" or char == "":
        return espacamento(file.read(1), estadoAtual)

    else:
        erro()


def reservada(char, estadoAnterior):
    estadoAtual = 6
    if char == " " or char == "\t" or char == "\n" or char == "":
        return espacamento(file.read(1), estadoAtual)

    global token
    token = token + char
    if charValido(char) or char.isdigit():
        identificador(file.read(1), estadoAtual)

    else:
        erro()


file = open("programa_pam.pam", "r")
espacamento(file.readline(1), -1)
output = open("tabela_de_tokens.pam", "w")
output.write(str(listaDeTokens))
