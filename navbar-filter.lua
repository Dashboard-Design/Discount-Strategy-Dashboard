-- navbar-filter.lua
function Meta(meta)
  quarto.doc.include_text("after-body", [[
<script>
document.addEventListener('DOMContentLoaded', function() {
  setTimeout(function() {
    var navbarContainer = document.querySelector('.navbar-container');
    if (navbarContainer) {
      var buttonsHtml = '<div class="navbar-buttons" style="display:flex;gap:15px;margin-left:auto!important;">';
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
  // Find the hidden Shiny download button and trigger it
  var shinyDownloadBtn = document.getElementById('navbar_download');
  if (shinyDownloadBtn) {
    // Trigger the download
    shinyDownloadBtn.click();
  } else if (window.Shiny) {
    // Fallback: use Shiny input if button not found
    Shiny.setInputValue('navbar_export', Date.now());
  } else {
    alert('Export functionality requires Shiny connection');
  }
}



function handleInfo() {
  if (!document.getElementById('infoModal')) {
    var modalHtml = [
      '<div class="modal fade" id="infoModal" tabindex="-1" style="z-index:1060;">',
      '  <div class="modal-dialog modal-lg">',
      '    <div class="modal-content">',
      '      <div class="modal-header bg-primary text-white">',
      '        <h5 class="modal-title"><i class="bi bi-info-circle"></i> Dashboard Guide</h5>',
      '        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>',
      '      </div>',
      '      <div class="modal-body">',
      '        <div class="row">',
      '          <div class="col-md-6">',
      '            <h6><i class="bi bi-funnel"></i> How to Use Filters</h6>',
      '            <div class="card mb-3">',
      '              <div class="card-body">',
      '                <p><strong>1. Select Region & Year</strong><br>Choose geographic area and time period for analysis.</p>',
      '                <p><strong>2. Set Business Goal</strong><br>',
      '                   &bull; Revenue Growth: Focus on expanding sales<br>',
      '                   &bull; Profit Protection: Maintain profitability<br>',
      '                   &bull; Market Share: Increase market presence<br>',
      '                   &bull; Customer Retention: Keep existing customers</p>',
      '                <p><strong>3. Choose Customer Priority</strong><br>Target specific customer segments for discount strategies.</p>',
      '              </div>',
      '            </div>',
      '            <h6><i class="bi bi-lightbulb"></i> Understanding the Table</h6>',
      '            <div class="card">',
      '              <div class="card-body">',
      '                <p><strong>Rank:</strong> Performance ranking within category based on Revenue.</p>',
      '                <p><strong>YoY Revenue %:</strong> Year-over-year growth (&#9650;) or decline (&#9660;).</p>',
      '                <p><strong>Discount %:</strong> Current discount level.</p>',
      '              </div>',
      '            </div>',
      '          </div>',
      '          <div class="col-md-6">',
      '            <h6><i class="bi bi-graph-up"></i> Key Metrics Explained</h6>',
      '            <div class="card mb-3">',
      '              <div class="card-body">',
      '                <p><strong>Elasticity Proxy (indicator)</strong><br>',
      '                Measures how price changes affect demand:<br>',
      '                &bull; <span style="color:green">&gt; 0.5</span>: High sensitivity - discounts boost sales<br>',
      '                &bull; <span style="color:grey">0 to 0.5</span>: Moderate sensitivity<br>',
      '                &bull; <span style="color:red">&lt; 0</span>: Low sensitivity - other factors matter more</p>',
      '                <p><strong>Discount Strategy Logic</strong><br>',
      '                Recommendations based on:<br>',
      '                &bull; Revenue trends and growth patterns<br>',
      '                &bull; Price elasticity measurements<br>',
      '                &bull; Profit margin considerations<br>',
      '                &bull; Strategic business objectives</p>',
      '              </div>',
      '            </div>',
      '            <h6><i class="bi bi-bar-chart"></i> Interpreting Results</h6>',
      '            <div class="card">',
      '              <div class="card-body">',
      '                <p><strong>Increase Discount When:</strong><br>',
      '                &bull; High elasticity (&gt;0.5) AND<br>',
      '                &bull; Positive growth trends AND<br>',
      '                &bull; Goal is revenue growth</p>',
      '                <p><strong>Maintain/Reduce Discount When:</strong><br>',
      '                &bull; Low elasticity (&lt; 0) OR<br>',
      '                &bull; Negative profit impact OR<br>',
      '                &bull; Goal is profit protection</p>',
      '              </div>',
      '            </div>',
      '          </div>',
      '        </div>',
      '        <div class="alert alert-info mt-3">',
      '          <h6><i class="bi bi-clock"></i> Quick Start Guide</h6>',
      '          <ol>',
      '            <li>Select your target region and year</li>',
      '            <li>Choose your primary business goal</li>',
      '            <li>Set customer segment priority</li>',
      '            <li>Review the discount strategy recommendations</li>',
      '            <li>Use export feature to save results</li>',
      '          </ol>',
      '        </div>',
      '        <div class="text-center text-muted small">',
      '          <hr>',
      '          <p>Developed by Sajjad Ahmadi | Data-driven discount optimization tool</p>',
      '        </div>',
      '      </div>',
      '      <div class="modal-footer">',
      '        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>',
      '        <button type="button" class="btn btn-primary" onclick="handleExport()">',
      '          <i class="bi bi-download"></i> Export Current View',
      '        </button>',
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

/* Modal enhancements */
.modal-lg {
  max-width: 900px;
}

.card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
}

.card-body {
  padding: 1.25rem;
}

.alert-info {
  background-color: #e7f3ff;
  border-color: #b3d9ff;
  color: #333;
}

.bg-primary {
  background-color: #007bff !important;
}

.modal-body h6 {
  color: #2c3e50;
  margin-top: 1rem;
  margin-bottom: 0.5rem;
}

.modal-body p {
  margin-bottom: 0.5rem;
}
</style>
  ]])
end
