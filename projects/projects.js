
  // Fixed toggle section functionality
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

  // Initialize on page load
  document.addEventListener('DOMContentLoaded', (event) => {
    // Set code content sections to hidden by default
    const codeSections = document.querySelectorAll('.code-content');
    codeSections.forEach(section => {
      section.style.display = 'none';
    });
    
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
  });
