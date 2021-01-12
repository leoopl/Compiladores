from models.stack import Stack
from lex import listaDeTokens
from models.tabela_sintatica import Singleton

tabela_sintatica = Singleton.instance()


def check(p):
    if listaDeTokens[p][0] == 'if':
        return condicional(p)
    elif listaDeTokens[p][0] == ":=":
        return atribuicao(p - 1)
    elif listaDeTokens[p][0] == "read" or listaDeTokens[p][0] == "write":
        return write_read(p)
    elif listaDeTokens[p][0] == "to":
        return toDo(p)
    elif listaDeTokens[p][0] == "while":
        return loop(p)
    elif listaDeTokens[p][0] == "do":
        return doUntil(p)
    return p


def condicional(p):
    p += 1
    condition = []
    while listaDeTokens[p][0] != 'then':
        condition.append(listaDeTokens[p][0])
        p += 1
    conditionValue = calc(condition)
    pilha_bloco = Stack()
    if conditionValue == "False":
        while (listaDeTokens[p][0] != 'else' and listaDeTokens[p][0] != 'fi') or not pilha_bloco.isEmpty():
            if listaDeTokens[p][0] == 'if' or listaDeTokens[p][0] == "to" or listaDeTokens[p][0] == "while":
                pilha_bloco.push(listaDeTokens[p][0])
            elif listaDeTokens[p][0] == 'end' or listaDeTokens[p][0] == "fi":
                pilha_bloco.pop()

            p += 1

        if listaDeTokens[p][0] == 'fi':
            return p
        p += 1
    while listaDeTokens[p][0] != 'else' and listaDeTokens[p][0] != 'fi':
        p = check(p) + 1

    while listaDeTokens[p][0] != 'fi':
        p += 1
    return p


def wrCont(p):
    next = listaDeTokens[p] #listaDeTokens+1
    while (next[0] != ';'):
        if next[2] == 'id' or next[3] == 'id_var':
            if (tabela_sintatica.tabela[next[0]]['value']).isnumeric():
              pass
            else:
              print("Error!!!")
              exit()         
        elif next[0] == ',':
            pass
        else:
            print("Error read or write variable")
            exit()
        p = p+1
        next = listaDeTokens[p]
    return p


def write_read(p):
    now = listaDeTokens[p]
    if now[0] == 'read':
        return wrCont(p+1)

    elif now[0] == 'write':
        return wrCont(p+1)


def toDo(p):
    id = listaDeTokens[p + 1][0]
    p += 3
    while listaDeTokens[p][0] != 'end':
        p = check(p) + 1

    return p


def loop(p):
    p += 1
    endPosition = None
    condition = []
    while listaDeTokens[p][0] != 'do':
        condition.append(listaDeTokens[p][0])
        p += 1
    conditionValue = calc(condition)
    p += 1
    i = p

    while conditionValue == "True":
        while listaDeTokens[i][0] != 'end':
            i = check(i) + 1
            conditionValue = calc(condition)

        endPosition = i
        i = p
    
    #caso o while inicie com condição falsa
    if endPosition == None:
        pilha_bloco = Stack()
        while listaDeTokens[p][0] != 'end' or not pilha_bloco.isEmpty():
            if listaDeTokens[p][0] == 'if' or listaDeTokens[p][0] == "to" or listaDeTokens[p][0] == "while":
                pilha_bloco.push(listaDeTokens[p][0])
            elif listaDeTokens[p][0] == 'end' or listaDeTokens[p][0] == "fi":
                pilha_bloco.pop()

            p += 1
        endPosition = p

    return endPosition


def doUntil(p):
    i = p
    while listaDeTokens[i][0] != "until":
        i += 1
    i += 1

    condition = []
    while listaDeTokens[i][0] != ';':
        condition.append(listaDeTokens[i][0])
        i += 1

    endPosition = i
    conditionValue = calc(condition)
    p += 1
    i = p
    while conditionValue == "False":
        if listaDeTokens[i][0] == "until":
            i = p
        i = check(i) + 1
        conditionValue = calc(condition)
    return endPosition


def atribuicao(p):
    variable = listaDeTokens[p][0]
    p += 2
    exp = []
    while listaDeTokens[p][0] != ";":
        exp.append(listaDeTokens[p][0])
        p += 1
    tabela_sintatica.tabela[variable]["value"] = calc(exp)
    return p


def infixToPostfix(tokenList):
    prec = {}
    prec["*"] = 3
    prec["/"] = 3
    prec["+"] = 2
    prec["-"] = 2
    prec["("] = 1
    prec[">"] = 0
    prec["<"] = 0
    prec["="] = 0
    prec[">="] = 0
    prec["<="] = 0

    opStack = Stack()
    postfixList = []
    for token in tokenList:
        if token.isnumeric() or token not in [
                '+', '-', '*', '/', '(', ')', '>', '<', '=', '<=', '>='
        ]:
            if not token.isnumeric():
                token = tabela_sintatica.tabela[token]['value']
                if not token.isnumeric():
                    print("erro! variável sem valor atribuído." + token)
                    exit()
            postfixList.append(token)
        elif token == '(':
            opStack.push(token)
        elif token == ')':
            topToken = opStack.pop()
            while topToken != '(':
                postfixList.append(topToken)
                topToken = opStack.pop()
        else:
            while (not opStack.isEmpty()) and \
                    (prec[opStack.peek()] >= prec[token]):
                postfixList.append(opStack.pop())
            opStack.push(token)

    while not opStack.isEmpty():
        postfixList.append(opStack.pop())
    return postfixList


def calc(exp):
    tabela_sintatica = Singleton.instance()
    postFix = infixToPostfix(exp)
    output = Stack()
    while len(postFix) > 0:
        if postFix[0].isnumeric():
            output.push(postFix.pop(0))

        elif postFix[0] not in [
                '+', '-', '*', '/', '(', ')', '>', '<', '=', '<=', '>='
        ]:
            output.push(tabela_sintatica.tabela[postFix.pop(0)]['value'])

        else:
            v1 = output.pop()
            v2 = output.pop()
            if not v1.isnumeric() or not v2.isnumeric():
                print('erro! tipo não suportado')
                exit()
            else:
                v1 = int(v1)
                v2 = int(v2)

            if postFix[0] == "+":
                output.push(str(v1 + v2))
            elif postFix[0] == '-':
                output.push(str(v2 - v1))
            elif postFix[0] == '*':
                output.push(str(v1 * v2))
            elif postFix[0] == '/':
                if v1 == 0:
                    print("erro! divisão por 0")
                    exit()
                if v2 % v1 != 0:
                    print('Erro! tipo não suportado')
                    exit()
                output.push(str(int(v2 / v1)))
            elif postFix[0] == '=':
                output.push(str(v1 == v2))
            elif postFix[0] == '<':
                output.push(str(v2 < v1))
            elif postFix[0] == '>':
                output.push(str(v2 > v1))
            elif postFix[0] == '>=':
                output.push(str(v2 >= v1))
            elif postFix[0] == '<=':
                output.push(str(v2 <= v1))
            else:
                print('erro! Operação inválida')
                exit()
            postFix.pop(0)
    return output.pop()
