bubble = document.getElementById("bubble");

document.body.onpointermove = (e) => {
    const {
        clientX, clientY
    } = e;

    bubble.animate({
        left: `${clientX - bubble.offsetWidth / 2}px`,
        top: `${clientY - bubble.offsetHeight / 2}px`
    }, {
        duration: 3000, fill: "forwards"
    })
}

flashes = document.getElementById("flashes");
setTimeout(() => {
    flashes.style.display = "none";
}, 3400);