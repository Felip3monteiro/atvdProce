import openpyxl
from PIL import Image

def imagem_para_matriz(imagem):
    # Converte a imagem para escala de cinza (para simplificar, se necessário)
    imagem_cinza = imagem.convert("L")
    
    # Obtém as dimensões da imagem
    largura, altura = imagem_cinza.size
    
    # Cria uma matriz para armazenar os dados dos pixels
    matriz_pixels = []
    
    # Loop pelos pixels da imagem e os adiciona à matriz
    for y in range(altura):
        linha = []
        for x in range(largura):
            # Obtém o valor do pixel na posição (x, y)
            pixel = imagem_cinza.getpixel((x, y))
            linha.append(pixel)
        matriz_pixels.append(linha)
    
    return matriz_pixels

def matriz_para_excel(matriz, nome_arquivo):
    # Cria um novo workbook do Excel
    wb = openpyxl.Workbook()
    ws = wb.active
    
    # Adiciona os valores da matriz ao Excel
    for linha in matriz:
        ws.append(linha)
    
    # Salva o arquivo Excel
    wb.save(nome_arquivo + ".xlsx")
    print("Arquivo Excel criado com sucesso!")

# Carrega a imagem
imagem = Image.open("cachorro pançudo.jpg")

# Converte a imagem em uma matriz
matriz_pixels = imagem_para_matriz(imagem)

# Salva a matriz em um arquivo Excel
matriz_para_excel(matriz_pixels, "saida_pixels")