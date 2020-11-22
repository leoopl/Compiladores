# -*- coding: utf-8 -*-

op = {">": "op_rel", "<": "op_rel",
      "=": "op_rel",  "+": "op_ad", "-": "op_ad", "*": "op_mul", "/": "op_mul", "<=": "op_rel",  ">=": "op_rel", "<>": "op_rel", ":=": "op_atrib"}
''
simbolos = {",": "simb", ";": "simb", ":": "simb", "(": "simb", ")": "simb"}

reservadas = {"begin": "reserv", "int": "reserv",
              "end": "reserv", "proc": "reserv", "func": "reserv",
              "read": "reserv", "until": "reserv", "write": "reserv",
              "to": "reserv", "do": "reserv", "if": "reserv", "fi": "reserv",
              "else": "reserv", "while": "reserv", "then": "reserv"}


token = ""


listaDeTokens = []


def opAtrib():
    pos = file.tell()
    prox = file.read(1)
    print(prox)
    file.seek(pos)
    return True if prox == "=" else False


def addToken(e):
    global token
    print("add " + token)
    estado = {
        1: 'ident',
        2: 'op',
        3: 'simb',
        4: 'num',
    }
    aux = [token, estado.get(e), "", ""]

    if e == 1:
        aux[2] = "reserv" if reservadas.get(token, False) else "id_var"

    elif e == 2:
        aux[2] = op.get(token)

    listaDeTokens.append(aux)
    token = ""


def charValido(ch):
    if 97 <= ord(ch) <= 122:
        return True
    return False


def erro(char):
    print('erro lexico, caractere "'+char+'" nao reconhecido')
    exit()


def espaco(char, estadoAnterior):
    global token
    print("espaço: char->" + char+(" ")+token)
    estadoAtual = 0
    if estadoAnterior != 0 and estadoAnterior != -1:
        addToken(estadoAnterior)

    if char == " " or char == "\t" or char == "\n" or char == "":

        if char == "":
            return
        return espaco(file.read(1), estadoAtual)

    token += char

    if charValido(char):
        identificador(file.read(1), estadoAtual)

    elif char.isdigit():
        numero(file.read(1), estadoAtual)

    elif op.get(char, False):
        operador(file.read(1), estadoAnterior)

    elif simbolos.get(char, False):
        if char == ":":
            if opAtrib():
                operador(file.read(1), estadoAnterior)
            else:
                simbolo(file.read(1), estadoAnterior)
        else:
            simbolo(file.read(1), estadoAnterior)
    else:
        erro(char)


def identificador(char, estadoAnterior):
    global token
    print("ident: char->" + char+(" ")+token)
    estadoAtual = 1

    if char == " " or char == "\t" or char == "\n" or char == "":
        espaco(file.read(1), estadoAtual)

    elif charValido(char) or char.isdigit():
        token += char
        identificador(file.read(1), estadoAtual)

    elif op.get(char, False):
        addToken(estadoAtual)
        token += char
        operador(file.read(1), estadoAnterior)

    elif simbolos.get(char, False):
        addToken(estadoAtual)
        token += char
        if char == ":":
            if opAtrib():
                operador(file.read(1), estadoAtual)
            else:
                simbolo(file.read(1), estadoAtual)
        else:
            simbolo(file.read(1), estadoAtual)

    else:
        erro(char)


def operador(char, estadoAnterior):
    global token
    print("op: char->" + char+(" ")+token)
    estadoAtual = 2
    if char == " " or char == "\t" or char == "\n" or char == "":
        espaco(file.read(1), estadoAtual)

    elif charValido(char):
        addToken(estadoAtual)
        token += char
        identificador(file.read(1), estadoAtual)

    elif char.isdigit():
        addToken(estadoAtual)
        token += char
        numero(file.read(1), estadoAtual)

    elif op.get(char, False):
        if op.get(token+char, False):
            token += char
            espaco(file.read(1), estadoAtual)
        else:
            addToken(estadoAtual)
            token += char
            operador(file.read(1), estadoAtual)

    elif simbolos.get(char, False):
        addToken(estadoAtual)
        token += char
        if char == ":":
            if opAtrib():
                operador(file.read(1), estadoAtual)
            else:
                simbolo(file.read(1), estadoAtual)
        else:
            simbolo(file.read(1), estadoAtual)

    else:
        erro(char)


def simbolo(char, estadoAnterior):
    global token
    print("simb: char->" + char+(" ")+token)
    estadoAtual = 3
    if char == " " or char == "\t" or char == "\n" or char == "":
        espaco(file.read(1), estadoAtual)

    elif charValido(char):
        addToken(estadoAtual)
        token += char
        identificador(file.read(1), estadoAtual)

    elif char.isdigit():
        addToken(estadoAtual)
        token += char
        numero(file.read(1), estadoAtual)

    elif op.get(char, False):
        addToken(estadoAtual)
        token += char
        operador(file.read(1), estadoAtual)

    elif simbolos.get(char, False):
        addToken(estadoAtual)
        token += char
        if char == ":":
            if opAtrib():
                operador(file.read(1), estadoAtual)
            else:
                simbolo(file.read(1), estadoAtual)
        else:
            simbolo(file.read(1), estadoAtual)
    else:
        erro(char)


def numero(char, estadoAnterior):
    global token
    print("num: char->" + char+(" ")+token)
    estadoAtual = 4
    if char == " " or char == "\t" or char == "\n" or char == "":
        espaco(file.read(1), estadoAtual)

    elif char.isdigit():
        token += char
        numero(file.read(1), estadoAtual)

    elif op.get(char, False):
        addToken(estadoAtual)
        token += char
        operador(file.read(1), estadoAtual)

    elif simbolos.get(char, False):
        addToken(estadoAtual)
        token += char
        if char == ":":
            if opAtrib():
                operador(file.read(1), estadoAtual)
            else:
                simbolo(file.read(1), estadoAtual)
        else:
            simbolo(file.read(1), estadoAtual)
    else:
        erro(char)


file = open("programa_pam.pam", "r")
espaco(file.read(1), -1)
res = open("tabela_de_tokens.pam", "w")
res.write(str(listaDeTokens))