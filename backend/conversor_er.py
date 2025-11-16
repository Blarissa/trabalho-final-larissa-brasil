from afn_epsilon import AFNEpsilon, Estado

class ConversorER:
    """Converte Expressões Regulares para AFN-ε usando Construção de Thompson"""
    
    def __init__(self):
        Estado.contador = 0
    
    def converter(self, expressao):
        """Converte uma expressão regular para AFN-ε"""
        Estado.contador = 0
        self.pos = 0
        self.expressao = expressao
        return self.parse_expressao()
    
    def parse_expressao(self):
        """Parse da expressão (união)"""
        termo = self.parse_termo()
        
        while self.pos < len(self.expressao) and self.expressao[self.pos] == '|':
            self.pos += 1
            proximo_termo = self.parse_termo()
            termo = self.uniao(termo, proximo_termo)
        
        return termo
    
    def parse_termo(self):
        """Parse de concatenação"""
        fator = self.parse_fator()
        
        while self.pos < len(self.expressao) and self.expressao[self.pos] not in '|)':
            proximo_fator = self.parse_fator()
            fator = self.concatenacao(fator, proximo_fator)
        
        return fator
    
    def parse_fator(self):
        """Parse de fator com fecho (*)"""
        base = self.parse_base()
        
        while self.pos < len(self.expressao) and self.expressao[self.pos] == '*':
            self.pos += 1
            base = self.fecho_kleene(base)
        
        return base
    
    def parse_base(self):
        """Parse de elemento básico (símbolo ou subexpressão)"""
        if self.pos >= len(self.expressao):
            return self.criar_epsilon()
        
        char = self.expressao[self.pos]
        
        if char == '(':
            self.pos += 1
            resultado = self.parse_expressao()
            if self.pos < len(self.expressao) and self.expressao[self.pos] == ')':
                self.pos += 1
            return resultado
        elif char == 'ε':
            self.pos += 1
            return self.criar_epsilon()
        else:
            self.pos += 1
            return self.criar_simbolo(char)
    
    def criar_simbolo(self, simbolo):
        """Cria AFN para um único símbolo"""
        afn = AFNEpsilon()
        inicial = Estado()
        final = Estado()
        
        afn.estado_inicial = inicial
        afn.estados_finais.add(final)
        afn.adicionar_transicao(inicial, simbolo, final)
        
        return afn
    
    def criar_epsilon(self):
        """Cria AFN para epsilon"""
        afn = AFNEpsilon()
        inicial = Estado()
        final = Estado()
        
        afn.estado_inicial = inicial
        afn.estados_finais.add(final)
        afn.adicionar_transicao(inicial, 'ε', final)
        
        return afn
    
    def concatenacao(self, afn1, afn2):
        """Concatena dois AFNs"""
        afn = AFNEpsilon()
        
        for (origem, simbolo), destinos in afn1.transicoes.items():
            for destino in destinos:
                afn.adicionar_transicao(origem, simbolo, destino)
        
        for (origem, simbolo), destinos in afn2.transicoes.items():
            for destino in destinos:
                afn.adicionar_transicao(origem, simbolo, destino)
        
        for final1 in afn1.estados_finais:
            afn.adicionar_transicao(final1, 'ε', afn2.estado_inicial)
        
        afn.estado_inicial = afn1.estado_inicial
        afn.estados_finais = afn2.estados_finais
        
        return afn
    
    def uniao(self, afn1, afn2):
        """Faz a união de dois AFNs"""
        afn = AFNEpsilon()
        
        novo_inicial = Estado()
        afn.estado_inicial = novo_inicial
        
        novo_final = Estado()
        afn.estados_finais.add(novo_final)
        
        for (origem, simbolo), destinos in afn1.transicoes.items():
            for destino in destinos:
                afn.adicionar_transicao(origem, simbolo, destino)
        
        for (origem, simbolo), destinos in afn2.transicoes.items():
            for destino in destinos:
                afn.adicionar_transicao(origem, simbolo, destino)
        
        afn.adicionar_transicao(novo_inicial, 'ε', afn1.estado_inicial)
        afn.adicionar_transicao(novo_inicial, 'ε', afn2.estado_inicial)
        
        for final1 in afn1.estados_finais:
            afn.adicionar_transicao(final1, 'ε', novo_final)
        for final2 in afn2.estados_finais:
            afn.adicionar_transicao(final2, 'ε', novo_final)
        
        return afn
    
    def fecho_kleene(self, afn1):
        """Aplica o fecho de Kleene em um AFN"""
        afn = AFNEpsilon()
        
        novo_inicial = Estado()
        novo_final = Estado()
        
        afn.estado_inicial = novo_inicial
        afn.estados_finais.add(novo_final)
        
        for (origem, simbolo), destinos in afn1.transicoes.items():
            for destino in destinos:
                afn.adicionar_transicao(origem, simbolo, destino)
        
        afn.adicionar_transicao(novo_inicial, 'ε', afn1.estado_inicial)
        afn.adicionar_transicao(novo_inicial, 'ε', novo_final)
        
        for final1 in afn1.estados_finais:
            afn.adicionar_transicao(final1, 'ε', novo_final)
            afn.adicionar_transicao(final1, 'ε', afn1.estado_inicial)
        
        return afn