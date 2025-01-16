$(document).ready(function () {
    // Contact Form Handler
    const contactForm = $(".contact-form");
    const contactFormMethod = contactForm.attr("method");
    const contactFormEndpoint = contactForm.attr("action");

    function displaySubmitting(submitBtn, defaultText, doSubmit) {
        if (doSubmit) {
            submitBtn.addClass("disabled");
            submitBtn.html("<i class='fa fa-spin fa-spinner'></i> Enviando...");
        } else {
            submitBtn.removeClass("disabled");
            submitBtn.html(defaultText);
        }
    }

    contactForm.submit(function (event) {
        event.preventDefault();
        const contactFormSubmitBtn = contactForm.find("[type='submit']");
        const contactFormSubmitBtnTxt = contactFormSubmitBtn.text();
        const contactFormData = contactForm.serialize();

        displaySubmitting(contactFormSubmitBtn, "", true);

        $.ajax({
            method: contactFormMethod,
            url: contactFormEndpoint,
            data: contactFormData,
            success: function (data) {
                contactForm[0].reset();
                $.alert({
                    title: "Success!",
                    content: data.message,
                    theme: "modern",
                });
                setTimeout(function () {
                    displaySubmitting(
                        contactFormSubmitBtn,
                        contactFormSubmitBtnTxt,
                        false
                    );
                }, 500);
            },
            error: function (error) {
                const jsonData = error.responseJSON;
                let msg = "";
                $.each(jsonData, function (key, value) {
                    msg += `${key}: ${value[0].message}<br/>`;
                });
                $.alert({
                    title: "Oops!",
                    content: msg,
                    theme: "modern",
                });
                setTimeout(function () {
                    displaySubmitting(
                        contactFormSubmitBtn,
                        contactFormSubmitBtnTxt,
                        false
                    );
                }, 500);
            },
        });
    });
});