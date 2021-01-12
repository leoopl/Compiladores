M = {
    "programa": {
        "tipo_var": ["declara", "rotina", ["begin", "ident", "reserv"], "sentencas", ["end", "ident", "reserv"]],
        "proc": ["declara", "rotina", ["begin", "ident", "reserv"], "sentencas", ["end", "ident", "reserv"]],
        "func": ["declara", "rotina", ["begin", "ident", "reserv"], "sentencas", ["end", "ident", "reserv"]],
        "begin": ["declara", "rotina", ["begin", "ident", "reserv"], "sentencas", ["end", "ident", "reserv"]],

    },
    "declara": {

        "tipo_var": ["tipo_var", "variaveis", [";", "simb"], "declara"],
        "$": ["$"],
        ";": ["$"],
        "proc": ["$"],
        "func": ["$"],
        "begin": ["$"]

    },
    "variaveis": {
        "id": ["id", "mais_var"],
    },
    "mais_var": {
        ",": [[",", "simb"], "variaveis"],
        ";": ["$"],
        "$": ["$"]
    },
    "rotina": {
        "proc": ["procedimento"],
        "func": ["funcao"],
        "$": ["$"],
        "begin": ["$"]
    },
    "procedimento": {
        "proc": [["proc", "ident", "reserv"], "id", "parametros", [";", "simb"], "declara", ["begin", "ident", "reserv"], "sentencas", ["end", "ident", "reserv"], "rotina"]
    },
    "funcao": {
        "func": [["func", "ident", "reserv"], "id", "parametros", [":", "simb"], "tipo_func", [";", "simb"], "declara", ["begin", "ident", "reserv"], "sentencas", ["end", "ident", "reserv"], "rotina"]
    },
    "parametros": {
        "(": [["(", "simb"], "lista_parametros", [")", "simb"]],
        "$": ["$"],
        ";": ["$"],
        ":": ["$"],

    },
    "lista_parametros": {
        "id": ["lista_id", [":", "simb"], "tipo_var", "cont_lista_par"]
    },
    "cont_lista_par": {
        ";": [[";", "simb"], "lista_parametros"],
        "$": ["$"],
        ")": ["$"]
    },
    "lista_id": {
        "id": ["id", "cont_lista_id"]
    },
    "cont_lista_id": {
        ",": [[",", "simb"], "lista_id"],
        "$": ["$"],
        ":": ["$"],
    },
    "sentencas": {
        "read": ["comando", "mais_sentencas"],
        "write": ["comando", "mais_sentencas"],
        "to": ["comando", "mais_sentencas"],
        "do": ["comando", "mais_sentencas"],
        "while": ["comando", "mais_sentencas"],
        "if": ["comando", "mais_sentencas"],
        "id_var": ["comando", "mais_sentencas"],
        "id_proc": ["comando", "mais_sentencas"]
    },
    "mais_sentencas": {
        ";": [[";", "simb"], "cont_sentencas"]
    },
    "cont_sentencas": {
        "read": ["sentencas"],
        "write": ["sentencas"],
        "to": ["sentencas"],
        "do": ["sentencas"],
        "while": ["sentencas"],
        "if": ["sentencas"],
        "id_var": ["sentencas"],
        "id_proc": ["sentencas"],
        "$": ["$"],
        "end": ["$"],
        "until": ["$"],
        "else": ["$"],
        "fi": ["$"]
    },
    "var_read": {
        "id_var": ["id_var", "mais_var_read"]
    },
    "mais_var_read": {
        ",": [[",", "simb"], "var_read"],
        "$": ["$"],
        ";": ["$"]
    },
    "var_write": {
        "id_var": ["id_var", "mais_var_write"]
    },
    "mais_var_write": {
        ",": [[",", "simb"], "var_write"],
        "$": ["$"],
        ";": ["$"]
    },
    "comando": {
        "read": [["read", "ident", "reserv"], "var_read"],
        "write": [["write", "ident", "reserv"], "var_write"],
        "to": [["to", "ident", "reserv"], "id_var", ["do", "ident", "reserv"], "sentencas", ["end", "ident", "reserv"]],
        "do": [["do", "ident", "reserv"], "sentencas", ["until", "ident", "reserv"], "condicao"],
        "while":  [["while", "ident", "reserv"], "condicao", ["do", "ident", "reserv"],
                   "sentencas", ["end", "ident", "reserv"]],
        "if": [["if", "ident", "reserv"], "condicao", ["then", "ident", "reserv"],
               "sentencas", "pfalsa", ["fi", "ident", "reserv"]],
        "id_var": ["id_var", "op_atrib", "expressao"],
        "id_proc":  ["chamada_procedimento"],
    },
    "chamada_procedimento": {
        "id_proc": ["id_proc", "argumentos"]
    },
    "argumentos": {
        "(": [["(", "simb"], "lista_arg", [")", "simb"]],
        "$": ["$"],
        "op_mul": ["$"],
        ",": ["$"],
        ")": ["$"],
        "op_rel": ["$"],
        "do": ["$"],
        "then": ["$"],
        ";": ["$"],
        "op_ad": ["$"]
    },
    "lista_arg": {
        "id_var": ["expressao", "cont_lista_arg"],
        "num": ["expressao", "cont_lista_arg"],
        "(": ["expressao", "cont_lista_arg"],
        "id_func": ["expressao", "cont_lista_arg"]
    },
    "cont_lista_arg": {
        ",": [[",", "simb"], "lista_arg"],
        "$": ["$"],
        ")": ["$"]
    },
    "condicao": {
        "id_var": ["expressao", "op_rel", "expressao"],
        "num": ["expressao", "op_rel", "expressao"],
        "(": ["expressao", "op_rel", "expressao"],
        "id_func": ["expressao", "op_rel", "expressao"]
    },
    "pfalsa": {
        "else": [["else", "ident", "reserv"], "sentencas"],
        "$": ["$"],
        "fi": ["$"]
    },
    "expressao": {
        "id_var": ["termo", "outros_termos"],
        "num": ["termo", "outros_termos"],
        "(": ["termo", "outros_termos"],
        "id_func": ["termo", "outros_termos"]
    },
    "outros_termos": {
        "op_ad": ["op_ad", "termo", "outros_termos"],
        "$": ["$"],
        ",": ["$"],
        ")": ["$"],
        "op_rel": ["$"],
        "do": ["$"],
        "then": ["$"],
        ";": ["$"],
    },
    "termo": {
        "id_var": ["fator", "mais_fatores"],
        "num": ["fator", "mais_fatores"],
        "(": ["fator", "mais_fatores"],
        "id_func": ["fator", "mais_fatores"],
    },
    "mais_fatores": {
        "op_mul": ["op_mul", "fator", "mais_fatores"],
        "$": ["$"],
        ",": ["$"],
        ")": ["$"],
        "op_rel": ["$"],
        "do": ["$"],
        "then": ["$"],
        ";": ["$"],
        "op_ad": ["$"]
    },
    "fator": {
        "id_var": ["id_var"],
        "num": ["num"],
        "(":  [["(", "simb"], "expressao", [")", "simb"]],
        "id_func": ["id_func", "argumentos"]
    }

}


def get(lin, col):

    if not M.get(lin):
        print("erro! não-terminal inexistente")
        exit()

    if col == "int":
        aux = M[lin].get("tipo_var", False)
        if not aux:
            aux = M[lin].get("tipo_func", False)

    else:
        aux = M[lin].get(col, False)

    return aux
