def carregar_pontos():
    with open("data/pontos.txt", "r") as arq:
        return int(arq.read().strip())

def salvar_pontos(quantidade):
    with open("data/pontos.txt", "w") as arq:
        arq.write(str(quantidade))