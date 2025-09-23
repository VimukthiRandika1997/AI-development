# 🖼️ Scenario

We have a folder of large images and want to resize them (or apply filters) as fast as possible using all CPU cores.

## Directory Structure

```markdown
images/
    img1.jpg
    img2.jpg
    ...
output/
```

## Code: Parallel Image Resizing

```python
import os
from pathlib import Path
from PIL import Image
from multiprocessing import Pool, cpu_count
import time

INPUT_DIR = Path("images")
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)


def resize_image(image_path: Path):
    """Resize a single image to 800x800 and save to OUTPUT_DIR."""
    img = Image.open(image_path)
    img = img.resize((800, 800))
    out_path = OUTPUT_DIR / image_path.name
    img.save(out_path, "JPEG")
    return f"Processed {image_path.name}"

if __name__ == "__main__":
    start = time.time()

    # List all JPG/PNG images
    image_files = [p for p in INPUT_DIR.iterdir() if p.suffix.lower() in (".jpg", ".png", ".jpeg")]

    # Use all CPU cores in the PC
    with Pool(processes=cpu_count()) as pool:
        for result in pool.imap_unordered(resize_image, image_files):
            print(result)

    print(f"Done in {time.time() - start:.2f} seconds")
```

## How this works:

- `Pool(processes=cpu_count())` spawns one process per CPU core
    - check no.of avaialble CPU cores using this command: `lscpu`
- Each worker:
    1. Opens a single image (I/O + CPU)
    2. Resizes it (CPU bound)
    3. Saves the result

- This scales almost linearly with cores:
    - If you have 8 cores and 100 images, you can get 8X speedup vs single-process
