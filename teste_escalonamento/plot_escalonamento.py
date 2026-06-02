import os
import glob
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.family'] = 'DejaVu Sans'

# ─────────────────────────────────────────────
# CONFIGURAÇÕES
# ─────────────────────────────────────────────

PASTAS = {
    "resultados-default":    "Padrão",
    "resultados-roundrobin": "Round-Robin",
    "resultados-loteria":    "Loteria",
    "resultados-garantido":  "Garantido",
}

# Mapeamento: nome do arquivo → número de processos
ARQUIVO_PARA_NPROC = {
    "resultados_01.txt": 100,
    "resultados_02.txt": 10,
    "resultados_03.txt": 25,
    "resultados_04.txt": 50,
}

# Ordem desejada no eixo X
ORDEM_NPROC = [10, 25, 50, 100]


# ─────────────────────────────────────────────
# FUNÇÕES
# ─────────────────────────────────────────────

def parse_arquivo(caminho):
    """
    Lê um arquivo de resultados e retorna as médias de tempo
    para processos CPU-bound e IO-bound separadamente.

    Formato esperado de cada linha:
        CPU   3   0.05
        IO    4   6035.97
    """
    tempos_cpu = []
    tempos_io  = []

    with open(caminho, "r") as f:
        for linha in f:
            linha = linha.strip()
            if not linha:
                continue
            partes = linha.split()
            if len(partes) != 3:
                continue
            tipo, _proc, tempo = partes
            try:
                t = float(tempo)
            except ValueError:
                continue

            if tipo.upper() == "CPU":
                tempos_cpu.append(t)
            elif tipo.upper() == "IO":
                tempos_io.append(t)

    media_cpu = np.mean(tempos_cpu) if tempos_cpu else 0.0
    media_io  = np.mean(tempos_io)  if tempos_io  else 0.0

    return media_cpu, media_io


def coletar_dados():
    """
    Percorre cada pasta/algoritmo e cada arquivo/cenário,
    retornando dicionários indexados por [algoritmo][nproc].
    """
    dados_cpu = {label: {} for label in PASTAS.values()}
    dados_io  = {label: {} for label in PASTAS.values()}

    for pasta, label in PASTAS.items():
        if not os.path.isdir(pasta):
            print(f"  [AVISO] Pasta não encontrada: '{pasta}' — pulando.")
            continue

        for arquivo, nproc in ARQUIVO_PARA_NPROC.items():
            caminho = os.path.join(pasta, arquivo)
            if not os.path.isfile(caminho):
                print(f"  [AVISO] Arquivo não encontrado: '{caminho}' — pulando.")
                dados_cpu[label][nproc] = 0.0
                dados_io[label][nproc]  = 0.0
                continue

            media_cpu, media_io = parse_arquivo(caminho)
            dados_cpu[label][nproc] = media_cpu
            dados_io[label][nproc]  = media_io
            print(f"  {label:15s} | {nproc:4d} processos | "
                  f"CPU média: {media_cpu:.4f}s | IO média: {media_io:.4f}s")

    return dados_cpu, dados_io


def plotar_graficos(dados_cpu, dados_io):
    """
    Gera dois gráficos de barras lado a lado:
    - Esquerda: tempos médios CPU-bound
    - Direita:  tempos médios IO-bound
    """
    algoritmos  = list(PASTAS.values())
    n_algos     = len(algoritmos)
    n_cenarios  = len(ORDEM_NPROC)

    x           = np.arange(n_cenarios)
    largura     = 0.18
    offsets     = np.linspace(-(n_algos - 1) / 2, (n_algos - 1) / 2, n_algos) * largura

    cores = ["#4878CF", "#F89A2A", "#6ABF69", "#D9534F"]

    fig, (ax_cpu, ax_io) = plt.subplots(1, 2, figsize=(13, 5))

    for i, (label, cor) in enumerate(zip(algoritmos, cores)):
        valores_cpu = [dados_cpu[label].get(n, 0.0) for n in ORDEM_NPROC]
        valores_io  = [dados_io[label].get(n, 0.0)  for n in ORDEM_NPROC]

        ax_cpu.bar(x + offsets[i], valores_cpu, largura, label=label, color=cor)
        ax_io.bar( x + offsets[i], valores_io,  largura, label=label, color=cor)

    # ── Eixo CPU ──
    ax_cpu.set_title("Processos CPU-bound", fontsize=13)
    ax_cpu.set_xlabel("Número de processos", fontsize=11)
    ax_cpu.set_ylabel("Tempo médio (s)", fontsize=11)
    ax_cpu.set_xticks(x)
    ax_cpu.set_xticklabels([str(n) for n in ORDEM_NPROC])
    ax_cpu.legend(fontsize=9)
    ax_cpu.grid(axis="y", linestyle="--", alpha=0.5)
    ax_cpu.set_axisbelow(True)

    # ── Eixo IO ──
    ax_io.set_title("Processos IO-bound", fontsize=13)
    ax_io.set_xlabel("Número de processos", fontsize=11)
    ax_io.set_ylabel("Tempo médio (s)", fontsize=11)
    ax_io.set_xticks(x)
    ax_io.set_xticklabels([str(n) for n in ORDEM_NPROC])
    ax_io.legend(fontsize=9)
    ax_io.grid(axis="y", linestyle="--", alpha=0.5)
    ax_io.set_axisbelow(True)

    plt.tight_layout()
    plt.savefig("grafico_escalonamento.png", dpi=150, bbox_inches="tight")
    print("\nGráfico salvo em: grafico_escalonamento.png")
    plt.show()


# ─────────────────────────────────────────────
# EXECUÇÃO
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Coletando dados ===\n")
    dados_cpu, dados_io = coletar_dados()
    print("\n=== Gerando gráficos ===\n")
    plotar_graficos(dados_cpu, dados_io)
