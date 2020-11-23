import models.tabela_m as tabela_m
from lex import listaDeTokens
from models.stack import Stack
from models.tabela_sintatica import TSintatica

pilha_nt = Stack()
pilha_nt.push("$")
pilha_nt.push("programa")
tabela_sintatica = TSintatica()
pilha_declara = Stack()
listaDeTokens.append("$")


def isTerminal(item):
    if type(item) == list:
        return True

    return (item == "op_ad" or item == "op_mul" or item == "op_atrib" or item == "id_var" or item == "id_func" or
            item == "id_proc" or item == "num" or item == "$" or item == "tipo_var" or item == "id")


def erro():
    print("erro sintatico")
    exit()


def addTerminal(item):
    for x in reversed(item):
        pilha_nt.push(x)


def tokenValido():
    listaDeTokens.pop(0)
    pilha_nt.pop()
    isEmpty = True if len(listaDeTokens) == 0 else False
    if pilha_nt.isEmpty() != isEmpty:
        erro()


def getItemKey(item):

    # para simbolos nao-terminais e vazio($)
    if type(item) == str:
        return item

    # para simbolos terminais
    aux = tabela_sintatica.check(item[0])
    if aux:
        return aux["cat"]

    if item[1] == "op":
        return item[2]

    elif item[1] == "ident":
        if item[0] == "int":
            return "tipo_var"
        return item[0] if item[2] == "reserv" else item[2]

    if item[1] == "simb":
        return item[0]

    else:
        return item[1]


def compare(head, token, item_pilha):

    if head == token == "$":
        return "fim"

    if isTerminal(item_pilha):

        if head == token or (token == "id"):
            return "token-valido"

        if head == "$":
            return "$"

        return "erro"

    valorTabela = tabela_m.get(head, token)

    return "nao-terminal"


def sin():
    fim = False
    while not fim:
        head = getItemKey(pilha_nt.peek())
        if tabela_sintatica.check(listaDeTokens[0][0]):
            token = tabela_sintatica.getCat(listaDeTokens[0][0])
        else:
            token = getItemKey(listaDeTokens[0])
        res_compare = compare(head, token, pilha_nt.peek())
        if res_compare == "fim":
            tokenValido()
            fim = True

        elif res_compare == "token-valido":
            if token == "id":
                aux = tabela_sintatica.check(listaDeTokens[0][0])
                if not aux:  # se nao esta na tabela
                    if pilha_declara.isEmpty():
                        erro()
                    tabela_sintatica.addLexema(
                        listaDeTokens[0], pilha_declara.pop())

                else:  # se esta na tabela
                    if not pilha_declara.isEmpty():
                        erro()

            tokenValido()

        elif res_compare == "nao-terminal":

            aux = tabela_m.get(head, token)

            if (head == "declara" and token == "tipo_var") or (head == "mais_var" and token == ","):
                pilha_declara.push("id_var")

            if (head == "procedimento" and token == "proc"):
                pilha_declara.push("id_proc")

            if (head == "funcao" and token == "func"):
                pilha_declara.push("id_func")

            if (head == "lista_parametros" and token == "id"):
                pilha_declara.push("id_var")

            if aux[0] != "$":
                pilha_nt.pop()

            addTerminal(tabela_m.get(head, token))
        elif res_compare == "$":
            pilha_nt.pop()
            pilha_nt.pop()
        elif res_compare == "erro":
            erro()


sin()
print(tabela_sintatica.tabela)
res = open("output_sintatico.pam", "w")
res.write(str(tabela_sintatica.tabela))
