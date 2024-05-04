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
        bloco_inicial = self.encontrar_bloco_livre() #2
        if bloco_inicial != -1:
            tamanho_restante = tamanho_arquivo #513
            bloco_atual = bloco_inicial #2
            blocos_alocados = []
            while tamanho_restante > 0 and bloco_atual < len(self.fat):
                if self.fat[bloco_atual]["livre"]:
                    tamanho_bloco_disponivel = self.tamanho_bloco #512
                    tamanho_a_alocar = min(tamanho_restante, tamanho_bloco_disponivel) #1
                    self.fat[bloco_atual]["livre"] = False
                    tamanho_restante -= tamanho_a_alocar #0
                    blocos_alocados.append(bloco_atual)
                bloco_atual += 1 #4
            
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
                return -2
        else:
            return -3 # Não há espaço suficiente na FAT para alocar o arquivo

    def ler_bloco(self, bloco):
        # Lógica para simular leitura de um bloco
        # Calcular a latência de acesso usando os tempos de seek, rotação e transferência
        latencia = self.tempo_seek + self.tempo_rotacao + self.tempo_transferencia
        return latencia

    def escrever_bloco(self, bloco, dados):
        # Lógica para simular escrita em um bloco
        # Calcular a latência de acesso usando os tempos de seek, rotação e transferência
        latencia = self.tempo_seek + self.tempo_rotacao + self.tempo_transferencia
        return latencia

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

    #Alocando arquivo exatamente do tamanho de um bloco.
    bloco_inicial = disco.alocar_arquivo(512)
    bloco_inical2 = disco.alocar_arquivo(512)
    bloco_inical3 = disco.alocar_arquivo(513)
    print(bloco_inicial)
    print(bloco_inical2)
    print(bloco_inical3)
    print(disco.fat[0])
    print(disco.fat[1])
    print(disco.fat[2])
    print(disco.fat[3])

    
    # Lista de blocos de dados para acessar
    #blocos = [10, 20, 30, 40, 50]

    # Simular leitura de blocos
    #for bloco in blocos:
        #latencia = disco.ler_bloco(bloco)
        #print(f"Latência de acesso para o bloco {bloco}: {latencia} ms")

if __name__ == "__main__":
    main()