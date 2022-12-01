const dateInput = document.getElementById('date');
const creditCardModal = document.getElementsByClassName('credit-card-modal');


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
            showCreditCardInput(data.isHighTraffic)
        });
    })
}

function showCreditCardInput(doDisplay) {
    if (doDisplay) creditCardModal[0].style.display = 'flex';
    else creditCardModal[0].style.display = 'none';
}