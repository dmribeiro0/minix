import os
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

# Mapeamento: prefixo do arquivo → número de processos
PREFIXO_PARA_NPROC = {
    "resultados_01": 100,
    "resultados_02": 10,
    "resultados_03": 25,
    "resultados_04": 50,
}

EXECUCOES = [1, 2, 3]

# Ordem desejada no eixo X
ORDEM_NPROC = [10, 25, 50, 100]


# ─────────────────────────────────────────────
# FUNÇÕES
# ─────────────────────────────────────────────

def parse_arquivo(caminho):
    """
    Lê um arquivo e retorna a média de tempo de CPU e IO separadamente.
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
    Para cada algoritmo e cenário, lê as 3 execuções separadamente,
    guarda a média de cada execução e calcula:
      - média geral (das 3 médias)
      - desvio padrão (entre as 3 médias)
    """
    # Estrutura: dados[label][nproc] = (media, desvio)
    dados_cpu = {label: {} for label in PASTAS.values()}
    dados_io  = {label: {} for label in PASTAS.values()}

    for pasta, label in PASTAS.items():
        if not os.path.isdir(pasta):
            print(f"  [AVISO] Pasta não encontrada: '{pasta}' — pulando.")
            for nproc in ORDEM_NPROC:
                dados_cpu[label][nproc] = (0.0, 0.0)
                dados_io[label][nproc]  = (0.0, 0.0)
            continue

        for prefixo, nproc in PREFIXO_PARA_NPROC.items():
            medias_cpu_exec = []  # média de CPU de cada execução
            medias_io_exec  = []  # média de IO  de cada execução

            for exec_num in EXECUCOES:
                nome    = f"{prefixo}_{exec_num}.txt"
                caminho = os.path.join(pasta, nome)

                if not os.path.isfile(caminho):
                    print(f"  [AVISO] Arquivo não encontrado: '{caminho}' — pulando.")
                    continue

                media_cpu, media_io = parse_arquivo(caminho)
                medias_cpu_exec.append(media_cpu)
                medias_io_exec.append(media_io)

            # Média e desvio padrão entre as execuções
            if medias_cpu_exec:
                media_cpu_final = np.mean(medias_cpu_exec)
                std_cpu         = np.std(medias_cpu_exec, ddof=1) if len(medias_cpu_exec) > 1 else 0.0
            else:
                media_cpu_final, std_cpu = 0.0, 0.0

            if medias_io_exec:
                media_io_final = np.mean(medias_io_exec)
                std_io         = np.std(medias_io_exec, ddof=1) if len(medias_io_exec) > 1 else 0.0
            else:
                media_io_final, std_io = 0.0, 0.0

            dados_cpu[label][nproc] = (media_cpu_final, std_cpu)
            dados_io[label][nproc]  = (media_io_final,  std_io)

            print(f"  {label:15s} | {nproc:4d} proc | "
                  f"CPU: {media_cpu_final:.4f}s ± {std_cpu:.4f}s | "
                  f"IO: {media_io_final:.4f}s ± {std_io:.4f}s "
                  f"({len(medias_cpu_exec)} execuções)")

    return dados_cpu, dados_io


def plotar_graficos(dados_cpu, dados_io):
    """
    Gera dois gráficos de barras lado a lado com barras de erro
    representando o desvio padrão entre as 3 execuções.
    """
    algoritmos = list(PASTAS.values())
    n_algos    = len(algoritmos)
    n_cenarios = len(ORDEM_NPROC)

    x       = np.arange(n_cenarios)
    largura = 0.18
    offsets = np.linspace(-(n_algos - 1) / 2, (n_algos - 1) / 2, n_algos) * largura

    cores = ["#4878CF", "#F89A2A", "#6ABF69", "#D9534F"]

    fig, (ax_cpu, ax_io) = plt.subplots(1, 2, figsize=(13, 5))

    for i, (label, cor) in enumerate(zip(algoritmos, cores)):
        valores_cpu = [dados_cpu[label].get(n, (0.0, 0.0))[0] for n in ORDEM_NPROC]
        erros_cpu   = [dados_cpu[label].get(n, (0.0, 0.0))[1] for n in ORDEM_NPROC]
        valores_io  = [dados_io[label].get(n,  (0.0, 0.0))[0] for n in ORDEM_NPROC]
        erros_io    = [dados_io[label].get(n,  (0.0, 0.0))[1] for n in ORDEM_NPROC]

        erro_kw = dict(elinewidth=1.2, ecolor="black", capsize=4, capthick=1.2)

        ax_cpu.bar(x + offsets[i], valores_cpu, largura,
                   label=label, color=cor,
                   yerr=erros_cpu, error_kw=erro_kw)

        ax_io.bar(x + offsets[i], valores_io, largura,
                  label=label, color=cor,
                  yerr=erros_io, error_kw=erro_kw)

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
