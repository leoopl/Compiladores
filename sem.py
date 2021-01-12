from models.stack import Stack
from lex import listaDeTokens
from models.tabela_sintatica import Singleton

tabela_sintatica = Singleton.instance()


def check(p):
    if listaDeTokens[p][0] == 'if':
        return condicional(p)
    elif listaDeTokens[p][0] == ":=":
        return atribuicao(p-1)
    elif listaDeTokens[p][0] == "read" or listaDeTokens[p][0] == "write":
        return read_write(p)
    elif listaDeTokens[p][0] == "to":
        return toDo(p)
    elif listaDeTokens[p][0] == "while":
        return loop(p)
    elif listaDeTokens[p][0] == "do":
        return doUntil(p)
    return p


def condicional(p):
    print('cond')
    p += 1
    condition = []
    while listaDeTokens[p][0] != 'then':
        condition.append(listaDeTokens[p][0])
        p += 1
    conditionValue = calc(condition)
    #print(condition, conditionValue)
    if conditionValue == "False":
        while listaDeTokens[p][0] != 'else' and listaDeTokens[p][0] != 'fi':
            p += 1

        if listaDeTokens[p][0] == 'fi':
            return p
        p += 1
    # print(listaDeTokens[p][0])
    while listaDeTokens[p][0] != 'else' and listaDeTokens[p][0] != 'fi':
        p = check(p) + 1

    while listaDeTokens[p][0] != 'fi':
        p += 1
    #tabela_sintatica = Singleton.instance()
    # print(tabela_sintatica.tabela)
    return p


def read_write(p):
    print("read_write")
    return p


def toDo(p):
    id = listaDeTokens[p+1][0]
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
    p +=1 
    i = p
    while conditionValue == "True":
        if listaDeTokens[i][0] == "end":
            endPosition = i
            i = p
        i = check(i) + 1
        conditionValue = calc(condition)
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
    while conditionValue == "True":
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
        if token.isnumeric() or token not in ['+', '-', '*', '/', '(', ')', '>', '<', '=', '<=', '>=']:
            if not token.isnumeric():
                token = tabela_sintatica.tabela[token]['value']
                if not token.isnumeric():
                    # print(postfixList)
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
    # print(exp)
    postFix = infixToPostfix(exp)
   # print(postFix)
    output = Stack()
    while len(postFix) > 0:
        if postFix[0].isnumeric():
            output.push(postFix.pop(0))

        elif postFix[0] not in ['+', '-', '*', '/', '(', ')', '>', '<', '=', '<=', '>=']:
            output.push(tabela_sintatica.tabela[postFix.pop(0)]['value'])

        else:
            v1 = output.pop()
            v2 = output.pop()
            #print(v1, v2)
            if not v1.isnumeric() or not v2.isnumeric():
                print('erro! tipo não suportado')
                exit()
            else:
                v1 = int(v1)
                v2 = int(v2)

            if postFix[0] == "+":
                output.push(str(v1+v2))
            elif postFix[0] == '-':
                output.push(str(v2-v1))
            elif postFix[0] == '*':
                output.push(str(v1*v2))
            elif postFix[0] == '/':
                
                if isinstance((v2/v1),float):
                    print('erro! tipo não suportado')
                    exit()
                    
                output.push(str(v2/v1))
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