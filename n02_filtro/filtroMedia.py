import cv2
import numpy as np
import argparse 

#passagem do filtro
def filtroMedia(img, filtro):
    imgAux = np.zeros((img.shape[0]+6, img.shape[1]+6))
    hAux = imgAux.shape[0]-3
    wAux = imgAux.shape[1]-3
    imgAux[3:hAux, 3:wAux] = img 
    imgFiltrada = imgAux.copy()
    
    h = imgAux.shape[0] 
    w = imgAux.shape[1]
    tamanhoFiltro = filtro-3
    
    for i in range(3, h-3):
        for j in range(3, w-3):
            vizinhos = []
            for k in range(-3, tamanhoFiltro):
                for l in range(-3, tamanhoFiltro):
                    v = imgAux.item(i+k, j+l)
                    vizinhos.append(v)
            vizinhosSoma = sum(vizinhos)
            media = vizinhosSoma/len(vizinhos)
            imgFiltrada.itemset((i, j), media)
        

    imgFiltrada = imgFiltrada[3:hAux, 3:wAux]
    return imgFiltrada

#função responsavel pelo numero de vezes que o filtro passará na imagem
def passagemFiltro(img, filtro, n):
    imgAux = img
    for i in range(n):
        imgAux = filtroMedia(imgAux, filtro)
    
    return imgAux

#Receber a imagem, tamanho do filtro e o numero de repeticoes
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="caminho para a image")
ap.add_argument("-f", "--filtro", required=True, help= "tamanho do filtro")
ap.add_argument("-n", "--numRepeticoes", required=True, help= "quantidade de passagem pelo filtro")
args = vars(ap.parse_args())

#abrir imagem
img = cv2.imread(args["image"], 0)
filtro = int(args["filtro"])
n = int(args["numRepeticoes"])

imgR = passagemFiltro(img, filtro, n)

#salvar imagem
salvar = "resultados/(" + str(filtro) + "-Media)" + args["image"][7:]
cv2.imwrite(salvar, imgR)

#plotar imagem
cv2.imshow("imagem", imgR)
cv2.waitKey(0)
cv2.destroyAllWindows()
