// Funções da calculadora - Conjunto de funções para manipular a calculadora interativa
//
// EXPLICAÇÃO DO PROBLEMA E DA SOLUÇÃO MELHORADA:
//
// Problema identificado:
// Quando um resultado é apresentado e o utilizador utiliza o teclado para introduzir um novo valor,
// o cursor não é posicionado corretamente. Especificamente, quando se digita um número após
// um resultado, o cursor fica posicionado antes do número introduzido, em vez de após o número.
//
// A solução anterior não funcionou completamente porque o navegador estava a posicionar o cursor
// incorretamente antes que pudéssemos intervir com o evento 'input'.
//
// Solução melhorada implementada:
// 1. Tornamos o cursor visível removendo o atributo readonly e utilizando CSS específico
// 2. Prevenimos a entrada direta utilizando o evento beforeinput
// 3. Adicionamos estilos visuais para tornar o cursor mais visível
// 4. Garantimos que o cursor é corretamente posicionado em todas as operações

// Variável global para controlar (indicador) se o ecrã está a mostrar um resultado dos cálculos
// Permite comportamentos diferentes dependendo se o que está no ecrã é um resultado ou uma entrada do utilizador
let resultDisplayed = false;

// appendToDisplay : Adiciona um número ou operador ao campo de introdução (ecrã)
function appendToDisplay(value) { 
    // Esta função recebe um parâmetro 'value' que representa o carácter a ser adicionado ao ecrã
    const display = document.getElementById('display');
    // Obtém o elemento HTML com id="display" (o campo de texto da calculadora) e guarda-o na constante 'display'
    
    // Verificar se o valor é um operador matemático ou uma função matemática
    const isOperator = ['+', '-', '*', '/', '×', '÷'].includes(value);
    // Verifica se o valor é uma função matemática (termina com parêntese aberto)
    const isMathFunction = value.endsWith('(');
    // Verifica se é operação de potência
    const isPowerOperation = value === '**' || value === '**2';
    
    // Se um resultado estiver a ser apresentado no ecrã...
    if (resultDisplayed) {
        // Se for um operador, uma função matemática ou potência, adiciona-o após o resultado
        if (isOperator || isMathFunction || isPowerOperation) {
            if (isMathFunction) {
                // Para funções matemáticas, coloca a função antes do resultado e adiciona o parêntese de fechamento
                display.value = value + display.value + ')';
                // Como neste caso estamos trabalhando com um resultado, posicionamos o cursor no final
                // Pois queremos manter o resultado inteiro dentro dos parênteses
                display.setSelectionRange(display.value.length, display.value.length);
            } else {
                // Para operadores ou potência, adiciona após o resultado
                display.value = display.value + value;
                // Posiciona o cursor no final da expressão
                display.setSelectionRange(display.value.length, display.value.length);
            }
        } else {
            // Se não for um operador nem uma função, substitui completamente o resultado atual pelo novo valor
            display.value = value;
            // Posiciona o cursor após o novo valor introduzido
            display.setSelectionRange(value.length, value.length);
        }
        
        // Repõe o estado para não ser mais considerado como resultado
        resultDisplayed = false;
        
        // Remove qualquer valor original armazenado quando o utilizador começa uma nova expressão
        // ADICIONADO - Para lidar com valores originais
        const form = document.querySelector('form');
        let hiddenInput = document.getElementById('originalValueInput');
        if (hiddenInput) {
            hiddenInput.parentNode.removeChild(hiddenInput);
        }
        
        // Mantém o foco no campo de introdução para permitir operações adicionais de teclado
        display.focus();
        
        // Armazena a posição atual do cursor num atributo de dados para recuperação posterior
        // NOVO - Para garantir que o cursor permaneça visível e corretamente posicionado
        display.setAttribute('data-cursor-pos', display.selectionStart);
        
        return; // Termina a execução da função aqui se estivermos a lidar com um resultado
    }
    
    // Comportamento normal quando não estamos a lidar com um resultado anterior
    const cursorPos = display.selectionStart;
    // Obtém a posição atual do cursor no campo de texto
    
    const textBefore = display.value.substring(0, cursorPos); 
    // Extrai o texto desde o início até à posição atual do cursor
    // O método substring(inicio, fim) retorna uma parte da string entre os índices especificados
    
    const textAfter = display.value.substring(cursorPos);
    // Extrai o texto desde a posição do cursor até ao final do campo
    
    // Verifica se o valor é uma função matemática (termina com parêntese aberto)
    if (value.endsWith('(')) {
        // Para funções matemáticas, adiciona o parêntese de fechamento automaticamente
        display.value = textBefore + value + ')' + textAfter;
        
        // Posiciona o cursor logo após o parêntese de abertura
        const newCursorPos = cursorPos + value.length;
        display.setSelectionRange(newCursorPos, newCursorPos);
    } else {
        // Para outros valores, comportamento normal
        display.value = textBefore + value + textAfter;
        
        // Posiciona o cursor logo após o valor inserido
        const newCursorPos = cursorPos + value.length;
        display.setSelectionRange(newCursorPos, newCursorPos);
    }
    
    // Mantém o foco no campo de introdução
    display.focus();
    // Garante que o utilizador pode continuar a digitar sem precisar de clicar novamente no campo
    
    // Armazena a posição atual do cursor num atributo de dados para recuperação posterior
    // NOVO - Para manter registo da posição do cursor entre operações
    display.setAttribute('data-cursor-pos', display.selectionStart);
}

// clearDisplay : Apaga todo o conteúdo do campo de introdução (ecrã)
function clearDisplay() {
    const display = document.getElementById('display');
    display.value = '';
    // Define o valor do campo de introdução como uma string vazia, apagando todo o conteúdo
    
    display.focus();
    // Mantém o foco no campo de introdução após limpá-lo
    
    resultDisplayed = false; // Repõe o estado do indicador de resultado
    // Como o ecrã foi limpo, já não está a mostrar um resultado
    
    // Remove qualquer valor original armazenado quando o utilizador limpa a tela
    // ADICIONADO - Para lidar com valores originais
    const form = document.querySelector('form');
    let hiddenInput = document.getElementById('originalValueInput');
    if (hiddenInput) {
        hiddenInput.parentNode.removeChild(hiddenInput);
    }
    
    // Redefine a posição do cursor para o início (0)
    // NOVO - Para garantir o correto posicionamento do cursor após limpar o ecrã
    display.setAttribute('data-cursor-pos', 0);
}

// backspaceDisplay : Remove o carácter à esquerda do cursor
function backspaceDisplay() {
    const display = document.getElementById('display');
    // Obtém o elemento do campo de introdução
    
    const cursorPos = display.selectionStart;
    // A propriedade selectionStart é nativa dos elementos de formulário HTML
    // que aceitam texto, como <input> e <textarea>
    // Guarda a posição atual do cursor numa variável
    
    // Não faz nada se o cursor estiver no início do campo
    if (cursorPos === 0) return;
    // Se o cursor estiver no início (posição 0), sai da função sem fazer alterações
    
    const textBefore = display.value.substring(0, cursorPos - 1);
    // Obtém todo o texto antes do carácter a ser apagado (até posição cursor-1)
    
    const textAfter = display.value.substring(cursorPos);
    // Obtém todo o texto após o cursor
    
    display.value = textBefore + textAfter;
    // Recombina o texto sem o carácter que estava imediatamente à esquerda do cursor
    
    // Posiciona o cursor no lugar correto após a eliminação
    const newCursorPos = cursorPos - 1;
    // A nova posição é um carácter antes da posição original
    
    display.setSelectionRange(newCursorPos, newCursorPos);
    // Define o cursor na nova posição
    
    // Mantém o foco no campo de introdução
    display.focus();
    
    // Atualiza a posição do cursor no atributo de dados
    // NOVO - Para manter registo da posição do cursor entre operações
    display.setAttribute('data-cursor-pos', newCursorPos);
}

// moveCursorLeft : Move o cursor uma posição para a esquerda
function moveCursorLeft() {
    const display = document.getElementById('display');
    // Obtém o elemento do campo de introdução
    
    const cursorPos = display.selectionStart;
    // Obtém a posição atual do cursor
    
    // Não faz nada se o cursor já estiver no início
    if (cursorPos > 0) {
        // Verifica se a posição é maior que zero (não está no início)
        const newPos = cursorPos - 1;
        display.setSelectionRange(newPos, newPos);
        // Move o cursor uma posição para a esquerda
        
        // Atualiza a posição do cursor no atributo de dados
        // NOVO - Para manter registo da posição do cursor
        display.setAttribute('data-cursor-pos', newPos);
    }
    
    display.focus();
    // Mantém o foco no campo de introdução
}

// moveCursorRight : Move o cursor uma posição para a direita
function moveCursorRight() {
    const display = document.getElementById('display');
    // Obtém o elemento do campo de introdução
    
    const cursorPos = display.selectionStart;
    // Obtém a posição atual do cursor
    
    const maxPos = display.value.length;
    // Calcula a posição máxima possível (comprimento do texto)
    
    // Não faz nada se o cursor já estiver no fim
    if (cursorPos < maxPos) {
        // Verifica se a posição é menor que a posição máxima (não está no fim)
        const newPos = cursorPos + 1;
        display.setSelectionRange(newPos, newPos);
        // Move o cursor uma posição para a direita
        
        // Atualiza a posição do cursor no atributo de dados
        // NOVO - Para manter registo da posição do cursor
        display.setAttribute('data-cursor-pos', newPos);
    }
    
    display.focus();
    // Mantém o foco no campo de introdução
}

// Função para submeter o formulário (calcular o resultado)
function submitForm() {
    const form = document.querySelector('form');
    if (form) {
        // Indica que após a submissão, o valor apresentado será um resultado
        setTimeout(function() {
            resultDisplayed = true;
            
            // NOVO - Coloca o cursor no final do resultado após a submissão
            const display = document.getElementById('display');
            if (display) {
                // Utiliza um pequeno atraso para garantir que o resultado já está no display
                setTimeout(function() {
                    // Posiciona o cursor no final do texto
                    const finalPos = display.value.length;
                    display.focus();
                    display.setSelectionRange(finalPos, finalPos);
                    
                    // Armazena a posição final no atributo data
                    display.setAttribute('data-cursor-pos', finalPos);
                }, 100); // Ajustar este delay se necessário
            }
        }, 10);
        
        form.submit();
    }
}

// Adicionar controlo do menu suspenso utilizando JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // 'document' é o objeto que representa toda a página HTML
    // addEventListener é um método que "escuta" por um evento específico
    // 'DOMContentLoaded' é o evento que ocorre quando o HTML termina de carregar
    // A função anónima function() { ... } contém o código a executar quando o evento ocorre
    // Garante que o script só é executado após o documento HTML estar completamente carregado

    // Controlo do menu suspenso
    const dropdownButton = document.getElementById('dropdownButton');
    // Obtém o botão que ativa o menu suspenso
    
    const dropdownContent = document.getElementById('dropdownContent');
    // Obtém o conteúdo do menu suspenso (opções)
    
    const dropdown = document.getElementById('mainDropdown');
    // Obtém o contentor principal do menu suspenso
    
    // Alterna o menu suspenso ao clicar no botão
    if (dropdownButton) {
        // Verifica se o botão existe antes de adicionar um detetor de eventos
        dropdownButton.addEventListener('click', function(e) {
            e.preventDefault(); // Impede o comportamento predefinido do botão (importante para botões em formulários)
            e.stopPropagation(); // Impede que o clique se propague para os elementos superiores
            dropdownContent.classList.toggle('show'); // Alterna a classe 'show' no elemento do menu
            // Se a classe 'show' não existir, é adicionada (menu aparece)
            // Se a classe 'show' já existir, é removida (menu desaparece)
        });
    }
    
    // Fechar menu suspenso quando se clica fora dele
    document.addEventListener('click', function(e) {
        // Adiciona um detetor de eventos de clique a toda a página
        if (dropdown && !dropdown.contains(e.target)) {
            // Verifica se o elemento clicado (e.target) NÃO está dentro do menu suspenso
            dropdownContent.classList.remove('show');
            // Remove a classe 'show', fazendo o menu desaparecer
        }
    });

    // Detetar quando um formulário é submetido (botão = pressionado)
    const form = document.querySelector('form');
    // Obtém o primeiro elemento 'form' na página
    
    if (form) {
        // Verifica se o formulário existe
        form.addEventListener('submit', function() {
            // Adiciona um detetor de eventos para submissão do formulário
            
            // Indica que após a submissão, o valor apresentado será um resultado
            setTimeout(function() {
                // Usa setTimeout para garantir que esta ação ocorre após o processamento do formulário
                resultDisplayed = true;
                // Define a variável global como verdadeira, indicando que o ecrã mostra um resultado
            // NOVO - Posiciona o cursor no final do resultado após receber resposta
                const display = document.getElementById('display');
                if (display) {
                    // Utiliza um delay maior para garantir que o resultado já foi processado
                    setTimeout(function() {
                        const finalPos = display.value.length;
                        display.focus();
                        display.setSelectionRange(finalPos, finalPos);
                        display.setAttribute('data-cursor-pos', finalPos);
                    }, 300); // Delay maior para lidar com o tempo de resposta do servidor
                }
            }, 10);
        });
    }

    // Painel de histórico
    const historyButton = document.getElementById('historyButton');
    // Obtém o botão que ativa o painel de histórico
    
    const historyPanel = document.getElementById('historyPanel');
    // Obtém o painel de histórico
    
    const closeHistoryBtn = document.getElementById('closeHistoryBtn');
    // Obtém o botão para fechar o painel de histórico
    
    // Mostrar/esconder o painel de histórico
    if (historyButton && historyPanel) {
        // Verifica se tanto o botão como o painel existem
        historyButton.addEventListener('click', function(e) {
            // Adiciona detetor de eventos de clique ao botão de histórico
            e.preventDefault(); // Impede o comportamento predefinido do botão
            e.stopPropagation(); // Impede que o evento se propague para elementos superiores
            historyPanel.classList.toggle('show'); // Alterna a visibilidade do painel
        });
    }
    
    // Fechar o painel de histórico ao clicar no botão fechar
    if (closeHistoryBtn && historyPanel) {
        // Verifica se tanto o botão fechar como o painel existem
        closeHistoryBtn.addEventListener('click', function() {
            // Adiciona detetor de eventos de clique ao botão fechar
            historyPanel.classList.remove('show');
            // Remove a classe 'show' para esconder o painel
        });
    }
    
    // Fechar o painel de histórico ao clicar fora dele
    document.addEventListener('click', function(e) {
        // Adiciona detetor de eventos de clique a todo o documento
        if (historyPanel && historyPanel.classList.contains('show')) {
            // Verifica se o painel de histórico existe e está visível
            
            // Verifica se o clique foi fora do painel e do botão de histórico
            if (!historyPanel.contains(e.target) && !historyButton.contains(e.target)) {
                // Se o clique não foi nem no painel nem no botão
                historyPanel.classList.remove('show');
                // Esconde o painel removendo a classe 'show'
            }
        }
    });
    
    // Configurar o toggle de modo angular
    const angleToggle = document.getElementById('angleModeToggle');
    const radText = document.querySelector('.angle-mode-toggle span:first-child');
    const degText = document.querySelector('.angle-mode-toggle span:last-child');
    
    // Função para atualizar visualmente o modo ativo
    function updateAngleModeDisplay() {
        if (angleToggle && angleToggle.checked) {
            // Modo graus
            radText.classList.remove('active');
            degText.classList.add('active');
        } else {
            // Modo radianos
            radText.classList.add('active');
            degText.classList.remove('active');
        }
    }
    
    if (angleToggle) {
        // Atualizar classes visuais baseado no estado inicial
        updateAngleModeDisplay();
        
        // Adicionar evento de alteração
        angleToggle.addEventListener('change', function() {
            // Atualizar visuais imediatamente
            updateAngleModeDisplay();
            // Enviar para o servidor para alternar o modo
            window.location.href = '/toggle_angle_mode';
        });
    }

    // SOLUÇÃO MELHORADA: Configuração do campo de visualização para cursor visível
    const display = document.getElementById('display');
    
    if (display && display.value && !display.value.includes('Erro')) {
        // Se o campo já tiver um valor que não é uma mensagem de erro,
        // considera esse valor como um resultado
        resultDisplayed = true;
    }
    
    if (display) {
        // NOVA IMPLEMENTAÇÃO: Tornando o cursor visível
        
        // 1. Removemos o atributo readonly para permitir que o cursor seja visível
        display.removeAttribute('readonly');
        
        // 2. Adicionamos uma classe CSS específica para garantir visibilidade do cursor
        display.classList.add('cursor-visible');
        
        // 3. Prevenimos entradas diretas de teclado através do evento beforeinput
        display.addEventListener('beforeinput', function(e) {
            e.preventDefault(); // Bloqueia a entrada direta mas permite visualização do cursor
        });
        
        // 4. Garantimos que o display mantém o foco e o cursor é posicionado corretamente
        display.addEventListener('blur', function() {
            // Pequeno atraso para evitar conflitos com outros cliques
            setTimeout(function() {
                // Retorna o foco se o utilizador não estiver interagindo com elementos de entrada
                if (document.activeElement === document.body || 
                    (document.activeElement && document.activeElement.tagName !== 'BUTTON' && 
                     document.activeElement.tagName !== 'INPUT' && 
                     document.activeElement.tagName !== 'SELECT')) {
                    
                    display.focus();
                    
                    // Restaurar a posição do cursor a partir do atributo data-cursor-pos
                    const savedPos = parseInt(display.getAttribute('data-cursor-pos') || '0');
                    const maxPos = display.value.length;
                    // Garantir que a posição está dentro dos limites
                    const validPos = Math.min(Math.max(0, savedPos), maxPos);
                    
                    display.setSelectionRange(validPos, validPos);
                }
            }, 10);
        });
        
        // 5. Armazenar a posição do cursor após cada clique ou movimento
        display.addEventListener('click', function() {
            display.setAttribute('data-cursor-pos', display.selectionStart);
        });
        
        // 6. Efeito de piscar para tornar o cursor mais visível
        let cursorBlinkInterval;
        
        display.addEventListener('focus', function() {
            // Cancelar qualquer intervalo existente
            if (cursorBlinkInterval) clearInterval(cursorBlinkInterval);
            
            // Adicionar classe que destaca o cursor quando ativo
            display.classList.add('cursor-active');
            
            // Criar efeito de piscar para o cursor
            cursorBlinkInterval = setInterval(function() {
                display.classList.toggle('cursor-blink');
            }, 500); // Alterna a cada 500ms (meio segundo)
        });
        
        display.addEventListener('blur', function() {
            // Limpar o intervalo quando o campo perde o foco
            if (cursorBlinkInterval) clearInterval(cursorBlinkInterval);
            display.classList.remove('cursor-active', 'cursor-blink');
        });
        
        // 7. Tratar eventos de teclado
        display.addEventListener('keydown', function(e) {
            // Prevenir o comportamento padrão para controlar manualmente
            e.preventDefault();
            
            // Tratamento para teclas de navegação
            if (e.key === 'ArrowLeft') {
                moveCursorLeft();
                return;
            }
            if (e.key === 'ArrowRight') {
                moveCursorRight();
                return;
            }
            if (e.key === 'Home') {
                display.setSelectionRange(0, 0);
                display.setAttribute('data-cursor-pos', 0);
                return;
            }
            if (e.key === 'End') {
                const endPos = display.value.length;
                display.setSelectionRange(endPos, endPos);
                display.setAttribute('data-cursor-pos', endPos);
                return;
            }
            
            // Tecla Backspace
            if (e.key === 'Backspace') {
                backspaceDisplay();
                return;
            }
            
            // Tecla Delete
            if (e.key === 'Delete') {
                // Simula uma função de delete (removendo o caractere à direita do cursor)
                const cursorPos = display.selectionStart;
                if (cursorPos < display.value.length) {
                    display.value = display.value.substring(0, cursorPos) + 
                                   display.value.substring(cursorPos + 1);
                    display.setSelectionRange(cursorPos, cursorPos);
                    display.setAttribute('data-cursor-pos', cursorPos);
                }
                return;
            }
            
            // Tecla Escape limpa o display
            if (e.key === 'Escape') {
                clearDisplay();
                return;
            }
            
            // Tecla Enter submete o formulário
            if (e.key === 'Enter') {
                submitForm();
                return;
            }
            
            // Para todas as outras teclas, usa a nossa função processadora
            handleKeyboardInput(e.key);
        });
        
        // Inicializar com foco para facilitar a utilização imediata
        display.focus();
    }
    
    // Adiciona evento de teclado global para capturar teclas mesmo quando o display não tem foco
    document.addEventListener('keydown', function(e) {
        // Se o display não tiver foco mas estivermos na página da calculadora
        if (display && document.activeElement !== display && 
            !e.ctrlKey && !e.altKey && !e.metaKey) {
            
            // Verifica se a tecla é relevante para a calculadora
            if (isCalculatorKey(e.key)) {
                e.preventDefault(); // Previne a ação padrão 
                
                // Dá foco ao display primeiro
                display.focus();
                
                // Processa a tecla conforme sua função
                if (e.key === 'Escape') {
                    clearDisplay();
                    return;
                }
                
                if (e.key === 'Backspace') {
                    backspaceDisplay();
                    return;
                }
                
                if (e.key === 'Enter' || e.key === '=') {
                    submitForm();
                    return;
                }
                
                // Usa o processador normal para outras teclas
                handleKeyboardInput(e.key);
            }
        }
    });
});

// Função para adicionar estilos CSS necessários para o cursor visível
function addCursorStyles() {
    // Verifica se os estilos já foram adicionados
    if (document.getElementById('cursor-styles')) return;
    
    // Cria um elemento de estilo
    const style = document.createElement('style');
    style.id = 'cursor-styles';
    style.textContent = `
        /* Estilos para garantir cursor visível */
        .cursor-visible {
            caret-color: #ff9500 !important; /* Cor laranja para o cursor */
            cursor: text !important;
            user-select: text !important;
            -webkit-user-select: text !important;
            -moz-user-select: text !important;
            -ms-user-select: text !important;
        }
        
        /* Destacar o cursor quando ativo */
        .cursor-active {
            outline: 2px solid #ff9500 !important; /* Contorno para indicar foco */
        }
        
        /* Efeito de piscar cursor */
        .cursor-blink {
            caret-color: transparent !important;
        }
        
        /* Sobrescrever qualquer estilo que possa ocultar o cursor */
        input[type="text"]:focus {
            caret-color: #ff9500 !important;
        }
    `;
    
    // Adiciona os estilos ao cabeçalho do documento
    document.head.appendChild(style);
}

// Executar a função para adicionar estilos assim que o DOM estiver pronto
document.addEventListener('DOMContentLoaded', addCursorStyles);

// SOLUÇÃO MELHORADA: Função de verificação mais abrangente
function isCalculatorKey(key) {
    // Lista completa de teclas que a calculadora deve processar
    const validKeys = [
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 
        '+', '-', '*', '/', '.',
        '(', ')', 
        'e', 'i', 'j', 'k', 'p',
        'Enter', 'Backspace', 'Escape', 'Delete',
        'ArrowLeft', 'ArrowRight', 'Home', 'End',
        'π', '×', '÷', ',', '=',
        's', 'c', 't', 'l'
    ];
    
    return validKeys.includes(key);
}

// Função para lidar com entrada de teclado
function handleKeyboardInput(key) {
    // SOLUÇÃO MELHORADA: Implementação mais robusta para teclas numéricas
    // Obtém o elemento de display uma única vez para eficiência
    const display = document.getElementById('display');
    
    // Verifica se a tecla é um dígito
    const isDigit = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'].includes(key);
    
    // Trata especificamente o caso de um dígito após um resultado
    if (isDigit && resultDisplayed) {
        // Substitui o resultado por este dígito
        display.value = key;
        // Posiciona o cursor após o dígito (posição 1)
        display.setSelectionRange(1, 1);
        // Marca como não mais exibindo um resultado
        resultDisplayed = false;
        // Armazena a nova posição do cursor
        display.setAttribute('data-cursor-pos', 1);
        return;
    }
    
    // Mapeamento de teclas para funções da calculadora
    switch(key) {
        // Números e operadores básicos
        case '0': case '1': case '2': case '3': case '4':
        case '5': case '6': case '7': case '8': case '9':
        case '+': case '-':
            appendToDisplay(key);
            break;
        
        // Operadores de multiplicação e divisão
        case '*': case '×':
            appendToDisplay('*');
            break;
        case '/': case '÷':
            appendToDisplay('/');
            break;
        
        // Ponto decimal (aceita tanto ponto quanto vírgula)
        case '.': case ',':
            appendToDisplay('.');
            break;
            
        // Parênteses
        case '(':
            appendToDisplay('(');
            break;
        case ')':
            appendToDisplay(')');
            break;
            
        // Valor Pi
        case 'p': case 'π':
            appendToDisplay('pi');
            break;
            
        // Unidades imaginárias
        case 'i':
            appendToDisplay('i');
            break;
        case 'j':
            appendToDisplay('j');
            break;
        case 'k':
            appendToDisplay('k');
            break;
            
        // Constante matemática e
        case 'e':
            appendToDisplay('exp(');
            break;
            
        // Igual
        case '=':
            // Quando pressiona igual, armazena explicitamente que queremos o cursor no final
            const display = document.getElementById('display');
            if (display) {
                display.setAttribute('data-cursor-end-after-submit', 'true');
            }
            submitForm();
            break;
            
        // Funções trigonométricas
        case 's':
            appendToDisplay('sin(');
            break;
        case 'c':
            appendToDisplay('cos(');
            break;
        case 't':
            appendToDisplay('tan(');
            break;
        
        // Logaritmo
        case 'l':
            appendToDisplay('log(');
            break;
    }
    
    // VERIFICAÇÃO ADICIONAL: garante que o cursor sempre será posicionado corretamente
    // Isso funciona como uma rede de segurança para qualquer cenário não previsto
    if (display && resultDisplayed === false) {
        // Se não estamos exibindo um resultado, o cursor deve estar numa posição válida
        const cursorPos = display.selectionStart;
        // Verifica se a posição está fora dos limites por algum motivo
        if (cursorPos === null || cursorPos === undefined || 
            cursorPos < 0 || cursorPos > display.value.length) {
            // Posiciona no final como forma de garantir uma posição válida
            const validPos = display.value.length;
            display.setSelectionRange(validPos, validPos);
            display.setAttribute('data-cursor-pos', validPos);
        } else {
            // Se a posição está válida, armazena-a
            display.setAttribute('data-cursor-pos', cursorPos);
        }
    }
}

// FUNÇÃO MODIFICADA: useHistoryItem com suporte para valores originais
// useHistoryItem : Utiliza um item do histórico na calculadora atual
function useHistoryItem(value, isExpression, originalData) {
    const display = document.getElementById('display');
    
    // Se há dados originais e estamos usando o resultado (não a expressão),
    // armazenamos também os dados originais como um atributo data no display
    if (originalData && !isExpression) {
        // Armazenar os dados originais como um atributo no elemento de display
        // Isso permite que o backend acesse esses dados quando o formulário for submetido
        display.setAttribute('data-original-value', originalData);
        
        // Podemos também adicionar um campo hidden ao formulário para transportar os dados originais
        const form = document.querySelector('form');
        let hiddenInput = document.getElementById('originalValueInput');
        
        // Se o campo hidden não existir, criá-lo
        if (!hiddenInput) {
            hiddenInput = document.createElement('input');
            hiddenInput.type = 'hidden';
            hiddenInput.id = 'originalValueInput';
            hiddenInput.name = 'original_value';
            form.appendChild(hiddenInput);
        }
        
        // Definir o valor do campo hidden como os dados originais
        hiddenInput.value = originalData;
    } else if (isExpression) {
        // Se estamos usando uma expressão, remover quaisquer dados originais armazenados
        display.removeAttribute('data-original-value');
        
        // Remover também o campo hidden se existir
        const hiddenInput = document.getElementById('originalValueInput');
        if (hiddenInput) {
            hiddenInput.parentNode.removeChild(hiddenInput);
        }
    }
    
    // Coloca o valor selecionado no campo de introdução
    display.value = value;
    
    // Define a posição do cursor no fim do valor
    display.focus(); // Dá foco ao campo primeiro
    display.setSelectionRange(value.length, value.length);
    // Posiciona o cursor após o último carácter do valor
    
    // Armazena a posição do cursor para recuperação posterior
    // NOVO - Para manter registo da posição do cursor
    display.setAttribute('data-cursor-pos', value.length);
    
    // Define se o display está mostrando um resultado ou uma expressão
    // Se for expressão, mantemos resultDisplayed como false para permitir continuar a edição
    // Se for resultado, definimos como true para que o próximo número substitua o resultado
    resultDisplayed = !isExpression;
    
    // Adiciona uma classe temporária para destacar o cursor após usar um item do histórico
    // NOVO - Para melhorar o feedback visual ao utilizador
    display.classList.add('cursor-highlight');
    setTimeout(function() {
        display.classList.remove('cursor-highlight');
    }, 1000); // Remove após 1 segundo
    
    // Fecha o painel de histórico
    const historyPanel = document.getElementById('historyPanel');
    // Obtém o elemento do painel de histórico
    
    if (historyPanel) {
        // Verifica se o painel existe
        historyPanel.classList.remove('show');
        // Esconde o painel removendo a classe 'show'
    }
}

// Evento para garantir que o cursor seja visível após a página ser carregada
window.addEventListener('load', function() {
    const display = document.getElementById('display');
    if (display && display.value) {
        // Se o campo já tiver um valor no carregamento da página (provavelmente um resultado)
        resultDisplayed = true;
        
        // Posiciona o cursor no final desse valor
        const finalPos = display.value.length;
        
        // Pequeno atraso para garantir que todos os outros manipuladores já foram executados
        setTimeout(function() {
            display.focus();
            display.setSelectionRange(finalPos, finalPos);
            display.setAttribute('data-cursor-pos', finalPos);
        }, 300);
    }
});

// Adiciona estilos específicos para o cursor destacado
document.addEventListener('DOMContentLoaded', function() {
    // SOLUÇÃO PARA O CURSOR VISÍVEL
    const display = document.getElementById('display');
    
    if (display) {
        // 1. Removemos o atributo readonly para permitir que o cursor seja visível
        display.removeAttribute('readonly');
        
        // 2. Adicionamos uma classe CSS específica para garantir visibilidade do cursor
        display.classList.add('cursor-visible');
        
        // 3. Prevenimos entradas diretas de teclado através do evento beforeinput
        display.addEventListener('beforeinput', function(e) {
            e.preventDefault(); // Bloqueia a entrada direta mas permite visualização do cursor
        });
        
        // 4. Garantimos que o display mantém o foco e o cursor é posicionado corretamente
        display.addEventListener('blur', function() {
            // Pequeno atraso para evitar conflitos com outros cliques
            setTimeout(function() {
                // Retorna o foco se o utilizador não estiver interagindo com outros elementos
                if (document.activeElement === document.body || 
                    (document.activeElement && document.activeElement.tagName !== 'BUTTON')) {
                    
                    display.focus();
                    
                    // Restaurar a posição do cursor a partir do atributo data-cursor-pos
                    const savedPos = parseInt(display.getAttribute('data-cursor-pos') || '0');
                    const maxPos = display.value.length;
                    // Garantir que a posição está dentro dos limites
                    const validPos = Math.min(Math.max(0, savedPos), maxPos);
                    
                    display.setSelectionRange(validPos, validPos);
                }
            }, 10);
        });
        
        // 5. Armazenar a posição do cursor após cada clique ou movimento
        display.addEventListener('click', function() {
            display.setAttribute('data-cursor-pos', display.selectionStart);
        });
        
        // 6. Assegurar que o cursor fique no final após submissão do formulário
        const form = document.querySelector('form');
        if (form) {
            form.addEventListener('submit', function() {
                // Marca que queremos o cursor no final após obter o resultado
                display.setAttribute('data-cursor-end-after-submit', 'true');
                
                // Depois de receber a resposta, posicionar o cursor no final
                setTimeout(function() {
                    const finalPos = display.value.length;
                    display.focus();
                    display.setSelectionRange(finalPos, finalPos);
                    display.setAttribute('data-cursor-pos', finalPos);
                }, 300);
            });
        }
        
        // 7. Garantir que eventos de teclado mantenham o cursor visível
        display.addEventListener('keydown', function(e) {
            const cursorPos = display.selectionStart;
            display.setAttribute('data-cursor-pos', cursorPos);
            
            // Para a tecla Enter, marcar que o cursor deve ficar no final
            if (e.key === 'Enter') {
                display.setAttribute('data-cursor-end-after-submit', 'true');
            }
        });
        
        // 8. Adicionar manipulador para o botão de submissão (=)
        const submitButtons = document.querySelectorAll('button[type="submit"], .submit');
        if (submitButtons.length > 0) {
            submitButtons.forEach(function(button) {
                button.addEventListener('click', function() {
                    // Marca que queremos o cursor no final após o resultado
                    display.setAttribute('data-cursor-end-after-submit', 'true');
                });
            });
        }
        
        // 9. Inicializar com cursor no final
        setTimeout(function() {
            const finalPos = display.value.length;
            display.focus();
            display.setSelectionRange(finalPos, finalPos);
            display.setAttribute('data-cursor-pos', finalPos);
        }, 100);
    }
    
    // Adicionar estilos CSS para o cursor
    const style = document.createElement('style');
    style.id = 'cursor-styles';
    style.textContent = `
        /* Estilos para garantir cursor visível */
        .cursor-visible {
            caret-color: #ff9500 !important; /* Cor laranja para o cursor */
            cursor: text !important;
            user-select: text !important;
            -webkit-user-select: text !important;
            -moz-user-select: text !important;
            -ms-user-select: text !important;
        }
        
        /* Sobrescrever qualquer estilo que possa ocultar o cursor */
        input[type="text"]:focus {
            caret-color: #ff9500 !important;
            outline: 2px solid #ff9500 !important;
        }
    `;
    document.head.appendChild(style);
});

// Função para detetar se o navegador está a esconder o cursor e aplicar correções específicas
function applyBrowserSpecificCursorFixes() {
    // NOVO - Para lidar com problemas específicos de navegadores
    const display = document.getElementById('display');
    if (!display) return;
    
    // Detetar o navegador
    const isFirefox = navigator.userAgent.indexOf('Firefox') !== -1;
    const isChrome = navigator.userAgent.indexOf('Chrome') !== -1;
    const isSafari = navigator.userAgent.indexOf('Safari') !== -1 && !isChrome;
    
    // Correções específicas para cada navegador
    if (isFirefox) {
        // Firefox às vezes tem problemas com o cursor em campos com eventos personalizados
        display.style.caretColor = '#ff9500';
        
        // Garantir que o evento 'input' não seja completamente bloqueado
        display.addEventListener('input', function(e) {
            // Ainda prevenimos a entrada direta, mas deixamos o cursor visível
            e.preventDefault();
            
            // Manter o cursor no local atual
            const cursorPos = display.selectionStart;
            setTimeout(function() {
                display.setSelectionRange(cursorPos, cursorPos);
            }, 0);
        });
    } 
    
    if (isSafari) {
        // Safari às vezes tem problemas com o cursor em campos com readonly
        // Garantir que o readonly seja removido mesmo que seja adicionado posteriormente
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.type === 'attributes' && mutation.attributeName === 'readonly') {
                    if (display.hasAttribute('readonly')) {
                        display.removeAttribute('readonly');
                    }
                }
            });
        });
        
        observer.observe(display, { attributes: true });
    }
}

// Executar correções específicas de navegador após o carregamento
window.addEventListener('load', applyBrowserSpecificCursorFixes);