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
        Main(
            Style("""
            body{padding-bottom:400px}
            .error-message{color:#ff4444}
            .error-message h3{color:#ff4444}
            .error-message ul{color:#ff4444}
            .error-message li{color:#ff4444}
            .exec-grid{display:flex;gap:24px;align-items:flex-start;margin:12px 0}
            .stack-wrapper{min-width:90px}
            .stack-box{display:flex;flex-direction:column;gap:4px;border:2px solid #6b5b3e;
                       padding:6px;background:#2a2f38;border-radius:6px}
            .stack-cell{width:64px;height:32px;border:2px solid #6b5b3e;border-radius:4px;
                        display:flex;align-items:center;justify-content:center;
                        background:#3a3f48;color:#f4f4f4;font-size:14px;font-weight:700}
            .history-wrapper ul{margin:8px 0 0 18px}
            .controls{margin-top:12px}
            .tape-wrapper{margin-top:8px}
            .tape-snapshot{display:flex;align-items:flex-start;gap:8px;margin-bottom:2px}
            .tape-row{display:flex;gap:4px}
            .tape-cell{min-width:24px;height:26px;background:#3569b1;color:#fff;
                       display:flex;align-items:center;justify-content:center;
                       border-radius:2px;font-size:14px;padding:0 4px}
            .tape-arrow-cell{min-width:24px;height:18px;display:flex;
                             align-items:flex-start;justify-content:center;color:#fff}
            .tape-estado{min-width:80px;font-weight:600;line-height:26px}
            .sim-mode{margin:8px 0 20px 0}
            .sim-mode label{margin:0 4px 0 8px;cursor:pointer}
            .sim-mode input[type="radio"]{cursor:pointer}
            .controls{display:flex;gap:8px;margin-top:12px}
            """),
            Script("""
                window.autoSimInterval = null;
                function verificarEExecutarAuto() {
                    const container = document.getElementById('simulacao-container');
                    if (!container) return;
                    
                    const isFinalizada = container.innerHTML.includes('Execução finalizada');
                    if (isFinalizada) {
                        if (window.autoSimInterval) {
                            clearInterval(window.autoSimInterval);
                            window.autoSimInterval = null;
                        }
                        return;
                    }
                    
                    const form = container.querySelector('form');
                    if (!form) return;
                    
                    const modoInput = form.querySelector('input[name="modo_simulacao"]');
                    if (!modoInput || modoInput.value !== 'automatico') {
                        if (window.autoSimInterval) {
                            clearInterval(window.autoSimInterval);
                            window.autoSimInterval = null;
                        }
                        return;
                    }
                    
                    if (window.autoSimInterval) return;
                    
                    let primeiroPasso = true;
                    window.autoSimInterval = setInterval(function() {
                        if (primeiroPasso) {
                            primeiroPasso = false;
                            return;
                        }
                        const containerEl = document.getElementById('simulacao-container');
                        if (!containerEl) {
                            clearInterval(window.autoSimInterval);
                            window.autoSimInterval = null;
                            return;
                        }
                        
                        const isFinalizada = containerEl.innerHTML.includes('Execução finalizada');
                        if (isFinalizada) {
                            clearInterval(window.autoSimInterval);
                            window.autoSimInterval = null;
                            return;
                        }
                        
                        const formEl = containerEl.querySelector('form');
                        if (!formEl) {
                            const isFinalizada = containerEl.innerHTML.includes('Execução finalizada');
                            if (isFinalizada) {
                                clearInterval(window.autoSimInterval);
                                window.autoSimInterval = null;
                            }
                            return;
                        }
                        
                        const estado = formEl.querySelector('input[name="exec_estado"]')?.value;
                        const pilha = formEl.querySelector('input[name="exec_pilha"]')?.value;
                        const entrada = formEl.querySelector('input[name="exec_entrada"]')?.value;
                        const definicao = formEl.querySelector('input[name="exec_definicao"]')?.value;
                        const history = formEl.querySelector('input[name="exec_history"]')?.value;
                        
                        if (!estado || pilha === undefined || entrada === undefined || !definicao) {
                            const isFinalizada = containerEl.innerHTML.includes('Execução finalizada');
                            if (isFinalizada) {
                                clearInterval(window.autoSimInterval);
                                window.autoSimInterval = null;
                            }
                            return;
                        }
                        
                        const formData = new FormData();
                        formData.append('exec_estado', estado);
                        formData.append('exec_pilha', pilha);
                        formData.append('exec_entrada', entrada);
                        formData.append('exec_definicao', definicao);
                        formData.append('exec_history', history || '[]');
                        formData.append('modo_simulacao', 'automatico');
                        
                        fetch('/proximo-passo', {
                            method: 'POST',
                            body: formData
                        })
                        .then(r => r.text())
                        .then(html => {
                            const containerEl = document.getElementById('simulacao-container');
                            if (!containerEl) return;
                            
                            containerEl.innerHTML = html;
                            
                            const scripts = containerEl.querySelectorAll('script');
                            scripts.forEach(oldScript => {
                                const newScript = document.createElement('script');
                                if (oldScript.src) {
                                    newScript.src = oldScript.src;
                                } else {
                                    newScript.textContent = oldScript.textContent;
                                }
                                oldScript.parentNode.replaceChild(newScript, oldScript);
                            });
                            
                            const isFinalizada = containerEl.innerHTML.includes('Execução finalizada');
                            if (isFinalizada && window.autoSimInterval) {
                                clearInterval(window.autoSimInterval);
                                window.autoSimInterval = null;
                            }
                        })
                        .catch(err => {
                            console.error(err);
                            clearInterval(window.autoSimInterval);
                            window.autoSimInterval = null;
                        });
                    }, 500);
                }
                
                let iniciouAuto = false;
                function iniciarVerificacaoAuto() {
                    if (iniciouAuto) return;
                    iniciouAuto = true;
                    setTimeout(function() {
                        setInterval(verificarEExecutarAuto, 100);
                        verificarEExecutarAuto();
                    }, 2000);
                }
                
                setInterval(function() {
                    const container = document.getElementById('simulacao-container');
                    if (container && container.querySelector('form input[name="modo_simulacao"][value="automatico"]')) {
                        if (!iniciouAuto && !window.autoSimInterval) {
                            iniciarVerificacaoAuto();
                        }
                    }
                }, 100);
                
                document.addEventListener('htmx:afterSwap', function(evt) {
                    if (evt.detail.target.id === 'simulacao-container') {
                        iniciouAuto = false;
                        if (window.autoSimInterval) {
                            clearInterval(window.autoSimInterval);
                            window.autoSimInterval = null;
                        }
                        setTimeout(function() {
                            iniciarVerificacaoAuto();
                        }, 2000);
                    }
                });
            """),
            H1("Simulador de Pilha em tempo real"),
            P("Trabalho da disciplina de Computabilidade"),
        Form(
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
            H2("Transições"),
            P("Observação: 'eps' representa o símbolo vazio (ε)."),
            P("Formato exemplo: q0,a,Z;q0,A / q0,b,A;q1,eps"),
            P("q0,a,Z;q0,A -> * q0: Estado atual;"),
            P("q0,a,Z;q0,A -> * 'a': Ler na fita;"),
            P("q0,a,Z;q0,A -> * 'Z': Ler na pilha;"),
            P("q0,a,Z;q0,A -> * q0: Estado destino;"),
            P("q0,a,Z;q0,A -> * 'A': Empilhar na pilha;"),
            Textarea(
                name = "transicoes_raw",
                rows = 3,
                cols = 70,
                value = "q0,a,Z;q0,A / q0,a,A;q0,A / q0,b,A;q1,eps / q1,b,A;q1,eps / q1,eps,Z;q2,eps"
            ),

            H2("simulação"),
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
            Button("Iniciar Simulação", value = "submit"),

            hx_post = "/inicia-simulacao",
            hx_target = "#simulacao-container",
            hx_swap = "innerHTML"
        ),
        Div(
            id = "simulacao-container",
            Cls = "container"),

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