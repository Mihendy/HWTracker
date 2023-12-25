document.getElementById("copy-button").addEventListener("click", function () {
    let input = document.getElementById("invite-url");
    input.select();
    input.setSelectionRange(0, input.value.length);
    document.execCommand("copy");
});


let textValue = document.getElementById("group-name").value

document.getElementById("group-name").addEventListener("input", function () {
    let renameButton = document.getElementById("rename-button");
    renameButton.disabled = this.value === textValue;
});