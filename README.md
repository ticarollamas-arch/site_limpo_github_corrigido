# Achadinhos da Shopee — versão para GitHub

Este pacote contém o frontend e o backend do site, com correções de navegação para a página do produto, tratamento de falhas de carregamento e busca de produtos por ID indexada em memória.

## Importante sobre o catálogo

O arquivo `backend/catalogo.json` **não é incluído neste repositório** porque pode conter cerca de 145 mil produtos e é excluído pelo `.gitignore`. Para a API exibir os produtos, mantenha esse arquivo no servidor, em `backend/catalogo.json`, ou configure o processo de importação para criá-lo nesse caminho. Sem ele, a API retorna um catálogo vazio; o endpoint `/api/health` informa o estado.

## Instalação do backend

```bash
cd backend
npm install
npm start
```

Por padrão, a API escuta em `127.0.0.1:3001`, conforme a configuração atual do projeto. O Nginx deve encaminhar `/api/` para essa porta e servir os arquivos da pasta `frontend`.

## Segredos

Não coloque `.env`, chaves da Shopee, tokens, credenciais ou dados privados no GitHub. Configure as variáveis de ambiente diretamente no servidor. O `.gitignore` exclui `.env`, o catálogo e dependências.

## Rotas úteis

- `GET /api/health` — estado da API e quantidade de produtos carregados.
- `GET /api/catalogo?page=1&limit=20` — lista paginada.
- `GET /api/produto/ID_DO_ITEM` — detalhes de um produto.
