#!/usr/bin/env python3

"""
UnicodeFix Web Application

A modern web interface for the UnicodeFix Unicode text cleaning utility.
Provides file upload and text paste functionality with a clean, responsive UI.

Run with: python web_app.py
Access at: http://localhost:8000
"""

import os
import tempfile
from pathlib import Path
from typing import Optional

import uvicorn
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Import our existing cleanup functionality
from bin.cleanup_text_module import clean_text

app = FastAPI(
    title="UnicodeFix Web Interface",
    description="Clean Unicode artifacts from text files and content",
    version="1.0.0"
)

# Serve static files (CSS, JS, etc.)
static_dir = Path("static")
static_dir.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")


class TextCleanRequest(BaseModel):
    """Request model for text cleaning."""
    text: str
    preserve_formatting: bool = True


class CleanResponse(BaseModel):
    """Response model for cleaned text."""
    success: bool
    cleaned_text: Optional[str] = None
    original_size: int
    cleaned_size: int
    changes_made: int
    error: Optional[str] = None


def count_unicode_changes(original: str, cleaned: str) -> int:
    """Count the number of Unicode characters that were changed."""
    changes = 0
    min_len = min(len(original), len(cleaned))
    
    # Count character differences
    for i in range(min_len):
        if original[i] != cleaned[i]:
            changes += 1
    
    # Add length difference (removed characters)
    changes += abs(len(original) - len(cleaned))
    
    return changes


@app.get("/", response_class=HTMLResponse)
async def get_index():
    """Serve the main web interface."""
    html_content = """
<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UnicodeFix - Clean Unicode Text</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    colors: {
                        'apple-blue': '#007AFF',
                        'apple-gray': '#8E8E93',
                    }
                }
            }
        }
    </script>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%23007AFF'><path d='M12 2L2 7v10c0 5.55 3.84 9.74 9 9.74s9-4.19 9-9.74V7l-10-5z'/></svg>">
</head>
<body class="bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-100 min-h-screen transition-colors duration-200">
    <div class="container mx-auto px-4 py-8 max-w-4xl">
        <!-- Header -->
        <div class="text-center mb-12">
            <div class="flex items-center justify-center mb-4">
                <svg class="w-12 h-12 text-apple-blue mr-3" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12 2L2 7v10c0 5.55 3.84 9.74 9 9.74s9-4.19 9-9.74V7l-10-5z"/>
                </svg>
                <h1 class="text-4xl font-bold bg-gradient-to-r from-apple-blue to-blue-600 bg-clip-text text-transparent">
                    UnicodeFix
                </h1>
            </div>
            <p class="text-xl text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
                Clean problematic Unicode characters from your text. Remove invisible characters, fix smart quotes, and normalize text for better compatibility.
            </p>
        </div>

        <!-- Dark Mode Toggle -->
        <div class="fixed top-4 right-4">
            <button id="darkModeToggle" class="p-2 rounded-lg bg-white dark:bg-gray-800 shadow-lg border border-gray-200 dark:border-gray-700 hover:shadow-xl transition-all duration-200">
                <svg class="w-5 h-5 hidden dark:block" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z" clip-rule="evenodd"></path>
                </svg>
                <svg class="w-5 h-5 block dark:hidden" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z"></path>
                </svg>
            </button>
        </div>

        <!-- Main Interface -->
        <div class="space-y-8">
            <!-- Method Selection -->
            <div class="flex justify-center">
                <div class="bg-white dark:bg-gray-800 p-1 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 inline-flex">
                    <button id="textModeBtn" class="px-6 py-3 rounded-md text-sm font-medium transition-all duration-200 bg-apple-blue text-white shadow-sm">
                        Paste Text
                    </button>
                    <button id="fileModeBtn" class="px-6 py-3 rounded-md text-sm font-medium transition-all duration-200 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100">
                        Upload File
                    </button>
                </div>
            </div>

            <!-- Text Input Mode -->
            <div id="textMode" class="space-y-6">
                <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-200 dark:border-gray-700 p-6">
                    <label for="textInput" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
                        Enter your text to clean:
                    </label>
                    <textarea 
                        id="textInput" 
                        rows="8" 
                        class="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-apple-blue focus:border-transparent bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder-gray-500 dark:placeholder-gray-400 resize-none transition-all duration-200"
                        placeholder="Paste your text here... It can contain problematic Unicode characters like "smart quotes", em—dashes, invisible characters, etc."
                    ></textarea>
                </div>
            </div>

            <!-- File Upload Mode -->
            <div id="fileMode" class="space-y-6 hidden">
                <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-200 dark:border-gray-700 p-6">
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
                        Upload a text file to clean:
                    </label>
                    <div id="dropZone" class="border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg p-8 text-center hover:border-apple-blue dark:hover:border-apple-blue transition-colors duration-200 cursor-pointer">
                        <svg class="mx-auto h-12 w-12 text-gray-400 dark:text-gray-500 mb-4" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                            <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                        </svg>
                        <p class="text-sm text-gray-600 dark:text-gray-400">
                            <span class="font-medium text-apple-blue hover:text-blue-600 cursor-pointer">Click to upload</span> or drag and drop
                        </p>
                        <p class="text-xs text-gray-500 dark:text-gray-500 mt-1">
                            TXT, MD, or other text files
                        </p>
                    </div>
                    <input type="file" id="fileInput" class="hidden" accept=".txt,.md,.text,.log,.csv,.json,.xml,.html,.css,.js,.py,.php,.java,.cpp,.c,.h" />
                </div>
            </div>

            <!-- Clean Button -->
            <div class="text-center">
                <button id="cleanBtn" class="bg-apple-blue hover:bg-blue-600 text-white font-medium py-3 px-8 rounded-lg shadow-lg hover:shadow-xl transition-all duration-200 transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none">
                    <span id="cleanBtnText">Clean Text</span>
                    <svg id="cleanBtnSpinner" class="hidden animate-spin -mr-1 ml-3 h-5 w-5 text-white inline" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                </button>
            </div>

            <!-- Results -->
            <div id="results" class="hidden bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-200 dark:border-gray-700 p-6">
                <div class="flex items-center justify-between mb-4">
                    <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100">Cleaned Text</h3>
                    <div class="flex space-x-2">
                        <button id="copyBtn" class="bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-300 px-4 py-2 rounded-lg text-sm font-medium transition-colors duration-200">
                            Copy
                        </button>
                        <button id="downloadBtn" class="bg-apple-blue hover:bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors duration-200">
                            Download
                        </button>
                    </div>
                </div>
                
                <div id="statsBar" class="bg-gray-50 dark:bg-gray-700 rounded-lg p-4 mb-4">
                    <div class="flex justify-between text-sm">
                        <span class="text-gray-600 dark:text-gray-400">
                            Changes made: <span id="changesCount" class="font-medium text-apple-blue">0</span>
                        </span>
                        <span class="text-gray-600 dark:text-gray-400">
                            Size: <span id="sizeInfo" class="font-medium">0 → 0 chars</span>
                        </span>
                    </div>
                </div>
                
                <textarea 
                    id="resultText" 
                    rows="8" 
                    readonly 
                    class="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-gray-100 resize-none"
                ></textarea>
            </div>

            <!-- Error Alert -->
            <div id="errorAlert" class="hidden bg-red-50 dark:bg-red-900/50 border border-red-200 dark:border-red-800 rounded-lg p-4">
                <div class="flex">
                    <svg class="h-5 w-5 text-red-400 mt-0.5 mr-3" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
                    </svg>
                    <div>
                        <h3 class="text-sm font-medium text-red-800 dark:text-red-200">Error</h3>
                        <p id="errorMessage" class="text-sm text-red-700 dark:text-red-300 mt-1"></p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Footer -->
        <footer class="mt-16 text-center text-sm text-gray-500 dark:text-gray-400">
            <p>UnicodeFix Web Interface • Made with ❤️ for clean text</p>
        </footer>
    </div>

    <script src="/static/app.js"></script>
</body>
</html>
    """
    return HTMLResponse(content=html_content)


@app.post("/api/clean-text", response_model=CleanResponse)
async def clean_text_endpoint(request: TextCleanRequest):
    """Clean Unicode artifacts from provided text."""
    try:
        if not request.text.strip():
            raise HTTPException(status_code=400, detail="No text provided")
        
        original_text = request.text
        cleaned_text = clean_text(original_text)
        
        changes_made = count_unicode_changes(original_text, cleaned_text)
        
        return CleanResponse(
            success=True,
            cleaned_text=cleaned_text,
            original_size=len(original_text),
            cleaned_size=len(cleaned_text),
            changes_made=changes_made
        )
    
    except Exception as e:
        return CleanResponse(
            success=False,
            error=str(e),
            original_size=len(request.text) if request.text else 0,
            cleaned_size=0,
            changes_made=0
        )


@app.post("/api/clean-file", response_model=CleanResponse)
async def clean_file_endpoint(file: UploadFile = File(...)):
    """Clean Unicode artifacts from uploaded file."""
    try:
        # Validate file type
        if not file.filename or not any(file.filename.lower().endswith(ext) 
                                       for ext in ['.txt', '.md', '.text', '.log', '.csv', 
                                                 '.json', '.xml', '.html', '.css', '.js', 
                                                 '.py', '.php', '.java', '.cpp', '.c', '.h']):
            raise HTTPException(status_code=400, detail="Unsupported file type")
        
        # Read file content
        content = await file.read()
        
        # Decode with error handling
        try:
            original_text = content.decode('utf-8')
        except UnicodeDecodeError:
            try:
                original_text = content.decode('utf-8', errors='replace')
            except Exception:
                raise HTTPException(status_code=400, detail="Could not decode file as text")
        
        if not original_text.strip():
            raise HTTPException(status_code=400, detail="File appears to be empty")
        
        cleaned_text = clean_text(original_text)
        changes_made = count_unicode_changes(original_text, cleaned_text)
        
        return CleanResponse(
            success=True,
            cleaned_text=cleaned_text,
            original_size=len(original_text),
            cleaned_size=len(cleaned_text),
            changes_made=changes_made
        )
    
    except HTTPException:
        raise
    except Exception as e:
        return CleanResponse(
            success=False,
            error=f"Error processing file: {str(e)}",
            original_size=0,
            cleaned_size=0,
            changes_made=0
        )


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "UnicodeFix Web Interface"}


if __name__ == "__main__":
    print("🚀 Starting UnicodeFix Web Interface...")
    print("📱 Access the interface at: http://localhost:8000")
    print("🔧 API docs available at: http://localhost:8000/docs")
    
    uvicorn.run(
        "web_app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 