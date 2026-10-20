import os
import json
import unicodedata
import re
import html as html_lib
import random

BASE_DIR = os.path.expanduser("~/centro-comando-unificado")
JSON_PATH = os.path.join(BASE_DIR, "backend/catalogo.json")
OFERTAS_DIR = os.path.join(BASE_DIR, "frontend/ofertas")
BASE_URL = "https://osachadinhosdashopee.com.br"

def slugify(texto):
    if len(texto) > 80: texto = texto[:80]
    texto = unicodedata.normalize('NFD', texto).encode('ascii', 'ignore').decode('utf-8')
    texto = re.sub(r'[^\w\s-]', '', texto).strip().lower()
    return re.sub(r'[-\s]+', '-', texto)

print("🔄 Lendo o banco de dados...")
with open(JSON_PATH, 'r', encoding='utf-8') as f:
    catalogo = json.load(f)

if not os.path.exists(OFERTAS_DIR):
    os.makedirs(OFERTAS_DIR)

# O Template com CSS Grid Correto (Dois Cards Independentes)
template = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titulo} - Achadinhos da Shopee</title>
<meta name="description" content="{seo_texto}">
<link rel="canonical" href="{url}">
<style>
body { font-family: system-ui, -apple-system, sans-serif; background: #F5F5F5; margin: 0; padding: 20px; color: #1E293B; }
.header { position: sticky; top: 0; z-index: 100; display: flex; align-items: center; justify-content: center; padding: 12px 15px; background: #FFF; box-shadow: 0 2px 8px rgba(0,0,0,0.06); margin-bottom: 15px; }
.logo { font-size: 15px; font-weight: 800; color: #EE4D2D; text-decoration: none; letter-spacing: -0.5px; display: flex; align-items: center; gap: 5px; }
.logo span { font-size: 20px; }

/* CARROSSEL */
.carousel-outer-wrapper { position: relative; width: 100%; max-width: 100%; margin: 10px 0 40px 0; border-radius: 14px; overflow: hidden; background: #FFF; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
.carousel-inner-container { display: flex !important; height: 100%; width: 100%; transition: transform 0.5s ease-in-out; margin: 0; padding: 0; list-style: none; }
.carousel-slide-item { display: block; flex: 0 0 100%; width: 100%; height: 100%; cursor: pointer; }
.carousel-slide-item img { width: 100%; height: auto; object-fit: contain; display: block; }
.carousel-btn { position: absolute; top: 50%; transform: translateY(-50%); background: rgba(255,255,255,0.9); border: none; width: 38px; height: 38px; cursor: pointer; font-size: 18px; border-radius: 50%; z-index: 10; display: flex; align-items: center; justify-content: center; }
.carousel-btn.prev { left: 12px; } .carousel-btn.next { right: 12px; }
.carousel-dots { position: absolute; bottom: 12px; left: 50%; transform: translateX(-50%); display: flex; gap: 6px; z-index: 10; }
.dot { width: 8px; height: 8px; background: rgba(255,255,255,0.5); border-radius: 50%; cursor: pointer; transition: 0.3s; }
.dot.active { background: #EE4D2D; width: 22px; border-radius: 10px; }

/* LAYOUT GRID (DOIS CARDS) */
.grid-container { width: 100%; max-width: 100%; margin: 0; display: grid; grid-template-columns: 1fr; gap: 20px; }
@media (min-width: 992px) { 
    .grid-container { grid-template-columns: 1fr 1fr; } 
    .card-relacionado { display: flex !important; }
}

/* ESTILO DO CARD (BLOCO) */
.card-produto { background: #FFF; border-radius: 14px; padding: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); display: flex; flex-direction: column; overflow: hidden; }
.card-relacionado { display: none; }

h1 { font-size: 16px; margin: 0 0 15px 0; line-height: 1.4; color: #334155; font-weight: 600; }

.img-wrapper { width: 100%; aspect-ratio: 1 / 1; overflow: hidden; border-radius: 8px; margin-bottom: 15px; background: #F8FAFC; }
.img-wrapper img { width: 100%; height: 100%; object-fit: cover; display: block; }

.preco { font-size: 26px; font-weight: bold; color: #EE4D2D; margin-bottom: 15px; }
.caixa-seo { background: #F8FAFC; border-left: 4px solid #EE4D2D; padding: 12px; margin-bottom: 15px; border-radius: 4px; flex-grow: 1; }
.caixa-seo h2 { font-size: 14px; margin: 0 0 8px 0; color: #1E293B; }
.caixa-seo p { font-size: 13px; color: #64748B; margin: 0 0 8px 0; line-height: 1.4; }
.hashtags { font-size: 12px; color: #0284C7; font-weight: bold; }

/* ANÚNCIOS */
.adsterra-container { text-align: center; margin: 15px 0; overflow: hidden; min-height: 50px; }

/* BOTÃO */
.btn { display: block; text-align: center; background: #B82400; color: white; text-decoration: none; padding: 14px; border-radius: 8px; font-size: 16px; font-weight: bold; margin-top: auto; width: 100%; box-sizing: border-box; }
.voltar { display: block; text-align: center; margin-top: 15px; color: #64748B; text-decoration: none; font-size: 14px; }
</style>

    <!-- Google Analytics 4 -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-ZC0P2HWSN6"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('consent', 'default', {
        'ad_storage': 'denied', 'ad_user_data': 'denied',
        'ad_personalization': 'denied', 'analytics_storage': 'denied'
      });
      gtag('js', new Date());
      gtag('config', 'G-ZC0P2HWSN6');
    </script>
</head>
<body>
    <div class="header"><a href="/" class="logo"><span>🛒</span> ACHADINHOS DA SHOPEE</a></div>
    
    <div class="carousel-outer-wrapper" id="carouselOuterWrapper">
      <div class="carousel-inner-container" id="banners-carrossel">
        <a class="carousel-slide-item" href="/"><img src="/assets/banner_1.webp" alt="Banner 1" fetchpriority="high"></a>
        <a class="carousel-slide-item" href="/"><img src="/assets/banner_2.webp" alt="Banner 2"></a>
      </div>
      <button class="carousel-btn prev" onclick="moveSlide(-1)">&#10094;</button>
      <button class="carousel-btn next" onclick="moveSlide(1)">&#10095;</button>
      <div class="carousel-dots" id="carouselDots"></div>
    </div>

    <div class="grid-container">
        <!-- CARD 1: PRODUTO PRINCIPAL -->
        <div class="card-produto">
            <h1>{titulo}</h1>
            <div class="img-wrapper"><img src="{imagem}" alt="{titulo}"></div>
            <div class="preco">R$ {preco}</div>
            <div class="caixa-seo">
                <h2>Por que comprar este produto?</h2>
                <p>{seo_texto}</p>
                <div class="hashtags">{hashtags_string}</div>
            </div>
            <div class="adsterra-container">
                <script data-cfasync="false">atOptions = {'key' : 'cd33c28fa30e9169704719566273bd0a','format' : 'iframe','height' : 90,'width' : 728,'params' : {}};</script>
                <script data-cfasync="false" src="https://www.highrevenueformat.com/cd33c28fa30e9169704719566273bd0a/invoke.js"></script>
            </div>
            <a href="{link_afiliado}" rel="nofollow sponsored" target="_blank" class="btn">🛒 Comprar na Shopee</a>
            <a href="/" class="voltar">← Voltar para a vitrine</a>
        </div>

        <!-- CARD 2: PRODUTO RELACIONADO -->
        <div class="card-produto card-relacionado">
            <h1>{titulo_relacionado}</h1>
            <div class="img-wrapper"><img src="{imagem_relacionada}" alt="{titulo_relacionado}"></div>
            <div class="preco">R$ {preco_relacionado}</div>
            <div class="caixa-seo">
                <h2>Por que comprar este produto?</h2>
                <p>{seo_texto_relacionado}</p>
                <div class="hashtags">{hashtags_relacionadas}</div>
            </div>
            <div class="adsterra-container">
                <script data-cfasync="false">atOptions = {'key' : 'cd33c28fa30e9169704719566273bd0a','format' : 'iframe','height' : 90,'width' : 728,'params' : {}};</script>
                <script data-cfasync="false" src="https://www.highrevenueformat.com/cd33c28fa30e9169704719566273bd0a/invoke.js"></script>
            </div>
            <a href="{link_afiliado_relacionado}" rel="nofollow sponsored" target="_blank" class="btn">🛒 Comprar na Shopee</a>
            <a href="/" class="voltar">← Voltar para a vitrine</a>
        </div>
    </div>

<script>
  let currentSlide = 0;
  const slides = document.querySelectorAll('.carousel-slide-item');
  const carouselInner = document.getElementById('banners-carrossel');
  const dotsContainer = document.getElementById('carouselDots');
  if(slides.length > 0) { slides.forEach((_, index) => { const dot = document.createElement('span'); dot.className = 'dot' + (index === 0 ? ' active' : ''); dot.onclick = () => goToSlide(index); dotsContainer.appendChild(dot); }); }
  function goToSlide(index) { currentSlide = index; carouselInner.style.transform = `translateX(-${currentSlide * 100}%)`; document.querySelectorAll('.dot').forEach((dot, i) => dot.classList.toggle('active', i === currentSlide)); }
  window.moveSlide = (dir) => { let newIndex = currentSlide + dir; if (newIndex >= slides.length) newIndex = 0; if (newIndex < 0) newIndex = slides.length - 1; goToSlide(newIndex); };
  setInterval(() => moveSlide(1), 5000);
</script>
</body>
</html>"""

print("🚀 GERANDO PÁGINAS COM LAYOUT DUPLO CORRIGIDO...")
count = 0

for index, p in enumerate(catalogo):
    try:
        # Pega o próximo produto para ser o relacionado
        p_rel = catalogo[index + 1] if index + 1 < len(catalogo) else catalogo[0]
        
        # --- DADOS DO PRODUTO 1 ---
        titulo = str(p.get('productName', 'Produto'))
        imagem = str(p.get('imageUrl', ''))
        preco = f"{float(p.get('priceMin', 0)):.2f}".replace('.', ',')
        link = str(p.get('offerLink', '#'))
        item_id = str(p.get('itemId', ''))
        cat = str(p.get('categoria', 'Achadinhos'))
        
        introducoes = [f"Você está procurando por {titulo}?", f"Conheça o incrível {titulo}!", f"Aproveite esta oportunidade para adquirir {titulo}.", f"O {titulo} é a escolha perfeita."]
        seo_texto = f"{random.choice(introducoes)} Este produto da categoria {cat} tem um custo-benefício imbatível. Garanta já o seu com desconto!"
        
        palavras = [w.capitalize() for w in re.findall(r'\b\w{4,}\b', titulo) if w.lower() not in ['com', 'para', 'sem', 'tamanho', 'cores', 'tam', 'unico', 'kit']]
        hashtags_string = f"{' '.join([f'#{w}' for w in palavras[:3]])} #{cat.replace(' ', '')} #Shopee #Ofertas"
        
        slug = slugify(titulo)
        url_final = f"{BASE_URL}/ofertas/{slug}-{item_id}.html"

        # --- DADOS DO PRODUTO 2 (RELACIONADO) ---
        titulo_rel = str(p_rel.get('productName', 'Produto Relacionado'))
        imagem_rel = str(p_rel.get('imageUrl', ''))
        preco_rel = f"{float(p_rel.get('priceMin', 0)):.2f}".replace('.', ',')
        link_rel = str(p_rel.get('offerLink', '#'))
        cat_rel = str(p_rel.get('categoria', 'Achadinhos'))
        
        intro_rel = random.choice(introducoes)
        seo_texto_rel = f"{intro_rel} Este produto da categoria {cat_rel} tem um custo-benefício imbatível."
        
        palavras_rel = [w.capitalize() for w in re.findall(r'\b\w{4,}\b', titulo_rel) if w.lower() not in ['com', 'para', 'sem', 'tamanho', 'cores', 'tam', 'unico', 'kit']]
        hashtags_rel = f"{' '.join([f'#{w}' for w in palavras_rel[:3]])} #{cat_rel.replace(' ', '')} #Shopee #Ofertas"

        # --- SUBSTITUIÇÃO SEGURA ---
        html_final = template
        html_final = html_final.replace('{titulo}', html_lib.escape(titulo))
        html_final = html_final.replace('{imagem}', imagem)
        html_final = html_final.replace('{preco}', preco)
        html_final = html_final.replace('{seo_texto}', html_lib.escape(seo_texto))
        html_final = html_final.replace('{hashtags_string}', hashtags_string)
        html_final = html_final.replace('{link_afiliado}', link)
        html_final = html_final.replace('{url}', url_final)
        
        html_final = html_final.replace('{titulo_relacionado}', html_lib.escape(titulo_rel))
        html_final = html_final.replace('{imagem_relacionada}', imagem_rel)
        html_final = html_final.replace('{preco_relacionado}', preco_rel)
        html_final = html_final.replace('{seo_texto_relacionado}', html_lib.escape(seo_texto_rel))
        html_final = html_final.replace('{hashtags_relacionadas}', hashtags_rel)
        html_final = html_final.replace('{link_afiliado_relacionado}', link_rel)

        with open(os.path.join(OFERTAS_DIR, f"{slug}-{item_id}.html"), 'w', encoding='utf-8') as f:
            f.write(html_final)
        count += 1
    except Exception as e:
        pass

print(f"✅ {count} páginas geradas com o layout de 2 blocos perfeitos!")
