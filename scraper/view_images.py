import os
import base64
from PIL import Image
import matplotlib.pyplot as plt

def view_images():
    """Muestra las imágenes descargadas en una ventana"""
    downloads_folder = "downloads"
    
    if not os.path.exists(downloads_folder):
        print("❌ Carpeta 'downloads' no existe")
        return
    
    images = [f for f in os.listdir(downloads_folder) if f.endswith(('.jpg', '.png', '.jpeg'))]
    
    if not images:
        print("❌ No hay imágenes en la carpeta 'downloads'")
        print("   Posibles causas:")
        print("   1. Instagram bloqueó las descargas (Error 403/429)")
        print("   2. Las imágenes son de perfiles privados")
        print("   3. Necesitas más tiempo entre peticiones")
        return
    
    print(f"📸 Encontradas {len(images)} imágenes en descargas:")
    for img in images:
        size = os.path.getsize(os.path.join(downloads_folder, img))
        print(f"   - {img} ({size/1024:.1f} KB)")
    
    # Mostrar primeras 3 imágenes
    for i, img_file in enumerate(images[:3]):
        img_path = os.path.join(downloads_folder, img_file)
        try:
            img = Image.open(img_path)
            print(f"\n✅ {img_file}: {img.size[0]}x{img.size[1]} píxeles")
            
            # Mostrar imagen
            plt.figure(figsize=(10, 8))
            plt.imshow(img)
            plt.title(f"Imagen {i+1}: {img_file}")
            plt.axis('off')
            plt.show()
        except Exception as e:
            print(f"❌ Error abriendo {img_file}: {e}")

if __name__ == "__main__":
    view_images()