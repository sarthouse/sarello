/**
 * Modals Module
 * Modal management and helpers
 */

/**
 * Modal Manager Class
 */
class ModalManager {
  constructor(modalSelector) {
    this.modal = typeof modalSelector === 'string' 
      ? document.querySelector(modalSelector) 
      : modalSelector;
    
    if (!this.modal) {
      console.warn('Modal not found:', modalSelector);
      return;
    }

    this.isOpen = false;
    this.onClose = null;
    this.onConfirm = null;
    
    this.init();
  }

  /**
   * Initialize modal
   */
  init() {
    // Close on backdrop click
    this.modal.addEventListener('click', (e) => {
      if (e.target === this.modal) {
        this.close();
      }
    });

    // Close button
    const closeBtn = this.modal.querySelector('[data-close-modal]');
    if (closeBtn) {
      closeBtn.addEventListener('click', () => this.close());
    }

    // Confirm button
    const confirmBtn = this.modal.querySelector('[data-confirm-modal]');
    if (confirmBtn) {
      confirmBtn.addEventListener('click', () => this.confirm());
    }

    // ESC key to close
    this.modal.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        this.close();
      }
    });
  }

  /**
   * Open modal
   */
  open() {
    this.isOpen = true;
    this.modal.classList.add('modal-open');
    this.modal.showModal?.();
    
    Utils?.dispatchEvent('modal:opened', { modalId: this.modal.id });
  }

  /**
   * Close modal
   */
  close() {
    this.isOpen = false;
    this.modal.classList.remove('modal-open');
    this.modal.close?.();
    
    if (this.onClose) {
      this.onClose();
    }
    
    Utils?.dispatchEvent('modal:closed', { modalId: this.modal.id });
  }

  /**
   * Confirm and close
   */
  confirm() {
    if (this.onConfirm) {
      this.onConfirm();
    }
    this.close();
    
    Utils?.dispatchEvent('modal:confirmed', { modalId: this.modal.id });
  }

  /**
   * Set modal content
   */
  setContent(content) {
    const contentEl = this.modal.querySelector('[data-modal-content]');
    if (contentEl) {
      if (typeof content === 'string') {
        contentEl.innerHTML = content;
      } else {
        contentEl.appendChild(content);
      }
    }
  }

  /**
   * Set modal title
   */
  setTitle(title) {
    const titleEl = this.modal.querySelector('[data-modal-title]');
    if (titleEl) {
      titleEl.textContent = title;
    }
  }

  /**
   * Clear modal
   */
  clear() {
    const contentEl = this.modal.querySelector('[data-modal-content]');
    if (contentEl) {
      contentEl.innerHTML = '';
    }
  }

  /**
   * Show loading state
   */
  setLoading(isLoading) {
    const spinner = this.modal.querySelector('[data-modal-loading]');
    if (spinner) {
      spinner.classList.toggle('hidden', !isLoading);
    }

    const content = this.modal.querySelector('[data-modal-content]');
    if (content) {
      content.classList.toggle('opacity-50', isLoading);
    }
  }
}

/**
 * Simple alert modal
 */
function showAlert(title, message, type = 'info') {
  const modal = document.createElement('div');
  modal.className = `modal modal-${type}`;
  modal.innerHTML = `
    <div class="modal-box">
      <h3 class="font-bold text-lg">${title}</h3>
      <p class="py-4">${message}</p>
      <div class="modal-action">
        <button class="btn btn-primary" onclick="this.closest('.modal').remove()">OK</button>
      </div>
    </div>
  `;
  
  document.body.appendChild(modal);
  const modalEl = new ModalManager(modal);
  modalEl.open();
}

/**
 * Confirmation modal
 */
function showConfirm(title, message, onConfirm, onCancel) {
  const modal = document.createElement('div');
  modal.className = 'modal modal-confirm';
  modal.innerHTML = `
    <div class="modal-box">
      <h3 class="font-bold text-lg">${title}</h3>
      <p class="py-4">${message}</p>
      <div class="modal-action">
        <button class="btn btn-ghost" data-cancel-modal>Cancelar</button>
        <button class="btn btn-primary" data-confirm-modal>Confirmar</button>
      </div>
    </div>
  `;
  
  document.body.appendChild(modal);
  const modalEl = new ModalManager(modal);
  
  modalEl.onConfirm = onConfirm;
  modalEl.onClose = onCancel;
  
  const cancelBtn = modal.querySelector('[data-cancel-modal]');
  if (cancelBtn) {
    cancelBtn.addEventListener('click', () => modalEl.close());
  }
  
  modalEl.open();
}

/**
 * Loading modal
 */
function showLoading(title = 'Cargando...') {
  const modal = document.createElement('div');
  modal.className = 'modal modal-loading';
  modal.innerHTML = `
    <div class="modal-box">
      <h3 class="font-bold text-lg">${title}</h3>
      <div class="py-4 flex justify-center">
        <div class="loading loading-spinner loading-lg"></div>
      </div>
    </div>
  `;
  
  document.body.appendChild(modal);
  const modalEl = new ModalManager(modal);
  modalEl.open();
  
  return modalEl;
}

/**
 * Input modal
 */
function showInput(title, message, placeholder = '', onConfirm) {
  const modal = document.createElement('div');
  modal.className = 'modal modal-input';
  modal.innerHTML = `
    <div class="modal-box">
      <h3 class="font-bold text-lg">${title}</h3>
      <p class="py-4">${message}</p>
      <input type="text" placeholder="${placeholder}" class="input input-bordered w-full" data-input-field />
      <div class="modal-action">
        <button class="btn btn-ghost" data-cancel-modal>Cancelar</button>
        <button class="btn btn-primary" data-confirm-modal>Confirmar</button>
      </div>
    </div>
  `;
  
  document.body.appendChild(modal);
  const modalEl = new ModalManager(modal);
  
  const inputField = modal.querySelector('[data-input-field]');
  
  modalEl.onConfirm = () => {
    if (onConfirm) {
      onConfirm(inputField.value);
    }
  };
  
  const cancelBtn = modal.querySelector('[data-cancel-modal]');
  if (cancelBtn) {
    cancelBtn.addEventListener('click', () => modalEl.close());
  }
  
  modalEl.open();
  inputField.focus();
  
  return { modal: modalEl, input: inputField };
}

/**
 * Export
 */
const Modals = {
  ModalManager,
  showAlert,
  showConfirm,
  showLoading,
  showInput,
};

// Make available globally
window.Modals = Modals;
window.ModalManager = ModalManager;
window.showAlert = showAlert;
window.showConfirm = showConfirm;
window.showLoading = showLoading;
window.showInput = showInput;

// Export for modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = Modals;
}
