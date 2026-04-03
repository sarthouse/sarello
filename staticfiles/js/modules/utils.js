/**
 * Shared Utilities Module
 * Common helper functions used across the application
 */

/**
 * Dispatch a custom event
 */
function dispatchEvent(eventName, detail = {}) {
  const event = new CustomEvent(eventName, { detail });
  document.dispatchEvent(event);
}

/**
 * Create element with class and content
 */
function createElement(tag, className = '', innerHTML = '') {
  const el = document.createElement(tag);
  if (className) el.className = className;
  if (innerHTML) el.innerHTML = innerHTML;
  return el;
}

/**
 * Check if element exists and is visible
 */
function isElementVisible(selector) {
  const el = document.querySelector(selector);
  if (!el) return false;
  return el.offsetParent !== null;
}

/**
 * Get all elements matching selector
 */
function getElements(selector) {
  return Array.from(document.querySelectorAll(selector));
}

/**
 * Check if element has class
 */
function hasClass(el, className) {
  return el && el.classList.contains(className);
}

/**
 * Add class(es) to element
 */
function addClass(el, ...classNames) {
  if (el) el.classList.add(...classNames);
}

/**
 * Remove class(es) from element
 */
function removeClass(el, ...classNames) {
  if (el) el.classList.remove(...classNames);
}

/**
 * Toggle class on element
 */
function toggleClass(el, className) {
  if (el) el.classList.toggle(className);
}

/**
 * Get computed style value
 */
function getStyle(el, property) {
  return window.getComputedStyle(el).getPropertyValue(property);
}

/**
 * Set data attribute
 */
function setData(el, key, value) {
  if (el) el.dataset[key] = value;
}

/**
 * Get data attribute
 */
function getData(el, key) {
  return el ? el.dataset[key] : null;
}

/**
 * Deep clone object
 */
function cloneObject(obj) {
  return JSON.parse(JSON.stringify(obj));
}

/**
 * Merge objects
 */
function mergeObjects(target, source) {
  return { ...target, ...source };
}

/**
 * Check if object is empty
 */
function isEmpty(obj) {
  return Object.keys(obj).length === 0;
}

/**
 * Delay execution
 */
function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Get URL parameters
 */
function getUrlParams() {
  const params = new URLSearchParams(window.location.search);
  const result = {};
  for (const [key, value] of params) {
    result[key] = value;
  }
  return result;
}

/**
 * Build query string from object
 */
function buildQueryString(params) {
  return new URLSearchParams(params).toString();
}

/**
 * Serialize form data to object
 */
function serializeForm(form) {
  const formData = new FormData(form);
  const result = {};
  for (const [key, value] of formData) {
    if (result[key]) {
      if (Array.isArray(result[key])) {
        result[key].push(value);
      } else {
        result[key] = [result[key], value];
      }
    } else {
      result[key] = value;
    }
  }
  return result;
}

/**
 * Check if string is empty or whitespace
 */
function isBlank(str) {
  return !str || str.trim().length === 0;
}

/**
 * Capitalize first letter
 */
function capitalize(str) {
  if (!str) return '';
  return str.charAt(0).toUpperCase() + str.slice(1);
}

/**
 * Convert snake_case to camelCase
 */
function toCamelCase(str) {
  return str.replace(/_([a-z])/g, (match, letter) => letter.toUpperCase());
}

/**
 * Convert camelCase to snake_case
 */
function toSnakeCase(str) {
  return str.replace(/([A-Z])/g, '_$1').toLowerCase();
}

/**
 * Truncate string to max length with ellipsis
 */
function truncate(str, maxLength = 50, suffix = '...') {
  if (str.length <= maxLength) return str;
  return str.slice(0, maxLength - suffix.length) + suffix;
}

/**
 * Generate unique ID
 */
function generateId(prefix = '') {
  return prefix + Math.random().toString(36).substr(2, 9);
}

/**
 * Local storage with JSON support
 */
const LocalStorage = {
  set: (key, value) => {
    try {
      localStorage.setItem(key, JSON.stringify(value));
    } catch (error) {
      console.error('LocalStorage set error:', error);
    }
  },
  get: (key, defaultValue = null) => {
    try {
      const item = localStorage.getItem(key);
      return item ? JSON.parse(item) : defaultValue;
    } catch (error) {
      console.error('LocalStorage get error:', error);
      return defaultValue;
    }
  },
  remove: (key) => {
    try {
      localStorage.removeItem(key);
    } catch (error) {
      console.error('LocalStorage remove error:', error);
    }
  },
  clear: () => {
    try {
      localStorage.clear();
    } catch (error) {
      console.error('LocalStorage clear error:', error);
    }
  },
};

/**
 * Export utilities
 */
const Utils = {
  dispatchEvent,
  createElement,
  isElementVisible,
  getElements,
  hasClass,
  addClass,
  removeClass,
  toggleClass,
  getStyle,
  setData,
  getData,
  cloneObject,
  mergeObjects,
  isEmpty,
  delay,
  getUrlParams,
  buildQueryString,
  serializeForm,
  isBlank,
  capitalize,
  toCamelCase,
  toSnakeCase,
  truncate,
  generateId,
  LocalStorage,
};

// Make available globally
window.Utils = Utils;

// Export for modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = Utils;
}
