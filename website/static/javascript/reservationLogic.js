const reserveForm = document.getElementById('reservation-form');
const dateInput = document.getElementById('date');

reserveForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const registerBeforeSubmitting = confirm("Do you want to register?");
    if (registerBeforeSubmitting) {
        const registerCheckbox = document.getElementById('register-user');
        registerCheckbox.checked = true;
    }

    reserveForm.submit();
})

dateInput.addEventListener('change', (e) => {
    const date = e.target.value;
    isHighTraffic(date);
})

function isHighTraffic(date) {
    fetch('/high-traffic', {
    method: 'POST',
    body: JSON.stringify({ date: date }),
    }).then((res) => {
        res.json().then((data) => {
            console.log(data);
        });
    })
}