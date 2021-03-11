function setClickByClass(clickTarget, elementTarget, classTaggle) {
    const clickElements = document.getElementsByClassName(clickTarget);
    for (let i = 0; i < clickElements.length; i++) {
        const element = clickElements[i];
        element.addEventListener('click', function () {
            const target = element.getElementsByClassName(elementTarget)[0];
            target.classList.toggle(classTaggle);
        });
    }
}

function setClickById(clickTarget, elementTarget, classTaggle) {
    const clickElemet = document.getElementById(clickTarget);
    clickElemet.addEventListener('click', function () {
        const target = document.getElementById(elementTarget);
        target.classList.toggle(classTaggle);
    });
}

document.addEventListener(
    'DOMContentLoaded', function () {
        setClickByClass('week', 'week-info', 'sub-cat-closed');
        setClickById('hamburger-bar', 'navigation', 'navigation-open');
    }
)
