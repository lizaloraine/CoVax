function validateStep(stepNumber) {
    const currentStep = document.getElementById(`step-${stepNumber}`);
    const inputs = currentStep.querySelectorAll('input[required], select[required], textarea[required]');
    let isValid = true;
    
    // Remove existing error messages
    currentStep.querySelectorAll('.error-message').forEach(msg => msg.remove());
    
    inputs.forEach(input => {
        input.classList.remove('error');
        
        if (!input.value.trim()) {
            isValid = false;
            input.classList.add('error');
            
            const errorMsg = document.createElement('div');
            errorMsg.className = 'error-message';
            errorMsg.textContent = 'This field is required';
            input.parentNode.appendChild(errorMsg);
        }

        // Special validation for radio button groups
        if (input.type === 'radio' && input.required) {
            const groupName = input.name;
            const checkedRadio = currentStep.querySelector(`input[name="${groupName}"]:checked`);
            if (!checkedRadio) {
                isValid = false;
                const container = input.closest('.radio-group');
                if (!container.querySelector('.error-message')) {
                    const errorMsg = document.createElement('div');
                    errorMsg.className = 'error-message';
                    errorMsg.textContent = 'Please select an option';
                    container.appendChild(errorMsg);
                }
            }
        }
    });
    
    // Specific validations for each step
    if (stepNumber === 1) {
        const email = currentStep.querySelector('input[type="email"]');
        if (email.value && !isValidEmail(email.value)) {
            isValid = false;
            email.classList.add('error');
            const errorMsg = document.createElement('div');
            errorMsg.className = 'error-message';
            errorMsg.textContent = 'Please enter a valid email address';
            email.parentNode.appendChild(errorMsg);
        }

        const phone = currentStep.querySelector('input[type="tel"]');
        if (phone.value && !isValidPhone(phone.value)) {
            isValid = false;
            const errorMsg = document.createElement('div');
            errorMsg.className = 'error-message';
            errorMsg.textContent = 'Please enter a valid phone number';
            phone.parentNode.appendChild(errorMsg);
        }
    }
    
    return isValid;
}

function nextStep(current) {
    if (validateStep(current)) {
        document.getElementById(`step-${current}`).style.display = "none";
        document.getElementById(`step-${current + 1}`).style.display = "block";
        
        // Update progress bar
        const steps = document.querySelectorAll('.step');
        steps[current].classList.add('active');
        
        // If moving to step 4, update review details
        if (current === 3) {
            updateReviewDetails();
        }
    }
}

function prevStep(current) {
    document.getElementById(`step-${current}`).style.display = "none";
    document.getElementById(`step-${current - 1}`).style.display = "block";
    
    // Update progress bar
    const steps = document.querySelectorAll('.step');
    steps[current - 1].classList.remove('active');
}

function updateReviewDetails() {
    const form = document.getElementById('appointmentForm');
    const reviewHtml = `
        <div class="review-group">
            <h4>Personal Information</h4>
            <p><strong>Name:</strong> ${form.fullName.value}</p>
            <p><strong>Date of Birth:</strong> ${form.dateOfBirth.value}</p>
            <p><strong>Gender:</strong> ${form.gender.value}</p>
            <p><strong>Phone:</strong> ${form.phone.value}</p>
            <p><strong>Email:</strong> ${form.email.value}</p>
            <p><strong>Address:</strong> ${form.address.value}</p>
        </div>
        <div class="review-group">
            <h4>Medical History</h4>
            <p><strong>Previous COVID-19 Vaccination:</strong> ${form.previousVaccine.value}</p>
            <p><strong>Preferred Vaccine:</strong> ${form.vaccineType.value}</p>
            <p><strong>Allergies:</strong> ${form.allergies.value === 'yes' ? 'Yes - ' + form.allergyDetails.value : 'No'}</p>
            <p><strong>Medical Conditions:</strong> ${form.conditions.value === 'yes' ? 'Yes - ' + form.conditionDetails.value : 'No'}</p>
            <p><strong>Pregnancy/Breastfeeding:</strong> ${form.pregnancy.value}</p>
            <p><strong>COVID-19 Symptoms:</strong> ${form.symptoms.value === 'yes' ? 'Yes - ' + form.symptomDetails.value : 'No'}</p>
        </div>
        <div class="review-group">
            <h4>Appointment Details</h4>
            <p><strong>Date:</strong> ${form.date.value}</p>
            <p><strong>Time:</strong> ${form.timeSlot.value}</p>
            <p><strong>Location:</strong> ${form.center.value}</p>
            <p><strong>Reminder Method:</strong> ${form.reminderMethod.value}</p>
            <p><strong>Assistance Required:</strong> ${form.assistance.value === 'yes' ? 'Yes - ' + form.assistanceDetails.value : 'No'}</p>
        </div>
    `;

    document.getElementById('review-details').innerHTML = reviewHtml;
}

// Date validation
document.querySelector('input[name="date"]').addEventListener('input', function() {
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const selectedDate = new Date(this.value);
    
    if (selectedDate < today) {
        this.setCustomValidity('Please select a future date');
    } else {
        this.setCustomValidity('');
        updateTimeSlots(this.value);
    }
});

// Update available time slots based on date
function updateTimeSlots(date) {
    const timeSelect = document.querySelector('select[name="timeSlot"]');
    timeSelect.innerHTML = '<option value="">Loading available slots...</option>';
    timeSelect.disabled = true;
    
    fetch(`/get-available-slots/${date}`)
        .then(response => response.json())
        .then(data => {
            timeSelect.innerHTML = '<option value="">Select Time</option>';
            
            if (data.daily_remaining <= 0) {
                timeSelect.innerHTML = '<option value="">No slots available for this date</option>';
                timeSelect.disabled = true;
                return;
            }
            
            data.available_slots.forEach(slot => {
                const option = document.createElement('option');
                option.value = slot.time;
                option.textContent = `${slot.time} (${slot.remaining} slots remaining)`;
                timeSelect.appendChild(option);
            });
            
            timeSelect.disabled = false;
            
            // Add daily limit warning if few slots remaining
            if (data.daily_remaining < 10) {
                const warningDiv = document.createElement('div');
                warningDiv.className = 'slot-warning';
                warningDiv.textContent = `Only ${data.daily_remaining} appointments remaining for this date`;
                timeSelect.parentNode.appendChild(warningDiv);
            }
        })
        .catch(error => {
            console.error('Error fetching time slots:', error);
            timeSelect.innerHTML = '<option value="">Error loading time slots</option>';
        });
}

function getAvailableSlots(date) {
    const allSlots = [
        '09:00 AM', '10:00 AM',
        '11:00 AM', '02:00 PM',
        '03:00 PM', '04:00 PM'
    ];
    
    // Randomly remove some slots to simulate unavailability
    return allSlots.filter(() => Math.random() > 0.3);
}

// Form validation feedback
document.querySelectorAll('.form-group input, .form-group select').forEach(input => {
    input.addEventListener('invalid', function() {
        this.classList.add('error');
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = this.validationMessage;
        this.parentNode.appendChild(errorDiv);
    });
    
    input.addEventListener('input', function() {
        this.classList.remove('error');
        const errorMessage = this.parentNode.querySelector('.error-message');
        if (errorMessage) {
            errorMessage.remove();
        }
    });
});

// Enhanced form submission
document.getElementById('appointmentForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    if (!validateStep(4)) {
        return;
    }
    
    // Show loading state
    const submitBtn = this.querySelector('.submit-btn');
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span class="spinner"></span> Processing...';
    
    // Generate reference number
    const refNo = 'VAX' + Date.now().toString().slice(-6);
    
    // Get reminder consent checkbox value safely
    const reminderCheckbox = document.querySelector('.checkbox-group input[type="checkbox"]:nth-of-type(2)');
    const reminderConsent = reminderCheckbox ? reminderCheckbox.checked : false;
    
    // Collect form data
    const formData = {
        refNo: refNo,
        fullName: this.fullName.value,
        phone: this.phone.value,
        email: this.email.value,
        center: this.center.value,
        vaccineType: this.vaccineType.value,
        date: this.date.value,
        timeSlot: this.timeSlot.value,
        reminderConsent: reminderConsent
    };
    
    // Send data to server
    fetch('/appointment/new', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showSuccessModal(formData, refNo);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('There was an error booking your appointment. Please try again.');
    })
    .finally(() => {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Confirm Appointment';
    });
});

function showSuccessModal(formData, refNo) {
    const modal = document.getElementById('successModal');
    modal.style.display = 'block';
    
    // Format date for display
    const appointmentDate = new Date(formData.date);
    const formattedDate = appointmentDate.toLocaleDateString('en-US', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
    
    document.getElementById('confirmation-details').innerHTML = `
        <div class="confirmation-header">
            <span class="success-icon">✓</span>
            <h3>Booking Successful!</h3>
            <p class="ref-number">Reference Number: ${refNo}</p>
        </div>
        <div class="confirmation-details">
            <div class="detail-group">
                <h4>Patient Information</h4>
                <p><strong>Name:</strong> ${formData.fullName}</p>
                <p><strong>Contact:</strong> ${formData.phone}</p>
                <p><strong>Email:</strong> ${formData.email || 'Not provided'}</p>
            </div>
            <div class="detail-group">
                <h4>Appointment Information</h4>
                <p><strong>Center:</strong> ${formData.center}</p>
                <p><strong>Vaccine:</strong> ${formData.vaccineType}</p>
                <p><strong>Date:</strong> ${formattedDate}</p>
                <p><strong>Time:</strong> ${formData.timeSlot}</p>
            </div>
        </div>
        <div class="important-notice">
            <h4>Important Reminders</h4>
            <ul>
                <li>Please arrive 15 minutes before your appointment</li>
                <li>Bring a valid ID</li>
                <li>Wear a face mask</li>
                <li>Cancel or reschedule at least 24 hours in advance</li>
            </ul>
        </div>
    `;
}

function downloadConfirmation() {
    // Implementation for downloading confirmation
    alert('Download functionality will be implemented');
}

function printConfirmation() {
    window.print();
}

function closeSuccessModal() {
    const modal = document.getElementById('successModal');
    modal.style.display = 'none';
    window.location.href = '/';
}

// Add event listener to update review details when reaching step 4
document.querySelector('.next-btn[onclick="nextStep(3)"]').addEventListener('click', updateReviewDetails);

// Update back to home button
const backButton = document.createElement('button');
backButton.className = 'back-home-btn';
backButton.innerHTML = '<i class="fas fa-arrow-left"></i>';
backButton.onclick = () => window.location.href = '/'; // Changed from '/' to '/home'
document.body.appendChild(backButton);

// Helper functions for validation
function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function isValidPhone(phone) {
    return /^[0-9]{11}$/.test(phone); // Validates 11-digit phone numbers
}

// Add input event listeners for real-time validation
document.querySelectorAll('.form-group input, .form-group select').forEach(input => {
    input.addEventListener('input', function() {
        this.classList.remove('error');
        const errorMessage = this.parentNode.querySelector('.error-message');
        if (errorMessage) {
            errorMessage.remove();
        }
    });
});

// Add event listeners for conditional fields
document.addEventListener('DOMContentLoaded', function() {
    // Handle allergies conditional field
    const allergyRadios = document.querySelectorAll('input[name="allergies"]');
    const allergyDetails = document.querySelector('textarea[name="allergyDetails"]');
    allergyRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            allergyDetails.style.display = this.value === 'yes' ? 'block' : 'none';
            allergyDetails.required = this.value === 'yes';
        });
    });

    // Handle medical conditions conditional field
    const conditionRadios = document.querySelectorAll('input[name="conditions"]');
    const conditionDetails = document.querySelector('textarea[name="conditionDetails"]');
    conditionRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            conditionDetails.style.display = this.value === 'yes' ? 'block' : 'none';
            conditionDetails.required = this.value === 'yes';
        });
    });

    // Handle COVID symptoms conditional field
    const symptomRadios = document.querySelectorAll('input[name="symptoms"]');
    const symptomDetails = document.querySelector('textarea[name="symptomDetails"]');
    symptomRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            symptomDetails.style.display = this.value === 'yes' ? 'block' : 'none';
            symptomDetails.required = this.value === 'yes';
        });
    });

    // Handle assistance conditional field
    const assistanceRadios = document.querySelectorAll('input[name="assistance"]');
    const assistanceDetails = document.querySelector('textarea[name="assistanceDetails"]');
    assistanceRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            assistanceDetails.style.display = this.value === 'yes' ? 'block' : 'none';
            assistanceDetails.required = this.value === 'yes';
        });
    });

    // Handle other vaccine type
    const vaccineSelect = document.querySelector('select[name="vaccineType"]');
    const otherVaccine = document.querySelector('input[name="otherVaccine"]');
    vaccineSelect.addEventListener('change', function() {
        otherVaccine.style.display = this.value === 'other' ? 'block' : 'none';
        otherVaccine.required = this.value === 'other';
    });
});
