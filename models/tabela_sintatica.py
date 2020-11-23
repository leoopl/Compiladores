class TSintatica:

    def __init__(self):
        self.tabela = {}

    def addLexema(self, lex, cat):
        aux = self.tabela.get(lex[0], False)

        if aux == False:
            self.tabela[lex[0]] = {
                "token": lex[1],
                "cat": cat,
                "value": "",
                "escopo": "global"
            }
            return self.tabela.get(lex[0])
        return False

    def check(self, lex):
        return self.tabela.get(lex, False)  



    def getCat(self, lex):
        return self.tabela[lex]["cat"]    