<p align="center">
 <a href="https://app.deepsource.com/gh/3ricsonn/PyDFCat/?ref=repository-badge}" target="_blank">
 <img alt="DeepSource" title="DeepSource" src="https://app.deepsource.com/gh/3ricsonn/PyDFCat.svg/?label=active+issues&show_trend=true&token=Y2NWKSxBUnhCv3qSaX8gARR-"/>
</a>
 <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

<h1 align="center">PyDFCat — PDF Editor</h1>

PyDFCat is a Python-based PDF editor built using the CustomTkinter library. It provides various functionalities to
display, rearrange, delete, duplicate, and add pages to a PDF file.

## (Planned) Features

- [x] Open and display PDF-Files.
- [x] Duplicate pages within a PDF document.
- [x] Copy, cut, and paste pages within the document.
- [x] Delete specific pages from a PDF document.
- [x] View copied and cut pages in the clipboard tab.
- [ ] Edit copied and cut pages in the clipboard tab.
- [ ] Add new pages from an existing PDF document.
- [ ] Undo and redo document changes.

## Usage
```bash
usage: pydfcat [-h] [-V] [FILE]

PyDFCat is a GUI PDF editor providing functionality to rearrange and delete pages within a PDF-file,
as well as adding pages from other PDF-files

positional arguments:
  FILE           path to the file to open in pydfcat

options:
  -h, --help     show this help message and exit
  -V, --version  show program's version number and exit
```

## Installation
To install PyDFCat, follow these steps:

1. Clone the repository from GitHub:
    ```bash
    git clone https://github.com/3ricsonn/PyDFCat.git
    ```

2. Navigate to the cloned repository:
    ```bash
    cd PyDFCat
    ```

3. Install the program using pip:
    ```bash
    pip install .
    ```

4. OPTIONAL: Install optional dependencies (if you want tooltips) from the optional-requirements.txt file:
    ```bash
    pip install -r optional-requirements.txt
    ```

5. Run the application:
    ```bash
    pydfcat
    ```

## Uninstall

1. To uninstall PyDFCat, use the following command:
   ```bash
   pip uninstall pydfcat
   ```

2. If you installed the optional dependencies
   ```bash
   pip uninstall -r optional-requirements.txt
   ```

3. Further, you can delete the downloaded files

## Contact

For any questions or inquiries, please contact us at 3ricsonn@protonmail.com.
