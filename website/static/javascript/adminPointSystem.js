function addPoints(userId) {
    // Obtain points from input
    const pointsInput = document.getElementById(`add-points-${userId}`);
    const points = parseInt(pointsInput.value);

    // Reset input
    pointsInput.value = "";

    // Update database
    fetch(`/admin/add-points/${points}/${userId}`, {method: "POST"})
    .then(response => {
        response.json().then(data => {
            updatePointsView(userId, data.points);
        });
    });
}

function updatePointsView(userId, points) {
    // Get user points view
    const pointsView = document.getElementById(`user-points-${userId}`);
    pointsView.innerHTML = points;
}