function deleteTable(tableId) {
    fetch('/admin/delete-table', {
        method: 'POST',
        body: JSON.stringify({ tableId: tableId }),
    }).then((res) => { window.location.href = '/admin/'; });
}

function deleteReservation(reservationId) {
    fetch('/delete-reservation', {
        method: 'POST',
        body: JSON.stringify({ reservationId: reservationId }),
    }).then((res) => { window.location.href = '/'; });
}