function checkWindowSize() {
    let element = document.getElementById("row-col-media");
    let element2 = document.getElementById("small-media")

    if (window.innerWidth < 768) {
        element.classList.add("flex-column");
        element2.classList.remove("w-50");
    } else {
        element.classList.remove("flex-column");
        element2.classList.add("w-50");
    }
}

window.addEventListener("resize", checkWindowSize);
checkWindowSize()