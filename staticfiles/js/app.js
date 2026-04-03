/**
 * Sarello ERP - Main App Entry Point
 * Initializes all modules and event listeners
 */

document.addEventListener('DOMContentLoaded', function() {
  console.log('Sarello ERP initialized');

  // Module initialization can be added here
  // Example: initForms();
  //         initTables();
  //         if (document.body.dataset.module === 'accounting') {
  //           initAccounting();
  //         }

  // HTMX configuration
  if (typeof htmx !== 'undefined') {
    htmx.config.historyCacheSize = 0;
    htmx.config.refreshOnHistoryMiss = true;
  }

  // Global error handling
  window.addEventListener('error', function(event) {
    console.error('Global error:', event.error);
  });

  // Handle unhandled promise rejections
  window.addEventListener('unhandledrejection', function(event) {
    console.error('Unhandled promise rejection:', event.reason);
  });
});

/**
 * Utility function for API calls
 */
async function apiCall(url, options = {}) {
  const defaultOptions = {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'X-Requested-With': 'XMLHttpRequest',
    },
  };

  // Add CSRF token if POST/PUT/DELETE
  if (['POST', 'PUT', 'DELETE', 'PATCH'].includes(defaultOptions.method)) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value ||
                      document.cookie.split('; ').find(row => row.startsWith('csrftoken='))?.split('=')[1];
    if (csrfToken) {
      defaultOptions.headers['X-CSRFToken'] = csrfToken;
    }
  }

  try {
    const response = await fetch(url, { ...defaultOptions, ...options });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('API call error:', error);
    throw error;
  }
}

/**
 * Utility function to show notifications
 */
function notify(message, type = 'info') {
  const alertClass = `alert-${type}`;
  const alert = document.createElement('div');
  alert.className = `alert ${alertClass} dismissible`;
  alert.innerHTML = `
    <span class="alert-content">
      <span class="alert-title">${type.toUpperCase()}</span>
      <span class="alert-message">${message}</span>
    </span>
    <button class="alert-close" onclick="this.parentElement.remove()">×</button>
  `;

  const container = document.querySelector('.alert-container') || document.body;
  container.insertBefore(alert, container.firstChild);

  // Auto-remove after 5 seconds
  setTimeout(() => alert.remove(), 5000);
}

/**
 * Utility function to debounce functions
 */
function debounce(func, delay) {
  let timeoutId;
  return function(...args) {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => func.apply(this, args), delay);
  };
}

/**
 * Utility function to throttle functions
 */
function throttle(func, limit) {
  let inThrottle;
  return function(...args) {
    if (!inThrottle) {
      func.apply(this, args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
}

/**
 * Format currency (Argentine Peso)
 */
function formatCurrency(value) {
  return new Intl.NumberFormat('es-AR', {
    style: 'currency',
    currency: 'ARS',
  }).format(value);
}

/**
 * Format number with locale
 */
function formatNumber(value, decimals = 2) {
  return new Intl.NumberFormat('es-AR', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  }).format(value);
}

/**
 * Parse currency from string
 */
function parseCurrency(str) {
  return parseFloat(str.replace(/[^\d,-]/g, '').replace(',', '.'));
}

// Export functions for use in other modules
window.Sarello = {
  apiCall,
  notify,
  debounce,
  throttle,
  formatCurrency,
  formatNumber,
  parseCurrency,
};
