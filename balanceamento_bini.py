import sympy
from collections import defaultdict
import re

##Parte 1
def obter_equacao():
    """
    Solicita reagentes e produtos ao usuário e retorna-os em listas.
    """
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
    print("\n--- Inserir Produtos ---")
    while True:
        produto = input("Digite um produto (ou 'fim' para parar): ")
        if produto.lower() == 'fim':
            break
        produtos.append(produto)

    return reagentes, produtos

##Partte 2
def parse_formula(formula):
    """
    Analisa uma fórmula química e retorna a contagem de átomos de cada elemento.
    Exemplo: "Fe2O3" -> {'Fe': 2, 'O': 3}
    """
    atoms = defaultdict(int)
    # Encontra elementos e seus subscritos
    matches = re.findall(r'([A-Z][a-z]*)(\d*)', formula)
    for element, count in matches:
        if count:
            atoms[element] += int(count)
        else:
            atoms[element] += 1
    return atoms

## Parte 3
def balancear_equacao(reagentes, produtos):
    """
    Balanceia a equação química usando o método algébrico.
    """
    todos_elementos = set()
    componentes = reagentes + produtos
    
    # Atribui uma variável simbólica a cada componente
    variaveis = sympy.symbols('a:z')[:len(componentes)]
    
    # Extrai todos os elementos únicos
    for componente in componentes:
        formula = parse_formula(componente)
        todos_elementos.update(formula.keys())
        
    # Cria as equações
    equacoes = []
    for elemento in todos_elementos:
        equacao_elementar = 0
        
        # Reagentes (sinal positivo)
        for i, reagente in enumerate(reagentes):
            formula = parse_formula(reagente)
            equacao_elementar += formula.get(elemento, 0) * variaveis[i]
            
        # Produtos (sinal negativo)
        for i, produto in enumerate(produtos):
            formula = parse_formula(produto)
            equacao_elementar -= formula.get(elemento, 0) * variaveis[len(reagentes) + i]
        
        equacoes.append(equacao_elementar)
    
    
## Parte 4    
    # Resolve o sistema de equações
    # Adiciona uma restrição para resolver, por exemplo, a primeira variável = 1
    equacoes.append(variaveis[0] - 1)
    
    solucao = sympy.solve(equacoes, variaveis)
    
    # Processa a solução para obter inteiros
    if not solucao:
        print("Não foi possível balancear a equação. Verifique o formato.")
        return
        
    coeficientes = [solucao[var] for var in variaveis]
    
    # Encontra o mínimo múltiplo comum para converter para inteiros
    # Esta parte é um pouco mais complexa, mas essencial para obter a resposta correta
    denominadores = [sympy.denom(c) for c in coeficientes]
    lcm = sympy.lcm(denominadores)
    
    coeficientes_inteiros = [int(c * lcm) for c in coeficientes]
    
    # Imprime a equação balanceada
    equacao_balanceada = " + ".join([f"{coef} {comp}" if coef != 1 else comp for coef, comp in zip(coeficientes_inteiros, reagentes)])
    equacao_balanceada += " -> "
    equacao_balanceada += " + ".join([f"{coef} {comp}" if coef != 1 else comp for coef, comp in zip(coeficientes_inteiros[len(reagentes):], produtos)])
    
    print("\nEquação balanceada:")
    print(equacao_balanceada)
    
    
## Parte 5   
## --- Execução do Programa ---
reagentes, produtos = obter_equacao()

if reagentes and produtos:
    balancear_equacao(reagentes, produtos)