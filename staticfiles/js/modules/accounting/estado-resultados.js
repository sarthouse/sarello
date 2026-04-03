/**
 * Módulo Estado de Resultados
 * Maneja la lógica del árbol expandible del estado de resultados
 * Similar a balance.js pero optimizado para resultados
 */

class EstadoResultadosManager {
  constructor(options = {}) {
    this.sections = options.sections || ['ingresos', 'egresos'];
    this.toggleSelector = options.toggleSelector || '.toggle-children';
    this.rowSelector = options.rowSelector || '.tree-row';
    
    this.init();
  }

  init() {
    this.bindEvents();
    this.collapseChildren();
  }

  bindEvents() {
    document.addEventListener('click', (e) => {
      if (e.target.closest(this.toggleSelector)) {
        e.stopPropagation();
        this.handleToggle(e.target.closest(this.toggleSelector));
      }
    });
  }

  /**
   * Manejar click en botón toggle
   */
  handleToggle(button) {
    const codigo = button.dataset.codigo;
    const icon = button.querySelector('i');
    const isExpanded = icon.classList.contains('fa-chevron-down');

    if (isExpanded) {
      icon.classList.remove('fa-chevron-down');
      icon.classList.add('fa-chevron-right');
      this.collapseChildren(codigo);
    } else {
      icon.classList.remove('fa-chevron-right');
      icon.classList.add('fa-chevron-down');
      this.expandChildren(codigo);
    }
  }

  /**
   * Obtener nivel de una cuenta por su código
   */
  getNivel(codigo) {
    return codigo.split('.').length - 1;
  }

  /**
   * Expandir subcuentas de una cuenta padre
   */
  expandChildren(parentCode) {
    this.sections.forEach(seccion => {
      const body = document.getElementById(`${seccion}-body`);
      if (!body) return;

      const rows = Array.from(body.querySelectorAll(this.rowSelector));
      const parentNivel = this.getNivel(parentCode);

      rows.forEach(row => {
        const codigo = row.dataset.codigo;
        
        if (codigo.startsWith(parentCode + '.')) {
          const nivel = this.getNivel(codigo);
          
          if (nivel === parentNivel + 1) {
            row.style.display = '';
          }
        }
      });
    });

    this.dispatchEvent('expanded', { codigo: parentCode });
  }

  /**
   * Contraer subcuentas de una cuenta padre
   */
  collapseChildren(parentCode = null) {
    this.sections.forEach(seccion => {
      const body = document.getElementById(`${seccion}-body`);
      if (!body) return;

      const rows = Array.from(body.querySelectorAll(this.rowSelector));

      rows.forEach(row => {
        const codigo = row.dataset.codigo;
        const nivel = this.getNivel(codigo);

        if (parentCode === null) {
          if (nivel > 0) {
            row.style.display = 'none';
          }
          const btn = row.querySelector(this.toggleSelector);
          if (btn) {
            const icon = btn.querySelector('i');
            if (icon) {
              icon.classList.remove('fa-chevron-down');
              icon.classList.add('fa-chevron-right');
            }
          }
        } else {
          if (codigo.startsWith(parentCode + '.')) {
            row.style.display = 'none';
            
            const btn = row.querySelector(this.toggleSelector);
            if (btn) {
              const icon = btn.querySelector('i');
              if (icon) {
                icon.classList.remove('fa-chevron-down');
                icon.classList.add('fa-chevron-right');
              }
            }

            this.collapseChildren(codigo);
          }
        }
      });
    });

    if (parentCode) {
      this.dispatchEvent('collapsed', { codigo: parentCode });
    }
  }

  /**
   * Expandir todos
   */
  expandAll() {
    this.sections.forEach(seccion => {
      const body = document.getElementById(`${seccion}-body`);
      if (!body) return;

      const rows = body.querySelectorAll(this.rowSelector);
      
      rows.forEach(row => {
        row.style.display = '';
        
        const btn = row.querySelector(this.toggleSelector);
        if (btn) {
          const icon = btn.querySelector('i');
          if (icon) {
            icon.classList.remove('fa-chevron-right');
            icon.classList.add('fa-chevron-down');
          }
        }
      });
    });

    this.dispatchEvent('expanded-all');
  }

  /**
   * Contraer todos
   */
  collapseAll() {
    this.collapseChildren();
    this.dispatchEvent('collapsed-all');
  }

  /**
   * Filtrar por rango de valores
   */
  filterByRange(minValue, maxValue) {
    this.sections.forEach(seccion => {
      const body = document.getElementById(`${seccion}-body`);
      if (!body) return;

      const rows = body.querySelectorAll(this.rowSelector);
      
      rows.forEach(row => {
        const valueCell = row.querySelector('td:nth-child(3)');
        if (valueCell) {
          const value = parseFloat(valueCell.textContent.replace(/[^\d.-]/g, '')) || 0;
          
          if (value >= minValue && value <= maxValue) {
            row.style.display = '';
          } else {
            row.style.display = 'none';
          }
        }
      });
    });

    this.dispatchEvent('filtered', { minValue, maxValue });
  }

  /**
   * Limpiar filtro
   */
  clearFilter() {
    this.collapseChildren();
    this.dispatchEvent('filter-cleared');
  }

  /**
   * Calcular total de una sección
   */
  getSectionTotal(seccion) {
    const body = document.getElementById(`${seccion}-body`);
    if (!body) return 0;

    let total = 0;
    const rows = body.querySelectorAll(`${this.rowSelector}[data-nivel="0"]`);
    
    rows.forEach(row => {
      const valueCell = row.querySelector('td:nth-child(3)');
      if (valueCell) {
        const value = parseFloat(valueCell.textContent.replace(/[^\d.-]/g, '')) || 0;
        total += value;
      }
    });

    return total;
  }

  /**
   * Exportar datos
   */
  exportData() {
    const data = {};

    this.sections.forEach(seccion => {
      const body = document.getElementById(`${seccion}-body`);
      if (!body) return;

      data[seccion] = [];
      const rows = body.querySelectorAll(this.rowSelector);
      
      rows.forEach(row => {
        if (row.style.display !== 'none') {
          const codigo = row.dataset.codigo;
          const valueCell = row.querySelector('td:nth-child(3)');
          const value = parseFloat(valueCell?.textContent.replace(/[^\d.-]/g, '')) || 0;
          
          data[seccion].push({
            codigo,
            valor: value,
          });
        }
      });
    });

    return data;
  }

  /**
   * Dispatch custom event
   */
  dispatchEvent(eventName, detail = {}) {
    const event = new CustomEvent(`estado-resultados:${eventName}`, { detail });
    document.dispatchEvent(event);
  }
}

/**
 * Inicializar manager globalmente cuando está listo
 */
let estadoResultadosManager = null;

document.addEventListener('DOMContentLoaded', function() {
  if (document.querySelector('.toggle-children[data-module="estado-resultados"]') || 
      document.getElementById('ingresos-body')) {
    estadoResultadosManager = new EstadoResultadosManager();
    
    window.EstadoResultadosManager = estadoResultadosManager;
    window.estadoResultadosManager = estadoResultadosManager;
  }
});

if (typeof module !== 'undefined' && module.exports) {
  module.exports = EstadoResultadosManager;
}
