import os
import json
from datetime import datetime, date


# --- Variáveis Globais ---
lista_tarefas = []
contador_id = 1  # ID único
ARQUIVO_TAREFAS = "tarefas.json"
ARQUIVO_ARQUIVADAS = "tarefas_arquivadas.json"

PRIORIDADES = ["Urgente", "Alta", "Média", "Baixa"]
STATUS = ["Pendente", "Fazendo", "Concluída", "Arquivado", "Excluída"]
ORIGENS = ["E-mail", "Telefone", "Chamado do Sistema"]


# --- Persistência dos Dados ---


def criar_arquivos_se_necessario():
    """Cria arquivos JSON vazios se não existirem."""
    for arquivo in [ARQUIVO_TAREFAS, ARQUIVO_ARQUIVADAS]:
        if not os.path.exists(arquivo):
            with open(arquivo, "w", encoding="utf-8") as f:
                json.dump([], f, indent=4)


def carregar_dados():
    """Carrega tarefas do arquivo JSON e ajusta contador de ID."""
    global lista_tarefas, contador_id

    with open(ARQUIVO_TAREFAS, "r", encoding="utf-8") as f:
        lista_tarefas = json.load(f)

    if lista_tarefas:
        contador_id = max(t["ID"] for t in lista_tarefas) + 1


def salvar_dados():
    """Salva tarefas no arquivo JSON."""
    with open(ARQUIVO_TAREFAS, "w", encoding="utf-8") as f:

        
        json.dump(lista_tarefas, f, indent=4, default=str)


def salvar_arquivada(tarefa):
    """Salva tarefa arquivada no histórico permanente."""
    with open(ARQUIVO_ARQUIVADAS, "r", encoding="utf-8") as f:
        historico = json.load(f)

    historico.append(tarefa)

    with open(ARQUIVO_ARQUIVADAS, "w", encoding="utf-8") as f:
        json.dump(historico, f, indent=4, default=str)


# --- Funções Auxiliares ---


def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')


def obter_entrada_validada(prompt, opcoes):
    print(f"Executando função obter_entrada_validada()")
    while True:
        limpar_tela()
        print(f"Opções disponíveis: {', '.join(opcoes)}")
        entrada = input(prompt).strip()
        if entrada in opcoes:
            return entrada
        input("\nValor inválido. Pressione ENTER para tentar novamente...")


# --- Ciclo de Vida da Tarefa ---


def criar_tarefa():
    print("Executando função criar_tarefa()")
    global contador_id

    limpar_tela()
    print("### CRIAÇÃO DE NOVA TAREFA ###\n")

    titulo = input("Título: ").strip()
    descricao = input("Descrição: ").strip()

    prioridade = obter_entrada_validada("Prioridade: ", PRIORIDADES)
    origem = obter_entrada_validada("Origem: ", ORIGENS)

    nova = {
        "ID": contador_id,
        "Título": titulo,
        "Descrição": descricao,
        "Prioridade": prioridade,
        "Status": "Pendente",
        "Origem": origem,
        "Data de Criação": datetime.now(),
        "Data de Conclusão": None
    }

    lista_tarefas.append(nova)
    contador_id += 1

    input("\nTarefa criada! Pressione ENTER...")


def verificar_urgencia():
    print("Executando função verificar_urgencia()")
    limpar_tela()

    em_exec = next((t for t in lista_tarefas if t["Status"] == "Fazendo"), None)
    if em_exec:
        print(f"Já existe tarefa em execução: {em_exec['Título']}")
        input("\nPressione ENTER...")
        return

    for prioridade in PRIORIDADES:
        for tarefa in lista_tarefas:
            if tarefa["Prioridade"] == prioridade and tarefa["Status"] == "Pendente":
                tarefa["Status"] = "Fazendo"
                input(f"\nTarefa {tarefa['Título']} iniciada. Pressione ENTER...")
                return

    input("\nNenhuma tarefa pendente. Pressione ENTER...")


def atualizar_prioridade():
    print("Executando função atualizar_prioridade()")
    limpar_tela()

    for i, t in enumerate(lista_tarefas):
        print(f"{i} - ID {t['ID']} | {t['Título']} | {t['Prioridade']}")

    try:
        idx = int(input("\nEscolha o número da tarefa: "))
        lista_tarefas[idx]["Prioridade"] = obter_entrada_validada("Nova prioridade: ", PRIORIDADES)
    except:
        pass

    input("\nAtualizado! ENTER...")


def concluir_tarefa():
    print("Executando função concluir_tarefa()")
    limpar_tela()

    fazendo = [t for t in lista_tarefas if t["Status"] == "Fazendo"]
    if not fazendo:
        input("Nenhuma tarefa em execução. ENTER...")
        return

    tarefa = fazendo[0]
    tarefa["Status"] = "Concluída"
    tarefa["Data de Conclusão"] = date.today()

    input(f"\nTarefa concluída! Pressione ENTER...")


def arquivar_tarefas_antigas():
    print("Executando função arquivar_tarefas_antigas()")
    hoje = date.today()

    for t in lista_tarefas:
        if t["Status"] == "Concluída" and (hoje - t["Data de Conclusão"]).days >= 7:
            t["Status"] = "Arquivado"
            salvar_arquivada(t)

    input("\nArquivamento concluído! ENTER...")


def excluir_tarefa():
    print("Executando função excluir_tarefa()")
    limpar_tela()

    for i, t in enumerate(lista_tarefas):
        print(f"{i} - {t['Título']} | Status: {t['Status']}")

    try:
        idx = int(input("\nEscolha o número da tarefa para excluir: "))
        lista_tarefas[idx]["Status"] = "Excluída"
    except:
        pass

    input("\nTarefa Excluída (lógico). ENTER...")


def exibir_relatorio():
    print("Executando função exibir_relatorio()")
    limpar_tela()

    for t in lista_tarefas:
        duracao = "-"
        if t["Data de Conclusão"]:
            duracao = (t["Data de Conclusão"] - t["Data de Criação"].date()).days
        print(f"ID {t['ID']} | {t['Status']:<10} | {t['Título']} | Execução: {duracao} dias")

    input("\nENTER...")


def relatorio_arquivadas():
    print("Executando função relatorio_arquivadas()")
    limpar_tela()

    arqu = [t for t in lista_tarefas if t["Status"] == "Arquivado"]

    if not arqu:
        input("Nenhuma arquivada. ENTER...")
        return

    for t in arqu:
        print(f"ID {t['ID']} | {t['Título']}")

    input("\nENTER...")


# --- MENU ---


def menu():
    while True:
        limpar_tela()
        print("""
===== GERENCIADOR DE TAREFAS =====
1 - Criar Tarefa
2 - Verificar Urgência (Iniciar)
3 - Atualizar Prioridade
4 - Concluir Tarefa
5 - Arquivar Concluídas Antigas
6 - Relatório Geral
7 - Relatório Arquivadas
8 - Excluir Tarefa
9 - Sair
""")
        opc = input("Escolha: ")

        if opc == "1": criar_tarefa()
        elif opc == "2": verificar_urgencia()
        elif opc == "3": atualizar_prioridade()
        elif opc == "4": concluir_tarefa()
        elif opc == "5": arquivar_tarefas_antigas()
        elif opc == "6": exibir_relatorio()
        elif opc == "7": relatorio_arquivadas()
        elif opc == "8": excluir_tarefa()
        elif opc == "9":
            salvar_dados()
            print("Salvo! Encerrando...")
            exit()
        else:
            input("Opção inválida... ENTER.")


# --- Execução Principal ---
criar_arquivos_se_necessario()
carregar_dados()
menu()

