// 🔐 Get CSRF token
const getCookie = name => {
  const cookies = document.cookie.split(';').map(c => c.trim());
  const match = cookies.find(c => c.startsWith(name + '='));
  return match ? decodeURIComponent(match.split('=')[1]) : null;
};

// 🏨 Room Data
let roomItems = [];

document.addEventListener('DOMContentLoaded', () => {
  fetch('/rooms/api/rooms/')
    .then(response => response.json())
    .then(data => {
      roomItems = data;
      renderRoomItems(roomItems);
      renderRoomPagination(roomItems);
    })
    .catch(error => {
      console.error('Error fetching room data:', error);
    });
});

// 🔧 DOM Elements
const roomContainer = document.getElementById('booking-container');
const roomPagination = document.getElementById('room-pagination');
const roomCategoryButtons = document.querySelectorAll('.room-category');
const roomSearchInput = document.getElementById('roomSearchInput');

let roomPage = 1;
const roomItemsPerPage = 6;
let roomCurrentCategory = 'all';

// 🖼️ Render Rooms
const renderRoomItems = items => {
  const start = (roomPage - 1) * roomItemsPerPage;
  const paginated = items.slice(start, start + roomItemsPerPage);
  roomContainer.innerHTML = paginated.map(item => `
    <div class="menu-item ${item.category}">
      <img src="${item.img}" alt="${item.name}">
      <h3>${item.name}</h3>
      <p>${item.desc}</p>
      <div class="price">${item.price}</div>
      <button class="order-btn" onclick='openBookingModal(${JSON.stringify(item)})'>Book Now</button>
    </div>
  `).join('');
};

// 🔢 Render Pagination
const renderRoomPagination = items => {
  const pageCount = Math.ceil(items.length / roomItemsPerPage);
  let buttons = [];

  if (roomPage > 1) buttons.push(`<button onclick="goToRoomPage(${roomPage - 1})">&lt;</button>`);
  for (let i = 1; i <= pageCount; i++) {
    buttons.push(`<button class="${i === roomPage ? 'active' : ''}" onclick="goToRoomPage(${i})">${i}</button>`);
  }
  if (roomPage < pageCount) buttons.push(`<button onclick="goToRoomPage(${roomPage + 1})">&gt;</button>`);

  roomPagination.innerHTML = buttons.join('');
};

// 🔍 Filter Rooms
const filterRooms = (category, search = '') => {
  return roomItems.filter(item => {
    const matchCategory = category === 'all' || item.category === category;
    const matchSearch = item.name.toLowerCase().includes(search.toLowerCase()) || item.desc.toLowerCase().includes(search.toLowerCase());
    return matchCategory && matchSearch;
  });
};

// 🔄 Page Navigation
window.goToRoomPage = page => {
  roomPage = page;
  const filtered = filterRooms(roomCurrentCategory, roomSearchInput.value);
  renderRoomItems(filtered);
  renderRoomPagination(filtered);
};

// 🧭 Category Filter
roomCategoryButtons.forEach(button => {
  button.addEventListener('click', () => {
    roomCategoryButtons.forEach(btn => btn.classList.remove('active'));
    button.classList.add('active');
    roomCurrentCategory = button.dataset.filter;
    roomPage = 1;
    const filtered = filterRooms(roomCurrentCategory, roomSearchInput.value);
    renderRoomItems(filtered);
    renderRoomPagination(filtered);
  });
});

// 🔎 Search Filter
roomSearchInput.addEventListener('input', () => {
  roomPage = 1;
  const filtered = filterRooms(roomCurrentCategory, roomSearchInput.value);
  renderRoomItems(filtered);
  renderRoomPagination(filtered);
});

// 📦 Booking Modal
const modal = {
  roomName: document.getElementById('modalRoomName'),
  roomImage: document.getElementById('modalRoomImage'),
  roomDesc: document.getElementById('modalRoomDesc'),
  roomPrice: document.getElementById('modalRoomPrice'),
  arrival: document.getElementById('arrivalDate'),
  departure: document.getElementById('departureDate'),
  guests: document.getElementById('numGuests'),
  terms: document.getElementById('termsCheckbox'),
  modalBox: document.getElementById('bookingModal')
};

function openBookingModal(room) {
  modal.roomName.textContent = room.name;
  modal.roomImage.src = room.img;
  modal.roomDesc.textContent = room.desc;
  modal.roomPrice.textContent = room.price;
  modal.arrival.value = '';
  modal.departure.value = '';
  modal.guests.value = 1;
  modal.terms.checked = false;
  modal.modalBox.style.display = 'block';
}

function closeBookingModal() {
  modal.modalBox.style.display = 'none';
}

// ✅ Confirm Booking
function confirmBooking() {
  const arrival = modal.arrival.value;
  const departure = modal.departure.value;
  const guests = parseInt(modal.guests.value);
  const agreed = modal.terms.checked;
  const roomName = modal.roomName.textContent;

  // ✅ Basic validation
  if (!arrival || !departure || guests < 1 || !agreed) {
    alert('Please fill all fields and accept terms.');
    return;
  }

  if (new Date(arrival) >= new Date(departure)) {
    alert('Departure date must be after arrival date.');
    return;
  }

  const bookingData = {
    roomName,
    arrivalDate: arrival,
    departureDate: departure,
    guests
  };

  fetch('/rooms/api/book/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify(bookingData)
  })
  .then(res => res.json())
  .then(data => {
    alert(data.message || data.error || 'Booking failed.');
    if (data.message) closeBookingModal();
  })
  .catch(err => {
    console.error('Error:', err);
    alert('Something went wrong.');
  });
}

// 🧹 Optional: Close modal on outside click or ESC
window.addEventListener('keydown', e => {
  if (e.key === 'Escape') closeBookingModal();
});

