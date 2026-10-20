const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');

const DB_FILE = path.join(__dirname, 'catalogo.json');
const TMP_FILE = path.join(__dirname, 'catalogo.json.tmp');

const aberturas = ["Descubra o", "Conheça o", "Aproveite o", "Não perca o", "Encontramos o", "Selecionamos o"];
const fechamentos = ["por um preço incrível na Shopee.", "com um custo-benefício imbatível.", "ideal para o seu dia a dia.", "que está fazendo muito sucesso."];

let gerandoHtml = false;

function normalizar(texto) {
    return texto ? texto.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase() : "";
}

function aplicarSEO() {
    if (!fs.existsSync(DB_FILE)) return;

    let catalogo = [];
    try {
        catalogo = JSON.parse(fs.readFileSync(DB_FILE, 'utf8'));
    } catch (e) {
        return; // Se o arquivo estiver sendo escrito pelo Garimpeiro, espera o próximo ciclo
    }

    let alterou = false;

    catalogo.forEach(p => {
        // Se não tem texto de SEO ou tem menos de 10 caracteres
        if (!p.seo_text || p.seo_text.length < 10) {
            const ab = aberturas[Math.floor(Math.random() * aberturas.length)];
            const fe = fechamentos[Math.floor(Math.random() * fechamentos.length)];
            p.seo_text = `${ab} ${p.productName}, ${fe}`;
            alterou = true;
        }

        // Se não tem hashtags ou a hashtag é a genérica antiga
        if (!p.hashtags || p.hashtags.length === 0 || p.hashtags.includes("#AchadinhosDaShopee")) {
            const palavras = normalizar(p.productName).split(/\s+/).filter(w => w.length > 4 && !['para', 'com', 'sem', 'dos', 'das'].includes(w));
            const tags = palavras.slice(0, 4).map(w => `#${w.charAt(0).toUpperCase() + w.slice(1)}`);
            p.hashtags = tags.length > 0 ? tags : ["#Oferta", "#Shopee"];
            alterou = true;
        }
    });

    if (alterou) {
        try {
            // Salva de forma atômica para não corromper
            fs.writeFileSync(TMP_FILE, JSON.stringify(catalogo, null, 2));
            fs.renameSync(TMP_FILE, DB_FILE);
            console.log(`🤖 [Auto-SEO] Textos e hashtags aplicados!`);

            // Chama o Python para gerar as páginas HTML
            if (!gerandoHtml) {
                gerandoHtml = true;
                exec('python3 gerador_seo.py', { cwd: __dirname }, (err, stdout, stderr) => {
                    gerandoHtml = false;
                    if (err) console.error("❌ Erro no gerador HTML:", err.message);
                    else console.log(`✅ [Auto-SEO] Páginas HTML atualizadas no disco!`);
                });
            }
        } catch (e) {
            console.log("⚠️ Erro ao salvar banco no Auto-SEO:", e.message);
        }
    }
}

console.log("🚀 AGENTE SEO AUTOMÁTICO INICIADO (RODA A CADA 10s)");
setInterval(aplicarSEO, 10000);
aplicarSEO(); // Roda a primeira vez agora
