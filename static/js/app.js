<<<<<<< HEAD
document.addEventListener(
    "DOMContentLoaded",
    () => {

        const form =
            document.querySelector(
                "form[action='/generate']"
            );


        if (!form) {

            return;

        }


        form.addEventListener(
            "submit",
            () => {

                const button =
                    form.querySelector(
                        "button[type='submit']"
                    );


                if (button) {

                    button.disabled = true;

                    button.textContent =
                        "Creating your comic...";

                }

            }
        );

    }
=======
document.addEventListener(
    "DOMContentLoaded",
    () => {

        const form =
            document.querySelector(
                "form[action='/generate']"
            );


        if (!form) {

            return;

        }


        form.addEventListener(
            "submit",
            () => {

                const button =
                    form.querySelector(
                        "button[type='submit']"
                    );


                if (button) {

                    button.disabled = true;

                    button.textContent =
                        "Creating your comic...";

                }

            }
        );

    }
>>>>>>> 4259a77dbb679077cc99e1d64f91f77e46761268
);