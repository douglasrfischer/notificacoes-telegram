from json import dump, load


class Usuarios:
    '''Model responsável por gerenciar os usuários e suas inscrições nas listas
    de notificações (lida com operações do ARQUIVO de dados).'''

    def _carregar(self) -> dict:
        '''Carrega dados de inscrição do arquivo "notificados.json".'''
        with open('data/notificados.json', 'r', encoding='utf8') as f:
            aux = load(f)
        return aux
    

    def _salvar(self, data: dict) -> None:
        '''Salva dados de inscrição para "dados.json". ⚠️ Utiliza o modo "w", 
        ou seja, TRUNCA o arquivo antes de inserir os dados.'''
        with open('data/notificados.json', 'w', encoding='utf8') as f:
            dump(data, f)


    def carregar_notificados(self) -> dict:
        '''Retorna LISTA de LISTAS de usuários a serem notificados.'''
        return self._carregar()['notificacoes']


    def carregar_pendentes(self) -> list:
        '''Retorna lista de usuários novos precisando de aprovação.'''
        return self._carregar()['pendentes']
    

    def carregar_bloqueados(self) -> list:
        '''Retorna lista de usuários bloqueados.'''
        return self._carregar()['bloqueados']


    def consultar_inscricoes(self, chat_id: int) -> list:
        '''Retorna listas de notificação nas quais o usuário está inscrito.'''
        listas = self._carregar()['notificacoes']
        return [x for x in listas if chat_id in listas[x]]


    def alterar_inscricao(self, chat_id: int, lista: str) -> int:
        '''Altera estado de inscrição do usuário na lista indicada. Caso o
        retorno seja 0, significa que o usuário foi removido. Se for 1 foi
        adicionado à lista.'''
        listas = self._carregar()

        foo = 0
        nenhuma_inscricao = False
        for key in listas['notificacoes'].keys():
            aux = listas['notificacoes'][key].count(chat_id)
            foo += aux
            if key == 'nenhuma' and aux:
                nenhuma_inscricao = True

        # Desinscreve
        if chat_id in listas['notificacoes'][lista]:
            listas['notificacoes'][lista].remove(chat_id)
            # Se estiver registrado em UMA lista que não 'nenhuma'
            if foo == 1 and not nenhuma_inscricao:
                listas['notificacoes']['nenhuma'].append(chat_id)
            self._salvar(listas)
            return 0
        
        # Inscreve
        listas['notificacoes'][lista].append(chat_id)
        # Se estiver apenas na lista 'nenhuma'
        if foo == 1 and nenhuma_inscricao:
            listas['notificacoes']['nenhuma'].remove(chat_id)
        self._salvar(listas)
        return 1


    def bloquear(self, chat_id: int) -> None:
        '''Move o usuário para a lista "bloqueados".'''
        dados = self._carregar()
        if chat_id not in self.carregar_bloqueados():
            dados['bloqueados'].append(chat_id)
            self._salvar(dados)


    def desbloquear(self, chat_id: int) -> None:
        '''Remove o usuário da lista de "bloqueados".'''
        dados = self._carregar()
        if chat_id in self.carregar_bloqueados():
            dados['bloqueados'].remove(chat_id)
            self._salvar(dados)
    

    def consultar_bloqueio(self, chat_id: int) -> bool:
        '''Consulta se o usuário informado está bloqueado.
        Se bloqueado, True.'''
        return chat_id in self.carregar_bloqueados()


    def adiciona_pendente(self, chat_id: int, nome: str) -> None:
        '''Adiciona o usuário à lista de "pendentes".'''
        dados = self._carregar()
        if str(chat_id) not in dados['pendentes'].keys():
            dados['pendentes'][chat_id] = nome
            self._salvar(dados)
