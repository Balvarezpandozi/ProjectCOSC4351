const billingAdressInput = document.getElementById('billing-address');
const billingAddressLabel = document.getElementById('billing-address-label');
const sameAddress = document.getElementById('billing-mailing-same');

sameAddress.addEventListener('change', () => {
    if (sameAddress.checked) {
        billingAdressInput.style.display = 'none';
        billingAddressLabel.style.display = 'none';
    } else {
        billingAdressInput.style.display = 'block';
        billingAddressLabel.style.display = 'block';
    }
});