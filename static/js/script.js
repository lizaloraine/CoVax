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

function toggleSidebar() {
    const navbar = document.getElementById('navbar');
    const openButton = document.getElementById('open-sidebar');
    const closeButton = document.getElementById('close-sidebar');

    navbar.classList.toggle('show');
    openButton.style.display = navbar.classList.contains('show') ? 'none' : 'block';
    closeButton.style.display = navbar.classList.contains('show') ? 'block' : 'none';
}

window.addEventListener('resize', function() {
    const navbar = document.getElementById('navbar');
    if (window.innerWidth > 700) {
        navbar.classList.remove('show');
        document.getElementById('open-sidebar').style.display = 'none';
        document.getElementById('close-sidebar').style.display = 'none';
    }else {
        document.getElementById('open-sidebar').style.display = 'block';
        document.getElementById('close-sidebar').style.display = 'none';
    }
});