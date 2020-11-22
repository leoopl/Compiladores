import tabela_m as tabela
op = {">": "rel", "<": "rel",
      "=": "rel",  "+": "op_ad",\
      "-": "op_ad", "*": "op_mul",\
      "/": "op_mul", "<=": "op_rel",\
      ">=": "op_rel", "<>": "op_rel",\
      ":=": "op_atrib"}#op organizado
from lex import erro#importado o metodo erro para uso na função analisador_sintatico()

listaTokens = []
pilhaNT = []


def push(data):

    while not data.empty():
        tipoToken = "nt"

        if type(data[0]) == list:
            tipoToken = "t"
        #não existe o método .empty pra checar se a lista é vazia, substituido por if list == []
        elif (data[0] == "op_ad" | data[0] == "op_mul" | data[0] == "op_rel" | data[0] == "op_atrib" |\
        data[0] == "id_var" | data[0] == "id_proc" | data[0] == "id_func" | data[0] == "num" | data[0] == "$"):
            tipoToken = "t"

        pilhaNT.append([data.pop(), tipoToken])

def compare(pilha, token):
    if pilha == token:
        pilhaNT.pop()
        return listaTokens.pop()

    aux = tabela.get(pilha, token)
    if aux:
        if aux  == "$":
            return pilhaNT.pop()
     
def analisador_sintatico():
    #não existe o método .push em lista, substituido por .append
    pilhaNT.append(["$"])
    pilhaNT.append(["programa"])
    fim = False
    while not fim:
        head = pilhaNT[0]#não exite o método .top, substituido por [0]

        if pilhaNT == [] and not listaTokens == [] or not pilhaNT== [] and listaTokens== []:
            erro()
            exit()

        if head[1] == "t":
            if type(head[0]) == list:
                if head[0][1] == "op":
                    break