const create = document.getElementById("create");

let input = document.getElementById("input-file");
let output = document.getElementById("output-file");
let checkbox = document.getElementById("send");

input.addEventListener('change', () => {
    document.getElementsByClassName("choosed-file-label")[0].textContent = input.files[0].name;
});

output.addEventListener('change', () => {
    document.getElementsByClassName("choosed-file-label")[1].textContent = output.files[0].name
});

// Когда нажимается кнопка "Отправить после сохранения" ее значение меняется
let value = false;
checkbox.addEventListener('click', () => {
    if (!value) value = true;
    else value = false;
});

create.addEventListener("click", () => {
    eel.start(input.files[0].name, output.files[0].name, value);
});