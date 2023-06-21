
// Code below for checking if username already exist 
 document.addEventListener('DOMContentLoaded', () => {
 const usernameInput = document.getElementById('username');
 const availabilitySpan = document.getElementById('username-availability');

 usernameInput.addEventListener('input', () => {
     const username = usernameInput.value.trim();
     if (username) {
     checkUsernameAvailability(username);
     } else {
     availabilitySpan.textContent = '';
     }
 });

 function checkUsernameAvailability(username) {
     fetch(`/check_username_availability/?username=${encodeURIComponent(username)}`)
     .then((response) => response.json())
     .then((data) => {
         availabilitySpan.textContent = data.message;
         availabilitySpan.style.color = data.available ? 'green' : 'red';
     })
     .catch((error) => {
         console.error('Error:', error);
     });
 }
 });
