import numpy as np
import queue
import cv2


class Node:
	def __init__(self):
		self.prob = None
		self.code = None
		self.data = None
		self.left = None
		self.right = None
	def __lt__(self, other):
		if (self.prob < other.prob):		
			return 1
		else:
			return 0
	def __ge__(self, other):
		if (self.prob > other.prob):
			return 1
		else:
			return 0

def get2smallest(data):
    first = second = 1;
    fid=sid=0
    for idx,element in enumerate(data):
        if (element < first):
            second = first
            sid = fid
            first = element
            fid = idx
        elif (element < second and element != first):
            second = element
    return fid,first,sid,second
    
def tree(probabilities):
	prq = queue.PriorityQueue()
	for color,probability in enumerate(probabilities):
		leaf = Node()
		leaf.data = color
		leaf.prob = probability
		prq.put(leaf)

	while (prq.qsize()>1):
        #Cria o nó
		newnode = Node()
        #Obter as menores probabilidades da folha e remover as duas menores folhas
		l = prq.get()
		r = prq.get()			
        
		newnode.left = l 		
		newnode.right = r
        #Soma dos 2 menores
		newprob = l.prob+r.prob	
		newnode.prob = newprob
        #Novo nó inserido substituindo os outros dois
		prq.put(newnode) 
        
    #Retorna o nó raiz a árvore está completa    
	return prq.get()		

#Percurso da árvore para gerar os códigos
def huffman_traversal(root_node,tmp_array,f):
	bits = ""
	if (root_node.left is not None):
		tmp_array[huffman_traversal.count] = 1
		huffman_traversal.count+=1
		huffman_traversal(root_node.left,tmp_array,f)
		huffman_traversal.count-=1
	if (root_node.right is not None):
		tmp_array[huffman_traversal.count] = 0
		huffman_traversal.count+=1
		huffman_traversal(root_node.right,tmp_array,f)
		huffman_traversal.count-=1
	else:
		huffman_traversal.output_bits[root_node.data] = huffman_traversal.count		#Numero de bits para cada intensidade
		bitstream = ''.join(str(cell) for cell in tmp_array[1:huffman_traversal.count]) 
		color = str(root_node.data)
        #sequência bits 
		bits = bits + bitstream
		wr_str = color+' '+ bitstream+'\n'
		f.write(wr_str)		# escrever a intensidade e o código em um arquivo
		#b.write(bits)
    
	return 

def descompressao(codCompressao, tabela, img):
    imgR = np.zeros((img.shape[0], img.shape[1]))
    listaAux = []
    t = len(codCompressao)
    
    for i in range (0, t):
        aux = codCompressao[i]
        
        for a in tabela:
            if aux == a[1]:
                listaAux.append(a[0])
                break
    
    linha = 0
    coluna = 0            
    for i in listaAux:
        
        if linha == img.shape[0]:
            break
    
        imgR[linha, coluna] = i 
        coluna = coluna + 1
        
        if coluna == img.shape[1]:
            coluna = 0
            linha = linha + 1
            
            
    return imgR

def criaCod(tabela, img):
    codCompleto = []
    cod = ""
    for i in range(img.shape[0]):
        print("i ", i)
        for j in range(img.shape[1]):
            for a in tabela:
                if int(a[0]) == img[i, j]:
                    #print("Ver ")
                    cod = a[1]
                    break
            codCompleto.append(str(cod))
            
    return codCompleto
    
def tabelaTupla(tabela):
    newTabela = []
    for i in range (0, len(tabela), 2):
        newTabela.append((tabela[i], tabela[i+1]))
    
    return newTabela
            
def erros(img1, img2):
    erros = 0
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img1[i, j] != img2[i, j]:
                erros = erros + 1
    
    return erros

    
# Ler imagem 
img = cv2.imread('images/image_2.tif', 0)

#Trecho do código para salvar os resultados(do método de huffman) nos arquivos.
"""# Histograma 
hist = np.bincount(img.ravel(),minlength=256)

# Probabilidades 
probabilities = hist/np.sum(hist)		

#Criar a árvore usando as probs.
root_node = tree(probabilities)			
tmp_array = np.ones([64],dtype=int)
huffman_traversal.output_bits = np.empty(256,dtype=int) 
huffman_traversal.count = 0
f = open('resultados/codesImg3.txt','w')

#Percorrer a árvore e escrever os códigos no arquivo
huffman_traversal(root_node,tmp_array, f)

#Calcular o numero de bits
input_bits = img.shape[0]*img.shape[1]*8
#Compressão 
compression = (1-np.sum(huffman_traversal.output_bits*hist)/input_bits)*100	
#Redundância relativa
r = 1 - (1/compression)"""


tabela = open('resultados/codesImg2.txt', 'r')

tabela = tabela.read()
tabela = tabela.split()
tabela = tabelaTupla(tabela)
tabela.reverse()
codCompleto = criaCod(tabela, img)

"""
print(len(codCompleto))
print('Compressão: ',compression)
print('Redundancia Relativa dos dados: ', r) """

imgDescomprensada = descompressao(codCompleto, tabela, img)
salvar = "resultados/(descomprimida)" + "image_2.png"
cv2.imwrite(salvar, imgDescomprensada)

erro = erros(img, imgDescomprensada)
print("Numero de erros: {}".format(erro))

#plotar imagem
cv2.imshow("imagem", imgDescomprensada)
cv2.waitKey(0)
cv2.destroyAllWindows()

