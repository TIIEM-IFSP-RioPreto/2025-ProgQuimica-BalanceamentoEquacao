from balanceamento import detalhes_elemento, separar_elementos

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
    massa_reagente = 0.0
    calculo_valido = True

    elementos = separar_elementos(reagente)
    # Se a fórmula for inválida, o resultado de separar_elementos será vazio
    if not elementos:
        print(f"Fórmula inválida ou não reconhecida: '{reagente}'")
        continue

    # Itera sobre cada tupla (símbolo, quantidade)
    for simbolo, quantidade in elementos:
        dados_do_elemento = detalhes_elemento(simbolo)
        if dados_do_elemento is None:
            print(f"  -> ERRO: Elemento desconhecido: '{simbolo}'")
            calculo_valido = False
            break

        if dados_do_elemento.massa_atomica is None:
            print(f"  -> ERRO: Elemento '{dados_do_elemento.nome}' ({simbolo}) não "
                  f"possui massa atômica definida.")
            calculo_valido = False
            break
        # Se for válido, acumula a massa do produto atual
        massa_reagente += dados_do_elemento.massa_atomica * quantidade

    if calculo_valido:
        massa_total += massa_reagente
        print(f"{reagente} ({massa_reagente:.6f} g/mol): {elementos}")
    else:
        print(f"{reagente} (Massa molar não determinada): {elementos}")
print(f"Massa total dos reagentes: {massa_total:.8f} g/mol")

print()
print("--- Quantidade de elementos nos produtos ---")
massa_total = 0
for produto in produtos:
    massa_produto = 0.0
    calculo_valido = True

    elementos = separar_elementos(produto)
    # Se a fórmula for inválida, o resultado de separar_elementos será vazio
    if not elementos:
        print(f"Fórmula inválida ou não reconhecida: '{produto}'")
        continue

    # Itera sobre cada tupla (símbolo, quantidade)
    for simbolo, quantidade in elementos:
        dados_do_elemento = detalhes_elemento(simbolo)
        if dados_do_elemento is None:
            print(f"  -> ERRO: Elemento desconhecido: '{simbolo}'")
            calculo_valido = False
            break

        if dados_do_elemento.massa_atomica is None:
            print(f"  -> ERRO: Elemento '{dados_do_elemento.nome}' ({simbolo}) não "
                  f"possui massa atômica definida.")
            calculo_valido = False
            break
        # Se for válido, acumula a massa do produto atual
        massa_produto += dados_do_elemento.massa_atomica * quantidade

    if calculo_valido:
        massa_total += massa_produto
        print(f"{produto} ({massa_produto:.6f} g/mol): {elementos}")
    else:
        print(f"{produto} (Massa molar não determinada): {elementos}")
print(f"Massa total dos produtos: {massa_total:.8f} g/mol")
