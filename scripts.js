/**
 * Portfolio Scripts
 * Main JavaScript file for portfolio website
 */

/**
 * Toggles code section visibility and applies syntax highlighting
 * @param {string} sectionId - The ID of the section to toggle
 */
function toggleCodeSection(sectionId) {
    const section = document.getElementById(sectionId);
    const mainContent = document.querySelector('.main-content');
    
    // Store current scroll position
    const scrollPos = window.scrollY;
    
    if (section.style.display === 'block') {
      section.style.display = 'none';
    } else {
      section.style.display = 'block';
      
      // Explicitly enforce main-content overflow settings
      if (mainContent) {
        mainContent.style.overflowX = 'hidden';
        mainContent.style.maxWidth = '100%';
      }
      
      // Apply syntax highlighting
      if (typeof hljs !== 'undefined') {
        section.querySelectorAll('pre code').forEach((block) => {
          hljs.highlightBlock(block);
        });
      }
    }
    
    // Restore scroll position
    window.scrollTo(0, scrollPos);
  }
  
  /**
   * Changes the active code tab
   * @param {string} panelId - The ID of the panel to display
   * @param {HTMLElement} tabElement - The tab element that was clicked
   */
  function changeCodeTab(panelId, tabElement) {
    // Store current scroll position
    const scrollPos = window.scrollY;
    
    // Get the code content container
    const codeContent = tabElement.closest('.code-content');
    
    // Hide all panels
    const panels = codeContent.getElementsByClassName('code-panel');
    for (let i = 0; i < panels.length; i++) {
      panels[i].classList.remove('active');
    }
    
    // Deactivate all tabs
    const tabs = tabElement.parentElement.getElementsByClassName('code-tab');
    for (let i = 0; i < tabs.length; i++) {
      tabs[i].classList.remove('active');
    }
    
    // Activate selected tab and panel
    document.getElementById(panelId).classList.add('active');
    tabElement.classList.add('active');
    
    // Restore scroll position
    window.scrollTo(0, scrollPos);
  }
  
  /**
   * Toggles math content visibility
   */
  function toggleMath() {
    const mathContent = document.getElementById('mathContent');
    const scrollPos = window.scrollY;
    
    if (mathContent.style.display === 'block') {
      mathContent.style.display = 'none';
    } else {
      mathContent.style.display = 'block';
    }
    
    // Restore scroll position
    window.scrollTo(0, scrollPos);
  }
  
  /**
   * Opens a tab in tabbed content
   * @param {Event} evt - The event object
   * @param {string} tabName - The ID of the tab to open
   */
  function openTab(evt, tabName) {
    // Store current scroll position
    const scrollPos = window.scrollY;
    
    // Hide all tab content
    const tabContent = document.getElementsByClassName("tab-content");
    for (let i = 0; i < tabContent.length; i++) {
      tabContent[i].style.display = "none";
    }
    
    // Remove 'active' class from all tab buttons
    const tabButtons = document.getElementsByClassName("tab-button");
    for (let i = 0; i < tabButtons.length; i++) {
      tabButtons[i].className = tabButtons[i].className.replace(" active", "");
    }
    
    // Show the selected tab and add 'active' class to the button
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
    
    // Restore scroll position
    window.scrollTo(0, scrollPos);
  }
  
  /**
   * Initialize elements on page load
   */
  document.addEventListener('DOMContentLoaded', (event) => {
    // Set code content sections to hidden by default
    const codeSections = document.querySelectorAll('.code-content');
    codeSections.forEach(section => {
      section.style.display = 'none';
    });
    
    // Hide math content by default
    const mathContent = document.getElementById('mathContent');
    if (mathContent) {
      mathContent.style.display = 'none';
    }
    
    // Apply syntax highlighting if available
    if (typeof hljs !== 'undefined') {
      document.querySelectorAll('pre code').forEach((block) => {
        hljs.highlightBlock(block);
      });
    }
    
    // Ensure main content has overflow set
    const mainContent = document.querySelector('.main-content');
    if (mainContent) {
      mainContent.style.overflowX = 'hidden';
      mainContent.style.maxWidth = '100%';
    }
    
    // Set first tab as active in any tab groups
    const tabContainers = document.querySelectorAll('.tab-container');
    tabContainers.forEach(container => {
      // Get the first tab button and content
      const firstTabButton = container.querySelector('.tab-button');
      const firstTabContent = document.querySelector('.tab-content');
      
      if (firstTabButton && firstTabContent) {
        // Add active class to first tab
        firstTabButton.classList.add('active');
        firstTabContent.style.display = 'block';
      }
    });
  });

/**
 * Dashboard Scripts
 * JavaScript functions for dashboard pages
 */

/**
 * Handles iframe loading and shows loading indicator
 */
document.addEventListener('DOMContentLoaded', function() {
    // Handle dashboard iframe loading
    const dashboardIframes = document.querySelectorAll('.dashboard-container iframe');
    
    dashboardIframes.forEach(iframe => {
      // Create loading container if it doesn't exist
      if (!iframe.parentNode.querySelector('.dashboard-loading')) {
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'dashboard-loading';
        
        const spinner = document.createElement('div');
        spinner.className = 'loading-spinner';
        loadingDiv.appendChild(spinner);
        
        const loadingText = document.createElement('p');
        loadingText.textContent = 'Loading dashboard...';
        loadingDiv.appendChild(loadingText);
        
        iframe.parentNode.appendChild(loadingDiv);
      }
      
      // Handle iframe loading
      iframe.addEventListener('load', function() {
        const loadingDiv = this.parentNode.querySelector('.dashboard-loading');
        if (loadingDiv) {
          loadingDiv.style.opacity = '0';
          setTimeout(() => {
            loadingDiv.style.display = 'none';
          }, 300);
        }
      });
      
      // Add error handling
      iframe.addEventListener('error', function() {
        const loadingDiv = this.parentNode.querySelector('.dashboard-loading');
        if (loadingDiv) {
          const loadingText = loadingDiv.querySelector('p');
          if (loadingText) {
            loadingText.textContent = 'Error loading dashboard. Please try again later.';
            loadingText.style.color = '#F44336';
          }
        }
      });
    });
    
    // Handle theme toggle for dashboards
    const themeToggles = document.querySelectorAll('.theme-toggle');
    
    themeToggles.forEach(toggle => {
      toggle.addEventListener('click', function() {
        const toggleSwitch = this.querySelector('.toggle-switch');
        toggleSwitch.classList.toggle('active');
        
        // Get the associated dashboard
        const dashboardId = this.getAttribute('data-dashboard');
        const dashboard = document.getElementById(dashboardId);
        
        if (dashboard) {
          // Toggle dashboard theme
          dashboard.classList.toggle('dark-theme');
          
          // Update toggle label
          const toggleLabel = this.querySelector('.toggle-label');
          if (toggleLabel) {
            toggleLabel.textContent = toggleSwitch.classList.contains('active') 
              ? 'Light Mode' 
              : 'Dark Mode';
          }
          
          // If there's an iframe, reload it with new theme
          const iframe = dashboard.querySelector('iframe');
          if (iframe) {
            // Get current src
            const currentSrc = iframe.src;
            
            // Check if there's a theme parameter
            if (currentSrc.includes('theme=')) {
              // Replace theme parameter
              const newTheme = toggleSwitch.classList.contains('active') ? 'light' : 'dark';
              const newSrc = currentSrc.replace(
                /theme=(dark|light)/i, 
                `theme=${newTheme}`
              );
              iframe.src = newSrc;
            } else {
              // Add theme parameter
              const separator = currentSrc.includes('?') ? '&' : '?';
              const newTheme = toggleSwitch.classList.contains('active') ? 'light' : 'dark';
              iframe.src = `${currentSrc}${separator}theme=${newTheme}`;
            }
          }
        }
      });
    });
    
    // Handle fullscreen button
    const fullscreenButtons = document.querySelectorAll('.fullscreen-button');
    
    fullscreenButtons.forEach(button => {
      button.addEventListener('click', function(e) {
        const dashboardId = this.getAttribute('data-dashboard');
        const dashboard = document.getElementById(dashboardId);
        
        if (!dashboard) return;
        
        const iframe = dashboard.querySelector('iframe');
        if (!iframe) return;
        
        // Open iframe source in new tab
        window.open(iframe.src, '_blank');
        
        // Prevent default link behavior
        e.preventDefault();
      });
    });
    
    // Initialize metric animations
    animateMetricValues();
  });
  
  /**
   * Animates metric values from 0 to their final value
   */
  function animateMetricValues() {
    const metricValues = document.querySelectorAll('.metric-value');
    
    metricValues.forEach(valueElement => {
      // Get the target value
      const finalValue = parseFloat(valueElement.getAttribute('data-value') || valueElement.textContent);
      const prefix = valueElement.getAttribute('data-prefix') || '';
      const suffix = valueElement.getAttribute('data-suffix') || '';
      const decimals = valueElement.getAttribute('data-decimals') || 0;
      
      // Don't animate if not a number
      if (isNaN(finalValue)) return;
      
      // Reset to 0
      valueElement.textContent = prefix + '0' + suffix;
      
      // Determine animation duration based on value size
      const duration = Math.min(2000, Math.max(1000, finalValue * 10));
      const startTime = performance.now();
      
      // Animation function
      function animate(currentTime) {
        // Calculate progress (0 to 1)
        const elapsedTime = currentTime - startTime;
        const progress = Math.min(elapsedTime / duration, 1);
        
        // Apply easing (cubic ease-out)
        const easedProgress = 1 - Math.pow(1 - progress, 3);
        
        // Calculate current value
        const currentValue = easedProgress * finalValue;
        
        // Format value with correct decimals
        const formattedValue = currentValue.toFixed(decimals);
        
        // Update element
        valueElement.textContent = prefix + formattedValue + suffix;
        
        // Continue animation if not finished
        if (progress < 1) {
          requestAnimationFrame(animate);
        }
      }
      
      // Start animation
      requestAnimationFrame(animate);
    });
  }
  
  /**
   * Checks if a dashboard is in the viewport and loads it
   */
  function loadVisibleDashboards() {
    const dashboards = document.querySelectorAll('[data-dashboard-lazy]');
    
    dashboards.forEach(dashboard => {
      // Skip if already loaded
      if (dashboard.hasAttribute('data-loaded')) return;
      
      const rect = dashboard.getBoundingClientRect();
      const isVisible = (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
      );
      
      if (isVisible) {
        // Get iframe URL from data attribute
        const iframeSrc = dashboard.getAttribute('data-dashboard-src');
        if (!iframeSrc) return;
        
        // Create iframe
        const iframe = document.createElement('iframe');
        iframe.src = iframeSrc;
        iframe.title = dashboard.getAttribute('data-title') || "Interactive Dashboard";
        iframe.allowFullscreen = true;
        
        // Clear placeholder if exists
        const placeholder = dashboard.querySelector('.dashboard-placeholder');
        if (placeholder) {
          dashboard.removeChild(placeholder);
        }
        
        // Add iframe to container
        dashboard.appendChild(iframe);
        
        // Mark as loaded
        dashboard.setAttribute('data-loaded', 'true');
        
        // Add loading indicator
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'dashboard-loading';
        
        const spinner = document.createElement('div');
        spinner.className = 'loading-spinner';
        loadingDiv.appendChild(spinner);
        
        const loadingText = document.createElement('p');
        loadingText.textContent = 'Loading dashboard...';
        loadingDiv.appendChild(loadingText);
        
        dashboard.appendChild(loadingDiv);
        
        // Handle iframe loading
        iframe.addEventListener('load', function() {
          loadingDiv.style.opacity = '0';
          setTimeout(() => {
            loadingDiv.style.display = 'none';
          }, 300);
        });
      }
    });
  }
  
  // Listen for scroll events to lazy load dashboards
  window.addEventListener('scroll', function() {
    loadVisibleDashboards();
  });
  
  // Check dashboards on initial load
  document.addEventListener('DOMContentLoaded', function() {
    loadVisibleDashboards();
  });
  
  /**
   * Refreshes a dashboard by reloading its iframe
   * @param {string} dashboardId - The ID of the dashboard container
   */
  function refreshDashboard(dashboardId) {
    const dashboard = document.getElementById(dashboardId);
    if (!dashboard) return;
    
    const iframe = dashboard.querySelector('iframe');
    if (!iframe) return;
    
    // Show loading indicator
    let loadingDiv = dashboard.querySelector('.dashboard-loading');
    
    if (!loadingDiv) {
      loadingDiv = document.createElement('div');
      loadingDiv.className = 'dashboard-loading';
      
      const spinner = document.createElement('div');
      spinner.className = 'loading-spinner';
      loadingDiv.appendChild(spinner);
      
      const loadingText = document.createElement('p');
      loadingText.textContent = 'Refreshing dashboard...';
      loadingDiv.appendChild(loadingText);
      
      dashboard.appendChild(loadingDiv);
    } else {
      loadingDiv.style.display = 'flex';
      loadingDiv.style.opacity = '1';
    }
    
    // Reload iframe
    iframe.src = iframe.src;
    
    // Handle load event
    iframe.addEventListener('load', function loadHandler() {
      loadingDiv.style.opacity = '0';
      setTimeout(() => {
        loadingDiv.style.display = 'none';
      }, 300);
      
      // Remove this specific instance of the event handler
      iframe.removeEventListener('load', loadHandler);
    });
  }