import os
import time
import shutil
import traceback
import moviepy.video.io.ImageSequenceClip
import PIL.Image

def create_temp_folder():
    """Tworzy folder tymczasowy 'pngtmp' w bieżącej lokalizacji."""
    temp_folder = os.path.join(os.getcwd(), "pngtmp")
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)
    return temp_folder

def remove_temp_folder(folder_path):
    """Usuwa cały folder tymczasowy wraz z zawartością."""
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)

def analyseImage(path):
    """
    Analiza animowanego obrazu w celu określenia trybu (full lub partial).
    """
    try:
        im = PIL.Image.open(path)
    except PIL.UnidentifiedImageError:
        print(f"Error: Nie można otworzyć lub zidentyfikować pliku obrazu: {path}")
        return {'size': (0, 0), 'mode': 'error'}
    results = {'size': im.size, 'mode': 'full'}
    try:
        while True:
            if im.tile:
                tile = im.tile[0]
                update_region = tile[1]
                update_region_dimensions = update_region[2:]
                if update_region_dimensions != im.size:
                    results['mode'] = 'partial'
                    break
            im.seek(im.tell() + 1)
    except EOFError:
        pass
    return results

def processImage(path, output_folder):
    """
    Przetwarza animowany obraz WebP, zapisując każdą klatkę jako PNG w folderze output_folder.
    Zwraca listę ścieżek do zapisanych klatek.
    """
    analysis_results = analyseImage(path)
    if analysis_results['mode'] == 'error':
        return []
    
    images = []
    mode = analysis_results['mode']
    i = 0
    try:
        im = PIL.Image.open(path)
        last_frame = im.convert('RGBA')
        while True:
            new_frame = PIL.Image.new('RGBA', im.size)
            if mode == 'partial':
                new_frame.paste(last_frame)
            new_frame.paste(im, (0, 0), im.convert('RGBA'))
            frame_path = os.path.join(output_folder, f"frame_{i}.png")
            new_frame.save(frame_path, 'PNG')
            images.append(frame_path)
            print(f"Zapisano klatkę: {frame_path}")
            i += 1
            last_frame = new_frame
            im.seek(im.tell() + 1)
    except EOFError:
        print("Koniec animacji - skończono przetwarzanie klatek.")
    except Exception as e:
        print("Wystąpił wyjątek podczas przetwarzania obrazu:")
        traceback.print_exc()
    return images

def webp_to_mp4(webp_folder):
    """
    Dla każdego pliku .webp w danym folderze:
      - Tworzy folder tymczasowy 'pngtmp' do zapisywania klatek.
      - Przetwarza animowany obraz, zapisuje klatki jako PNG.
      - Łączy klatki w plik wideo .mp4 przy użyciu MoviePy.
      - Na końcu usuwa cały folder tymczasowy.
    """
    temp_folder = create_temp_folder()
    for filename in os.listdir(webp_folder):
        if filename.lower().endswith(".webp"):
            webp_path = os.path.join(webp_folder, filename)
            mp4_path = os.path.join(webp_folder, filename[:-5] + ".mp4")
            print(f"\nPrzetwarzanie pliku: {webp_path}")
            images = processImage(webp_path, temp_folder)
            print(f"Liczba wyekstrahowanych klatek: {len(images)}")
            if images:
                try:
                    fps = 24  # Możesz dostosować wartość FPS do swoich potrzeb
                    clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(images, fps=fps)
                    # Usunięto argument verbose, ponieważ nie jest obsługiwany
                    clip.write_videofile(mp4_path, logger='bar')
                    print(f"Plik .mp4 został pomyślnie zapisany: {mp4_path}")
                except Exception as e:
                    print(f"Błąd przy tworzeniu wideo z plików klatek z {webp_path}: {e}")
                    traceback.print_exc()
            else:
                print(f"Brak klatek do konwersji dla pliku: {webp_path}")
    remove_temp_folder(temp_folder)

if __name__ == "__main__":
    # Podaj odpowiednią ścieżkę do folderu zawierającego pliki .webp
    webp_folder = "x:\\outputs\\"
    webp_to_mp4(webp_folder)
