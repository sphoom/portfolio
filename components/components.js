// Function to load HTML components
function loadComponent(url, elementId) {
    fetch(url)
      .then(response => response.text())
      .then(data => {
        document.getElementById(elementId).innerHTML = data;
      })
      .catch(error => console.error('Error loading component:', error));
  }
  
  document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('header-placeholder')) {
      loadComponent('components/header.html', 'header-placeholder');
    }
    
    if (document.getElementById('footer-placeholder')) {
      loadComponent('components/footer.html', 'footer-placeholder');
    }
  });