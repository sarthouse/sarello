/**
 * Módulo de Balance - Árbol Expandible
 * Maneja la lógica de toggle de subcuentas en el balance
 */

class BalanceTreeManager {
  constructor(options = {}) {
    this.sections = options.sections || ['activo', 'pasivo', 'patrimonio'];
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
        
        // Mostrar solo los hijos directos
        if (codigo.startsWith(parentCode + '.')) {
          const nivel = this.getNivel(codigo);
          
          // Mostrar solo nivel inmediato inferior
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

        // Si no hay parentCode, ocultar todos menos nivel 0
        if (parentCode === null) {
          if (nivel > 0) {
            row.style.display = 'none';
          }
          // Resetear iconos
          const btn = row.querySelector(this.toggleSelector);
          if (btn) {
            const icon = btn.querySelector('i');
            if (icon) {
              icon.classList.remove('fa-chevron-down');
              icon.classList.add('fa-chevron-right');
            }
          }
        } else {
          // Ocultar hijos de parentCode
          if (codigo.startsWith(parentCode + '.')) {
            row.style.display = 'none';
            
            // Resetear iconos de los hijos
            const btn = row.querySelector(this.toggleSelector);
            if (btn) {
              const icon = btn.querySelector('i');
              if (icon) {
                icon.classList.remove('fa-chevron-down');
                icon.classList.add('fa-chevron-right');
              }
            }

            // Recursivamente ocultar nietos
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
   * Expandir todos los niveles
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
   * Contraer todos los niveles
   */
  collapseAll() {
    this.collapseChildren();
    this.dispatchEvent('collapsed-all');
  }

  /**
   * Toggle un nivel específico
   */
  toggleLevel(level) {
    this.sections.forEach(seccion => {
      const body = document.getElementById(`${seccion}-body`);
      if (!body) return;

      const rows = body.querySelectorAll(this.rowSelector);
      
      rows.forEach(row => {
        const nivel = this.getNivel(row.dataset.codigo);
        
        if (nivel <= level) {
          row.style.display = '';
        } else {
          row.style.display = 'none';
        }
      });
    });

    this.dispatchEvent('level-toggled', { level });
  }

  /**
   * Buscar y expandir cuenta
   */
  searchAndExpand(searchTerm) {
    const searchLower = searchTerm.toLowerCase();
    let found = false;

    this.sections.forEach(seccion => {
      const body = document.getElementById(`${seccion}-body`);
      if (!body) return;

      const rows = body.querySelectorAll(this.rowSelector);
      
      rows.forEach(row => {
        const codigo = row.dataset.codigo;
        
        if (codigo.includes(searchLower)) {
          found = true;
          row.style.display = '';
          row.classList.add('highlight');
          
          // Expandir todos los padres
          this.expandAllParents(codigo);
        }
      });
    });

    this.dispatchEvent('search-completed', { found, term: searchTerm });
    return found;
  }

  /**
   * Expandir todos los padres de una cuenta
   */
  expandAllParents(codigo) {
    const parts = codigo.split('.');
    
    for (let i = 1; i < parts.length; i++) {
      const parentCode = parts.slice(0, i).join('.');
      this.expandChildren(parentCode);
    }
  }

  /**
   * Limpiar búsqueda
   */
  clearSearch() {
    this.sections.forEach(seccion => {
      const body = document.getElementById(`${seccion}-body`);
      if (!body) return;

      const rows = body.querySelectorAll(this.rowSelector);
      rows.forEach(row => {
        row.classList.remove('highlight');
      });
    });

    this.collapseChildren();
    this.dispatchEvent('search-cleared');
  }

  /**
   * Obtener estado actual del árbol
   */
  getState() {
    const state = {};

    this.sections.forEach(seccion => {
      state[seccion] = {
        expanded: [],
        collapsed: [],
      };

      const body = document.getElementById(`${seccion}-body`);
      if (!body) return;

      const rows = body.querySelectorAll(this.rowSelector);
      rows.forEach(row => {
        const btn = row.querySelector(this.toggleSelector);
        if (btn) {
          const icon = btn.querySelector('i');
          const codigo = row.dataset.codigo;
          
          if (icon.classList.contains('fa-chevron-down')) {
            state[seccion].expanded.push(codigo);
          } else {
            state[seccion].collapsed.push(codigo);
          }
        }
      });
    });

    return state;
  }

  /**
   * Restaurar estado del árbol
   */
  restoreState(state) {
    this.sections.forEach(seccion => {
      if (!state[seccion]) return;

      const body = document.getElementById(`${seccion}-body`);
      if (!body) return;

      state[seccion].expanded.forEach(codigo => {
        this.expandChildren(codigo);
      });
    });

    this.dispatchEvent('state-restored');
  }

  /**
   * Dispatch custom event
   */
  dispatchEvent(eventName, detail = {}) {
    const event = new CustomEvent(`balance:${eventName}`, { detail });
    document.dispatchEvent(event);
  }
}

/**
 * Inicializar manager globalmente cuando está listo
 */
let balanceManager = null;

document.addEventListener('DOMContentLoaded', function() {
  // Solo inicializar si hay elementos del balance
  if (document.querySelector('.toggle-children')) {
    balanceManager = new BalanceTreeManager();
    
    // Hacer disponible globalmente
    window.BalanceTreeManager = balanceManager;
    window.balanceManager = balanceManager;
  }
});

// Exportar para uso en módulos
if (typeof module !== 'undefined' && module.exports) {
  module.exports = BalanceTreeManager;
}
