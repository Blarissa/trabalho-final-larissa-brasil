class Estado:
    """Representa um estado do autômato"""
    contador = 0
    
    def __init__(self, nome=None):
        if nome is None:
            self.nome = f"q{Estado.contador}"
            Estado.contador += 1
        else:
            self.nome = nome
    
    def __repr__(self):
        return self.nome
    
    def __eq__(self, other):
        return isinstance(other, Estado) and self.nome == other.nome
    
    def __hash__(self):
        return hash(self.nome)


class AFNEpsilon:
    """Autômato Finito Não Determinístico com transições epsilon"""
    
    def __init__(self):
        self.estados = set()
        self.alfabeto = set()
        self.transicoes = {}
        self.estado_inicial = None
        self.estados_finais = set()
    
    def adicionar_transicao(self, origem, simbolo, destino):
        """Adiciona uma transição ao autômato"""
        self.estados.add(origem)
        self.estados.add(destino)
        if simbolo != 'ε':
            self.alfabeto.add(simbolo)
        
        chave = (origem, simbolo)
        if chave not in self.transicoes:
            self.transicoes[chave] = set()
        self.transicoes[chave].add(destino)
    
    def fecho_epsilon(self, estados):
        """Calcula o fecho epsilon de um conjunto de estados"""
        pilha = list(estados)
        fecho = set(estados)
        
        while pilha:
            estado = pilha.pop()
            chave = (estado, 'ε')
            if chave in self.transicoes:
                for proximo in self.transicoes[chave]:
                    if proximo not in fecho:
                        fecho.add(proximo)
                        pilha.append(proximo)
        
        return fecho
    
    def mover(self, estados, simbolo):
        """Retorna os estados alcançáveis a partir de um conjunto de estados com um símbolo"""
        resultado = set()
        for estado in estados:
            chave = (estado, simbolo)
            if chave in self.transicoes:
                resultado.update(self.transicoes[chave])
        return resultado
    
    def reconhecer(self, cadeia):
        """Verifica se uma cadeia é aceita pelo autômato"""
        if self.estado_inicial is None:
            return False
        
        estados_atuais = self.fecho_epsilon({self.estado_inicial})
        
        for simbolo in cadeia:
            estados_atuais = self.fecho_epsilon(self.mover(estados_atuais, simbolo))
            if not estados_atuais:
                return False
        
        return bool(estados_atuais & self.estados_finais)
    
    def __str__(self):
        """Representação textual do autômato"""
        resultado = []
        str = f"""--- Autômato Finito Não Determinístico com ε-transições ---
                Estados: {{{', '.join(str(e) for e in sorted(self.estados, key=lambda x: x.nome))}}}
                Alfabeto: {{{', '.join(sorted(self.alfabeto))}}}
                Estado Inicial: {self.estado_inicial}
                Estados Finais: 
                {{{', '.join(str(e) for e in sorted(self.estados_finais, key=lambda x: x.nome))}}}
                Transições:
                """
        resultado.append(str)
        
        transicoes_ordenadas = sorted(self.transicoes.items(), 
                                      key=lambda x: (x[0][0].nome, x[0][1]))
        for (origem, simbolo), destinos in transicoes_ordenadas:
            destinos_str = ', '.join(str(d) for d in sorted(destinos, key=lambda x: x.nome))
            resultado.append(f"  δ({origem}, {simbolo}) = {{{destinos_str}}}")
        
        return '\n'.join(resultado)