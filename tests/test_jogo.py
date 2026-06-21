import pytest
from src import funcoes
from src import upgrades

def test_formatar_tempo_minutos_exatos():
    assert funcoes.formatar_tempo(0) == "00:00"
    assert funcoes.formatar_tempo(120) == "02:00"

def test_formatar_tempo_segundos_quebrados():
    assert funcoes.formatar_tempo(45) == "00:45"
    assert funcoes.formatar_tempo(125) == "02:05"

def test_calcular_intervalo_spawn_dificuldade_inicial():
    assert funcoes.calcular_intervalo_spawn(1) == 800

def test_calcular_intervalo_spawn_dificuldade_media():
    assert funcoes.calcular_intervalo_spawn(3) == 660

def test_calcular_intervalo_spawn_limite_minimo():
    assert funcoes.calcular_intervalo_spawn(20) == 300

def test_criar_niveis_torre():
    niveis = upgrades.criar_niveis_torre()

    assert isinstance(niveis, dict)
    assert "dano" in niveis
    assert niveis["dano"] == 0
    assert "vida" in niveis
    assert niveis["vida"] == 0

def test_buscar_upgrade_sucesso():
    upgrade = upgrades.buscar_upgrade("raio")

    assert upgrade is not None
    assert upgrade["nome"] == "Raio"
    assert upgrade["atributo"] == "raio_ataque"

def test_buscar_upgrade_falha():
    upgrade = upgrades.buscar_upgrade("upgrade_fantasma")

    assert upgrade is None

def test_calcular_custo_nivel_zero():
    upgrade_teste = {
        "custo_base": 50,
        "custo_por_nivel": 15
    }
    assert upgrades.calcular_custo(upgrade_teste, 0) == 50

def test_calcular_custo_nivel_avancado():
    upgrade_teste = {
        "custo_base": 50,
        "custo_por_nivel": 15
    }
    assert upgrades.calcular_custo(upgrade_teste, 4) == 110