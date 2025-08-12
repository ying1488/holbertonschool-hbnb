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
    container.innerHTML = ''; // clear old items

    places.forEach(place => {
        const card = document.createElement('div');
        card.classList.add('place-card');
        card.innerHTML = `
            <h3>${place.title}</h3>
            <p>${place.description}</p>
            <p>Price: $${place.price}</p>
        `;
        container.appendChild(card);
    });
}


function setupFilterListener() {
    const filter = document.getElementById('price-filter');
    if (!filter) return;

    filter.addEventListener('change', () => {
        const selectedPrice = filter.value;
        const places = document.querySelectorAll('.place-item');

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

        const rating = document.getElementById('place-rating').value;

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


