import time

def scrape_profile_info(page, username):
    """Extrae información del perfil"""
    profile_url = f"https://www.instagram.com/{username}/"
    print(f"🔍 Navegando a {profile_url}")
    page.goto(profile_url)
    page.wait_for_timeout(4000)
    
    profile_data = {
        'username': username,
        'bio': 'No disponible',
        'posts_count': 'N/A',
        'followers_count': 'N/A',
        'following_count': 'N/A'
    }
    
    # Extraer nombre de usuario
    try:
        username_elem = page.locator("header h1, header h2").first
        if username_elem:
            profile_data['username'] = username_elem.inner_text()
    except:
        pass
    
    # Extraer biografía
    bio_selectors = ["div._aa_6 span", "header section span"]
    for selector in bio_selectors:
        try:
            if page.locator(selector).count() > 0:
                bio = page.locator(selector).first.inner_text()
                if bio and len(bio) > 3:
                    profile_data['bio'] = bio[:500]
                    break
        except:
            continue
    
    # Extraer estadísticas
    try:
        # Buscar números en spans
        numbers = page.locator("header span, header li span").all()
        nums = []
        for span in numbers:
            try:
                text = span.inner_text()
                if text and any(c.isdigit() for c in text):
                    clean = text.split()[0] if ' ' in text else text
                    nums.append(clean)
            except:
                continue
        
        if len(nums) >= 3:
            profile_data['posts_count'] = nums[0]
            profile_data['followers_count'] = nums[1]
            profile_data['following_count'] = nums[2]
    except:
        pass
    
    print(f"📊 Datos: {profile_data['followers_count']} seguidores, {profile_data['posts_count']} posts")
    return profile_data