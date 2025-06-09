#!/usr/bin/env python3

"""
Quick test script for UnicodeFix web interface components
"""

def test_cleanup_module():
    """Test the cleanup text module."""
    print("Testing cleanup_text_module...")
    
    try:
        from bin.cleanup_text_module import clean_text
        
        # Test with problematic Unicode
        test_text = '"Hello" — This contains problematic characters… like smart quotes and em-dashes.'
        cleaned = clean_text(test_text)
        
        print(f"Original: {test_text}")
        print(f"Cleaned:  {cleaned}")
        print("✅ cleanup_text_module works correctly!")
        return True
    except Exception as e:
        print(f"❌ Error testing cleanup module: {e}")
        return False

def test_web_imports():
    """Test if we can import web dependencies."""
    print("\nTesting web dependencies...")
    
    try:
        import fastapi
        import uvicorn
        from fastapi import FastAPI
        print("✅ FastAPI and Uvicorn imported successfully!")
        return True
    except ImportError as e:
        print(f"❌ Error importing web dependencies: {e}")
        return False

def test_basic_web_app():
    """Test basic web app functionality."""
    print("\nTesting web app components...")
    
    try:
        from web_app import app, clean_text_endpoint, CleanResponse, TextCleanRequest
        print("✅ Web app components imported successfully!")
        return True
    except Exception as e:
        print(f"❌ Error testing web app: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 UnicodeFix Web Interface Test")
    print("=" * 40)
    
    tests = [
        test_cleanup_module,
        test_web_imports,
        test_basic_web_app
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The web interface should work correctly.")
        print("\n🚀 To start the web interface:")
        print("   python run_web.py")
        print("   or")
        print("   .\\unicodefix-web.bat")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main() 