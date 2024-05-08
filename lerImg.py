import openpyxl
from PIL import Image

def imagem_para_matriz(imagem):
    largura, altura = imagem.size

    # Criar uma matriz para armazenar os dados dos pixels
    matriz_pixels = []

    # Loop pelos pixels da imagem e adicionar na matriz
    for y in range(altura):
        linha = []
        for x in range(largura):
            pixel = imagem.getpixel((x, y))
            linha.append(pixel)
        matriz_pixels.append(linha)

    return matriz_pixels

def matriz_para_excel(matriz, nome_arquivo):
    wb = openpyxl.Workbook()
    ws = wb.active
    
    # Adicionar os valores da matriz no Excel
    for linha in matriz:
        linha_str = [str(valor[0]) + "," + str(valor[1]) + "," + str(valor[2]) if isinstance(valor, tuple) else str(valor) for valor in linha]
        ws.append(linha_str)
    
    # Salvar o arquivo no Excel
    wb.save(nome_arquivo + ".xlsx")
    print("Arquivo Excel criado com sucesso!")

def alterar_cor_pixels(imagem, cor_original, nova_cor):
    imagem_editada = imagem.copy()
    
    # Pega o tamanho da imagem
    largura, altura = imagem_editada.size
    
    # Loop dp pixels da imagem
    for y in range(altura):
        for x in range(largura):
            cor_pixel = imagem_editada.getpixel((x, y))
            if cor_pixel == cor_original:
                imagem_editada.putpixel((x, y), nova_cor)
    
    return imagem_editada

# Exemplo de uso:
imagem_original = Image.open("cachorro pançudo.jpg")
cor_original = (0, 0, 0)  # Coloque uma cor que aparece na imagem
nova_cor = (0, 0, 255) # azul
imagem_editada = alterar_cor_pixels(imagem_original, cor_original, nova_cor)
imagem_editada.show()  # Mostra a imagem com novas cores

# Testa o código
'''
imagem = Image.open("cachorro pançudo.jpg")
matriz_pixels = imagem_para_matriz(imagem)
matriz_para_excel(matriz_pixels, "saida_pixels")
'''
