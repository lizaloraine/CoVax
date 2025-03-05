document.addEventListener('DOMContentLoaded', function() {
    // Search functionality
    const searchInput = document.getElementById('searchInput');
    searchInput.addEventListener('input', filterAppointments);

    // Filter functionalities
    const statusFilter = document.getElementById('statusFilter');
    const vaccineFilter = document.getElementById('vaccineFilter');
    const dateFilter = document.getElementById('dateFilter');

    statusFilter.addEventListener('change', filterAppointments);
    vaccineFilter.addEventListener('change', filterAppointments);
    dateFilter.addEventListener('change', filterAppointments);

    // Close modal when clicking the close button or outside the modal
    const modal = document.getElementById('viewModal');
    const closeBtn = document.querySelector('.close');

    closeBtn.onclick = function() {
        modal.style.display = 'none';
    }

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    }
});

function filterAppointments() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const status = document.getElementById('statusFilter').value.toLowerCase();
    const vaccine = document.getElementById('vaccineFilter').value.toLowerCase();
    const date = document.getElementById('dateFilter').value;

    const rows = document.querySelectorAll('tbody tr');

    rows.forEach(row => {
        const name = row.children[1].textContent.toLowerCase();
        const rowStatus = row.querySelector('.status-badge').textContent.toLowerCase();
        const rowVaccine = row.children[2].textContent.toLowerCase();
        const rowDate = row.children[3].textContent;

        const matchesSearch = name.includes(searchTerm);
        const matchesStatus = !status || rowStatus.includes(status);
        const matchesVaccine = !vaccine || rowVaccine.includes(vaccine);
        const matchesDate = !date || rowDate === date;

        row.style.display = 
            matchesSearch && matchesStatus && matchesVaccine && matchesDate
            ? '' 
            : 'none';
    });
}

function viewAppointment(appointmentNo) {
    fetch(`/get-appointment/${appointmentNo}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                // Update modal with appointment details
                document.getElementById('modal-name').textContent = data.appointment.patient_name;
                document.getElementById('modal-phone').textContent = data.appointment.phone;
                document.getElementById('modal-center').textContent = data.appointment.center;
                document.getElementById('modal-ref').textContent = data.appointment.appointment_no;
                document.getElementById('modal-date').textContent = data.appointment.date;
                document.getElementById('modal-time').textContent = data.appointment.time;
                document.getElementById('modal-vaccine').textContent = data.appointment.vaccine_type;
                document.getElementById('modal-status').textContent = data.appointment.status;

                // Show modal
                const modal = document.getElementById('viewModal');
                modal.style.display = 'block';
            } else {
                alert(data.message || 'Failed to load appointment details');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while loading appointment details. Please try again.');
        });
}

function approveAppointment(appointmentNo) {
    if (confirm('Are you sure you want to approve this appointment?')) {
        fetch('/approve-appointment', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ appointment_no: appointmentNo })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Update status badge
                const row = document.querySelector(`tr[data-appointment="${appointmentNo}"]`);
                const statusBadge = row.querySelector('.status-badge');
                statusBadge.textContent = 'Confirmed';
                statusBadge.className = 'status-badge confirmed';
                
                // Hide approve/cancel buttons
                const actionButtons = row.querySelector('.actions');
                actionButtons.innerHTML = `
                    <button onclick="viewAppointment('${appointmentNo}')" class="action-btn view">
                        <i class="fas fa-eye"></i>
                    </button>`;

                // Show success message
                alert('Appointment approved successfully');
            } else {
                alert(data.message || 'Failed to approve appointment');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while approving the appointment');
        });
    }
}

function cancelAppointment(appointmentNo) {
    if (confirm('Are you sure you want to cancel this appointment?')) {
        fetch('/cancel-appointment', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ appointment_no: appointmentNo })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Update status badge
                const row = document.querySelector(`tr[data-appointment="${appointmentNo}"]`);
                const statusBadge = row.querySelector('.status-badge');
                statusBadge.textContent = 'Cancelled';
                statusBadge.className = 'status-badge cancelled';
                
                // Hide approve/cancel buttons
                const actionButtons = row.querySelector('.actions');
                actionButtons.innerHTML = `
                    <button onclick="viewAppointment('${appointmentNo}')" class="action-btn view">
                        <i class="fas fa-eye"></i>
                    </button>`;

                // Show success message
                alert('Appointment cancelled successfully');
            } else {
                alert(data.message || 'Failed to cancel appointment');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while cancelling the appointment');
        });
    }
}
