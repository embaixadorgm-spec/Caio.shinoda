import requests
import math
import os # <-- Linha nova
import telebot # <-- Linha nova

# --- CONFIGURAÇÕES ---
# O código agora lê automaticamente do Render.com:
API_KEY = os.environ.get("API_KEY") 
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
bot = telebot.TeleBot(TELEGRAM_TOKEN) # <-- Inicializa o bot aqui

def calcular_poisson(media, x):
    return (math.exp(-media) * (media**x)) / math.factorial(x)

def buscar_stats_e_odds(fixture_id):
    url = f"https://v3.football.api-sports.io{fixture_id}"
    headers = {'x-apisports-key': API_KEY}
    res = requests.get(url, headers=headers).json()['response'][0]

    # Médias de gols (Simulado: em um bot real, você puxaria do endpoint /teams/statistics)
    media_casa = 1.8  # Ex: Média de gols marcados pelo time da casa
    media_fora = 1.2  # Ex: Média de gols marcados pelo time visitante
    
    # Pegando a Odd da Casa (Bookmaker)
    odd_casa_site = 2.10 # Valor de exemplo que viria da API
    
    return media_casa, media_fora, odd_casa_site

def motor_de_analise(fixture_id):
    m_casa, m_fora, odd_site = buscar_stats_e_odds(fixture_id)
    
    # 1. CÁLCULO DA PROBABILIDADE REAL (POISSON) - Vitória Casa
    prob_casa = 0
    for c in range(0, 6):
        for f in range(0, c):
            prob_casa += calcular_poisson(m_casa, c) * calcular_poisson(m_fora, f)
    
    # 2. MÉTRICAS FINANCEIRAS
    prob_implicita = 1 / odd_site
    ev = (prob_casa * (odd_site - 1)) - (1 - prob_casa)
    vig = 1.05 - 1 # Exemplo de taxa de 5% da casa
    
    # 3. CRITÉRIO DE KELLY (Gestão de Banca)
    b = odd_site - 1
    p = prob_casa
    q = 1 - p
    kelly_sugerido = ((p * b) - q) / b if b > 0 else 0
    
    # 4. FILTRO DE ENTRADA (O SEGREDO)
    if ev > 0.05: # Só entra se tiver mais de 5% de Valor Esperado
        mensagem = (
            f"✅ **OPORTUNIDADE ENCONTRADA**\n"
            f"📈 Prob. Real: {prob_casa*100:.2f}%\n"
            f"📊 Prob. Implícita (Casa): {prob_implicita*100:.2f}%\n"
            f"💰 EV+: {ev*100:.2f}%\n"
            f"🏦 Sugestão Kelly: {kelly_sugerido*10:.2f}% da banca"
        )
        enviar_telegram(mensagem)

def enviar_telegram(msg):
    url = f"https://api.telegram.org{TOKEN_TELEGRAM}/sendMessage?chat_id={CHAT_ID}&text={msg}&parse_mode=Markdown"
    requests.get(url)

# Execução
motor_de_analise(854321) # ID de exemplo de um jogo
