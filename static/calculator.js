// Funções da calculadora - Conjunto de funções para manipular a calculadora interativa

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
        
        // Mantém o foco no campo de introdução para permitir operações adicionais de teclado
        display.focus();
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
}

// clearDisplay : Apaga todo o conteúdo do campo de introdução (ecrã)
function clearDisplay() {
    document.getElementById('display').value = '';
    // Define o valor do campo de introdução como uma string vazia, apagando todo o conteúdo
    
    document.getElementById('display').focus();
    // Mantém o foco no campo de introdução após limpá-lo
    
    resultDisplayed = false; // Repõe o estado do indicador de resultado
    // Como o ecrã foi limpo, já não está a mostrar um resultado
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

    // Configurar o campo de introdução para permitir posicionamento do cursor
    const display = document.getElementById('display');
    // Obtém o elemento do campo de introdução
    
    if (display && display.value && !display.value.includes('Erro')) {
        // Verifica se o campo existe, tem algum valor e não contém 'Erro'
        
        // Se tiver valor e não for erro, considera como resultado
        resultDisplayed = true;
        // Se o campo já contiver um valor ao carregar a página (e não for uma mensagem de erro), 
        // considera-o como um resultado existente
    }
    
    if (display) {
        // Verifica se o campo existe
        
        // Torna o campo manipulável mas bloqueia entrada direta
        display.removeAttribute('readonly');
        // Remove o atributo "readonly" para permitir que o cursor seja posicionado
        
        // Permitir apenas teclas de navegação e retrocesso
        display.addEventListener('keydown', function(e) {
            // Adiciona detetor de eventos para teclas pressionadas no campo
            if (e.key === 'ArrowLeft' || e.key === 'ArrowRight' || e.key === 'Backspace' || 
                e.key === 'Home' || e.key === 'End' || e.key === 'Delete') {
                // Verifica se a tecla pressionada é uma das teclas de navegação ou edição permitidas
                
                // Permite estas teclas específicas
                if (e.key === 'Backspace') {
                    // Caso especial para a tecla de retrocesso
                    e.preventDefault(); // Impede o comportamento predefinido
                    backspaceDisplay(); // Usa a nossa própria função de retrocesso
                }
            } else {
                // Todas as outras teclas (números, letras, etc.)
                e.preventDefault(); // Impede a introdução direta de texto
                // Desta forma, o utilizador só pode adicionar conteúdo através dos botões da calculadora
            }
        });
        
        // Restaurar a posição do cursor quando o campo recebe foco
        display.addEventListener('focus', function() {
            // Adiciona detetor de eventos para quando o campo recebe foco
            
            // Mantém a posição atual do cursor ou posiciona no fim se não houver posição definida
            if (this.selectionStart !== undefined) {
                // Verifica se a propriedade selectionStart existe e está definida
                const pos = this.selectionStart; // Guarda a posição atual
                
                setTimeout(() => {
                    // Usa setTimeout para executar após o comportamento predefinido do navegador
                    this.setSelectionRange(pos, pos);
                    // Restaura a posição do cursor
                }, 0);
                // O setTimeout com 0ms coloca esta função na fila de tarefas do navegador
                // para ser executada logo após o processamento do evento de foco
                
                // Problema: Quando um campo recebe foco, alguns navegadores reposicionam
                // automaticamente o cursor (geralmente no final do texto)
                // Solução: O setTimeout coloca a nossa função na fila de tarefas para ser executada
                // após qualquer manipulação predefinida do cursor pelo navegador
            }
        });
        
        // Permitir clique para posicionar o cursor
        display.addEventListener('mouseup', function() {
            // O navegador já posiciona o cursor automaticamente quando o utilizador clica
            // Este detetor está aqui para possíveis funcionamentos adicionais futuros
        });
    }
});

// useHistoryItem : Utiliza um item do histórico na calculadora atual
function useHistoryItem(expression, result) {
    const display = document.getElementById('display');
    // Obtém o elemento do campo de introdução
    
    // Coloca a expressão no campo de introdução
    display.value = expression;
    // Substitui o conteúdo atual pelo valor da expressão do histórico
    
    // Define a posição do cursor no fim da expressão
    display.focus(); // Dá foco ao campo primeiro
    display.setSelectionRange(expression.length, expression.length);
    // Posiciona o cursor após o último carácter da expressão
    
    // Fecha o painel de histórico
    const historyPanel = document.getElementById('historyPanel');
    // Obtém o elemento do painel de histórico
    
    if (historyPanel) {
        // Verifica se o painel existe
        historyPanel.classList.remove('show');
        // Esconde o painel removendo a classe 'show'
    }
}