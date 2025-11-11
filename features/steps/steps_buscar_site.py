# ============================================================
# 🧩 Importação das bibliotecas necessárias
# ============================================================

from behave import given, when, then  
# Importa as anotações (decorators) do framework Behave, que são usadas para
# definir etapas do comportamento BDD:
# @given → representa o "Dado que"
# @when  → representa o "Quando"
# @then  → representa o "Então"
# Elas conectam o texto escrito no arquivo .feature com o código que o executa.

from selenium.webdriver import Edge  
# Importa o driver do navegador Microsoft Edge, usado pelo Selenium para controlar o navegador.

from selenium.webdriver.edge.options import Options  
# Importa a classe Options, que permite configurar parâmetros do navegador (como tela cheia, logs, etc).

from selenium.webdriver.common.by import By  
# Classe que define os diferentes tipos de seletores (estratégias para localizar elementos na página),
# como: By.ID, By.NAME, By.XPATH, By.CSS_SELECTOR, etc.

from selenium.webdriver.common.keys import Keys  
# Permite simular o uso de teclas do teclado, como ENTER, TAB, SETA, etc.

import time  
# Biblioteca padrão do Python usada aqui para adicionar pausas (delays) entre as ações.
# Isso garante que a página tenha tempo de carregar antes do próximo comando.

# ============================================================
# 🧠 Definição dos passos do teste BDD (Gherkin)'''
# ============================================================


# ----------------------------------------
# 1️⃣ Etapa "DADO QUE..."
# ----------------------------------------
@given("que o navegador Microsoft Edge está aberto")
def step_open_browser(context):
    # Cria um objeto de configuração do navegador
    options = Options()

    # Inicia o navegador maximizado (em tela cheia)
    options.add_argument("--start-maximized")

    # Desativa a detecção de automação (impede que sites saibam que o navegador é controlado por Selenium)
    options.add_argument("--disable-blink-features=AutomationControlled")

    # Remove mensagens de log desnecessárias no terminal (de "DevTools" e "EdgeAuth")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    # Inicializa o navegador Edge com as opções definidas acima
    context.driver = Edge(options=options)

    # Abre o site inicial: Google
    context.driver.get("https://web.whatsapp.com/")

    # Aguarda 3 segundos para garantir que a página carregue
    time.sleep(30)


# ----------------------------------------
# 2️⃣ Etapa "QUANDO..."
# ----------------------------------------
@when('eu pesquisar por QA no WhatsAppWeb')
def step_search_whatsapp(context):
    # Localiza o campo de busca do Whatsapp pelo atributo CLASSE
    campo = context.driver.find_element(By.CLASS_NAME,"selectable-text")

    # Digita o texto "[QA IBTECH | AGO/25]" no campo de pesquisa
    campo.send_keys("[QA IBTECH | AGO/25]")

    # Pressiona a tecla ENTER para executar a busca
    campo.send_keys(Keys.RETURN)

    # Espera 4 segundos até os resultados aparecerem
    time.sleep(4)


# ----------------------------------------
# 3️⃣ Etapa "ENTÃO..."
# ----------------------------------------
@then("devo mandar uma mensagem no grupo com sucesso")
def step_verify_site(context):
    # Aguarda o carregamento da tela de resultados
    time.sleep(3)   
   
    # Captura todos os elementos que representam títulos de resultados "x10l6tqk"
    resultados = context.driver.find_elements(By.CSS_SELECTOR, ".x10l6tqk.xh8yej3.x1g42fcv")

    # Verifica se há pelo menos um resultado de busca
    if resultados:
        # Clica no primeiro resultado (simula o clique do usuário)
        resultados[0].click()

        # Aguarda 4 segundos para o grupo abrir completamente
        time.sleep(4)

        from selenium.webdriver.support.ui import WebDriverWait
        #Serve para esperar até que um elemento apareça na tela.
        
        from selenium.webdriver.support import expected_conditions as EC
        #Define o que você está esperando que aconteça.

        campo = WebDriverWait(context.driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "footer div[contenteditable='true']")))
        #esperar até 20segundos para que esse elemento apareça
        #so continua quando o campo existir na pagina
        #seleciona qualquer campo de texto no footer para digitar a msg
        
        # Digita o texto "Mensagem enviada com sucesso!" no campo texto do whatsapp
        campo.send_keys("Mensagem enviada com sucesso!" + Keys.ENTER)
        
        # Espera 4 segundos até os resultados aparecerem
        time.sleep(4)
      
        # Exibe uma mensagem de sucesso no terminal
        print("🌐 Mensagem enviada ao grupo com sucesso!")
    else:
        # Caso nenhum resultado tenha sido encontrado, lança um erro de teste
        raise AssertionError("❌ Nenhum resultado encontrado.")

    # Encerra o navegador ao final do teste
    context.driver.quit()
