const create = document.getElementById("create");

let input = document.getElementById("input-file");
let output = document.getElementById("output-file");
let checkbox = document.getElementById("send");

// Pop Up
let popupBg = document.getElementsByClassName('popup__bg')[0]; // Фон попап окна
let popup = document.getElementsByClassName('popup')[0]; // Само окно
let openPopupButton = document.getElementsByClassName('open-popup')[0]; // Кнопки для показа окна
let closePopupButton = document.getElementsByClassName('close-popup')[0]; // Кнопка для скрытия окна

openPopupButton.addEventListener('click', (e) => { // Для каждой вешаем обработчик событий на клик
    e.preventDefault(); // Предотвращаем дефолтное поведение браузера
    popupBg.classList.add('active'); // Добавляем класс 'active' для фона
    popup.classList.add('active'); // И для самого окна
})

closePopupButton.addEventListener('click', () => { // Вешаем обработчик на крестик
    popupBg.classList.remove('active'); // Убираем активный класс с фона
    popup.classList.remove('active'); // И с окна
});

document.addEventListener('click', (e) => { // Вешаем обработчик на весь документ
    if (e.target === popupBg) { // Если цель клика - фон, то:
        popupBg.classList.remove('active'); // Убираем активный класс с фона
        popup.classList.remove('active'); // И с окна
    }
});

let emailForm = document.forms[popup.getAttribute('name')];

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
    try {
        if (output.files[0] == undefined){
            eel.start(input.files[0].name, '', value);
        } else {
            eel.start(input.files[0].name, output.files[0].name, value);
        }
    } catch (error) {
        if (error instanceof TypeError) document.getElementById('error').textContent = "Выберите файлы";
        else document.getElementById('error').textContent = "Что то пошло не так...";
    }

});

document.getElementById('send-email').addEventListener('click', () => {
    let email = emailForm.elements["email"].value;
    let password = emailForm.elements["password"].value;
    console.log(email, password);
    eel.create_email_info(email, password) // Оба из формы
})

eel.expose(raise_error);
function raise_error(error) {
    document.getElementById('error').textContent = error;
}