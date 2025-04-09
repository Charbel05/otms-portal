document.getElementById('toggle-button').addEventListener('click', function() {
    const extraButtons = document.getElementById('extra-buttons');
    if (extraButtons.classList.contains('hidden')) {
        extraButtons.classList.remove('hidden');
    } else {
        extraButtons.classList.add('hidden');
    }
});

function showText(text) {
    const displayText = document.getElementById('display-text');
    displayText.textContent = text;
}

// Função para atualizar textos estáticos após selecionar um elemento select
function updateInfo(selectId, dataAttribute, fields, compareField) {
    var select = document.getElementById(selectId);
    var selectedOption = select.options[select.selectedIndex].text;
    var data = JSON.parse(select.getAttribute(dataAttribute));

    for (var i = 0; i < data.length; i++) {
        if (data[i][compareField] === selectedOption) { 
            for (var field in fields) {
                if (fields.hasOwnProperty(field)) {
                    var element = document.getElementById(fields[field]);
                    if (element) {
                        element.innerHTML = data[i][field];
                    }
                }
            }
            break;
        }
    }
}

// Exemplo de uso
updateInfo("loc", "data-info", {
    groups: "groups"
}, "description_category");  // Passar o campo de comparação como parâmetro



// Função para auxiliar na edição de itens do RPN
function updateText(selectId, textId, data) {
    var select = document.getElementById(selectId);
    var selectedValue = select.value;
    var textElement = document.getElementById(textId);
    textElement.innerText = data[selectedValue] || "None";
}




