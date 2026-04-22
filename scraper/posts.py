import time
import re
import os
from playwright.sync_api import sync_playwright

def extract_hashtags_and_mentions(text):
    """Extrae hashtags y menciones del texto"""
    if not text:
        return [], []
    hashtags = re.findall(r'#([\w\u00f1\u00d1]+)', text)
    mentions = re.findall(r'@([\w\u00f1\u00d1]+)', text)
    return list(set(hashtags)), list(set(mentions))

def download_image_with_playwright(page, img_url, post_id, index, download_folder="downloads"):
    """Descarga imágenes usando Playwright (evita bloqueo 403)"""
    if not img_url:
        return None
    
    os.makedirs(download_folder, exist_ok=True)
    
    # Limpiar URL para obtener mejor calidad
    if '?' in img_url:
        base_url = img_url.split('?')[0]
    else:
        base_url = img_url
    
    # Intentar obtener máxima calidad
    if '150x150' in base_url or '320x320' in base_url:
        base_url = base_url.replace('150x150', '1080x1080').replace('320x320', '1080x1080')
    
    filename = f"{post_id}_img_{index}.jpg"
    filepath = os.path.join(download_folder, filename)
    
    # Si ya existe, no descargar de nuevo
    if os.path.exists(filepath):
        print(f"      ℹ️ Imagen ya existe: {filename}")
        return filepath
    
    try:
        # Usar la página actual para navegar directamente a la imagen
        # Esto usa las cookies y sesión activa de Instagram
        response = page.goto(base_url, timeout=15000)
        
        if response and response.status == 200:
            # Obtener el contenido binario
            img_data = response.body()
            
            # Verificar que sea una imagen válida (mínimo 1KB)
            if len(img_data) > 1024:
                with open(filepath, 'wb') as f:
                    f.write(img_data)
                print(f"      ✅ Imagen descargada: {filename} ({len(img_data)/1024:.1f} KB)")
                return filepath
            else:
                print(f"      ⚠️ Imagen muy pequeña ({len(img_data)} bytes), puede ser inválida")
                return None
        else:
            print(f"      ⚠️ Error HTTP {response.status if response else 'No response'}")
            return None
            
    except Exception as e:
        print(f"      ⚠️ Error descargando: {str(e)[:80]}")
        return None

def extract_post_details(page, post_url, download_images=True):
    """Extrae todos los detalles de un post usando Playwright"""
    print(f"   📸 Procesando: {post_url[:60]}...")
    
    try:
        # Navegar al post
        page.goto(post_url, timeout=15000)
        page.wait_for_timeout(3500)  # Esperar más tiempo para que carguen las imágenes
        
        post_id = post_url.split('/p/')[1].split('/')[0]
        
        # Extraer tipo
        post_type = "imagen"
        try:
            if page.locator("video").count() > 0:
                post_type = "video"
        except:
            pass
        
        # Extraer likes
        likes = None
        like_selectors = [
            "a[href$='/liked_by/'] span",
            "span.html-span:has-text('likes')",
            "div[role='button'] span:has-text('like')",
            "section span:has-text(','), section span:has-text('K')"
        ]
        for selector in like_selectors:
            try:
                likes_elem = page.locator(selector).first
                if likes_elem:
                    likes_text = likes_elem.inner_text()
                    if likes_text and any(c.isdigit() for c in likes_text):
                        likes = likes_text
                        break
            except:
                continue
        
        # Extraer descripción
        description = None
        caption_selectors = [
            "div._a9zr h1 span",
            "div.x1i10hfl span",
            "h1 span[dir='auto']",
            "div[data-testid='post-container'] div span"
        ]
        for selector in caption_selectors:
            try:
                if page.locator(selector).count() > 0:
                    desc_text = page.locator(selector).first.inner_text()
                    if desc_text and len(desc_text) > 5:
                        description = desc_text
                        break
            except:
                continue
        
        # Extraer fecha
        fecha = None
        try:
            time_elem = page.locator("time").first
            if time_elem:
                fecha = time_elem.get_attribute("datetime")
        except:
            pass
        
        # Extraer hashtags y menciones
        hashtags = []
        menciones = []
        if description:
            hashtags, menciones = extract_hashtags_and_mentions(description)
        
        # 🔥 SECCIÓN CRÍTICA: Extraer imágenes
        imagenes = []
        if download_images:
            try:
                # Múltiples selectores para encontrar imágenes en Instagram
                img_selectors = [
                    "article img[decoding='async']",
                    "div[class*='_aagv'] img",
                    "img[class*='x5yr21d']",
                    "div[role='presentation'] img",
                    "img[style*='object-fit']"
                ]
                
                found_images = set()  # Para evitar duplicados
                
                for selector in img_selectors:
                    try:
                        img_elements = page.locator(selector).all()
                        for idx, img in enumerate(img_elements[:5]):
                            try:
                                # Obtener URL de la imagen
                                img_url = img.get_attribute("src")
                                
                                # Si no hay src, probar con srcset
                                if not img_url or 'blank' in img_url:
                                    srcset = img.get_attribute("srcset")
                                    if srcset:
                                        urls = re.findall(r'(https?://[^\s]+)', srcset)
                                        if urls:
                                            # Tomar la URL de mayor calidad (última en la lista)
                                            img_url = urls[-1]
                                
                                # Verificar que sea una URL válida de Instagram
                                if img_url and ('cdninstagram.com' in img_url or 'fbcdn.net' in img_url):
                                    # Evitar duplicados
                                    if img_url not in found_images:
                                        found_images.add(img_url)
                                        
                                        # Descargar usando Playwright
                                        local_path = download_image_with_playwright(page, img_url, post_id, idx, "downloads")
                                        if local_path:
                                            imagenes.append({
                                                "url": img_url,
                                                "local_path": local_path,
                                                "orden": len(imagenes)
                                            })
                                            print(f"      🖼️ Imagen {len(imagenes)} guardada")
                                            break  # Una imagen por post es suficiente
                            except Exception as e:
                                continue
                    except:
                        continue
                
                if not imagenes:
                    print(f"      ⚠️ No se encontraron imágenes para este post")
                    
            except Exception as e:
                print(f"      ⚠️ Error extrayendo imágenes: {str(e)[:80]}")
        
        # Extraer comentarios
        comentarios = []
        try:
            comment_selectors = [
                "div._a9zr div span",
                "div.x1i10hfl div span",
                "ul div span",
                "div[data-testid='post-container'] div span"
            ]
            for selector in comment_selectors:
                try:
                    comments = page.locator(selector).all()
                    for comment in comments[:5]:
                        comment_text = comment.inner_text()
                        if comment_text and len(comment_text) > 5 and 'likes' not in comment_text.lower():
                            if comment_text not in comentarios:
                                comentarios.append(comment_text[:200])
                    if comentarios:
                        break
                except:
                    continue
        except:
            pass
        
        return {
            "url": post_url,
            "tipo": post_type,
            "likes": likes,
            "descripcion": description[:500] if description else None,
            "fecha": fecha,
            "hashtags": hashtags[:10],
            "menciones": menciones[:10],
            "imagenes": imagenes,
            "comentarios": comentarios[:5],
            "post_id": post_id
        }
        
    except Exception as e:
        print(f"   ❌ Error en post: {str(e)[:100]}")
        return {
            "url": post_url,
            "error": str(e),
            "tipo": "error",
            "imagenes": []
        }

def scroll_and_get_links(page, max_posts=20):
    """Recolecta enlaces de publicaciones"""
    post_links = []
    last_height = 0
    no_new_posts_count = 0
    
    print(f"📜 Buscando {max_posts} posts...")
    
    # Esperar carga inicial
    page.wait_for_timeout(3000)
    
    # Cerrar posibles popups
    try:
        page.locator("div[role='button']:has-text('Ahora no')").click()
        page.wait_for_timeout(1000)
    except:
        pass
    
    while len(post_links) < max_posts and no_new_posts_count < 20:
        new_found = 0
        
        # Buscar enlaces de posts
        try:
            links = page.locator("a[href*='/p/']").all()
            for link in links:
                try:
                    href = link.get_attribute("href")
                    if href and '/p/' in href:
                        if href.startswith('/'):
                            full_url = f"https://www.instagram.com{href}"
                        else:
                            full_url = href
                        
                        full_url = full_url.split('/?')[0]
                        
                        if full_url not in post_links and '/p/' in full_url:
                            post_links.append(full_url)
                            new_found += 1
                except:
                    continue
        except:
            pass
        
        if new_found > 0:
            print(f"   ✅ Encontrados {len(post_links)} posts...")
            no_new_posts_count = 0
        else:
            no_new_posts_count += 1
            print(f"   🔄 Scroll {no_new_posts_count}/20...")
        
        # Scroll suave
        page.evaluate("window.scrollBy(0, window.innerHeight)")
        page.wait_for_timeout(2500)
        
        # Verificar fin de página
        new_height = page.evaluate("document.body.scrollHeight")
        if new_height == last_height and no_new_posts_count > 5:
            break
        last_height = new_height
    
    # Limpiar y devolver URLs únicas
    unique_links = []
    for link in post_links:
        if link not in unique_links:
            unique_links.append(link)
    
    print(f"✅ Total posts encontrados: {len(unique_links[:max_posts])}")
    return unique_links[:max_posts]