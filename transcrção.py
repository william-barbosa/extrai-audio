# Considerações iniciais:
# Antes de iniciar é importante destacar que foi utilizado Python 3.12.3 com o sitema opercaional Ubtuntu 22.04. Assim, será necessário primeiro instalar:
# pip install -U openai-whisper |- Porém, existem algumas dependências: 
# sudo apt update && sudo apt install ffmpeg
# pip install setuptools-rust

from spellchecker import SpellChecker # Pacote utilizado para realizar a correção ortográfica
import yt_dlp   # Pacote utilizado para a extração do áudio.
import whisper  # Modelo utilizado para a transcrição. 
# Esse é um modelo da openai, que é uma rede neural chamada Whisper. 
# Existem vários tipos de modelos disponibilizados pela empresa: tiny, base, small, medium, large, turbo. Ver: https://github.com/openai/whisper

# Função para extrair o áudio de um vídeo
def download_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(id)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        'postprocessor_args': [
            '-ar', '44100'  # Define a taxa de amostragem para 44.1kHz (defini essa por simplicidade)
        ],
        'prefer_ffmpeg': True,
        'keepvideo': False,  # Remove o vídeo após o download
        'ffmpeg_location': '/usr/bin/ffmpeg'  # Configurar o caminho do ffmpeg (no meu caso é em Linux)
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Realiza a extração do áudio do vídeo e salva no formato de .wave
download_audio('https://www.youtube.com/watch?v=8IgzAP7kW9c')

# Função para transcrever o áudio. O modelo selecionado foi o 'medium', mas esse é um modelo pesado
def transcrever_audio(caminho_audio, caminho_arquivo_saida):
    modelo = whisper.load_model("medium")  # Carregar o modelo Whisper tiny, small
    # Realizar a transcrição    
    resultado = modelo.transcribe(caminho_audio, language="pt", task="transcribe") # resultado = modelo.transcribe(caminho_audio)

    # Obter o texto transcrito
    transcricao = resultado["text"]

    # Exibir a transcrição
    print("Transcrição: ")
    print(transcricao)

    # Salvar a transcrição em um arquivo de texto
    with open(caminho_arquivo_saida, 'w') as arquivo:
        arquivo.write(transcricao)

    print(f"Transcrição salva em {caminho_arquivo_saida}")

transcrever_audio('8IgzAP7kW9c.wav', 'transcricao_audio.txt')



## Ajustar e correção ortográfica. Isso ajudará posteriormente na análise de sentimentos
with open('transcricao_audio.txt', 'r', encoding='utf-8') as arquivo:
    transcricao = arquivo.read()

def corrigir_transcricao(transcricao):
    spell = SpellChecker(language='pt')  # Seleciona o dicionário em português
    palavras = transcricao.split()  # Divide o texto em palavras
    palavras_corrigidas = []  # Lista para guardar as palavras corrigidas

    for palavra in palavras:
        correcao = spell.correction(palavra)  # Tenta corrigir a palavra
        if correcao is not None:
            palavras_corrigidas.append(correcao)  # Se conseguiu corrigir, usa a correção
        else:
            palavras_corrigidas.append(palavra)  # Se não conseguiu, mantém a original

    return " ".join(palavras_corrigidas)  # Junta as palavras corrigidas num texto só

transcricao_corrigida = corrigir_transcricao(transcricao)


