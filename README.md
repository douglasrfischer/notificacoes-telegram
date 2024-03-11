# Notificações Telegram

Envio de notificações automatizadas por meio do [python-telegram-bot](https://python-telegram-bot.org/).

- Os caminhos dos arquivos a serem verificados pela rotina _cargas_ devem ser inseridos diretamente no arquivo `dados.json` dentro da lista `caminhos`. Além disso, as contrabarras presentes no caminho devem estar escapadas (i.e., `C:\Windows` &rarr; `C:\\Windows`) e deve obedecer o formato **nome do projeto: caminho** (chave: valor).

# Roadmap
## Alpha 1.0
- [x] Rotina de conferência das cargas
- [x] Disparo das mensagens (via Task Scheduler)

## Alpha 1.1
- [x] Rotina de verificação de divergência no fechamento das unidades

## Beta 1.0 - Refatoração e Autenticação
- [x] Implementação de controle de acesso/autenticação
- [x] Descarte do Task Scheduler para o envio das notificações

## Beta 1.1 - Desempenho e Detalhes nas Diferenças
- [x] Alterar a identificação de "Fechamento unidades" para "Importação das Vendas"
- [x] Para cada unidade que houver diferença, adicionar essa informação
- [x] Reduzir uso de CPU da função `main.executar_rotinas()`

## Beta 1.1.5 - Log PIDs
- [x] Adicionar log para armazenar os PIDs dos processos.

## Beta 1.2
- [ ] Transformar os usuários presentes em `notificados.json` em par chave valor, onde chave = id e valor = nome (assim como na lista `pendentes`), a fim de facilitar a identificação
- [ ] Notificar o usuário sobre sua aprovação
- [ ] Gerenciar caminhos dos projetos cuja carga deve ser conferida (integrar ao Gestor)


#
_Adaptado de projeto real_