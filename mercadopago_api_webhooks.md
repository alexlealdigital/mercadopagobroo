# Mercado Pago API: Webhooks

Webhooks (também conhecidos como web callbacks) são um método simples que permite que uma aplicação ou sistema forneça informações em tempo real sempre que um evento ocorre.

As notificações de webhooks podem ser configuradas para cada aplicação criada em [Suas integrações](https://www.mercadopago.com.mx/developers/en/docs/your-integrations/introduction). Você também pode configurar uma URL de teste que, juntamente com suas credenciais de teste, permite testar o funcionamento correto de suas notificações antes de entrar em produção.

## Configuração através de Suas Integrações

Para configurar as notificações de Webhooks via Suas integrações, é necessário especificar as URLs onde elas serão recebidas e os eventos para os quais você deseja receber notificações.

### Passos para Configuração:

1.  Acesse [Suas integrações](https://www.mercadopago.com.mx/developers/en/docs/your-integrations/introduction) e selecione a aplicação para a qual deseja habilitar as notificações.
2.  No menu esquerdo, clique em **Webhooks > Configurar notificações** e configure as URLs que serão usadas para receber as notificações. Recomenda-se usar URLs diferentes para o modo de teste e o modo de produção.
    *   **URL do modo de teste:** Forneça uma URL que permita testar o funcionamento correto das notificações durante a fase de teste ou desenvolvimento.
    *   **URL do modo de produção:** Forneça uma URL para receber notificações com sua integração produtiva.
3.  Selecione os **eventos** dos quais você deseja receber notificações no formato `JSON` via um `HTTP POST` para a URL especificada anteriormente. Um evento pode ser qualquer tipo de atualização no objeto relatado, incluindo mudanças de status ou atributos.
4.  Finalmente, clique em **Salvar**. Isso gerará uma **assinatura secreta** única para sua aplicação, permitindo validar a autenticidade das notificações recebidas, garantindo que foram enviadas pelo Mercado Pago.

### Validação da Origem da Notificação

As notificações enviadas pelo Mercado Pago incluirão a assinatura secreta no cabeçalho `x-signature`, permitindo validar sua autenticidade para maior segurança e prevenção de fraudes.

**Exemplo de `x-signature`:**

`ts=1704908010,v1=618c85345248dd820d5fd456117c2ab2ef8eda45a0282ff693eac24131a5e839`

Para configurar esta validação:

1.  Extraia o timestamp (`ts`) e a assinatura (`v1`) do cabeçalho `x-signature`.
2.  Preencha um template com os dados recebidos na notificação, o `ts` do cabeçalho e o `x-request-id` do cabeçalho.
    *   **Template:** `id:[data.id_url];request-id:[x-request-id_header];ts:[ts_header];`
3.  Obtenha a assinatura secreta gerada para sua aplicação em Suas integrações.
4.  Gere uma assinatura HMAC (Hash-based Message Authentication Code) usando a função hash SHA256 em base hexadecimal. Use a **assinatura secreta** como chave e o template preenchido como mensagem.
5.  Compare a chave gerada com a chave extraída do cabeçalho (`v1`).

## Simulação de Notificações

Para verificar se as notificações estão configuradas corretamente:

1.  Após configurar as URLs e eventos, clique em **Salvar**.
2.  Clique em **Simular** para testar se a URL especificada está recebendo notificações.
3.  Selecione a URL a ser testada (teste ou produção), o tipo de evento e insira a identificação que será enviada no corpo da notificação.
4.  Clique em **Enviar teste** para verificar a requisição, a resposta do servidor e a descrição do evento.
