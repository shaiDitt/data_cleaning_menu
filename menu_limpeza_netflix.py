##################################################################################################################################################
###################################################### PROJETO - NETFLIX #########################################################################
##################################################################################################################################################


##################################################################################################################################################
####################################### MÓDULO 1 — Notebook de Análise de Qualidade de Dados #####################################################
##################################################################################################################################################

import os
import sys

import pandas as pd

caminho_ficheiro = "netflix_titles_modificado.csv"
df = pd.read_csv(caminho_ficheiro)

def clean():
    if os.name == "nt":
        os.system('cls')
    else:
        os.system("clear")

def prima_enter():
    input("Prima ENTER para continuar ")
    
def continuar_ou_sair():
    escolha = ler_string("Deseja continuar? [s/n] ").lower().strip()
    return escolha == 's'  # True = quer continuar | False = quer sair

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

def gravar_alteracao_df():
    if caminho_ficheiro.lower().endswith('.csv'):
        df.to_csv(caminho_ficheiro, index=False)
        print("Alterações gravadas com sucesso no ficheiro CSV original!")
    else:
        df.to_excel(caminho_ficheiro, index=False)
        print("Alterações gravadas com sucesso no ficheiro Excel original!")

##################################################################################################################################################
############################################ MÓDULO 2 - Limpeza e Tratamento de Dados ############################################################
##################################################################################################################################################

def mostrar_valores_em_falta(df):
    percentagem = (df.isnull().sum() / len(df)) * 100

    print("## Percentagem de valores em falta por coluna ##")
    for c, l in percentagem.round(2).items():
        print(f"{c}: {l}%")
    print("-" * 56)
    
def remover_linhas_vazias(coluna):
    global df
    if coluna not in df.columns:
        print("Erro: A coluna não existe no DataFrame ou não tem números em falta.")
        prima_enter()
        return df
   
    linhas_vazias = df[coluna].isnull().sum()

    if linhas_vazias == 0:
        print("Não há linhas vazias nessa coluna.")
        prima_enter()
    else:
        escolha = ler_string("Tem certeza que deseja remover linhas vazias? [s/n] ").lower().strip()
        if escolha == 's':
            clean()
            df = df.dropna(subset = coluna)
            print(f"Foram removidas {linhas_vazias } linhas da coluna '{coluna}'")
            salvar_operacao_realizada(f"Foram removidas {linhas_vazias} linhas da coluna '{coluna}'")
            prima_enter()
            clean()
        else: 
            print("Operação cancelada.")
            clean()
            return df
    
def preencher_media_mediana(df, coluna):
    if coluna not in df.columns:
        print("Erro: A coluna não existe no DataFrame.")
        prima_enter()
        clean()
        return df

    if df[coluna].isna().sum() == 0:
        print(f"Não há valores vazios na coluna '{coluna}'. Nada para preencher.")
        prima_enter()
        clean()
        return df

    if df[coluna].dtype not in ("int64", "float64"):
        print(56 * "-")
        print("Essa opção só pode ser usada em colunas numéricas. Retorne ao menu inicial")
        print(f"O tipo de dado é {df[coluna].dtype}")
        print(56 * "-")
        prima_enter()
 
    else:
        print("[1] - Preencher com a média")
        print("[2] - Preencher com a mediana")

        escolha = ler_string("Escolhe uma opção: ")
        print(56*"-")

        if escolha == "1":
            valor = df[coluna].mean()
            df[coluna] = df[coluna].fillna(valor)
            print(f"Os valores vazios da coluna '{coluna}' foram preenchidos com a média: {valor:.0f}")
            salvar_operacao_realizada(f"Os valores vazios da coluna '{coluna}' foram preenchidos com a média: {valor:.0f}")

        elif escolha == "2":
            valor = df[coluna].median()
            df[coluna] = df[coluna].fillna(valor)
            print(f"Os valores vazios da coluna '{coluna}' foram preenchidos com a mediana: {valor:.0f}")   
            salvar_operacao_realizada(f"Os valores vazios da coluna '{coluna}' foram preenchidos com a mediana: {valor:.0f}")

        else:
            print("Opção inválida.")
            prima_enter()
            clean()
            return df
        prima_enter()
        clean()
    
def preencher_linha_valor_fixo(df, coluna, valor_fixo):

    if coluna not in df.columns:
        print("Erro: A coluna não existe no DataFrame.")
        prima_enter()
        clean()
        return df
    
    linhas_nulas = df[coluna].isna().sum()

    if linhas_nulas == 0:
        print("Não há linhas vazias. Confira a tabela a seguir.")
        prima_enter()
        clean()
        return df
    else:
        df.loc[df[coluna].isna(), coluna] = valor_fixo
        print(f"Foram preenchidas {linhas_nulas} linhas totalmente vazias da coluna {coluna} com o valor {valor_fixo}.")
        salvar_operacao_realizada(f"Foram preenchidas {linhas_nulas} linhas totalmente vazias da coluna '{coluna}' com o valor fixo: {valor_fixo}.")
 
    prima_enter()
    clean()

def menu_ver_linhas_em_falta():
    while True:
        clean()
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║                     ✦ VALORES EM FALTA ✦                     ║")
        print("╠══════════════════════════════════════════════════════════════╣")
        mostrar_valores_em_falta(df)
        print("╠══════════════════════════════════════════════════════════════╣")
        print("║ [1] - Remover linhas vazias de uma coluna específica         ║")
        print("║ [2] - Preencher linhas vazias com valor fixo                 ║")
        print("║ [3] - Preencher com a média ou mediana                       ║")
        print("║ [4] - Voltar ao menu principal                               ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        opcao = ler_int("   ╰─▶ Escolhe uma opção: ")

        if opcao == 1: 
            x = ler_string("De qual coluna você quer remover as linhas vazias? ").lower().strip()
            remover_linhas_vazias(x)

        elif opcao == 2:
            y = ler_string("De qual coluna você quer substituir as linhas vazias? ").lower().strip()
            
            if y == "release_year":
                x = ler_float("Qual o valor fixo que você deseja substituir nas linhas vazias? ")
            else:
                x = ler_string("Qual o valor fixo que você deseja substituir nas linhas vazias? ").lower()
            preencher_linha_valor_fixo(df, y, x)

        elif opcao == 3:
            x = ler_string("Qual coluna você gostaria de preencher? ").lower().strip()
            preencher_media_mediana(df, x)

        elif opcao == 4:
                print("Volte ao menu!")
                break
        else:
            print("Opção Inválida!")
            prima_enter()

##################################################################################################################################################
################################################ MÓDULO 2 - DUPLICADOS ###########################################################################
##################################################################################################################################################

def ver_duplicados(df):
    ver_duplicados = df.duplicated().sum()
    texto_duplicados = f" O número de informações duplicadas é: {ver_duplicados}"
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║" + texto_duplicados.ljust(62) + "║")
    print("╚══════════════════════════════════════════════════════════════╝")

def menu_remover_todas_linhas_duplicadas(df):
    clean()
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║              ✦ LINHAS DUPLICADAS ENCONTRADAS ✦               ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print(56 * "-")
    print(df[df.duplicated()])
    print(56 * "-")

    resultado = df[df.duplicated()]
    if resultado.empty:
        print("Não há informações duplicadas. Volte ao menu!")
        prima_enter()
        return df
    else:
        quer_remover = ler_string("Tem certeza que deseja remover todas as linhas duplicações? [s/n] ").lower()
        if quer_remover == "s":
            remover_todas_linhas_duplicadas(df)
        else:
            print("Nenhuma linha duplicada será removida!")
            prima_enter()
        clean()

def remover_todas_linhas_duplicadas(df):
    clean()
    
    subset = definir_coluna_processamento(df)
    if subset is None:
        return 
    
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║               ✦ REMOÇÃO DE LINHAS DUPLICADAS ✦               ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    linhas_antes = len(df)
    df.drop_duplicates(subset=[subset], keep='first', inplace=True)
    linhas_depois = len(df)
    linhas_removidas = linhas_antes - linhas_depois
    salvar_operacao_realizada(f"Foram removidas todas as ({linhas_removidas}) linhas duplicadas pela coluna '{subset}'")
    print(f"Foram removidas {linhas_removidas} linhas duplicadas.")
    prima_enter()
    clean()

def definir_coluna_processamento(df):
    colunas_disponiveis = identificar_colunas(df)
    while True:
        mostrar_colunas_existentes(df)
        print(56 * "-")
        sub_set = ler_string("Qual coluna deseja utilizar como subset para a remoção? (ou digite 'sair' para cancelar): ").strip()
        if sub_set == 'sair':
            return
        elif sub_set == '':
            print("Uma coluna deve ser selecionada antes de prosseguir, ou digite 'sair' para cancelar.")
        elif sub_set not in colunas_disponiveis:
            print(f"Erro: A coluna '{sub_set}' não existe neste ficheiro. Tente novamente.")
            prima_enter()
            clean()

        else:
            return sub_set
            
def mostrar_colunas_existentes(df):
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║                   ✦ VISUALIZANDO COLUNAS ✦                   ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    colunas = identificar_colunas(df)
    for i, nome_coluna in enumerate(colunas, start=1):
       print(f"- {nome_coluna}")

def remover_linha_duplicada(df):

    subset = definir_coluna_processamento(df)
    if subset is None:
        return 
    
    linhas_removidas = 0
    df_analise = df[df.duplicated(subset=[subset], keep=False)]
    
    ids_duplicados = df_analise[subset].unique()

    for id in ids_duplicados:
        
        ocorrencias = df[df[subset] == id]
        print(f"\n--- Analisando o {subset}: {id} (Encontradas {len(ocorrencias)} cópias) ---")
        print(ocorrencias)

        if ocorrencias.empty:
            print("Não há ocorrências.")
            prima_enter()
            return
        else:
        
            decisao = input("Deseja apagar as cópias deste ID e manter apenas a primeira? (s/n): ").lower()
            if decisao == 's':
                quantidade_copias = len(ocorrencias) - 1
                
                indices_para_apagar = ocorrencias.index[1:]
                
                df.drop(indices_para_apagar, inplace=True)
                linhas_removidas += quantidade_copias
                print(f"{quantidade_copias} cópias removidas para o ID {id}.")
            else:
                print(f"Mantidas todas as linhas para o ID {id}.")

    salvar_operacao_realizada(f"Foram removidas {quantidade_copias} linhas duplicadas do '{subset}' {id}")
    prima_enter()  
    clean()
    return linhas_removidas


def visualizar_editar_linhas_duplicadas_menu(df):
    while True:
        clean()
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║                    ✦ LINHAS DUPLICADAS ✦                     ║")
        print("╠══════════════════════════════════════════════════════════════╣")
        ver_duplicados(df)
        print("╠══════════════════════════════════════════════════════════════╣")
        print("║ [1] - Remover todas as duplicadas de uma vez                 ║")
        print("║ [2] - Analisar e remover UMA A UMA manualmente               ║")
        print("║ [3] - Voltar ao menu principal                               ║")
        print("╚══════════════════════════════════════════════════════════════╝")

        opcao = ler_int("   ╰─▶ Escolhe uma opção: ")

        if opcao == 1:
            menu_remover_todas_linhas_duplicadas(df)
        elif opcao == 2:
            remover_linha_duplicada(df)
        elif opcao == 3:
            clean()
            break
        else:
            print("Opção inválida!")
            prima_enter()

##################################################################################################################################################
################################################## MÓDULO 2 - EXTRA ##############################################################################
##################################################################################################################################################

def ver_colunas():
    clean()
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║                   ✦ VISUALIZANDO COLUNAS ✦                   ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    colunas = identificar_colunas(df)
    for i, nome_coluna in enumerate(colunas, start=1):
       print(f"[{i}] - {nome_coluna}")

def ver_colunas_atualizadas():
    clean()
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║                   ✦ COLUNAS ATUALIZADAS ✦                    ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    for i, nome_coluna in enumerate(df.columns, start=1):
        print(f"[{i}] - {nome_coluna}")
    prima_enter()
    clean()

def editar_colunas():
    ver_colunas()

    colunas = list(df.columns)
    escolha = ler_int("Escolha o número da coluna que deseja editar (0 para cancelar): ")

    if escolha == 0:
        print("Operação cancelada.")
        clean()
        return df

    elif escolha < 1 or escolha > len(colunas):
        print("Opção inválida.")
        clean()
        return df

    coluna_escolhida = colunas[escolha - 1]
    nome_novo = ler_string(f"Novo nome para a coluna '{coluna_escolhida}': ")
    
    df.rename(columns={coluna_escolhida :nome_novo}, inplace=True)

    print(f"A coluna [{coluna_escolhida}] foi renomeada para [{nome_novo}]")
    salvar_operacao_realizada(f"A coluna '{coluna_escolhida}' foi renomeada para '{nome_novo}'")
    ver_colunas_atualizadas()

def remover_espacos():
    ver_colunas()

    colunas = list(df.columns)
    escolha = ler_int("Escolha o número da coluna que deseja remover espaços (0 para cancelar): ")

    if escolha == 0:
        print("Operação cancelada.")
        clean()
        return df

    if escolha < 1 or escolha > len(colunas):
        print("Opção inválida.")
        clean()
        return df
    
    coluna_escolhida = colunas[escolha - 1]
    confirmar = input(f"Tem certeza que deseja remover os espaços da coluna '{coluna_escolhida}'? (s/n): ").lower()

    if confirmar == "s":
        df[coluna_escolhida] = df[coluna_escolhida].str.replace(' ', '', regex=False)
        titulo_coluna = f"✦ VISUALIZANDO {coluna_escolhida.upper()} ✦"
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║" + titulo_coluna.center(62) + "║")
        print("╚══════════════════════════════════════════════════════════════╝")
        for i in df[coluna_escolhida].head(10):
            print(i)
        salvar_operacao_realizada(f"Os espaços da coluna '{coluna_escolhida}' foram removidos.")
        prima_enter()
        clean()
    else:
        print("Operação cancelada.")
        prima_enter()
        clean()

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
   confirmar = ler_string(f"Tem certeza que deseja excluir a coluna '{coluna_escolhida}'? (s/n): ").lower()

   if confirmar == "s":
        df = df.drop(columns=[coluna_escolhida])
        
        print(f"Coluna '{coluna_escolhida}' excluída com sucesso.\n")
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║                   ✦ COLUNAS ATUALIZADAS ✦                    ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        for i, nome_coluna in enumerate(df.columns, start=1):
            print(f"[{i}] - {nome_coluna}")
        salvar_operacao_realizada(f"A coluna '{coluna_escolhida}' foi removida.")
        ver_colunas_atualizadas()
        prima_enter()
        clean()
   else:
       print("Operação cancelada.")
       prima_enter()
       clean()

def identificar_colunas(df):
    return list(df.columns)

def menu_extra_2():
    while True:
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║                        ✦ MENU EXTRA ✦                        ║")
        print("╠══════════════════════════════════════════════════════════════╣")
        print("║ [1] - Editar nome das colunas                                ║")
        print("║ [2] - Remover Espaços de uma coluna                          ║")
        print("║ [3] - Excluir colunas                                        ║")
        print("║ [4] - Voltar ao menu principal                               ║")
        print("╚══════════════════════════════════════════════════════════════╝")

        opcao = ler_int("   ╰─▶ Escolhe uma opção: ")

        if opcao == 1:
            ver_colunas()
            editar_colunas()

        elif opcao == 2:
            remover_espacos()
        elif opcao == 3:
            excluir_coluna(df)
        
        elif opcao == 4:
            prima_enter()
            break

        else:
            print("Opção inválida, tenta outra vez.")

##################################################################################################################################################
####################################################### MÓDULO 2 - MENU ##########################################################################
##################################################################################################################################################

def menu_modulo2():
    global df
    if df is not None:
        while True:
            clean()
            print("╔══════════════════════════════════════════════════════════════╗")
            print("║              ✦ LIMPEZA E TRATAMENTO DE DADOS ✦               ║")
            print("╠══════════════════════════════════════════════════════════════╣")
            print("║ [1] - Valores em Falta                                       ║")
            print("║ [2] - Linhas Duplicadas                                      ║")
            print("║ [3] - EXTRA                                                  ║")
            print("║ [4] - Voltar ao menu principal                               ║")
            print("╚══════════════════════════════════════════════════════════════╝")

            opcao = ler_int("   ╰─▶ Escolhe uma opção: ")

            if opcao == 1:
                clean()
                menu_ver_linhas_em_falta()

            elif opcao == 2:
                clean()
                visualizar_editar_linhas_duplicadas_menu(df)
                

            elif opcao == 3:
                clean()
                menu_extra_2()

            elif opcao == 4:
                prima_enter()
                break

            else:
                print("Opção inválida, tenta outra vez.")
                prima_enter()

##################################################################################################################################################
################################################# MÓDULO 3 — GESTÃO DE FICHEIRO EXCEL ############################################################
##################################################################################################################################################
def ver_primeiras_linhas(df):
    inicio = df.head()
    print("As 5 primeiras linhas do seu DataFrame são: ")
    print(56 * "-")
    print(f"{inicio}")

def filtro(df):
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║                         ✦ FILTRAR ✦                          ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    colunas = df.columns
    print(colunas)
    print(56*"-")
    coluna = ler_string("Qual coluna deseja utilizar como filtro? ").strip().lower()

    if coluna not in colunas:
        print("Erro: A coluna não existe no DataFrame.")
        prima_enter()
        clean()
        return

    if df[coluna].dtype not in ["int64", "float64"]:
        filtro = ler_string("Por qual valor deseja filtrar? ").strip().lower()
        print( 56 * "-")
        resultado = df.loc[df[coluna].str.lower() == filtro]
        if resultado.empty:
            print(f"Não existe(m) linha(s) que atenda estas condições: {coluna} = {filtro}\n")
            prima_enter()
 
        else:
            print(resultado)
            prima_enter()

    else: 
        filtro = ler_float("Por qual valor deseja filtrar? ")
        print( 56 * "-")
        resultado = df.loc[df[coluna] == filtro]
        if resultado.empty:
            print(f"Não existe(m) linha(s) que atenda estas condições: {coluna} = {filtro}\n")
            prima_enter()
        else:
            print(resultado)
            prima_enter()

    print( 56 * "-")
    clean()

def consulta_indice_valor(df):
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║                   ✦ CONSULTA ESPECÍFICA ✦                    ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print(f"Você quer visualizar: \n[1] - Uma linha \n[2] - Um valor específico")

    print(56 * "-")
    escolha = ler_int("Escolha a opção: ")
    print( 56 * "-")

    if escolha == 1:
        posicao = ler_int("Escolha a posição numérica da linha que quer aceder: ") 
        print( 56 * "-")
        linhas, colunas = df.shape

        if posicao > linhas or posicao < 0:
            print("Erro: A posição numérica não existe no DataFrame.")

        else:
            print(f"Os valores na posição {posicao} são:\n")
            for valor, resultado in df.iloc[posicao].items():
                print(f"{valor}: {resultado}")
                print( 56 * "-")
        prima_enter()
        clean()

    elif escolha == 2:
        clean()
        mostrar_colunas_existentes(df)
        coluna = ler_string("Escolha a coluna que quer aceder: ").lower().strip()
        indice = ler_int("Escolha o índice que quer aceder: ")
        print(56*"-")
        linhas, colunas = df.shape

        if coluna not in df.columns or indice > linhas or indice < 0:
            print("Erro: A coluna não existe no DataFrame ou não existe esse índice.")
            prima_enter()
            return df
        else:
            print(f"O valor na posição {indice} e na coluna {coluna} é:\n {df.loc[indice, coluna]}")
            prima_enter()
            clean()

    else: 
        print("Opção Inválida")
        prima_enter()
        clean()

def valores_unicos(df):
    mostrar_colunas_existentes(df)
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║                      ✦ VALORES ÚNICOS ✦                      ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    coluna = ler_string("Verificar qual coluna? ").strip().lower()
    if coluna not in df.columns:
        print("Erro: A coluna não existe no DataFrame ou não tem números em falta.")
        return df
    else:
        print(f"Contagem de valores únicos da coluna {coluna}:")
        for valor, numero in df[coluna].value_counts().items():
            print(f"{valor}: [{numero}]")
            print(150* "-")

    prima_enter()
    clean()

def informacao_geral(df):
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║                    ✦ INFORMAÇÕES GERAIS ✦                    ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        df.info()
        print( 56 * "-") 
        prima_enter()
        clean()
        
##################################################################################################################################################
############################################### MÓDULO 3 - MENU CONSULTAR DADOS ##################################################################
##################################################################################################################################################

def consultar_dados():
    global df
    while True:
        clean()
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║                     ✦ CONSULTAR DADOS ✦                      ║")
        print("╠══════════════════════════════════════════════════════════════╣")
        ver_primeiras_linhas(df)
        print("╠══════════════════════════════════════════════════════════════╣")
        print("║ [1] - Filtrar                                                ║")
        print("║ [2] - Consultar índice e valor                               ║")
        print("║ [3] - Contar valores únicos                                  ║")
        print("║ [4] - Ver informações gerais                                 ║")
        print("║ [5] - Voltar ao menu principal                               ║")
        print("╚══════════════════════════════════════════════════════════════╝")

        opcao = ler_int("   ╰─▶ Escolha uma opção: ")

        if opcao == 1:
            clean()
            filtro(df)

        elif opcao == 2:
            clean()
            consulta_indice_valor(df)

        elif opcao == 3:
            clean()
            valores_unicos(df)

        elif opcao == 4:
            clean()
            informacao_geral(df)

        elif opcao == 5:
            print("Volte ao menu!")
            prima_enter()
            break

        else:
            print("Opção Inválida!")
            prima_enter()

##################################################################################################################################################
############################################### MÓDULO 3 - ADICIONAR LINHA #############"#########################################################
##################################################################################################################################################

def adicionar_linha(df, caminho_excel):
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║                   ✦ ADICIONAR NOVA LINHA ✦                   ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print("Veja cada coluna e adicione o valor.")
    print(36*"-")

    nova_linha = {}

    print("As colunas do arquivo são: ")
    for coluna in df.columns:
        print(coluna)
    print(36*"-")

    for coluna in df.columns:
        if coluna == "show_id":
            print("Coluna 'show_id é a chave primária e foi adicionada automaticamente.")
            prima_enter()
            clean()
            novo_id = f"s{len(df)}"
            texto_id = f" O novo id é {novo_id}"
            print("╔══════════════════════════════════════════════════════════════╗")
            print("║" + texto_id.ljust(62) + "║")
            print("╚══════════════════════════════════════════════════════════════╝")
            
            nova_linha["show_id"] = novo_id

        else:

            if df[coluna].dtype not in ["int64", "float64"]:
                print(f"--------------Coluna: {coluna}--------------")
                valor_str = ler_string("Valor adicionado: ").strip()
                
                nova_linha[coluna] = valor_str
            else:
                print(f"--------------Coluna: {coluna}--------------")
                valor_float = ler_float("Valor adicionado: ")
                print(f"-{coluna}: [{valor_float}]")

                nova_linha[coluna] = valor_float 
    
    df.loc[len(df)] = nova_linha
    prima_enter()
    clean()

    print(f"'{nova_linha}'\n Linha adicionada com com sucesso! (ID: {novo_id})")
    salvar_operacao_realizada(f"A nova linha: \n'{nova_linha}'\n foi adicionada com sucesso no DataFrame! (ID: {novo_id})")
    prima_enter()
    clean()

##################################################################################################################################################
############################################### MÓDULO 3 - EDITAR E REMOVER ######################################################################
##################################################################################################################################################

def editar_celula(df):
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║               ✦ EDITAR UMA CÉLULA EXISTENTE ✦                ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    mostrar_colunas_existentes(df)
    coluna = ler_string("Insira qual a coluna que você quer editar: ").strip().lower()

    if coluna not in df.columns:
        print("Essa coluna não existe no DataFrame.")
    else:
        indice = ler_int("Insira qual o índice que quer editar: ")
        prima_enter()
        clean()

        tamanho = (len(df[coluna]) - 1)

        if indice > tamanho or indice < 0:
            print("Indíce inválido.")

        else:
            print(56 * "-")
            print(f"==== Valor atual — Coluna {coluna}: indice [{indice}]\n'{df.loc[indice, coluna]}'")
            print(56 * "-")
            print(f"\n\n==== Valores gerais ====\n {df.iloc[indice]}")
                
            decisao = ler_string("Tem certeza que deseja alterar? s / n: ").lower()
            print(56* "-")

            if decisao == "s":
                
                novo_valor = ler_string(f"Escreva o que vai modificar na — Coluna {coluna}: indice [{indice}] \nDigite: ").strip().capitalize()
                prima_enter()
                
                if novo_valor != "":
                    if df[coluna].dtype in ["int64", "float64"]:
                        try:
                            novo_valor = int(novo_valor)
                        except ValueError:
                            print("Valor inválido para coluna numérica, mantendo o original.")
                            clean()
                            return df
                                                    
                df.loc[indice, coluna] = novo_valor
                print(56 * "-")
                print(f"Valor atualizado com sucesso! Linha atual: \n {df.iloc[indice]}")
                salvar_operacao_realizada(f"O valor {novo_valor} foi atualizado com sucesso na coluna '{coluna}'! Linha atual: \n {df.iloc[indice]}")
            else: 
                print("A célula não foi alterada!")

    prima_enter()
    clean()

def remover_linha(df):
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║                      ✦ REMOVER LINHA ✦                       ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    
    indice = ler_int("Insira o indice que deseja remover: ")
    
    tamanho = (len(df) - 1)

    if indice > tamanho or indice < 0:
        print("Indíce inválido.")    

    else:
        print("Os valores da linha selecionada são: ")
        for coluna, valor in df.loc[indice].items():
            print(f"{coluna}: {valor}")
    
        pergunta = ler_string(f"Tem a certeza que quer remover os valores do índice {indice})? (s/n): ").strip().lower()
    
        if pergunta == "s":
            df = df.drop(index=indice)
            print(f"Linha de índice {indice} foi removida com sucesso!")
            salvar_operacao_realizada(f"A linha de índice [{indice}] foi removida! A linha era: {df.iloc[indice]}")
            print(150 * "-")
            clean()
            return df
        else:
            print("Operação cancelada.")
            prima_enter()
            return df
                    
##################################################################################################################################################
################################################### MÓDULO 3 - EXTRA #############################################################################
##################################################################################################################################################

def template(df):
    cabecalho = list(df.columns)
    df_cabecalho = pd.DataFrame(columns=cabecalho)
    colunas_com_erro = []
    
    try:
        df_cabecalho.to_excel('cabecalhos.xlsx', index=False)
    except:
        clean()
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║                 ✦ ERRO AO SALVAR FICHEIRO ✦                  ║")
        print("╠══════════════════════════════════════════════════════════════╣")
        print("║ Não foi possível salvar o ficheiro.                          ║")
        print("║ Feche o Excel e tente novamente!                             ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        prima_enter()
        clean()
        return df
            
        
    clean()
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║               ✦ TEMPLATE CRIADO COM SUCESSO ✦                ║")
    print("╠══════════════════════════════════════════════════════════════╣")
    print("║ Arquivo 'cabecalhos.xlsx' criado com sucesso!                ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    prima_enter()
    clean()
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║                    ✦ PREENCHER TEMPLATE ✦                    ║")
    print("╠══════════════════════════════════════════════════════════════╣")
    print("║ Abra o arquivo gerado e preencha com os valores que desejar  ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    prima_enter()
    clean()

    while True:
        print("=====================================================")
        ok = ler_string("Já preencheu e salvou o arquivo? [s/n] ").lower().strip()

        if ok == 'n':
            prima_enter()
            if continuar_ou_sair():
                clean()
                continue
            else:
                clean()
                return df

        elif ok == 's':
            prima_enter()
            clean()
            try:
                df_preenchido = pd.read_excel('cabecalhos.xlsx', usecols=cabecalho)

            except ValueError:
                print("ALERTA: As colunas do arquivo foram alteradas!\n")
                print(f"Certifique-se que as colunas sejam:")
                for colunas in cabecalho:
                    print(f"[{colunas}]")
                prima_enter()
                if continuar_ou_sair():
                    clean()
                    continue
                else:
                    clean()
                    return df

            colunas_excel = list(df_preenchido.columns)

            if df_preenchido.empty:
                print("Não foi inserido nenhum valor.")
                if continuar_ou_sair():
                    clean()
                    continue
                else:
                    clean()
                    return df
            elif cabecalho != colunas_excel:
                print("ALERTA: As colunas do arquivo foram alteradas!\n")
                print(f"Certifique-se que as colunas sejam:")
                for colunas in cabecalho:
                    print(f"[{colunas}]")
                prima_enter()
                if continuar_ou_sair():
                    clean()
                    continue
                else:
                    clean()
                    return df
            else:
                df_novos_dados = df_preenchido[cabecalho]
                df_novos_dados = df_novos_dados.replace(r'^\s*$', pd.NA, regex = True)
            
                for col in cabecalho:
                    if df[col].dtype in ["int64", "float64"]:
                        convertido = pd.to_numeric(df_novos_dados[col], errors="coerce")
                        se_falhou = df_novos_dados[col].notna() & convertido.isna()
                        if se_falhou.any():
                            colunas_com_erro.append(col)
                            print("========================================")
                            print("ALERTA: Foram encontrados valores não numéricos nas colunas:")
                            for col in colunas_com_erro:
                                print(f"  - {col}")
                            print("Corrija o ficheiro 'cabecalhos.xlsx' antes de continuar.")
                            print("=====================================================")
                            if continuar_ou_sair():
                                clean()
                                continue
                            else:
                                clean()
                                continue
                        else:
                            df_novos_dados[col] = convertido               
           
                            print("╔══════════════════════════════════════════════════════════════╗")
                            print("║               ✦ VISUALIZANDO DADOS INSERIDOS ✦               ║")
                            print("╚══════════════════════════════════════════════════════════════╝")
                            print(df_novos_dados)
                            prima_enter()
                            clean()

                            df_concatenado = pd.concat([df, df_novos_dados], ignore_index=True)
                            salvar_operacao_realizada(f"Foram adicionadas {len(df_novos_dados)} linhas ao DataFrame principal através do ficheiro Excel")

                            print(f"\nSucesso! Foram adicionadas {len(df_novos_dados)} linhas ao DataFrame principal.")
                            print(f"Total de linhas no df final: {len(df_concatenado)}")
                            prima_enter()
                            clean()

                            inicio = df_concatenado.tail(10)
                            print("╔══════════════════════════════════════════════════════════════╗")
                            print("║              ✦ ÚLTIMAS 10 LINHAS DO DATAFRAME ✦              ║")
                            print("╚══════════════════════════════════════════════════════════════╝")
                            print(f"{inicio}")
                            prima_enter()
                            clean()
                            return df_concatenado

        else:
            print("Valor inválido!")
            prima_enter()
            clean()

##################################################################################################################################################
###################################################### MÓDULO 3 - MENU ############################################################################
##################################################################################################################################################

def editor_dados():
    global df, caminho_ficheiro
    while True:
        clean()
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║                     ✦ EDITOR DE DADOS ✦                      ║")
        print("╠══════════════════════════════════════════════════════════════╣")
        print("║ [1] - Consultar dados                                        ║")
        print("║ [2] - Adicionar nova linha                                   ║")
        print("║ [3] - Editar uma célula existente                            ║")
        print("║ [4] - Remover uma linha                                      ║")
        print("║ [5] - Template preenchido                                    ║")
        print("║ [6] - Voltar ao menu principal                               ║")
        print("╚══════════════════════════════════════════════════════════════╝")

        opcao = ler_int("   ╰─▶ Escolhe uma opção: ")

        if opcao == 1:
            consultar_dados() #Abre o menu de consultar dados. 

        elif opcao == 2:
            clean()
            adicionar_linha(df, caminho_ficheiro)

        elif opcao == 3:
            clean()
            editar_celula(df)

        elif opcao == 4:
            clean()
            df = remover_linha(df)

        elif opcao == 5:
            df = template(df)
            

        elif opcao == 6:
            print("Volte ao menu!")
            prima_enter()
            break

        else:
            print("Opção Inválida!")
            prima_enter()
            clean()
            

##################################################################################################################################################
################################################## FIM FUNÇÕES DO MENU ###########################################################################
##################################################################################################################################################

operacoes = []

def salvar_operacao_realizada(operacao):
    operacoes.append(f"Operação realizada : {operacao}")
        
def f_ficheiro_operacoes_realizadas(df):
    ficheiro = open("historico_operacoes.txt", "w", encoding="utf-8")
    total_linhas_alteradas = 0

    for item in operacoes:
        total_linhas_alteradas += 1
        ficheiro.write(f"{item}\n")
    ficheiro.close()

    linhas =  colunas = 0
    if df is not None:
        linhas, colunas = df.shape

    ficheiro = open("historico_operacoes.txt", "a", encoding="utf-8")
    ficheiro.write(f"Total de linhas alteradas: {total_linhas_alteradas}\nTotal Final: {linhas} linhas, {colunas} colunas")
    ficheiro.close()

def salvar_ficheiro_modificado():
    opcao = ler_string("Deseja salvar o ficheiro modificado? S ou N \n")
    if opcao.upper() == "S":
        gravar_alteracao_df()
        f_ficheiro_operacoes_realizadas(df)
        print("Ficheiro Salvo: netflix_titles_modificado.csv")
    else:
        print("Nada será salvo!")

##################################################################################################################################################
########################################################## PROJETO - MENU ########################################################################
##################################################################################################################################################

def menu():
    global df 
    while True:
        clean()
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║          ✦ PROGRAMA DE LIMPEZA E GESTÃO DE DADOS ✦           ║")
        print("╠══════════════════════════════════════════════════════════════╣")
        print("║ [1] - MÓDULO 1: Notebook de Análise de Dados                 ║")
        print("║ [2] - MÓDULO 2: Limpeza e Tratamento de Dados                ║")
        print("║ [3] - MÓDULO 3: Gestão de um Ficheiro Excel                  ║")
        print("║ [4] - Salvar ficheiro modificado, alterações feitas e sair   ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        opcao = ler_int("   ╰─▶ Escolhe uma opção: ")
        
        if opcao == 1:
            print("Acesse o arquivo Notebook para ver a nossa análise!")
            prima_enter()

        elif opcao == 2:
            menu_modulo2()

        elif opcao == 3:
            clean()
            editor_dados()

        elif opcao == 4:
            salvar_ficheiro_modificado()
            print("Obrigada. Volte sempre!")
            break

        else:
            print("Opção inválida, tenta outra vez.")
            prima_enter()

def main():
    try:
        menu()
    except KeyboardInterrupt:
        print("\nObrigada. Volte sempre!")
        sys.exit(0)  # Fecha o terminal de forma limpa

if __name__ == "__main__":
    main()
