
    const hamburger = document.querySelector(".hamburger");
    const navMenu = document.querySelector(".nav-menu");

    hamburger.addEventListener("click", () => {
        hamburger.classList.toggle("active");
        navMenu.classList.toggle("active");
    });


    function showAuthModal() {
    document.getElementById('authModal').style.display = 'block';
}

function closeAuthModal() {
    document.getElementById('authModal').style.display = 'none';
}
document.addEventListener('DOMContentLoaded', function () {
  const showLogin = document.getElementById('showLoginFlag').value;
  if (showLogin === 'true') {
    showAuthModal();
    showLogin();
  }
});

function showLogin() {
    document.getElementById('loginForm').classList.add('active');
    document.getElementById('signupForm').classList.remove('active');
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
}

function showSignup() {
    document.getElementById('signupForm').classList.add('active');
    document.getElementById('loginForm').classList.remove('active');
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
}


function checkAuthStatus() {
    const savedUser = localStorage.getItem('currentUser');
    if (savedUser) {
        currentUser = JSON.parse(savedUser);
        updateUIForLoggedInUser();
    }
}

function updateUIForLoggedInUser() {
    const loginBtn = document.querySelector('.login-btn');
    if (loginBtn && currentUser) {
        loginBtn.textContent = `${currentUser.name} (${currentUser.role})`;
        loginBtn.onclick = logout;
    }
}

function logout() {
    currentUser = null;
    localStorage.removeItem('currentUser');
    const loginBtn = document.querySelector('.login-btn');
    if (loginBtn) {
        loginBtn.textContent = 'Login';
        loginBtn.onclick = showAuthModal;
    }
    showNotification('Logged out successfully!', 'success');
    // Redirect to home if on dashboard
    if (window.location.pathname.includes('dashboard')) {
        window.location.href = 'index.html';
    }
}

function redirectToDashboard() {
    if (currentUser) {
        switch (currentUser.role) {
            case 'customer':
                window.location.href = 'customer-dashboard.html';
                break;
            case 'admin':
                window.location.href = 'admin-dashboard.html';
                break;
            case 'worker':
                window.location.href = 'worker-dashboard.html';
                break;
        }
    }
}



// Fetch from backend
fetch('/api/menu-items/')
  .then(response => response.json())
  .then(data => {
    isLoggedIn = data.is_logged_in;
    menuItems = data.items;
    renderMenuItems(menuItems);
    renderMenuPagination(menuItems);
  });

// carousel

  const slides = document.querySelectorAll('.slide');
  const dots = document.querySelectorAll('.dot');
  let currentIndex = 0;

 function showSlide(index) {
  const slidesContainer = document.querySelector('.slides');
  const slideWidth = slides[0].clientWidth;
  slidesContainer.style.transform = `translateX(-${index * slideWidth}px)`;

  // Update dots
  dots.forEach((dot, i) => {
    dot.classList.toggle('active', i === index);
  });
}

  document.getElementById('next').addEventListener('click', () => {
    currentIndex = (currentIndex + 1) % slides.length;
    showSlide(currentIndex);
  });

  document.getElementById('prev').addEventListener('click', () => {
    currentIndex = (currentIndex - 1 + slides.length) % slides.length;
    showSlide(currentIndex);
  });

  dots.forEach((dot, i) => {
    dot.addEventListener('click', () => {
      currentIndex = i;
      showSlide(currentIndex);
    });
  });

  // Optional: Auto-slide
  setInterval(() => {
    currentIndex = (currentIndex + 1) % slides.length;
    showSlide(currentIndex);
  }, 8000);

