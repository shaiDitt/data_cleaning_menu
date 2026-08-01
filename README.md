# Programa de Limpeza e Gestão de Dados — Netflix Titles

Programa em Python, executado via terminal, para limpeza, tratamento e edição de dados do dataset **Netflix Titles**, utilizando a biblioteca `pandas`.

## 👥 Autoras

- **Ana Larissa Souto**: [@allimasouto](https://github.com/allimasouto)
- **Laura Carvalho**: [...]
- **Letícia Alexandre**: [@leticia-alexandre](https://github.com/leticia-alexandre)
- **Shaini Dittberner**: [@shaiDitt](https://github.com/shaiDitt)

## 🎯 Objetivo

Facilitar tarefas comuns de um analista de dados júnior — tratar valores em falta, remover duplicados, consultar e editar registos — através de um menu interativo no terminal.

## 📁 Arquivos necessários

Para rodar o programa, é preciso ter na mesma pasta:

- O script principal (`menu_limpeza_netflix.py`)
- O ficheiro `netflix_titles_modificado.csv` (disponibilizado neste repositório)

> ⚠️ O ficheiro `netflix_titles_modificado.csv` foi criado a partir do dataset original (`netflix_titles.csv`), com duplicados e valores em falta inseridos propositalmente, para permitir testar as funcionalidades de limpeza do menu. O ficheiro já está disponibilizado neste repositório, portanto não é necessário gerá-lo.

O notebook `modulo1_refinado02.ipynb` também está incluído, mas é opcional — serve apenas para documentar a análise exploratória do dataset original e as modificações feitas que deu origem ao ficheiro `netflix_titles_modificado.csv`.

## 🔧 Requisitos / Instalação

- Python 3.x
- Bibliotecas:
```bash
  pip install pandas tabulate
```
  (`matplotlib` e `seaborn` são necessárias apenas se quiser executar o notebook do Módulo 1)

## ▶️ Como executar

```bash
python gestao_dados_netflix.py
```

O programa apresenta um menu principal com 3 módulos (Análise de Dados, Limpeza e Tratamento de Dados, e Gestão do Ficheiro). Ao sair (opção 4), as alterações são salvas em `netflix_titles_modificado.csv` e um histórico das operações é gerado em `historico_operacoes.txt`.

## ⚙️ Funcionalidades

- **Módulo 1** — Análise exploratória dos dados (notebook)
- **Módulo 2** — Limpeza e tratamento de dados (valores em falta, duplicados, colunas)
- **Módulo 3** — Consulta e edição de registos (Excel)

## 💾 Saída gerada

| Ficheiro | Origem | Descrição |
|---|---|---|
| `netflix_titles_modificado.csv` | Já disponibilizado no repositório, mas gerado na execução do `modulo1_refinado02.ipynb`; depois sobrescrito ao salvar alterações no menu | Dataset de testes/atualizado com as alterações feitas |
| `historico_operacoes.txt` | Script principal | Registo de todas as operações realizadas durante a sessão |
| `cabecalhos.xlsx` | Script principal (Módulo 3) | Template gerado ao usar a opção de inserção em lote |

