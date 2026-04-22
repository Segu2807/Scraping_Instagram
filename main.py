import json
import time
import os
from datetime import datetime
from scraper.browser import InstagramBrowser
from scraper.profile import scrape_profile_info
from scraper.posts import scroll_and_get_links, extract_post_details
from scraper.display import display_results, save_pretty_json

def main():
    # Configuración
    TARGET_USERNAME = "nasa"
    MAX_POSTS = 10  # Reducir a 5 para pruebas más rápidas
    
    print("🚀 Iniciando Instagram Scraper...")
    print(f"🎯 Cuenta objetivo: @{TARGET_USERNAME}")
    print(f"📸 Máximo de posts: {MAX_POSTS}")
    
    # Crear carpetas necesarias
    os.makedirs("data/resultados", exist_ok=True)
    os.makedirs("downloads", exist_ok=True)
    
    # Inicializar navegador
    browser_manager = InstagramBrowser(headless=False)
    browser_manager.start()
    page = browser_manager.get_page()
    
    # Extraer datos del perfil
    perfil = scrape_profile_info(page, TARGET_USERNAME)
    if not perfil:
        print("❌ No se pudo acceder al perfil")
        browser_manager.close()
        return
    
    # Extraer enlaces de posts
    print("\n🔍 Buscando publicaciones...")
    post_urls = scroll_and_get_links(page, max_posts=MAX_POSTS)
    
    if not post_urls:
        print("⚠️ No se encontraron posts")
        resultado = {
            "fechaExtraccion": datetime.now().isoformat(),
            "perfil": TARGET_USERNAME,
            "totalPostsEncontrados": 0,
            "exitosos": 0,
            "publicaciones": []
        }
        
        save_pretty_json(resultado, "data/resultados/perfil_extraido.json")
        display_results(resultado)
        browser_manager.close()
        return
    
    # Extraer detalles de cada post
    print(f"\n📸 Extrayendo detalles de {len(post_urls)} posts...")
    publicaciones = []
    exitosos = 0
    
    for i, url in enumerate(post_urls, 1):
        print(f"\n📌 Procesando post {i}/{len(post_urls)}")
        detalles = extract_post_details(page, url, download_images=True)
        publicaciones.append(detalles)
        
        if 'error' not in detalles:
            exitosos += 1
        
        # Pausa más larga entre posts para evitar bloqueos
        if i < len(post_urls):
            print("   ⏳ Esperando 3 segundos antes del siguiente post...")
            time.sleep(3)
    
    # Guardar resultados
    resultado_final = {
        "fechaExtraccion": datetime.now().isoformat(),
        "perfil": perfil,
        "totalPostsEncontrados": len(publicaciones),
        "exitosos": exitosos,
        "publicaciones": publicaciones
    }
    
    output_file = "data/resultados/perfil_extraido.json"
    save_pretty_json(resultado_final, output_file)
    
    # Mostrar resultados
    display_results(resultado_final)
    
    # Cerrar navegador
    browser_manager.close()
    
    print(f"\n💾 Datos guardados en: {output_file}")
    print(f"🖼️ Imágenes guardadas en: downloads/")
    
    # Mostrar resumen de imágenes descargadas
    imagenes_descargadas = sum(len(p.get('imagenes', [])) for p in publicaciones)
    print(f"📊 Resumen: {imagenes_descargadas} imágenes descargadas de {len(publicaciones)} posts")

if __name__ == "__main__":
    main()