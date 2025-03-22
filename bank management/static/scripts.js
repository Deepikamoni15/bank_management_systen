document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.querySelector("form");

    if (loginForm) {
        loginForm.addEventListener("submit", function (event) {
            let username = document.querySelector("input[name='username']").value.trim();
            let password = document.querySelector("input[name='password']").value.trim();

            if (username === "" || password === "") {
                alert("Username and password cannot be empty!");
                event.preventDefault();
            }
        });
    }

    const depositForm = document.querySelector("form[action*='deposit']");
    const withdrawForm = document.querySelector("form[action*='withdraw']");

    if (depositForm) {
        depositForm.addEventListener("submit", function (event) {
            let amount = parseFloat(document.querySelector("input[name='amount']").value);
            if (isNaN(amount) || amount <= 0) {
                alert("Please enter a valid deposit amount.");
                event.preventDefault();
            }
        });
    }

    if (withdrawForm) {
        withdrawForm.addEventListener("submit", function (event) {
            let amount = parseFloat(document.querySelector("input[name='amount']").value);
            if (isNaN(amount) || amount <= 0) {
                alert("Please enter a valid withdrawal amount.");
                event.preventDefault();
            }
        });
    }
});
