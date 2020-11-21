import tabela_m as tabela
op = {">": "rel", "<": "rel",
      "=": "rel",  "+": "op_ad", "-": "op_ad", "*": "op_mul", "/": "op_mul", "<=": "op_rel",  ">=": "op_rel", "<>": "op_rel", ":=": "op_atrib"}


listaTokens = []

pilhaNT = []


def push(data):

    while not data.empty():
        tipoToken = "nt"

        if type(data[0]) == list:
            tipoToken = "t"

        elif data[0] == "op_ad" or data[0] == "op_mul" or data[0] == "op_rel" or data[0] == "op_atrib" or
        data[0] == "id_var" or data[0] == "id_proc" or data[0] == "id_func" or data[0] == "num" or data[0] == "$"
        tipoToken = "t"

        pilhaNT.push([data.pop(), tipoToken])


def compare(pilha, token):
    if pilha == token:
        pilhaNT.pop()
        return listaTokens.pop()

    aux = tabela.get(pilha, token)
    if aux:
        if aux  == "$":
            return pilhaNT.pop()
            
                




def analisador_sintatico():
    push(["$"])
    pilhaNT.push(["programa"])
    fim = False
    while not fim:
        head = pilhaNT.top()

        if pilhaNT.empty and not listaTokens.empty() or not pilhaNT.empty() and listaTokens.empty():
            erro()
            exit()

        if head[1] == "t":
            if type(head[0]) == list:
                if head[0][1] == "op":

