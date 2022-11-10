function deleteNote(noteId) {
    fetch('/delete-note', {
        method: 'POST',
        body: JSON.stringify({ noteId: noteId }),
    }).then((res) => { window.location.href = '/'; });
}

function deleteReservation(reservationId) {
    fetch('/delete-reservation', {
        method: 'POST',
        body: JSON.stringify({ reservationId: reservationId }),
    }).then((res) => { window.location.href = '/'; });
}