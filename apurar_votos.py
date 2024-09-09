import os
import time
import discord
import pandas as pd
from colorama import Fore, Style
import datetime
from uploadToServer import upload_to_server

# Inicializando intents para permitir acesso completo ao servidor e canais
intents = discord.Intents.all()

# Criando uma instância do bot cliente com os intents
client = discord.Client(intents=intents)

TOKEN = os.getenv('DISCORD_TOKEN')
nome_de_interesse = "Adriel de Souza"

if(TOKEN == None):
    print('Variável de ambiente DISCORD_TOKEN não encontrada. Encerrando...')
    exit()

async def atualizar_ranking():
    # Obtendo o servidor e o canal
    guild = client.get_guild(1277631721822748742)
    channel = guild.get_channel(1277631722716008535)

    # Coleta todas as mensagens do canal
    messages = await channel.history(limit=None).flatten()
    messages = messages[::-1]  # Revertendo a ordem para a mais antiga primeiro
        
    print(f"Encontradas {len(messages)} mensagens")

    # Inicializando a lista do leaderboard
    leaderboard = []
        
    # Itera sobre cada mensagem e extrai informações do embed e reações
    for message in messages:
        votes = 0
        if(len(message.reactions) > 0):  
            for r in message.reactions:
                if r.emoji == '⭐':
                    votes = r.count
                    break
        fields = message.embeds[0].fields   # Extrai campos do embed da mensagem
        nome = fields[0].value              # Nome do participante
        github = fields[1].value            # GitHub do participante
        #f'<a href="{fields[1].value}">{fields[1].value.split("/")[-1]}</a>'  # Link do GitHub
        link_mensagem = message.jump_url    # Link para a mensagem no Discord
        #f'<a href="{message.jump_url}">Vote aqui!</a>'  # Link da mensagem

        # Adiciona uma entrada ao leaderboard com votos, nome e GitHub
        leaderboard.append((votes, nome, github, link_mensagem))
    
    # Criando um DataFrame com os dados coletados
    d = pd.DataFrame(leaderboard, columns=["Votos", "Nome", "GitHub", "Link para Votar"])
    # Ordena o DataFrame pelo número de votos mudando o index
    d = d.sort_values(by="Votos", ascending=False) # Ordena o DataFrame
    d.index = range(1, len(d) + 1)  # Atualiza o index
    

    # Salva o ranking em um arquivo HTML
    with open('apuracao-imersao-dev.html', 'w', encoding='utf-8') as f:
        promoting = '<p style="font-size: .9rem;">Já viu meu projeto? <b><a href="https://github.com/dsadriel/imersao-dev-alura-gemini"target="_blank">Sabores da Alma</a></b> é um catálogo de receitas online que oferece uma experiência simples e prática para quem busca descobrir novos sabores e transformar a rotina na cozinha. Este projeto foi desenvolvido durante a Imersão Dev daAlura + Google Gemini.<a href="https://discord.com/channels/1277631721822748742/1277631722716008535/1281331538960580672"target="_blank">Deixe seu voto</a></p>'
        html = '<!DOCTYPE html><html lang="pt-br"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Apuração NÃO OFICIAL dos votos | Imersão DEV Alura + Google Gemini</title><style>body {font-family: "Inter", sans-serif;background-color: var(--cor-fundo);min-height: 100vh;display: flex;flex-direction: column;justify-content: space-between;}table {border-collapse: collapse;width: 100%;table-layout:auto;}th {text-align: center;}table th:first-child,table td:first-child,table th:nth-child(2),table td:nth-child(2) {text-align: center;}td {padding: 2px 5px;}table tr:nth-child(n+31) {background-color: #d6d6d6;}table tr:nth-child(n+101) {background-color: #bbb;}</style></head><body><main style="max-width: 90%; margin: auto;"><h1>Apuração NÃO OFICIAL dos votos</h1><p><b>Este projeto é uma iniciativa independente e não possui qualquer relação com a Alura, Google ou qualquer outra empresa. </b>O objetivo é apenas possibilitar a apuração dos votos de forma transparente e acessível a todos os participantes da Imersão DEV.</p>'+promoting+'<pre>'
        html += 'Última atualização: ' + datetime.datetime.now().strftime("%d/%m/%Y às %H:%M:%S") +  '  (GMT-3 - Horário de Brasília)\n\n</pre>'
        html += d.to_html(index=True)
        html += """</main><script>
                document.querySelectorAll('tbody tr').forEach(l => {
                    // Atualizar link na coluna 4
                    l.children[4].innerHTML = '<a href="' + l.children[4].innerText + '" target="_blank">Vote aqui!</a>';
                    
                    // Limitar o tamanho do texto na coluna 3
                    if (l.children[3].innerText.length > 50) {
                        l.children[3].innerHTML = '<a href="' + l.children[3].innerText + '" target="_blank">' + l.children[3].innerText.slice(0, 50) + '...</a>';
                    } else {
                        l.children[3].innerHTML = '<a href="' + l.children[3].innerText + '" target="_blank">' + l.children[3].innerText + '</a>';
                    }
                    });
                    </script>
                    </body></html>"""
        f.write(html)
    
    
    # Envia o arquivo HTML para o servidor e exibe mensagem de confirmação
    upload_to_server('apuracao-imersao-dev.html')
    print(f'{datetime.datetime.now().strftime("%d/%m/%Y às %H:%M:%S")}: Ranking atualizado e enviado para o servidor.')
    

    # Exibe informações sobre a posição ocupada pelo nome de interesse no ranking    
    if(nome_de_interesse is None):   
        return 

    posicao = d[d["Nome"] == nome_de_interesse].index[0]
    diferencas = [int(d.loc[posicao - x, "Votos"] - d.loc[posicao, "Votos"]) for x in range(1, min(5, posicao))]
    
    print(f"\n{nome_de_interesse} está na posição {Fore.GREEN}{Style.BRIGHT}{posicao}{Fore.RESET} do ranking com {d.loc[posicao, 'Votos']} votos {Style.RESET_ALL} e está {diferencas} votos atrás dos próximos colocados.")
    print(f'\t A diferença para o 30º colocado é de {d.loc[30, "Votos"] - d.loc[posicao, "Votos"]} votos')


@client.event
async def on_ready():
    """
    Função executada quando o bot se conecta com sucesso ao servidor do Discord.
    Coleta mensagens do canal especificado e cria um ranking baseado nas reações às mensagens.
    """
    print(f"Conectado como {client.user}")

    while(True):
        # Atualiza o ranking a cada 5 minutos
        await atualizar_ranking()
        if datetime.datetime.now().strftime("%d/%m/%Y") == "09/09/2024":
            print('Data de encerramento do bot atingida. Encerrando...')
            break
        time.sleep(60 *5)  # Espera 5 minutos antes de atualizar o ranking
        
    # Encerra a execução do bot
    await client.close()
    os.system('shutdown /s /t 1') # Desliga o computador após 1 segundo

# Executa o bot
client.run(TOKEN, bot=False)