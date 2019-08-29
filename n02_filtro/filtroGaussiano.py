import cv2
import numpy as np
import argparse 

#passagem do filtro
def filtroGaussiano(img):
    imgAux = np.zeros((img.shape[0]+6, img.shape[1]+6))
    hAux = imgAux.shape[0]-3
    wAux = imgAux.shape[1]-3
    imgAux[3:hAux, 3:wAux] = img 
    imgFiltrada = imgAux.copy()
    
    h = imgAux.shape[0] 
    w = imgAux.shape[1]
    
    gaussiano = (1.0/57) * np.array(
        [[0, 1, 2, 1, 0],
        [1, 3, 5, 3, 1],
        [2, 5, 9, 5, 2],
        [1, 3, 5, 3, 1],
        [0, 1, 2, 1, 0]])
    
    for i in range(2, h-2):
        for j in range(2, w-2):
            soma = 0
            for k in range(-2, 3):
                for l in range(-2, 3):
                    v = imgAux.item(i+k, j+l)
                    p = gaussiano[2+k, 2+l]
                    soma = soma + (p * v)
            novoValor = soma
            imgFiltrada.itemset((i, j), novoValor)
        

    imgFiltrada = imgFiltrada[3:hAux, 3:wAux]
    return imgFiltrada

#função responsavel pelo numero de vezes que o filtro passará na imagem
def passagemFiltro(img, n):
    imgAux = img
    for i in range(n):
        imgAux = filtroGaussiano(imgAux)
    
    return imgAux

#Receber a imagem e o numero de repeticoes
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="caminho para a image")
ap.add_argument("-n", "--numRepeticoes", required=True, help= "quantidade de passagem pelo filtro")
args = vars(ap.parse_args())

#abrir imagem
img = cv2.imread(args["image"], 0)
n = int(args["numRepeticoes"])

imgR = passagemFiltro(img, n)

#salvar imagem
salvar = "resultados/(Gaussiano)testeAaa22" + args["image"][7:]
cv2.imwrite(salvar, imgR)

#plotar imagem
cv2.imshow("imagem", imgR)
cv2.waitKey(0)
cv2.destroyAllWindows()
