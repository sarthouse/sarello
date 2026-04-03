/**
 * Tables Module
 * Generic table functionality (sorting, filtering, pagination)
 */

/**
 * Table Manager Class
 */
class TableManager {
  constructor(tableSelector) {
    this.table = typeof tableSelector === 'string' 
      ? document.querySelector(tableSelector) 
      : tableSelector;
    
    if (!this.table) {
      console.warn('Table not found:', tableSelector);
      return;
    }

    this.thead = this.table.querySelector('thead');
    this.tbody = this.table.querySelector('tbody');
    this.rows = Array.from(this.tbody?.querySelectorAll('tr') || []);
    this.originalRows = JSON.parse(JSON.stringify(this.rows.map(r => r.innerHTML)));
    
    this.sortColumn = null;
    this.sortDirection = 'asc';
    this.filters = {};
    this.currentPage = 1;
    this.pageSize = null;
    
    this.init();
  }

  /**
   * Initialize table
   */
  init() {
    // Add click handlers to header for sorting
    if (this.thead) {
      this.thead.querySelectorAll('th').forEach((th, index) => {
        if (!th.dataset.noSort) {
          th.style.cursor = 'pointer';
          th.addEventListener('click', () => this.sort(index, th));
        }
      });
    }
  }

  /**
   * Sort by column
   */
  sort(columnIndex, headerCell) {
    const currentSort = this.sortColumn === columnIndex;
    const newDirection = currentSort && this.sortDirection === 'asc' ? 'desc' : 'asc';
    
    this.sortColumn = columnIndex;
    this.sortDirection = newDirection;

    // Update header visual
    this.thead?.querySelectorAll('th').forEach((th, idx) => {
      th.classList.remove('sort-asc', 'sort-desc');
      if (idx === columnIndex) {
        th.classList.add(`sort-${newDirection}`);
      }
    });

    // Sort rows
    this.rows.sort((a, b) => {
      const aCell = a.querySelectorAll('td')[columnIndex];
      const bCell = b.querySelectorAll('td')[columnIndex];
      
      let aValue = aCell?.textContent.trim() || '';
      let bValue = bCell?.textContent.trim() || '';

      // Try to parse as number
      const aNum = parseFloat(aValue);
      const bNum = parseFloat(bValue);
      
      if (!isNaN(aNum) && !isNaN(bNum)) {
        aValue = aNum;
        bValue = bNum;
      }

      if (newDirection === 'asc') {
        return aValue > bValue ? 1 : -1;
      } else {
        return aValue < bValue ? 1 : -1;
      }
    });

    this.render();
  }

  /**
   * Filter rows
   */
  filter(columnIndex, value) {
    this.filters[columnIndex] = value.toLowerCase();
    this.currentPage = 1;
    this.render();
  }

  /**
   * Clear all filters
   */
  clearFilters() {
    this.filters = {};
    this.currentPage = 1;
    this.render();
  }

  /**
   * Get filtered rows
   */
  getFilteredRows() {
    return this.rows.filter(row => {
      return Object.entries(this.filters).every(([colIndex, filterValue]) => {
        if (!filterValue) return true;
        const cell = row.querySelectorAll('td')[colIndex];
        const cellText = cell?.textContent.toLowerCase() || '';
        return cellText.includes(filterValue);
      });
    });
  }

  /**
   * Render table
   */
  render() {
    const filteredRows = this.getFilteredRows();
    
    // Clear tbody
    if (this.tbody) {
      this.tbody.innerHTML = '';
      
      // Add filtered rows
      filteredRows.forEach(row => {
        this.tbody.appendChild(row.cloneNode(true));
      });
    }

    // Dispatch event
    Utils?.dispatchEvent('table:rendered', {
      rowCount: filteredRows.length,
      filterCount: Object.keys(this.filters).length,
    });
  }

  /**
   * Get selected rows (if table has checkboxes)
   */
  getSelectedRows() {
    const checkboxes = this.tbody?.querySelectorAll('input[type="checkbox"]:checked') || [];
    return Array.from(checkboxes).map(cb => cb.closest('tr'));
  }

  /**
   * Get selected IDs (if rows have data-id)
   */
  getSelectedIds() {
    return this.getSelectedRows().map(row => row.dataset.id).filter(id => id);
  }

  /**
   * Select all rows
   */
  selectAll(checked = true) {
    const checkboxes = this.tbody?.querySelectorAll('input[type="checkbox"]') || [];
    checkboxes.forEach(cb => cb.checked = checked);
  }

  /**
   * Get row data
   */
  getRowData(row) {
    const result = {};
    const cells = row.querySelectorAll('td');
    const headers = this.thead?.querySelectorAll('th') || [];
    
    headers.forEach((header, index) => {
      const key = header.dataset.key || header.textContent.toLowerCase();
      const value = cells[index]?.textContent || '';
      result[key] = value.trim();
    });
    
    return result;
  }

  /**
   * Export to CSV
   */
  exportToCSV(filename = 'table.csv') {
    const headers = Array.from(this.thead?.querySelectorAll('th') || [])
      .map(th => th.textContent.trim());
    
    const rows = this.getFilteredRows().map(row => {
      return Array.from(row.querySelectorAll('td'))
        .map(td => `"${td.textContent.trim().replace(/"/g, '""')}"`)
        .join(',');
    });

    const csv = [headers.join(','), ...rows].join('\n');
    
    // Download
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    window.URL.revokeObjectURL(url);

    Utils?.dispatchEvent('table:exported', { filename });
  }

  /**
   * Reset to original state
   */
  reset() {
    this.sortColumn = null;
    this.sortDirection = 'asc';
    this.filters = {};
    this.currentPage = 1;

    if (this.thead) {
      this.thead.querySelectorAll('th').forEach(th => {
        th.classList.remove('sort-asc', 'sort-desc');
      });
    }

    this.render();
  }
}

/**
 * Export
 */
const Tables = {
  TableManager,
};

// Make available globally
window.Tables = Tables;
window.TableManager = TableManager;

// Export for modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = Tables;
}
