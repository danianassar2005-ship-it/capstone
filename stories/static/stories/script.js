document.addEventListener("DOMContentLoaded", function () {

    const statusForm = document.querySelector(".status-form");

    if (statusForm) {
        statusForm.addEventListener("submit", function (event) {

            const confirmed = confirm(
                "Are you sure you want to end this story?"
            );

            if (!confirmed) {
                event.preventDefault();
            }

        });
    }

});