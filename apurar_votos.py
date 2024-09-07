import os
import discord
import pandas as pd
from colorama import Fore, Style
import datetime

# Inicializando intents para permitir acesso completo ao servidor e canais
intents = discord.Intents.all()

# Criando uma instância do bot cliente com os intents
client = discord.Client(intents=intents)

TOKEN = os.getenv('DISCORD_TOKEN')
nome_de_interesse = "Adriel de Souza" # Nome do participante a ser monitorado

if(TOKEN == None):
    print('Variável de ambiente DISCORD_TOKEN não encontrada. Encerrando...')
    exit()


@client.event
async def on_ready():
    """
    Função executada quando o bot se conecta com sucesso ao servidor do Discord.
    Coleta mensagens do canal especificado e cria um ranking baseado nas reações às mensagens.
    """
    print(f"Conectado como {client.user}")

    # IDs do servidor (guild) e canal. Substitua pelos seus próprios IDs.
    guild_id = 1277631721822748742  # Exemplo: ID do servidor
    channel_id = 1277631722716008535  # Exemplo: ID do canal

    # Obtendo o servidor e o canal
    guild = client.get_guild(guild_id)
    channel = guild.get_channel(channel_id)

    # Coleta todas as mensagens do canal
    messages = await channel.history(limit=None).flatten()
    messages = messages[::-1]  # Revertendo a ordem para a mais antiga primeiro
        
    print(f"Encontradas {len(messages)} mensagens")

    # Inicializando a lista do leaderboard
    leaderboard = []
        
    # Itera sobre cada mensagem e extrai informações do embed e reações
    for message in messages:
        votes = message.reactions[0].count  # Contagem de reações (ajuste conforme necessário)
        fields = message.embeds[0].fields   # Extrai campos do embed da mensagem
        nome = fields[0].value              # Nome do participante
        github = fields[1].value            # Link do GitHub

        # Adiciona uma entrada ao leaderboard com votos, nome e GitHub
        leaderboard.append((votes, nome, github))
        
    # Ordenando o leaderboard pela quantidade de votos em ordem decrescente
    leaderboard.sort(key=lambda x: x[0], reverse=True)
    
    # Criando um DataFrame com os dados coletados
    d = pd.DataFrame(leaderboard, columns=["Votos", "Nome", "GitHub"])
    d.index = range(1, len(d) + 1)
    d["Posição"] = [f'{x}º' for x in range(1, len(d) + 1)]
    d = d[["Posição", "Votos", "Nome", "GitHub"]]  # Rearranja as colunas

    # Salvando o ranking em um arquivo CSV com cabeçalho informativo
    with open("apuracao.csv", "w", encoding='utf-8') as f:
        f.write("# Atualizado em " + datetime.datetime.now().strftime("%d/%m/%Y às %H:%M:%S") + "\n")
        f.write("# Classificação NÃO oficial e parcial\n")
        d.to_csv(f, index=False, lineterminator='\n')
    
    # Exibindo as primeiras 30 entradas do ranking no console
    print(d.head(30))
    
    # Verifica a posição de "Adriel de Souza" no ranking
    posicao = d[d["Nome"] == nome_de_interesse].index[0]
    diferencas = [int(d.loc[posicao - x, "Votos"] - d.loc[posicao, "Votos"]) for x in range(1, min(5, posicao))]
    
    # Exibe as informações da posição de Adriel no ranking
    print(f"\n{nome_de_interesse} está na posição {Fore.GREEN}{Style.BRIGHT}{posicao}{Fore.RESET} do ranking com {d.loc[posicao, 'Votos']} votos {Style.RESET_ALL} e está {diferencas} votos atrás dos próximos colocados.")
    print(f'\t A diferença para o 10º colocado é de {d.loc[posicao - 10, "Votos"] - d.loc[posicao, "Votos"]} votos')

    # Encerra a execução do bot
    await client.close()

# Executa o bot
client.run(TOKEN, bot=False)