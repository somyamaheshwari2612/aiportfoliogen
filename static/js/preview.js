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
    uploadArea.addEventListener('dragenter', (e) => {
        e.preventDefault();
    });

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
            fileInput.files = e.dataTransfer.files; // Sync to native input
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
        document.getElementById('results-container').style.display = 'block';
        resultsArea.style.display = 'none';
        
        const errorContainer = document.getElementById('error-container');
        if (errorContainer) errorContainer.style.display = 'none';
        
        loaderContainer.style.display = 'block';
        
        // Scroll to the results container smoothly
        document.getElementById('results-container').scrollIntoView({ behavior: 'smooth', block: 'start' });
        
        // Dynamic Loading State
        const loadingText = document.getElementById('loading-text');
        const loadingDots = document.getElementById('loading-dots');
        const loadingSteps = [
            { text: "Parsing Resume", dots: "●●●●○" },
            { text: "Calling Gemini", dots: "○●●●●" },
            { text: "Structuring Data", dots: "○○●●●" },
            { text: "Applying Design", dots: "○○○●●" },
            { text: "Rendering HTML", dots: "○○○○●" }
        ];
        
        let stepIndex = 0;
        
        if (loadingText) loadingText.textContent = loadingSteps[0].text;
        if (loadingDots) loadingDots.textContent = loadingSteps[0].dots;
        
        const loadingInterval = setInterval(() => {
            stepIndex = (stepIndex + 1) % loadingSteps.length;
            if (loadingText) loadingText.textContent = loadingSteps[stepIndex].text;
            if (loadingDots) loadingDots.textContent = loadingSteps[stepIndex].dots;
        }, 1000);
        
        const formData = new FormData();
        formData.append('resume', selectedFile);
        formData.append('theme', selectedTheme);
        
        try {
            const response = await fetch('/generate', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            clearInterval(loadingInterval);
            
            if (data.success) {
                // Show results after a tiny delay so they see 100%
                setTimeout(() => {
                    loaderContainer.style.display = 'none';
                    document.getElementById('error-container').style.display = 'none';
                    resultsArea.style.display = 'block';
                    resultsArea.classList.add('active');
                    generateBtn.disabled = false; // Re-enable button for regeneration
                    
                    // Animate completeness meter
                    const completenessRing = document.getElementById('completeness-ring');
                    const completenessText = document.getElementById('completeness-text');
                    
                    if (completenessRing && completenessText) {
                        const targetCompleteness = data.completeness || 82; // Fallback to 82 for demo
                        const circumference = 327; // 2 * PI * r (52)
                        
                        setTimeout(() => {
                            const offset = circumference - (targetCompleteness / 100) * circumference;
                            completenessRing.style.strokeDashoffset = offset;
                            
                            // Animate number count up
                            let currentNumber = 0;
                            const duration = 1500;
                            const interval = 30;
                            const step = targetCompleteness / (duration / interval);
                            
                            const counter = setInterval(() => {
                                currentNumber += step;
                                if (currentNumber >= targetCompleteness) {
                                    currentNumber = targetCompleteness;
                                    clearInterval(counter);
                                }
                                completenessText.textContent = Math.round(currentNumber) + '%';
                            }, interval);
                        }, 100);
                    }
                    
                    // Dynamically populate missing items
                    const missingContainer = document.getElementById('missing-items-container');
                    const missingList = document.getElementById('missing-items-list');
                    missingList.innerHTML = '';
                    
                    if (data.missing && data.missing.length > 0) {
                        data.missing.forEach(item => {
                            const li = document.createElement('li');
                            li.style.marginBottom = '0.5rem';
                            li.textContent = '• ' + item;
                            missingList.appendChild(li);
                        });
                        missingContainer.style.display = 'block';
                    } else {
                        missingContainer.style.display = 'none';
                    }
                }, 400);
            } else {
                loaderContainer.style.display = 'none';
                resultsArea.style.display = 'none';
                const errorContainer = document.getElementById('error-container');
                document.getElementById('error-text').textContent = data.error;
                errorContainer.style.display = 'block';
                generateBtn.disabled = false;
            }
        } catch (error) {
            clearInterval(loadingInterval);
            console.error(error);
            loaderContainer.style.display = 'none';
            resultsArea.style.display = 'none';
            const errorContainer = document.getElementById('error-container');
            document.getElementById('error-text').textContent = "A network or server error occurred. Please try again.";
            errorContainer.style.display = 'block';
            generateBtn.disabled = false;
        }
    });
    
    // PDF Button "Coming Soon" intercept
    const downloadPdfBtn = document.getElementById('download-pdf-btn');
    if (downloadPdfBtn) {
        downloadPdfBtn.addEventListener('click', (e) => {
            e.preventDefault();
            downloadPdfBtn.textContent = 'Coming soon!';
            downloadPdfBtn.style.cursor = 'not-allowed';
            downloadPdfBtn.style.opacity = '0.7';
        });
    }

    // Theme Toggle Logic
    const themeToggleBtn = document.getElementById('theme-toggle-btn');
    if (themeToggleBtn) {
        const currentTheme = localStorage.getItem('app-theme') || 'light';
        if (currentTheme === 'dark') {
            document.documentElement.setAttribute('data-theme', 'dark');
            themeToggleBtn.textContent = '☀️';
        }

        themeToggleBtn.addEventListener('click', () => {
            if (document.documentElement.getAttribute('data-theme') === 'dark') {
                document.documentElement.removeAttribute('data-theme');
                localStorage.setItem('app-theme', 'light');
                themeToggleBtn.textContent = '🌙';
            } else {
                document.documentElement.setAttribute('data-theme', 'dark');
                localStorage.setItem('app-theme', 'dark');
                themeToggleBtn.textContent = '☀️';
            }
        });
    }
});
