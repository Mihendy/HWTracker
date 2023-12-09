let textarea = document.getElementById("TextArea");

textarea.addEventListener("input", function () {
    let lines = textarea.value.split("\n");
    // for (let i = 0; i < lines.length; i++) {
    //     if (lines[i].length > 32) {
    //         lines[i] = lines[i].substring(0, 32);
    //         lines[i + 1] = lines[i].substring(32,);
    //     }
    // }
    // textarea.value = lines.join("\n");

    if (lines.length > 5) {
        textarea.value = lines.slice(0, 5).join("\n");
    }
});