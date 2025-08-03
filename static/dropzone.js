// Dropzone functionality
function initializeDropzone() {
    const dropzoneOverlay = document.getElementById('dropzoneOverlay');
    const fileInput = document.getElementById('file-upload');
    let dropzoneActive = false;

    function showDropzone() {
        dropzoneOverlay.style.display = 'flex';
        dropzoneActive = true;
    }
    
    function hideDropzone() {
        dropzoneOverlay.style.display = 'none';
        dropzoneActive = false;
    }

    window.addEventListener('dragover', function(e) {
        e.preventDefault();
        if (!dropzoneActive) showDropzone();
    });
    
    window.addEventListener('dragleave', function(e) {
        if (e.target === document.body || e.pageX <= 0 || e.pageY <= 0) {
            hideDropzone();
        }
    });
    
    window.addEventListener('drop', function(e) {
        e.preventDefault();
        hideDropzone();
        if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
            fileInput.files = e.dataTransfer.files;
            fileInput.dispatchEvent(new Event('change'));
        }
    });
}

// File upload functionality
function enableSubmitButton() {
    const fileInput = document.getElementById('file-upload');
    const submitButton = document.getElementById('submit-button');
    submitButton.disabled = !fileInput.value;
}

function initializeFileUpload() {
    document.getElementById('file-upload').addEventListener('change', function(e) {
        var fileName = e.target.files.length ? e.target.files[0].name : '';
        document.getElementById('filenameDisplay').textContent = fileName;
    });
}

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeDropzone();
    initializeFileUpload();
}); 