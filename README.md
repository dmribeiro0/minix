# Projeto de Sistemas Operacionais – Modificações no Kernel do Minix

Este repositório contém o desenvolvimento do projeto final da disciplina de **Sistemas Operacionais**, no qual são realizadas modificações e extensões no kernel do sistema operacional **Minix**.

O trabalho está sendo desenvolvido pelos alunos como parte das atividades acadêmicas da **Universidade Federal de São Paulo (UNIFESP)**, sob orientação do **Prof. Dr. Joahannes Bruno Dias da Costa**.

## Alunos
* Camila F. Lima
* Daniel M. Ribeiro
* Henrique R. Ribeiro
* João Vitor M. Gomes
* Lael K. Hayashi
* Lucas A. Gazale

## Sobre o Repositório

Este repositório é uma **cópia (fork)** do repositório original do Minix 3 utilizada para o desenvolvimento do projeto final da disciplina de Sistemas Operacionais.

As modificações realizadas concentram-se na implementação e avaliação de diferentes políticas de escalonamento de processos. Para facilitar a organização e comparação entre as soluções desenvolvidas, cada algoritmo foi implementado em uma branch independente:

- `algoritmo/round-robin`
- `algoritmo/loteria`
- `algoritmo/garantido`

Cada branch contém uma implementação completa e funcional do respectivo algoritmo de escalonamento, permitindo sua execução e análise de forma isolada.

## Algoritmos Implementados

### Round Robin (`algoritmo/round-robin`)

Implementado por meio de alterações no servidor de escalonamento (`servers/sched/schedule.c`), removendo os mecanismos de ajuste dinâmico de prioridade para processos de usuário. Dessa forma, todos os processos permanecem na mesma fila de prioridade e são executados em rodízio circular utilizando quanta de tempo iguais.

### Escalonamento por Loteria (`algoritmo/loteria`)

Implementado no kernel por meio de modificações em `kernel/proc.h` e `kernel/proc.c`. Cada processo recebe uma quantidade de bilhetes e, a cada decisão de escalonamento, é realizado um sorteio para determinar qual processo receberá a CPU. Processos com mais bilhetes possuem maior probabilidade de serem selecionados.

### Escalonamento Garantido (`algoritmo/garantido`)

Implementado através de modificações no kernel e no servidor de escalonamento. O algoritmo monitora o tempo de CPU efetivamente recebido por cada processo e compara esse valor com a parcela de CPU que deveria ter recebido. A CPU é sempre atribuída ao processo mais prejudicado, buscando garantir uma distribuição justa do tempo de processamento.

## Objetivo

O principal objetivo deste projeto é proporcionar uma compreensão aprofundada do funcionamento interno de um sistema operacional, por meio da análise e modificação direta de seu código-fonte.

## Observações

* Este repositório é destinado exclusivamente a fins acadêmicos.
* As modificações realizadas podem não refletir boas práticas de produção, uma vez que o foco está no aprendizado e experimentação.
