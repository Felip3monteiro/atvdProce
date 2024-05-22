from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import convolve
import os

def calcular_histograma(imagem):
    histograma = np.zeros((256, 3))
    for canal in range(3):
        for pixel in imagem[:, :, canal].flatten():
            histograma[pixel, canal] += 1
    return histograma

def normalizar_histograma(histograma, num_pixels):
    return histograma / num_pixels

def calcular_cdf(histograma):
    cdf = np.cumsum(histograma, axis=0)
    cdf_normalizado = cdf / cdf[-1, :]
    return cdf_normalizado

def equalizar_histograma(imagem, cdf_normalizado):
    imagem_equalizada = np.zeros_like(imagem)
    for canal in range(3):
        imagem_equalizada[:, :, canal] = np.interp(imagem[:, :, canal].flatten(), range(256), cdf_normalizado[:, canal] * 255).reshape(imagem[:, :, canal].shape)
    return imagem_equalizada.astype(np.uint8)

def remover_canais(imagem, remover_r=False, remover_g=False, remover_b=False):
    imagem_modificada = imagem.copy()
    if remover_r:
        imagem_modificada[:, :, 0] = 0
    if remover_g:
        imagem_modificada[:, :, 1] = 0
    if remover_b:
        imagem_modificada[:, :, 2] = 0
    return imagem_modificada

def aplicar_filtro_blur(imagem, tamanho_kernel=5):
    kernel = np.ones((tamanho_kernel, tamanho_kernel)) / (tamanho_kernel * tamanho_kernel)
    imagem_blur = np.zeros_like(imagem)
    for canal in range(3):
        imagem_blur[:, :, canal] = convolve(imagem[:, :, canal], kernel)
    return imagem_blur

def aplicar_filtro_deteccao_bordas(imagem):
    kernel_sobel = np.array([[-1, -2, -1], 
                             [0, 0, 0], 
                             [1, 2, 1]])
    imagem_bordas = np.zeros_like(imagem)
    for canal in range(3):
        imagem_bordas[:, :, canal] = convolve(imagem[:, :, canal], kernel_sobel)
    return imagem_bordas

def exibir_imagens(*imagens):
    num_imagens = len(imagens)
    plt.figure(figsize=(12, 6))
    for i, (imagem, titulo) in enumerate(imagens):
        plt.subplot(1, num_imagens, i + 1)
        plt.title(titulo)
        plt.imshow(imagem)
    plt.show()

def principal(caminho_imagem):
    imagem = Image.open(caminho_imagem).convert('RGB')
    imagem_np = np.array(imagem)

    while True:
        os.system('cls') or None
        print("+==================+MENU+=====================+")
        print("1. Equalização de Histograma")
        print("2. Remover Cor")
        print("3. Aplicar Filtro Blur")
        print("4. Aplicar Filtro de Detecção de Bordas")
        print("5. Sair")
        print("+=============================================+")
        escolha = input("Digite o número da operação desejada: ")
        os.system('cls') or None
        if escolha == '1':

            print("----------------Equalização de Histograma-------------->")
            histograma = calcular_histograma(imagem_np)
            num_pixels = imagem_np.shape[0] * imagem_np.shape[1]
            histograma_normalizado = normalizar_histograma(histograma, num_pixels)
            cdf_normalizado = calcular_cdf(histograma_normalizado)
            imagem_np = equalizar_histograma(imagem_np, cdf_normalizado)
            exibir_imagens((imagem_np, "Imagem Equalizada"))

        elif escolha == '2':
            print("==============Opçoes de remoção de cor=====================")
            remover_red = input("Remover canal vermelho? (S/N): ").lower() == 's'
            remover_green = input("Remover canal verde? (S/N): ").lower() == 's'
            remover_blue = input("Remover canal azul? (S/N): ").lower() == 's'
            imagem_np = remover_canais(imagem_np, remover_red, remover_green, remover_blue)
            exibir_imagens((imagem_np, "Imagem com Canais Removidos"))
            print("===========================================================")

        elif escolha == '3':
            print("========================Aplicando Blur==========================")
            tamanho_kernel = int(input("Digite o tamanho do kernel: "))
            imagem_np = aplicar_filtro_blur(imagem_np, tamanho_kernel)
            exibir_imagens((imagem_np, "Imagem com Filtro Blur"))
            print("================================================================")
        elif escolha == '4':
            print("========================Detecção de Borda===========================")
            imagem_np = aplicar_filtro_deteccao_bordas(imagem_np)
            exibir_imagens((imagem_np, "Imagem com Filtro de Detecção de Bordas"))
            print("====================================================================")
        elif escolha == '5':
            print("SAINDO !!!")
            break

        else:
            print("Escolha inválida. Tente novamente.")

if __name__ == '__main__':
    principal('wind.jpeg')
