# Desafio Automação Digital — Gestão de Peças, Qualidade e Armazenamento

## Visão geral
Projeto em Python que simula o controle de qualidade e armazenamento de peças produzidas por uma linha industrial. O sistema:
- Avalia automaticamente peças segundo critérios de qualidade;
- Armazena peças aprovadas em caixas com capacidade limitada;
- Mantém histórico, gera relatórios e exporta CSV.

## Critérios de Qualidade (implementados)
- Peso: **95g a 105g** (inclusivo)
- Cor: **"azul"** ou **"verde"** (case-insensitive)
- Comprimento: **10cm a 20cm** (inclusivo)

## Funcionalidades
- Cadastro de peça com avaliação automática
- Registro de motivos de reprovação
- Armazenamento em caixas (capacidade = 10 peças)
- Remoção de peça (retira do cadastro e de caixas, se presente)
- Geração de relatório final (console + `relatorio_final.csv`)
- Persistência em `data_store.json`
- Código modularizado com classes e fácil manutenção

## Como executar (passo-a-passo)
1. Clonar repositório ou baixar os arquivos (`main.py`, `README.md`, `data_store.json`).
2. Ter Python 3.8+ instalado.
3. No terminal, executar:
```bash
python main.py
```
4. Use o menu interativo para cadastrar e testar.

## Estrutura do repositório
- `main.py` — código fonte principal (CLI)
- `data_store.json` — arquivo de dados com persistência
- `relatorio_final.csv` — gerado ao pedir relatório
- `README.md` — este arquivo
- `documento_teorico.md` — documento teórico com explicações
- `roteiro_video.txt` — roteiro sugerido para o pitch

## Exemplo rápido (entrada / saída)
- Entrada:
  - Peso: `100`
  - Cor: `Azul`
  - Comprimento: `15`
- Saída esperada:
  - Peça aprovada e inserida na Caixa 1

## Como subir no GitHub (resumo)
```bash
git init
git add main.py README.md data_store.json documento_teorico.md roteiro_video.txt
git commit -m "Versão aprimorada - automação de peças"
git branch -M main
git remote add origin https://github.com/<seu-usuario>/desafio-automacao-pecas.git
git push -u origin main
```

## Observações e melhorias futuras
- Integrar com sensores (peso, câmera para cor, sensor de comprimento)
- API REST para cadastro remoto
- Interface web para visualização dos relatórios
- Testes unitários e CI/CD
