const API_BASE = ''; // Relative path since serving from same Flask app

// Elements
const loginView = document.getElementById('login-view');
const registerView = document.getElementById('register-view');
const dashboardView = document.getElementById('dashboard-view');
const navLogin = document.getElementById('nav-login');
const navRegister = document.getElementById('nav-register');
const logoutBtn = document.getElementById('logout-btn');
const toast = document.getElementById('toast');
const statsGraph = document.getElementById('stats-graph');

// View Switching
function showView(viewName) {
    [loginView, registerView, dashboardView].forEach(el => el.classList.remove('active-view'));
    [navLogin, navRegister].forEach(el => el.classList.remove('active'));

    if (viewName === 'login') {
        loginView.classList.add('active-view');
        navLogin.classList.add('active');
        logoutBtn.classList.add('hidden');
    } else if (viewName === 'register') {
        registerView.classList.add('active-view');
        navRegister.classList.add('active');
        logoutBtn.classList.add('hidden');
    } else if (viewName === 'dashboard') {
        dashboardView.classList.add('active-view');
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

navLogin.addEventListener('click', () => showView('login'));
navRegister.addEventListener('click', () => showView('register'));
logoutBtn.addEventListener('click', () => {
    // Simple client-side logout
    navLogin.classList.remove('hidden');
    navRegister.classList.remove('hidden');
    showView('login');
    showToast('Logged out successfully');
});

document.getElementById('refresh-btn').addEventListener('click', loadGraph);

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
        showToast('Login Successful!');
        showView('dashboard');
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
    // Add a timestamp to prevent caching
    statsGraph.src = `/stats/registrations.png?t=${new Date().getTime()}`;
}

// Utilities
function showToast(message) {
    toast.textContent = message;
    toast.classList.remove('hidden');
    setTimeout(() => {
        toast.classList.add('hidden');
    }, 3000);
}
