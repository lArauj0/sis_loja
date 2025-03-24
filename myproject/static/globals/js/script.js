const form = document.querySelector('form');
form.addEventListener('submit', () => {
    const submitButton = form.querySelector('[type="submit"]');
    submitButton.disabled = true;
    submitButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Pesquisando...';
});

window.addEventListener('scroll', () => {
    document.body.style.backgroundPositionY = `${window.scrollY * 0.5}px`;
});
