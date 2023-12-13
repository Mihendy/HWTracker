let textarea = document.getElementById("TextArea");

textarea.addEventListener("input", function () {
    let lines = textarea.value.split("\n");

    if (lines.length > 5) {
        textarea.value = lines.slice(0, 5).join("\n");
    }
});