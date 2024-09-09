# Apuração NÃO OFICIAL dos Votos | Imersão DEV Alura + Google Gemini

Este projeto foi desenvolvido durante a Imersão Dev da Alura + Google Gemini e tem como objetivo realizar a **apuração NÃO OFICIAL** dos votos de participantes, exibindo um ranking com base em reações a mensagens do Discord. O projeto é composto por um bot que coleta dados de um canal do Discord e uma interface web para exibir os resultados.

> [!WARNING] 
> Este projeto é uma iniciativa independente e não possui qualquer relação com a Alura, Google ou qualquer outra empresa. O objetivo é apenas possibilitar a apuração dos votos de forma transparente e acessível a todos os participantes da Imersão DEV.

## Funcionalidades

### Bot do Discord (Python)

- **Coleta de dados**: O bot coleta todas as mensagens e reações de um canal específico no Discord.
- **Apuração de votos**: O ranking dos participantes é gerado com base nas reações às mensagens.
- **Exportação de dados**: O ranking é exportado para um arquivo CSV com a posição, quantidade de votos, nome e GitHub dos participantes.
- **Análise personalizada**: O bot também identifica e exibe a posição de um participante específico no ranking, destacando as diferenças de votos para os próximos colocados.

## Tecnologias Utilizadas

- Python
- Discord.py
- Pandas

## Como Executar o Projeto

### 1. Bot do Discord

1. Clone o repositório:
 ```bash
git clone https://github.com/dsadriel/imersao-dev-alura-apuracao
cd imersao-dev-alura-apuracao
```
2. Instale as dependências do projeto:
```bash
pip install discord pandas colorama
```
3. Configure a variável de ambiente DISCORD_TOKEN com o token do seu bot:
```bash
export DISCORD_TOKEN=seu-token-aqui
```
4. Execute o bot:
```bash
python apurar_votos.py
```
> O bot irá gerar um arquivo HTML com o ranking dos participantes.


## Contribuições

Sinta-se à vontade para abrir uma issue ou enviar um pull request com melhorias.
## Licença

Este projeto está licenciado sob a licença MIT - consulte o arquivo [LICENSE](LICENSE) para obter detalhes.