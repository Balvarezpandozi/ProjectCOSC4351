const reserveForm = document.getElementById('reservation-form');

reserveForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const registerBeforeSubmitting = confirm("Do you want to register?");
    if (registerBeforeSubmitting) {
        const registerCheckbox = document.getElementById('register-user');
        registerCheckbox.checked = true;
    }

    reserveForm.submit();
})