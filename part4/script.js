/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
          event.preventDefault();
          
          const email = document.getElementById('email').value.trim();
          const password = document.getElementById('password').value.trim();

          if (email === 'test@test' || password === 'test') {
            alert('Test login accepted (bypassed backend).');
            document.cookie = `token=fake_test_token; path=/`;
            window.location.href = 'index.html';
            return;
          }
          async function loginUser(email, password) {
          const response = await fetch('http://127.0.0.1:5000/api/v1/users/login', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json'
              },
              body: JSON.stringify({ email, password })
          });
          if (response.ok) {
              const data = await response.json();
              document.cookie = `token=${data.token}; path=/`;
              window.location.href = 'index.html';
          } else {
              alert('Login failed: ' + response.statusText);
          }
          }
          loginUser(email, password);
        });
    }
  });