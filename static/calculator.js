// Funções da calculadora

// Variável global para controlar (flag) se o display está a mostrar um resultado dos cálculos
let resultDisplayed = false;

// appendToDisplay : Adiciona um número ou operador ao campo de input (display)
function appendToDisplay(value) { 
    // Esta linha define a função appendToDisplay que aceita um parâmetro value (o valor a ser adicionado ao display).
    const display = document.getElementById('display');
    //Obtém o elemento HTML com id="display" (o campo de texto da calculadora) e armazena na constante display.
    
    // Verificar se é um operador
    const isOperator = ['+', '-', '*', '/', '×', '÷'].includes(value);
    // Cria uma constante isOperator que será true se o valor passado for um dos operadores na lista, e false caso contrário. 
    // Usa o método includes() para verificar.
    
    // Se um resultado está a aparecer no dislpay...
    if (resultDisplayed) {
        // Se for operador, adiciona após o resultado
        if (isOperator) {
            // Mantém o resultado e adiciona o operador no final
            display.value = display.value + value;
            // Posiciona o cursor no final
            display.setSelectionRange(display.value.length, display.value.length);
            // setSelectionRange(start, end)
            // start: O índice onde a seleção deve começar (índice baseado em zero)
            // end: O índice onde a seleção deve terminar
            // display.value.length representa o número total de caracteres no display
            // Por exemplo, se o display mostra "123+45", então display.value.length é 6
            // Ao definir ambos os parâmetros como 6, o cursor é posicionado após o último caractere "5"
        } else {
            // Se não for operador, substitui o resultado
            display.value = value;
            // Posiciona o cursor após o novo valor
            display.setSelectionRange(value.length, value.length);
        }
        
        // Resetar o estado para não ser mais considerado resultado
        resultDisplayed = false;
        
        // Mantém o foco no display
        display.focus();
        return;
    }
    
    // Código normal para quando não é resultado (comportamento atual)
    const cursorPos = display.selectionStart;
    const textBefore = display.value.substring(0, cursorPos); // .substring(startIndex, endIndex)
    const textAfter = display.value.substring(cursorPos);
    // Se não estiver a exibir um resultado, obtém a posição atual do cursor e 
    // divide o texto em duas partes: antes e depois do cursor.
    
    display.value = textBefore + value + textAfter;
    // Insere o novo valor na posição atual do cursor, entre as partes "antes" e "depois".
    
    // Posiciona o cursor após o caracter inserido
    const newCursorPos = cursorPos + value.length;
    display.setSelectionRange(newCursorPos, newCursorPos);
    // Calcula a nova posição do cursor após a inserção e move o cursor para lá.
    
    // Mantém o foco no display
    display.focus();
}

// clearDisplay : Apaga todo o conteúdo do campo de input (display)
function clearDisplay() {
    document.getElementById('display').value = '';
    document.getElementById('display').focus();
    resultDisplayed = false; // Resetar estado
}

function backspaceDisplay() {
    const display = document.getElementById('display');
    const cursorPos = display.selectionStart;
    // A propriedade selectionStart é uma propriedade nativa dos elementos de formulário HTML
    // que aceitam entrada de texto, como <input> e <textarea>.
    // Armazenando a posição atual do cursor em uma variável chamada cursorPos
    
    // Não fazer nada se o cursor estiver no início
    if (cursorPos === 0) return;
    
    const textBefore = display.value.substring(0, cursorPos - 1);
    const textAfter = display.value.substring(cursorPos);
    
    display.value = textBefore + textAfter;
    // Recombina o texto sem o caractere que estava imediatamente à esquerda do cursor.
    
    // Posiciona o cursor no lugar certo após a eliminação
    const newCursorPos = cursorPos - 1;
    display.setSelectionRange(newCursorPos, newCursorPos);
    
    // Mantém o foco no display
    display.focus();
}

function moveCursorLeft() {
    const display = document.getElementById('display');
    const cursorPos = display.selectionStart;
    
    // Não fazer nada se o cursor estiver no início
    if (cursorPos > 0) {
        display.setSelectionRange(cursorPos - 1, cursorPos - 1);
    }
    
    display.focus();
}

function moveCursorRight() {
    const display = document.getElementById('display');
    const cursorPos = display.selectionStart;
    const maxPos = display.value.length;
    
    // Não fazer nada se o cursor estiver no final
    if (cursorPos < maxPos) {
        display.setSelectionRange(cursorPos + 1, cursorPos + 1);
    }
    
    display.focus();
}

// Adicionar controlo do dropdown usando javascript
document.addEventListener('DOMContentLoaded', function() {
    // document é o objeto que representa toda a página HTML
    // addEventListener é um método que "escuta" por um evento específico
    // 'DOMContentLoaded' é o nome do evento que ocorre quando o HTML termina de carregar
    // A função anônima function() { ... } contém o código que será executado quando o evento ocorrer
    // Basicamente, esta função garante que o script só executa depois que o documento HTML está completamente carregado

    // Controle do dropdown menu
    const dropdownButton = document.getElementById('dropdownButton');
    const dropdownContent = document.getElementById('dropdownContent');
    const dropdown = document.getElementById('mainDropdown');
    
    // Toggle dropdown ao clicar no botão
    if (dropdownButton) {
        dropdownButton.addEventListener('click', function(e) {
            e.preventDefault(); // Impede o comportamento padrão do botão (importante para botões dentro de formulários)
            e.stopPropagation(); // Impede que o click se propague para os elementos pai
            dropdownContent.classList.toggle('show');// Alterna a classe 'show' no elemento do menu
            // Se a classe 'show' não existir, ela é adicionada (menu aparece)
            // Se a classe 'show' já existir, ela é removida (menu desaparece)
        });
    }
    
    // Fechar dropdown quando clicar fora dele
    document.addEventListener('click', function(e) { // Adiciona um detector de eventos de click a toda a página
        if (dropdown && !dropdown.contains(e.target)) { // Verifica se o elemento clicado (e.target) NÃO está dentro do dropdown
            dropdownContent.classList.remove('show'); // Remove a classe 'show', fazendo o menu desaparecer
        }
    });

     // Detectar quando um formulário é submetido (botão = pressionado)
    const form = document.querySelector('form');
        if (form) {
            form.addEventListener('submit', function() {
             // Marcar que após o submit, o valor exibido será um resultado
                setTimeout(function() {
                    resultDisplayed = true;
                }, 10);
            });
        }

    // Painel de histórico
    const historyButton = document.getElementById('historyButton');
    const historyPanel = document.getElementById('historyPanel');
    const closeHistoryBtn = document.getElementById('closeHistoryBtn');
    
    // Mostrar/esconder o painel de histórico
    if (historyButton && historyPanel) {
        historyButton.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            historyPanel.classList.toggle('show');
        });
    }
    
    // Fechar o painel de histórico ao clicar no botão fechar
    if (closeHistoryBtn && historyPanel) {
        closeHistoryBtn.addEventListener('click', function() {
            historyPanel.classList.remove('show');
        });
    }
    
    // Fechar o painel de histórico ao clicar fora dele
    document.addEventListener('click', function(e) {
        if (historyPanel && historyPanel.classList.contains('show')) {
            // Verifica se o click foi fora do painel e do botão de histórico
            if (!historyPanel.contains(e.target) && !historyButton.contains(e.target)) {
                historyPanel.classList.remove('show');
            }
        }
    });

    // Configurar o display para permitir posicionamento do cursor
    const display = document.getElementById('display');
    if (display && display.value && !display.value.includes('Erro')) {
        // Se tiver valor e não for erro, considerar como resultado
        resultDisplayed = true;
        // Se o display já contiver um valor ao carregar a página (e não for uma mensagem de erro), 
        // considera-o como um resultado.
    }
    if (display) {
        // Tornar o display manipulável mas bloquear entrada direta
        display.removeAttribute('readonly');
        // Remove o atributo "readonly" do display para permitir que o cursor seja posicionado.
        
        // Permitir apenas teclas de navegação e backspace
        display.addEventListener('keydown', function(e) {
            if (e.key === 'ArrowLeft' || e.key === 'ArrowRight' || e.key === 'Backspace' || 
                e.key === 'Home' || e.key === 'End' || e.key === 'Delete') {
                // Permitir estas teclas
                if (e.key === 'Backspace') {
                    e.preventDefault();
                    backspaceDisplay();
                }
            } else {
                // Bloquear outras teclas
                e.preventDefault();
            }
        });
        
        // Restaurar o cursor quando o input recebe foco
        display.addEventListener('focus', function() {
            // Manter a posição atual do cursor ou posicionar no fim se não houver posição
            if (this.selectionStart !== undefined) {
                const pos = this.selectionStart;
                setTimeout(() => {
                    this.setSelectionRange(pos, pos);
                }, 0);
                // Problema: Quando um campo recebe foco, alguns navegadores automaticamente
                // reposicionam o cursor (geralmente no final do texto) após executar o manipulador de evento focus
                // Solução: O setTimeout(0) coloca a nossa função na fila de tarefas do navegador para ser executada 
                // depois de qualquer manipulação padrão do cursor

                // Esta técnica garante que quando o utilizador clica no campo de exibição da calculadora, 
                // o cursor permanece exatamente onde o utilizador clicou, em vez de ser movido para o início ou fim por 
                // comportamentos padrão do navegador.
            }
        });
        
        // Permitir clique para posicionar o cursor
        display.addEventListener('mouseup', function() {
            // O navegador já posiciona o cursor automaticamente
        });
    }
});

// Função para usar um item do histórico
function useHistoryItem(expression, result) {
    const display = document.getElementById('display');
    // Colocar a expressão no display
    display.value = expression;
    
    // Setar posição do cursor no final
    display.focus();
    display.setSelectionRange(expression.length, expression.length);
    
    // Fechar o painel de histórico
    const historyPanel = document.getElementById('historyPanel');
    if (historyPanel) {
        historyPanel.classList.remove('show');
    }
}