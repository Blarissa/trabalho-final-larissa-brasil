# Conversor de Expressões Regulares para AFN-ε

Projeto de Teoria da Computação que implementa a conversão de Expressões Regulares (ER) para Autômatos Finitos Não Determinísticos com transições epsilon (AFN-ε) utilizando a **Construção de Thompson**.

## Índice

- [Descrição do Projeto](#descrição-do-projeto)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Como Executar](#como-executar)
- [Exemplos de Uso](#exemplos-de-uso)
- [Operadores Suportados](#operadores-suportados)
- [Funcionamento](#funcionamento)
- [Autora](#autora)

---

## Descrição do Projeto

Este projeto implementa um conversor de expressões regulares para AFN-ε com interface web interativa, apresentando as seguintes funcionalidades:

- Conversão de ER para AFN-ε usando Construção de Thompson
- Reconhecimento de cadeias no AFN-ε resultante
- Interface Web moderna e responsiva com Tailwind CSS
- API REST com Flask
- Visualização textual do autômato gerado
- Exportação dos resultados em arquivo texto

---

## Tecnologias Utilizadas

### Backend
- **Python 3.8+**
- **Flask 3.0.0** - Framework web minimalista
- **Flask-CORS 4.0.0** - Gerenciamento de CORS

### Frontend
- **HTML5** - Estrutura da página
- **Tailwind CSS 3.x** - Estilização moderna via CDN
- **JavaScript (ES6+)** - Lógica de interação

---

## Estrutura do Projeto

```
trabalho-final/
│
├── backend/
│   ├── afn_epsilon.py       # Classes Estado e AFNEpsilon
│   ├── conversor_er.py      # Construção de Thompson
│   ├── server.py            # API REST Flask
│   └── requirements.txt     # Dependências Python
│
├── frontend/
│   ├── index.html           # Interface Web
│   └── app.js               # Lógica JavaScript
│
├── venv/                    # Ambiente virtual (não versionado)
├── .gitignore              # Arquivos ignorados
└── README.md               # Documentação
```

---

## Pré-requisitos

### Windows

1. **Python 3.8 ou superior**
   - Baixe em: https://www.python.org/downloads/
   - Durante a instalação, marque "Add Python to PATH"

2. **Verificar instalação:**
   ```bash
   python --version
   pip --version
   ```

3. **Navegador web moderno** (Chrome, Firefox, Edge)

---

### macOS

1. **Python 3.8 ou superior**
   
   **Opção 1: Homebrew (Recomendado)**
   ```bash
   # Instale o Homebrew
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   
   # Instale o Python
   brew install python@3.11
   
   # Verifique
   python3 --version
   pip3 --version
   ```
   
   **Opção 2: Download direto**
   - Acesse: https://www.python.org/downloads/macos/
   - Baixe e execute o instalador `.pkg`

2. **Navegador web moderno** (Safari, Chrome, Firefox)

---

### Linux

#### Ubuntu/Debian

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv

python3 --version
pip3 --version
```

---

## Instalação

### Passo 1: Navegue até a pasta do projeto

**Windows:**
```bash
cd trabalho-final-larissa-brasil
```

**macOS/Linux:**
```bash
cd ~/trabalho-final-larissa-brasil
```

---

### Passo 2: Criar Ambiente Virtual

**Windows:**
```bash
python -m venv venv
```

**macOS/Linux:**
```bash
python3 -m venv venv
```

---

### Passo 3: Ativar Ambiente Virtual

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

Você verá `(venv)` no início do prompt quando estiver ativo.

---

### Passo 4: Instalar Dependências

**Com o ambiente virtual ativado:**

```bash
cd backend
pip install -r requirements.txt
```

**Verificar instalação:**
```bash
pip list
```

Você deve ver Flask e Flask-CORS listados.

---

## Como Executar

### 1. Navegue até a pasta backend

```bash
cd backend
```

---

### 2. Inicie o servidor

```bash
python server.py
```

**Saída esperada:**
```
Servidor iniciado em http://localhost:5000
Acesse o frontend em: http://localhost:5000
 * Serving Flask app 'server'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

**Nota:** O aviso sobre "development server" é normal para uso local/acadêmico.

---

### 3. Acesse no navegador

Abra seu navegador e acesse:
```
http://localhost:5000
```

---

### 4. Para encerrar

Pressione `CTRL + C` no terminal.

Para desativar o ambiente virtual:
```bash
deactivate
```

---

## Exemplos de Uso

### Exemplo 1: Expressão Simples `a|b`

1. Digite no campo "Expressão Regular": `a|b`
2. Clique em "Converter para AFN-ε"
3. Visualize o autômato gerado

**Teste as cadeias:**
- `a` → ACEITA
- `b` → ACEITA
- `ab` → REJEITA
- `c` → REJEITA

---

### Exemplo 2: Fecho de Kleene `a*`

**Expressão:** `a*`

**Teste as cadeias:**
- `ε` (vazio) → ACEITA
- `a` → ACEITA
- `aa` → ACEITA
- `aaa` → ACEITA
- `b` → REJEITA

---

### Exemplo 3: Expressão Complexa `(a|b)*abb`

**Expressão:** `(a|b)*abb`

**Teste as cadeias:**
- `abb` → ACEITA
- `aabb` → ACEITA
- `babb` → ACEITA
- `ababb` → ACEITA
- `abc` → REJEITA

**Autômato gerado (exemplo):**
```
--- Autômato Finito Não Determinístico com ε-transições ---

Estados: {q0, q1, q2, ..., q15}
Alfabeto: {a, b}
Estado Inicial: q0
Estados Finais: {q15}

Transições:
  δ(q0, ε) = {q1, q7}
  δ(q1, ε) = {q2, q4}
  δ(q2, a) = {q3}
  δ(q3, ε) = {q6}
  δ(q4, b) = {q5}
  δ(q5, ε) = {q6}
  δ(q6, ε) = {q1, q7}
  δ(q7, a) = {q8}
  δ(q8, ε) = {q9}
  δ(q9, b) = {q10}
  δ(q10, ε) = {q11}
  δ(q11, b) = {q12}
  δ(q12, ε) = {q15}
```

---

### Exemplo 4: Números Binários Terminados em 0 `(0|1)*0`

**Expressão:** `(0|1)*0`

**Teste as cadeias:**
- `0` → ACEITA
- `10` → ACEITA
- `110` → ACEITA
- `1010` → ACEITA
- `111` → REJEITA

---

## Operadores Suportados

| Operador | Nome | Descrição | Exemplo | Aceita |
|----------|------|-----------|---------|--------|
| `\|` | União | Aceita uma das alternativas | `a\|b` | `a`, `b` |
| `*` | Fecho de Kleene | Zero ou mais repetições | `a*` | `ε`, `a`, `aa`, `aaa`... |
| Concatenação | Sequência | Símbolos em sequência | `ab` | `ab` |
| `()` | Agrupamento | Altera precedência | `(a\|b)*` | `ε`, `a`, `b`, `aa`, `ab`... |
| `ε` | Epsilon | Cadeia vazia | `ε` | cadeia vazia |

### Precedência dos Operadores

1. **Parênteses `()`** - Maior precedência
2. **Fecho de Kleene `*`**
3. **Concatenação**
4. **União `|`** - Menor precedência

---

## Funcionamento

### Algoritmo de Construção de Thompson

O conversor implementa a Construção de Thompson recursivamente:

#### 1. Casos Base

**Símbolo único:**
```
   a
q0 → q1
```

**Epsilon:**
```
   ε
q0 → q1
```

#### 2. União (r|s)

```
      ε    [AFN r]    ε
  ┌────→ inicial_r ────┐
  │                    ↓
q0                    qf
  │                    ↑
  └────→ inicial_s ────┘
      ε    [AFN s]    ε
```

#### 3. Concatenação (rs)

```
[AFN r]    ε    [AFN s]
inicial_r → final_r = inicial_s → final_s
```

#### 4. Fecho de Kleene (r*)

```
        ε
    ┌───────────────┐
    ↓               │
    ε    [AFN r]    ε
q0 → inicial_r → final_r → qf
 └──────────────────────────┘
              ε
```

### Reconhecimento de Cadeias

**Algoritmo:**
```python
estados_atuais = fecho_epsilon({estado_inicial})

para cada simbolo em cadeia:
    estados_atuais = fecho_epsilon(mover(estados_atuais, simbolo))

retorna: estados_atuais ∩ estados_finais ≠ ∅
```

---

## Guia Rápido de Comandos

### Primeira vez (Setup completo)

**Windows:**
```bash
cd trabalho-final-larissa-brasil
python -m venv venv
venv\Scripts\activate
cd backend
pip install -r requirements.txt
python server.py
```

**macOS/Linux:**
```bash
cd ~trabalho-final-larissa-brasil
python3 -m venv venv
source venv/bin/activate
cd backend
pip install -r requirements.txt
python server.py
```

---

### Uso diário (após setup)

**Windows:**
```bash
cd trabalho-final-larissa-brasil
venv\Scripts\activate
cd backend
python server.py
```

**macOS/Linux:**
```bash
cd ~/trabalho-final
source venv/bin/activate
cd backend
python server.py
```

---

## Sugestões de Teste

### Teste 1: Validação Básica
```
ER: a
Aceita: a
Rejeita: b, aa, ε
```

### Teste 2: União
```
ER: a|b|c
Aceita: a, b, c
Rejeita: ab, aa, d
```

### Teste 3: Concatenação
```
ER: abc
Aceita: abc
Rejeita: ab, bc, a, abcc
```

### Teste 4: Fecho
```
ER: (ab)*
Aceita: ε, ab, abab, ababab
Rejeita: a, b, aba, ababa
```

### Teste 5: Complexo
```
ER: (a|b)*a(a|b)(a|b)
Aceita: aaa, baa, abaa, aaab, baab
Rejeita: a, aa, ab, ba
```

---

## Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'flask'"

**Solução:**
```bash
# Ative o venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Instale
cd backend
pip install -r requirements.txt
```

---

### Erro: "Address already in use"

**Solução - Mude a porta:**
```python
# Em backend/server.py, última linha
app.run(debug=True, port=5001)
```

**Solução - Mate o processo:**
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID [número] /F

# macOS/Linux
lsof -ti:5000 | xargs kill -9
```

---

### Interface não carrega

1. Verifique se o servidor está rodando
2. Limpe cache do navegador (Ctrl+Shift+Del)
3. Tente modo anônimo
4. Verifique firewall

---

### AFN não aparece após converter

1. Abra Console do navegador (F12)
2. Verifique erros JavaScript
3. Confirme que servidor Flask responde

---

## Autora

Larissa Brasil

Ciência da Computação - Teoria da Computação  
UFPI - 2025

*Desenvolvido para a disciplina de Teoria da Computação.*
