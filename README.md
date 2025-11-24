## COMO INICIAR O PROJETO:

1 - Entre na pasta do projeto 'TRABALHOCOMPUTABILIDADE'
2 - Crie o ambiente virtual: python -m venv .venv 
3 - Ative a venv, no terminal da IDE, com o mando: .\.venv\Scripts\Activate.ps1 
4 - Instale as dependências dentro da venv: pip install -r requeriments
5 - Suba o servidor, com esse comando, dentro da venv: uvicorn app:app --reload --port 8000 
6 - No seu navegador, entre nesse link para acessar o projeto: http://127.0.0.1:8000/


## PARA TESTAR:

1: 
    - Estados: q0,q1,qf
    - Alfabeto de entrada: a,b
    - Alfabeto Pilha: B
    - Estado inicial: q0
    - Estados finais: qf
    - Transições: q0,a,eps;q0,B / q0,b,B;q1,eps / q1,b,B;q1,eps / q1,?,?;qf,eps / q0,?,?;qf,eps
    - Entrada: aabb
    * Resultado: ACEITA *

2: 
    - Estados: q0,q1,qf
    - Alfabeto de entrada: a,b
    - Alfabeto Pilha: B
    - Estado inicial: q0
    - Estados finais: qf
    - Transições: q0,a,eps;q0,B / q0,b,B;q1,eps / q1,b,B;q1,eps / q1,?,?;qf,eps / q0,?,?;qf,eps
    - Entrada: aaab
    * Resultado: REJEITA *

3 (reconhece palavras a^n b a^n):
    - Estados: q0,q1,qf
    - Alfabeto de entrada: a,b
    - Alfabeto Pilha: A,B
    - Estado inicial: q0
    - Estados finais: qf
    - Transições: q0,a,eps;q0,A / q0,b,eps;q1,eps / q1,a,A;q1,eps / q1,?,?;qf,eps
    - Entrada: aabaa
    * Resultado: ACEITA *

4:
    - Estados: q0,q1,qf
    - Alfabeto de entrada: a,b
    - Alfabeto Pilha: A,B
    - Estado inicial: q0
    - Estados finais: qf
    - Transições: q0,a,eps;q0,A / q0,b,eps;q1,eps / q1,a,A;q1,eps / q1,?,?;qf,eps
    - Entrada: aabbaaa
    * Resultado: REJEITA *
