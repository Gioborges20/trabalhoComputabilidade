#Arquivo que armazenará as funções que geram HTML
#bibliotecas que serão utilizadas
from fasthtml.common import *
import json

#iniciação da estrutura da para para sua conversão em HTML
def mainLayout(): 
    return Title("Simulador de Automatos com Pilha"), \
        Main(
            H1("Simulador de Pilha em tempo real"),
            P("Trabalho da disciplina de Computabilidade"),
        #Formulário para a coleta de dados do usuário
        Form(
            H2("Definição do Autômato"),
            #Entrada dos estados
            Div(
                Label("Estados (Q) (Separados por vírgula): "),
                Input(name = "EstadosPilha", value = "q0, q1, q2"),
            ),
            #Entrada do alfabeto
            Div(
                Label("Alfabeto de Entrada (Σ):"),
                Input(name = "AlfabetoEntrada", value = "a, b,"),
            ),
            #O alfabeto, as letras que estão na pilha
            Div(
                Label("Alfabeto Pilha: "),
                Input(name = "alfabetoPilha", value = "A, Z"),
            ),
            # Estado inicial do autômato
            Div(
                Label("Estado inicial: "),
                Input(name = "estadoInicial", value = "q0"),
            ),
            Div(
                Label("Estados finais: "),
                Input(name = "estadosFinais", value = "q2"),
            ),
            H2("Transições"),
            P("Formato: q0,a,Z;q0,AZ / q0,b,A;q1,esp"),
            Textarea(
                name = "transicoes_raw",
                rows = 5,
                cols = 70,
                value = "q0,a,Z,AZ;q0,AZ/q0,a,A;q0,AA/q0,b,A;q1,esp/q1,b,A;q1,eps/q1,eps,Z;q2,eps"
            ),

            H2("simulação"),
            Div(
                Label("Entrada: "),
                Input(name = "sentenca", value = "aabb"),
            ),
            Button("Iniciar Simulação", value = "submit"),

            hx_post = "/inicia-simulacao",
            hx_target = "#simulacao-container",
            hx_swap = "innerHTML"
        ),
        Div(
            id = "simulador-container",
            Cls = "container")

        Cls = "container"
        )

def simulatorView(estadoAtual, pilha, entrada, defineAutomato):
    pilhaSerializada = json.dumps(pilha)
    definicaoSerializada = json.dumps(defineAutomato)

    return Div()