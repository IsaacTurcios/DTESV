 
document.addEventListener('DOMContentLoaded', function() {
 //window.addEventListener('load', function()    {
      // Declarar empresaSeleccionada
  
  var empresaSeleccionada;

  // Función para obtener la empresa seleccionada
  function obtenerEmpresaSeleccionada() {
    return empresaSeleccionada;
  }

  // Función para cambiar la empresa seleccionada
  function cambiarEmpresa() {
    var empresasSelect = document.getElementById('empresas');
    empresaSeleccionada = empresasSelect.options[empresasSelect.selectedIndex].value;
    document.cookie = "empresaSeleccionada=" + empresaSeleccionada;
  }

  // Evento para detectar el cambio en el select de empresas
  document.getElementById('empresas').addEventListener('change', cambiarEmpresa);
  var defaultHiddenColumns = [13, 14];
  // Llama a cambiarEmpresa al cargar la página para inicializar empresaSeleccionada
  cambiarEmpresa();   
    // Obtener el enlace de documentos
    var dashboardLink = document.getElementById('dashboard-link');
    var documentosLink = document.getElementById('documentos-link');
    var contingeiasLInk = document.getElementById('contingencias-link');
    //console.log(documentosLink);
    //var settingsLink = document.getElementById('settings-link');
    
    // Obtener el contenedor para la tabla de documentos
    var dashboardContainer = document.getElementById('dashboard-container');
    var documentosContainer = document.getElementById('documentos-container');
    var contingenciasContainer = document.getElementById('contingencia-container');
    //var settingsContainer = document.getElementById('settings-container');
    var reprocessButton ;
    
    
    
    

    var bt_busqueda;

    const dataTableOptions = {
      "order": [[7, 'desc']],
      columnDefs: [
        
        { className: 'centered', targets: [0, 1, 2] },
        { searching: true, targets: [0, 3, 9] },
       // { searchable: false, targets: [2] },
        { "type": "time-uni", "targets": 7 }
      ],
      pageLength: 25,
      destroy: true,
      responsive: true
    };
    
    
    
  
    // Función para cargar la tabla de documentos
    function cargarDocumentos(fecha_desde_p, fecha_hasta_p) {https://www.bing.com/ck/a?!&&p=f5f2f725623062baJmltdHM9MTY5MDI0MzIwMCZpZ3VpZD0zMmUwMzVjOS00MGIzLTYyODQtMDhlMy0yNmZlNDEwZDYzYjQmaW5zaWQ9NTA0MQ&ptn=3&hsh=3&fclid=32e035c9-40b3-6284-08e3-26fe410d63b4&u=a1Lz9GT1JNPVo5RkQx&ntb=1
    
        
        //var pageNumber = myTable.page.info().page + 1; // Obtener el número de página actual
        //var pageLength = myTable.page.info().length;

      
      // Realizar una petición AJAX para o
      var todayDate = new Date();
      var options = { day: '2-digit', month: '2-digit', year: 'numeric' };
      var fechaActual = todayDate.toLocaleDateString('es-SV', options).split('/').reverse().join('-');

      if (!fecha_desde_p) {
        fecha_desde_p = fechaActual
      }
      
   
      if (!fecha_hasta_p) {
        fecha_hasta_p = fechaActual
      }
     
       
      var xhr = new XMLHttpRequest();
      //xhr.open('GET', '/dtesv/documentos/');
     // console.log(fecha_desde_p)
     // console.log(fecha_hasta_p)
      xhr.open('GET', '/dtesv/documentos/' + fecha_desde_p + '/' + fecha_hasta_p +'/'+empresaSeleccionada);
      showLoader();
      xhr.onload = function() {
        if (xhr.status === 200) {

      
          // Actualizar el contenido del contenedor con la respuesta del servidor
          documentosContainer.innerHTML = xhr.responseText;
          $('#myTable').DataTable(dataTableOptions);
         
       // agregarEventosPopup();
        agregarEventoShowData();
        sentDocumentMh();
        generatePDF();
        clickcelda();
        sentEmail();
        fixTableColumnWidth();
        edit_cliente();
        edit_document();
        upateInformacionLote();
        reprocess();
        generarPDFS(); 
        descargarArchivos();
        hideLoader();
        initializeColumnDropdown(defaultHiddenColumns);
         
      
         
         
        fecha_desde.value = fecha_desde_p;
        fecha_hasta.value = fecha_hasta_p;
        filtro_fecha();
        

        // Inicializar los filtros de búsqueda
        $('#myTable thead th').each(function() {
          var title = $(this).text();
          $(this).html(title + '<input type="text" class="form-control form-control-sm" placeholder="Buscar ' + title + '">');
        });

        // Aplicar la búsqueda en la tabla
        $('#myTable').DataTable().columns().every(function() {
          var column = this;
          $('input', this.header()).on('keyup change', function() {
            if (column.search() !== this.value) {
              column.search(this.value).draw();
            }
          });
        });
        
      } else {
        console.log('Error al cargar la tabla de documentos');
      }
    };
    xhr.send();
      }
    
 
      function cargarContingencias() {
        var xhr = new XMLHttpRequest();
          xhr.open('GET', '/dtesv/contingencias/');
          xhr.onload = function() {
            if (xhr.status === 200) {
              contingenciasContainer.innerHTML = xhr.responseText; // Actualizar el contenido del contenedor de gráficos
             
  
            //  var chart = createChart('anioActual');
              
               
            }
          };
    xhr.send();
      }

    function cargarDashboard() {
      var xhr = new XMLHttpRequest();
        xhr.open('GET', '/dtesv/dashboard/');
        xhr.onload = function() {
          if (xhr.status === 200) {
            dashboardContainer.innerHTML = xhr.responseText; // Actualizar el contenido del contenedor de gráficos
           

            var chart = createChart('mesActual');
            
             
          }
        };
  xhr.send();
    }




    
    function url_statusDte() {
      console.log("SI");
      var xhr = new XMLHttpRequest();
      xhr.open('GET', '/dtesv/urls_status/');
      xhr.onload = function() {
        if (xhr.status === 200) {
          dashboardContainer.insertAdjacentHTML('beforeend', xhr.responseText); // Adjunta el contenido al final del contenedor
          
          // Llama a la función para llenar la tabla con nombres
          urls_status("name");
        }
      };
      xhr.send();
    }
  // Agregar un evento click al enlace de documentos
  documentosLink.addEventListener('click', function(e) {
    e.preventDefault(); // Evitar la acción predeterminada del enlace
    
   
    cargarDocumentos();
    documentosContainer.style.display = 'block'; // Mostrar documentosContainer
    dashboardContainer.style.display = 'none';
    contingenciasContainer.style.display = 'none';
    
  
     
  });

  


  // Agregar un evento click al enlace de Dashboard
  contingeiasLInk.addEventListener('click', function(e) {
    e.preventDefault(); // Evitar la acción predeterminada del enlace
    //url_statusDte();
    cargarContingencias();
    contingenciasContainer.style.display = 'block';
    documentosContainer.style.display = 'none'; // Ocultar documentosContainer    
    dashboardContainer.style.display = 'none'; // Mostrar settingsContainer
   
   
  });

  
   // Agregar un evento click al enlace de Dashboard
   dashboardLink.addEventListener('click', function(e) {
    e.preventDefault(); // Evitar la acción predeterminada del enlace
    url_statusDte();
    cargarDashboard();

    dashboardContainer.style.display = 'block'; // Mostrar settingsContainer
    documentosContainer.style.display = 'none'; // Ocultar documentosContainer
    contingenciasContainer.style.display = 'none';
    
   
  });
  // Verificar si se debe cargar la tabla de documentos al cargar la página
 

  // Llamar a DataTables en $(document).ready()
  $(document).ready(function() {
    $('#myTable').DataTable(dataTableOptions);
   
   
   // fixTableColumnWidth();
   
    
     
     
});

function initializeColumnDropdown(defaultHiddenColumns) {
  var table = $('#myTable').DataTable();
  var columns = table.columns().header().to$();
  columns.each(function(index) {
      var columnTitle = $(this).text();
      var column = table.column(index);
      var columnOption = $('<a class="dropdown-item column-option" href="#" data-column="' + index + '">' + columnTitle + '</a>');
      if (defaultHiddenColumns.includes(index)) {
          column.visible(false);
          columnOption.addClass('column-hidden');
      }
      $('#columnDropdown').append(columnOption);
  });

  // Ocultar la lista desplegable inicialmente
  $('#columnDropdown').hide();

  // Mostrar u ocultar la lista desplegable al hacer clic en el botón
  $('#dropdownMenuButton').on('click', function() {
      $('#columnDropdown').toggle();
  });

  // Mostrar u ocultar columnas al hacer clic en una opción de la lista desplegable
  $('.column-option').on('click', function() {
      var columnIdx = $(this).data('column');
      var column = table.column(columnIdx);
      column.visible(!column.visible());
      $(this).toggleClass('column-hidden');
  });
}
  function filtro_fecha()
  {
    bt_busqueda = document.getElementById('busca_ids');
    
    var todayDate = new Date();
    var options = { day: '2-digit', month: '2-digit', year: 'numeric' };
    var fechaActual = todayDate.toLocaleDateString('es-SV', options).split('/').reverse().join('-');
    
    if (!fecha_desde.value) {
      fecha_desde.value = fechaActual;
    }
    if (!fecha_hasta.value) {
      fecha_hasta.value = fechaActual;
    }
    bt_busqueda.addEventListener('click', function() {
      // Obtener los valores de fecha_desde y fecha_hasta de los campos de fecha
      
       // console.log(fecha_desde.value)
       // console.log(fecha_hasta.value)
      // Llamar a la función cargarDocumentos con los valores de fecha
        cargarDocumentos(fecha_desde.value, fecha_hasta.value);
        bt_busqueda.click();
     });

  }
 
     
  function showLoader() {
    var loader = document.getElementById("loader");
    if (loader) {
      loader.style.display = "block";
    }
  }

  // Función para ocultar la imagen de carga
  function hideLoader() {
    document.getElementById("loader").style.display = "none";
  }

  // Función para fijar el ancho de la columna deseada
  function fixTableColumnWidth() {
    
    var fixedColumnIndex = 1;
    var table = document.getElementById('myTable');
     
     
   
    if (table) {
      var rows = table.rows;
     // console.log(rows);
      if(table.rows.length >2)
      {
      for (var i = 0; i < rows.length; i++) {
        var cell = rows[i].cells[fixedColumnIndex];
        
        cell.classList.add('fixed-column');
        cell.addEventListener('click', function() {
        this.classList.toggle('column-expanded');
        });
      }
    }
    }
  }

  function clickcelda()
  {
    $(document).on('click', '#myTable td', function() {
      var columnIndex = $(this).index();
      var cellText = $(this).text();
      var columnName = $('#myTable th').eq(columnIndex).text();
      
  
      if (columnName != "Opciones del Documento")
        {
          var infoText =  columnName + ' : ' + cellText;
          mostrarDatosEnPopup(infoText,"view");
        }
      // Realiza las acciones que necesites con la información de la columna y la celda
    });


  }

  function agregarEventosPopup() {
    
    var dataTable = $('#myTable').DataTable();
    var totalRowCount  = dataTable.rows.length;
    

    dataTable.on('draw', function() {
      dataTable.rows().every(function() {
        var row = this.node();
        
        var cell = row.cells[8]; // Reemplaza el índice 7 con el índice correcto de la columna "Observaciones MH"
        
        if (cell.classList.contains('truncate-text')) {
          var fullText = cell.textContent;
  
          if (fullText.length > 5) {
            cell.classList.add('truncated');
            cell.addEventListener('click', function() {
              var overlayContent = document.getElementById('overlay-content');
              overlayContent.textContent = fullText;
              $('#myModal').modal('show'); // Mostrar el modal
            });
          }
        }
      });
    });
  }  
  
  

  function agregarEventoShowData() {
    

    $('#myTable tbody').on('click', 'button#show_data', function() {
      var rowData = $(this).closest('tr').find('td'); // Obtener todas las celdas de la fila
      var documentId = rowData.eq(3).text(); 
      fetch('/dtesv/documentos/' + documentId)
      .then(response => response.json())
      .then(data => {
        // Aquí puedes hacer lo que necesites con los datos del documento
       // console.log(data);
        // Mostrar los datos en un cuadro de diálogo o superposición
        mostrarDatosEnPopup(data,"view");
      })
      .catch(error => {
        console.log('Error al obtener los datos del documento:', error);
      });
  });
  }
  function sentDocumentMh() {
    var csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    $('#myTable tbody').on('click', 'button#sent_mh', function() {
      var rowData = $(this).closest('tr').find('td'); // Obtener todas las celdas de la fila
      
      var plianIcon = $(this).find('i');
      plianIcon.removeClass('fa-solid fa-paper-plane').addClass('fa fa-refresh fa-spin');
          // Obtener los encabezados de columna
      var columnHeaders = $('#myTable thead th').map(function() {
        return $(this).text();
      }).get();

      // Definir el nombre de la columna que deseas buscar
      var nombreColumna = 'Codigo de Generacion';

      // Verificar si el nombre de la columna existe en los encabezados
      var columnIndex = columnHeaders.indexOf(nombreColumna);
      if (columnIndex !== -1) {
        var documentId = rowData.eq(columnIndex).text();

        // Realizar las operaciones que necesites con el valor de la celda
        // ...
      } else {
        console.log("La columna '" + nombreColumna + "' no existe en la tabla.");
      }



      
      var documentId = rowData.eq(3).text();
      //console.log(documentId);
      var postData = {       
        codigoGen: documentId,
        fecha_desde: fecha_desde,
        fecha_hasta: fecha_hasta
    };
      fetch('/dtesv/process_data/' + documentId + '/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
          },
          body: JSON.stringify({ codigoGen: documentId })
        })
        .then(response => response.json())
        .then(data => {
          // Hacer algo con la respuesta de la API
         // alert(data.message);
         plianIcon.removeClass('fa fa-refresh fa-spin').addClass('fa-solid fa-paper-plane');
          mostrarDatosEnPopup(data,"process");
         
          
          
        })
        
        .catch(error => {
          console.log(error);
          console.error('Error al procesar los datos:', error);
        });
    });

  }

  function edit_cliente() {
    var csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    $('#myTable tbody').on('click', 'button#edit_cliente', function() {
      var rowData = $(this).closest('tr').find('td'); // Obtener todas las celdas de la fila
      
      var plianIcon = $(this).find('i');
      //plianIcon.removeClass('fa-solid fa-paper-plane').addClass('fa fa-refresh fa-spin');
          // Obtener los encabezados de columna
      var columnHeaders = $('#myTable thead th').map(function() {
        return $(this).text();
      }).get();

      // Definir el nombre de la columna que deseas buscar
      var nombreColumna = 'Codigo de Generacion';

      // Verificar si el nombre de la columna existe en los encabezados
      var columnIndex = columnHeaders.indexOf(nombreColumna);
      if (columnIndex !== -1) {
        var documentId = rowData.eq(columnIndex).text();

        // Realizar las operaciones que necesites con el valor de la celda
        // ...
      } else {
        console.log("La columna '" + nombreColumna + "' no existe en la tabla.");
      }


      
      
      var documentId = rowData.eq(3).text();
      //console.log(documentId);
      var postData = {       
        codigoGen: documentId,
        fecha_desde: fecha_desde,
        fecha_hasta: fecha_hasta
    };
      fetch('/dtesv/get_receptor/' + documentId + '/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
          },
          body: JSON.stringify({ codigoGen: documentId })
        })
        .then(response => response.json())
        .then(data => {
          // Hacer algo con la respuesta de la API
         // alert(data.message);
         //plianIcon.removeClass('fa fa-refresh fa-spin').addClass('fa-solid fa-paper-plane');
         // mostrarDatosEnPopup(data,"process");
         console.log(data);
         editar_cliente(data.message);
          
          
        })
        
        .catch(error => {
          console.log(error);
          console.error('Error al procesar los datos:', error);
        });
    });

  }
  function editar_cliente(codigocliente) {
    // Realizar una solicitud AJAX o llamar a un método en tu backend
    // para obtener el código de cliente a partir del "codigoGeneracion"
    var currentDomain = window.location.hostname;
    
    var port = window.location.port ? ':' + window.location.port : '';
    console.log(currentDomain+port);
    // Una vez que tengas el código de cliente, abre la ventana emergente
    var url = "http://"+currentDomain+port+"/dtesv/editar-receptor/" + codigocliente +"/";
    abrirVentanaEmergente(url);
  }
  function edit_document() {
    var csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    $('#myTable tbody').on('click', 'button#edit_documento', function() {
      var rowData = $(this).closest('tr').find('td'); // Obtener todas las celdas de la fila
      
      var plianIcon = $(this).find('i');
      //plianIcon.removeClass('fa-solid fa-paper-plane').addClass('fa fa-refresh fa-spin');
          // Obtener los encabezados de columna
      var columnHeaders = $('#myTable thead th').map(function() {
        return $(this).text();
      }).get();

      // Definir el nombre de la columna que deseas buscar
      var nombreColumna = 'Codigo de Generacion';

      // Verificar si el nombre de la columna existe en los encabezados
      var columnIndex = columnHeaders.indexOf(nombreColumna);
      if (columnIndex !== -1) {
        var documentId = rowData.eq(columnIndex).text();

        // Realizar las operaciones que necesites con el valor de la celda
        // ...
      } else {
        console.log("La columna '" + nombreColumna + "' no existe en la tabla.");
      }



      
      var documentId = rowData.eq(3).text();
      //console.log(documentId);
       
      
      editar_documento(documentId);
          
          
      
    });

  }
  function editar_documento(codigoGeneracion) {
    // Realizar una solicitud AJAX o llamar a un método en tu backend
    // para obtener el código de cliente a partir del "codigoGeneracion"
  
    // Una vez que tengas el código de cliente, abre la ventana emergente
    var currentDomain = window.location.hostname;
    
    var port = window.location.port ? ':' + window.location.port : '';
    console.log(currentDomain+port);
    var url = "http://"+currentDomain+port+"/dtesv/editar_documentos/" + codigoGeneracion +"/";
    abrirVentanaEmergente(url);
  }
  
  function abrirVentanaEmergente(url) {
    window.open(url, "popup", "width=600,height=400,scrollbars=yes");
  }
  
  
  function mostrarDatosEnPopup(data, eventType) {
    var jsonContainer = document.getElementById('jsonContainer');
  
    if (data && data.message) {
      jsonContainer.innerHTML = data.message;
    } else {
      jsonContainer.innerHTML = JSON.stringify(data, null, 2);
    }
  
    $('#Modal_json').modal('show');
  
    $('#Modal_json').on('hidden.bs.modal', function () {
      if (data && data.message) {
        // cargarDocumentos(fecha_desde,fecha_hasta);
      }
      if (eventType === 'process') {
        bt_busqueda.click();
        //console.log('Hola puto')
        // location.reload();
        // Realiza acciones específicas si se llamó desde el evento 'process'
        // cargarDocumentos(fecha_desde, fecha_hasta);
      }
    });
  }
  
  
  

  function generatePDF() {
    var csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    $('#myTable').on('click', 'button#pdf_gen', function() {
      var rowData = $(this).closest('tr').find('td');
      var documentId = rowData.eq(3).text();
  
      var pdfIcon = $(this).find('i');
      pdfIcon.removeClass('fa-file-pdf').addClass('fa-spinner fa-spin');
  
      fetch('/dtesv/generar_pdf/' + documentId + '/', {
        method: 'GET',
        headers: {
          'X-CSRFToken': csrfToken
        }
      })
        .then(response => response.blob())
        .then(blob => {
          const pdfUrl = URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = pdfUrl;
          a.download = documentId + '.pdf';
          a.style.display = 'none';
          document.body.appendChild(a);
          a.click();
          document.body.removeChild(a);
          URL.revokeObjectURL(pdfUrl);
  
          pdfIcon.removeClass('fa-spinner fa-spin').addClass('fa-file-pdf');
        })
        .catch(error => {
          console.error('Error al generar el PDF:', error);
          pdfIcon.removeClass('fa-spinner fa-spin').addClass('fa-file-pdf');
        });
    });
  }

  function upateInformacionLote() {
    var csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    $('#myTable').on('click', 'button#update_lote', function() {
      //var rowData = $(this).closest('tr').find('td');
      var documentId = null;
  
      var cubeIcon = $(this).find('i');
      cubeIcon.removeClass('fa-cubes').addClass('fa-spinner fa-spin');
  
      fetch('/dtesv/upadate_lote_data/' + documentId + '/', {
        method: 'GET',
        headers: {
          'X-CSRFToken': csrfToken
        }
      })
        .then(response => response.blob())
        .then(blob => {          
  
          cubeIcon.removeClass('fa-spinner fa-spin').addClass('fa-cubes');
        })
        .catch(error => {
          console.error('Error al generar el PDF:', error);
          cubeIcon.removeClass('fa-spinner fa-spin').addClass('fa-cubes');
        });
    });
  }



  function sentEmail() {
    var csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    $('#myTable tbody').on('click', 'button#sent_email', function() {
      var rowData = $(this).closest('tr').find('td'); // Obtener todas las celdas de la fila
      //console.log('hola')
      var plianIcon = $(this).find('i');
      plianIcon.removeClass('fa fa-envelope').addClass('fa fa-refresh fa-spin');
          // Obtener los encabezados de columna
      var columnHeaders = $('#myTable thead th').map(function() {
        return $(this).text();
      }).get();

      // Definir el nombre de la columna que deseas buscar
      var nombreColumna = 'Codigo de Generacion';
      //console.log(nombreColumna)
      // Verificar si el nombre de la columna existe en los encabezados
      var columnIndex = columnHeaders.indexOf(nombreColumna);
      if (columnIndex !== -1) {
        var documentId = rowData.eq(columnIndex).text();

        // Realizar las operaciones que necesites con el valor de la celda
        // ...
      } else {
        console.log("La columna '" + nombreColumna + "' no existe en la tabla.");
      }




      var documentId = rowData.eq(3).text();

      fetch('/dtesv/sentemail/' + documentId + '/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
          },
          body: JSON.stringify({ codigoGen: documentId })
        })
        .then(response => response.json())
        .then(data => {
          // Hacer algo con la respuesta de la API
         // alert(data.message);
         plianIcon.removeClass('fa fa-refresh fa-spin').addClass('fa fa-envelope');
          mostrarDatosEnPopup(data,"view");
          //alert(data.message);
          //console.log(data.message);
          
        })
        
        .catch(error => {
          console.error('Error al enviar Email:', error);
        });
    });

  }
  
 
   function sentEmail() {
    var csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    $('#myTable tbody').on('click', 'button#sent_email', function() {
      var rowData = $(this).closest('tr').find('td'); // Obtener todas las celdas de la fila
      //console.log('hola')
      var plianIcon = $(this).find('i');
      plianIcon.removeClass('fa fa-envelope').addClass('fa fa-refresh fa-spin');
          // Obtener los encabezados de columna
      var columnHeaders = $('#myTable thead th').map(function() {
        return $(this).text();
      }).get();

      // Definir el nombre de la columna que deseas buscar
      var nombreColumna = 'Codigo de Generacion';
      //console.log(nombreColumna)
      // Verificar si el nombre de la columna existe en los encabezados
      var columnIndex = columnHeaders.indexOf(nombreColumna);
      if (columnIndex !== -1) {
        var documentId = rowData.eq(columnIndex).text();

        // Realizar las operaciones que necesites con el valor de la celda
        // ...
      } else {
        console.log("La columna '" + nombreColumna + "' no existe en la tabla.");
      }




      var documentId = rowData.eq(3).text();

      fetch('/dtesv/sentemail/' + documentId + '/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
          },
          body: JSON.stringify({ codigoGen: documentId })
        })
        .then(response => response.json())
        .then(data => {
          // Hacer algo con la respuesta de la API
         // alert(data.message);
         plianIcon.removeClass('fa fa-refresh fa-spin').addClass('fa fa-envelope');
          mostrarDatosEnPopup(data,"view");
          //alert(data.message);
          //console.log(data.message);
          
        })
        
        .catch(error => {
          console.error('Error al enviar Email:', error);
        });
    });

  }
  
 


  var hash = window.location.hash;
  if (hash === '#documentos') {
    cargarDocumentos();
    
    documentosContainer.style.display = 'block'; // Mostrar documentosContainer
    dashboardContainer.style.display = 'none';
    contingenciasContainer.style.display = 'none'; // Mostrar settingsContainer
  //  settingsContainer.style.display = 'none'; // Ocultar settingsContainer
 /* } else if (hash === '#settings') {
    cargarSettings();
    documentosContainer.style.display = 'none'; // Ocultar documentosContainer
    dashboardContainer.style.display = 'none';
    settingsContainer.style.display = 'block'; // Mostrar settingsContainer
    */
  }
  else if (hash === '#dashboard') {
      url_statusDte();
      cargarDashboard();
  
  contingenciasContainer.style.display = 'none'; // Mostrar settingsContainer
  documentosContainer.style.display = 'none'; // Ocultar documentosContainer  
 // settingsContainer.style.display = 'none'; // Mostrar settingsContainer
  dashboardContainer.style.display = 'block';
}
else if (hash === '#contingencias' )
{

  documentosContainer.style.display = 'none'; // Ocultar documentosContainer  
 // settingsContainer.style.display = 'none'; // Mostrar settingsContainer
  dashboardContainer.style.display = 'none';
  contingenciasContainer.style.display = 'block';


}
window.cambiarEmpresa = cambiarEmpresa
// Evento para detectar el cambio en el select de empresas
function reprocess()
      {
      reprocessButton =   document.getElementById('reprocess');
      //  console.log(reprocessButton);
      if(reprocessButton)  
      {
      //var reprocessButton = document.getElementById('reprocess');
      reprocessButton.addEventListener('click', function() {
        var csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
        // Obtener las fechas desde los campos de fecha
        //var fecha_desde = document.getElementById('fecha_desde').value;
        //var fecha_hasta = document.getElementById('fecha_hasta').value;
        console.log("DM");
  
        // Realizar una petición AJAX al servidor para ejecutar la vista correspondiente
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/dtesv/reprocess_data/' + fecha_desde.value + '/' + fecha_hasta.value + '/', true);
        xhr.setRequestHeader('Content-Type', 'application/json' );
        xhr.setRequestHeader('X-CSRFToken', csrfToken);
        xhr.onreadystatechange = function() {
          if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
              // La solicitud fue exitosa, puedes manejar la respuesta aquí
              var response = JSON.parse(xhr.responseText);
              console.log(response); 
              mostrarDatosEnPopup(response,"process");// Mostrar la respuesta en la consola
              // Puedes hacer más cosas con la respuesta, dependiendo de tus necesidades
            } else {
              // La solicitud falló
              console.error('Error al ejecutar la vista:', xhr.status);
            }
          }
        };
  
        // Enviar los datos al servidor (fechas)
        var data = {
          fecha_desde: fecha_desde,
          fecha_hasta: fecha_hasta
        };
        xhr.send(JSON.stringify(data));
      });}
    }

    // PARA GENERERAR TODOS LOS PDF FILTRADOS =============================================================================================================
function obtenerCodigosGeneracionFiltrados() {
  // Obtener la instancia de DataTable
      var dataTable = $('#myTable').DataTable();

      // Obtener los datos solo de las filas visibles después de aplicar los filtros
      var codigosGeneracionArray = dataTable.rows({ search: 'applied' }).data().toArray();

      var codigosGeneracion = codigosGeneracionArray.map(function(row) {
        return row[3]; // Ajusta el índice si es necesario (ten en cuenta que JavaScript usa índices basados en cero)
      });
      // Devolver el array de códigosGeneracion
      return codigosGeneracion;
}

function generarPDFS() {
  GnerarPDFSButton = document.getElementById('generarPDFS');
  if (GnerarPDFSButton) {
      GnerarPDFSButton.addEventListener('click', function () {
          var csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
          codigosGeneracionFiltrados = obtenerCodigosGeneracionFiltrados();
          //console.log('CódigosGeneracion filtrados:', codigosGeneracionFiltrados);
          var nombreUsuario = document.getElementById('nombreUsuario').textContent;
          var now = new Date();
          var fecha = now.getFullYear() + '_' + ('0' + (now.getMonth() + 1)).slice(-2) + '_' + ('0' + now.getDate()).slice(-2);

          var datos = {
              'codigosGeneracion': codigosGeneracionFiltrados,
              'company': empresaSeleccionada
              // Agrega más campos según sea necesario
          };

          fetch('/dtesv/generarPDFS/', {
              method: 'POST',
              headers: {
                  'X-CSRFToken': csrfToken
              },
              body: JSON.stringify(datos)
          })
          .then(response => {
              // Verificar si la respuesta indica un error
              if (!response.ok) {
                 mostrarDatosEnPopup('No existen documentos',"view");
                  throw new Error('No existen documentos');
              }
              return response.blob();
          })
          .then(blob => {
              const pdfUrl = URL.createObjectURL(blob);
              const a = document.createElement('a');
              a.href = pdfUrl;
              
              a.download = nombreUsuario + '_' + fecha + '.pdf';
              a.style.display = 'none';
              document.body.appendChild(a);
              a.click();
              document.body.removeChild(a);
              URL.revokeObjectURL(pdfUrl);
          })
          .catch(error => {
              // Manejar el mensaje de error
              console.error('Error al generar el PDF:', error.message);
          });
      });
  }
}



function descargarArchivos() {
  var csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
  $('#myTable tbody').on('click', 'button#download_docs', function() {
    var rowData = $(this).closest('tr').find('td'); // Obtener todas las celdas de la fila
    var plianIcon = $(this).find('i');
    plianIcon.removeClass('fa-solid fa-download').addClass('fa fa-refresh fa-spin');

    // Obtener los encabezados de columna
    var columnHeaders = $('#myTable thead th').map(function() {
      return $(this).text();
    }).get();

    // Definir el nombre de la columna que deseas buscar
    var nombreColumna = 'Codigo de Generacion';

    // Verificar si el nombre de la columna existe en los encabezados
    var columnIndex = columnHeaders.indexOf(nombreColumna);
    if (columnIndex !== -1) {
      var documentId = rowData.eq(columnIndex).text();

      // Realizar las operaciones que necesites con el valor de la celda
      // ...

      fetch('/dtesv/api/download-files/' + documentId, {
          method: 'GET',
          headers: {
            'X-CSRFToken': csrfToken
          },
        })
        .then(response => {
          // Verificar si la respuesta indica un error
          if (!response.ok) {
            mostrarDatosEnPopup('No existen documentos', "view");
            throw new Error('No existen documentos');
          }
          return response.blob();
        })
        .then(blob => {
          const zipUrl = URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = zipUrl;
          a.download = documentId + '_archivos.zip'; // Cambiar el nombre del archivo ZIP según sea necesario
          plianIcon.removeClass('fa fa-refresh fa-spin').addClass('fa-solid fa-download');
          a.style.display = 'none';
          document.body.appendChild(a);
          a.click();
          document.body.removeChild(a);
          URL.revokeObjectURL(zipUrl);
        })
        .catch(error => {
          // Manejar el mensaje de error
          console.error('Error al descargar el ZIP:', error.message);
        });
    } else {
      console.log("La columna '" + nombreColumna + "' no existe en la tabla.");
    }
  });
}

    //=================================================================================================================================================
     
});

 


  
  
  
 


function obtenerDatosTabla() {
  // Obtener la referencia a la tabla DataTable
  var dataTable = $('#myTable').DataTable();

  // Obtener los datos de la tabla
  var data = dataTable.rows().data(); // Esto obtiene todos los datos de todas las filas

  // Convertir los datos en un formato adecuado para la exportación a Excel
  var tableData = [];

  // Recorrer los datos y construir una matriz para la exportación
  data.each(function(row) {
    var rowData = [];

    // Recorrer cada celda de la fila y agregar su valor a la matriz
    row.forEach(function(cellData) {
      rowData.push(cellData); // Agregar el valor de la celda a la fila
    });

    tableData.push(rowData); // Agregar la fila a los datos de la tabla
  });

  return tableData;
}

