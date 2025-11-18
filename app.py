from fasthtml.common import *
import json
from componentes import mainLayout, simulatorView
from automato import PushdownAutomaton, Transition, EPS

app, rt = fast_app()


@rt("/")
def get_index():
    return mainLayout()


@rt("/inicia-simulacao")
def post_inicia_simulacao(EstadosPilha:str, AlfabetoEntrada:str, alfabetoPilha:str,
                          estadoInicial:str, estadosFinais:str,
                          transicoes_raw:str = "", sentenca:str = "", modo_simulacao:str = "passo"):

    erros_campos = []
    if not EstadosPilha or not EstadosPilha.strip():
        erros_campos.append("O campo 'Estados (Q)' é obrigatório.")
    if not AlfabetoEntrada or not AlfabetoEntrada.strip():
        erros_campos.append("O campo 'Alfabeto de Entrada (Σ)' é obrigatório.")
    if not alfabetoPilha or not alfabetoPilha.strip():
        erros_campos.append("O campo 'Alfabeto Pilha' é obrigatório.")
    if not estadoInicial or not estadoInicial.strip():
        erros_campos.append("O campo 'Estado inicial' é obrigatório.")
    if not estadosFinais or not estadosFinais.strip():
        erros_campos.append("O campo 'Estado(s) final(is)' é obrigatório.")
    if not transicoes_raw or not transicoes_raw.strip():
        erros_campos.append("O campo 'Transições' é obrigatório.")
    
    if erros_campos:
        return Div(
            H3("Erros: Campos obrigatórios não preenchidos"),
            Ul(*[Li(err) for err in erros_campos]),
            id = "simulacao-container",
            Cls = "container error-message"
        )

    estados = [s.strip() for s in EstadosPilha.split(",") if s.strip()]
    alfa_entrada = [s.strip() for s in AlfabetoEntrada.split(",") if s.strip()]
    alfa_pilha = [s.strip() for s in alfabetoPilha.split(",") if s.strip()]
    finais = [s.strip() for s in estadosFinais.split(",") if s.strip()]
    start_stack = alfa_pilha[-1] if alfa_pilha else "Z"

    try:
        transitions = PushdownAutomaton.parse_transitions(transicoes_raw)
    except ValueError as e:
        return Div(
            H3("Erro ao processar transições"),
            P(str(e)),
            id = "simulacao-container",
            Cls = "container error-message"
        )
    if not transitions:
        return Div(
            H3("Erro: Transições não definidas"),
            P("Defina transições válidas no formato q,a,X;q',Γ (use 'eps' p/ ε)."),
            id = "simulacao-container",
            Cls = "container error-message"
        )

    validation_errors = PushdownAutomaton.validate_definition(
        estados, alfa_entrada, alfa_pilha, estadoInicial, finais, transitions, sentenca or ""
    )
    if validation_errors:
        return Div(
            H3("Erros de validação"),
            Ul(*[Li(err) for err in validation_errors]),
            id = "simulacao-container",
            Cls = "container error-message"
        )

    pda = PushdownAutomaton(estados, alfa_entrada, alfa_pilha, estadoInicial, finais, start_stack, transitions)

    estado0, pilha0, entrada0 = pda.initial_configuration(sentenca or "")
    definicao = {
        "EstadosPilha": estados,
        "AlfabetoEntrada": alfa_entrada,
        "alfabetoPilha": alfa_pilha,
        "estadoInicial": estadoInicial,
        "estadosFinais": finais,
        "startStack": start_stack,
        "transicoes_raw": transicoes_raw,
        "entradaOriginal": sentenca or "",
        "history": [{"pos": 0, "estado": ""}]
    }
    return simulatorView(estado0, pilha0, entrada0, definicao, modo=modo_simulacao)


@rt("/proximo-passo")
def post_proximo_passo(exec_estado:str, exec_pilha:str, exec_entrada:str, exec_definicao:str, exec_history:str = "[]", modo_simulacao:str = "passo"):
    data = json.loads(exec_definicao)
    transitions = PushdownAutomaton.parse_transitions(data.get("transicoes_raw",""))
    pda = PushdownAutomaton(
        data.get("EstadosPilha", []),
        data.get("AlfabetoEntrada", []),
        data.get("alfabetoPilha", []),
        data.get("estadoInicial", ""),
        data.get("estadosFinais", []),
        data.get("startStack", "Z"),
        transitions
    )
    pilha = json.loads(exec_pilha)
    step = pda.step(exec_estado, pilha, exec_entrada or "")
    if step is None:
        accepted = pda.is_accepted(exec_estado, pilha, exec_entrada or "")
        result = "ACEITA" if accepted else "REJEITADA"
        try:
            history = json.loads(exec_history)
        except Exception:
            history = []
        original = data.get("entradaOriginal", "")
        entrada_restante = exec_entrada or ""
        if entrada_restante == "":
            pos_final = len(original) + 1
            ultima_pos = history[-1].get("pos", -1) if history else -1
            if ultima_pos != pos_final:
                history.append({"pos": pos_final, "estado": exec_estado})
        else:
            caracteres_processados = len(original) - len(entrada_restante)
            if caracteres_processados <= 0:
                pos_na_fita = 1
            elif caracteres_processados > len(original):
                pos_na_fita = len(original)
            else:
                pos_na_fita = caracteres_processados
            pos_final_vazio = len(original) + 1
            history = [h for h in history if h.get("pos", -1) != pos_final_vazio and h.get("pos", -1) <= pos_na_fita]
            if history:
                history[-1] = {"pos": pos_na_fita, "estado": exec_estado}
            else:
                history.append({"pos": pos_na_fita, "estado": exec_estado})
        data["history"] = history
        return Div(
            H2("Execução finalizada"),
            P(f"Resultado: {result}"),
            simulatorView(exec_estado, pilha, exec_entrada or "", data, False),
            id = "simulacao-container",
            Cls = "container"
        )
    estado1, pilha1, entrada1 = step
    try:
        history = json.loads(exec_history)
    except Exception:
        history = []
    original = data.get("entradaOriginal", "")

    if entrada1 != exec_entrada:
        pos_novo = len(original) - len(entrada1 or "")
        if pos_novo < 1:
            pos_novo = 1
        elif pos_novo > len(original):
            pos_novo = len(original)
        history.append({"pos": pos_novo, "estado": estado1})

    if pda.is_accepted(estado1, pilha1, entrada1 or ""):
        pos_final = len(original) + 1
        history.append({"pos": pos_final, "estado": estado1})
        data["history"] = history
        return Div(
            H2("Execução finalizada"),
            P(f"Resultado: ACEITA"),
            simulatorView(estado1, pilha1, entrada1 or "", data, False),
            id = "simulacao-container",
            Cls = "container"
        )

    data["history"] = history
    return simulatorView(estado1, pilha1, entrada1, data, modo=modo_simulacao)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)


