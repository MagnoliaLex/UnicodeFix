/**
 * UnicodeFix Web Interface JavaScript
 * 
 * Handles UI interactions, file upload, text processing, and API communication.
 */

class UnicodeFix {
    constructor() {
        this.currentMode = 'text';
        this.init();
    }

    init() {
        this.bindEventListeners();
        this.initDarkMode();
        this.updateUI();
    }

    bindEventListeners() {
        // Mode switching
        document.getElementById('textModeBtn').addEventListener('click', () => this.switchMode('text'));
        document.getElementById('fileModeBtn').addEventListener('click', () => this.switchMode('file'));

        // File upload
        const fileInput = document.getElementById('fileInput');
        const dropZone = document.getElementById('dropZone');

        dropZone.addEventListener('click', () => fileInput.click());
        dropZone.addEventListener('dragover', this.handleDragOver.bind(this));
        dropZone.addEventListener('drop', this.handleDrop.bind(this));
        fileInput.addEventListener('change', this.handleFileSelect.bind(this));

        // Clean button
        document.getElementById('cleanBtn').addEventListener('click', this.processText.bind(this));

        // Results actions
        document.getElementById('copyBtn').addEventListener('click', this.copyResult.bind(this));
        document.getElementById('downloadBtn').addEventListener('click', this.downloadResult.bind(this));

        // Dark mode toggle
        document.getElementById('darkModeToggle').addEventListener('click', this.toggleDarkMode.bind(this));

        // Keyboard shortcuts
        document.addEventListener('keydown', this.handleKeyboard.bind(this));
    }

    initDarkMode() {
        const isDark = localStorage.getItem('darkMode') === 'true';
        if (isDark) {
            document.documentElement.classList.add('dark');
        } else {
            document.documentElement.classList.remove('dark');
        }
    }

    toggleDarkMode() {
        const isDark = document.documentElement.classList.toggle('dark');
        localStorage.setItem('darkMode', isDark);
    }

    switchMode(mode) {
        this.currentMode = mode;
        this.updateUI();
        this.hideResults();
    }

    updateUI() {
        const textMode = document.getElementById('textMode');
        const fileMode = document.getElementById('fileMode');
        const textModeBtn = document.getElementById('textModeBtn');
        const fileModeBtn = document.getElementById('fileModeBtn');

        if (this.currentMode === 'text') {
            textMode.classList.remove('hidden');
            fileMode.classList.add('hidden');
            textModeBtn.classList.add('bg-apple-blue', 'text-white', 'shadow-sm');
            textModeBtn.classList.remove('text-gray-600', 'dark:text-gray-400', 'hover:text-gray-900', 'dark:hover:text-gray-100');
            fileModeBtn.classList.remove('bg-apple-blue', 'text-white', 'shadow-sm');
            fileModeBtn.classList.add('text-gray-600', 'dark:text-gray-400', 'hover:text-gray-900', 'dark:hover:text-gray-100');
        } else {
            textMode.classList.add('hidden');
            fileMode.classList.remove('hidden');
            fileModeBtn.classList.add('bg-apple-blue', 'text-white', 'shadow-sm');
            fileModeBtn.classList.remove('text-gray-600', 'dark:text-gray-400', 'hover:text-gray-900', 'dark:hover:text-gray-100');
            textModeBtn.classList.remove('bg-apple-blue', 'text-white', 'shadow-sm');
            textModeBtn.classList.add('text-gray-600', 'dark:text-gray-400', 'hover:text-gray-900', 'dark:hover:text-gray-100');
        }
    }

    handleDragOver(e) {
        e.preventDefault();
        e.stopPropagation();
        const dropZone = document.getElementById('dropZone');
        dropZone.classList.add('border-apple-blue', 'bg-blue-50', 'dark:bg-blue-900/20');
    }

    handleDrop(e) {
        e.preventDefault();
        e.stopPropagation();
        
        const dropZone = document.getElementById('dropZone');
        dropZone.classList.remove('border-apple-blue', 'bg-blue-50', 'dark:bg-blue-900/20');

        const files = e.dataTransfer.files;
        if (files.length > 0) {
            this.processFile(files[0]);
        }
    }

    handleFileSelect(e) {
        const files = e.target.files;
        if (files.length > 0) {
            this.processFile(files[0]);
        }
    }

    async processText() {
        this.hideError();

        if (this.currentMode === 'text') {
            const textInput = document.getElementById('textInput');
            const text = textInput.value.trim();
            
            if (!text) {
                this.showError('Please enter some text to clean.');
                return;
            }

            await this.cleanText(text);
        } else {
            const fileInput = document.getElementById('fileInput');
            if (!fileInput.files.length) {
                this.showError('Please select a file to clean.');
                return;
            }
            await this.processFile(fileInput.files[0]);
        }
    }

    async processFile(file) {
        this.setLoading(true);
        this.hideError();

        try {
            const formData = new FormData();
            formData.append('file', file);

            const response = await fetch('/api/clean-file', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (result.success) {
                this.showResults(result, file.name);
            } else {
                this.showError(result.error || 'Failed to process file');
            }
        } catch (error) {
            console.error('Error processing file:', error);
            this.showError('Network error. Please try again.');
        } finally {
            this.setLoading(false);
        }
    }

    async cleanText(text) {
        this.setLoading(true);
        this.hideError();

        try {
            const response = await fetch('/api/clean-text', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: text,
                    preserve_formatting: true
                })
            });

            const result = await response.json();

            if (result.success) {
                this.showResults(result);
            } else {
                this.showError(result.error || 'Failed to clean text');
            }
        } catch (error) {
            console.error('Error cleaning text:', error);
            this.showError('Network error. Please try again.');
        } finally {
            this.setLoading(false);
        }
    }

    showResults(result, filename = null) {
        const resultsDiv = document.getElementById('results');
        const resultText = document.getElementById('resultText');
        const changesCount = document.getElementById('changesCount');
        const sizeInfo = document.getElementById('sizeInfo');

        resultText.value = result.cleaned_text;
        changesCount.textContent = result.changes_made;
        sizeInfo.textContent = `${result.original_size} → ${result.cleaned_size} chars`;

        // Store result for download
        this.lastResult = {
            text: result.cleaned_text,
            filename: filename
        };

        resultsDiv.classList.remove('hidden');
        resultsDiv.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    hideResults() {
        const resultsDiv = document.getElementById('results');
        resultsDiv.classList.add('hidden');
    }

    showError(message) {
        const errorAlert = document.getElementById('errorAlert');
        const errorMessage = document.getElementById('errorMessage');
        
        errorMessage.textContent = message;
        errorAlert.classList.remove('hidden');
        errorAlert.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }

    hideError() {
        const errorAlert = document.getElementById('errorAlert');
        errorAlert.classList.add('hidden');
    }

    setLoading(isLoading) {
        const cleanBtn = document.getElementById('cleanBtn');
        const cleanBtnText = document.getElementById('cleanBtnText');
        const cleanBtnSpinner = document.getElementById('cleanBtnSpinner');

        cleanBtn.disabled = isLoading;
        
        if (isLoading) {
            cleanBtnText.textContent = 'Processing...';
            cleanBtnSpinner.classList.remove('hidden');
        } else {
            cleanBtnText.textContent = 'Clean Text';
            cleanBtnSpinner.classList.add('hidden');
        }
    }

    async copyResult() {
        const resultText = document.getElementById('resultText');
        
        try {
            await navigator.clipboard.writeText(resultText.value);
            this.showTemporaryFeedback('copyBtn', 'Copied!');
        } catch (error) {
            // Fallback for older browsers
            resultText.select();
            document.execCommand('copy');
            this.showTemporaryFeedback('copyBtn', 'Copied!');
        }
    }

    downloadResult() {
        if (!this.lastResult) return;

        const blob = new Blob([this.lastResult.text], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        
        const a = document.createElement('a');
        a.href = url;
        a.download = this.lastResult.filename 
            ? this.lastResult.filename.replace(/\.[^/.]+$/, '.clean.txt')
            : 'cleaned-text.txt';
        
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        
        URL.revokeObjectURL(url);
        this.showTemporaryFeedback('downloadBtn', 'Downloaded!');
    }

    showTemporaryFeedback(buttonId, message) {
        const button = document.getElementById(buttonId);
        const originalText = button.textContent;
        
        button.textContent = message;
        button.classList.add('bg-green-500', 'hover:bg-green-600');
        
        setTimeout(() => {
            button.textContent = originalText;
            button.classList.remove('bg-green-500', 'hover:bg-green-600');
        }, 2000);
    }

    handleKeyboard(e) {
        // Ctrl/Cmd + Enter to process
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            e.preventDefault();
            this.processText();
        }
        
        // Escape to hide results
        if (e.key === 'Escape') {
            this.hideResults();
            this.hideError();
        }
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new UnicodeFix();
});

// Add some example text for demonstration
document.addEventListener('DOMContentLoaded', () => {
    const textInput = document.getElementById('textInput');
    if (textInput) {
        textInput.placeholder = `Paste your text here... It can contain problematic Unicode characters like "smart quotes", em—dashes, invisible characters, etc.

Try this example:
"Hello World" — This text contains problematic Unicode characters like smart quotes, em-dashes, and non-breaking spaces that can cause issues in code and documents.`;
    }
}); 