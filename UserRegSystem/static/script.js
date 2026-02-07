const API_BASE = ''; // Relative path since serving from same Flask app

// Elements
const homeView = document.getElementById('home-view');
const loginView = document.getElementById('login-view');
const registerView = document.getElementById('register-view');
const dashboardView = document.getElementById('dashboard-view');
const navHome = document.getElementById('nav-home');
const navLogin = document.getElementById('nav-login');
const navRegister = document.getElementById('nav-register');
const logoutBtn = document.getElementById('logout-btn');
const toast = document.getElementById('toast');
const statsGraph = document.getElementById('stats-graph');
const eventsContainer = document.getElementById('events-container');
const eventStatsGraph = document.getElementById('event-stats-graph');

// User session
let currentUser = null;
let userRegisteredEvents = [];

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Check for saved session
    const savedUser = localStorage.getItem('currentUser');
    if (savedUser) {
        currentUser = JSON.parse(savedUser);
        loadUserRegistrations();
    }
    loadEvents();
    loadEventStatsGraph();
});

// View Switching
function showView(viewName) {
    [homeView, loginView, registerView, dashboardView].forEach(el => el.classList.remove('active-view'));
    [navHome, navLogin, navRegister].forEach(el => el.classList.remove('active'));

    if (viewName === 'home') {
        homeView.classList.add('active-view');
        navHome.classList.add('active');
        navHome.classList.remove('hidden');
        navLogin.classList.remove('hidden');
        navRegister.classList.remove('hidden');
        if (currentUser) {
            navLogin.classList.add('hidden');
            navRegister.classList.add('hidden');
            logoutBtn.classList.remove('hidden');
        } else {
            logoutBtn.classList.add('hidden');
        }
        loadEvents();
        loadEventStatsGraph();
    } else if (viewName === 'login') {
        loginView.classList.add('active-view');
        navLogin.classList.add('active');
        logoutBtn.classList.add('hidden');
    } else if (viewName === 'register') {
        registerView.classList.add('active-view');
        navRegister.classList.add('active');
        logoutBtn.classList.add('hidden');
    } else if (viewName === 'dashboard') {
        dashboardView.classList.add('active-view');
        navHome.classList.remove('hidden');
        navLogin.classList.add('hidden');
        navRegister.classList.add('hidden');
        logoutBtn.classList.remove('hidden');
        loadGraph();
    }
}

// Event Listeners for Navigation
document.getElementById('goto-register').addEventListener('click', (e) => {
    e.preventDefault();
    showView('register');
});

document.getElementById('goto-login').addEventListener('click', (e) => {
    e.preventDefault();
    showView('login');
});

navHome.addEventListener('click', () => showView('home'));
navLogin.addEventListener('click', () => showView('login'));
navRegister.addEventListener('click', () => showView('register'));
logoutBtn.addEventListener('click', () => {
    currentUser = null;
    userRegisteredEvents = [];
    localStorage.removeItem('currentUser');
    navLogin.classList.remove('hidden');
    navRegister.classList.remove('hidden');
    showView('home');
    showToast('Logged out successfully');
});

document.getElementById('refresh-btn').addEventListener('click', loadGraph);
document.getElementById('refresh-event-stats').addEventListener('click', loadEventStatsGraph);

// API Interactions
async function handleAuth(endpoint, formData) {
    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
        const data = await response.json();

        if (response.ok) {
            return { success: true, data };
        } else {
            return { success: false, message: data.message };
        }
    } catch (error) {
        return { success: false, message: 'Network error occurred' };
    }
}

// Forms
document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;

    const result = await handleAuth('/login', { username, password });

    if (result.success) {
        currentUser = { id: result.data.user_id, username };
        localStorage.setItem('currentUser', JSON.stringify(currentUser));
        await loadUserRegistrations();
        showToast('Login Successful!');
        showView('home');
    } else {
        showToast(result.message || 'Login Failed');
    }
});

document.getElementById('register-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('reg-username').value;
    const password = document.getElementById('reg-password').value;

    const result = await handleAuth('/register', { username, password });

    if (result.success) {
        showToast('Registration Successful! Please Login.');
        showView('login');
    } else {
        showToast(result.message || 'Registration Failed');
    }
});

// Graph Loading
function loadGraph() {
    statsGraph.src = `/stats/registrations.png?t=${new Date().getTime()}`;
}

function loadEventStatsGraph() {
    eventStatsGraph.src = `/stats/event_registrations.png?t=${new Date().getTime()}`;
}

// Load user's registered events
async function loadUserRegistrations() {
    if (!currentUser) return;

    try {
        const response = await fetch(`/api/user/${currentUser.id}/registrations`);
        const data = await response.json();
        if (data.success) {
            userRegisteredEvents = data.event_ids;
        }
    } catch (error) {
        console.error('Failed to load user registrations:', error);
    }
}

// Events Loading and Display
async function loadEvents() {
    try {
        const response = await fetch('/api/events');
        const data = await response.json();

        if (data.success) {
            renderEvents(data.events);
        } else {
            eventsContainer.innerHTML = '<p class="error">Failed to load events</p>';
        }
    } catch (error) {
        eventsContainer.innerHTML = '<p class="error">Failed to load events</p>';
        console.error('Error loading events:', error);
    }
}

function renderEvents(events) {
    if (events.length === 0) {
        eventsContainer.innerHTML = '<p>No events available</p>';
        return;
    }

    eventsContainer.innerHTML = events.map((event, index) => {
        const isRegistered = userRegisteredEvents.includes(event.id);
        const formattedDate = formatDate(event.event_date);

        return `
            <div class="event-card" data-event-id="${event.id}">
                <div class="event-card-inner">
                    <div class="event-image-wrapper">
                        <img src="${event.image_url || getPlaceholderImage(index)}" alt="${event.name}" onerror="this.src='${getPlaceholderImage(index)}'">
                        <div class="event-image-overlay"></div>
                    </div>
                    <div class="event-content">
                        <div>
                            <h3 class="event-name">${event.name}</h3>
                            <p class="event-date">${formattedDate}</p>
                            <p class="event-description">${event.description || 'Join us for an amazing event!'}</p>
                        </div>
                        <div class="event-footer">
                            <div class="event-registrations">
                                <span>${event.registration_count}</span> registered
                            </div>
                            <button 
                                class="register-btn ${isRegistered ? 'registered' : ''}" 
                                onclick="toggleEventRegistration(${event.id}, event)"
                                ${isRegistered ? 'data-registered="true"' : ''}
                            >
                                ${isRegistered ? '✓ Registered' : 'Register'}
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }).join('');
}

function getPlaceholderImage(index) {
    const colors = ['39ff14', '03dac6', '9945FF'];
    const texts = ['TECH', 'CULTURE', 'SPORTS'];
    return `https://via.placeholder.com/400x300/${colors[index % 3]}/000000?text=${texts[index % 3]}`;
}

function formatDate(dateString) {
    if (!dateString) return 'Date TBD';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

// Event Registration Toggle
async function toggleEventRegistration(eventId, e) {
    e.stopPropagation();

    if (!currentUser) {
        showToast('Please login to register for events');
        showView('login');
        return;
    }

    const btn = e.target;
    const isRegistered = btn.dataset.registered === 'true';
    const endpoint = isRegistered ? '/api/events/unregister' : '/api/events/register';

    btn.disabled = true;

    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: currentUser.id, event_id: eventId })
        });
        const data = await response.json();

        if (data.success) {
            if (isRegistered) {
                userRegisteredEvents = userRegisteredEvents.filter(id => id !== eventId);
                showToast('Unregistered from event');
            } else {
                userRegisteredEvents.push(eventId);
                showToast('Registered successfully!');
            }
            loadEvents();
            loadEventStatsGraph();
        } else {
            showToast(data.message || 'Operation failed');
        }
    } catch (error) {
        showToast('Network error occurred');
        console.error('Registration error:', error);
    } finally {
        btn.disabled = false;
    }
}

// Utilities
function showToast(message) {
    toast.textContent = message;
    toast.classList.remove('hidden');
    setTimeout(() => {
        toast.classList.add('hidden');
    }, 3000);
}
