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


document.getElementById('foto').addEventListener('change', function(event) {
    var reader = new FileReader();
    reader.onload = function() {
        var preview = document.getElementById('preview');
        preview.src = reader.result;
        preview.style.display = 'block';
    }
    reader.readAsDataURL(event.target.files[0]);
});
    

// Função para atualizar textos estáticos após selecionar um elemento select
function updateInfo(selectId, fields) {
    var select = document.getElementById(selectId);
    var selectedOption = select.options[select.selectedIndex];
    var baseUrl = select.getAttribute('data-base-url');

    Object.keys(fields).forEach(field => {
        var element = document.getElementById(fields[field]);
        if (element) {
            if (field === 'fotos') {
                element.src = baseUrl + selectedOption.getAttribute('data-' + field);
            } else {
                var value = selectedOption.getAttribute('data-' + field);
                element.innerHTML = value;
                if (field === 'active') {
                    element.style.color = value === 'True' ? 'green' : 'red';
                }
            }
        }
    });
}

// Função para auxiliar na edição de itens do RPN
function updateText(selectId, textId, data) {
    var select = document.getElementById(selectId);
    var selectedValue = select.value;
    var textElement = document.getElementById(textId);
    textElement.innerText = data[selectedValue] || "None";
}
    