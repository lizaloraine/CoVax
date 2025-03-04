const modal = document.getElementById('detailsModal');
const closeModalBtn = document.querySelector('.close-modal');
const checkStatusBtn = document.getElementById('check-status-btn');
const cancelRequestBtn = document.getElementById('cancel-request-btn');
const sendCodeBtn = document.getElementById('send-code-btn');
const refNoInput = document.getElementById('ref-no');
const verificationCodeInput = document.getElementById('verification-code');
const refNoFeedback = document.getElementById('ref-no-feedback');
const verificationFeedback = document.getElementById('verification-feedback');

const modalTitle = document.getElementById('modal-title');
const modalBody = document.getElementById('modal-body');

//Modal for Check Status
checkStatusBtn.addEventListener('click', function () {
    const refNo = document.getElementById('ref-no').value;
    if (!refNo) {
        alert('Please enter your reference number.');
        return;
    }

    fetch('/manage-requests', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            refNo: refNo,
            action: 'check_status'
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            modalTitle.textContent = 'Appointment Details';
            modalBody.innerHTML = `
                <p><strong>Appointment No.:</strong> ${refNo}</p>
                <p><strong>Date:</strong> ${data.appointment.date}</p>
                <p><strong>Time:</strong> ${data.appointment.time}</p>
                <p><strong>Patient Name:</strong> ${data.appointment.patient_name}</p>
                <p><strong>Status:</strong> ${data.appointment.status}</p>
                <p><strong>Center:</strong> ${data.appointment.center}</p>
            `;
            modal.style.display = 'block';
        } else {
            alert(data.message);
        }
    })
    .catch(error => console.error('Error:', error));
});

//Modal for Request Cancellation
cancelRequestBtn.addEventListener('click', function () {
    const refNo = document.getElementById('ref-no').value;
    const verificationCode = document.getElementById('verification-code').value;

    if (!refNo || !verificationCode) {
        if (!verificationCode) {
            verificationFeedback.textContent = "Please enter the verification code.";
            verificationFeedback.style.color = "red";
        }
        alert('Please enter both reference number and verification code.');
        return;
    }

    console.log("Sending cancel request with refNo:", refNo, "and verificationCode:", verificationCode);

    fetch('/manage-requests', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            refNo: refNo,
            verificationCode: verificationCode,
            action: 'cancel_request'
        }),
    })
    .then(response => response.json())
    .then(data => {
        console.log("Response data:", data);
        if (data.success) {
            modalTitle.textContent = 'Cancellation Details';
            modalBody.innerHTML = `
                <p><strong>Appointment No.:</strong> ${refNo}</p>
                <p><strong>Date:</strong> ${data.appointment.date}</p>
                <p><strong>Time:</strong> ${data.appointment.time}</p>
                <p><strong>Patient Name:</strong> ${data.appointment.patient_name}</p>
                <p><strong>Center:</strong> ${data.appointment.center}</p>
                <p><strong>Application Approved:</strong> Yes</p>
                <p>An email has been sent with the cancellation details.</p>
            `;
            modal.style.display = 'block';
        } else {
            alert(data.message);
        }
    })
    .catch(error => console.error('Error:', error));
});

let timer;
let timeLeft = 30; 

sendCodeBtn.addEventListener('click', function () {
    // Disable the button and start timer
    sendCodeBtn.disabled = true;
    sendCodeBtn.style.backgroundColor = '#ccc'; 
    sendCodeBtn.innerHTML = `Code Sent! (${timeLeft}s)`;

    console.log("Sending verification code...");

    // Start timer for resending code
    timer = setInterval(function () {
        timeLeft--;
        if (timeLeft <= 0) {
            clearInterval(timer);
            sendCodeBtn.disabled = false;
            sendCodeBtn.style.backgroundColor = '#28a745'; 
            sendCodeBtn.innerHTML = 'Send Code'; 
        } else {
            sendCodeBtn.innerHTML = `Code Sent! (${timeLeft}s)`;
        }
    }, 1000);
});

// Close modal
closeModalBtn.addEventListener('click', function () {
    modal.style.display = 'none';
});

// Close modal when clicking outside
window.addEventListener('click', function (event) {
    if (event.target === modal) {
        modal.style.display = 'none';
    }
});

// Check if appointment reference number is valid
refNoInput.addEventListener('input', function() {
    const refNo = refNoInput.value.trim();
    if (refNo) {
        checkAppointmentStatus(refNo).then(isValid => {
            if (isValid) {
                refNoFeedback.textContent = "Appointment found!";
                refNoFeedback.style.color = "green";
            } else {
                refNoFeedback.textContent = "Appointment not found.";
                refNoFeedback.style.color = "red";
            }
        });
    } else {
        refNoFeedback.textContent = "";
    }
});

// Function to check appointment status
function checkAppointmentStatus(refNo) {
    return fetch('/manage-requests', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            refNo: refNo,
            action: 'check_status'
        }),
    })
    .then(response => response.json())
    .then(data => {
        return data.success;
    });
}
