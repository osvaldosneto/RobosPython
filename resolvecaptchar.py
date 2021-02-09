from collections import Counter
from pprint import pprint
from string import ascii_letters, digits
from PIL import Image
from pytesseract import image_to_string

class resolveCaptchar:

    def obter_caracteres(self, imagem):
        caracteres = [list() for _ in range(6)]
        resultados = self.tentar_layouts(imagem)
        for posicao in range(6):
            for resultado in resultados:
                for indice, caractere in enumerate(caracteres):
                    try:
                        caractere.append(resultado[indice])
                    except IndexError:
                        pass
        return caracteres


    def tentar_layouts(self, imagem):
        resultados = []
        layouts = [7, 8, 9, 10, 11, 13]
        for layout in layouts:
            resultados.append(self.reconhecer_caracteres(imagem, layout))
        return resultados


    def reconhecer_caracteres(imagem, layout):
        return image_to_string(
            imagem,
            config=
            f"""--psm {layout} 
            -c tessedit_char_whitelist={ascii_letters + digits}""")


    def remover_ruidos(imagem):
        limite = 1
        largura, altura = imagem.size
        pixels = imagem.load()

        for linha in range(altura):
            for coluna in range(largura):
                if pixels[coluna, linha] > 128:
                    continue
                escuros = 0
                for pixel in range(coluna, largura):
                    if pixels[pixel, linha] < 128:
                        escuros += 1
                    else:
                        break
                if escuros <= limite:
                    for pixel in range(escuros):
                        pixels[coluna + pixel, linha] = 255
                coluna += escuros

        for coluna in range(largura):
            for linha in range(altura):
                if pixels[coluna, linha] > 128:
                    continue
                escuros = 0
                for pixel in range(linha, altura):
                    if pixels[coluna, pixel] < 128:
                        escuros += 1
                    else:
                        break
                if escuros <= limite:
                    for pixel in range(escuros):
                        pixels[coluna, linha + pixel] = 255
                linha += escuros

        return imagem


    def contar_caracteres(listas):
        for lista in listas:
            mais_comuns = [list() for _ in range(len(listas))]
            for indice, _ in enumerate(mais_comuns):
                try:
                    mais_comuns[indice] = Counter(listas[indice]).most_common()[0][0]
                except IndexError:
                    pass
        return mais_comuns