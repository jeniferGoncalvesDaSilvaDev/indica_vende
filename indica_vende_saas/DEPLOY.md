# Guia de Deploy no Render - IndicaVende API

Este guia mostra como fazer deploy do backend FastAPI no Render.

## 📋 Pré-requisitos

1. Conta no [Render](https://render.com) (gratuita)
2. Repositório no GitHub com o código
3. Python 3.10 ou superior

## 🚀 Passos para Deploy

### 1. Preparar o Repositório

Certifique-se de que seu repositório tenha os seguintes arquivos configurados:

- ✅ `render.yaml` - Configuração do Render (já está configurado)
- ✅ `backend/requirements.txt` - Dependências Python
- ✅ `.gitignore` - Arquivos a ignorar

### 2. Fazer Push para GitHub

```bash
git add .
git commit -m "Configurar para deploy no Render"
git push origin main
```

### 3. Conectar ao Render

1. Acesse [Render Dashboard](https://dashboard.render.com/)
2. Clique em **"New +"** → **"Blueprint"**
3. Conecte seu repositório GitHub
4. O Render detectará automaticamente o arquivo `render.yaml`
5. Clique em **"Apply"**

### 4. Configurar Variáveis de Ambiente (Opcional)

O Render já configurará automaticamente as variáveis definidas no `render.yaml`:

- `PYTHON_VERSION`: 3.10
- `SECRET_KEY`: Gerado automaticamente
- `ACCESS_TOKEN_EXPIRE_MINUTES`: 60
- `DATABASE_URL`: sqlite:///./indicavende.db

Se precisar adicionar novas variáveis:

1. Acesse seu serviço no Render
2. Vá em **"Environment"**
3. Adicione as variáveis necessárias

### 5. Deploy Automático

Após conectar o repositório:

- O Render fará o build automaticamente
- Instalará as dependências do `requirements.txt`
- Iniciará o servidor FastAPI
- Fornecerá uma URL pública (ex: `https://indicavende-api.onrender.com`)

## 🔄 Atualizações Automáticas

Com `autoDeploy: true` configurado, cada push na branch `main` dispara um novo deploy automaticamente.

## ⚠️ Importante: SQLite em Produção

**ATENÇÃO**: SQLite no Render **NÃO persiste dados** entre redeploys. Para produção, considere:

### Opção 1: Migrar para PostgreSQL (Recomendado)

1. No Render Dashboard, crie um **PostgreSQL Database** (gratuito disponível)
2. Copie a URL de conexão fornecida
3. Atualize a variável de ambiente `DATABASE_URL` no seu serviço
4. Modifique `database.py` para remover `connect_args` (não necessário para PostgreSQL):

```python
engine = create_engine(SQLALCHEMY_DATABASE_URL)
```

### Opção 2: Manter SQLite com Limitações

Se optar por manter SQLite, saiba que:
- Dados serão perdidos a cada redeploy
- Não recomendado para produção
- Útil apenas para testes/desenvolvimento

## 📝 Logs e Monitoramento

Para ver logs da aplicação:

1. Acesse seu serviço no Render
2. Clique em **"Logs"**
3. Veja logs em tempo real

## 🔗 Acessar a API

Após o deploy bem-sucedido:

- **URL da API**: `https://[seu-servico].onrender.com`
- **Documentação Interativa**: `https://[seu-servico].onrender.com/docs`
- **OpenAPI Schema**: `https://[seu-servico].onrender.com/openapi.json`

## 🐛 Troubleshooting

### Erro: "Application failed to start"

1. Verifique os logs no Render Dashboard
2. Confirme que `requirements.txt` tem todas as dependências
3. Verifique se o caminho do `startCommand` está correto

### Erro: "Port already in use"

- O Render define automaticamente a variável `$PORT`
- Certifique-se de que o comando usa `--port $PORT`

### Problemas com Banco de Dados

- Verifique a variável `DATABASE_URL`
- Para SQLite: dados não persistem entre deploys
- Considere migrar para PostgreSQL

## 📚 Recursos Adicionais

- [Documentação Render](https://render.com/docs)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Render Blueprint Spec](https://render.com/docs/blueprint-spec)

---

✅ **Deploy Concluído!** Sua API FastAPI está rodando no Render.
