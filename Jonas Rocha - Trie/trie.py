class Node(object):
    '''
    A classe Node representa os nodes da arvore
    '''

    def __init__(self, char):
        self.letra = char
        self.filhos = []
        self.finalPalavra = False

    def __str__(self):
        return self.letra

    def fimPalavra(self):
        return self.finalPalavra

    def setFimPalavra(self, folha):
        self.finalPalavra = folha

    def freeNode(self):
        return len(self.filhos) == 0

    def indiceNode(self, letra):
        '''
        retorna o indice da letra na lista de filhos
        '''
        for i, j in enumerate(self.filhos):
            if letra == j.letra:
                index = i
        return index

class Trie(object):

    def __init__(self):
        self.root = Node(" ")

    def addPalavra(self, palavra ):
        '''
        Adiciona uma palavra na arvore se ela nao existir
        '''
        nodeAtual = self.root

        for le in palavra:
            foundLetra = False

            #percorre todos os nodes da lista de filhos do node atual
            for i in nodeAtual.filhos:
                if le == i.letra:
                    nodeAtual = i
                    foundLetra = True
                    # sai do for interno para procurar a proxima letra
                    break

            #se a letra nao existe, add na arvore
            if foundLetra == False:
                newNode = Node(le)
                nodeAtual.filhos.append(newNode)
                #o node atual passa a ser o novo node, para constinuar escrevendo a palavra
                nodeAtual = newNode
        # marca como fim da palavra
        nodeAtual.setFimPalavra(True)

    def searcPalavra(self, palavra):
        '''
        Procura se a palvra existe na arvore
        '''
        nodeAtual = self.root

        for le in palavra:

            for i in nodeAtual.filhos:
                foundLetra = False
                if le == i.letra:
                    nodeAtual = i
                    foundLetra = True
                    break

            if not foundLetra:
                return False

        return True if foundLetra and nodeAtual.fimPalavra() else False

    def deletePalavra(self, palavra):
        self.delete( self.root, palavra, 0, len(palavra))

    def delete(self,nodeAtual,key,level,length):
        '''
        Remover recursivamente os nodes da arvore
        '''
        if nodeAtual:
            # condicao de parada
            if level == length:

                if nodeAtual.fimPalavra():
                    nodeAtual.setFimPalavra(False)
                # retorna se o node pode ser removido da arvore
                return True if nodeAtual.freeNode() else False
            else:
                index = nodeAtual.indiceNode(key[level])

                if self.delete(nodeAtual.filhos[index], key,level+1,length):
                    # se for um node sem irmaos, o node eh removido da arvore
                    del nodeAtual.filhos[index]

                    return nodeAtual.fimPalavra() == False and nodeAtual.freeNode()
        return False

tree = Trie()

palavras = ['bola', 'bolada','bolas', 'bolinha', 'bolinhazinha', 'carro', 'carroca', 'carpete']

# Adicionando palavras na Trie
for i in palavras:
    tree.addPalavra(i)

print("\n================== Palavras Adicionadas ==================\n")

for i in palavras:
  print(i)

print("\n================== Palavras Buscadas ==================\n")

#buscando palavras
for i in palavras:
    print(i,'-->', tree.searcPalavra(i))

print("jonas",'-->', tree.searcPalavra("jonas"))
print("barraca",'-->', tree.searcPalavra("barraca"))


print("\n================== Palavras Deletadas ==================\n")

delPalavras = ['bolinha', 'carpete', 'bola']

#deletando palavras
for i in delPalavras:
    tree.deletePalavra(i)
    print(i)

print("\n================== Palavras Restantes ==================\n")

for i in palavras:
    print(i,'-->', tree.searcPalavra(i))
