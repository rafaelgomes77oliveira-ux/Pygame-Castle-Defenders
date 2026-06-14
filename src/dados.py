def carregar_moedas():
    with open("data/moedas.txt", "r") as arq:
        return int(arq.read().strip())

def salvar_moedas(quantidade):
    with open("data/moedas.txt", "w") as arq:
        arq.write(str(quantidade))

def carregar_nivel():
    with open("data/nivel.txt", "r") as arq:
        return int(arq.read().strip())

def salvar_nivel(nivel):
    with open("data/nivel.txt", "w") as arq:
        arq.write(str(nivel))

def carregar_upgrades():
    upgrades_dict = {}
    with open("data/upgrades.txt", "r") as arq:
        for linha in arq:
            linha = linha.strip()
            if "=" in linha:
                chave, valor = linha.split("=", 1)
                try:
                    upgrades_dict[chave.strip()] = int(valor.strip())
                except ValueError:
                    pass
    return upgrades_dict

def salvar_upgrades(niveis_upgrades):
    with open("data/upgrades.txt", "w") as arq:
        for chave, valor in niveis_upgrades.items():
            arq.write(f"{chave}={valor}\n")