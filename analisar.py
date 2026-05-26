import requests

API_KEY = "cc47bf1f2acb982f8ce51aa4f79eabb5"

url = "https://api.the-odds-api.com/v4/sports/soccer_brazil_campeonato/odds"

parametros = {
    "apiKey": API_KEY,
    "regions": "eu",
    "markets": "h2h",
    "oddsFormat": "decimal"
}

resposta = requests.get(url, params=parametros)
dados = resposta.json()

print("=== ANALISE DE SINAIS ===\n")

sinais_encontrados = 0

for jogo in dados:
    casa = jogo["home_team"]
    fora = jogo["away_team"]
    data = jogo["commence_time"][:10]

    bookmaker = jogo["bookmakers"][0]
    mercado = bookmaker["markets"][0]
    outcomes = mercado["outcomes"]

    odd_casa = next(o["price"] for o in outcomes if o["name"] == casa)
    odd_fora = next(o["price"] for o in outcomes if o["name"] == fora)

    # ── CRITERIOS DO SINAL ──────────────────────────
    odd_minima = 1.50
    odd_maxima = 3.50
    diferenca_maxima = 1.50

    casa_valida = odd_minima <= odd_casa <= odd_maxima
    fora_valida = odd_minima <= odd_fora <= odd_maxima
    equilibrado = abs(odd_casa - odd_fora) <= diferenca_maxima

    if casa_valida and fora_valida and equilibrado:
        sinais_encontrados += 1
        print(f"✅ SINAL ENCONTRADO!")
        print(f"   Jogo : {casa} x {fora}")
        print(f"   Data : {data}")
        print(f"   Odds : Casa {odd_casa} | Fora {odd_fora}")
        print(f"   Dica : Jogo equilibrado — apostar no mais baixo")
        print()

if sinais_encontrados == 0:
    print("Nenhum sinal encontrado hoje.")

print(f"Total analisado : {len(dados)} jogos")
print(f"Sinais gerados  : {sinais_encontrados}")