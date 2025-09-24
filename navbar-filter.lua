-- navbar-filter.lua
function Meta(meta)
  quarto.doc.include_text("after-body", [[
<script>
document.addEventListener('DOMContentLoaded', function() {
  setTimeout(function() {
    var navbarContainer = document.querySelector('.navbar-container');
    if (navbarContainer) {
      var buttonsHtml = '<div class="navbar-buttons" style="display:flex;gap:10px;margin-left:auto!important;">';
      buttonsHtml += '<button class="btn btn-outline-light btn-sm" onclick="handleExport()">';
      buttonsHtml += '<i class="bi bi-download"></i> Export';
      buttonsHtml += '</button>';
      buttonsHtml += '<button class="btn btn-outline-light btn-sm" onclick="handleInfo()">';
      buttonsHtml += '<i class="bi bi-info-circle"></i> Info';
      buttonsHtml += '</button>';
      buttonsHtml += '</div>';
      
      var collapseDiv = navbarContainer.querySelector('#dashboard-collapse');
      if (collapseDiv) {
        collapseDiv.insertAdjacentHTML('beforebegin', buttonsHtml);
      }
    }
  }, 100);
});

function handleExport() {
  if (window.Shiny) {
    Shiny.setInputValue('navbar_export', Date.now());
  } else {
    alert('Export functionality requires Shiny connection');
  }
}

function handleInfo() {
  if (!document.getElementById('infoModal')) {
    var modalHtml = [
      '<div class="modal fade" id="infoModal" tabindex="-1">',
      '  <div class="modal-dialog modal-dialog-centered">',
      '    <div class="modal-content">',
      '      <div class="modal-header">',
      '        <h5 class="modal-title">Dashboard Information</h5>',
      '        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>',
      '      </div>',
      '      <div class="modal-body">',
      '        <h6>Filters Section</h6>',
      '        <ul>',
      '          <li><strong>Region:</strong> Geographic filtering</li>',
      '          <li><strong>Year:</strong> Reporting period</li>',
      '          <li><strong>Goal:</strong> Business objective</li>',
      '          <li><strong>Priority:</strong> Customer segments</li>',
      '        </ul>',
      '        <h6>Developed by Sajjad Ahmadi</h6>',
      '      </div>',
      '      <div class="modal-footer">',
      '        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>',
      '      </div>',
      '    </div>',
      '  </div>',
      '</div>'
    ].join('');
    document.body.insertAdjacentHTML('beforeend', modalHtml);
  }
  
  var modal = new bootstrap.Modal(document.getElementById('infoModal'));
  modal.show();
}
</script>

<style>
.navbar-buttons {
  margin-left: auto !important;
}
</style>
  ]])
end