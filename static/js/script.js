// Add Turnstile validation
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', async (e) => {
        if (ENABLE_TURNSTILE) {
            e.preventDefault();
            await turnstile.render('#cloudflare-turnstile', {
                sitekey: 'YOUR_SITE_KEY',
                callback: async (token) => {
                    if (token) {
                        // Add the token to the form data
                        const formData = new FormData(form);
                        formData.append('cf-turnstile-response', token);

                        // Submit the form
                        const response = await fetch(form.action, {
                            method: 'POST',
                            body: formData
                        });

                        if (response.ok) {
                            window.location.reload();
                        } else {
                            alert('An error occurred while submitting the form.');
                        }
                    }
                }
            });
        }
    });
});
