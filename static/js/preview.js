document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('file-input');
    const uploadArea = document.getElementById('upload-area');
    const uploadText = document.querySelector('.upload-text');
    const themeCards = document.querySelectorAll('.theme-card');
    const generateBtn = document.getElementById('generate-btn');
    const form = document.getElementById('generator-form');
    
    const resultsArea = document.getElementById('results-area');
    const loaderContainer = document.getElementById('loader-container');
    const meterFill = document.querySelector('.meter-fill');
    
    let selectedFile = null;
    let selectedTheme = 'modern';
    
    // Drag & Drop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });
    
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        
        if (e.dataTransfer.files.length) {
            handleFileSelect(e.dataTransfer.files[0]);
        }
    });
    
    // Click to upload
    uploadArea.addEventListener('click', () => {
        fileInput.click();
    });
    
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length) {
            handleFileSelect(e.target.files[0]);
        }
    });
    
    function handleFileSelect(file) {
        selectedFile = file;
        uploadText.textContent = file.name;
        updateGenerateBtn();
    }
    
    // Theme Selection
    themeCards.forEach(card => {
        card.addEventListener('click', () => {
            // Remove selected class from all
            themeCards.forEach(c => c.classList.remove('selected'));
            
            // Add to clicked
            card.classList.add('selected');
            selectedTheme = card.dataset.theme;
        });
    });
    
    function updateGenerateBtn() {
        generateBtn.disabled = !selectedFile;
    }
    
    // Form Submission
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        if (!selectedFile) return;
        
        // UI Updates
        generateBtn.disabled = true;
        resultsArea.style.display = 'none';
        loaderContainer.style.display = 'block';
        
        const formData = new FormData();
        formData.append('resume', selectedFile);
        formData.append('theme', selectedTheme);
        
        try {
            const response = await fetch('/generate', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (data.success) {
                // Show results
                loaderContainer.style.display = 'none';
                resultsArea.style.display = 'block';
                
                // Animate completeness meter
                setTimeout(() => {
                    meterFill.style.width = `${data.completeness}%`;
                }, 100);
            } else {
                alert('Generation failed: ' + data.error);
                loaderContainer.style.display = 'none';
                generateBtn.disabled = false;
            }
        } catch (error) {
            alert('An error occurred during generation.');
            console.error(error);
            loaderContainer.style.display = 'none';
            generateBtn.disabled = false;
        }
    });
});
