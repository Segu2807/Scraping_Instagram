let currentData = null;

// Cargar datos desde el archivo JSON
async function loadData() {
    showLoading(true);
    hideError();
    
    try {
        const response = await fetch('/api/data');
        if (response.ok) {
            currentData = await response.json();
            renderData(currentData);
        } else {
            throw new Error('No se pudo cargar el archivo');
        }
    } catch (error) {
        console.error('Error:', error);
        showError('No se encontró el archivo de datos. Por favor, carga un archivo JSON manualmente.');
        // Mostrar demo con datos de ejemplo
        showDemoData();
    } finally {
        showLoading(false);
    }
}

// Mostrar datos de ejemplo para demostración
function showDemoData() {
    const demoData = {
        perfil: {
            username: "nasa",
            bio: "Explore the universe and discover our home planet",
            posts_count: "4761",
            followers_count: "89.5M",
            following_count: "342"
        },
        publicaciones: [
            {
                url: "https://instagram.com/p/example1",
                tipo: "imagen",
                likes: "1.2M",
                descripcion: "¡Bienvenidos al dashboard de Instagram Scraper! Aquí podrás visualizar todos los datos extraídos de Instagram de forma clara y ordenada.",
                fecha: "2026-04-22T15:10:59.000Z",
                hashtags: ["NASA", "Space", "Earth"],
                menciones: ["nasa", "spacex"],
                imagenes: [],
                comentarios: ["¡Increíble!", "Me encanta"]
            }
        ]
    };
    renderData(demoData);
    showError("⚠️ Datos de demostración - Carga un archivo JSON real usando el botón 'Cargar JSON'");
}

// Cargar desde archivo local
function loadFromFile(file) {
    showLoading(true);
    hideError();
    
    const reader = new FileReader();
    reader.onload = function(e) {
        try {
            currentData = JSON.parse(e.target.result);
            renderData(currentData);
        } catch (error) {
            showError('Error al parsear el JSON: ' + error.message);
        } finally {
            showLoading(false);
        }
    };
    reader.onerror = function() {
        showError('Error al leer el archivo');
        showLoading(false);
    };
    reader.readAsText(file);
}

// Renderizar todos los datos
function renderData(data) {
    if (data.perfil) {
        renderProfile(data.perfil);
    }
    
    if (data.publicaciones) {
        renderPosts(data.publicaciones);
    }
    
    document.getElementById('profile').classList.remove('hidden');
    document.getElementById('timeline').classList.remove('hidden');
}

// Renderizar perfil
function renderProfile(perfil) {
    const username = perfil.username || perfil || 'usuario';
    document.getElementById('profileUsername').textContent = `@${typeof username === 'string' ? username : (username.username || 'usuario')}`;
    document.getElementById('profileBio').textContent = perfil.bio || 'Sin biografía disponible';
    document.getElementById('statPosts').textContent = formatNumber(perfil.posts_count);
    document.getElementById('statFollowers').textContent = formatNumber(perfil.followers_count);
    document.getElementById('statFollowing').textContent = formatNumber(perfil.following_count);
    
    const initial = (typeof username === 'string' ? username[0] : 'U').toUpperCase();
    document.getElementById('profileAvatar').textContent = initial;
}

// Renderizar posts
function renderPosts(posts) {
    const container = document.getElementById('postsContainer');
    container.innerHTML = '';
    
    if (!posts || posts.length === 0) {
        container.innerHTML = '<p style="color:white; text-align:center; grid-column:1/-1;">No hay publicaciones para mostrar</p>';
        return;
    }
    
    posts.forEach((post, index) => {
        const postCard = createPostCard(post, index);
        container.appendChild(postCard);
    });
}

// Crear tarjeta de post
function createPostCard(post, index) {
    const card = document.createElement('div');
    card.className = 'post-card';
    card.onclick = () => showModal(post);
    
    // Determinar el texto a mostrar
    let displayText = post.descripcion || post.caption || '';
    if (!displayText && post.likes && typeof post.likes === 'string') {
        // Si no hay descripción, usar el texto de likes que puede contener la descripción
        displayText = post.likes;
    }
    
    // Limpiar texto (quitar emojis extraños)
    displayText = displayText.replace(/[⁣]/g, '').trim();
    
    const shortCaption = displayText.substring(0, 120);
    const hasMore = displayText.length > 120;
    
    // Likes display
    let likesDisplay = 'Sin likes';
    if (post.likes) {
        if (typeof post.likes === 'string') {
            likesDisplay = post.likes.substring(0, 30);
        } else if (typeof post.likes === 'number') {
            likesDisplay = formatNumber(post.likes);
        }
    }
    
    card.innerHTML = `
        <div class="post-image-placeholder">📸</div>
        <div class="post-content">
            <div class="post-caption">${escapeHtml(shortCaption)}${hasMore ? '...' : ''}</div>
            <div class="post-meta">
                <span class="post-likes">❤️ ${escapeHtml(likesDisplay)}</span>
                <span>📅 ${formatDate(post.fecha)}</span>
            </div>
        </div>
    `;
    
    return card;
}

// Mostrar modal con detalles del post
function showModal(post) {
    const modal = document.getElementById('postModal');
    const modalBody = document.getElementById('modalBody');
    
    // Obtener el texto completo
    let fullText = post.descripcion || post.caption || '';
    if (!fullText && post.likes && typeof post.likes === 'string') {
        fullText = post.likes;
    }
    fullText = fullText.replace(/[⁣]/g, '').trim();
    
    // Hashtags
    let hashtagsHtml = '';
    if (post.hashtags && post.hashtags.length > 0) {
        hashtagsHtml = `
            <div class="modal-hashtags">
                ${post.hashtags.map(tag => `<span class="hashtag">#${escapeHtml(tag)}</span>`).join('')}
            </div>
        `;
    }
    
    // Menciones
    let mencionesHtml = '';
    if (post.menciones && post.menciones.length > 0) {
        mencionesHtml = `
            <div class="modal-hashtags">
                ${post.menciones.map(mention => `<span class="hashtag">@${escapeHtml(mention)}</span>`).join('')}
            </div>
        `;
    }
    
    // Comentarios
    let comentariosHtml = '';
    if (post.comentarios && post.comentarios.length > 0) {
        comentariosHtml = `
            <div style="margin-top: 15px;">
                <strong>💬 Comentarios (${post.comentarios.length}):</strong>
                <ul style="margin-top: 10px; list-style: none; padding-left: 0;">
                    ${post.comentarios.map(c => `<li style="margin-bottom: 8px; padding: 8px; background: #f5f5f5; border-radius: 8px;">${escapeHtml(c.substring(0, 200))}</li>`).join('')}
                </ul>
            </div>
        `;
    }
    
    modalBody.innerHTML = `
        <div class="modal-image-placeholder">📸</div>
        <div class="modal-caption">${escapeHtml(fullText)}</div>
        ${hashtagsHtml}
        ${mencionesHtml}
        <div class="modal-meta">
            <span>❤️ ${escapeHtml(post.likes || 'N/A')}</span>
            <span>📅 ${formatDate(post.fecha)}</span>
            <span>🔗 <a href="${post.url}" target="_blank">Ver en Instagram</a></span>
        </div>
        ${comentariosHtml}
    `;
    
    modal.classList.remove('hidden');
    
    const closeBtn = modal.querySelector('.close');
    closeBtn.onclick = () => modal.classList.add('hidden');
    modal.onclick = (e) => {
        if (e.target === modal) modal.classList.add('hidden');
    };
}

// Utilidades
function formatNumber(num) {
    if (!num || num === 'N/A') return '0';
    const str = num.toString();
    // Si ya tiene formato K/M, devolverlo
    if (str.includes('K') || str.includes('M')) return str;
    const n = parseInt(str.replace(/[^0-9]/g, ''));
    if (isNaN(n)) return str;
    if (n >= 1000000) return (n / 1000000).toFixed(1) + 'M';
    if (n >= 1000) return (n / 1000).toFixed(1) + 'K';
    return n.toString();
}

function formatDate(dateStr) {
    if (!dateStr) return 'Fecha desconocida';
    try {
        const date = new Date(dateStr);
        return date.toLocaleDateString('es-ES', { year: 'numeric', month: 'short', day: 'numeric' });
    } catch {
        return dateStr;
    }
}

function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function showLoading(show) {
    const loading = document.getElementById('loading');
    if (show) {
        loading.classList.remove('hidden');
    } else {
        loading.classList.add('hidden');
    }
}

function showError(message) {
    const error = document.getElementById('error');
    error.textContent = message;
    error.classList.remove('hidden');
    setTimeout(() => {
        error.classList.add('hidden');
    }, 5000);
}

function hideError() {
    document.getElementById('error').classList.add('hidden');
}

// Event Listeners
document.getElementById('refreshBtn').addEventListener('click', loadData);
document.getElementById('fileInput').addEventListener('change', (e) => {
    if (e.target.files[0]) {
        loadFromFile(e.target.files[0]);
    }
});

// Cargar datos automáticamente al iniciar
loadData();