class Disco:
    def __init__(self, tamanho_bloco, trilhas, blocos_por_trilha, tempo_seek, tempo_rotacao, tempo_transferencia):
        """
        Inicializa o disco com os parâmetros especificados.

        Args:
        tamanho_bloco (int): Tamanho de cada bloco em bytes.
        trilhas (int): Número de trilhas no disco.
        blocos_por_trilha (int): Número de blocos por trilha.
        tempo_seek (float): Tempo médio de busca (em ms).
        tempo_rotacao (float): Tempo médio de rotação (em ms).
        tempo_transferencia (float): Tempo médio de transferência (em ms).
        """
        self.tamanho_bloco = tamanho_bloco
        self.trilhas = trilhas
        self.blocos_por_trilha = blocos_por_trilha
        self.tempo_seek = tempo_seek
        self.tempo_rotacao = tempo_rotacao
        self.tempo_transferencia = tempo_transferencia
        self.fat = [{"livre": True, "prox_bloco": -1} for _ in range(trilhas * blocos_por_trilha)] # Inicializando a FAT com cada entrada representando um bloco livre e apontando para -1

    def encontrar_bloco_livre(self):
        """
        Encontra o primeiro bloco livre na FAT.

        Returns:
        int: Índice do primeiro bloco livre encontrado. Retorna -1 se não houver blocos livres.
        """
        bloco_livre = -1
        for i, bloco in enumerate(self.fat):
            if bloco["livre"]: 
                bloco_livre = i
                break
        return bloco_livre
    
    def alocar_arquivo(self, tamanho_arquivo):
        """
        Aloca um arquivo na FAT usando o método First Fit.

        Args:
        tamanho_arquivo (int): Tamanho do arquivo em bytes.

        Returns:
        list: Lista de índices dos blocos alocados para o arquivo.
        
        Raises:
        ValueError: Se não houver espaço suficiente na FAT para alocar o arquivo.
        """
        bloco_inicial = self.encontrar_bloco_livre()
        
        if bloco_inicial == -1:
             raise ValueError("Todos os blocos da FAT estão ocupados. Não há espaço suficiente na FAT para alocar o arquivo.")
        
        tamanho_restante = tamanho_arquivo
        bloco_atual = bloco_inicial
        blocos_alocados = []
        estado_inicial = [{"livre": bloco["livre"], "prox_bloco": bloco["prox_bloco"]} for bloco in self.fat]
        
        while tamanho_restante > 0 and bloco_atual < len(self.fat):
            bloco_atual, tamanho_restante, blocos_alocados = self._alocar_bloco(bloco_atual, tamanho_restante, blocos_alocados)
            
        if len(blocos_alocados) > 1:
            self._atualizar_fat_com_prox_bloco(blocos_alocados)
            
        # Verifica se o arquivo foi alocado completamente
        if tamanho_restante == 0:
            return blocos_alocados
        else:
            # Se não houver espaço suficiente na FAT para alocar o arquivo
            # marca os blocos anteriores como livres novamente
            self._resetar_blocos_iniciais(bloco_inicial, bloco_atual, estado_inicial)
            raise ValueError("Há bloco livre na FAT, mas não o suficiente para alocar o arquivo.")
             
        
    def _alocar_bloco(self, bloco_atual, tamanho_restante, blocos_alocados):
        """
        Aloca um bloco para o arquivo e atualiza os valores de bloco_atual, tamanho_restante e blocos_alocados.

        Args:
        bloco_atual (int): Índice do bloco atual.
        tamanho_restante (int): Tamanho do arquivo restante a ser alocado.
        blocos_alocados (list): Lista de índices dos blocos alocados para o arquivo.

        Returns:
        tuple: (bloco_atual, tamanho_restante, blocos_alocados)
        """
        if self.fat[bloco_atual]["livre"]:
            tamanho_bloco_disponivel = self.tamanho_bloco
            tamanho_a_alocar = min(tamanho_restante, tamanho_bloco_disponivel)
            self.fat[bloco_atual]["livre"] = False
            tamanho_restante -= tamanho_a_alocar
            blocos_alocados.append(bloco_atual)
        return bloco_atual + 1, tamanho_restante, blocos_alocados
    
    def _atualizar_fat_com_prox_bloco(self, blocos_alocados):
        """
        Atualiza a FAT com os índices dos blocos alocados como próximos blocos.

        Args:
        blocos_alocados (list): Lista de índices dos blocos alocados para o arquivo.
        """
        for i in range(len(blocos_alocados) - 1):
            self.fat[blocos_alocados[i]]["prox_bloco"] = blocos_alocados[i + 1]

    def _resetar_blocos_iniciais(self, bloco_inicial, bloco_atual, estado_inicial):
        """
        Marca os blocos anteriores como livres novamente e atualiza os próximos blocos na FAT para -1.

        Args:
        bloco_inicial (int): Índice do bloco inicial.
        bloco_atual (int): Índice do bloco atual.
        estado_inicial (list): Estado inicial dos blocos na FAT.
        """
        for i in range(bloco_inicial, bloco_atual):
            self.fat[i]["livre"] = estado_inicial[i]["livre"]
            self.fat[i]["prox_bloco"] = estado_inicial[i]["prox_bloco"]
    
    def remover_arquivo(self, bloco_inicial):
        """
        Remove um arquivo da FAT, liberando os blocos alocados.

        Args:
        bloco_inicial (int): Índice do bloco inicial do arquivo.
        """
        bloco_atual = bloco_inicial
        while bloco_atual != -1:
            # Configura o próximo bloco do bloco atual para -1
            proximo_bloco = self.fat[bloco_atual]["prox_bloco"]
            self.fat[bloco_atual]["prox_bloco"] = -1
            # Libera o bloco atual, marcando-o como livre na FAT
            self.fat[bloco_atual]["livre"] = True
            # Atualiza o bloco atual para o próximo bloco
            bloco_atual = proximo_bloco
        return None
    

    def calcular_espaco_livre_fragmentado(self):
        """
        Calcula o espaço livre fragmentado no disco, que é a quantidade total de espaço livre disponível
        que está fragmentado em pequenos blocos não contíguos.
    
        Returns:
        int: A quantidade total de espaço livre fragmentado, em bytes.
        """
        espaco_livre_fragmentado = 0
        espaco_livre_contiguo = 0
        for bloco in self.fat:
            if bloco["livre"]:
                espaco_livre_contiguo += self.tamanho_bloco
            else:
                if espaco_livre_contiguo > 0:
                    espaco_livre_fragmentado += espaco_livre_contiguo
                    espaco_livre_contiguo = 0
        return espaco_livre_fragmentado
    
    def calcular_taxa_fragmentacao(self):
        """
        Calcula a taxa de fragmentação do disco, que é a proporção do espaço livre total com o espaço livre fragmentado.

        Returns:
        float: A taxa de fragmentação, em porcentagem.
        """
        espaco_livre_total = self.trilhas * self.blocos_por_trilha * self.tamanho_bloco
        espaco_fragmentado = self.calcular_espaco_livre_fragmentado()
        taxa_fragmentacao = (espaco_fragmentado / espaco_livre_total) * 100
        return taxa_fragmentacao
    
    def exibir_estado_fat(self):
        """
        Exibe o estado atual da FAT
        """
        for indice, bloco in enumerate(self.fat):
            print(f'Bloco {indice}: {bloco}')

def main():
    tamanho_bloco = 4000 
    trilhas = 4
    blocos_por_trilha = 16
    tempo_seek = 5
    tempo_rotacao = 10 
    tempo_transferencia = 2

    disco = Disco(tamanho_bloco, trilhas, blocos_por_trilha, tempo_seek, tempo_rotacao, tempo_transferencia)

# SIMULAÇÕES
    #CENÁRIO 0
    print("----- Estado Inicial da FAT -----")
    disco.exibir_estado_fat()

    print("===== Cenário 0 =====")
    print("----- Estado Atual da FAT -----")
    print("Alocando arquivos de tamanhos variados.",
          "\nTamanho do bloco:", tamanho_bloco, "Bytes",
          "\nTamanho do arquivo A:", 4000, "Bytes",
          "\nTamanho do arquivo B:", 12000, "Bytes",
          "\nTamanho do arquivo C:", 24000, "Bytes",
          "\nTamanho do arquivo D:", 56000, "Bytes")
    bloco_alocadoA = disco.alocar_arquivo(4000)
    bloco_alocadoB = disco.alocar_arquivo(13000)
    bloco_alocadoC = disco.alocar_arquivo(24000)
    bloco_alocadoD = disco.alocar_arquivo(55000)
    print("Blocos", bloco_alocadoA, bloco_alocadoB, bloco_alocadoC, bloco_alocadoD, "alocados.")
    disco.exibir_estado_fat()


    #CENÁRIO 1
    print("===== Cenário 1 =====")
    print("----- Estado Atual da FAT -----")
    print("Alocando arquivo E, F e G de tamanhos 3.6 KB, 15 KB e 57 KB, respectivamente",
          "\nTamanho do bloco:", tamanho_bloco, "Bytes",
          "\nTamanho do arquivo E:", 3600, "Bytes",
          "\nTamanho do arquivo F:", 15000, "Bytes",
          "\nTamanho do arquivo G:", 57000, "Bytes")
    bloco_alocadoE = disco.alocar_arquivo(3600)
    bloco_alocadoF = disco.alocar_arquivo(15000)
    bloco_alocadoG = disco.alocar_arquivo(57000)
    print("Blocos", bloco_alocadoE, bloco_alocadoF, bloco_alocadoG, "alocados.")
    disco.exibir_estado_fat()

    print("Removendo arquivos B e E.",
          "\nTamanho do bloco:", tamanho_bloco, "Bytes",
          "\nTamanho do arquivo B:", 12000, "Bytes",
          "\nTamanho do arquivo E:", 3600, "Bytes")
    disco.remover_arquivo(1) 
    disco.remover_arquivo(25)
    print("Arquivo salvo no bloco inicial 1 removido.")
    print("Arquivo salvo no bloco inicial 25 removido.")
    disco.exibir_estado_fat()

    #FRAGMENTAÇAO DO SISTEMA DE ARQUIVOS
    taxa_fragmentacao1 = disco.calcular_taxa_fragmentacao()
    print(f'Taxa de Fragmentação: {taxa_fragmentacao1:.2f}%')



    #CENÁRIO 2
    print("===== Cenário 2 =====")
    print("----- Estado Atual da FAT -----")
    print("Alocando arquivos H e I de tamanhos 8 KB e 18 KB, respectivamente.",
          "\nTamanho do bloco:", tamanho_bloco, "Bytes",
          "\nTamanho do arquivo H:", 8000, "Bytes",
          "\nTamanho do arquivo I:", 18000, "Bytes")
    bloco_alocadoH = disco.alocar_arquivo(8000)
    bloco_alocadoI = disco.alocar_arquivo(18000)
    print("Blocos", bloco_alocadoH, bloco_alocadoI, "alocados.")
    disco.exibir_estado_fat()
    

if __name__ == "__main__":
    main()