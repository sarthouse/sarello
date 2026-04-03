/**
 * Treasury Module
 * Movement form line management (add/remove lines, totals)
 */

class LineaManager {
  constructor(tableId, totalDebeId, totalHaberId, totalFormId) {
    this.tbody = document.getElementById(tableId);
    this.totalDebeEl = document.getElementById(totalDebeId);
    this.totalHaberEl = document.getElementById(totalHaberId);
    this.totalForm = document.getElementById(totalFormId);
    this.addBtn = document.getElementById('add-line');

    if (!this.tbody || !this.addBtn || !this.totalForm) return;

    this.updateTotals();

    this.addBtn.addEventListener('click', () => this.addLine());
    this.tbody.addEventListener('input', () => this.updateTotals());
  }

  updateTotals() {
    let totalDebe = 0, totalHaber = 0;
    this.tbody.querySelectorAll('tr').forEach(row => {
      const debe = row.querySelector('input[name$="-debe"]');
      const haber = row.querySelector('input[name$="-haber"]');
      if (debe) totalDebe += parseFloat(debe.value) || 0;
      if (haber) totalHaber += parseFloat(haber.value) || 0;
    });
    if (this.totalDebeEl) this.totalDebeEl.textContent = totalDebe.toFixed(2);
    if (this.totalHaberEl) this.totalHaberEl.textContent = totalHaber.toFixed(2);
  }

  addLine() {
    const idx = parseInt(this.totalForm.value);
    const firstRow = this.tbody.querySelector('tr');
    if (!firstRow) return;

    const newRow = firstRow.cloneNode(true);
    newRow.querySelectorAll('input, select, textarea').forEach(input => {
      input.name = input.name.replace(/-\d+-/, `-${idx}-`);
      input.id = input.id.replace(/-\d+-/, `-${idx}-`);
      if (input.type !== 'hidden') input.value = '';
    });

    this.tbody.appendChild(newRow);
    this.totalForm.value = idx + 1;
    this.updateTotals();
  }
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('lineas-table')) {
    new LineaManager('lineas-body', 'total-debe', 'total-haber', 'id_lineas-TOTAL_FORMS');
  }
});
