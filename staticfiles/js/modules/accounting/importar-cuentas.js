/**
 * Módulo Importar Cuentas
 * Maneja la importación de archivo CSV y validación
 */

class ImportarCuentasManager {
  constructor(options = {}) {
    this.fileInputId = options.fileInputId || 'file-input';
    this.formId = options.formId || 'import-form';
    this.previewTableId = options.previewTableId || 'preview-table';
    this.submitBtnId = options.submitBtnId || 'submit-btn';
    this.maxRows = options.maxRows || 1000;
    
    this.init();
  }

  init() {
    this.cacheElements();
    this.bindEvents();
  }

  cacheElements() {
    this.fileInput = document.getElementById(this.fileInputId);
    this.form = document.getElementById(this.formId);
    this.previewTable = document.getElementById(this.previewTableId);
    this.submitBtn = document.getElementById(this.submitBtnId);
  }

  bindEvents() {
    if (this.fileInput) {
      this.fileInput.addEventListener('change', (e) => {
        this.handleFileSelect(e);
      });
    }

    if (this.form) {
      this.form.addEventListener('submit', (e) => {
        this.handleSubmit(e);
      });
    }
  }

  /**
   * Manejar selección de archivo
   */
  handleFileSelect(event) {
    const file = event.target.files[0];
    
    if (!file) return;

    // Validar tipo de archivo
    if (!file.name.endsWith('.csv')) {
      Sarello.notify('Solo se aceptan archivos CSV', 'error');
      this.fileInput.value = '';
      return;
    }

    // Validar tamaño (máx 5MB)
    if (file.size > 5 * 1024 * 1024) {
      Sarello.notify('El archivo es demasiado grande (máx 5MB)', 'error');
      this.fileInput.value = '';
      return;
    }

    this.readAndPreviewFile(file);
  }

  /**
   * Leer y previsualizar archivo
   */
  readAndPreviewFile(file) {
    const reader = new FileReader();
    
    reader.onload = (e) => {
      try {
        const csv = e.target.result;
        const rows = this.parseCSV(csv);
        
        if (rows.length === 0) {
          Sarello.notify('El archivo CSV está vacío', 'warning');
          return;
        }

        if (rows.length > this.maxRows) {
          Sarello.notify(
            `El archivo contiene ${rows.length} filas. Se procesarán solo las primeras ${this.maxRows}`,
            'warning'
          );
          rows.splice(this.maxRows);
        }

        this.displayPreview(rows);
        this.dispatchEvent('file-loaded', { file, rows });
      } catch (error) {
        Sarello.notify(`Error al procesar archivo: ${error.message}`, 'error');
      }
    };

    reader.onerror = () => {
      Sarello.notify('Error al leer el archivo', 'error');
    };

    reader.readAsText(file);
  }

  /**
   * Parsear CSV a array de objetos
   */
  parseCSV(csv) {
    const lines = csv.trim().split('\n');
    if (lines.length < 2) return [];

    const headers = this.parseCSVLine(lines[0]);
    const rows = [];

    for (let i = 1; i < lines.length; i++) {
      const values = this.parseCSVLine(lines[i]);
      if (values.length === 0) continue;

      const row = {};
      headers.forEach((header, index) => {
        row[header] = values[index] || '';
      });
      rows.push(row);
    }

    return rows;
  }

  /**
   * Parsear una línea de CSV
   */
  parseCSVLine(line) {
    const result = [];
    let current = '';
    let insideQuotes = false;

    for (let i = 0; i < line.length; i++) {
      const char = line[i];

      if (char === '"') {
        insideQuotes = !insideQuotes;
      } else if (char === ',' && !insideQuotes) {
        result.push(current.trim());
        current = '';
      } else {
        current += char;
      }
    }

    result.push(current.trim());
    return result;
  }

  /**
   * Mostrar previsualización de datos
   */
  displayPreview(rows) {
    if (!this.previewTable) return;

    // Limpiar tabla anterior
    this.previewTable.innerHTML = '';

    // Crear header
    const headerRow = document.createElement('tr');
    const firstRow = rows[0];

    Object.keys(firstRow).forEach(key => {
      const th = document.createElement('th');
      th.textContent = key;
      headerRow.appendChild(th);
    });

    const thead = document.createElement('thead');
    thead.className = 'bg-gray-100';
    thead.appendChild(headerRow);
    this.previewTable.appendChild(thead);

    // Crear filas (máximo 10)
    const tbody = document.createElement('tbody');
    const previewRows = rows.slice(0, 10);

    previewRows.forEach((row, index) => {
      const tr = document.createElement('tr');
      tr.className = index % 2 === 0 ? '' : 'bg-gray-50';

      Object.values(row).forEach(value => {
        const td = document.createElement('td');
        td.textContent = value;
        td.className = 'px-4 py-2 border';
        tr.appendChild(td);
      });

      tbody.appendChild(tr);
    });

    this.previewTable.appendChild(tbody);

    // Mostrar info
    const info = document.createElement('div');
    info.className = 'mt-4 text-sm text-gray-600';
    info.innerHTML = `
      <p><strong>Cuentas a importar:</strong> ${rows.length}</p>
      ${rows.length > 10 ? `<p class="text-yellow-600">Se muestran solo las primeras 10 en la previsualización</p>` : ''}
    `;
    this.previewTable.after(info);

    // Habilitar botón submit
    if (this.submitBtn) {
      this.submitBtn.disabled = false;
    }

    this.dispatchEvent('preview-displayed', { rowCount: rows.length });
  }

  /**
   * Validar datos antes de importar
   */
  validateRows(rows) {
    const errors = [];

    rows.forEach((row, index) => {
      // Validar campos requeridos
      if (!row.codigo) {
        errors.push(`Fila ${index + 1}: Falta el código`);
      }
      if (!row.nombre) {
        errors.push(`Fila ${index + 1}: Falta el nombre`);
      }
      if (!row.tipo) {
        errors.push(`Fila ${index + 1}: Falta el tipo`);
      }

      // Validar tipo válido
      const tiposValidos = ['activo', 'pasivo', 'patrimonio', 'ingreso', 'egreso'];
      if (row.tipo && !tiposValidos.includes(row.tipo.toLowerCase())) {
        errors.push(`Fila ${index + 1}: Tipo de cuenta inválido`);
      }
    });

    return errors;
  }

  /**
   * Manejar submit del formulario
   */
  handleSubmit(e) {
    e.preventDefault();

    if (!this.fileInput.files[0]) {
      Sarello.notify('Por favor selecciona un archivo', 'warning');
      return;
    }

    // Los datos se enviarán al servidor automáticamente
    // ya que el archivo está en el input file

    this.dispatchEvent('submit', {
      file: this.fileInput.files[0],
    });
  }

  /**
   * Resetear formulario
   */
  reset() {
    if (this.fileInput) {
      this.fileInput.value = '';
    }
    if (this.previewTable) {
      this.previewTable.innerHTML = '';
    }
    if (this.submitBtn) {
      this.submitBtn.disabled = true;
    }
    this.dispatchEvent('reset');
  }

  /**
   * Descargar template CSV
   */
  downloadTemplate() {
    const headers = ['codigo', 'nombre', 'tipo', 'padre', 'acepta_movimientos'];
    const example = ['1', 'Activos', 'activo', '', '0'];

    const csv = [headers.join(','), example.join(',')].join('\n');
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'template_cuentas.csv';
    a.click();
    window.URL.revokeObjectURL(url);

    this.dispatchEvent('template-downloaded');
  }

  /**
   * Dispatch custom event
   */
  dispatchEvent(eventName, detail = {}) {
    const event = new CustomEvent(`importar-cuentas:${eventName}`, { detail });
    document.dispatchEvent(event);
  }
}

/**
 * Inicializar manager globalmente cuando está listo
 */
let importarCuentasManager = null;

document.addEventListener('DOMContentLoaded', function() {
  if (document.getElementById('import-form')) {
    importarCuentasManager = new ImportarCuentasManager();
    
    window.ImportarCuentasManager = importarCuentasManager;
    window.importarCuentasManager = importarCuentasManager;
  }
});

if (typeof module !== 'undefined' && module.exports) {
  module.exports = ImportarCuentasManager;
}
