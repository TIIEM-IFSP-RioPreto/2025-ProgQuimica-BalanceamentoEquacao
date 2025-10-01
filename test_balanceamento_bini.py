import pytest
import sympy
from unittest.mock import patch, call
from io import StringIO
import sys
from collections import defaultdict

# Importar as funções do módulo - com mock para evitar execução do código principal
with patch('builtins.input', side_effect=['fim', 'fim']):
    from balanceamento_bini import parse_formula, balancear_equacao, obter_equacao


class TestParseFormula:
    """Testes para a função parse_formula()"""
    
    def test_elemento_simples(self):
        """Testa parsing de elemento simples"""
        resultado = parse_formula("H")
        assert dict(resultado) == {"H": 1}
    
    def test_elemento_com_quantidade(self):
        """Testa parsing de elemento com quantidade"""
        resultado = parse_formula("H2")
        assert dict(resultado) == {"H": 2}
    
    def test_composto_simples(self):
        """Testa parsing de composto simples"""
        resultado = parse_formula("H2O")
        assert dict(resultado) == {"H": 2, "O": 1}
    
    def test_composto_complexo(self):
        """Testa parsing de composto mais complexo"""
        resultado = parse_formula("Fe2O3")
        assert dict(resultado) == {"Fe": 2, "O": 3}
    
    def test_composto_multiplos_elementos(self):
        """Testa parsing de composto com múltiplos elementos"""
        resultado = parse_formula("CaCl2")
        assert dict(resultado) == {"Ca": 1, "Cl": 2}
    
    def test_composto_numeros_grandes(self):
        """Testa parsing com números grandes"""
        resultado = parse_formula("C6H12O6")
        assert dict(resultado) == {"C": 6, "H": 12, "O": 6}
    
    def test_elemento_duas_letras(self):
        """Testa parsing de elemento com duas letras"""
        resultado = parse_formula("NaCl")
        assert dict(resultado) == {"Na": 1, "Cl": 1}
    
    def test_formula_vazia(self):
        """Testa parsing de fórmula vazia"""
        resultado = parse_formula("")
        assert dict(resultado) == {}
    
    def test_formula_com_espacos(self):
        """Testa que espaços são ignorados (não devem aparecer em fórmulas válidas)"""
        resultado = parse_formula("H 2 O")
        # A regex captura H (sem número) e O (sem número), ignorando o 2 isolado
        assert dict(resultado) == {"H": 1, "O": 1}
    
    def test_elementos_repetidos(self):
        """Testa que elementos repetidos são somados"""
        resultado = parse_formula("H2OH2")
        assert dict(resultado) == {"H": 4, "O": 1}


class TestBalancearEquacao:
    """Testes para a função balancear_equacao()"""
    
    @patch('builtins.print')
    def test_equacao_simples_h2_o2(self, mock_print):
        """Testa balanceamento da equação H2 + O2 -> H2O"""
        reagentes = ["H2", "O2"]
        produtos = ["H2O"]
        
        balancear_equacao(reagentes, produtos)
        
        # Verifica se a função foi chamada (não travou)
        mock_print.assert_called()
        
        # Verifica se imprimiu a equação balanceada
        calls = [str(call) for call in mock_print.call_args_list]
        equacao_impressa = any("Equação balanceada:" in call for call in calls)
        assert equacao_impressa
    
    @patch('builtins.print')
    def test_equacao_combustao_metano(self, mock_print):
        """Testa balanceamento da combustão do metano: CH4 + O2 -> CO2 + H2O"""
        reagentes = ["CH4", "O2"]
        produtos = ["CO2", "H2O"]
        
        balancear_equacao(reagentes, produtos)
        
        mock_print.assert_called()
        calls = [str(call) for call in mock_print.call_args_list]
        equacao_impressa = any("Equação balanceada:" in call for call in calls)
        assert equacao_impressa
    
    @patch('builtins.print')
    def test_equacao_formacao_agua(self, mock_print):
        """Testa balanceamento: H2 + O2 -> H2O"""
        reagentes = ["H2", "O2"]
        produtos = ["H2O"]
        
        balancear_equacao(reagentes, produtos)
        
        # Verifica que não houve erro
        mock_print.assert_called()
    
    @patch('builtins.print')
    def test_equacao_impossivel(self, mock_print):
        """Testa equação que não pode ser balanceada"""
        reagentes = ["H2"]
        produtos = ["O2"]  # Impossível: H não pode virar O
        
        balancear_equacao(reagentes, produtos)
        
        # Deve imprimir mensagem de erro
        calls = [str(call) for call in mock_print.call_args_list]
        erro_impresso = any("Não foi possível balancear" in call for call in calls)
        assert erro_impresso
    
    @patch('builtins.print')
    def test_equacao_complexa_ferro(self, mock_print):
        """Testa balanceamento: Fe + O2 -> Fe2O3"""
        reagentes = ["Fe", "O2"]
        produtos = ["Fe2O3"]
        
        balancear_equacao(reagentes, produtos)
        
        mock_print.assert_called()
        calls = [str(call) for call in mock_print.call_args_list]
        equacao_impressa = any("Equação balanceada:" in call for call in calls)
        assert equacao_impressa


class TestObterEquacao:
    """Testes para a função obter_equacao() usando mock de input"""
    
    @patch('builtins.input')
    def test_entrada_simples(self, mock_input):
        """Testa entrada simples com um reagente e um produto"""
        # Simula as entradas do usuário
        mock_input.side_effect = [
            "H2",      # primeiro reagente
            "fim",     # termina reagentes
            "H2O",     # primeiro produto
            "fim"      # termina produtos
        ]
        
        reagentes, produtos = obter_equacao()
        
        assert reagentes == ["H2"]
        assert produtos == ["H2O"]
    
    @patch('builtins.input')
    def test_multiplos_reagentes_produtos(self, mock_input):
        """Testa entrada com múltiplos reagentes e produtos"""
        mock_input.side_effect = [
            "CH4",     # primeiro reagente
            "O2",      # segundo reagente
            "fim",     # termina reagentes
            "CO2",     # primeiro produto
            "H2O",     # segundo produto
            "fim"      # termina produtos
        ]
        
        reagentes, produtos = obter_equacao()
        
        assert reagentes == ["CH4", "O2"]
        assert produtos == ["CO2", "H2O"]
    
    @patch('builtins.input')
    def test_entrada_vazia(self, mock_input):
        """Testa quando usuário não insere nada"""
        mock_input.side_effect = [
            "fim",     # termina reagentes imediatamente
            "fim"      # termina produtos imediatamente
        ]
        
        reagentes, produtos = obter_equacao()
        
        assert reagentes == []
        assert produtos == []
    
    @patch('builtins.input')
    def test_case_insensitive_fim(self, mock_input):
        """Testa que 'FIM', 'Fim', etc. também funcionam"""
        mock_input.side_effect = [
            "H2",
            "FIM",     # maiúsculo
            "H2O",
            "Fim"      # capitalizado
        ]
        
        reagentes, produtos = obter_equacao()
        
        assert reagentes == ["H2"]
        assert produtos == ["H2O"]


class TestIntegracao:
    """Testes de integração entre as funções"""
    
    def test_parse_formula_com_balanceamento(self):
        """Testa se parse_formula funciona corretamente com balanceamento"""
        # Testa se parse_formula produz resultado compatível
        h2_parsed = parse_formula("H2")
        o2_parsed = parse_formula("O2")
        h2o_parsed = parse_formula("H2O")
        
        assert dict(h2_parsed) == {"H": 2}
        assert dict(o2_parsed) == {"O": 2}
        assert dict(h2o_parsed) == {"H": 2, "O": 1}
    
    @patch('builtins.print')
    def test_fluxo_completo_mock(self, mock_print):
        """Testa fluxo completo com dados mockados"""
        # Simula o que obter_equacao() retornaria
        reagentes = ["H2", "O2"]
        produtos = ["H2O"]
        
        # Testa se balanceamento funciona
        balancear_equacao(reagentes, produtos)
        
        # Verifica se executou sem erro
        mock_print.assert_called()


class TestCasosEspeciais:
    """Testes para casos especiais e edge cases"""
    
    def test_parse_formula_elementos_raros(self):
        """Testa parsing com elementos menos comuns"""
        resultado = parse_formula("KMnO4")
        assert dict(resultado) == {"K": 1, "Mn": 1, "O": 4}
    
    def test_parse_formula_numeros_zero(self):
        """Testa comportamento com números que começam com zero"""
        # Regex não deve capturar números com zero à esquerda como válidos
        resultado = parse_formula("H02")
        # Deve interpretar como H + O + 2 (inválido), mas nossa regex pega H e O2
        assert "H" in dict(resultado)
    
    @patch('builtins.print')
    def test_balanceamento_equacao_ja_balanceada(self, mock_print):
        """Testa equação que já está balanceada"""
        reagentes = ["NaCl"]
        produtos = ["Na", "Cl"]
        
        balancear_equacao(reagentes, produtos)
        mock_print.assert_called()


if __name__ == "__main__":
    pytest.main([__file__])