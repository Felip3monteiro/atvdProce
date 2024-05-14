from PIL import Image
import openpyxl
from collections import Counter

def imagem_para_matriz(imagem):
    largura, altura = imagem.size
    matriz_pixels = []

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

    for linha in matriz:
        linha_str = [str(valor[0]) + "," + str(valor[1]) + "," + str(valor[2]) if isinstance(valor, tuple) else str(valor) for valor in linha]
        ws.append(linha_str)

    wb.save(nome_arquivo + ".xlsx")
    print("Arquivo Excel criado com sucesso!")

def destacar_cores_por_frequencia(imagem):
    # Converter a imagem para tons de cinza
    imagem_cinza = imagem.convert('L')
    largura, altura = imagem_cinza.size
    pixels = []

    for y in range(altura):
        for x in range(largura):
            pixel = imagem_cinza.getpixel((x, y))
            pixels.append(pixel)

    # Contar a frequência de cada tom de cinza
    contador = Counter(pixels)
    total_pixels = largura * altura

    # Ordenar tons de cinza por frequência
    tons_ordenados = sorted(contador.items(), key=lambda item: item[1])

    # Calcular a porcentagem acumulada
    porcentagem_acumulada = 0
    mapa_tons = {}
    for tom, freq in tons_ordenados:
        porcentagem = (freq / total_pixels) * 100
        porcentagem_acumulada += porcentagem
        mapa_tons[tom] = porcentagem_acumulada

    # Normalizar e acumular os valores
    normalizado_acumulado = {}
    valor_acumulado = 0
    for tom, porcentagem_acumulada in mapa_tons.items():
        valor_normalizado = porcentagem_acumulada / 100 * 255
        valor_acumulado += valor_normalizado
        normalizado_acumulado[tom] = min(255, valor_acumulado)

    # Criar uma nova imagem com os tons destacados
    imagem_editada = imagem_cinza.copy()
    for y in range(altura):
        for x in range(largura):
            tom_pixel = imagem_cinza.getpixel((x, y))
            intensidade = int(normalizado_acumulado[tom_pixel])
            imagem_editada.putpixel((x, y), intensidade)

    return imagem_editada

# Exemplo de uso:
imagem_original = Image.open("cachorro pançudo.jpg")
imagem_editada = destacar_cores_por_frequencia(imagem_original)
imagem_editada.show()  # Mostra a imagem com os tons destacados

# Testa o código de conversão e exportação
'''
imagem = Image.open("cachorro pançudo.jpg")
matriz_pixels = imagem_para_matriz(imagem)
matriz_para_excel(matriz_pixels, "saida_pixels")
'''
