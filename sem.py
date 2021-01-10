from models.stack import Stack

flag_atrib = False
atrib = []
tabela_sintatica = {}

# {head: , itemKey: , token: , valueToken: , isTerminal: }


def precedence(op, opStack):

    if op in ['*', '/'] and opStack in ['+', '-']:
        return True

    if op == '(' or opStack == '(':
        return True

    if op in ['+', '-', ')']:
        return False

    else:
        return False


def toPostfix():
    global atrib
    global tabela_sintatica
    closeParFlag = False
    openParCount = 0
    token = atrib.pop(0)
    output = []
    stack = Stack()

    atrib.pop(0)
    print('inicio=>' + str(atrib))
    while len(atrib) > 0:
        if atrib[0].isnumeric():
            print('add isnumeric ' + atrib[0])
            output.append(int(atrib.pop(0)))

        elif atrib[0] not in ['+', '-', '*', '/', '(', ')']:
            if tabela_sintatica.get(atrib[0], False) and tabela_sintatica[atrib[0]].value != '':
                output.append(int(tabela_sintatica[atrib.pop(0)].value))
            else:
                print('erro! valor de identificador inválido.')
                exit()

        else:

            # push
            if stack.isEmpty() or precedence(atrib[0], stack.peek()):

                print('push ' + atrib[0])
                stack.push(atrib.pop(0))

            # pop
            else:
                if atrib[0] == ')':
                    while stack.peek() != '(':
                        print('add ' + stack.peek())
                        output.append(stack.pop())
                    atrib.pop(0)
                    stack.pop()
                else:
                    print('add ' + stack.peek())
                    output.append(stack.pop())

    while not stack.isEmpty():

        print('add ' + stack.peek())
        output.append(stack.pop())

    print('output:')
    print(output)
    return token, output


def calc():
    token, exp = toPostfix()
    output = Stack()
    print(token, exp)
    while len(exp) > 0:
        if type(exp[0]) == int:
            output.push(exp.pop(0))

        else:
            v1 = output.pop()
            v2 = output.pop()

            if exp[0] == "+":
                output.push(v1+v2)
            elif exp[0] == '-':
                output.push(v2-v1)
            elif exp[0] == '*':
                output.push(v1*v2)
            elif exp[0] == '/':
                if v1 == 0:
                    print('erro! Operação inválida, divisão por zero')
                    exit()
                output.push(int(v2/v1))
            else:
                print('erro! Operação inválida')
                exit()
            exp.pop(0)
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

atrib = ['x', ':=', '(', '11', '+', '2', ')', '-', '(', '3', '+', '4', ')']

res = calc()
print(res)
