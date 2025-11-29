from fasthtml.common import *
import json


def tape_snapshot_view(entrada_original: str, pos: int, estado: str):
    if not entrada_original:
        cells = [
            Div("@", Cls="tape-cell"),
            Div("", Cls="tape-cell"),
        ]
        idx = 0 if pos <= 0 else 1
        arrows = [
            Div("▲" if i == idx else "", Cls="tape-arrow-cell")
            for i in range(2)
        ]
    else:
        n_sym = len(entrada_original)
        n = n_sym + 2
        cells = []
        for i in range(n):
            if i == 0:
                cells.append(Div("@", Cls="tape-cell"))
            elif 1 <= i <= n_sym:
                cells.append(Div(entrada_original[i-1], Cls="tape-cell"))
            else:
                cells.append(Div("", Cls="tape-cell"))
        idx = min(max(pos, 0), n - 1)
        arrows = [
            Div("▲" if i == idx else "", Cls="tape-arrow-cell")
            for i in range(n)
        ]
    fita = Div(
        Div(*cells, Cls="tape-row"),
        Div(*arrows, Cls="tape-row"),
        Cls="tape-fita",
    )
    label = f"Estado: {estado}" if estado else ""
    return Div(
        fita,
        Span(label, Cls="tape-estado"),
        Cls="tape-snapshot",
    )


def mainLayout(): 
    return Title("Simulador de Automatos com Pilha"), \
Link(rel="preconnect", href="https://fonts.googleapis.com"), \
        Link(rel="preconnect", href="https://fonts.gstatic.com", crossorigin=""), \
        Link(href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700&display=swap", rel="stylesheet"), \
        Main(
            Style("""
    body {
        padding-bottom: 400px; 
        font-family: 'Nunito', sans-serif; 
        background-color: #ffff; 
        color: #414141; 
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Nunito', sans-serif;
        color: #414141; 
    }

    /* Inputs e Textareas */
    input, textarea {
        background-color: #ffffff !important;
        color: #414141 !important;
        border: 1px solid #AEAEAE;
        font-family: 'Nunito', sans-serif; /* Garante fonte nos inputs */
    }
    
    /* Botões */
    button { 
        cursor: pointer; 
        background: #5C5C5C; 
        color: white; 
        border: none; 
        padding: 10px 20px; 
        border-radius: 2px; 
        font-weight: bold; 
        font-family: 'Nunito', sans-serif; /* Garante fonte no botão */
    }
    button:hover { background: #5C5C5C; }

    /* Layout Grid */
    .form-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 30px;
        margin-bottom: 30px;
        align-items: start;
    }
    
    @media (max-width: 768px) {
        .form-grid { grid-template-columns: 1fr; }
    }

    .left-col {
        background: #E6E6E6;
        padding: 20px;
        border-radius: 6px;
        border: 1px solid #AEAEAE;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }

    .right-col {
        background: #E6E6E6;
        padding: 20px;
        border-radius: 6px;
        border: 1px solid #AEAEAE;
        height: 100%;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }

    .simulacao-box {
        max-width: 600px;
        margin: 0 auto;
        background: #E6E6E6;
        padding: 20px;
        border: 1px solid #AEAEAE;
        border-radius: 6px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    /* Estilos de Erro e Simulação */
    .error-message{color:#d32f2f}
    .error-message h3{color:#d32f2f}
    .error-message ul{color:#d32f2f}
    
    .exec-grid{display:flex;gap:24px;align-items:flex-start;margin:12px 0}
    
    .stack-wrapper{min-width:90px}
    .stack-box{display:flex;flex-direction:column;gap:4px;border:2px solid #6b5b3e;
               padding:6px;background:#fff8e1; border-radius:6px}
    .stack-cell{width:64px;height:32px;border:2px solid #6b5b3e;border-radius:4px;
                display:flex;align-items:center;justify-content:center;
                background:#ffecb3;color:#4e342e;font-size:14px;font-weight:700;
                font-family: 'Nunito', sans-serif;}

    .history-wrapper ul{margin:8px 0 0 18px}
    .controls{margin-top:12px}
    .tape-wrapper{margin-top:8px}
    .tape-snapshot{display:flex;align-items:flex-start;gap:8px;margin-bottom:2px}
    .tape-row{display:flex;gap:4px}
    
    .tape-cell{min-width:24px;height:26px;background:#5C5C5C;color:#fff;
               display:flex;align-items:center;justify-content:center;
               border-radius:2px;font-size:14px;padding:0 4px;
               font-family: monospace;} /* Fita geralmente fica melhor com monospace, mas pode mudar para Nunito se quiser */
               
    .tape-arrow-cell{min-width:24px;height:18px;display:flex;
                     align-items:flex-start;justify-content:center;color:#414141}
    .tape-estado{min-width:80px;font-weight:600;line-height:26px; color: #414141;}
    
    .sim-mode{margin:8px 0 20px 0}
    .sim-mode label{margin:0 4px 0 8px;cursor:pointer; color: #414141;}
    .sim-mode input[type="radio"]{cursor:pointer}
    .controls{display:flex;gap:8px;margin-top:12px}
    
    textarea { 
        width: 100%; box-sizing: border-box; resize: vertical; 
        background: #fff; color: #414141; border: 1px solid #ccc; padding: 8px;
    }
    input[type="text"] { 
        width: 100%; box-sizing: border-box; margin-bottom: 10px; 
        background: #fff; color: #414141; border: 1px solid #ccc; padding: 8px;
    }
    label { color: #414141; font-weight: 500; }
"""),
            H1("Simulador de Pilha em tempo real", Style="text-align: center; color: #414141;"),
            P("Trabalho da disciplina de Computabilidade", Style="text-align: center; color: #666; margin-bottom: 30px;"),
            
        Form(
            Div(
                Div(
                    H2("Definição do Autômato"),
                    Div(
                        Label("Estados (Q) (Separados por vírgula): "),
                        Input(name = "EstadosPilha", value = "q0,q1,q3"),
                    ),
                    Div(
                        Label("Alfabeto de Entrada (Σ):"),
                        Input(name = "AlfabetoEntrada", value = "a,b"),
                    ),
                    Div(
                        Label("Alfabeto Pilha: "),
                        Input(name = "alfabetoPilha", value = "A, Z"),
                    ),
                    Div(
                        Label("Estado inicial: "),
                        Input(name = "estadoInicial", value = "q0"),
                    ),
                    Div(
                        Label("Estado(s) final(is): "),
                        Input(name = "estadosFinais", value = "q2"),
                    ),
                    Cls="left-col"
                ),
                
                Div(
                    H2("Transições"),
                    P("Observação: 'eps' representa o símbolo vazio (ε).", Style="font-size: 0.9em; color: #555;"),
                    P("Formato: q0,a,Z;q0,A", Style="font-size: 0.9em; color: #555;"),
                    Textarea(
                        name = "transicoes_raw",
                        rows = 12,
                        value = "q0,a,Z;q0,A / q0,a,A;q0,A / q0,b,A;q1,eps / q1,b,A;q1,eps / q1,eps,Z;q2,eps"
                    ),
                    Cls="right-col"
                ),
                Cls="form-grid"
            ),

            Div(
                H2("Simulação"),
                Div(
                    Label("Entrada: "),
                    Input(name = "sentenca", value = "aabb"),
                ),
                Div(
                    Label("Modo: "),
                    Input(type="radio", name="modo_simulacao", value="passo", id="modo-passo", checked=True),
                    Label("Passo a passo", For="modo-passo"),
                    Input(type="radio", name="modo_simulacao", value="automatico", id="modo-automatico"),
                    Label("Simulação automática", For="modo-automatico"),
                    Cls="sim-mode"
                ),
                Button("Iniciar Simulação", value = "submit", Style="width: 100%"),
                Cls="simulacao-box"
            ),

            hx_post = "/inicia-simulacao",
            hx_target = "#simulacao-container",
            hx_swap = "innerHTML"
        ),
        
        Div(
            id = "simulacao-container",
            Cls = "container",
            Style = "margin-top: 40px;"
        ),

        Cls = "container"
        )

def simulatorView(estadoAtual, pilha, entrada, defineAutomato, show_controls: bool = True, modo: str = "passo"):
    pilhaSerializada = json.dumps(pilha)
    definicaoSerializada = json.dumps(defineAutomato)
    historico = defineAutomato.get("history", [])
    entrada_original = defineAutomato.get("entradaOriginal", "")

    min_slots = 5
    slots = max(min_slots, len(pilha))
    filled = [""] * (slots - len(pilha)) + list(pilha) 
    stack_cells = [Div(Strong(sym) if sym else "", Cls="stack-cell") for sym in filled]
    stack_view = Div(H3("Pilha"), Div(*stack_cells, Cls="stack-box"), Cls="stack-wrapper")

    snapshots = [
        tape_snapshot_view(entrada_original, step.get("pos", 0), step.get("estado", ""))
        for step in historico
    ]
    history_view = Div(
        H3("Histórico da fita"),
        Div(*snapshots, Cls="tape-wrapper"),
        Cls="history-wrapper"
    )

    controls = None
    if show_controls:
        if modo == "passo":
            controls = Form(
                Input(type="hidden", name="exec_estado", value=estadoAtual),
                Input(type="hidden", name="exec_pilha", value=pilhaSerializada),
                Input(type="hidden", name="exec_entrada", value=entrada),
                Input(type="hidden", name="exec_definicao", value=definicaoSerializada),
                Input(type="hidden", name="exec_history", value=json.dumps(historico)),
                Input(type="hidden", name="modo_simulacao", value="passo"),
                Button("Próximo passo", value="next"),
                hx_post = "/proximo-passo",
                hx_target = "#simulacao-container",
                hx_swap = "innerHTML",
                Cls = "controls"
            )
        else:
            controls = Form(
                Input(type="hidden", name="exec_estado", value=estadoAtual),
                Input(type="hidden", name="exec_pilha", value=pilhaSerializada),
                Input(type="hidden", name="exec_entrada", value=entrada),
                Input(type="hidden", name="exec_definicao", value=definicaoSerializada),
                Input(type="hidden", name="exec_history", value=json.dumps(historico)),
                Input(type="hidden", name="modo_simulacao", value="automatico"),
                Cls = "controls"
            )

    return Div(
        H2("Execução"),
        Div(stack_view, history_view, Cls = "exec-grid"),
        controls if controls is not None else "",
        id = "simulacao-container",
        Cls = "container"
    )