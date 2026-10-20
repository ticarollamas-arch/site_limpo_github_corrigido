import os
import glob
import re
import unicodedata

DIR = os.path.expanduser("~/centro-comando-unificado/frontend/ofertas")
arquivos = glob.glob(os.path.join(DIR, "*.html"))

print(f"🚀 OTIMIZANDO METATAGS E REESCREVENDO {len(arquivos)} PÁGINAS...")

count = 0
for arq in arquivos:
    try:
        with open(arq, 'r', encoding='utf-8') as f:
            html = f.read()

        # 1. GARANTE O NOFOLLOW EM TODOS OS LINKS DA SHOPEE
        pattern_nofollow = re.compile(r'<a\s+(?![^>]*rel=")([^>]*href="https?://(?:s\.)?shopee\.com\.br[^>]*)>', re.IGNORECASE)
        html = pattern_nofollow.sub(r'<a rel="nofollow sponsored" \1>', html)

        # 2. OTIMIZA A META DESCRIPTION (Se estiver curta)
        # Pega o título do produto para usar como base se a meta estiver curta
        match_title = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
        if match_title:
            titulo = match_title.group(1).replace(" | Achadinhos da Shopee", "").strip()
            desc_padrao = f"Confira o {titulo} na Shopee com o melhor preço. Aproveite as ofertas selecionadas dos Achadinhos da Shopee e economize hoje mesmo!"
            
            # Substitui a meta description se ela existir e for muito curta
            match_desc = re.search(r'<meta\s+name="description"\s+content="(.*?)"', html, re.IGNORECASE)
            if match_desc:
                desc_atual = match_desc.group(1)
                if len(desc_atual) < 50:
                    html = html.replace(f'<meta name="description" content="{desc_atual}"', f'<meta name="description" content="{desc_padrao}"')
            else:
                # Se não existir, injeta antes do </head>
                html = html.replace('</head>', f'    <meta name="description" content="{desc_padrao}">\n</head>')

        # 3. SALVA O ARQUIVO
        with open(arq, 'w', encoding='utf-8') as f:
            f.write(html)
        
        count += 1
    except Exception as e:
        print(f"⚠️ Erro ao processar {os.path.basename(arq)}: {e}")

print(f"🎉 SUCESSO! {count} páginas foram otimizadas com título, descrição e nofollow corretos.")
