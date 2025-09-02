from balanceamento import calcular_massa, detalhes_elemento, separar_elementos


def calcular_massa_e_elementos(substancias, tipo):
    print(f"--- Quantidade de elementos nos {tipo} ---")
    massa_total = 0
    calculo_valido = True
    for substancia in substancias:
        massa_substancia = calcular_massa(substancia)
        if massa_substancia:
            massa_total += massa_substancia
            print(f"{substancia} ({massa_substancia:.6f} g/mol)")
        else:
            print(f"{substancia} (Massa molar não determinada)")
            calculo_valido = False
    if calculo_valido:
        print(f"Massa total dos {tipo}: {massa_total:.8f} g/mol")

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
calcular_massa_e_elementos(reagentes, "reagentes")

print()
calcular_massa_e_elementos(produtos, "produtos")
