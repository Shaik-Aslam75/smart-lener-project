// ================================
// Smart Lender AI - script.js
// ================================

// Page Loaded
document.addEventListener("DOMContentLoaded", function () {
    console.log("Smart Lender AI Loaded Successfully");
});

// Confirm Logout
function confirmLogout() {
    return confirm("Are you sure you want to logout?");
}

// Apply to Logout Button
const logoutBtn = document.getElementById("logoutBtn");

if (logoutBtn) {
    logoutBtn.addEventListener("click", function (e) {
        if (!confirmLogout()) {
            e.preventDefault();
        }
    });
}

// Button Animation
const buttons = document.querySelectorAll(".btn");

buttons.forEach(btn => {
    btn.addEventListener("mouseenter", () => {
        btn.style.transform = "scale(1.05)";
        btn.style.transition = "0.3s";
    });

    btn.addEventListener("mouseleave", () => {
        btn.style.transform = "scale(1)";
    });
});

// Card Hover
const cards = document.querySelectorAll(".card");

cards.forEach(card => {

    card.addEventListener("mouseenter", () => {
        card.style.transform = "translateY(-8px)";
        card.style.transition = "0.3s";
    });

    card.addEventListener("mouseleave", () => {
        card.style.transform = "translateY(0)";
    });

});

// Loading Effect
window.onload = function () {

    document.body.style.opacity = "1";

};

// Auto Hide Alerts
setTimeout(function () {

    let alerts = document.querySelectorAll(".alert");

    alerts.forEach(alert => {
        alert.style.display = "none";
    });

}, 3000);

// Loan Form Validation
const loanForm = document.querySelector("form");

if (loanForm) {

    loanForm.addEventListener("submit", function (e) {

        const income = document.getElementsByName("ApplicantIncome")[0];

        if (income && income.value <= 0) {

            alert("Applicant Income must be greater than 0");

            e.preventDefault();

        }

    });

}