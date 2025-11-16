// Configuração da API
const API_URL = 'http://localhost:5000/api';

class AFNSimulador {
    constructor() {
        this.afnAtual = null;
    }

    async converter(expressao) {
        const response = await fetch(`${API_URL}/converter`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ expressao })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.erro || 'Erro ao converter');
        }

        return await response.json();
    }

    async reconhecer(cadeia) {
        const response = await fetch(`${API_URL}/reconhecer`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ cadeia })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.erro || 'Erro ao reconhecer');
        }

        const result = await response.json();
        return result.aceita;
    }

    formatarAFN(afn) {
        let resultado = '<b>Autômato Finito Não Determinístico com ε-transições </b>\n\n';
        resultado += `Estados: {${afn.estados.join(', ')}}\n`;
        resultado += `Alfabeto: {${afn.alfabeto.join(', ')}}\n`;
        resultado += `Estado Inicial: ${afn.estadoInicial}\n`;
        resultado += `Estados Finais: {${afn.estadosFinais.join(', ')}}\n\n`;
        resultado += 'Transições:\n';
        
        afn.transicoes.forEach(t => {
            resultado += `  δ(${t.origem}, ${t.simbolo}) = {${t.destino}}\n`;
        });
        
        return resultado;
    }
}

// Inicialização
const simulador = new AFNSimulador();
let afnAtual = null;

const operadores = [
    { operador: '|', nome :'União (OU)', exemplo: 'Exemplo: a|b aceita "a" ou "b"'}, 
    { operador:'.', nome: 'Concatenação', exemplo: 'Exemplo: ab aceita "ab"'}, 
    { operador:'ε', nome: 'Epsilon', exemplo: 'Transição sem consumir símbolo'}, 
    { operador:'*', nome: 'Fecho de Kleene', exemplo: 'Exemplo: a* aceita "", "a", "aa", "aaa"...'},
    { operador:'()', nome: 'Agrupamento', exemplo: 'Exemplo: (a|b)* aceita qualquer combinação'}
];

const exemplos = [
    '(a|b)*',
    '(a|b)*abb',
    'a*b*c*',
    '(0|1)*0'
];

// Renderizar operadores dinamicamente
function renderizarOperadores() {
    const container = document.getElementById('operadores-container');
    if (!container) return;
    
    container.innerHTML = operadores.map(op => `
        <div class="flex items-center">
            <span class="inline-block w-8 h-8 bg-blue-50 rounded text-center leading-8 font-mono font-bold text-gray-700 mr-3">
                ${op.operador}
            </span>
            <div>
                <p class="font-semibold text-gray-700">${op.nome}</p>
                <p class="text-sm text-gray-600">${op.exemplo}</p>
            </div>
        </div>
    `).join('');
}

// Renderizar exemplos dinamicamente
function renderizarExemplos() {
    const container = document.getElementById('exemplos-container');
    if (!container) return;
    
    container.innerHTML = exemplos.map(exemplo => `
        <button class="example-btn w-full text-center px-4 py-2 bg-indigo-50 hover:bg-indigo-100 rounded-lg transition duration-200 font-mono text-sm">
            ${exemplo}
        </button>
    `).join('');
    
    // Adicionar event listeners aos novos botões
    document.querySelectorAll('.example-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.getElementById('regex-input').value = btn.textContent.trim();
        });
    });
}

// Inicialização quando a página carregar
document.addEventListener('DOMContentLoaded', () => {
    renderizarOperadores();
    renderizarExemplos();
});

// Event Listeners
document.getElementById('convert-btn').addEventListener('click', async () => {
    const expressao = document.getElementById('regex-input').value.trim();
    
    if (!expressao) {
        mostrarErro('Por favor, digite uma expressão regular.');
        return;
    }
    
    const btn = document.getElementById('convert-btn');
    btn.disabled = true;
    
    try {
        afnAtual = await simulador.converter(expressao);
        exibirAFN(afnAtual);
        limparResultados();
    } catch (error) {
        mostrarErro('Erro ao converter expressão: ' + error.message);
    } finally {
        btn.disabled = false;
        btn.textContent = 'Converter';
    }
});

document.getElementById('test-btn').addEventListener('click', async () => {
    if (!afnAtual) {
        mostrarErro('Primeiro converta uma expressão regular.');
        return;
    }
    
    let cadeia = document.getElementById('string-input').value.trim();
    if (cadeia === 'ε') cadeia = '';
    
    const btn = document.getElementById('test-btn');
    btn.disabled = true;
    
    try {
        const aceita = await simulador.reconhecer(cadeia);
        adicionarResultadoTeste(cadeia, aceita);
        document.getElementById('string-input').value = '';
    } catch (error) {
        mostrarErro('Erro ao testar cadeia: ' + error.message);
    } finally {
        btn.disabled = false;
    }
});

// Enter para testar
document.getElementById('string-input').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        document.getElementById('test-btn').click();
    }
});

// Enter para converter
document.getElementById('regex-input').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        document.getElementById('convert-btn').click();
    }
});

// Exemplos
document.querySelectorAll('.example-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.getElementById('regex-input').value = btn.textContent.trim();
    });
});

// Limpar
document.getElementById('clear-btn').addEventListener('click', () => {
    document.getElementById('regex-input').value = '';
    document.getElementById('string-input').value = '';
    document.getElementById('afn-output').innerHTML = `
        <p class="text-gray-400 text-center py-8">
            Digite uma expressão regular e clique em "Converter"
        </p>
    `;
    limparResultados();
    afnAtual = null;
});

// Exportar
document.getElementById('export-btn').addEventListener('click', () => {
    if (!afnAtual) {
        mostrarErro('Não há AFN para exportar.');
        return;
    }
    
    const texto = simulador.formatarAFN(afnAtual);
    const blob = new Blob([texto], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'afn-e.txt';
    a.click();
});

// Funções auxiliares
function exibirAFN(afn) {
    const output = document.getElementById('afn-output');
    output.innerHTML = `<pre class="text-gray-800">${simulador.formatarAFN(afn)}</pre>`;
}

function adicionarResultadoTeste(cadeia, aceita) {
    const results = document.getElementById('test-results');
    const cadeiaDisplay = cadeia === '' ? 'ε (vazio)' : cadeia;
    
    const div = document.createElement('div');
    div.className = `p-3 rounded-lg border-l-4 ${aceita ? 'bg-green-50 border-green-500' : 'bg-red-50 border-red-500'}`;
    div.innerHTML = `
        <div class="flex items-center justify-between">
            <span class="font-mono font-semibold">"${cadeiaDisplay}"</span>
            <span class="px-3 py-1 rounded-full text-sm font-bold ${aceita ? 'bg-green-500 text-white' : 'bg-red-500 text-white'}">
                ${aceita ? 'ACEITA' : 'REJEITA'}
            </span>
        </div>
    `;
    
    results.insertBefore(div, results.firstChild);
}

function limparResultados() {
    document.getElementById('test-results').innerHTML = '';
}

function mostrarErro(mensagem) {
    const output = document.getElementById('afn-output');
    output.innerHTML = `
        <div class="bg-red-50 border-l-4 border-red-500 p-4 rounded">
            <div class="flex items-center">
                <p class="text-red-700">${mensagem}</p>
            </div>
        </div>
    `;
}