function setWeekOpenClick() {
    const clickElements = document.getElementsByClassName('week');
    for (let i = 0; i < clickElements.length; i++) {
        const element = clickElements[i];
        element.addEventListener('click', function (clickElement) {
            if (clickElement.target.tagName === 'A') {
                return false;
            }
            const target = element.getElementsByClassName('week-info')[0];
            target.classList.toggle('sub-cat-closed');
            const arrow = element.getElementsByTagName("ion-icon")[0];
            arrow.classList.toggle('arrow-open');

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
        setWeekOpenClick();
        setClickById('hamburger-bar', 'navigation', 'navigation-open');
    }
)
