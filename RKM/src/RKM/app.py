"""
Um app para anotar os gastos.
"""
#Inicia a virtualização -> source beeware-venv/bin/activate
#Execultar o app -> briefcase dev
#Buildar -> briefcase build android

#Importar bibliotecas
import pandas as pd
import shutil
import time
import os
import toga
import toga.dialogs, asyncio
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER

class Duck(toga.App): 
    def startup(self):


        main_box = toga.Box(style=Pack(direction=COLUMN, alignment=CENTER, background_color="white"))  

        # Colocar a logo
        my_image = toga.Image('RKM.png') 

        image_view = toga.ImageView(
            image=my_image,
            style=Pack(width=100,
                       height=100,
                       padding_top=10) 
        )

        # Escolher a Máquina 
        Maquina_label = toga.Label(
            "Foi gasto com:",
            style=Pack(padding=(10), text_align='left', color="black"),
        )

        opoes_maquina = ['Alimentação','Saúde','Luxos','Fixo', 'Educação']

        self.Maquina_Select = toga.Selection(
            items=opoes_maquina, 
            style=Pack(flex=1)
        )

        Escolha_box = toga.Box(style=Pack(direction=COLUMN, padding=5))
        Escolha_box.add(Maquina_label)
        Escolha_box.add(self.Maquina_Select)

        # Colocar as peças
        Peca_label = toga.Label(
            "Compra:",
            style=Pack(padding=(10), text_align='left', color="black"),
        )
        self.Peca_input = toga.TextInput(style=Pack(flex=1))

        Peca_box = toga.Box(style=Pack(direction=COLUMN, padding=5))
        Peca_box.add(Peca_label)
        Peca_box.add(self.Peca_input)

        # Colocar as quantidades
        Quantidade_label = toga.Label(
            "Quantidade",
            style=Pack(padding=(10),text_align='left', color="black"),
        )
        self.Quantidade_input = toga.TextInput(style=Pack(flex=1))

        Quantidade_box = toga.Box(style=Pack(direction=COLUMN, padding=5))
        Quantidade_box.add(Quantidade_label)
        Quantidade_box.add(self.Quantidade_input)

        # Colocar os Preços
        Preco_label = toga.Label(
            "Preço",
            style=Pack(padding=(10), text_align='left', color="black"),
        )
        self.Preco_input = toga.TextInput(style=Pack(flex=1))

        Preco_box = toga.Box(style=Pack(direction=COLUMN, padding=5))
        Preco_box.add(Preco_label)
        Preco_box.add(self.Preco_input)

        # Botão de registrar
        button = toga.Button(
            "Registrar",
            on_press=self.registrar,
            style=Pack(flex=1, padding=5),
        )
        
        #Função para Downloud
        Downloud = toga.Button(
            "Downloud",
            on_press=self.baixar,
            style=Pack(flex=1, padding=5),
        )

        #Vai apertar para aparecer uma tela onde vai confirma se ralmente quer resetar o arquivo .csv
        Tela_Resetar = toga.Button(
            'Apagar Planilha',
            on_press=self.Resetar,
            style=Pack(flex=1, padding=5), 
        )


        #Coloca dentro da caixa com os botões principais
        button_box = toga.Box(style=Pack(direction=ROW, padding=10))
        button_box.add(button)
        button_box.add(Downloud)


        #Coloca dentro da caixa para aparecer a tela ou ser execultado. 
        main_box.add(image_view)
        main_box.add(Escolha_box)
        main_box.add(Peca_box)
        main_box.add(Quantidade_box)
        main_box.add(Preco_box)
        main_box.add(button_box)
        main_box.add(Tela_Resetar)


        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    # Função que pega as informações e coloca na planilha.
    def registrar(self, widget):
        # Pegar data e hora atual
        Pegar_dia = time.localtime()
        dia = Pegar_dia.tm_mday
        mes = Pegar_dia.tm_mon
        ano = Pegar_dia.tm_year

        Pegar_hora = time.localtime()
        hora = Pegar_hora.tm_hour
        minuto = Pegar_hora.tm_min
        segundo = Pegar_hora.tm_sec

        # Formatar a data e hora
        Formatar_Data = f'{dia}/{mes}/{ano}'
        Formatar_Hora = f'{hora}:{minuto}:{segundo}'

        # Pegar as informações dos inputs
        Escolha_maquina = self.Maquina_Select.value
        Peca = self.Peca_input.value
        Quantidade = self.Quantidade_input.value
        Preco = self.Preco_input.value

        # Imprimir os valores para depuração
        print(f"Data: {Formatar_Data}, Hora: {Formatar_Hora}")
        print(f"Maquina: {Escolha_maquina}, Peça: {Peca}, Quantidade: {Quantidade}, Preço: {Preco}")

        # Criar um dicionário com os dados para adicionar no CSV
        dados = {
            'Data': [Formatar_Data],
            'Hora': [Formatar_Hora],
            'Máquina': [Escolha_maquina],
            'Peça': [Peca],
            'Quantidade': [Quantidade],
            'Preço': [Preco]
        }

        # Criar o DataFrame com os dados
        df = pd.DataFrame(dados)

        # Nome do arquivo CSV
        nome_arquivo = "registro_de_compras.csv"

        # Caminho completo do arquivo
        diretorio = "/storage/emulated/0/Documents/RKM/"
        arquivo_csv = os.path.join(diretorio, nome_arquivo)

        # Garantir que a pasta exista
        if not os.path.exists(diretorio):
            os.makedirs(diretorio)  # Cria a pasta caso não exista

        # Verificar se o arquivo já existe
        if os.path.exists(arquivo_csv):
            # Se o arquivo existe, adiciona os dados sem cabeçalho
            print("Adicionando ao arquivo CSV existente.")
            df.to_csv(arquivo_csv, mode='a', header=False, index=False, sep=';')
        else:
            # Se o arquivo não existir, cria o arquivo com cabeçalho
            print("Criando novo arquivo CSV.")
            df.to_csv(arquivo_csv, mode='w', header=True, index=False, sep=';')

        self.Peca_input.value = ''      
        self.Quantidade_input.value = '' 
        self.Preco_input.value = ''      
        print("Os campos foram limpos!")

        # Exibir no console a confirmação do registro
        print(f"Registrado:\n Máquina: {Escolha_maquina}\n Peça = {Peca}\n Quantidade = {Quantidade}\n Preço = R$ {Preco}")
        #============================================================================#
    
    def baixar(self, widget):
        # Caminho do arquivo original
        arquivo_original = os.path.expanduser('/storage/emulated/0/Documents/RKM/registro_de_compras.csv')

        # Caminho da cópia, incluindo o nome do arquivo
        pasta_download = '/storage/emulated/0/Download'
        arquivo_copia = os.path.join(pasta_download, 'registro_de_compras.csv')

        # Garantir que a pasta de download exista
        if not os.path.exists(pasta_download):
            os.makedirs(pasta_download)

        # Verificar se o arquivo original existe
        if os.path.exists(arquivo_original):
            try:
                shutil.copy(arquivo_original, arquivo_copia)
                print("Baixado com sucesso! O arquivo está na sua pasta de Download")
            except Exception as e:
                print(f"Erro ao copiar o arquivo: {e}")
        else:
            print(f"Erro: O arquivo {arquivo_original} não foi encontrado.")

    def Resetar(self, widget, **kwargs):
        ask_a_question = toga.QuestionDialog("Olá", "Tem certeza que deseja fazer isso? Recomendamos que você faça um backup antes de apagar a planilha para evitar a perda de dados. Caso faça um novo registro, uma nova planilha será criada automaticamente.")

        task = asyncio.create_task(self.main_window.dialog(ask_a_question))
        task.add_done_callback(self.dialog_dismissed)
    
    def dialog_dismissed(self, task):
        if task.result():
            # Caminho absoluto para o arquivo no Android
            caminho_arquivo = "/storage/emulated/0/Documents/RKM/registro_de_compras.csv"

            # Verificar se o diretório existe
            if os.path.exists(caminho_arquivo):
                try:
                    os.remove(caminho_arquivo)  # Apaga o arquivo
                    print("Sucesso", "O arquivo CSV foi apagado com sucesso!")
                except Exception as e:
                    print(f"Erro ao apagar o arquivo: {e}")
            else:
                print("Erro", "O arquivo CSV não foi encontrado!")
        else:
            print("Sempre faça Backup ")

def main():
    return Duck() 