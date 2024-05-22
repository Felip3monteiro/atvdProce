from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

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

def principal(caminho_imagem):
    imagem = Image.open(caminho_imagem).convert('RGB')
    imagem_np = np.array(imagem)
    
    histograma = calcular_histograma(imagem_np)
    
    num_pixels = imagem_np.shape[0] * imagem_np.shape[1]
    histograma_normalizado = normalizar_histograma(histograma, num_pixels)
    
    cdf_normalizado = calcular_cdf(histograma_normalizado)
    
    imagem_equalizada_np = equalizar_histograma(imagem_np, cdf_normalizado)
    
    imagem_equalizada = Image.fromarray(imagem_equalizada_np)
    imagem_equalizada.save('imagem_equalizada.png')
    

    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.title('Imagem Original')
    plt.imshow(imagem_np)
    plt.subplot(1, 2, 2)
    plt.title('Imagem Equalizada')
    plt.imshow(imagem_equalizada_np)
    plt.show()

if __name__ == '__main__':
    principal('wind.jpeg')
