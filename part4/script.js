console.log('script loaded')

document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM loaded');
    loginUser();
    checkAuthentication();
    setupFilterListener();
    getPlaces();
    populatePlaceDropdown();
    setupReviewForm();
    setupLogout();
    loadPlaceDetails();
});

function loginUser() {
    const loginForm = document.getElementById('login-form');

    if (!loginForm) return;

    loginForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        
        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value.trim();

        // Test bypass
        if (email === 'test@test' && password === 'test') {
            setCookie('token', 'fake_test_token', 1);
            window.location.href = 'index.html';
            return;
        }

        // Real login
        try {
            const response = await fetch('http://127.0.0.1:5000/api/v1/users/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'include',
                body: JSON.stringify({ email, password })
            });

            if (response.ok) {
                const data = await response.json();
                
                if (data.token) setCookie('token', data.token, 1);
                if (data.user_id) setCookie('user_id', data.user_id, 1);
                else console.error('user_id missing from login response');

                
                console.log('User ID from cookie:', data.user_id);
                //debugger;

                window.location.href = 'index.html';
            } else {
                alert('Login failed: ' + response.statusText);
            }
        } catch (error) {
            console.error(error);
            alert('An error occurred.');
        }
    });
}

function setCookie(name, value, days) {
    let expires = "";
    if (days) {
        const date = new Date();
        date.setTime(date.getTime() + (days*24*60*60*1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + value + expires + "; path=/";
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

function checkAuthentication() {
    const loginLink = document.getElementById('login-link');
    const logoutBtn = document.getElementById('logout-btn');
    const token = getCookie('token');
    const isLoggedIn = !!token;

    if (loginLink) {
        loginLink.style.display = isLoggedIn ? 'none' : 'block';
    }
    if (logoutBtn) {
        logoutBtn.style.display = isLoggedIn ? 'block' : 'none';
    }
}



function setupLogout() {
    const logoutBtn = document.getElementById('logout-btn');
    if (!logoutBtn) return;

    logoutBtn.addEventListener('click', () => {
        setCookie('token', '', -1); // delete token
        setCookie('user_id', '', -1); // delete user id
        window.location.href = '/login.html';
    });
}

async function getPlaces() {
    const token = getCookie('token');
    if (!token) return;

    try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/places', {
            method: 'GET',
            headers: { 'Authorization': `Bearer ${token}` },
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
  const container = document.getElementById('places-list');
  container.innerHTML = '';

  places.forEach(place => {
    const link = document.createElement('a');
    link.href = `place.html?id=${place.id}`;
    link.className = 'place-card block p-4 border rounded hover:bg-gray-100 transition';
    link.dataset.price = place.price;

    link.innerHTML = `
      <h3 class="text-xl font-semibold">${place.title}</h3>
      <p class="text-sm text-gray-600">$${place.price}</p>
    `;

    container.appendChild(link);
  });
}



function setupFilterListener() {
    const filter = document.getElementById('price-filter');
    if (!filter) return;

    filter.addEventListener('change', () => {
        const selectedPrice = filter.value;
        const places = document.querySelectorAll('.place-card');

        places.forEach(place => {
            const price = parseFloat(place.dataset.price);
            place.style.display = (selectedPrice === 'all' || price <= parseFloat(selectedPrice)) ? 'block' : 'none';
        });
    });
}

function setupReviewForm() {
    const reviewForm = document.getElementById('review-form');
    if (!reviewForm) return;

    const reviewsList = document.getElementById('reviews-list');
    const token = getCookie('token');
    const userId = getCookie('user_id');
    console.log('User ID from cookie:', userId);

    console.log('Review form element:', reviewForm);


    reviewForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        console.log('Review form submitted');

        const reviewText = document.getElementById('text').value.trim();
        const placeSelect = document.getElementById('place-select');
        const placeId = placeSelect ? placeSelect.value : null;

        const rating = document.getValueById('place-rating');

        if (!reviewText) {
            alert('Please write a review before submitting.');
            return;
        }

        try {
            const response = await fetch('http://127.0.0.1:5000/api/v1/reviews', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                credentials: 'include',
                body: JSON.stringify({
                    text: reviewText,
                    user_id: userId, 
                    rating: rating,
                    place_id: placeId
                })
            });

            if (response.ok) {
                const newReviewEl = document.createElement('div');
                newReviewEl.className = 'p-4 border border-gray-300 rounded-md';
                newReviewEl.textContent = `${reviewText} (⭐ ${rating})`;
                reviewsList.appendChild(newReviewEl);
                reviewForm.reset();
            } else {
                const errData = await response.json();
                alert('Failed to submit review: ' + (errData.error || 'Unknown error'));
            }
        } catch (error) {
            console.error('Error submitting review:', error);
            alert('An error occurred. Please try again later.');
        }
    });
}

async function populatePlaceDropdown() {
    const token = getCookie('token'); // make sure you have this function
    if (!token) {
        console.error("No token found. Cannot load places.");
        return;
    }

    try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/places', {
            method: 'GET',
            headers: { 'Authorization': `Bearer ${token}` },
            credentials: 'include'
        });

        if (!response.ok) {
            console.error('Failed to fetch places:', response.status, response.statusText);
            return;
        }

        const places = await response.json();

        const select = document.getElementById('place-select');
        if (!select) {
            console.error("place-select element not found");
            return;
        }

        // Clear and add default placeholder
        select.innerHTML = '<option value="" disabled selected>Select a place</option>';

        // Populate dropdown
        places.forEach(place => {
            const option = document.createElement('option');
            option.value = place.id;        // This will be the value sent on form submit
            option.textContent = place.title; // This is what the user sees
            select.appendChild(option);
        });

    } catch (error) {
        console.error('Error fetching places:', error);
    }
}


async function loadPlaceDetails() {
    const params = new URLSearchParams(window.location.search);
    const placeId = params.get('id');
    if (!placeId) return; // no id in URL, nothing to load

    const token = getCookie('token');
    if (!token) {
        console.error("No token found. Cannot load place details.");
        return;
    }

    try {
        const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, {
            method: 'GET',
            headers: { 'Authorization': `Bearer ${token}` },
            credentials: 'include'
        });

        if (!response.ok) {
            console.error('Failed to fetch place:', response.status, response.statusText);
            return;
        }

        const place = await response.json();

        // ill in the details dynaFmically
        const detailsSection = document.getElementById('place-details');
        detailsSection.innerHTML = `
          <div class="grid grid-cols-1 md:grid-cols-2 gap-8 items-start">
            <div class="rounded-lg overflow-hidden">
              <img src="${place.image_url || 'img/placeholder.jpg'}" 
                   alt="${place.title}" 
                   class="w-full h-full object-cover">
            </div>
            <div class="flex flex-col gap-6">
              <div>
                <h2 class="text-4xl font-normal mb-6">${place.title}</h2>
                <div class="space-y-4">
                  <div>
                    <h3 class="uppercase tracking-widest text-sm text-gray-600">Host</h3>
                    <p class="text-lg">${place.host || 'Unknown'}</p>
                  </div>
                  <div>
                    <h3 class="uppercase tracking-widest text-sm text-gray-600">Description</h3>
                    <p class="text-lg">${place.description || 'No description provided.'}</p>
                  </div>
                  <div>
                    <h3 class="uppercase tracking-widest text-sm text-gray-600">Price</h3>
                    <p class="text-lg">$${place.price}/night</p>
                  </div>
                  <div>
                    <h3 class="uppercase tracking-widest text-sm text-gray-600">Amenities</h3>
                    <ul class="list-disc list-inside text-lg">
                      ${(place.amenities || []).map(a => `<li>${a}</li>`).join('')}
                    </ul>
                  </div>
                  <div>
                    <h3 class="uppercase tracking-widest text-sm text-gray-600">Lat, Long</h3>
                    <p class="text-lg">${place.latitude}, ${place.longitude}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        `;
    } catch (error) {
        console.error('Error fetching place details:', error);
    }
}
