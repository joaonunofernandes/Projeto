// Variáveis globais para controlo da calculadora
let resultDisplayed = false;
let expressionFromHistoryForResult = null;

/**
 * Adiciona um número ou operador ao campo de introdução (ecrã)
 * @param {string} value - Carácter a ser adicionado ao ecrã
 */
function appendToDisplay(value) {
    const display = document.getElementById('display');
    const isOperator = ['+', '-', '*', '/', '×', '÷', '**'].includes(value);
    const isMathFunction = value.endsWith('(');
    const isPowerOperation = value === '**' || value === '**2';

    if (resultDisplayed) {
        if (isOperator || isMathFunction || isPowerOperation) {
            if (expressionFromHistoryForResult) {
                display.value = '(' + expressionFromHistoryForResult + ')' + value;
                expressionFromHistoryForResult = null;
            } else if (isMathFunction) {
                display.value = value.slice(0, -1) + display.value + ')';
            } else {
                display.value = display.value + value;
            }
        } else {
            display.value = value;
            expressionFromHistoryForResult = null;
        }
        resultDisplayed = false;
        display.focus();
        display.setSelectionRange(display.value.length, display.value.length);
        return;
    }

    const cursorPos = display.selectionStart;
    const textBefore = display.value.substring(0, cursorPos);
    const textAfter = display.value.substring(cursorPos);

    if (!isOperator && expressionFromHistoryForResult) {
        expressionFromHistoryForResult = null;
    }

    if (value.endsWith('(')) {
        display.value = textBefore + value + ')' + textAfter;
        const newCursorPos = cursorPos + value.length;
        display.setSelectionRange(newCursorPos, newCursorPos);
    } else {
        display.value = textBefore + value + textAfter;
        const newCursorPos = cursorPos + value.length;
        display.setSelectionRange(newCursorPos, newCursorPos);
    }

    display.focus();
}

/**
 * Apaga todo o conteúdo do campo de introdução (ecrã)
 */
function clearDisplay() {
    document.getElementById('display').value = '';
    document.getElementById('display').focus();
    resultDisplayed = false;
    expressionFromHistoryForResult = null;
}

/**
 * Remove o carácter à esquerda do cursor
 */
function backspaceDisplay() {
    const display = document.getElementById('display');
    const cursorPos = display.selectionStart;
    
    if (cursorPos === 0) return;
    
    const textBefore = display.value.substring(0, cursorPos - 1);
    const textAfter = display.value.substring(cursorPos);
    
    display.value = textBefore + textAfter;
    
    const newCursorPos = cursorPos - 1;
    display.setSelectionRange(newCursorPos, newCursorPos);
    display.focus();
}

/**
 * Move o cursor uma posição para a esquerda
 */
function moveCursorLeft() {
    const display = document.getElementById('display');
    const cursorPos = display.selectionStart;
    
    if (cursorPos > 0) {
        display.setSelectionRange(cursorPos - 1, cursorPos - 1);
    }
    
    display.focus();
}

/**
 * Move o cursor uma posição para a direita
 */
function moveCursorRight() {
    const display = document.getElementById('display');
    const cursorPos = display.selectionStart;
    const maxPos = display.value.length;
    
    if (cursorPos < maxPos) {
        display.setSelectionRange(cursorPos + 1, cursorPos + 1);
    }
    
    display.focus();
}

/**
 * Submete o formulário para calcular o resultado
 */
function submitForm() {
    const form = document.querySelector('form');
    if (form) {
        setTimeout(function() {
            resultDisplayed = true;
            expressionFromHistoryForResult = null;
        }, 10);

        form.submit();
    }
}

/**
 * Verifica se uma tecla é válida para a calculadora
 * @param {string} key - Tecla pressionada
 * @returns {boolean} - Verdadeiro se a tecla for válida
 */
function isCalculatorKey(key) {
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

/**
 * Processa entrada de teclado
 * @param {string} key - Tecla pressionada
 */
function handleKeyboardInput(key) {
    const display = document.getElementById('display');
    const isDigit = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'].includes(key);
    
    if (isDigit && resultDisplayed) {
        display.value = key;
        display.setSelectionRange(1, 1);
        resultDisplayed = false;
        return;
    }
    
    switch(key) {
        case '0': case '1': case '2': case '3': case '4':
        case '5': case '6': case '7': case '8': case '9':
        case '+': case '-':
            appendToDisplay(key);
            break;
        
        case '*': case '×':
            appendToDisplay('*');
            break;
        case '/': case '÷':
            appendToDisplay('/');
            break;
        
        case '.': case ',':
            appendToDisplay('.');
            break;
            
        case '(':
            appendToDisplay('(');
            break;
        case ')':
            appendToDisplay(')');
            break;
            
        case 'p': case 'π':
            appendToDisplay('pi');
            break;
            
        case 'i':
            appendToDisplay('i');
            break;
        case 'j':
            appendToDisplay('j');
            break;
        case 'k':
            appendToDisplay('k');
            break;
            
        case 'e':
            appendToDisplay('exp(');
            break;
            
        case '=':
            submitForm();
            break;
            
        case 's':
            appendToDisplay('sin(');
            break;
        case 'c':
            appendToDisplay('cos(');
            break;
        case 't':
            appendToDisplay('tan(');
            break;
        
        case 'l':
            appendToDisplay('log(');
            break;
    }
    
    if (display && resultDisplayed === false) {
        const cursorPos = display.selectionStart;
        if (cursorPos === null || cursorPos === undefined || 
            cursorPos < 0 || cursorPos > display.value.length) {
            display.setSelectionRange(display.value.length, display.value.length);
        }
    }
}

/**
 * Utiliza um item do histórico na calculadora
 * @param {string} value - Valor a ser utilizado
 * @param {boolean} isExpression - Se é uma expressão ou resultado
 * @param {string} originalExpression - Expressão original que gerou o resultado
 */
function useHistoryItem(value, isExpression, originalExpression = null) {
    const display = document.getElementById('display');
    display.value = value;

    display.focus();
    display.setSelectionRange(value.length, value.length);

    if (isExpression) {
        resultDisplayed = false;
        expressionFromHistoryForResult = null;
    } else {
        resultDisplayed = true;
        expressionFromHistoryForResult = originalExpression;
    }

    const historyPanel = document.getElementById('historyPanel');
    if (historyPanel) {
        historyPanel.classList.remove('show');
    }
}

// Eventos carregados quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', function() {
    // Controlo do menu suspenso
    const dropdownButton = document.getElementById('dropdownButton');
    const dropdownContent = document.getElementById('dropdownContent');
    const dropdown = document.getElementById('mainDropdown');
    
    if (dropdownButton) {
        dropdownButton.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            dropdownContent.classList.toggle('show');
        });
    }
    
    document.addEventListener('click', function(e) {
        if (dropdown && !dropdown.contains(e.target)) {
            dropdownContent.classList.remove('show');
        }
    });

    // Submissão do formulário
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function() {
            setTimeout(function() {
                resultDisplayed = true;
            }, 10);
        });
    }

    // Painel de histórico
    const historyButton = document.getElementById('historyButton');
    const historyPanel = document.getElementById('historyPanel');
    const closeHistoryBtn = document.getElementById('closeHistoryBtn');
    
    if (historyButton && historyPanel) {
        historyButton.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            historyPanel.classList.toggle('show');
        });
    }
    
    if (closeHistoryBtn && historyPanel) {
        closeHistoryBtn.addEventListener('click', function() {
            historyPanel.classList.remove('show');
        });
    }
    
    document.addEventListener('click', function(e) {
        if (historyPanel && historyPanel.classList.contains('show')) {
            if (!historyPanel.contains(e.target) && !historyButton.contains(e.target)) {
                historyPanel.classList.remove('show');
            }
        }
    });
    
    // Alternador de modo angular
    const angleToggle = document.getElementById('angleModeToggle');
    const radText = document.querySelector('.angle-mode-toggle span:first-child');
    const degText = document.querySelector('.angle-mode-toggle span:last-child');
    
    function updateAngleModeDisplay() {
        if (angleToggle && angleToggle.checked) {
            radText.classList.remove('active');
            degText.classList.add('active');
        } else {
            radText.classList.add('active');
            degText.classList.remove('active');
        }
    }
    
    if (angleToggle) {
        updateAngleModeDisplay();
        
        angleToggle.addEventListener('change', function() {
            updateAngleModeDisplay();
            window.location.href = '/toggle_angle_mode';
        });
    }

    // Configuração do campo de visualização
    const display = document.getElementById('display');
    
    if (display && display.value && !display.value.includes('Erro')) {
        resultDisplayed = true;
    }
    
    if (display) {        
        display.tabIndex = 0;
        
        display.addEventListener('keydown', function(e) {
            e.preventDefault();
            
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
            
            if (e.key === 'Backspace') {
                backspaceDisplay();
                return;
            }
            
            if (e.key === 'Delete') {
                const cursorPos = display.selectionStart;
                if (cursorPos < display.value.length) {
                    display.value = display.value.substring(0, cursorPos) + 
                                   display.value.substring(cursorPos + 1);
                    display.setSelectionRange(cursorPos, cursorPos);
                }
                return;
            }
            
            if (e.key === 'Escape') {
                clearDisplay();
                return;
            }
            
            if (e.key === 'Enter') {
                submitForm();
                return;
            }
            
            handleKeyboardInput(e.key);
        });
    }
    
    // Eventos de teclado globais
    document.addEventListener('keydown', function(e) {
        if (display && document.activeElement !== display && 
            !e.ctrlKey && !e.altKey && !e.metaKey) {
            
            if (isCalculatorKey(e.key)) {
                e.preventDefault();
                
                display.focus();
                
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
                
                handleKeyboardInput(e.key);
            }
        }
    });
});