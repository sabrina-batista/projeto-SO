import simpy
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
                    self.fat[i]["livre"] = True
                return print("Há bloco livre na FAT, mas não o suficiente na FAT para alocar o arquivo. Todos os blocos são livres novamente.")
        else:
            return print("Todos os blocos da FAT estão ocupados. Não há espaço suficiente na FAT para alocar o arquivo")
        
    def remover_arquivo(self, bloco_inicial):
        bloco_atual = bloco_inicial
        while bloco_atual != -1:
            # Libera o bloco atual, marcando-o como livre na FAT
            self.fat[bloco_atual]["livre"] = True
            # Obtém o índice do próximo bloco no arquivo
            proximo_bloco = self.fat[bloco_atual]["prox_bloco"]
            # Atualiza o bloco atual para o próximo bloco
            bloco_atual = proximo_bloco

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
    bloco_alocadoErro = disco.alocar_arquivo(512)
    print(bloco_alocadoErro)

    print("===== Estado Final da FAT =====")
    for indice, bloco in enumerate(disco.fat):
            print(f'Bloco {indice}: {bloco}')