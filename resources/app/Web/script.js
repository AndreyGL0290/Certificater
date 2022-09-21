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
let inputLabel = ''
let outputLabel = ''
input.addEventListener('change', () => {
    if (input.files[0] === undefined) {
        inputLabel = 'Не выбрано'
    } else {
        inputLabel = input.files[0].name
    }
    if (inputLabel.length > 20) inputLabel = inputLabel.slice(0, 19)+'...xlsx';
    document.getElementsByClassName("choosed-file-label")[0].textContent = inputLabel;
});

output.addEventListener('change', () => {
    if (output.files[0] === undefined) {
        outputLabel = 'Не выбрано'
    } else {
        outputLabel = output.files[0].name
    }
    if (outputLabel.length > 20) outputLabel = outputLabel.slice(0, 19)+'...pptx';
    document.getElementsByClassName("choosed-file-label")[1].textContent = outputLabel;
});

// Когда нажимается кнопка "Отправить после сохранения" ее значение меняется
let value = 0;
checkbox.addEventListener('click', () => {
    if (!value) value = 1;
    else value = 0;
});

// Запускаем главный алгоритм
const sendToPython = (args) => {
    window.api.start(args)
};

// Обновляем почту пользователя
const updateEmail = (args) => {
    window.api.updateEmail(args)
};

// Добавляем ошибку, пришедшую с бэка, на главную страницу
window.api.onResponse((message) => {
    document.getElementById('error').textContent = message;
})


btn = document.getElementById('create');

btn.addEventListener('click', () => {
    try {
        if (output.files[0] === undefined){
            sendToPython([input.files[0].path, '', value]);
        } else {
            sendToPython([input.files[0].path, output.files[0].path, value]);
        }
    } catch (error) {
        if (error instanceof TypeError) document.getElementById('error').textContent = "Выберите файлы";
        else document.getElementById('error').textContent = "Что то пошло не так..."; console.log(error);
    }
});

document.getElementById('send-email').addEventListener('click', () => {
    let email = emailForm.elements["email"].value;
    let password = emailForm.elements["password"].value;
    // console.log(email, password);
    updateEmail([email, password]);
});