/**
 * Módulo de Contabilidad - Entry Point
 * Carga e inicializa todos los submódulos de contabilidad
 */

// Importar managers (en un ambiente de bundler, estos serían imports ES6)
// Para desarrollo sin bundler, estos se cargan automáticamente

/**
 * Inicializar módulo de contabilidad
 */
function initAccounting() {
  // Verificar que los managers estén disponibles
  const managers = {
    asientos: typeof AsientosManager !== 'undefined',
    balance: typeof BalanceTreeManager !== 'undefined',
    planCuentas: typeof PlanCuentasManager !== 'undefined',
    estadoResultados: typeof EstadoResultadosManager !== 'undefined',
    importarCuentas: typeof ImportarCuentasManager !== 'undefined',
  };

  // Log de carga
  console.log('Accounting module initialized', {
    managers,
    timestamp: new Date().toISOString(),
  });

  // Registrar listeners de eventos globales
  registerGlobalListeners();

  // Dispatch evento de inicialización
  dispatchEvent('accounting-initialized', { managers });
}

/**
 * Registrar listeners globales
 */
function registerGlobalListeners() {
  // Asientos - validación antes de enviar
  document.addEventListener('asientos:totals-calculated', (e) => {
    const { debe, haber } = e.detail;
    updateAsientosStatus(debe, haber);
  });

  document.addEventListener('asientos:unbalanced', () => {
    console.warn('Asiento desbalanceado');
  });

  document.addEventListener('asientos:balanced', () => {
    console.log('Asiento balanceado');
  });

  // Balance - tracking de expansiones
  document.addEventListener('balance:expanded', (e) => {
    console.log('Account expanded:', e.detail.codigo);
  });

  document.addEventListener('balance:collapsed', (e) => {
    console.log('Account collapsed:', e.detail.codigo);
  });

  // Plan de Cuentas - bulk actions
  document.addEventListener('plan-cuentas:action-confirmed', (e) => {
    const { action, count } = e.detail;
    console.log(`Bulk action "${action}" on ${count} accounts`);
  });

  // Estado de Resultados
  document.addEventListener('estado-resultados:filtered', (e) => {
    const { minValue, maxValue } = e.detail;
    console.log(`Filtered results: ${minValue} - ${maxValue}`);
  });

  // Importar Cuentas
  document.addEventListener('importar-cuentas:file-loaded', (e) => {
    const { rows } = e.detail;
    console.log(`Loaded ${rows.length} rows from file`);
  });

  document.addEventListener('importar-cuentas:preview-displayed', (e) => {
    const { rowCount } = e.detail;
    console.log(`Displaying preview of ${rowCount} rows`);
  });
}

/**
 * Actualizar estado del asiento
 */
function updateAsientosStatus(debe, haber) {
  const diff = Math.abs(debe - haber);
  const isBalanced = diff < 0.01;

  // Actualizar indicador visual si existe
  const statusEl = document.getElementById('asiento-status');
  if (statusEl) {
    if (isBalanced) {
      statusEl.classList.remove('text-red-600');
      statusEl.classList.add('text-green-600');
      statusEl.textContent = '✓ Balanceado';
    } else {
      statusEl.classList.remove('text-green-600');
      statusEl.classList.add('text-red-600');
      statusEl.textContent = `✗ Desbalanceado (diferencia: ${diff.toFixed(2)})`;
    }
  }
}

/**
 * Dispatch custom event
 */
function dispatchEvent(eventName, detail = {}) {
  const event = new CustomEvent(`accounting:${eventName}`, { detail });
  document.dispatchEvent(event);
}

/**
 * Exportar funciones públicas
 */
const AccoutingModule = {
  init: initAccounting,
  dispatchEvent,
  updateAsientosStatus,
};

// Hacer disponible globalmente
window.AccoutingModule = AccoutingModule;
window.initAccounting = initAccounting;

// Inicializar automáticamente si está en página de contabilidad
document.addEventListener('DOMContentLoaded', function() {
  if (document.body.dataset.module === 'accounting' || 
      document.getElementById('asiento-form') ||
      document.querySelector('.toggle-children')) {
    initAccounting();
  }
});

// Exportar para módulos
if (typeof module !== 'undefined' && module.exports) {
  module.exports = AccoutingModule;
}
