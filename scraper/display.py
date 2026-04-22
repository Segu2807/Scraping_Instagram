import json
from datetime import datetime

def display_results(data):
    """Muestra los resultados en formato legible en la consola"""
    print("\n" + "="*80)
    print("📊 INSTAGRAM SCRAPER - RESULTADOS")
    print("="*80)
    
    # Información del perfil (ahora es un diccionario)
    perfil = data.get('perfil', {})
    if isinstance(perfil, dict):
        print(f"\n👤 PERFIL: {perfil.get('username', 'N/A')}")
        print(f"   📝 Bio: {perfil.get('bio', 'N/A')[:100]}")
        print(f"   📸 Posts: {perfil.get('posts_count', 'N/A')}")
        print(f"   👥 Seguidores: {perfil.get('followers_count', 'N/A')}")
        print(f"   👣 Siguiendo: {perfil.get('following_count', 'N/A')}")
    else:
        print(f"\n👤 PERFIL: {data.get('perfil', 'N/A')}")
    
    # Estadísticas de extracción
    print(f"\n📈 ESTADÍSTICAS:")
    print(f"   Total posts encontrados: {data.get('totalPostsEncontrados', 0)}")
    print(f"   Posts exitosos: {data.get('exitosos', 0)}")
    print(f"   Fecha extracción: {data.get('fechaExtraccion', 'N/A')}")
    
    # Publicaciones
    publicaciones = data.get('publicaciones', [])
    if publicaciones:
        print(f"\n📸 PUBLICACIONES ({len(publicaciones)}):")
        print("-" * 80)
        
        for idx, post in enumerate(publicaciones, 1):
            print(f"\n{idx}. 📌 {post.get('url', 'N/A')}")
            print(f"   Tipo: {post.get('tipo', 'N/A')}")
            
            if post.get('likes'):
                print(f"   ❤️ Likes: {post.get('likes')}")
            
            if post.get('descripcion'):
                desc = post.get('descripcion')[:150]
                print(f"   📝 Descripción: {desc}...")
            
            if post.get('fecha'):
                print(f"   📅 Fecha: {post.get('fecha')}")
            
            if post.get('hashtags'):
                hashtags_str = ', '.join(post.get('hashtags')[:5])
                print(f"   #️⃣ Hashtags: {hashtags_str}")
            
            if post.get('menciones'):
                menciones_str = ', '.join(post.get('menciones')[:5])
                print(f"   @️⃣ Menciones: {menciones_str}")
            
            if post.get('imagenes'):
                print(f"   🖼️ Imágenes descargadas: {len(post.get('imagenes'))}")
                for img in post.get('imagenes')[:2]:
                    if img.get('local_path'):
                        print(f"      📁 {img.get('local_path')}")
                    if img.get('url'):
                        print(f"      🔗 {img.get('url')[:80]}...")
            
            if post.get('comentarios'):
                print(f"   💬 Comentarios ({len(post.get('comentarios'))}):")
                for comment in post.get('comentarios')[:2]:
                    print(f"      • {comment[:80]}...")
            
            if post.get('error'):
                print(f"   ❌ Error: {post.get('error')}")
            
            print("-" * 40)
    
    print("\n" + "="*80)
    print("✅ Scraping completado!")
    print("="*80 + "\n")

def save_pretty_json(data, filename):
    """Guarda el JSON con formato bonito"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)