import numpy as np
import PIL.Image as pil
import cv2

#Direções do vertices (se é convexo ou concâvo)
def label_vertices(chain_code, points):
    dic_vertices = {"01":'P',
                    "03":'B',
                    "10":'B',
                    "12":'P',
                    "21":'B',
                    "23":'P',
                    "30":'P',
                    "32":'B'}
    
    vertices = []
    vertices.append((points[0], 'B'))
    for i in range(len(chain_code)-1):
        code = chain_code[i:i+2]
        try:
            tipoVertice = dic_vertices[code]
            ponto = points[i+1]
            
            if tipoVertice == 'P':
                if code == "01":
                    ponto = (ponto[0]-1, ponto[1]-1)
                elif code == "12":
                    ponto = (ponto[0]+1, ponto[1]-1)
                elif code == "23":
                    ponto = (ponto[0]+1, ponto[1]+1)
                else: #code == "30"
                    ponto = (ponto[0]-1, ponto[1]+1)
            
            vertices.append((ponto, tipoVertice))
        except:
            pass
    
    return vertices            

# Determinante para o achar o ponto mpp
def sinal(p1, p2, p3):
    p1 = p1[0]
    p2 = p2[0]
    p3 = p3[0]
    matriz = np.array([[p1[0], p1[1], 1],
                       [p2[0], p2[1], 1],
                       [p3[0], p3[1], 1]])
    
    return np.linalg.det(matriz)
    

#Algortimo
def mpp(vertices):
    vertices_mpp = []
    v0 = vertices[0]
    Br = Pr =  v0
    
    vertices_mpp.append(v0)
    
    for i in range(1, len(vertices)):
        Vk = vertices[i]
        Vl = vertices_mpp[-1]
        
        if sinal(Vl, Br, Vk) > 0:
            vertices_mpp.append(Br)
            Pr = Br
        elif sinal(Vl, Pr, Vk) >= 0:
            if Vk[1] == 'B':
                Br = Vk
            else:
                Pr = Vk
        else: #sinal(Vl, Pr, Vk) < 0:
            vertices_mpp.append(Pr)
            Br = Pr
    
    
    Vk = vertices[0]
    Vl = vertices_mpp[-1]
    
    if sinal(Vl, Br, Vk) > 0:
        vertices_mpp.append(Br)
    elif sinal(Vl, Pr, Vk) < 0:
        vertices_mpp.append(Pr)
    
    return vertices_mpp

def distanciaPonto(i, j):
    return ((i[0] - j[0])**2 + (i[1] - j[1])**2)**0.5

#Fazer a linha de um ponto mpp para outro mpp
def encontrarPontoProximo(p1, p2):
    (y, x) = p1
    pontos = [(y-1,x-1), (y-1, x), (y-1, x+1), 
              (y, x-1), p1, (y, x+1),
              (y+1, x-1), (y+1, x),(y+1, x+1)]
    
    nextP = p1
    distanciaMinima = float('inf')
    for p in pontos:
        current_distance = distanciaPonto(p, p2)
        if current_distance < distanciaMinima:
            distanciaMinima = current_distance
            nextP = p
    
    return nextP

def desenharPoligono(vertices_mpp, imageShape):
    imagemPreenchida = np.zeros(imageShape)
    
    for i in range(len(vertices_mpp)-1):
        ponto1 = vertices_mpp[i][0]
        ponto2 = vertices_mpp[i+1][0]
        
        imagemPreenchida[ponto1] = 255
        while ponto1 != ponto2:
            ponto1 = encontrarPontoProximo(ponto1, ponto2)
            imagemPreenchida[ponto1] = 255
        
    
    ponto1 = vertices_mpp[-1][0]
    ponto2 = vertices_mpp[0][0]
    
    imagemPreenchida[ponto1] = 255
    while ponto1 != ponto2:
        ponto1 = encontrarPontoProximo(ponto1, ponto2)
        imagemPreenchida[ponto1] = 255
    
    return imagemPreenchida


def findBC(img, b, c):
    caminho = {(b[0]-1,b[1]-1):(b[0]-1,b[1]),
               (b[0]-1,b[1]):(b[0]-1,b[1]+1),
               (b[0]-1,b[1]+1):(b[0],b[1]+1),
               (b[0],b[1]+1):(b[0]+1,b[1]+1),
               (b[0]+1,b[1]+1):(b[0]+1,b[1]),
               (b[0]+1,b[1]):(b[0]+1,b[1]-1),
               (b[0]+1,b[1]-1):(b[0],b[1]-1),
               (b[0],b[1]-1):(b[0]-1,b[1]-1)}
    
    coordAtual = c
    for temp in range(8):
        coord = caminho[coordAtual]
        if img[coord[0], coord[1]] == 1:
            return coord, coordAtual
        coordAtual = coord
        
def firstPoint(img):
    for i in range (img.shape[0]):
        for j in range (img.shape[1]):
            if img[i, j] == 1:
                return (i, j)

def seguidorContorno(img):
    imgR = np.zeros((img.shape[0], img.shape[1]), 'uint8')
    img = img/255
    
    partida = firstPoint(img)
    c0 = (partida[0], partida[1]-1)
    
    b = partida
    c = c0
    
    coordList = []
    
    while(True):
        coordList.append(b)
        imgR[b[0], b[1]] = 1
        b, c = findBC(img, b, c)
        
        if b in coordList:
            break
    
    return imgR, coordList

def create_grid(img_shape, steps):
    newImg = np.zeros(img_shape)
    coord_list_grid = []
    for i in range(0, img_shape[0], steps):
        for j in range(0, img_shape[1], steps):
            coord_list_grid.append((i, j))
            newImg[i, j] = 1
    return newImg, coord_list_grid

def resample(border_img, coord_list, min_dist, grid_steps):
    grid, coord_grid = create_grid(border_img.shape, grid_steps)
    resample_list = []
    newImg = np.zeros(border_img.shape)
    
    for p1 in coord_grid:
        for p2 in coord_list:
            if distanciaPonto(p1, p2) < min_dist:
                if p1 not in resample_list:
                    resample_list.append(p1)
                    newImg[p1[0], p1[1]] = 1
    
    return newImg, resample_list, grid

def get8chainDirection(a, b):
    direcoes = {(-1,-1) :"3",
                (-1,0)  :"2",
                (-1,1)  :"1",
                (0,1)   :"0",
                (1,1)   :"7",
                (1,0)   :"6",
                (1,-1)  :"5",
                (0,-1)  :"4"}
    
    d = (b[0]-a[0], b[1]-a[1])
    return direcoes[d]

def isDiagonal(a, b):
    direcoes = {(-1,-1) :True,
                (-1,0)  :False,
                (-1,1)  :True,
                (0,1)   :False,
                (1,1)   :True,
                (1,0)   :False,
                (1,-1)  :True,
                (0,-1)  :False}
    d = (b[0]-a[0], b[1]-a[1])
    return direcoes[d]

def get4chainDirection(a, b):
    direcoes = {(-1,-1) :"_",
                (-1,0)  :"1",
                (-1,1)  :"_",
                (0,1)   :"0",
                (1,1)   :"_",
                (1,0)   :"3",
                (1,-1)  :"_",
                (0,-1)  :"2"}
    
    d = (b[0]-a[0], b[1]-a[1])
    return direcoes[d]

def isSameDirection(dir1, dir2):
    return abs(int(dir1)-int(dir2)) == 2

def addChainCode(code, newDir, newPoint, pointList):
    if len(code) == 0:
        code += newDir
        pointList.append(newPoint)
    elif isSameDirection(code[-1], newDir):
        code = code[:-1]
        pointList = pointList[:-1]
    else:
        code += newDir
        pointList.append(newPoint)
    
    return code, pointList
    

def chain_code(resample_list, grid_value, chain_type):
    
    assert chain_type == 4 or chain_type == 8
    
    chain_code = ""
    
    resample_list_normalized = []
    for p in resample_list:
        p = (p[0]/grid_value, p[1]/grid_value)
        resample_list_normalized.append(p)
    
    m = 0
    n = 0
    resample_list_normalized = np.array(resample_list_normalized).astype(np.uint16)
    for p in resample_list_normalized:
        if(p[0] > m):
            m = p[0]
        if(p[1] > n):
            n = p[1]
    
    m = int(m)
    n = int(n)
    chainCodeMatrix = np.zeros((m+2,n+2))

    for p in resample_list_normalized:
        chainCodeMatrix[p[0], p[1]] = 1
        
    pil.fromarray(chainCodeMatrix.astype(np.uint8)*255).convert("L").save("resultados/chainCodeMatrixG15.png")
    

    b0 = firstPoint(chainCodeMatrix)
    c0 = (b0[0], b0[1] - 1)
    
    b = b0 # no inicio sao iguais
    c = c0
    
    coord_list = []
    coord_list.append(b)
    while(True):
        new_b, c = findBC(chainCodeMatrix, b, c)
        if chain_type == 8:
            chain_code += get8chainDirection(b, new_b)
            coord_list.append(b)
        else:
            if isDiagonal(b, new_b):
                fisrt_code = get4chainDirection(b, c)
                second_code = get4chainDirection(c, new_b)
                chain_code, coord_list = addChainCode(chain_code, fisrt_code, c, coord_list)
                chain_code, coord_list = addChainCode(chain_code, second_code, new_b, coord_list)
            else:
                direcao = get4chainDirection(b, new_b)
                chain_code, coord_list = addChainCode(chain_code, direcao, new_b, coord_list)
        
        b = new_b
        if b in coord_list:
            new_b, new_c = findBC(chainCodeMatrix, b, c)
            if new_b in coord_list:
                break
            
    return chain_code, coord_list, chainCodeMatrix

if __name__ == "__main__":
    grid_value = 15
    min_dist = 9
    run_all = True
    
    if run_all:
        img2 = cv2.imread('images/image_2.png', 0)
        img2 = img2 / np.max(img2)
        img2 = np.logical_not(img2)*255
        pil.fromarray(img2.astype(np.uint8)).convert("L").save("resultados/notImage2G15.png")
        notImage2 = cv2.imread('resultados/notImage2G15.png', 0)
        
        borderImg, coordList = seguidorContorno(notImage2)
        resample_img, resample_list, grid = resample(borderImg, coordList, min_dist, grid_value)
            
        gridOrBorder = np.logical_or(grid, borderImg)*255
        pil.fromarray(gridOrBorder.astype(np.uint8)).convert("L").save("resultados/gridOrBorderImgG15.png")
        
        x = grid + borderImg + resample_img
        x = (x/np.max(x))*255
        pil.fromarray(x.astype(np.uint8)).convert("L").save("resultados/xG15.png")
        
        pil.fromarray(resample_img*255).convert("L").save("resultados/resampleBorderImgG15.png")
        pil.fromarray(grid*255).convert("L").save("resultados/gridG15.png")
    else:
        resample_img = cv2.imread('resultados/resampleBorderImgG15.png', 0)/255
        resample_list = np.where(resample_img == 1)
        resample_list = list(zip(resample_list[0], resample_list[1]))
    
    chain_code4, points_c_code_4, chainCodeMatrix_4 = chain_code(resample_list, grid_value, chain_type=4)
    
    for i in range(len(points_c_code_4)):
        points_c_code_4[i] = (points_c_code_4[i][0]*grid_value, points_c_code_4[i][1]*grid_value)
        
    pontos_rotulados = label_vertices(chain_code4, points_c_code_4)
    
    
    vertices_mpp = mpp(pontos_rotulados)
    
    img_vertices_mpp = np.zeros((542, 636))
    for p in vertices_mpp:
        img_vertices_mpp[p[0]] = 255
    
    pil.fromarray(img_vertices_mpp).convert("L").save("resultados/vertices_mppG15.png")
    
    imagem_completa = desenharPoligono(vertices_mpp, (542, 636))
    pil.fromarray(imagem_completa).convert("L").save("resultados/poligono_mppG15.png")
    
