/**
 * Forms Module
 * Generic form utilities and helpers
 */

/**
 * Form Manager Class
 */
class FormManager {
  constructor(formSelector) {
    this.form = typeof formSelector === 'string' 
      ? document.querySelector(formSelector) 
      : formSelector;
    
    if (!this.form) {
      console.warn('Form not found:', formSelector);
      return;
    }

    this.fields = {};
    this.errors = {};
    this.isSubmitting = false;
    this.onSubmit = null;
    this.validators = {};
    
    this.init();
  }

  /**
   * Initialize form
   */
  init() {
    // Collect all form fields
    this.form.querySelectorAll('[name]').forEach(field => {
      this.fields[field.name] = field;
      
      // Add change listener for validation
      field.addEventListener('change', () => this.validateField(field.name));
    });

    // Handle submit
    this.form.addEventListener('submit', (e) => this.handleSubmit(e));
  }

  /**
   * Register field validator
   */
  addValidator(fieldName, validatorFunc) {
    if (!this.validators[fieldName]) {
      this.validators[fieldName] = [];
    }
    this.validators[fieldName].push(validatorFunc);
  }

  /**
   * Validate single field
   */
  validateField(fieldName) {
    const field = this.fields[fieldName];
    if (!field || !this.validators[fieldName]) return true;

    const validators = this.validators[fieldName];
    for (const validator of validators) {
      const error = validator(field.value, field);
      if (error) {
        this.setFieldError(fieldName, error);
        return false;
      }
    }

    this.clearFieldError(fieldName);
    return true;
  }

  /**
   * Validate all fields
   */
  validateAll() {
    let isValid = true;
    Object.keys(this.validators).forEach(fieldName => {
      if (!this.validateField(fieldName)) {
        isValid = false;
      }
    });
    return isValid;
  }

  /**
   * Set field error
   */
  setFieldError(fieldName, message) {
    const field = this.fields[fieldName];
    if (!field) return;

    this.errors[fieldName] = message;
    
    // Add error class to field
    field.classList.add('input-error');
    
    // Create/update error message element
    let errorEl = field.parentElement.querySelector('.field-error');
    if (!errorEl) {
      errorEl = document.createElement('div');
      errorEl.className = 'field-error text-red-600 text-sm mt-1';
      field.parentElement.appendChild(errorEl);
    }
    errorEl.textContent = message;
  }

  /**
   * Clear field error
   */
  clearFieldError(fieldName) {
    const field = this.fields[fieldName];
    if (!field) return;

    delete this.errors[fieldName];
    field.classList.remove('input-error');
    
    const errorEl = field.parentElement.querySelector('.field-error');
    if (errorEl) {
      errorEl.remove();
    }
  }

  /**
   * Handle form submit
   */
  async handleSubmit(e) {
    e.preventDefault();

    if (this.isSubmitting) return;

    // Validate before submit
    if (!this.validateAll()) {
      console.warn('Form validation failed');
      return;
    }

    this.isSubmitting = true;
    
    try {
      if (this.onSubmit) {
        await this.onSubmit(this.getData());
      } else {
        // Default: submit form normally
        this.form.submit();
      }
    } catch (error) {
      console.error('Form submit error:', error);
    } finally {
      this.isSubmitting = false;
    }
  }

  /**
   * Get form data
   */
  getData() {
    return new FormData(this.form);
  }

  /**
   * Get form data as object
   */
  getDataAsObject() {
    const formData = new FormData(this.form);
    const result = {};
    for (const [key, value] of formData) {
      result[key] = value;
    }
    return result;
  }

  /**
   * Set form data
   */
  setData(data) {
    Object.keys(data).forEach(key => {
      const field = this.fields[key];
      if (field) {
        if (field.type === 'checkbox' || field.type === 'radio') {
          field.checked = data[key];
        } else {
          field.value = data[key];
        }
      }
    });
  }

  /**
   * Clear form
   */
  clear() {
    this.form.reset();
    this.errors = {};
    this.form.querySelectorAll('.field-error').forEach(el => el.remove());
    this.form.querySelectorAll('.input-error').forEach(el => {
      el.classList.remove('input-error');
    });
  }

  /**
   * Disable form submission
   */
  disable() {
    this.form.querySelectorAll('input, textarea, select, button').forEach(el => {
      el.disabled = true;
    });
  }

  /**
   * Enable form submission
   */
  enable() {
    this.form.querySelectorAll('input, textarea, select, button').forEach(el => {
      el.disabled = false;
    });
  }

  /**
   * Show loading state
   */
  setLoading(isLoading) {
    const submitBtn = this.form.querySelector('button[type="submit"]');
    if (submitBtn) {
      submitBtn.disabled = isLoading;
      submitBtn.classList.toggle('loading', isLoading);
    }
  }
}

/**
 * Common validators
 */
const Validators = {
  required: (value) => {
    if (!value || !value.toString().trim()) {
      return 'Este campo es requerido';
    }
    return null;
  },

  minLength: (minLen) => (value) => {
    if (value && value.length < minLen) {
      return `Mínimo ${minLen} caracteres`;
    }
    return null;
  },

  maxLength: (maxLen) => (value) => {
    if (value && value.length > maxLen) {
      return `Máximo ${maxLen} caracteres`;
    }
    return null;
  },

  email: (value) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (value && !emailRegex.test(value)) {
      return 'Email inválido';
    }
    return null;
  },

  number: (value) => {
    if (value && isNaN(parseFloat(value))) {
      return 'Debe ser un número';
    }
    return null;
  },

  minValue: (minVal) => (value) => {
    if (value && parseFloat(value) < minVal) {
      return `Debe ser mayor o igual a ${minVal}`;
    }
    return null;
  },

  maxValue: (maxVal) => (value) => {
    if (value && parseFloat(value) > maxVal) {
      return `Debe ser menor o igual a ${maxVal}`;
    }
    return null;
  },

  pattern: (regex, message = 'Formato inválido') => (value) => {
    if (value && !regex.test(value)) {
      return message;
    }
    return null;
  },

  match: (otherFieldSelector, message = 'Los campos no coinciden') => (value, field) => {
    const otherField = document.querySelector(otherFieldSelector);
    if (otherField && value !== otherField.value) {
      return message;
    }
    return null;
  },
};

/**
 * Export
 */
const Forms = {
  FormManager,
  Validators,
};

// Make available globally
window.Forms = Forms;
window.FormManager = FormManager;

// Export for modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = Forms;
}
