const express = require('express');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = Number(process.env.PORT) || 3001;
const dbFile = path.join(__dirname, 'catalogo.json');
let catalogoCache = [];
let produtosPorId = new Map();
let ultimaFalhaBanco = null;

function carregarBanco() {
    try {
        if (!fs.existsSync(dbFile)) {
            catalogoCache = [];
            produtosPorId = new Map();
            ultimaFalhaBanco = `Arquivo de catálogo ausente: ${dbFile}`;
            return;
        }
        const dados = JSON.parse(fs.readFileSync(dbFile, 'utf8'));
        if (!Array.isArray(dados)) throw new Error('O catálogo precisa conter uma lista JSON.');
        const novoMapa = new Map();
        for (const produto of dados) {
            if (produto && produto.itemId != null) novoMapa.set(String(produto.itemId), produto);
        }
        catalogoCache = dados;
        produtosPorId = novoMapa;
        ultimaFalhaBanco = null;
    } catch (e) {
        // Preserve o último catálogo válido caso uma atualização esteja incompleta.
        ultimaFalhaBanco = e.message;
        console.error('[Catálogo] Não foi possível atualizar o catálogo:', e.message);
    }
}

carregarBanco();
setInterval(carregarBanco, 120000).unref();

app.get('/api/health', (req, res) => {
    res.setHeader('Cache-Control', 'no-store');
    res.json({ ok: !ultimaFalhaBanco, totalProdutos: catalogoCache.length, erroCatalogo: ultimaFalhaBanco });
});

app.get('/api/catalogo', (req, res) => {
    res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate');
    const page = Math.max(1, Number.parseInt(req.query.page, 10) || 1);
    const limit = Math.min(100, Math.max(1, Number.parseInt(req.query.limit, 10) || 20));
    const q = String(req.query.q || '').trim().toLocaleLowerCase('pt-BR');
    const cat = String(req.query.cat || 'Todos');

    let filtrado = catalogoCache;
    if (q) filtrado = filtrado.filter(p => String(p?.productName || '').toLocaleLowerCase('pt-BR').includes(q));
    if (cat !== 'Todos') filtrado = filtrado.filter(p => (p?.categoria || 'Novidades / Variedades') === cat);

    const inicio = (page - 1) * limit;
    res.json({ total: filtrado.length, page, data: filtrado.slice(inicio, inicio + limit) });
});

app.get('/api/produto/:id', (req, res) => {
    res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate');
    const prod = produtosPorId.get(String(req.params.id));
    if (prod) return res.json(prod);
    res.status(404).json({ error: 'Produto não encontrado' });
});

app.get('/api/admin/stats', (req, res) => {
    const comSEO = catalogoCache.filter(p => p && (p.seo_text || p.seo_texto)).length;
    res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate');
    res.json({ totalProdutos: catalogoCache.length, produtosComSEO: comSEO, velocidade: 0, memoria: Math.round(process.memoryUsage().rss / 1024 / 1024) + ' MB', erroCatalogo: ultimaFalhaBanco });
});

app.listen(PORT, '127.0.0.1', () => console.log(`API rodando na porta ${PORT}; catálogo carregado: ${catalogoCache.length} produtos`));
