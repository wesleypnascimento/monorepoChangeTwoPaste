# monorepoChangeTwoPaste

Repositório para testar builds em pastas diferentes e verificar se o Jenkins
reconhece em qual pasta houve alteração.

## Estrutura

- `apps/server`: API HTTP em Python, sem dependências externas.
- `apps/web`: página HTML que envia nome e sobrenome para a API e mostra o
  resultado.

## Executar localmente

É necessário ter Python 3 instalado.

1. Em um terminal, inicie a API:

   ```bash
   python3 apps/server/server.py
   ```

2. Em outro terminal, na raiz do repositório, inicie a página:

   ```bash
   python3 -m http.server 5500 --directory apps/web
   ```

3. Acesse <http://localhost:5500>, preencha os campos e clique em **Juntar
   nomes**.

A API fica disponível em `http://localhost:3000`. Para alterar a porta, defina
a variável de ambiente `PORT` antes de iniciar o servidor.

## Teste de mudanças no Jenkins

O frontend e o backend ficam em diretórios independentes. Assim, um pipeline
pode observar `apps/web/**` e `apps/server/**` em etapas distintas.
