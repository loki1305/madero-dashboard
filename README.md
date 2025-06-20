# Dashboard de Cancelamentos - Grupo Madero

## Descrição
Site responsivo e interativo para análise de dados de cancelamentos de pedidos do iFood do Grupo Madero.

## Funcionalidades Implementadas

### ✅ Funcionalidades Principais
- **Upload de Planilhas**: Upload de arquivos Excel (.xlsx) com dados de cancelamentos
- **Visualizações Interativas**: Gráficos de barras e pizza com dados de cancelamentos
- **Resumo Executivo**: Cards com métricas principais (total de pedidos, vendas, percentuais)
- **Filtros por Data**: Filtrar dados por período específico
- **Export de Dados**: Download de planilhas filtradas
- **Design Responsivo**: Funciona em desktop e mobile
- **Tema Grupo Madero**: Cores preto e amarelo escuro conforme solicitado

### ✅ Funcionalidades Técnicas
- **Backend Flask**: API REST completa para processamento de dados
- **Frontend React**: Interface moderna com Tailwind CSS e shadcn/ui
- **Processamento de Dados**: Análise automática com pandas
- **Área Administrativa**: Sistema de login para funcionalidades protegidas
- **CORS Habilitado**: Comunicação frontend-backend
- **Arquitetura Modular**: Código organizado e escalável

### ✅ Visualizações Disponíveis
1. **Gráfico Geral**: Cancelamento Inicial vs Reversão vs Cancelamento Final
2. **Gráfico por Status**: Distribuição de cancelamentos por tipo de status
3. **Gráfico por Regional**: Cancelamentos finais por regional
4. **Métricas**: Total de pedidos, venda total, percentuais antes/após reversão

## Estrutura do Projeto

```
madero_dashboard/
├── src/
│   ├── main.py              # Aplicação Flask principal
│   ├── routes/
│   │   ├── dashboard.py     # Rotas para dados e upload
│   │   └── admin.py         # Rotas administrativas
│   ├── static/              # Frontend React compilado
│   └── uploads/             # Arquivos de planilhas
├── requirements.txt         # Dependências Python
├── start.sh                 # Script para iniciar o dashboard (NOVO!)
├── stop.sh                  # Script para parar o dashboard (NOVO!)
└── venv/                   # Ambiente virtual

madero_frontend/
├── src/
│   ├── App.jsx             # Componente principal
│   ├── components/ui/      # Componentes UI
│   └── assets/             # Recursos estáticos
└── dist/                   # Build de produção
```

## Como Usar (MUITO MAIS SIMPLES!)

### 1. Preparação (Apenas uma vez!)

*   **Extraia o arquivo compactado**: Você receberá um arquivo `.tar.gz`. Use um programa como 7-Zip (Windows) ou o Terminal (`tar -xzf nome_do_arquivo.tar.gz` no Linux/macOS) para extraí-lo. Isso criará uma pasta chamada `madero_dashboard_completo`.
*   **Entre na pasta do projeto**: Dentro de `madero_dashboard_completo`, você encontrará a pasta `madero_dashboard`. Esta é a pasta principal do projeto.

### 2. Iniciar o Dashboard

*   **Abra o Terminal/Prompt de Comando**: No Windows, pesquise por "Prompt de Comando". No macOS/Linux, pesquise por "Terminal".
*   **Vá para a pasta do projeto**: Digite `cd ` (com um espaço) e arraste a pasta `madero_dashboard` para a janela do Terminal. Pressione `Enter`.
*   **Execute o script de início**: Digite `./start.sh` e pressione `Enter`.
    *   **No Windows**: Se `./start.sh` não funcionar, tente `bash start.sh` (você pode precisar instalar o Git Bash ou WSL para usar comandos Linux no Windows).
*   Você verá uma mensagem como "Dashboard iniciado! Acesse http://localhost:5000 no seu navegador.". **Não feche esta janela do Terminal!** Ela mantém o dashboard funcionando.

### 3. Acessar o Dashboard

*   Abra seu navegador de internet (Chrome, Firefox, Edge, etc.).
*   Digite `http://localhost:5000` na barra de endereços e pressione `Enter`.
*   Pronto! O dashboard estará funcionando.

### 4. Parar o Dashboard

*   **Abra uma NOVA janela do Terminal/Prompt de Comando** (não feche a que está rodando o dashboard).
*   **Vá para a pasta do projeto**: Digite `cd ` (com um espaço) e arraste a pasta `madero_dashboard` para a janela do Terminal. Pressione `Enter`.
*   **Execute o script de parada**: Digite `./stop.sh` e pressione `Enter`.
    *   **No Windows**: Se `./stop.sh` não funcionar, tente `bash stop.sh`.
*   Você verá a mensagem "Dashboard parado.". Agora você pode fechar as duas janelas do Terminal.

## Como Usar (Funcionalidades do Dashboard)

#### **1. Upload de Planilhas (Carregar seus Dados)**

Esta é a forma principal de alimentar o dashboard com seus dados de cancelamento.

*   Na parte superior da página, você verá uma seção "Upload e Filtros". Certifique-se de que a aba "**Upload de Planilha**" esteja selecionada.
*   Clique no botão "**Selecionar Planilha (.xlsx)**" (ou "Choose File" / "Escolher Arquivo").
*   Uma janela do seu computador se abrirá. Navegue até a sua planilha de cancelamentos do iFood (o arquivo `.xlsx` que você me enviou ou uma versão mais recente).
*   Selecione o arquivo e clique em "Abrir" ou "OK".
*   Agora, clique no botão "**Enviar Planilha**" no dashboard.
*   Aguarde um momento. O dashboard processará os dados. Se tudo der certo, a mensagem de erro sumirá e os gráficos e resumos aparecerão automaticamente na tela!

#### **2. Visualizando os Dados e Gráficos**

Após o upload, o dashboard exibirá as seguintes informações:

*   **Resumo Geral**: Na parte superior, você verá cards com números importantes como "Total de Pedidos", "Venda Total iFood", "% Antes da Reversão" e "% Após Reversão".
*   **Gráfico Geral de Cancelamentos**: Um gráfico de barras mostrando o volume de "Cancelamento Inicial", "Reversão" e "Cancelamento Final".
*   **Cancelamentos por Status**: Um gráfico de pizza (redondo) que mostra a proporção de cancelamentos por diferentes status (ex: Reembolso Aprovado, Consumer, etc.).
*   **Cancelamentos por Regional**: Um gráfico de barras que exibe o cancelamento final por cada regional (Kleber Riquelme, Gustavo Direito, etc.).

#### **3. Filtrando Dados por Data**

You can analyze the data for a specific period:

*   In the "Upload and Filters" section, click on the "**Filtros por Data**" tab.
*   You will see two fields: "Data Início" and "Data Fim". Click on each to open a calendar and select the desired dates.
*   After choosing the dates, click the "**Filtrar**" button. The charts and summaries will automatically update to show only the data for the selected period.

#### **4. Exporting Filtered Data**

If you have filtered the data and want to save this version of the spreadsheet:

*   After applying the filters (as in step 3), click the "**Exportar**" button (next to the "Filtrar" button).
*   Your browser will download a new Excel file (`.xlsx`) containing only the data from the period you filtered.

#### **5. Administrative Area (Optional - For Advanced Users)**

The dashboard has an administrative area for more advanced functionalities, such as manual data entry or upload history. This area is password protected.

*   **Default Password**: The password to access the administrative area is `madero2025`.
*   **Access**: Currently, access to this area is done directly via API (for developers). If you need to use manual entry or upload history, let me know and I can guide you or adapt the interface to facilitate access.

---

**Desenvolvido por Ricardo Junior**
**Grupo Madero - Dashboard de Cancelamentos iFood**

