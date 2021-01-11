from models.stack import Stack

flag_atrib = False
atrib = []
tabela_sintatica = {}

# {head: , itemKey: , token: , valueToken: , isTerminal: }


def condicional(p, listaDeTokens):
    print(p, listaDeTokens)





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

    opStack = Stack()
    postfixList = []
    for token in tokenList:
        if token.isnumeric() or token not in ['+', '-', '*', '/', '(', ')', '>', '<', '=']:
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


def calc(exp, tabela_sintatica):
    postFix = infixToPostfix(exp)
    print(postFix)
    output = Stack()
    while len(postFix) > 0:
        if postFix[0].isnumeric():
            output.push(postFix.pop(0))

        elif postFix[0] not in ['+', '-', '*', '/', '(', ')', '>', '<', '=']:
            output.push(tabela_sintatica[postFix.pop(0)]['value'])

        else:
            v1 = output.pop()
            v2 = output.pop()
            print(v1, v2)
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
                output.push(str(v2/v1))
            elif postFix[0] == '=':
                output.push(str(v1 == v2))
            elif postFix[0] == '<':
                output.push(str(v2 < v1))
            elif postFix[0] == '>':
                output.push(str(v2 > v1))
            else:
                print('erro! Operação inválida')
                exit()
            postFix.pop(0)
    return output.pop()


def atribuicao(data):
    global atrib, flag_atrib
    if isTerminal:
        if data.token == ';':
            calc()
            flag_atrib = False
        else:
            atrib.append(data.token)


def analise_semantica(data):
    global flag_atrib
    if flag_atrib:
        atribuicao(data)


atrib = ['(', '3', '+', '4', ')', '/', '(', '3', '+', '4', ')']



res = calc(atrib, {})
print(res)


