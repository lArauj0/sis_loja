const accordions = document.querySelectorAll('.accordion-collapse');
accordions.forEach((accordion) => {
    accordion.addEventListener('show.bs.collapse', () => {
        accordion.style.transition = 'height 0.4s ease';
    });
});

const form = document.querySelector('form');
form.addEventListener('submit', () => {
    const submitButton = form.querySelector('[type="submit"]');
    submitButton.disabled = true;
    submitButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Pesquisando...';
});

window.addEventListener('scroll', () => {
    document.body.style.backgroundPositionY = `${window.scrollY * 0.5}px`;
});
