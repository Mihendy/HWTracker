function showOtherField(selectElement) {
    let otherGroupDiv = document.getElementById("otherGroupDiv");
    let otherGroupInput = document.getElementById("otherGroupInput");

    if (selectElement.value === "other") {
        otherGroupDiv.removeAttribute("style");
        otherGroupInput.required = true;
    } else {
        otherGroupDiv.style.display = "none";
        otherGroupInput.required = false;
        otherGroupInput.value = '';
    }
}

let groupInput = document.getElementById("groupInput")
showOtherField(groupInput)