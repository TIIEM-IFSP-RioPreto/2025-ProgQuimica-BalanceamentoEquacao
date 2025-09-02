from dataclasses import dataclass
from typing import Dict, Optional, Union


@dataclass
class Elemento:
    """
    Representa um elemento químico com suas propriedades fundamentais.
    """
    numero_atomico: int
    simbolo: str
    nome: str
    massa_atomica: Optional[float]

    def __repr__(self) -> str:
        """Retorna uma representação textual amigável do objeto."""
        massa_str = f"{self.massa_atomica:.4f}" if self.massa_atomica is not None else "N/A"
        return (f"Elemento(Z={self.numero_atomico}, símbolo='{self.simbolo}', "
                f"nome='{self.nome}', massa_atomica={massa_str})")


# --- FASE DE INICIALIZAÇÃO E CARREGAMENTO ---
# Fonte: https://iupac.qmul.ac.uk/AtWt/
# Os dados brutos ainda são mantidos em uma estrutura simples.
# Obs:
# 1. Pesos atômicos são None onde não disponíveis.
# 2. Pesos entre colchetes ou com variação (intervalo) foram convertidos para
#    um valor convencional de uso comum
_dados_elementos_raw = [
    (1, 'H', 'Hidrogênio', 1.008000), (2, 'He', 'Hélio', 4.002602),
    (3, 'Li', 'Lítio', 6.940000), (4, 'Be', 'Berílio', 9.012183),
    (5, 'B', 'Boro', 10.810000), (6, 'C', 'Carbono', 12.011000),
    (7, 'N', 'Nitrogênio', 14.007000), (8, 'O', 'Oxigênio', 15.999000),
    (9, 'F', 'Flúor', 18.998403), (10, 'Ne', 'Neônio', 20.179700),
    (11, 'Na', 'Sódio', 22.989769), (12, 'Mg', 'Magnésio', 24.305000),
    (13, 'Al', 'Alumínio', 26.981538), (14, 'Si', 'Silício', 28.085000),
    (15, 'P', 'Fósforo', 30.973762), (16, 'S', 'Enxofre', 32.060000),
    (17, 'Cl', 'Cloro', 35.450000), (18, 'Ar', 'Argônio', 39.950000),
    (19, 'K', 'Potássio', 39.098300), (20, 'Ca', 'Cálcio', 40.078000),
    (21, 'Sc', 'Escândio', 44.955907), (22, 'Ti', 'Titânio', 47.867000),
    (23, 'V', 'Vanádio', 50.941500), (24, 'Cr', 'Cromo', 51.996100),
    (25, 'Mn', 'Manganês', 54.938043), (26, 'Fe', 'Ferro', 55.845000),
    (27, 'Co', 'Cobalto', 58.933194), (28, 'Ni', 'Níquel', 58.693400),
    (29, 'Cu', 'Cobre', 63.546000), (30, 'Zn', 'Zinco', 65.380000),
    (31, 'Ga', 'Gálio', 69.723000), (32, 'Ge', 'Germânio', 72.630800),
    (33, 'As', 'Arsênio', 74.921595), (34, 'Se', 'Selênio', 78.971800),
    (35, 'Br', 'Bromo', 79.904000), (36, 'Kr', 'Criptônio', 83.798000),
    (37, 'Rb', 'Rubídio', 85.467800), (38, 'Sr', 'Estrôncio', 87.620000),
    (39, 'Y', 'Ítrio', 88.905838), (40, 'Zr', 'Zircônio', 91.222000),
    (41, 'Nb', 'Nióbio', 92.906370), (42, 'Mo', 'Molibdênio', 95.950000),
    (43, 'Tc', 'Tecnécio', None), (44, 'Ru', 'Rutênio', 101.070000),
    (45, 'Rh', 'Ródio', 102.905490), (46, 'Pd', 'Paládio', 106.420000),
    (47, 'Ag', 'Prata', 107.868200), (48, 'Cd', 'Cádmio', 112.414000),
    (49, 'In', 'Índio', 114.818000), (50, 'Sn', 'Estanho', 118.710700),
    (51, 'Sb', 'Antimônio', 121.760000), (52, 'Te', 'Telúrio', 127.600000),
    (53, 'I', 'Iodo', 126.904470), (54, 'Xe', 'Xenônio', 131.293600),
    (55, 'Cs', 'Césio', 132.905452), (56, 'Ba', 'Bário', 137.327000),
    (57, 'La', 'Lantânio', 138.905477), (58, 'Ce', 'Cério', 140.116000),
    (59, 'Pr', 'Praseodímio', 140.907660), (60, 'Nd', 'Neodímio', 144.242000),
    (61, 'Pm', 'Promécio', None), (62, 'Sm', 'Samário', 150.360000),
    (63, 'Eu', 'Európio', 151.964000), (64, 'Gd', 'Gadolínio', 157.249000),
    (65, 'Tb', 'Térbio', 158.925354), (66, 'Dy', 'Disprósio', 162.500000),
    (67, 'Ho', 'Hólmio', 164.930329), (68, 'Er', 'Érbio', 167.259000),
    (69, 'Tm', 'Túlio', 168.934219), (70, 'Yb', 'Itérbio', 173.045000),
    (71, 'Lu', 'Lutécio', 174.966690), (72, 'Hf', 'Háfnio', 178.486000),
    (73, 'Ta', 'Tântalo', 180.947880), (74, 'W', 'Tungstênio', 183.840000),
    (75, 'Re', 'Rênio', 186.207000), (76, 'Os', 'Ósmio', 190.230000),
    (77, 'Ir', 'Irídio', 192.217000), (78, 'Pt', 'Platina', 195.084900),
    (79, 'Au', 'Ouro', 196.966570), (80, 'Hg', 'Mercúrio', 200.592000),
    (81, 'Tl', 'Tálio', 204.380000), (82, 'Pb', 'Chumbo', 207.200000),
    (83, 'Bi', 'Bismuto', 208.980400), (84, 'Po', 'Polônio', None),
    (85, 'At', 'Astato', None), (86, 'Rn', 'Radônio', None),
    (87, 'Fr', 'Frâncio', None), (88, 'Ra', 'Rádio', None),
    (89, 'Ac', 'Actínio', None), (90, 'Th', 'Tório', 232.037700),
    (91, 'Pa', 'Protactínio', 231.035880), (92, 'U', 'Urânio', 238.028910),
    (93, 'Np', 'Netúnio', None), (94, 'Pu', 'Plutônio', None),
    (95, 'Am', 'Amerício', None), (96, 'Cm', 'Cúrio', None),
    (97, 'Bk', 'Berquélio', None), (98, 'Cf', 'Califórnio', None),
    (99, 'Es', 'Einstênio', None), (100, 'Fm', 'Férmio', None),
    (101, 'Md', 'Mendelévio', None), (102, 'No', 'Nobélio', None),
    (103, 'Lr', 'Laurêncio', None), (104, 'Rf', 'Rutherfórdio', None),
    (105, 'Db', 'Dúbnio', None), (106, 'Sg', 'Seabórgio', None),
    (107, 'Bh', 'Bóhrio', None), (108, 'Hs', 'Hássio', None),
    (109, 'Mt', 'Meitnério', None), (110, 'Ds', 'Darmstádio', None),
    (111, 'Rg', 'Roentgênio', None), (112, 'Cn', 'Copernício', None),
    (113, 'Nh', 'Nihônio', None), (114, 'Fl', 'Fleróvio', None),
    (115, 'Mc', 'Moscóvio', None), (116, 'Lv', 'Livermório', None),
    (117, 'Ts', 'Tenessino', None), (118, 'Og', 'Oganessônio', None)
]

# Dicionários para busca rápida (O(1)).
# Estes são criados UMA VEZ quando o script é carregado.
_elementos_por_numero: Dict[int, Elemento] = {}
_elementos_por_simbolo: Dict[str, Elemento] = {}

# Loop de inicialização que popula os dicionários
for dados in _dados_elementos_raw:
    elemento = Elemento(
            numero_atomico=dados[0],
            simbolo=dados[1],
            nome=dados[2],
            massa_atomica=dados[3]
    )
    _elementos_por_numero[elemento.numero_atomico] = elemento
    _elementos_por_simbolo[elemento.simbolo] = elemento


def detalhes_elemento(identificador: Union[int, str]) -> Optional[Elemento]:
    """
    Busca e retorna os detalhes de um elemento químico de forma eficiente,
    usando dicionários pré-carregados.

    Args:
        identificador: O número atômico (int) ou o símbolo (str) do elemento.

    Returns:
        Uma instância da dataclass Elemento com os dados do elemento encontrado,
        ou None se o elemento não for encontrado.
    """
    if isinstance(identificador, int):
        return _elementos_por_numero.get(identificador)

    if isinstance(identificador, str):
        return _elementos_por_simbolo.get(identificador.capitalize())

    return None


def separar_elementos(formula: str) -> list[tuple[str, int]]:
    """
    Separa os elementos químicos de uma fórmula usando expressoes regulares.
    
    Args:
      formula: A fórmula química (Al2O3, CH4...) como uma string.
    
    Returns:
      Uma lista de tuplas, onde cada tupla contém o símbolo do elemento
      e sua quantidade ([("Al", 2), ("O", 3)], [("C", 1), ("H", 4)]...).
    """
    import re
    # A expressão regular encontra um padrão de:
    # 1. Uma letra maiúscula ([A-Z])
    # 2. Opcionalmente, uma letra minúscula ([a-z]?)
    # 3. Opcionalmente, um ou mais dígitos (\d*)
    padrao = r"([A-Z][a-z]?)(\d*)"

    # re.findall encontrará todas as correspondências do padrão na string
    matches = re.findall(padrao, formula)

    resultado = []
    for e, q in matches:
        # Se a quantidade for uma string vazia, significa que é 1
        if q == "":
            quantidade = 1
        else:
            # Converte a string de quantidade para um número inteiro
            quantidade = int(q)
        resultado.append((e, quantidade))

    return resultado
