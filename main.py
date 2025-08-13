from balanceamento import massa_atomica, separar_elementos

# Lista para armazenar os reagentes e produtos
reagentes = []
produtos = []

# Captura dos reagentes
print("--- Inserir Reagentes ---")
while True:
    reagente = input("Digite um reagente (ou 'fim' para parar): ")
    if reagente.lower() == 'fim':
        break
    reagentes.append(reagente)

# Captura dos produtos
print()
print("--- Inserir Produtos ---")
while True:
    produto = input("Digite um produto (ou 'fim' para parar): ")
    if produto.lower() == 'fim':
        break
    produtos.append(produto)

# Monta a equação no formato texto
equacao_reagentes = " + ".join(reagentes)
equacao_produtos = " + ".join(produtos)

# Imprime a equação final
print()
print("--- Equação Química ---")
print(f"{equacao_reagentes} -> {equacao_produtos}")

print()
print()
print("--- Quantidade de elementos nos reagentes ---")
massa_total = 0
for reagente in reagentes:
    massa = 0
    elementos = separar_elementos(reagente)
    for elemento in elementos:
        if massa_atomica(elemento[0]) is False:
            print(f"Elemento desconhecido: {elemento[0]}")
            continue
        massa += massa_atomica(elemento[0]) * elemento[1]
        massa_total += massa
    print(f"{reagente} ({massa:.8f} g/mol): {elementos}")
print(f"Massa total dos reagentes: {massa_total:.8f} g/mol")

massa_total = 0
print()
print("--- Quantidade de elementos nos produtos ---")
for produto in produtos:
    massa = 0
    elementos = separar_elementos(produto)
    for elemento in elementos:
        if massa_atomica(elemento[0]) is False:
            print(f"Elemento desconhecido: {elemento[0]}")
            continue
        massa += massa_atomica(elemento[0]) * elemento[1]
        massa_total += massa
    print(f"{produto} ({massa:.8f} g/mol): {elementos}")
print(f"Massa total dos produtos: {massa_total:.8f} g/mol")
