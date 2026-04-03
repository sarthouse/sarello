/**
 * Módulo Plan de Cuentas
 * Maneja bulk actions, select all, y confirmaciones
 */

class PlanCuentasManager {
  constructor(options = {}) {
    this.bulkFormId = options.bulkFormId || 'bulk-form';
    this.selectAllId = options.selectAllId || 'select-all';
    this.checkboxSelector = options.checkboxSelector || '.cuenta-checkbox';
    this.bulkActionId = options.bulkActionId || 'bulk-action';
    this.bulkSubmitId = options.bulkSubmitId || 'bulk-submit';

    this.init();
  }

  init() {
    this.cacheElements();
    this.bindEvents();
  }

  cacheElements() {
    this.bulkForm = document.getElementById(this.bulkFormId);
    this.selectAllCheckbox = document.getElementById(this.selectAllId);
    this.bulkActionSelect = document.getElementById(this.bulkActionId);
    this.bulkSubmitBtn = document.getElementById(this.bulkSubmitId);
    this.checkboxes = document.querySelectorAll(this.checkboxSelector);
  }

  bindEvents() {
    if (!this.selectAllCheckbox) return;

    // Select all checkbox
    this.selectAllCheckbox.addEventListener('change', () => {
      this.toggleSelectAll();
    });

    // Individual checkboxes
    this.checkboxes.forEach(checkbox => {
      checkbox.addEventListener('change', () => {
        this.updateBulkUI();
      });
    });

    // Bulk action select change
    if (this.bulkActionSelect) {
      this.bulkActionSelect.addEventListener('change', () => {
        this.updateBulkUI();
      });
    }

    // Form submit
    if (this.bulkForm) {
      this.bulkForm.addEventListener('submit', (e) => {
        this.handleSubmit(e);
      });
    }
  }

  /**
   * Toggle select all checkboxes
   */
  toggleSelectAll() {
    const isChecked = this.selectAllCheckbox.checked;
    
    this.checkboxes.forEach(checkbox => {
      checkbox.checked = isChecked;
    });

    this.updateBulkUI();
    this.dispatchEvent('select-all-toggled', { isChecked });
  }

  /**
   * Actualizar UI de bulk actions
   */
  updateBulkUI() {
    const checkedCount = this.getCheckedCount();
    const hasSelection = checkedCount > 0;

    // Habilitar/deshabilitar botones
    if (this.bulkActionSelect) {
      this.bulkActionSelect.disabled = !hasSelection;
    }

    if (this.bulkSubmitBtn) {
      this.bulkSubmitBtn.disabled = !hasSelection;
    }

    // Cambiar color del botón según acción
    if (this.bulkActionSelect && this.bulkSubmitBtn) {
      const action = this.bulkActionSelect.value;
      
      this.bulkSubmitBtn.classList.remove('bg-green-600', 'hover:bg-green-700', 'bg-red-600', 'hover:bg-red-700');

      if (action === 'delete') {
        this.bulkSubmitBtn.classList.add('bg-red-600', 'hover:bg-red-700');
      } else {
        this.bulkSubmitBtn.classList.add('bg-green-600', 'hover:bg-green-700');
      }
    }

    // Actualizar select all checkbox
    if (this.selectAllCheckbox) {
      this.selectAllCheckbox.checked = checkedCount === this.checkboxes.length && checkedCount > 0;
      this.selectAllCheckbox.indeterminate = checkedCount > 0 && checkedCount < this.checkboxes.length;
    }

    this.dispatchEvent('ui-updated', { checkedCount });
  }

  /**
   * Obtener cantidad de checkboxes marcados
   */
  getCheckedCount() {
    return document.querySelectorAll(`${this.checkboxSelector}:checked`).length;
  }

  /**
   * Obtener IDs de cuentas seleccionadas
   */
  getSelectedIds() {
    return Array.from(document.querySelectorAll(`${this.checkboxSelector}:checked`))
      .map(checkbox => checkbox.value);
  }

  /**
   * Manejar submit del formulario
   */
  handleSubmit(e) {
    const action = this.bulkActionSelect?.value;
    const count = this.getCheckedCount();

    if (!action || count === 0) {
      e.preventDefault();
      return;
    }

    let confirmMessage = '';

    switch (action) {
      case 'delete':
        confirmMessage = `¿Eliminar ${count} cuenta${count > 1 ? 's' : ''}?`;
        break;
      case 'activate':
        confirmMessage = `¿Activar ${count} cuenta${count > 1 ? 's' : ''}?`;
        break;
      case 'deactivate':
        confirmMessage = `¿Desactivar ${count} cuenta${count > 1 ? 's' : ''}?`;
        break;
      default:
        confirmMessage = `¿Ejecutar acción "${action}" en ${count} cuenta${count > 1 ? 's' : ''}?`;
    }

    if (!confirm(confirmMessage)) {
      e.preventDefault();
      return;
    }

    this.dispatchEvent('action-confirmed', { action, count });
  }

  /**
   * Seleccionar cuentas por tipo
   */
  selectByType(type) {
    this.checkboxes.forEach(checkbox => {
      const row = checkbox.closest('tr');
      if (row) {
        const tipoCell = row.textContent;
        checkbox.checked = tipoCell.includes(type);
      }
    });

    this.updateBulkUI();
    this.dispatchEvent('selected-by-type', { type });
  }

  /**
   * Deseleccionar todo
   */
  deselectAll() {
    this.checkboxes.forEach(checkbox => {
      checkbox.checked = false;
    });

    if (this.selectAllCheckbox) {
      this.selectAllCheckbox.checked = false;
    }

    this.updateBulkUI();
    this.dispatchEvent('all-deselected');
  }

  /**
   * Invertir selección
   */
  invertSelection() {
    this.checkboxes.forEach(checkbox => {
      checkbox.checked = !checkbox.checked;
    });

    this.updateBulkUI();
    this.dispatchEvent('selection-inverted');
  }

  /**
   * Dispatch custom event
   */
  dispatchEvent(eventName, detail = {}) {
    const event = new CustomEvent(`plan-cuentas:${eventName}`, { detail });
    document.dispatchEvent(event);
  }
}

/**
 * Inicializar manager globalmente cuando está listo
 */
let planCuentasManager = null;

document.addEventListener('DOMContentLoaded', function() {
  // Solo inicializar si el formulario existe
  if (document.getElementById('bulk-form')) {
    planCuentasManager = new PlanCuentasManager();
    
    // Hacer disponible globalmente
    window.PlanCuentasManager = planCuentasManager;
    window.planCuentasManager = planCuentasManager;
  }
});

// Exportar para uso en módulos
if (typeof module !== 'undefined' && module.exports) {
  module.exports = PlanCuentasManager;
}
