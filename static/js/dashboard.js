document.addEventListener('DOMContentLoaded', function() {
    // Appointment Trends Chart
    const trendsCtx = document.getElementById('appointmentTrends').getContext('2d');
    new Chart(trendsCtx, {
        type: 'bar',
        data: {
            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            datasets: [{
                label: 'Appointments',
                data: [12, 19, 15, 17, 14, 8, 5],
                backgroundColor: '#28a745',
                borderRadius: 5
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 5
                    }
                }
            }
        }
    });

    // Vaccine Distribution Chart
    const distributionCtx = document.getElementById('vaccineDistribution').getContext('2d');
    new Chart(distributionCtx, {
        type: 'pie',
        data: {
            labels: ['Pfizer', 'Moderna', 'Johnson & Johnson'],
            datasets: [{
                data: [45, 35, 20],
                backgroundColor: [
                    '#4caf50',
                    '#2196f3',
                    '#ff9800'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
});

function viewAppointment(appointmentNo) {
    // Implement view appointment details
    console.log('Viewing appointment:', appointmentNo);
}
