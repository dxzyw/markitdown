# MarkItDown GUI

A desktop application for converting documents to Markdown format, based on [Microsoft's MarkItDown](https://github.com/microsoft/markitdown).

![MarkItDown Screenshot](public/screenshot.png)

## Features

- 📄 **Document Support**
  - PDF to Markdown conversion
  - Microsoft Word (.docx, .doc)
  - PowerPoint presentations (.pptx)
  - Excel spreadsheets (.xlsx)

- 🎯 **Key Features**
  - Simple GUI interface
  - Drag & drop support
  - Preview converted content
  - Quick file saving
  - Error handling & feedback

- 🔍 **Smart Recognition**
  - Built-in OCR technology
  - Table structure preservation
  - Image extraction & embedding
  - List formatting support
  - Heading hierarchy preservation

## Quick Start

### For Users

1. Download the latest release for your platform:
   - [Windows GUI Package](https://github.com/dxzyw/markitdown/releases/latest)
   - macOS (Coming Soon)
   - Linux (Coming Soon)

2. Run the application:
   - Windows: Double-click the `.exe` file
   - Preview the converted markdown
   - Save the result

### For Developers

1. Clone the repository:
```bash
git clone https://github.com/dxzyw/markitdown.git
cd markitdown
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python src/main.py
```

## Building from Source

To build the executable:

```bash
python build.py
```

The output will be in the `dist` directory.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Based on [Microsoft's MarkItDown](https://github.com/microsoft/markitdown)
- Uses [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) for the GUI
- Built with [PyInstaller](https://www.pyinstaller.org/) for distribution

---

<p align="center">Made with ❤️ for document conversion</p>