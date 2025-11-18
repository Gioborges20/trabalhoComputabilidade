from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple, Dict, Optional

EPS = "eps"
QMARK = "?"

@dataclass(frozen=True)
class Transition:
    from_state: str
    input_symbol: str  
    stack_top: str     
    to_state: str
    stack_push: str    


class PushdownAutomaton:
    def __init__(
        self,
        states: List[str],
        input_alphabet: List[str],
        stack_alphabet: List[str],
        initial_state: str,
        final_states: List[str],
        start_stack_symbol: str = "Z",
        transitions: Optional[List[Transition]] = None,
    ) -> None:
        self.states = states
        self.input_alphabet = input_alphabet
        self.stack_alphabet = stack_alphabet
        self.initial_state = initial_state
        self.final_states = set(final_states)
        self.start_stack_symbol = start_stack_symbol
        self.transitions = transitions or []

        self._index: Dict[Tuple[str, str, str], List[Transition]] = {}
        for t in self.transitions:

            if t.input_symbol not in (QMARK,) and t.stack_top not in (QMARK, EPS):
                self._index.setdefault((t.from_state, t.input_symbol, t.stack_top), []).append(t)
            if t.stack_top == EPS and t.input_symbol not in (QMARK,):
                self._index.setdefault((t.from_state, t.input_symbol, ""), []).append(t)

    @staticmethod
    def parse_transitions(raw: str) -> List[Transition]:
        if not raw:
            return []
        parts = [p.strip() for p in raw.replace("\n", "/").split("/") if p.strip()]
        transitions: List[Transition] = []
        for part in parts:
            if ";" not in part:
                continue
            left, right = part.split(";", 1)
            left_items = [s.strip() for s in left.split(",")]
            right_items = [s.strip() for s in right.split(",")]
            if len(left_items) != 3 or len(right_items) != 2:
                continue
            q_from, a_in, x_top = left_items
            q_to, gamma = right_items
            a_in = a_in if a_in else EPS
            a_in = EPS if a_in.lower() in ("eps", "ε") else a_in
            gamma = "" if gamma.lower() in ("eps", "ε") else gamma
            if len(gamma) > 1:
                raise ValueError(f"Empilhar mais de 1 símbolo não é permitido: '{part}'")
            transitions.append(Transition(q_from, a_in, x_top, q_to, gamma))
        return transitions

    @staticmethod
    def validate_definition(
        states: List[str],
        input_alphabet: List[str],
        stack_alphabet: List[str],
        initial_state: str,
        final_states: List[str],
        transitions: List[Transition],
        input_string: str
    ) -> List[str]:
        errors: List[str] = []
        state_set = set(states)
        input_set = set(input_alphabet)
        stack_set = set(stack_alphabet)

        if not initial_state or initial_state not in state_set:
            errors.append(f"Estado inicial inválido: '{initial_state}'.")
        missing_finals = [q for q in final_states if q not in state_set]
        if missing_finals:
            errors.append(f"Estados finais inexistentes: {', '.join(missing_finals)}.")

        for t in transitions:
            if t.from_state not in state_set:
                errors.append(f"Transição usa estado inexistente (origem): {t.from_state}.")
            if t.to_state not in state_set:
                errors.append(f"Transição usa estado inexistente (destino): {t.to_state}.")
            if t.input_symbol not in (EPS, QMARK) and t.input_symbol not in input_set:
                errors.append(f"Símbolo de entrada inválido na transição: {t.input_symbol}.")
            if t.stack_top not in (QMARK, EPS) and t.stack_top not in stack_set:
                errors.append(f"Topo de pilha inválido na transição: {t.stack_top}.")
            if t.stack_push != "" and t.stack_push not in stack_set:
                errors.append(f"Símbolo a empilhar inválido na transição: {t.stack_push}.")

        for ch in input_string:
            if ch not in input_set:
                errors.append(f"Caractere da entrada fora do alfabeto: '{ch}'.")

        return errors

    def initial_configuration(self, input_string: str) -> Tuple[str, List[str], str]:
        stack = []
        return self.initial_state, stack, input_string

    def _matching_transitions(self, state: str, input_symbol: str, stack: List[str]) -> List[Transition]:
        candidates: List[Transition] = []

        stack_top = stack[-1] if stack else ""
        candidates.extend(self._index.get((state, input_symbol, stack_top), []))
        candidates.extend(self._index.get((state, EPS, stack_top), []))
        if stack_top == "":
            candidates.extend(self._index.get((state, input_symbol, ""), []))
            candidates.extend(self._index.get((state, EPS, ""), []))

        for t in self.transitions:
            if t.from_state != state:
                continue
            stack_empty = (len(stack) == 0)
            input_empty = (len(input_symbol) == 0)

            if t.stack_top == QMARK:
                stack_ok = stack_empty
            elif t.stack_top == EPS:
                stack_ok = True  
            else:
                stack_ok = (len(stack) > 0 and stack[-1] == t.stack_top)

            if not stack_ok:
                continue

    
            if t.input_symbol == QMARK:
                input_ok = input_empty
            elif t.input_symbol == EPS:
                input_ok = True
            else:
                input_ok = (len(input_symbol) > 0 and input_symbol == t.input_symbol)

            if input_ok:
                if t not in candidates:
                    candidates.append(t)

        return candidates

    def step(self, state: str, stack: List[str], input_remaining: str) -> Optional[Tuple[str, List[str], str]]:
        current_symbol = input_remaining[0] if input_remaining else ""

        candidates = []
        candidates.extend(self._matching_transitions(state, current_symbol, stack))

        if not candidates:
            return None

        t = candidates[0]
        if t.stack_top in (QMARK, EPS):
            new_stack = list(stack)
        else:
            new_stack = stack[:-1]
        if t.stack_push != "":
            new_stack.append(t.stack_push)
        new_state = t.to_state
        new_input = input_remaining
        if t.input_symbol not in (EPS, QMARK) and new_input:
            new_input = new_input[0+1:] 
        return new_state, new_stack, new_input

    def is_accepted(self, state: str, stack: List[str], input_remaining: str) -> bool:
        return (len(input_remaining) == 0) and (state in self.final_states)

