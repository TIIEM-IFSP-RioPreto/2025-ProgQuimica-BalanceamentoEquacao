# Testes para o Módulo balanceamento_bini.py

Este arquivo contém testes abrangentes para as funções do módulo `balanceamento_bini.py`, que implementa um sistema de balanceamento de equações químicas usando métodos algébricos com SymPy.

## Funções Testadas

### 1. `parse_formula(formula)`
Analisa uma fórmula química e retorna a contagem de átomos de cada elemento.

**Casos testados:**
- **Elementos simples**: H, O, Fe
- **Elementos com quantidade**: H2, O3, Fe2
- **Compostos simples**: H2O, NaCl, CaCl2
- **Compostos complexos**: Fe2O3, C6H12O6, KMnO4
- **Casos especiais**: fórmulas vazias, espaços, elementos repetidos

### 2. `balancear_equacao(reagentes, produtos)`
Balanceia equações químicas usando o método algébrico com SymPy.

**Casos testados:**
- **Equações simples**: H2 + O2 → H2O
- **Combustão**: CH4 + O2 → CO2 + H2O
- **Formação de óxidos**: Fe + O2 → Fe2O3
- **Equações impossíveis**: H2 → O2 (deve falhar)
- **Verificação de saída**: confirma que a equação balanceada é impressa

### 3. `obter_equacao()`
Solicita reagentes e produtos ao usuário via input.

**Casos testados:**
- **Entrada simples**: um reagente, um produto
- **Múltiplas entradas**: vários reagentes e produtos
- **Entrada vazia**: usuário não insere nada
- **Case insensitive**: "fim", "FIM", "Fim" funcionam igual

## Como Executar os Testes

### Pré-requisitos
```bash
pip install pytest sympy
```

### Executar todos os testes
```bash
python -m pytest test_balanceamento_bini.py -v
```

### Executar testes específicos
```bash
# Apenas testes da função parse_formula
python -m pytest test_balanceamento_bini.py::TestParseFormula -v

# Apenas testes da função balancear_equacao
python -m pytest test_balanceamento_bini.py::TestBalancearEquacao -v

# Apenas testes da função obter_equacao
python -m pytest test_balanceamento_bini.py::TestObterEquacao -v
```

## Estrutura dos Testes

Os testes estão organizados em 5 classes:

- **TestParseFormula**: 10 testes para parsing de fórmulas químicas
- **TestBalancearEquacao**: 5 testes para balanceamento de equações
- **TestObterEquacao**: 4 testes para entrada de dados do usuário
- **TestIntegracao**: 2 testes de integração entre funções
- **TestCasosEspeciais**: 3 testes para casos especiais e edge cases

## Técnicas de Teste Utilizadas

### Mocking
- **`@patch('builtins.print')`**: Para capturar e verificar saídas impressas
- **`@patch('builtins.input')`**: Para simular entrada do usuário
- **Mock na importação**: Para evitar execução do código principal

### Verificações
- **Estruturas de dados**: Verificação de dicionários retornados
- **Saída de console**: Confirmação de mensagens impressas
- **Comportamento de erro**: Teste de casos impossíveis
- **Integração**: Teste do fluxo completo entre funções

## Exemplos de Uso dos Testes

### Teste de parsing de fórmula
```python
def test_composto_complexo(self):
    resultado = parse_formula("Fe2O3")
    assert dict(resultado) == {"Fe": 2, "O": 3}
```

### Teste de balanceamento com mock
```python
@patch('builtins.print')
def test_equacao_combustao_metano(self, mock_print):
    reagentes = ["CH4", "O2"]
    produtos = ["CO2", "H2O"]
    
    balancear_equacao(reagentes, produtos)
    
    # Verifica se imprimiu resultado
    mock_print.assert_called()
```

### Teste de entrada do usuário
```python
@patch('builtins.input')
def test_entrada_simples(self, mock_input):
    mock_input.side_effect = ["H2", "fim", "H2O", "fim"]
    
    reagentes, produtos = obter_equacao()
    
    assert reagentes == ["H2"]
    assert produtos == ["H2O"]
```

## Cobertura de Testes

Os testes cobrem:
- ✅ Parsing correto de fórmulas químicas
- ✅ Balanceamento de equações válidas
- ✅ Tratamento de equações impossíveis
- ✅ Entrada interativa do usuário
- ✅ Casos especiais e edge cases
- ✅ Integração entre componentes
- ✅ Saídas de console apropriadas

## Resultados Esperados

Todos os 24 testes devem passar quando executados. Os testes verificam tanto o comportamento correto quanto o tratamento adequado de casos de erro.

## Limitações dos Testes

- **Balanceamento complexo**: Alguns testes apenas verificam se a função executa sem erro, não a correção matemática completa
- **Interface de usuário**: Testes de `obter_equacao()` são limitados por dependerem de mocking
- **Casos matemáticos**: Não testam todos os casos possíveis de sistemas de equações lineares

## Notas Técnicas

- O arquivo `balanceamento_bini.py` contém código de execução no final, que é contornado usando mocking durante a importação
- Os testes usam `sympy` para operações matemáticas, assim como o código principal
- Verificações de saída usam `mock_print.assert_called()` para confirmar execução sem analisar conteúdo específico