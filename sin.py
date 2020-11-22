import tabela_m as tabela_m
from lex import listaDeTokens
from stack import Stack

print(tabela_m.get("mais_fatores", "op_mul"))
pilha_nt = Stack()
pilha_nt.push("$")
pilha_nt.push("programa")

listaDeTokens.append("$")


def isTerminal(item):
    if type(item) == list:
        return True

    return (item == "op_ad" or item == "op_mul" or item == "op_atrib" or item == "id_var" or item == "id_func" or item == "id_proc" or item == "num" or item == "$" or item == "tipo_var")


def erro():
    print("erro sintatico")
    exit()


def addTerminal(item):
    for x in reversed(item):
        pilha_nt.push(x)


def getItemKey(item):

    # para simbolos terminais e vazio($)
    if type(item) == str:
        return item

    # para simbolos terminais

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
        if head == token:
            return "token-valido"

        if head == "$":
            return "$"

        return "erro"

    valorTabela = tabela_m.get(head, token)

    return "erro" if not valorTabela else "terminal"


def tokenValido():
    pilha_nt.pop()
    listaDeTokens.pop(0)


def sin():
    fim = False
    while not fim:
        head = getItemKey(pilha_nt.peek())
        token = getItemKey(listaDeTokens[0])
        print(head, token)
        res_compare = compare(head, token, pilha_nt.peek())
        print(res_compare)
        if res_compare == "fim":
            tokenValido()
            fim = True

        elif res_compare == "token-valido":
            tokenValido()

        elif res_compare == "terminal":
            if tabela_m.get(head, token)[0] != "$":
                pilha_nt.pop()
            addTerminal(tabela_m.get(head, token))

        elif res_compare == "$":
            pilha_nt.pop()
            pilha_nt.pop()

        elif res_compare == "erro":
            erro()


sin()