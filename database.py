import sqlite3

# 1. CRIAR O BANCO DE DADOS
def iniciar_banco():
    conn = sqlite3.connect('analises_bot.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historico (
            id INTEGER PRIMARY KEY,
            jogo TEXT,
            previsao_placar TEXT,
            ev_detectado REAL,
            resultado_real TEXT,
            lucro_prejuizo REAL
        )
    ''')
    conn.commit()
    conn.close()

# 2. SALVAR APOSTA REALIZADA
def salvar_aposta(jogo, previsao, ev):
    conn = sqlite3.connect('analises_bot.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO historico (jogo, previsao_placar, ev_detectado) VALUES (?, ?, ?)', 
                   (jogo, previsao, ev))
    conn.commit()
    conn.close()

# 3. AUTO-AJUSTE (APRENDER COM O RESULTADO)
def atualizar_aprendizado():
    conn = sqlite3.connect('analises_bot.db')
    cursor = conn.cursor()
    # Pega as últimas 50 apostas para ver a Porcentagem de Acerto Real
    cursor.execute('SELECT lucro_prejuizo FROM historico WHERE resultado_real IS NOT NULL')
    resultados = cursor.fetchall()
    
    if len(resultados) > 0:
        win_rate = sum(1 for r in resultados if r[0] > 0) / len(resultados)
        print(f"Sua taxa de acerto real atual é: {win_rate*100:.2f}%")
        
        # Se a taxa de acerto cair abaixo de 45%, o bot sugere reduzir o Kelly
        if win_rate < 0.45:
            print("⚠️ Alerta: Estratégia perdendo eficiência. Reduzindo exposição de banca.")
    
    conn.close()

iniciar_banco()
