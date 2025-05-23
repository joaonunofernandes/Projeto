// Funções da calculadora - Conjunto de funções para manipular a calculadora interativa

// Variável global para controlar (indicador) se o ecrã está a mostrar um resultado dos cálculos
// Permite comportamentos diferentes dependendo se o que está no ecrã é um resultado ou uma entrada do utilizador
let resultDisplayed = false;

// Variável global para armazenar a expressão original de um resultado reutilizado
let expressionFromHistoryForResult = null;

// appendToDisplay : Adiciona um número ou operador ao campo de introdução (ecrã)
function appendToDisplay(value) {
    // Esta função recebe um parâmetro 'value' que representa o carácter a ser adicionado ao ecrã
    const display = document.getElementById('display');
    // Obtém o elemento HTML com id="display" (o campo de texto da calculadora) e guarda-o na constante 'display'

    // Verificar se o valor é um operador matemático ou uma função matemática
    const isOperator = ['+', '-', '*', '/', '×', '÷', '**'].includes(value); // Adicionado '**' para potências
    // Verifica se o valor é uma função matemática (termina com parêntese aberto)
    const isMathFunction = value.endsWith('(');
    // Verifica se é operação de potência (para tratamento específico se necessário, embora '**' já esteja em isOperator)
    const isPowerOperation = value === '**' || value === '**2';

    // Se um resultado estiver a ser apresentado no ecrã...
    if (resultDisplayed) {
        // Se for um operador, uma função matemática ou potência, adiciona-o após o resultado
        if (isOperator || isMathFunction || isPowerOperation) {
            if (expressionFromHistoryForResult) {
                // Se temos uma expressão guardada de um "Usar Resultado", usamos essa expressão
                // envolvida em parêntesis para garantir a precedência correta.
                display.value = '(' + expressionFromHistoryForResult + ')' + value;
                expressionFromHistoryForResult = null; // Limpar após usar
            } else if (isMathFunction) {
                // Para funções matemáticas, coloca a função antes do resultado e adiciona o parêntese de fechamento
                // Se o resultado for numérico e a função for algo como 'sin(', queremos 'sin(resultado)'
                display.value = value.slice(0, -1) + display.value + ')';
            }
            else {
                // Para operadores ou potência, adiciona após o resultado numérico que está no display
                display.value = display.value + value;
            }
        } else {
            // Se não for um operador nem uma função (ou seja, é um número ou outro símbolo),
            // substitui completamente o resultado atual pelo novo valor
            display.value = value;
            expressionFromHistoryForResult = null; // Limpar, pois estamos a substituir o resultado
        }
        resultDisplayed = false; // Já não estamos a mostrar um resultado "puro" do cálculo anterior

        // Mantém o foco no campo de introdução para permitir operações adicionais de teclado
        display.focus();
        // Posiciona o cursor no final da expressão
        display.setSelectionRange(display.value.length, display.value.length);
        return; // Termina a execução da função aqui se estávamos a lidar com um resultado
    }

    // Comportamento normal quando não estamos a lidar com um resultado anterior no display
    const cursorPos = display.selectionStart;
    // Obtém a posição atual do cursor no campo de texto

    const textBefore = display.value.substring(0, cursorPos);
    // Extrai o texto desde o início até à posição atual do cursor

    const textAfter = display.value.substring(cursorPos);
    // Extrai o texto desde a posição do cursor até ao final do campo

    // Se o utilizador começar a digitar algo novo (que não seja um operador)
    // após ter clicado em "Usar Resultado" (resultDisplayed já terá sido definido como false acima,
    // mas expressionFromHistoryForResult ainda pode estar preenchida se não foi usada),
    // e o novo valor não é um operador, então a expressão guardada já não é relevante
    // para ser automaticamente concatenada com um operador.
    // Limpamos para evitar que seja usada indevidamente numa próxima operação.
    if (!isOperator && expressionFromHistoryForResult) {
        expressionFromHistoryForResult = null;
    }

    // Verifica se o valor é uma função matemática (termina com parêntese aberto)
    if (value.endsWith('(')) {
        // Para funções matemáticas, adiciona o parêntese de fechamento automaticamente
        display.value = textBefore + value + ')' + textAfter;

        // Posiciona o cursor logo após o parêntese de abertura
        const newCursorPos = cursorPos + value.length; // value já inclui '('
        display.setSelectionRange(newCursorPos, newCursorPos);
    } else {
        // Para outros valores (números, operadores que não foram tratados acima, etc.)
        display.value = textBefore + value + textAfter;

        // Posiciona o cursor logo após o valor inserido
        const newCursorPos = cursorPos + value.length;
        display.setSelectionRange(newCursorPos, newCursorPos);
    }

    // Mantém o foco no campo de introdução
    display.focus();
    // Garante que o utilizador pode continuar a digitar sem precisar de clicar novamente no campo
}

// clearDisplay : Apaga todo o conteúdo do campo de introdução (ecrã)
function clearDisplay() {
    document.getElementById('display').value = '';
    document.getElementById('display').focus();
    resultDisplayed = false;
    expressionFromHistoryForResult = null; // Limpar aqui também
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
        display.setSelectionRange(cursorPos - 1, cursorPos - 1);
        // Move o cursor uma posição para a esquerda
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
        display.setSelectionRange(cursorPos + 1, cursorPos + 1);
        // Move o cursor uma posição para a direita
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
            // Após a submissão de um novo cálculo, a expressão anterior do histórico
            // já não é relevante para o *próximo* input.
            expressionFromHistoryForResult = null;
        }, 10); // Pequeno atraso para garantir a execução após o processamento do formulário

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
            }, 10);
            // Pequeno atraso de 10ms para garantir a execução após o processamento do formulário
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

    //Configuração do campo de visualização
    const display = document.getElementById('display');
    
    if (display && display.value && !display.value.includes('Erro')) {
        // Se o campo já tiver um valor que não é uma mensagem de erro,
        // considera esse valor como um resultado
        resultDisplayed = true;
    }
    
    if (display) {        
        // Garante que o campo ainda pode receber foco
        display.tabIndex = 0;
        
        // Trata as teclas de navegação diretamente
        display.addEventListener('keydown', function(e) {
            // Sempre previne a ação padrão para garantir que temos controlo total
            e.preventDefault();
            
            // Navegação com teclas de seta
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
                return;
            }
            if (e.key === 'End') {
                display.setSelectionRange(display.value.length, display.value.length);
                return;
            }
            
            // Tecla backspace
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
        
        // Eventos de clique do rato para posicionar o cursor
        display.addEventListener('click', function() {
            // Não faz nada especial, permite o posicionamento normal do cursor
        });
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
            display.setSelectionRange(display.value.length, display.value.length);
        }
    }
}

// useHistoryItem : Utiliza um item do histórico na calculadora atual
function useHistoryItem(value, isExpression, originalExpression = null) {
    const display = document.getElementById('display');
    display.value = value; // Mostra o valor (seja expressão ou resultado string)

    display.focus();
    display.setSelectionRange(value.length, value.length);

    if (isExpression) {
        resultDisplayed = false;
        expressionFromHistoryForResult = null; // Não estamos usando um resultado para recálculo, mas sim a expressão diretamente
    } else {
        // Se estamos "A usar Resultado", mostramos o resultado numérico (como string 'value')
        // mas guardamos a expressão original para ser usada se o próximo input for um operador.
        resultDisplayed = true; // O display agora mostra um "resultado"
        expressionFromHistoryForResult = originalExpression; // Guarda a expressão que gerou este resultado
    }

    const historyPanel = document.getElementById('historyPanel');
    if (historyPanel) {
        historyPanel.classList.remove('show');
    }
}
