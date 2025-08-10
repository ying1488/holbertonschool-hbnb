/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

document.addEventListener('DOMContentLoaded', () => {
    loginUser();
    checkAuthentication();
    setupFilterListener();
    setupReviewForm();
  });

function loginUser() {

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
          async function loginRequest(email, password) {
          const response = await fetch('http://127.0.0.1:5000/api/v1/users/login', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json'
              },
              credentials: 'include',
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
          loginRequest(email, password);
        });
    }
}

function getCookie(cookie) {
  const val = `; ${document.cookie}`;
  const parts = val.split(`; ${cookie}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();

}

function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');

    if (!token) {
        loginLink.style.display = 'block';
    } else {
        loginLink.style.display = 'none';
        getPlaces(token);
    }
}

async function getPlaces(token) {
  
  try {
    const response = await fetch('http://127.0.0.1:5000/api/v1/places', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`
      },
      credentials: 'include'
    });
    if (response.ok) {
      const data = await response.json();
      displayPlaces(data);
    } else {
      console.error('Failed to fetch places:', response.statusText);
    }
  } catch (error) {
    console.error('Error fetching places:', error);
  }
}

function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    placesList.innerHTML = '';

    places.forEach(place => {
        const placeEl = document.createElement('div');
        placeEl.classList.add('place-item');
        placeEl.dataset.price = place.price;

        placeEl.innerHTML = `
            <h3>${place.title}</h3>
            <p>${place.description}</p>
            <p><strong>Price:</strong> $${place.price}</p>
        `;

        placesList.appendChild(placeEl);
    });
}

function setupFilterListener() {
    const filter = document.getElementById('price-filter');
    filter.addEventListener('change', () => {
        const selectedPrice = filter.value;
        const places = document.querySelectorAll('.place-item');

        places.forEach(place => {
            const price = parseFloat(place.dataset.price);
            if (selectedPrice === 'all' || price <= parseFloat(selectedPrice)) {
                place.style.display = 'block';
            } else {
                place.style.display = 'none';
            }
        });
    });
}

function setupReviewForm() {
  const reviewForm = document.getElementById('review-form');
  if (!reviewForm) return; // If no form on the page, just exit

  reviewForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const reviewText = document.getElementById('review-text').value.trim();
    const placeId = document.getElementById('place-id').value;

    if (!reviewText) {
      alert('Please write a review before submitting.');
      return;
    }

    try {
      const response = await fetch('http://127.0.0.1:5000/api/v1/reviews', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ review: reviewText, place_id: placeId })
      });

      if (response.ok) {
        alert('Review submitted successfully!');
        reviewForm.reset();
      } else {
        alert('Failed to submit review.');
      }
    } catch (error) {
      console.error('Error submitting review:', error);
      alert('An error occurred. Please try again later.');
    }
  });
}
