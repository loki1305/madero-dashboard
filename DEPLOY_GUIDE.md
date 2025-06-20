# 🌐 Guia de Deploy do Dashboard Grupo Madero no Render.com

Este guia te ajudará a colocar o dashboard online gratuitamente usando o Render.com.

## 📋 Pré-requisitos

1. **Conta no GitHub**: Você precisará de uma conta gratuita no GitHub (github.com)
2. **Conta no Render**: Você precisará de uma conta gratuita no Render.com
3. **Arquivos do projeto**: O projeto preparado para deploy

## 🚀 Passo a Passo para Deploy

### Passo 1: Preparar o GitHub

1. **Crie uma conta no GitHub** (se ainda não tiver):
   - Acesse: https://github.com
   - Clique em "Sign up" e siga as instruções

2. **Crie um novo repositório**:
   - Após fazer login, clique no botão verde "New" ou no ícone "+" no canto superior direito
   - Escolha "New repository"
   - Nome do repositório: `madero-dashboard`
   - Deixe como "Public" (público)
   - Marque a opção "Add a README file"
   - Clique em "Create repository"

### Passo 2: Fazer Upload dos Arquivos

1. **Na página do seu repositório recém-criado**:
   - Clique em "uploading an existing file" ou "Add file" > "Upload files"

2. **Faça upload dos arquivos do projeto**:
   - Arraste toda a pasta `madero_dashboard` para a área de upload
   - Ou clique em "choose your files" e selecione todos os arquivos da pasta `madero_dashboard`
   - **Importante**: Certifique-se de que todos os arquivos estão sendo enviados, incluindo:
     - `src/` (pasta com todo o código)
     - `requirements.txt`
     - `Procfile`
     - `runtime.txt`
     - `build.sh`

3. **Confirme o upload**:
   - Na parte inferior da página, escreva uma mensagem como "Initial commit - Dashboard Grupo Madero"
   - Clique em "Commit changes"

### Passo 3: Configurar o Render

1. **Crie uma conta no Render** (se ainda não tiver):
   - Acesse: https://render.com
   - Clique em "Get Started for Free"
   - Você pode fazer login usando sua conta do GitHub (recomendado)

2. **Conecte sua conta do GitHub**:
   - No dashboard do Render, clique em "New +"
   - Escolha "Web Service"
   - Conecte sua conta do GitHub se solicitado
   - Selecione o repositório `madero-dashboard` que você criou

### Passo 4: Configurar o Serviço Web

1. **Configurações básicas**:
   - **Name**: `madero-dashboard` (ou outro nome de sua preferência)
   - **Region**: Escolha a região mais próxima (ex: Oregon para Brasil)
   - **Branch**: `main` (ou `master`, dependendo do que aparece)
   - **Root Directory**: Deixe em branco (vazio)

2. **Configurações de build e deploy**:
   - **Runtime**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: Deixe em branco (o Render usará o Procfile automaticamente)

3. **Configurações do plano**:
   - **Instance Type**: Escolha "Free" (gratuito)

4. **Variáveis de ambiente** (opcional):
   - Você pode adicionar variáveis se necessário, mas para o básico não é preciso

5. **Clique em "Create Web Service"**

### Passo 5: Aguardar o Deploy

1. **Processo de deploy**:
   - O Render começará a fazer o build do seu projeto
   - Você verá logs em tempo real na tela
   - O processo pode levar alguns minutos

2. **Deploy concluído**:
   - Quando terminar, você verá uma mensagem de sucesso
   - O Render fornecerá uma URL pública para seu site
   - A URL será algo como: `https://madero-dashboard-xxxx.onrender.com`

### Passo 6: Testar o Site

1. **Acesse a URL fornecida pelo Render**
2. **Teste as funcionalidades**:
   - Upload de planilhas
   - Visualização de gráficos
   - Filtros por data
   - Export de dados

## ⚠️ Limitações da Hospedagem Gratuita

- **Sleep Mode**: O site pode "dormir" após 15 minutos de inatividade e levar alguns segundos para "acordar" no próximo acesso
- **Recursos limitados**: 512MB de RAM, que é suficiente para o dashboard
- **Armazenamento temporário**: Arquivos enviados podem ser perdidos quando o serviço reinicia (isso é normal em hospedagens gratuitas)
- **Tempo de build**: Pode levar alguns minutos para fazer deploy de atualizações

## 🔄 Como Atualizar o Site

Para fazer mudanças no site:

1. **Faça as alterações nos arquivos locais**
2. **Faça upload dos arquivos atualizados no GitHub**:
   - Vá para seu repositório no GitHub
   - Clique em "Add file" > "Upload files"
   - Substitua os arquivos antigos pelos novos
   - Faça commit das mudanças
3. **O Render fará deploy automaticamente** das mudanças

## 🆘 Solução de Problemas

### Se o deploy falhar:
1. **Verifique os logs** na página do Render para ver qual erro ocorreu
2. **Arquivos comuns que podem estar faltando**:
   - `requirements.txt`
   - `Procfile`
   - `runtime.txt`
   - Pasta `src/` completa

### Se o site não carregar:
1. **Aguarde alguns minutos** - o primeiro acesso pode ser lento
2. **Verifique se todos os arquivos estáticos estão na pasta `src/static/`**
3. **Verifique os logs do Render** para erros de execução

### Se o upload de planilhas não funcionar:
- **Isso é esperado na hospedagem gratuita** - os arquivos não persistem entre reinicializações
- Para uso em produção real, seria necessário usar um serviço de armazenamento externo (como AWS S3)

## 📞 Suporte

Se você encontrar problemas durante o deploy, anote:
1. **A mensagem de erro exata**
2. **Em qual passo o erro ocorreu**
3. **Screenshots da tela de erro**

E me envie essas informações para que eu possa te ajudar a resolver.

---

**Desenvolvido por Ricardo Junior**
**Grupo Madero - Dashboard de Cancelamentos iFood**

