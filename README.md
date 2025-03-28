# WebP to MP4 Conversion Script

This script converts animated WebP files into MP4 video files. It extracts individual frames from the WebP file, saves them as PNG images, and assembles them into an MP4 video using the MoviePy library.

---

## Requirements

- **Python 3.6+**
- **Libraries**:
  - `moviepy`
  - `Pillow`

### Installation

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/wasyleque/webp_to_mp4
   cd webp_to_mp4
   pip install moviepy Pillow
  
How to Use
    Place the WebP files you want to convert into a folder.
    Edit the script to point to the folder containing WebP files by modifying the webp_folder variable:
    
    webp_folder = "path/to/your/webp/files"

Converted MP4 files will be saved in the same folder as the WebP files.

Tools and Libraries Used

    Pillow (PIL) - For handling image processing.

    MoviePy - For creating video files from images.

    Python Standard Libraries - Libraries such as os, time, shutil, and traceback for general scripting tasks.  

Authors and Acknowledgments

    Script Author: wasyleque

    Third-party Libraries:

        MoviePy (https://github.com/Zulko/moviepy)

        Pillow (https://github.com/python-pillow/Pillow)

If you use this script in your project, please give proper credit to the author and acknowledge the libraries used.

License

This project is licensed under the MIT License - see the 
You can customize the sections to suit your needs or add more information. If you have any other questions, let me know! 😊
