/**
 * Módulo de Asientos Contables
 * Maneja la lógica de agregar/eliminar líneas y cálculo de totales
 */

class AsientosManager {
  constructor(options = {}) {
    this.formId = options.formId || 'asiento-form';
    this.tableId = options.tableId || 'lineas-table';
    this.lineaBodyId = options.lineaBodyId || 'lineas-body';
    this.debeInputSelector = options.debeInputSelector || '.debe-input';
    this.haberInputSelector = options.haberInputSelector || '.haber-input';
    this.totalDebeId = options.totalDebeId || 'total-debe';
    this.totalHaberId = options.totalHaberId || 'total-haber';
    
    this.init();
  }

  init() {
    this.cacheElements();
    this.bindEvents();
    this.calculateTotals();
  }

  cacheElements() {
    this.form = document.getElementById(this.formId);
    this.tbody = document.getElementById(this.lineaBodyId);
    this.totalDebeEl = document.getElementById(this.totalDebeId);
    this.totalHaberEl = document.getElementById(this.totalHaberId);
  }

  bindEvents() {
    if (!this.form) return;

    // Delegated event listeners for inputs
    this.form.addEventListener('input', (e) => {
      if (e.target.matches(this.debeInputSelector + ', ' + this.haberInputSelector)) {
        this.calculateTotals();
      }
    });

    this.form.addEventListener('change', (e) => {
      if (e.target.matches(this.debeInputSelector + ', ' + this.haberInputSelector)) {
        this.calculateTotals();
      }
    });

    // Handle add-line button
    this.form.addEventListener('click', (e) => {
      if (e.target.closest('[data-action="add-line"]')) {
        e.preventDefault();
        this.addLine();
      }
    });

    // Handle remove-line button
    this.form.addEventListener('click', (e) => {
      if (e.target.closest('[data-action="remove-line"]')) {
        e.preventDefault();
        const button = e.target.closest('button');
        this.removeLine(button);
      }
    });

    // Prevent form submission if not balanced
    this.form.addEventListener('submit', (e) => {
      if (!this.validate()) {
        e.preventDefault();
      }
    });
  }

  /**
   * Agregar nueva línea a la tabla
   */
  addLine() {
    if (!this.tbody) return;

    const newRow = document.createElement('tr');
    newRow.className = 'linea-row border-t';
    newRow.innerHTML = this.getLineHTML();
    this.tbody.appendChild(newRow);
    this.calculateTotals();

    // Dispatch custom event
    this.dispatchEvent('linea-added', { row: newRow });
  }

  /**
   * Remover línea de la tabla
   */
  removeLine(button) {
    const rows = document.querySelectorAll('.linea-row');
    
    // No permitir eliminar si es la única línea
    if (rows.length <= 1) {
      Sarello.notify('Debe haber al menos una línea de asiento', 'warning');
      return;
    }

    const row = button.closest('tr');
    row.remove();
    this.calculateTotals();

    // Dispatch custom event
    this.dispatchEvent('linea-removed', { row });
  }

  /**
   * Calcular totales de debe y haber
   */
  calculateTotals() {
    if (!this.totalDebeEl || !this.totalHaberEl) return;

    let totalDebe = 0;
    let totalHaber = 0;

    // Sumar debe
    document.querySelectorAll(this.debeInputSelector).forEach(input => {
      totalDebe += parseFloat(input.value) || 0;
    });

    // Sumar haber
    document.querySelectorAll(this.haberInputSelector).forEach(input => {
      totalHaber += parseFloat(input.value) || 0;
    });

    // Formatear y mostrar
    this.totalDebeEl.textContent = totalDebe.toFixed(2);
    this.totalHaberEl.textContent = totalHaber.toFixed(2);

    // Validar balance
    this.validateBalance(totalDebe, totalHaber);

    // Dispatch custom event
    this.dispatchEvent('totals-calculated', { debe: totalDebe, haber: totalHaber });
  }

  /**
   * Validar que debe y haber estén balanceados
   */
  validateBalance(debe, haber) {
    const diff = Math.abs(debe - haber);
    const tolerance = 0.01; // Tolerancia para redondeos

    if (diff > tolerance) {
      // Asiento desbalanceado
      this.totalDebeEl.classList.add('text-red-600');
      this.totalHaberEl.classList.add('text-red-600');
      this.dispatchEvent('unbalanced');
    } else {
      // Asiento balanceado
      this.totalDebeEl.classList.remove('text-red-600');
      this.totalHaberEl.classList.remove('text-red-600');
      this.dispatchEvent('balanced');
    }
  }

  /**
    * Generar HTML para nueva línea
    */
  getLineHTML() {
    return `
      <td class="px-2 py-2">
        <select name="cuenta_id" class="w-full border rounded px-2 py-1 text-sm">
          <option value="">-- Seleccionar cuenta --</option>
          ${this.getCuentasOptions()}
        </select>
      </td>
      <td class="px-2 py-2">
        <input type="number" name="debe" value="" step="0.01" min="0" 
               class="w-full border rounded px-2 py-1 text-sm text-right debe-input">
      </td>
      <td class="px-2 py-2">
        <input type="number" name="haber" value="" step="0.01" min="0" 
               class="w-full border rounded px-2 py-1 text-right haber-input">
      </td>
      <td class="px-2 py-2">
        <input type="text" name="linea_descripcion" value="" 
               class="w-full border rounded px-2 py-1 text-sm">
      </td>
      <td class="px-2 py-2 text-center">
        <button type="button" class="text-red-600 hover:text-red-800 delete-line-btn" 
                data-action="remove-line">
          <i class="fas fa-times"></i>
        </button>
      </td>
    `;
  }

  /**
   * Obtener opciones de cuentas
   */
  getCuentasOptions() {
    const options = document.querySelector('select[name="cuenta_id"]');
    if (!options) return '';
    
    return Array.from(options.options)
      .map(opt => `<option value="${opt.value}">${opt.textContent}</option>`)
      .join('');
  }

  /**
   * Validar que no haya líneas con debe y haber simultáneamente
   */
  validateLines() {
    const errors = [];
    
    document.querySelectorAll('.linea-row').forEach((row, index) => {
      const debeInput = row.querySelector(this.debeInputSelector);
      const haberInput = row.querySelector(this.haberInputSelector);
      
      const debe = parseFloat(debeInput.value) || 0;
      const haber = parseFloat(haberInput.value) || 0;

      if (debe > 0 && haber > 0) {
        errors.push(`Línea ${index + 1}: No puede tener debe y haber simultáneamente`);
      }

      if (debe === 0 && haber === 0) {
        errors.push(`Línea ${index + 1}: Debe especificar debe o haber`);
      }
    });

    return errors;
  }

  /**
   * Limpiar formulario
   */
  clear() {
    if (this.form) {
      this.form.reset();
      this.calculateTotals();
    }
  }

  /**
   * Dispatch custom event
   */
  dispatchEvent(eventName, detail = {}) {
    const event = new CustomEvent(`asientos:${eventName}`, { detail });
    document.dispatchEvent(event);
  }

  /**
   * Validar antes de enviar
   */
  validate() {
    const errors = this.validateLines();
    
    if (errors.length > 0) {
      Sarello.notify(errors.join('\n'), 'error');
      return false;
    }

    const rows = document.querySelectorAll('.linea-row');
    if (rows.length === 0) {
      Sarello.notify('Debe haber al menos una línea de asiento', 'error');
      return false;
    }

    return true;
  }

  /**
   * Exportar datos del formulario
   */
  exportData() {
    const lineas = [];
    
    document.querySelectorAll('.linea-row').forEach(row => {
      const cuentaSelect = row.querySelector('select[name="cuenta_id"]');
      const debe = parseFloat(row.querySelector(this.debeInputSelector).value) || 0;
      const haber = parseFloat(row.querySelector(this.haberInputSelector).value) || 0;
      const descripcion = row.querySelector('input[name="linea_descripcion"]').value;

      lineas.push({
        cuenta_id: cuentaSelect.value,
        debe,
        haber,
        descripcion,
      });
    });

    return lineas;
  }
}

/**
 * Inicializar manager globalmente cuando está listo
 */
let asientosManager = null;

document.addEventListener('DOMContentLoaded', function() {
  // Solo inicializar si el formulario existe
  if (document.getElementById('asiento-form')) {
    asientosManager = new AsientosManager();
    
    // Hacer disponible globalmente
    window.AsientosManager = asientosManager;
    window.asientosManager = asientosManager;
  }
});

// Exportar para uso en módulos
if (typeof module !== 'undefined' && module.exports) {
  module.exports = AsientosManager;
}
