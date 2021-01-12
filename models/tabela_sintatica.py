class Singleton:
    _instance = None
    tabela = None

    def __init__(self):
        self.tabela = {}

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def addLexema(self, lex, cat, fp=None):
        aux = self.tabela.get(lex[0], False)

        if aux == False:
            self.tabela[lex[0]] = {
                "token": lex[1],
                "cat": cat,
                "value": "",
                "escopo": "global"
            }
            if cat == "id_func" or cat == "id_proc":
                self.tabela[lex[0]]["inicialPosition"] = fp

            return self.tabela.get(lex[0])
        return False

    def check(self, lex):
        return self.tabela.get(lex, False)
