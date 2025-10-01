# Testes para o Módulo de Balanceamento

Este arquivo contém um conjunto abrangente de testes para as funções do módulo `balanceamento`.

## Funções Testadas

### 1. `detalhes_elemento(identificador)`
- **Busca por número atômico**: Testa elementos válidos (H, O, Ca)
- **Busca por símbolo**: Testa símbolos válidos e em diferentes casos
- **Elementos sem massa atômica**: Testa elementos como Tecnécio (Tc)
- **Casos inválidos**: Números inexistentes, símbolos inexistentes, tipos inválidos

### 2. `separar_elementos(formula)`
- **Fórmulas simples**: H, H2, H2O
- **Fórmulas complexas**: Al2O3, C6H12O6, NaCl
- **Casos especiais**: Fórmulas vazias, apenas números, elementos múltiplos
- **Validação**: Verifica se a separação está correta

### 3. `calcular_massa(substancia)`
- **Elementos simples**: H, H2
- **Compostos comuns**: H2O (água), CO2 (dióxido de carbono)
- **Compostos complexos**: Al2O3 (óxido de alumínio), C6H12O6 (glicose)
- **Casos de erro**: Elementos inexistentes, sem massa atômica, fórmulas inválidas

## Como Executar os Testes

### Pré-requisitos
```bash
pip install pytest
```

### Executar todos os testes
```bash
python -m pytest test_balanceamento.py -v
```

### Executar testes específicos
```bash
# Apenas testes da função detalhes_elemento
python -m pytest test_balanceamento.py::TestDetalhesElemento -v

# Apenas testes da função separar_elementos
python -m pytest test_balanceamento.py::TestSepararElementos -v

# Apenas testes da função calcular_massa
python -m pytest test_balanceamento.py::TestCalcularMassa -v
```

### Executar um teste específico
```bash
python -m pytest test_balanceamento.py::TestCalcularMassa::test_massa_agua -v
```

## Estrutura dos Testes

Os testes estão organizados em classes:

- **TestDetalhesElemento**: 7 testes para a função `detalhes_elemento()`
- **TestSepararElementos**: 9 testes para a função `separar_elementos()`
- **TestCalcularMassa**: 11 testes para a função `calcular_massa()`
- **TestIntegracao**: 2 testes de integração entre as funções

## Cobertura de Testes

Os testes cobrem:
- ✅ Casos de sucesso (happy path)
- ✅ Casos de erro e exceções
- ✅ Validação de tipos de entrada
- ✅ Elementos com e sem massa atômica
- ✅ Fórmulas químicas simples e complexas
- ✅ Integração entre funções

## Exemplos de Uso dos Testes

### Verificar se um elemento existe
```python
def test_busca_por_simbolo_valido(self):
    elemento = detalhes_elemento("O")
    assert elemento is not None
    assert elemento.simbolo == "O"
```

### Verificar cálculo de massa
```python
def test_massa_agua(self):
    massa = calcular_massa("H2O")
    assert massa == pytest.approx(18.015000, rel=1e-6)
```

### Verificar separação de elementos
```python
def test_formula_glucose(self):
    resultado = separar_elementos("C6H12O6")
    assert resultado == [("C", 6), ("H", 12), ("O", 6)]
```

## Resultados Esperados

Todos os 29 testes devem passar quando executados. Se algum teste falhar, isso indica um problema na implementação das funções.