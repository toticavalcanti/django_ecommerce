document.addEventListener("DOMContentLoaded", function() {
    var toastElList = [].slice.call(document.querySelectorAll('.toast'));
    toastElList.map(function(toastEl) {
      return new bootstrap.Toast(toastEl);
    });
  });