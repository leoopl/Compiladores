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
            item == "id_proc" or item == "num" or item == "$" or item == "int" or item == "id" or item == "op_rel" 
            or item == "tipo_var" or item == "tipo_func")


def erro():
    print("erro sintatico")
    exit()


def addTerminal(item):
    for x in reversed(item):
        pilha_nt.push(x)
    print("pilha=> " + pilha_nt.toString())


def tokenValido():
    listaDeTokens.pop(0)
    pilha_nt.pop()


def getItemKey(item):

    # para simbolos nao-terminais, vazio($)
    if type(item) == str:
        return item

    # para simbolos terminais

    if item[1] == "op":
        return item[2]

    elif item[1] == "ident":

        aux = tabela_sintatica.check(item[0])
        if aux:
            return aux["cat"]

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
        token = getItemKey(listaDeTokens[0])
        print("tokens=> " + head + " " + token)

        if head == token and token == "$":
            fim = True

        elif not isTerminal(pilha_nt.peek()):  # se o item da pilha é nao-terminal

            aux = tabela_m.get(head, token)
            if aux == False:
                erro()

            if aux[0] != "$":
                pilha_nt.pop()

            addTerminal(aux)

            if head == "variaveis" or head == "lista_id":
                pilha_declara.push("id_var")

            elif head == "procedimento":
                pilha_declara.push("id_proc")

            elif head == "funcao":
                pilha_declara.push("id_func")

        else:

            if head == "$":
                pilha_nt.pop()
                pilha_nt.pop()
                print("pilha=> " + pilha_nt.toString())

            elif head == token or (token == "int" and (head == "tipo_var" or head == "tipo_func")):

                if token == "id":
                    aux = tabela_sintatica.check(listaDeTokens[0][0])
                    if aux or pilha_declara.isEmpty():  # se esta na tabela ou não esta sendo declarado
                        erro()

                    tabela_sintatica.addLexema(
                        listaDeTokens[0], pilha_declara.pop())

                elif token == "id_var" or token == "id_proc":
                    aux = tabela_sintatica.check(listaDeTokens[0][0])
                    if not aux:  # se nao esta declarada
                        erro()

                tokenValido()

            else:
                erro()


sin()
print(tabela_sintatica.tabela)
res = open("output_sintatico.pam", "w")
res.write(str(tabela_sintatica.tabela))
