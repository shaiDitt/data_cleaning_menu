import os
import random
from datetime import datetime

import pandas as pd
from tabulate import tabulate


def clean():
    if os.name == "nt":
        os.system('cls')
    else:
        os.system("clear")


def prima_enter():
    input("Prima ENTER para continuar")

def ler_int(mensagem):
    while True:
        entrada = input(mensagem)
        try:
            return int(entrada)
        except:
            print("Inválido.")
 
def ler_float(mensagem):
    while True:
        entrada = input(mensagem)
        try:
            return float(entrada)
        except:
            print("Inválido.")

def ler_string(mensagem):
    return input(mensagem)


# FUNÇÕES DO MENU #

##################################################################################################################################################
# EM FALTA - MODULO 2

def mostrar_valores_em_falta(df):
    percentagem = (df.isnull().sum() / len(df)) * 100

    print("## Percentagem de valores em falta por coluna ##")
    for c, l in percentagem.round(2).items():
        print(f"{c}: {l}%")

def remover_linhas_vazias(df, coluna):
    if coluna not in df.columns:
        print("Erro: A coluna não existe no DataFrame ou não tem números em falta.")
        return df
   
    linhas_vazias = df[coluna].isnull().sum()

    if linhas_vazias == 0:
        print("Não há linhas vazias nessa coluna.")
    else:
        df = df.dropna(subset = coluna)
        print(f"Foram removidas {linhas_vazias } linhas da coluna [{coluna}]")
   
 
def preencher_media_mediana(df, coluna):

    if df[coluna].dtype not in ["int64", "float64"]:
        print(56 * "-")
        print("Essa opção só pode ser usada em colunas numéricas. Retorne ao menu inicial")
        print(56 * "-")
        prima_enter()
 
    else:
        print("[1] - Preencher com a média")
        print("[2] - Preencher com a mediana")

        escolha = ler_string("Escolhe uma opção: ")

        if escolha == "1":
            valor = df[coluna].mean()
        elif escolha == "2":
            valor = df[coluna].median()
        else:
            print("Opção inválida.")
            return df

        df[coluna] = df[coluna].fillna(valor)
        print(f"OS valores vazios da coluna '{coluna}' foram preenchidos com: {valor:.0f}")


def preencher_linha_valor_fixo(df, coluna, valor_fixo):
    linhas_nulas = df[coluna].isna().sum()

    if linhas_nulas == 0:
        print("Não há linhas vazias. Confira a tabela a seguir.")
        return df

    df.loc[df[coluna].isna(), coluna] = valor_fixo
 
    print(f"Foram preenchidas {linhas_nulas} linhas totalmente vazias da coluna {coluna} com o valor {valor_fixo}.")
 
    return df

def ver_duplicados(df):
    ver_duplicados = df.duplicated().sum()
    print(f"O número de informações duplicadas é: {ver_duplicados}")

##################################################################################################################################################
# EM FALTA - MENU - MODULO 2

def menu_ver_linhas_em_falta():
    print("\n===== Visualizar e editar valores em falta ===== ")     
    print( 56 * "-")
    mostrar_valores_em_falta(df)
    print( 56 * "-")  
    print("[1] - Remover linhas vazias de uma coluna específica")
    print("[2] - Preencher linhas vazias com valor fixo")
    print("[3] - Preencher com a média ou mediana")
    print("[4] - Voltar ao menu principal.")

    print( 56 * "-")
    opcao = ler_int("Escolhe uma opção: ")

    if opcao == 1: 
        x = ler_string("De qual coluna você quer remover as linhas vazias? ").lower()
        remover_linhas_vazias(df, x)
        prima_enter()

    elif opcao == 2:
        y = ler_string("De qual coluna você quer substituir as linhas vazias? ").lower().strip()
        if y == "release_year":
            x = ler_float("Qual o valor fixo que você deseja substituir nas linhas vazias? ")
        else:
            x = ler_string("Qual o valor fixo que você deseja substituir nas linhas vazias? ").lower()
        preencher_linha_valor_fixo(df, y, x)
        prima_enter()

    elif opcao == 3:
        x = ler_string("Qual coluna você gostaria de preencher? ").lower()
        preencher_media_mediana(df, x)
        prima_enter()

    elif opcao == 4:
            print("Volte ao menu!")
            prima_enter()
    else:
        print("Opção Inválida!")

##################################################################################################################################################
# DUPLICADOS - MODULO 2

def visualizar_editar_linhas_duplicadas_menu():
    while True:
        print("\n===== Visualizar e editar linhas duplicadas =====")
        print( 56 * "-")
        ver_duplicados(df)
        print( 56 * "-")  
        print("[1] - Remover todas as duplicadas de uma vez")
        print("[2] - Analisar e remover UMA A UMA manualmente")
        print("[3] - Voltar ao menu principal")

        opcao = ler_int("Escolhe uma opção: ")

        if opcao == 1:
            menu_remover_todas_linhas_duplicadas()
        elif opcao == 2:
            remover_linha_linha_duplicada()
        elif opcao == 3:
            clean()
            break
        else: 
            print("Opção inválida!")

def menu_remover_todas_linhas_duplicadas():
    clean()
    print("\n===== As linhas duplicadas são =====")
    print(56 * "-")
    print(df[df.duplicated()])
    print(56 * "-")
    quer_remover = ler_string("Tem certeza que deseja remover todas as linhas duplicações? S ou N \n")
    if quer_remover.upper() == "S":
        remover_todas_linhas_duplicadas()
    else:
        print("Nenhuma linha duplicada será removida!")

def remover_todas_linhas_duplicadas():
    print("\n===== Inicio da remoção das linhas duplicadas =====")
    linhas_antes = len(df)
    df.drop_duplicates(subset=['show_id'], keep='first', inplace=True)
    linhas_depois = len(df)
    linhas_removidas = linhas_antes - linhas_depois
    # Todas as operações devem ser salvas para o ficheiro TXT de ações realizadas
    salvar_operacao_realizada("Remoção de todas as linhas duplicadas", linhas_removidas)
    print(f"Foram removidas {linhas_removidas} linhas duplicadas.")

def remover_linha_linha_duplicada():
    linhas_removidas = 0
    df_analise = df[df.duplicated(subset=['show_id'], keep=False)]
    
    ids_duplicados = df_analise['show_id'].unique()

    for show_id in ids_duplicados:
        
        ocorrencias = df[df['show_id'] == show_id]
        print(f"\n--- Analisando o SHOW_ID: {show_id} (Encontradas {len(ocorrencias)} cópias) ---")
        print(ocorrencias)
        
        decisao = input("Deseja apagar as cópias deste ID e manter apenas a primeira? (S/N): ").lower()
        if decisao == 's':
            quantidade_copias = len(ocorrencias) - 1
            
            indices_para_apagar = ocorrencias.index[1:]
            
            df.drop(indices_para_apagar, inplace=True)
            linhas_removidas += quantidade_copias
            print(f"{quantidade_copias} cópias removidas para o ID {show_id}.")
        else:
            print(f"Mantidas todas as linhas para o ID {show_id}.")
    salvar_operacao_realizada("Remoção linhas duplicadas", linhas_removidas)  
    return linhas_removidas


def remover_linhas_duplicadas():
    print("\n===== Inicio da remoção das linhas duplicadas =====")
    linhas_antes = len(df)
    df.drop_duplicates(subset=['show_id'], keep='first', inplace=True)
    linhas_depois = len(df)
    linhas_removidas = linhas_antes - linhas_depois
    # Todas as operações devem ser salvas para o ficheiro TXT de ações realizadas
    salvar_operacao_realizada("Remoção de linhas duplicadas", linhas_removidas)
    print(f"Foram removidas {linhas_removidas} linhas duplicadas.")

##################################################################################################################################################
# EXTRA - MODULO 2

def ver_colunas():
    print("========================================")
    print(f"========= Visualizando Colunas =========")
    print("========================================")
    colunas = list(df.columns)
    for i, nome_coluna in enumerate(colunas, start=1):
       print(f"[{i}] - {nome_coluna}")
def ver_colunas_atualizadas():
    print("========================================")
    print("===== Colunas atualizadas =====")
    print("========================================")
    for i, nome_coluna in enumerate(df.columns, start=1):
        print(f"[{i}] - {nome_coluna}")

def editar_colunas():
    ver_colunas()

    colunas = list(df.columns)
    escolha = ler_int("Escolha o número da coluna que deseja editar (0 para cancelar): ")

    if escolha == 0:
        print("Operação cancelada.")
        return df

    elif escolha < 1 or escolha > len(colunas):
        print("Opção inválida.")
        return df

    coluna_escolhida = colunas[escolha - 1]
    nome_novo = ler_string(f"Novo nome para a coluna [{coluna_escolhida}]: ")
    
    df.rename(columns={coluna_escolhida :nome_novo}, inplace=True)

    print(f"A coluna [{coluna_escolhida}] foi renomeada para [{nome_novo}]]")
    ver_colunas_atualizadas()
    prima_enter()



def remover_espacos():
    ver_colunas()

    
    colunas = list(df.columns)
    escolha = ler_int("Escolha o número da coluna que deseja remover espaços (0 para cancelar): ")

    if escolha == 0:
        print("Operação cancelada.")
        return df

    if escolha < 1 or escolha > len(colunas):
        print("Opção inválida.")
        return df
    coluna_escolhida = colunas[escolha - 1]
    confirmar = input(f"Tem certeza que deseja remover os espaços da coluna '{coluna_escolhida}'? (s/n): ").lower()

    if confirmar == "s":
        df[coluna_escolhida] = df[coluna_escolhida].str.replace(' ', '', regex=False)
        print(f"=========== Visualizando {coluna_escolhida}===========")
        for i in df[coluna_escolhida].head(10):
            print(i)
        prima_enter()
    else:
        print("Operação cancelada.")

def excluir_coluna(df):
   ver_colunas()

   colunas = list(df.columns)
   escolha = ler_int("Escolha o número da coluna que deseja excluir (0 para cancelar): ")

   if escolha == 0:
       print("Operação cancelada.")
       return df

   if escolha < 1 or escolha > len(colunas):
       print("Opção inválida.")
       return df
   coluna_escolhida = colunas[escolha - 1]
   confirmar = input(f"Tem certeza que deseja excluir a coluna '{coluna_escolhida}'? (s/n): ").lower()

   if confirmar == "s":
       df = df.drop(columns=[coluna_escolhida])
       print(f"Coluna '{coluna_escolhida}' excluída com sucesso.\n")
       print("========================================")
       print("===== Colunas atualizadas =====")
       print("========================================")
       for i, nome_coluna in enumerate(df.columns, start=1):
            print(f"[{i}] - {nome_coluna}")
       prima_enter()
   else:
       print("Operação cancelada.")


##################################################################################################################################################
# CONSULTAR DADOS - MODULO 3

def ver_primeiras_linhas(df):
    inicio = df.head()
    print(f"As 5 primeiras linhas do seu DataFrame são:\n{inicio}")

def filtro(df):
    print("\n===== Filtrar =====")
    coluna = ler_string("Qual coluna deseja utilizar como filtro? ")
    filtro = ler_string("Por qual valor deseja filtrar? ")
    print( 56 * "-")
    try:
        resultado = df.loc[df[coluna] == filtro]
        print(tabulate(resultado, headers='keys', tablefmt='psql'))
    except:
        print(f"Não existe(m) linha(s) que atenda estas condições: {coluna} = {filtro}\n")
    print( 56 * "-")
    prima_enter()

def consulta_indice_valor(df):
    print("\n==== Consulta específica ====")
    print(f"Você quer visualizar: [1] - Uma linha \n[2] - Um valor específico")

    escolha = ler_int("Escolha a opção: ")
    print( 56 * "-")

    if escolha == 1:
        x = ler_int("Escolha a posição numérica que quer aceder: ")

        linhas, colunas = df.shape

        if x > linhas or x < 0:
            print("Erro: A posição numérica não existe no DataFrame.")

        else:
            print(f"Os valores na posição {x} são: ")
            for valor, resultado in df.iloc[x].items():
                print(f"{valor}: {resultado}")
                print( 56 * "-")
        prima_enter()

    elif escolha == 2:
        x = ler_int("Escolha o índice que quer aceder: ")
        y = ler_string("Escolha a coluna que quer aceder: ").lower()

        linhas, colunas = df.shape

        if y not in df.columns or x > linhas or x < 0:
            print("Erro: A coluna não existe no DataFrame ou não existe esse índice.")
            return df
        else:
            print(f"O valor na posição {x} e na coluna {y} é:\n {df.loc[x, y]}")
        prima_enter()

    else: 
        print("Opção Inválida")
        prima_enter()

def valores_unicos(df):
    print("\n==== Valores Únicos ====")
    coluna = ler_string("Verificar qual coluna? ").lower()
    if coluna not in df.columns:
        print("Erro: A coluna não existe no DataFrame ou não tem números em falta.")
        return df
    else:
        print(f"Contagem de valores únicos da coluna {coluna}:")
        for valor, numero in df[coluna].value_counts().items():
            print(f"{valor}: [{numero}]")
            print(70* "-")

    prima_enter()

def informacao_geral(df):
        print("\n==== Informações gerais ====")
        df.info()
        print( 56 * "-") 
        prima_enter()

def consultar_dados():
    while True:
        print("\n===== Consultar dados ===== ")     
        print( 56 * "-")
        ver_primeiras_linhas(df)
        print( 56 * "-")  
        print("[1] - Filtrar")
        print("[2] - Consultar índice ou valor")
        print("[3] - Contar Valores únicos")
        print("[4] - Ver informações gerais")
        print("[5] - Voltar ao menu principal")
        print( 56 * "-")

        opcao = ler_int("Escolha uma opção: ")

        if opcao == 1: 
            filtro(df)

        elif opcao == 2:
            consulta_indice_valor(df)

        elif opcao == 3: 
            valores_unicos()

        elif opcao == 4:
            informacao_geral()

        elif opcao == 5:
            print("Volte ao menu!")
            prima_enter()

        else:
            print("Opção Inválida!")

##################################################################################################################################################
# ADD LINHA - MODULO 3

def adicionar_linha(df, caminho_excel):
    print("\n===== Adicionar nova linha ao catálogo da Netflix =====")
    
    novo_id = f"s{len(df) + 1}"
    
    tipo = ""
    while tipo not in ["Movie", "TV Show"]:
        tipo = ler_string("Tipo (Movie / TV Show): ").strip()
        if tipo not in ["Movie", "TV Show"]:
            print("Opção inválida, escreva exatamente 'Movie' ou 'TV Show'.")
    
    titulo = ""
    while titulo == "":
        print("O título é obrigatório!")
        titulo = ler_string("Título: ").strip()
    
    diretor = ler_string("Diretor (Enter para deixar em branco): ").strip()
    if diretor == "":
        None
    
    elenco = ler_string("Elenco (separado por vírgulas, Enter para branco): ").strip()
    if elenco == "":
        None
    
    pais = ler_string("País (Enter para deixar em branco): ").strip()
    if pais == "":
        None
    
    data_hoje = datetime.today().strftime("%B %d, %Y")
    data_adicionado = input(f"Data de adição (Enter para usar hoje: {data_hoje}): ").strip()
    data_adicionado = data_adicionado if data_adicionado != "" else data_hoje
    
    ano_publicado = ler_int("Ano de lançamento (Enter para deixar em branco): ").strip()
    if ano_publicado == "":
        None
    
    rating = ler_string("Classificação/Rating (ex: PG-13, TV-MA, Enter p/ branco): ").strip()
    if rating == "":
        None
    
    duracao = ler_string("Duração (ex: '90 min' ou '2 Seasons'): ").strip()
    if duracao == "":
        None
    
    genero = ler_string("Género(s) (ex: 'Dramas, Comedies'): ").strip()
    if genero == "":
        None
    
    descricao = ler_string("Descrição/sinopse (Enter p/ branco): ").strip()
    if descricao == "":
        None
    
    nova_linha = {
        "show_id": novo_id,
        "type": tipo,
        "title": titulo,
        "director": diretor,
        "cast": elenco,
        "country": pais,
        "date_added": data_adicionado,
        "release_year": ano_publicado,
        "rating": rating,
        "duration": duracao,
        "listed_in": genero,
        "description": descricao
    }
    
    df.loc[len(df)] = nova_linha
    
    df.to_excel(caminho_excel, index=False)
    
    print(f"'{titulo}' foi adicionado com sucesso! (ID: {novo_id})")

##################################################################################################################################################
# EDITAR E REMOVER - MODULO 3

def editar_linha(df, caminho_excel):
    print("\n===== Editar título existente =====")
    
    show_id = ler_string("Insira o show_id do título que deseja editar (ex: s146): ").strip()
    
    if show_id not in df["show_id"].values:
        print("Esse show_id não existe no DataFrame.")
        return df
    
    indice = df[df["show_id"] == show_id].index[0]
    
    print(f"Dados atuais de '{df.loc[indice, 'title']}':")
    print(df.loc[indice])
    
    print("\nPrima Enter para manter o valor atual.\n")
    
    for coluna in df.columns:
        if coluna == "show_id":
            continue  
        
        valor_atual = df.loc[indice, coluna]
        novo_valor = ler_string(f"Escreva o que vai modificar na {coluna}! \n (valor atual: {valor_atual})\n Digite: ").strip()
        
        if novo_valor != "":
            if coluna == "release_year":
                try:
                    novo_valor = int(novo_valor)
                except ValueError:
                    print("Valor inválido para ano, mantendo o original.")
                    continue
            df.loc[indice, coluna] = novo_valor
    
    df.to_excel(caminho_excel, index=False)
    print(f"Título '{df.loc[indice, 'title']}' atualizado com sucesso!")


def remover_linha(df, caminho_excel):
    print("\n===== Remover título =====")
    
    show_id = ler_string("Insira o show_id do título que deseja remover (ex: s146): ").strip()
    
    if show_id not in df["show_id"].values:
        print("Esse show_id não existe no DataFrame.")

    else:
        valor_a_remover = df.loc[df["show_id"] == show_id, "title"].values[0]
    
        pergunta = ler_string(f"Tem a certeza que quer remover '{valor_a_remover}' (ID: {show_id})? (s/n): ").strip().lower()
    
        if pergunta == "s":
            df = df[df["show_id"] != show_id].reset_index(drop=True)
            df.to_excel(caminho_excel, index=False)
            print(f"'{valor_a_remover}' foi removido com sucesso!")
        else:
            print("Operação cancelada.")
        
        return df

##################################################################################################################################################

def template():
    print("god, please, help me!")

##################################################################################################################################################
# MENU MODULO 3

def editor_dados():
    print("\n===== GESTÃO DE UM FICHEIRO DE EXCEL =====")
    print("\n============ Editor de Dados ============")
    print( 56 * "-")
    print("[1] - Consultar dados")
    print("[2] - Adicionar nova linha")
    print("[3] - Editar uma linha existente")
    print("[4] - Remover uma linha")
    print("[5] - Template preenchido")
    print("[6] - Voltar ao menu principal")
    print( 56 * "-")

    opcao = ler_int("Escolhe uma opção: ")

    if opcao == 1: 
        consultar_dados()

    elif opcao == 2:
        
        caminho = "netflix_titles_excel_modificado.xlsx"
        df = pd.read_excel(caminho)

        df = adicionar_linha(df, caminho)

    elif opcao == 3:
        caminho = "netflix_titles_excel_modificado.xlsx"
        df = pd.read_excel(caminho)
        
        editar_linha(df, caminho)
        prima_enter()

    elif opcao == 5:
        template()

    elif opcao == 4:
        print("Volte ao menu!")
        prima_enter()

    else:
        print("Opção Inválida!")

##################################################################################################################################################

# FIM FUNÇÕES DO MENU #
##################################################################################################################################################

# IMPORTANDO O FICHEIRO #

# df = pd.read_csv("netflix_titles.csv")

##################################################################################################################################################
# FICHEIRO COM DADOS DUPLICADOS

df = pd.read_csv("netflix_titles_modificado.csv")

##################################################################################################################################################

#SALVAR FICHEIROS

##################################################################################################################################################

operacoes = []

def salvar_operacao_realizada(operacao, linhas):
    operacoes.append({"operacao": operacao, "linha": linhas})

def salvar_ficheiro_modificado():
    opcao = ler_string("Deseja salvar o ficheiro modificado? S ou N \n")
    if opcao.upper() == "S":
        df.to_csv("netflix_titles_modificado_modulo2.csv", index=False)
        print("Ficheiro Salvo: netflix_titles_modificado_modulo2.csv")
    else:
        print("Nada será salvo!")
        
def gravar_ficheiro_operacoes_realizadas():
    ficheiro = open("historico_operacoes.txt", "a", encoding="utf-8")
    total_linhas_alteradas = 0
    for item in operacoes:
        total_linhas_alteradas += int(item['linha'])
        ficheiro.write(f"Operação: {item['operacao']} | Linhas afetadas: {item['linha']}\n")
    ficheiro.write(f"Total Final: {total_linhas_alteradas}\n")
    ficheiro.close()

##################################################################################################################################################

#MENU

def menu():
    global df 
    while True:
        clean()
        print("\n===== PROGRAMA DE LIMPEZA E GESTÃO DE DADOS =====")
        print("[1] - MÓDULO 1: Notebook de Análise de Dados")
        print("[2] - MÓDULO 2: Limpeza e Tratamento de Dados")
        print("[3] - MÓDULO 3: Gestão de um Ficheiro Excel")
        print("[4] - Salvar ficheiro modificado, alterações feitas e sair")

        opcao = ler_int("Escolhe uma opção: ")

        if opcao == 1:
            print("Acesse o arquivo Notebook para ver a nossa análise!")

        elif opcao == 2:
            
            while True:
                clean()
                print("\n===== PROGRAMA DE LIMPEZA E GESTÃO DE DADOS =====")
                print("[1] - Visualizar e editar valores em falta")
                print("[2] - Visualizar e editar linhas duplicadas")
                print("[3] - EXTRA")
                print("[4] -  Voltar ao menu principal")
                
                opcao = ler_int("Escolhe uma opção: ")
                
                if opcao == 1: 
                    clean()
                    menu_ver_linhas_em_falta()
                
                elif opcao == 2:
                    clean()
                    visualizar_editar_linhas_duplicadas_menu()

                elif opcao == 3:
                    while True:
                        print("======================================")
                        print("[1] - Editar nome das colunas")
                        print("[2] - Remover Espaços de uma coluna")
                        print("[3] - Excluir colunas")
                        print("[4] - Voltar ao menu principal")
                        print("======================================")


                        opcao = ler_int("Escolhe uma opção: ")

                        if opcao == 1:
                            ver_colunas()
                            editar_colunas()

                        elif opcao == 2:
                            remover_espacos()
                        elif opcao == 3:
                            excluir_coluna(df)
                        
                        elif opcao == 4:
                            break

                        else:
                            print("Opção inválida, tenta outra vez.")
                

                elif opcao == 4:
                    break

                else:
                    print("Opção inválida, tenta outra vez.")

        elif opcao == 3:
            clean()
            editor_dados()

        elif opcao == 4:
            gravar_ficheiro_operacoes_realizadas() 
            salvar_ficheiro_modificado()
            print("Obrigada. Volte sempre!")
            break

        else:
            print("Opção inválida, tenta outra vez.")

# Chamada da função de menu
# visualizar_editar_linhas_duplicadas_menu()
menu()
