class DocumentConverter {
    constructor() {
        this.dropZone = document.getElementById('dropZone');
        this.fileInput = document.getElementById('fileInput');
        this.resultText = document.getElementById('resultText');
        this.downloadBtn = document.getElementById('downloadBtn');
        this.progressBar = document.querySelector('.progress');
        
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        this.dropZone.addEventListener('dragover', this.handleDragOver.bind(this));
        this.dropZone.addEventListener('dragleave', this.handleDragLeave.bind(this));
        this.dropZone.addEventListener('drop', this.handleDrop.bind(this));
        this.dropZone.addEventListener('click', () => this.fileInput.click());
        this.fileInput.addEventListener('change', this.handleFileSelect.bind(this));
        this.downloadBtn.addEventListener('click', this.downloadMarkdown.bind(this));
    }

    handleDragOver(e) {
        e.preventDefault();
        this.dropZone.classList.add('dragover');
    }

    handleDragLeave(e) {
        e.preventDefault();
        this.dropZone.classList.remove('dragover');
    }

    handleDrop(e) {
        e.preventDefault();
        this.dropZone.classList.remove('dragover');
        const files = e.dataTransfer.files;
        if (files.length) this.processFile(files[0]);
    }

    handleFileSelect(e) {
        if (e.target.files.length) this.processFile(e.target.files[0]);
    }

    async processFile(file) {
        const formData = new FormData();
        formData.append('file', file);

        this.showProgress();
        this.resultText.value = 'Converting...';
        this.downloadBtn.disabled = true;

        try {
            const response = await fetch('/convert', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (data.status === 'success') {
                this.resultText.value = data.content;
                this.downloadBtn.disabled = false;
            } else {
                this.resultText.value = `Conversion failed: ${data.message}`;
            }
        } catch (error) {
            this.resultText.value = `Error: ${error.message}`;
        } finally {
            this.hideProgress();
        }
    }

    downloadMarkdown() {
        const content = this.resultText.value;
        if (!content) return;

        const blob = new Blob([content], { type: 'text/markdown' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'converted.md';
        document.body.appendChild(a);
        a.click();
        URL.revokeObjectURL(url);
        a.remove();
    }

    showProgress() {
        this.progressBar.classList.remove('d-none');
    }

    hideProgress() {
        this.progressBar.classList.add('d-none');
    }
}

// Initialize the converter
document.addEventListener('DOMContentLoaded', () => {
    new DocumentConverter();
}); 