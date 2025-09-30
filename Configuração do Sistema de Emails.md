# Configuração do Sistema de Emails

O sistema de emails já está implementado e funcional. Aqui estão as instruções para configurá-lo:

## 1. Configuração do Gmail (Recomendado)

### Passo 1: Habilitar Autenticação de 2 Fatores
1. Acesse sua conta Google
2. Vá em "Segurança" > "Verificação em duas etapas"
3. Ative a verificação em duas etapas

### Passo 2: Gerar Senha de App
1. Na mesma seção de Segurança
2. Clique em "Senhas de app"
3. Selecione "Email" e "Outro (nome personalizado)"
4. Digite "Sistema Cobrança MP"
5. Copie a senha gerada (16 caracteres)

### Passo 3: Configurar no .env
```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USER=seu_email@gmail.com
EMAIL_PASSWORD=sua_senha_de_app_16_caracteres
```

## 2. Outras Opções de Email

### SendGrid (Profissional)
```env
SMTP_SERVER=smtp.sendgrid.net
SMTP_PORT=587
EMAIL_USER=apikey
EMAIL_PASSWORD=sua_api_key_do_sendgrid
```

### Outlook/Hotmail
```env
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587
EMAIL_USER=seu_email@outlook.com
EMAIL_PASSWORD=sua_senha_ou_app_password
```

### Yahoo Mail
```env
SMTP_SERVER=smtp.mail.yahoo.com
SMTP_PORT=587
EMAIL_USER=seu_email@yahoo.com
EMAIL_PASSWORD=sua_senha_de_app
```

## 3. Templates de Email Incluídos

O sistema já possui templates HTML profissionais para:

### Email de Cobrança
- Design responsivo e moderno
- Botão de pagamento destacado
- Informações da cobrança organizadas
- Link de pagamento seguro

### Email de Confirmação
- Confirmação visual de pagamento aprovado
- Detalhes da transação
- ID do pagamento para referência

## 4. Funcionalidades Implementadas

✅ **Envio Automático**: Email enviado automaticamente ao criar cobrança
✅ **Confirmação de Pagamento**: Email enviado quando pagamento é aprovado
✅ **Reenvio Manual**: Botão para reenviar email de cobrança
✅ **Templates Responsivos**: Emails funcionam em desktop e mobile
✅ **Tratamento de Erros**: Sistema robusto com logs de erro
✅ **Validação**: Verificação de emails válidos

## 5. Teste do Sistema

Para testar o envio de emails:

1. Configure as variáveis no arquivo `.env`
2. Execute o sistema: `python src/main.py`
3. Crie uma cobrança de teste
4. Verifique se o email foi recebido
5. Teste o webhook simulando um pagamento

## 6. Monitoramento

O sistema registra logs de:
- Emails enviados com sucesso
- Erros de envio
- Tentativas de reenvio
- Status das cobranças

## 7. Segurança

- Senhas armazenadas em variáveis de ambiente
- Conexão SMTP com TLS/SSL
- Validação de emails
- Proteção contra spam

O sistema de emails está completamente funcional e pronto para uso em produção!
