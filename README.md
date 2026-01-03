
# 🎨 Image to ASCII Converter (CLI) - Day68 

A simple yet powerful **Image → ASCII Art** converter written in Python.  
Convert any image into detailed ASCII output directly in your terminal or save it as a `.txt` file.

Perfect for fun, creative projects, or adding stylish text art to your console apps.

---

## 🚀 Features

- Convert any image to ASCII art  
- Adjustable output width  
- Two character ramps (default & extended)  
- Optional color output (24-bit ANSI)  
- Invert brightness for white/black backgrounds  
- Save ASCII to file  
- Works on Windows, Linux, macOS, and Termux  

---

## 📦 Installation

```bash
pip install pillow colorama
For Termux users:

bash
Copy code
pkg install python clang libjpeg-turbo libpng
pip install pillow colorama
🖼 Usage
Basic conversion
bash
Copy code
python img2ascii.py image.jpg
Custom width
bash
Copy code
python img2ascii.py image.jpg --width 120
Save output to file
bash
Copy code
python img2ascii.py image.jpg -W 140 -o output.txt
Extended ramp (more detail)
bash
Copy code
python img2ascii.py image.jpg --ramp extended
Invert brightness
bash
Copy code
python img2ascii.py image.jpg --invert
Colored ASCII output
bash
Copy code
python img2ascii.py image.jpg --color
Colored background mode
bash
Copy code
python img2ascii.py image.jpg --color --background
🧩 Example
arduino
Copy code
python img2ascii.py portrait.jpg --width 100
Outputs a detailed ASCII representation in your terminal.

📝 Requirements
Python 3.8+

Pillow

Colorama (optional but recommended on Windows)

📄 License
This project is open-source and free to use.

🤝 Contribute
Feel free to fork the project and add:

Web UI

Drag-and-drop GUI

Faster conversion engines

Different ASCII palettes

Pull requests are welcome!
