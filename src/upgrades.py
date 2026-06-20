UPGRADES_TORRE = [
    {
        "id": "dano",
        "nome": "Dano",
        "descricao": "Mais dano por clique",
        "atributo": "dano_ataque",
        "incremento": 5,
        "custo_base": 25,
        "custo_por_nivel": 20,
        "nivel_maximo": 8,
    },
    {
        "id": "raio",
        "nome": "Raio",
        "descricao": "Area maior do ataque",
        "atributo": "raio_ataque",
        "incremento": 5,
        "custo_base": 30,
        "custo_por_nivel": 25,
        "nivel_maximo": 6,
    },
    {
        "id": "vida",
        "nome": "Vida",
        "descricao": "Mais vida maxima",
        "atributo": "vida_maxima",
        "incremento": 25,
        "custo_base": 40,
        "custo_por_nivel": 35,
        "nivel_maximo": 5,
        "curar_ao_comprar": True,
    },
    {
        "id": "Combo",
        "nome": "Combo",
        "descricao": "Aumenta o bônus de dano por acertos seguidos",
        "atributo": "bonus_combo_por_acerto",
        "incremento": 0.05, 
        "custo_base": 2000,
        "custo_por_nivel": 0,
        "nivel_maximo": 1,
    },
]


def criar_niveis_torre():
    return {upgrade["id"]: 0 for upgrade in UPGRADES_TORRE}


def buscar_upgrade(id_upgrade):
    for upgrade in UPGRADES_TORRE:
        if upgrade["id"] == id_upgrade:
            return upgrade

    return None


def calcular_custo(upgrade, nivel_atual):
    return upgrade["custo_base"] + (upgrade["custo_por_nivel"] * nivel_atual)


def comprar_upgrade(torre, id_upgrade):
    upgrade = buscar_upgrade(id_upgrade)
    if upgrade is None:
        return False

    nivel_atual = torre.niveis_upgrades.get(id_upgrade, 0)
    if nivel_atual >= upgrade["nivel_maximo"]:
        return False

    custo = calcular_custo(upgrade, nivel_atual)
    if torre.dinheiro < custo:
        return False

    torre.dinheiro -= custo
    torre.niveis_upgrades[id_upgrade] = nivel_atual + 1

    atributo = upgrade["atributo"]
    valor_atual = getattr(torre, atributo)
    setattr(torre, atributo, valor_atual + upgrade["incremento"])

    if upgrade.get("curar_ao_comprar"):
        torre.vida = min(torre.vida + upgrade["incremento"], torre.vida_maxima)

    return True

def processar_ataque(torre, acertou_inimigo, inimigo_alvo=None):
    if acertou_inimigo:
        multiplicador = 1.0 + (torre.combo_atual * torre.bonus_combo_por_acerto)
        dano_final = round(torre.dano_ataque * multiplicador)
        torre.combo_atual += 1
        return dano_final
    else:
        torre.combo_atual = 0
        return 0