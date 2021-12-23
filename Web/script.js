const create = document.getElementById("create");

let input = document.getElementById("input-file");
let output = document.getElementById("output-file");

input.addEventListener('change', () => {
    document.getElementsByClassName("choosed-file-label")[0].textContent = input.files[0].name;
});

output.addEventListener('change', () => {
    document.getElementsByClassName("choosed-file-label")[1].textContent = output.files[0].name
});

create.addEventListener("click", () => {
    eel.start(input.files[0].name, output.files[0].name);
});