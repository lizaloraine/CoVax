function openModal() {
    document.getElementById("appointmentModal").style.display = "block";
}

function closeModal() {
    document.getElementById("appointmentModal").style.display = "none";
}

function nextStep(current) {
    document.getElementById(`step-${current}`).style.display = "none";
    document.getElementById(`step-${current + 1}`).style.display = "block";

    document.getElementById(`step${current}`).classList.remove("active");
    document.getElementById(`step${current + 1}`).classList.add("active");
}

function prevStep(current) {
    document.getElementById(`step-${current}`).style.display = "none";
    document.getElementById(`step-${current - 1}`).style.display = "block";

    document.getElementById(`step${current}`).classList.remove("active");
    document.getElementById(`step${current - 1}`).classList.add("active");
}
