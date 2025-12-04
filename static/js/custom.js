// Example JavaScript for interactivity or client-side validation

document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form.needs-validation');
    Array.prototype.slice.call(forms)
      .forEach(function(form) {
        form.addEventListener('submit', function(event) {
          if (!form.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
            alert('Please fill in all required fields!');
          }
          form.classList.add('was-validated');
        }, false);
    });
});
