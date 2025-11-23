// basic client-side helpers for the simple prototype

document.addEventListener('DOMContentLoaded', function () {
  // Example: simple form validation can be added here
  const loginForm = document.getElementById('loginForm');
  if (loginForm) {
    loginForm.addEventListener('submit', function (e) {
      // we rely on required attributes; extra checks here if needed
    });
  }

  const registerForm = document.getElementById('registerForm');
  if (registerForm) {
    registerForm.addEventListener('submit', function (e) {
      // basic password length check
      const pw = registerForm.querySelector('input[name="password"]').value;
      if (pw.length < 4) {
        e.preventDefault();
        alert('Password should be at least 4 characters (for demo).');
      }
    });
  }

  const createForm = document.getElementById('createForm');
  if (createForm) {
    createForm.addEventListener('submit', function (e) {
      // basic date/time presence checks are already required
      // you can add regex checks here if you want
    });
  }
});
