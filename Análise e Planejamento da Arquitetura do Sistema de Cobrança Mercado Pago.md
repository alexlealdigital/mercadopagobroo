# Análise e Planejamento da Arquitetura do Sistema de Cobrança Mercado Pago

## 1. Introdução

Este documento descreve a arquitetura proposta para o sistema de cobrança do Mercado Pago, substituindo a funcionalidade anteriormente provida pelo n8n. O sistema será construído utilizando Python (com Flask para o backend), HTML/CSS para o frontend, armazenamento de dados em JSON versionado no Git, e deploy via Netlify. O envio de e-mails automáticos será uma funcionalidade central para notificar os clientes sobre as cobranças.

## 2. Componentes Principais

O sistema será dividido nos seguintes componentes principais:

*   **Frontend (HTML/CSS):** Interface do usuário para interação com o sistema de cobrança. Pode incluir formulários para iniciar cobranças, exibir status, etc.
*   **Backend (Python/Flask):** Lógica de negócios, integração com a API do Mercado Pago, manipulação de dados e orquestração do envio de e-mails.
*   **Mercado Pago API:** Plataforma de pagamentos para criação e gestão de cobranças.
*   **Armazenamento de Dados (JSON no Git):** Utilizado para persistir informações sobre as cobranças, clientes e configurações. A versão no Git permitirá um histórico e colaboração.
*   **Serviço de Envio de E-mails:** Módulo responsável por enviar notificações transacionais aos clientes.
*   **Netlify:** Plataforma de deploy para o frontend e, potencialmente, para funções serverless do backend (se aplicável).

## 3. Fluxo de Cobrança Proposto

1.  **Início da Cobrança:** Um usuário (administrador) inicia uma nova cobrança através da interface frontend.
2.  **Requisição ao Backend:** O frontend envia os dados da cobrança para o backend Python.
3.  **Criação no Mercado Pago:** O backend utiliza a API do Mercado Pago para criar a preferência de pagamento ou link de cobrança.
4.  **Armazenamento de Dados:** As informações da cobrança (ID do Mercado Pago, status, dados do cliente, etc.) são salvas em um arquivo JSON, que será versionado no Git.
5.  **Envio de E-mail:** O backend aciona o serviço de e-mail para enviar uma notificação ao cliente com o link de pagamento do Mercado Pago.
6.  **Webhook do Mercado Pago:** O Mercado Pago notifica o backend (via webhook) sobre o status do pagamento (aprovado, pendente, recusado).
7.  **Atualização de Status:** O backend atualiza o status da cobrança no arquivo JSON e, se necessário, envia um e-mail de confirmação ao cliente.

## 4. Considerações Técnicas

*   **Segurança:** Proteção das chaves da API do Mercado Pago e dados sensíveis. Uso de variáveis de ambiente.
*   **Autenticação/Autorização:** Como o administrador acessará o frontend e o backend.
*   **Persistência:** Detalhes sobre a estrutura do JSON e como ele será atualizado e versionado no Git.
*   **Deploy:** Estratégias para deploy do frontend no Netlify e do backend (considerando opções como Netlify Functions para Python ou um serviço de hosting separado).
*   **Envio de E-mails:** Escolha de um provedor de e-mail (e.g., SendGrid, Mailgun, ou um serviço SMTP simples).

## 5. Próximos Passos

*   Pesquisar a API do Mercado Pago para entender os endpoints necessários.
*   Definir a estrutura exata dos arquivos JSON para armazenamento de dados.
*   Escolher um provedor de e-mail e entender sua integração.
*   Esboçar a estrutura do projeto Flask e dos arquivos HTML/CSS.
