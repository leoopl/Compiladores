import models.tabela_m as tabela_m
from lex import listaDeTokens
from models.stack import Stack
from models.tabela_sintatica import Singleton
import json
import sem

pilha_nt = Stack()
pilha_nt.push("$")
pilha_nt.push("programa")
tabela_sintatica = Singleton.instance()
pilha_declara = Stack()
listaDeTokens.append("$")
pilha_condicional = Stack()
fila_analise_semantica = []
p = 0


escopo = Stack()
escopo


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
    # print("pilha=> " + pilha_nt.toString())


def tokenValido():
    global p
    p += 1
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


def sin():

    fim = False

    while not fim:

        head = getItemKey(pilha_nt.peek())
        token = getItemKey(listaDeTokens[p])

        # print("tokens=> " + head + " " + token)

        if head == token and token == "$":
            fim = True

        elif not isTerminal(pilha_nt.peek()):  # se o item da pilha é nao-terminal

            aux = tabela_m.get(head, token)
            if aux == False:
                erro()

            if aux[0] != "$":
                pilha_nt.pop()

            addTerminal(aux)

            # or (head == "comando" and token == "to")
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
                # ("pilha=> " + pilha_nt.toString())

            elif head == token or (token == "int" and (head == "tipo_var" or head == "tipo_func")):

                if token == "id":
                    aux = tabela_sintatica.check(listaDeTokens[p][0])
                    if aux or pilha_declara.isEmpty():  # se está na tabela ou não esta sendo declarado
                        erro()

                    tabela_sintatica.addLexema(
                        listaDeTokens[p], pilha_declara.pop(), p - 1)

                elif token == "id_var" or token == "id_proc":
                    aux = tabela_sintatica.check(listaDeTokens[p][0])
                    if not aux:  # se nao está declarada
                        erro()

                # semantico

                    # em caso de comandos de bloco
                if token == 'if' or token == 'proc' or token == 'func' or token == "to" or token == "while":
                    pilha_condicional.push({"token": token, "position": p})

                elif not pilha_condicional.isEmpty() and (token == 'fi' or token == 'end'): # em caso de comandos de bloco
                    aux = pilha_condicional.pop()
                    if pilha_condicional.isEmpty():
                        fila_analise_semantica.append(aux['position'])
                    #

                    # comandos sem bloco
                elif pilha_condicional.isEmpty():
                    if token == "op_atrib" or token == "do" or token == "read" or token == "write":
                        fila_analise_semantica.append(p)
                    #    
                #

                tokenValido()

            else:
                erro()


sin()
for i in fila_analise_semantica:
    sem.check(i)
print(tabela_sintatica.tabela)
res = open("output_sintatico.json", "w")
res.write(json.dumps(tabela_sintatica.tabela))
