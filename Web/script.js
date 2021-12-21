const create = document.getElementById("create");


create.addEventListener("click", () => {
    let inputFile = document.getElementById("input-file").files[0].name;
    let outputFile = document.getElementById("output-file").files[0].name;
    console.log(inputFile, outputFile);
    eel.start(inputFile, outputFile);
});
let input = document.getElementById("input-file");
input.addEventListener('change', () => {
    console.log(input.files[0].name)
    document.getElementsByClassName("choosed-file-label")[0].innerHTML = input.files[0].name;
});

let output = document.getElementById("output-file");
output.addEventListener('change', () => {
    document.getElementsByClassName("choosed-file-label")[1].innerHTML = output.files[0].name
});