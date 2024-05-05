import math

class Disco:
    def __init__(self, tamanho_bloco, trilhas, blocos_por_trilha, tempo_seek, tempo_rotacao, tempo_transferencia):
        self.tamanho_bloco = tamanho_bloco
        self.trilhas = trilhas
        self.blocos_por_trilha = blocos_por_trilha
        self.tempo_seek = tempo_seek
        self.tempo_rotacao = tempo_rotacao
        self.tempo_transferencia = tempo_transferencia
        self.fat = [{"livre": True, "prox_bloco": -1} for _ in range(trilhas * blocos_por_trilha)] # Inicializando a FAT com cada entrada representando um bloco livre e apontando para -1

    def encontrar_bloco_livre(self):
        # Encontra o primeiro bloco livre que possa acomodar o tamanho do arquivo
        bloco_livre = -1
        for i, bloco in enumerate(self.fat):
            if bloco["livre"]:  # Verifica se o bloco está livre
                bloco_livre = i
                break
        return bloco_livre
    
    def alocar_arquivo(self, tamanho_arquivo):
         #Aloca um arquivo na FAT usando o método First Fit
        bloco_inicial = self.encontrar_bloco_livre()
        if bloco_inicial != -1:
            tamanho_restante = tamanho_arquivo
            bloco_atual = bloco_inicial
            blocos_alocados = []
            estado_inicial = [bloco["livre"] for bloco in self.fat]
            while tamanho_restante > 0 and bloco_atual < len(self.fat):
                if self.fat[bloco_atual]["livre"]:
                    tamanho_bloco_disponivel = self.tamanho_bloco
                    tamanho_a_alocar = min(tamanho_restante, tamanho_bloco_disponivel)
                    self.fat[bloco_atual]["livre"] = False
                    tamanho_restante -= tamanho_a_alocar
                    blocos_alocados.append(bloco_atual)
                bloco_atual += 1
            
            if len(blocos_alocados) > 1:
                for i in range(len(blocos_alocados) - 1):
                    self.fat[blocos_alocados[i]]["prox_bloco"] = blocos_alocados[i + 1]

            # Verifica se o arquivo foi alocado completamente
            if tamanho_restante == 0:
                return blocos_alocados
            else:
            # Se não houver espaço suficiente na FAT para alocar o arquivo
            # marca os blocos anteriores como livres novamente
                for i in range(bloco_inicial, bloco_atual):
                    self.fat[i]["livre"] = estado_inicial[i]
                return print("Há bloco livre na FAT, mas não o suficiente para alocar o arquivo.")
        else:
            return print("Todos os blocos da FAT estão ocupados. Não há espaço suficiente na FAT para alocar o arquivo.")
        
    def remover_arquivo(self, bloco_inicial):
        bloco_atual = bloco_inicial
        while bloco_atual != -1:
            # Configura o próximo bloco do bloco atual para -1
            proximo_bloco = self.fat[bloco_atual]["prox_bloco"]
            self.fat[bloco_atual]["prox_bloco"] = -1
            # Libera o bloco atual, marcando-o como livre na FAT
            self.fat[bloco_atual]["livre"] = True
            # Atualiza o bloco atual para o próximo bloco
            bloco_atual = proximo_bloco
            
        return print("Arquivo salvo no bloco inicial", bloco_inicial, "removido.")

def main():
    # Configuração do disco
    tamanho_bloco = 512 #bytes
    trilhas = 5
    blocos_por_trilha = 10
    tempo_seek = 5 #milisegundos
    tempo_rotacao = 10 
    tempo_transferencia = 2

    # Criar instância do disco
    disco = Disco(tamanho_bloco, trilhas, blocos_por_trilha, tempo_seek, tempo_rotacao, tempo_transferencia)

    print("===== Estado Inicial da FAT =====")
    for indice, bloco in enumerate(disco.fat):
            print(f'Bloco {indice}: {bloco}')

    print("----- Cenário 1 -----")
    print("Alocando arquivo exatamente do tamanho de um bloco.",
          "\nTamanho do bloco:", tamanho_bloco, "Bytes",
          "\nTamanho do arquivo:", 512, "Bytes")
    bloco_alocado0 = disco.alocar_arquivo(512)
    print("Bloco", bloco_alocado0, "alocado.") # Bloco 0 alocado

    print("----- Cenário 2 -----")
    print("Alocando 2 arquivos exatamente do tamanho de um bloco.",
          "\nTamanho do bloco:", tamanho_bloco, "Bytes",
          "\nTamanho do arquivo 1:", 512, "Bytes",
          "\nTamanho do arquivo 2:", 512, "Bytes")
    bloco_alocado1 = disco.alocar_arquivo(512)
    bloco_alocado2 = disco.alocar_arquivo(512)
    print("Bloco", bloco_alocado1, "alocado") # Bloco 1 alocado
    print("Bloco", bloco_alocado2, "alocado") # Bloco 2 alocado

    print("----- Cenário 3 -----")
    print("Alocando arquivo menor do que o tamanho de um bloco.",
          "\nTamanho do bloco:", tamanho_bloco, "Bytes",
          "\nTamanho do arquivo:", 100, "Bytes")
    bloco_alocado3 = disco.alocar_arquivo(100)
    print("Bloco", bloco_alocado3, "alocado") # Bloco 3 alocado
    desperdicio = tamanho_bloco - 100
    print("Desperdício de", desperdicio, "Bytes")

    print("----- Cenário 4 -----")
    print("Alocando arquivo maior do que o tamanho de um bloco.",
          "\nTamanho do bloco:", tamanho_bloco, "Bytes",
          "\nTamanho do arquivo:", 513, "Bytes")
    blocos_alocados = disco.alocar_arquivo(513)
    print("Blocos", blocos_alocados, "alocados") # Blocos 4 e 5 serão alocados
    print("Desperdício de", 513 - tamanho_bloco, "Bytes")

    print("----- Cenário 4.1 -----")
    print("Alocando arquivo maior do que o tamanho de um bloco, nesse caso, o ocupará todos os blocos livres restantes",
          "\nTamanho do bloco:", tamanho_bloco, "Bytes",
          "\nTamanho do arquivo:", 512 * 44, "Bytes")
    blocos_alocados1 = disco.alocar_arquivo(512 * 44)
    print("Blocos", blocos_alocados1, "alocados")

    print("----- Cenário 5 -----")
    print("Alocando arquivo do mesmo tamanho de um bloco, mas todos os blocos estão ocupados",
          "\nTamanho do bloco:", tamanho_bloco, "Bytes",
          "\nTamanho do arquivo:", 512, "Bytes")
    espaco_insuficiente = disco.alocar_arquivo(512)
    print(espaco_insuficiente)

    print("----- Cenário 5.1 -----")
    print("Alocando arquivo de tamanho qualquer em um cenário em que não há blocos livres.",
          "\nTamanho do bloco:", tamanho_bloco, "Bytes",
          "\nTamanho do arquivo:", 328, "Bytes")
    print(disco.alocar_arquivo(328))

    print("----- Cenário 6 -----")
    print("Removendo arquivo do mesmo tamanho de um bloco",
          "\nTamanho do bloco:", tamanho_bloco, "Bytes",
          "\nTamanho do arquivo:", 512, "Bytes")
    print(disco.remover_arquivo(0))

    print("----- Cenário 7 -----")
    print("Removendo arquivo de tamanho maior que um bloco",
          "\nTamanho do bloco:", tamanho_bloco, "Bytes",
          "\nTamanho do arquivo:", 513, "Bytes")
    print(disco.remover_arquivo(4))

    print("===== Estado Final da FAT após Cenário 7 =====")
    for indice, bloco in enumerate(disco.fat):
            print(f'Bloco {indice}: {bloco}')

    print("----- Cenário 8 -----")
    print("Alocando arquivo de tamanho 4 vezes maior que um bloco (precisará de 4 blocos, porém só 3 estão livres)",
          "\nTamanho do bloco:", tamanho_bloco, "Bytes",
          "\nTamanho do arquivo:", 512 * 4, "Bytes")
    print(disco.alocar_arquivo(512 * 4))

    print("===== Estado Final da FAT após Cenário 8 =====")
    for indice, bloco in enumerate(disco.fat):
            print(f'Bloco {indice}: {bloco}')

    print("----- Cenário 9 -----")
    print("Alocando arquivo de tamanho 3 vezes maior que um bloco (precisará de 3 blocos e deve ser alocado nos 3 blocos disponíveis)",
          "\nTamanho do bloco:", tamanho_bloco, "Bytes",
          "\nTamanho do arquivo:", 512 * 3, "Bytes")
    print("Blocos", disco.alocar_arquivo(512 * 3), "alocados")

    print("----- Cenário 10 -----")
    print("Removendo arquivo de tamanho menor que um bloco",
          "\nTamanho do bloco:", tamanho_bloco, "Bytes",
          "\nTamanho do arquivo:", 100, "Bytes")
    print(disco.remover_arquivo(3))

    print("----- Cenário 11 -----")
    print("Removendo arquivo de tamanho 44 vezes maior que um bloco (remoção de arquivo que consome mais da metade dos blocos)",
          "\nTamanho do bloco:", tamanho_bloco, "Bytes",
          "\nTamanho do arquivo:", 512 * 44, "Bytes")
    print(disco.remover_arquivo(6))

    print("===== Estado Final da FAT =====")
    for indice, bloco in enumerate(disco.fat):
            print(f'Bloco {indice}: {bloco}')

if __name__ == "__main__":
    main()