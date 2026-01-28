# 🔐 File Hashing Tool

A professional web-based application for calculating and comparing cryptographic hashes of files. Built with Streamlit and following software engineering best practices.

## ✨ Features

- **Multiple Hash Algorithms**: Support for MD5, SHA-1/224/256/384/512, SHA3-256/512, BLAKE2b/s
- **Batch Processing**: Hash up to 5 files simultaneously (1GB each)
- **Real-time Progress**: Visual progress bars for each file being processed
- **Hash Comparison**: View results in easy-to-compare table format
- **Export Options**: Download results as CSV or formatted text
- **Dark/Light Mode**: Toggle between themes for comfortable viewing
- **Session History**: Keep track of all hashed files during your session
- **Click-to-Copy**: Click any hash value to copy to clipboard

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/hash-tool.git
   cd hash-tool
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open in browser**
   - The app will automatically open at `http://localhost:8501`

## 📁 Project Structure

```
hash-tool/
├── app.py                      # Main application entry point
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── src/
│   ├── core/
│   │   ├── hasher.py          # Hash calculation logic
│   │   └── file_handler.py    # File operations and validation
│   ├── ui/
│   │   ├── components.py      # Reusable UI components
│   │   ├── layout.py          # Main page layout
│   │   └── theme.py           # Theme management
│   └── utils/
│       ├── formatters.py      # Data formatting utilities
│       └── exporters.py       # Export functionality
├── docs/
│   ├── README.md              # This file
│   └── CONTRIBUTING.md        # Contribution guidelines
└── tests/                      # Unit tests (coming soon)
```

## 🎯 Usage

### Basic Workflow

1. **Select Hash Algorithms**
   - Choose 1-3 algorithms from the sidebar
   - Default is SHA-256

2. **Upload Files**
   - Click "Browse files" or drag and drop
   - Maximum 5 files, 1GB each

3. **Generate Hashes**
   - Click "Generate Hashes" button
   - Watch real-time progress for each file

4. **View Results**
   - Compare hashes in the table view
   - Expand detailed view for more information
   - Click any hash to copy

5. **Export Results**
   - Download as CSV for spreadsheet analysis
   - Download as text for documentation

### Configuration

Edit `config.py` to customize:

```python
MAX_FILE_SIZE_BYTES = 1073741824  # 1GB
MAX_FILES_ALLOWED = 5
CHUNK_SIZE = 8192  # 8KB chunks
```

## 🛠️ Development

### Code Organization

The project follows a modular architecture:

- **Core Logic** (`src/core/`): Pure Python functions, UI-independent
- **UI Components** (`src/ui/`): Streamlit-specific rendering
- **Utilities** (`src/utils/`): Helper functions
- **Configuration** (`config.py`): Centralized settings

### Adding New Hash Algorithms

1. Import the algorithm in `config.py`
2. Add to `HASH_ALGORITHMS` dictionary
3. Algorithm automatically appears in UI

```python
# In config.py
import hashlib

HASH_ALGORITHMS = {
    'NEW-ALGO': hashlib.new_algorithm,  # Add here
    # ... existing algorithms
}
```

### Running Tests

```bash
# Coming soon
pytest tests/
```

## 🌐 Deployment

### Streamlit Cloud (Recommended)

1. Push code to GitHub
2. Visit https://share.streamlit.io/
3. Connect repository and deploy

### Docker (Alternative)

```bash
# Coming soon
docker build -t hash-tool .
docker run -p 8501:8501 hash-tool
```

## 📊 Supported Hash Algorithms

| Algorithm | Output Size | Speed | Use Case |
|-----------|-------------|-------|----------|
| MD5 | 128-bit | Very Fast | Legacy checksums |
| SHA-1 | 160-bit | Fast | Legacy (deprecated) |
| SHA-256 | 256-bit | Medium | **Most common** |
| SHA-512 | 512-bit | Medium | Extra security |
| SHA3-256 | 256-bit | Medium | Modern standard |
| SHA3-512 | 512-bit | Medium | High security |
| BLAKE2b | 512-bit | Very Fast | Modern, fast |
| BLAKE2s | 256-bit | Very Fast | Modern, smaller |


### Quick Contribution Guide

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly
5. Commit (`git commit -m 'Add amazing feature'`)
6. Push (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Uses Python's built-in `hashlib` module
- Inspired by the need for better file verification tools

---

**Made with ❤️ for secure file verification**