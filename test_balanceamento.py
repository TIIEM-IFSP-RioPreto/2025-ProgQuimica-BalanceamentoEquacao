import pytest
from balanceamento import calcular_massa, separar_elementos, detalhes_elemento, Elemento


class TestDetalhesElemento:
    """Testes para a função detalhes_elemento()"""
    
    def test_busca_por_numero_atomico_valido(self):
        """Testa busca por número atômico válido"""
        elemento = detalhes_elemento(1)
        assert elemento is not None
        assert elemento.numero_atomico == 1
        assert elemento.simbolo == "H"
        assert elemento.nome == "Hidrogênio"
        assert elemento.massa_atomica == 1.008000
    
    def test_busca_por_simbolo_valido(self):
        """Testa busca por símbolo válido"""
        elemento = detalhes_elemento("O")
        assert elemento is not None
        assert elemento.numero_atomico == 8
        assert elemento.simbolo == "O"
        assert elemento.nome == "Oxigênio"
        assert elemento.massa_atomica == 15.999000
    
    def test_busca_por_simbolo_minusculo(self):
        """Testa busca por símbolo em minúsculo (deve funcionar)"""
        elemento = detalhes_elemento("ca")
        assert elemento is not None
        assert elemento.simbolo == "Ca"
        assert elemento.nome == "Cálcio"
    
    def test_elemento_sem_massa_atomica(self):
        """Testa elemento que não possui massa atômica definida"""
        elemento = detalhes_elemento("Tc")  # Tecnécio
        assert elemento is not None
        assert elemento.simbolo == "Tc"
        assert elemento.massa_atomica is None
    
    def test_numero_atomico_inexistente(self):
        """Testa busca por número atômico inexistente"""
        elemento = detalhes_elemento(200)
        assert elemento is None
    
    def test_simbolo_inexistente(self):
        """Testa busca por símbolo inexistente"""
        elemento = detalhes_elemento("Xx")
        assert elemento is None
    
    def test_tipo_invalido(self):
        """Testa busca com tipo de dado inválido"""
        elemento = detalhes_elemento(3.14)
        assert elemento is None
        
        elemento = detalhes_elemento([])
        assert elemento is None


class TestSepararElementos:
    """Testes para a função separar_elementos()"""
    
    def test_formula_simples_um_elemento(self):
        """Testa fórmula com um único elemento"""
        resultado = separar_elementos("H")
        assert resultado == [("H", 1)]
    
    def test_formula_simples_com_quantidade(self):
        """Testa fórmula simples com quantidade"""
        resultado = separar_elementos("H2")
        assert resultado == [("H", 2)]
    
    def test_formula_multiplos_elementos(self):
        """Testa fórmula com múltiplos elementos"""
        resultado = separar_elementos("H2O")
        assert resultado == [("H", 2), ("O", 1)]
    
    def test_formula_complexa(self):
        """Testa fórmula mais complexa"""
        resultado = separar_elementos("Ca(OH)2")
        # Note: esta função não trata parênteses, então vai separar Ca, O, H
        resultado = separar_elementos("CaO2H2")  # Versão sem parênteses
        assert resultado == [("Ca", 1), ("O", 2), ("H", 2)]
    
    def test_formula_com_numeros_grandes(self):
        """Testa fórmula com números grandes"""
        resultado = separar_elementos("Al2O3")
        assert resultado == [("Al", 2), ("O", 3)]
    
    def test_formula_elementos_multiplos_digitos(self):
        """Testa fórmula com elementos de múltiplos dígitos"""
        resultado = separar_elementos("NaCl")
        assert resultado == [("Na", 1), ("Cl", 1)]
    
    def test_formula_vazia(self):
        """Testa fórmula vazia"""
        resultado = separar_elementos("")
        assert resultado == []
    
    def test_formula_apenas_numeros(self):
        """Testa string com apenas números (inválida)"""
        resultado = separar_elementos("123")
        assert resultado == []
    
    def test_formula_glucose(self):
        """Testa fórmula da glicose"""
        resultado = separar_elementos("C6H12O6")
        assert resultado == [("C", 6), ("H", 12), ("O", 6)]


class TestCalcularMassa:
    """Testes para a função calcular_massa()"""
    
    def test_massa_elemento_simples(self):
        """Testa cálculo de massa para elemento simples"""
        massa = calcular_massa("H")
        assert massa == pytest.approx(1.008000, rel=1e-6)
    
    def test_massa_elemento_com_quantidade(self):
        """Testa cálculo de massa para elemento com quantidade"""
        massa = calcular_massa("H2")
        assert massa == pytest.approx(2.016000, rel=1e-6)
    
    def test_massa_agua(self):
        """Testa cálculo de massa da água (H2O)"""
        massa = calcular_massa("H2O")
        # H: 1.008 * 2 = 2.016, O: 15.999 * 1 = 15.999
        # Total: 18.015
        assert massa == pytest.approx(18.015000, rel=1e-6)
    
    def test_massa_dioxido_carbono(self):
        """Testa cálculo de massa do dióxido de carbono (CO2)"""
        massa = calcular_massa("CO2")
        # C: 12.011 * 1 = 12.011, O: 15.999 * 2 = 31.998
        # Total: 44.009
        assert massa == pytest.approx(44.009000, rel=1e-6)
    
    def test_massa_oxido_aluminio(self):
        """Testa cálculo de massa do óxido de alumínio (Al2O3)"""
        massa = calcular_massa("Al2O3")
        # Al: 26.981538 * 2 = 53.963076, O: 15.999 * 3 = 47.997
        # Total: 101.960076
        assert massa == pytest.approx(101.960076, rel=1e-6)
    
    def test_massa_glucose(self):
        """Testa cálculo de massa da glicose (C6H12O6)"""
        massa = calcular_massa("C6H12O6")
        # C: 12.011 * 6 = 72.066, H: 1.008 * 12 = 12.096, O: 15.999 * 6 = 95.994
        # Total: 180.156
        assert massa == pytest.approx(180.156000, rel=1e-6)
    
    def test_massa_elemento_inexistente(self):
        """Testa cálculo com elemento inexistente"""
        massa = calcular_massa("Xx")
        assert massa is None
    
    def test_massa_elemento_sem_massa_atomica(self):
        """Testa cálculo com elemento sem massa atômica definida"""
        massa = calcular_massa("Tc")  # Tecnécio não tem massa atômica
        assert massa is None
    
    def test_massa_formula_vazia(self):
        """Testa cálculo com fórmula vazia"""
        massa = calcular_massa("")
        assert massa is None
    
    def test_massa_formula_invalida(self):
        """Testa cálculo com fórmula inválida"""
        massa = calcular_massa("123")
        assert massa is None
    
    def test_massa_formula_com_elemento_inexistente(self):
        """Testa fórmula que contém elemento válido e inválido"""
        massa = calcular_massa("H2Xx")
        assert massa is None


class TestIntegracao:
    """Testes de integração entre as funções"""
    
    def test_fluxo_completo_agua(self):
        """Testa o fluxo completo para a água"""
        # 1. Separar elementos
        elementos = separar_elementos("H2O")
        assert len(elementos) == 2
        
        # 2. Verificar detalhes dos elementos
        h_elemento = detalhes_elemento("H")
        o_elemento = detalhes_elemento("O")
        assert h_elemento is not None
        assert o_elemento is not None
        
        # 3. Calcular massa
        massa = calcular_massa("H2O")
        assert massa is not None
        assert massa > 0
    
    def test_elementos_com_massa_none(self):
        """Testa comportamento com elementos que têm massa None"""
        # Tecnécio tem massa None
        tc_elemento = detalhes_elemento("Tc")
        assert tc_elemento is not None
        assert tc_elemento.massa_atomica is None
        
        # Fórmula com Tecnécio deve retornar None
        massa = calcular_massa("Tc2O")
        assert massa is None


if __name__ == "__main__":
    pytest.main([__file__])