# Mercado Pago API: Criar Pagamento

Este endpoint permite criar um pagamento e incluir todas as informações necessárias. Em caso de sucesso, a requisição retornará uma resposta com status 201.

## Endpoint

`POST https://api.mercadopago.com/v1/payments`

## Parâmetros da Requisição

### HEADER

*   `X-Idempotency-Key` (string, **REQUIRED**): Permite tentar novamente as requisições com segurança, sem o risco de realizar acidentalmente a mesma ação mais de uma vez. Útil para evitar erros, como a criação de dois pagamentos idênticos.
*   `Authorization` (string, **REQUIRED**): Token de acesso (Bearer token).

### BODY

Os principais campos do corpo da requisição incluem:

*   `additional_info` (object): Dados adicionais, como itens, informações do pagador e detalhes de envio.
    *   `items` (array of objects): Lista de produtos ou serviços. Cada item pode ter `id`, `title`, `description`, `picture_url`, `category_id`, `quantity`, `unit_price`, etc.
    *   `payer` (object): Informações do pagador, como `first_name`, `last_name`, `phone`, `address`.
*   `application_fee` (number): Comissão que terceiros cobram de seus clientes.
*   `binary_mode` (boolean): Se `true`, pagamentos só podem ser aprovados ou rejeitados.
*   `callback_url` (string): URL para onde o Mercado Pago redireciona após o pagamento (apenas para transferências bancárias).
*   `description` (string): Descrição do pagamento.
*   `external_reference` (string): Referência externa para o pagamento.
*   `installments` (number): Número de parcelas.
*   `payer` (object): Informações do pagador, incluindo `entity_type`, `type`, `id`, `email`, `identification`.
*   `payment_method_id` (string): ID do método de pagamento.
*   `token` (string): Token do cartão (se aplicável).
*   `transaction_amount` (number, **REQUIRED**): Valor total da transação.

## Exemplo de Requisição (cURL)

```bash
curl -X POST \
  'https://api.mercadopago.com/v1/payments'\
  -H 'Content-Type: application/json' \
  -H 'X-Idempotency-Key: 0d5020ed-1af6-469c-ae06-c3bec19954bb' \
  -H 'Authorization: Bearer TEST-4599*********755-11221*********d497ae962*********ecf8d85-1*********' \
  -d '{
  "additional_info": {
    "items": [
      {
        "id": "MLB2907679857",
        "title": "Point Mini",
        "description": "Point product for card payments via Bluetooth.",
        "picture_url": "https://http2.mlstatic.com/resources/frontend/statics/growth-sellers-landings/device-mlb-point-i_medium2x.png",
        "category_id": "electronics",
        "quantity": 1,
        "unit_price": 58,
        "type": "electronics",
        "event_date": "2023-12-31T09:37:52.000-04:00",
        "warranty": false,
        "category_descriptor": {
          "passenger": {},
          "route": {}
        }
      }
    ],
    "payer": {
      "first_name": "Test",
      "last_name": "Test",
      "phone": {
        "area_code": 11,
        "number": "987654321"
      },
      "address": {
        "zip_code": "12312-123",
        "street_name": "Av das Nacoes Unidas",
        "street_number": 3003,
        "neighborhood": null,
        "city": 3003,
        "federal_unit": 3003
      }
    }
  },
  "application_fee": null,
  "binary_mode": false,
  "campaign_id": null,
  "capture": false,
  "coupon_amount": null,
  "description": "Payment for product",
  "differential_pricing_id": null,
  "external_reference": "MP0001",
  "installments": 1,
  "metadata": null,
  "payer": {
    "entity_type": "individual",
    "type": "customer",
    "id": null,
    "email": "test_user_123@testuser.com",
    "identification": {
      "type": "CPF",
      "number": "95749019047"
    }
  },
  "payment_method_id": "master",
  "token": "ff8080814c11e237014c1ff593b57b4d",
  "transaction_amount": 58
}
'
```

## Resposta de Exemplo

```json
{
  "id": 20359978,
  "date_created": "2019-07-10T14:41:00.000-04:00",
  "date_approved": "2019-07-10T14:41:00.000-04:00",
  "date_last_updated": "2019-07-10T14:41:00.000-04:00",
  "money_release_date": "2019-07-26T15:41:00.000-04:00",
  "issuer_id": 25,
  "payment_type_id": "credit_card",
  "status": "approved",
  "status_detail": "accredited",
  "currency_id": "BRL",
  "description": "Point Mini",
  "taxes_amount": 0,
  "shipping_amount": 0,
  "pos_id": null,
  "store_id": null,
  "collector_id": 444646180,
  "payer": {
    "id": 444646180,
    "email": "test_user_123@testuser.com",
    "first_name": "Test",
    "last_name": "Test",
    "identification": {
      "type": "CPF",
      "number": "95749019047"
    },
    "phone": {
      "area_code": "11",
      "number": "987654321"
    },
    "address": {
      "zip_code": "12312-123",
      "street_name": "Av das Nacoes Unidas",
      "street_number": "3003"
    }
  },
  "metadata": {},
  "additional_info": {
    "items": [
      {
        "id": "MLB2907679857",
        "title": "Point Mini",
        "description": "Point product for card payments via Bluetooth.",
        "picture_url": "https://http2.mlstatic.com/resources/frontend/statics/growth-sellers-landings/device-mlb-point-i_medium2x.png",
        "category_id": "electronics",
        "quantity": 1,
        "unit_price": 58,
        "type": "electronics",
        "event_date": "2023-12-31T09:37:52.000-04:00",
        "warranty": false,
        "category_descriptor": {
          "passenger": {},
          "route": {}
        }
      }
    ],
    "payer": {
      "first_name": "Test",
      "last_name": "Test",
      "phone": {
        "area_code": "11",
        "number": "987654321"
      },
      "address": {
        "zip_code": "12312-123",
        "street_name": "Av das Nacoes Unidas",
        "street_number": "3003"
      }
    },
    "shipments": {
      "receiver_address": {
        "zip_code": "12312-123",
        "state_name": "Rio de Janeiro",
        "city_name": "Buzios",
        "street_name": "Av das Nacoes Unidas",
        "street_number": "3003"
      },
      "width": null,
      "height": null
    }
  },
  "order": {},
  "external_reference": "MP0001",
  "installments": 1,
  "transaction_details": {
    "net_received_amount": 55.66,
    "total_paid_amount": 58,
    "overpaid_amount": 0,
    "installment_amount": 0,
    "financial_free_amount": 0,
    "commissions_amount": 2.34,
    "discount_amount": 0,
    "free_account_money": 0,
    "escrow_amount": 0
  },
  "fee_details": [
    {
      "type": "mercadopago_fee",
      "amount": 2.34,
      "fee_payer": "collector"
    }
  ],
  "captured": true,
  "card": {},
  "notification_url": null,
  "refunds": [],
  "sponsor_id": null,
  "call_for_authorize_id": null,
  "statement_descriptor": "MERCADOPAGO",
  "date_of_expiration": null,
  "live_mode": false,
  "merchant_of_properties": {},
  "point_of_interaction": {
    "type": "standard",
    "business_info": {
      "unit": "",
      "sub_unit": ""
    },
    "transaction_data": {
      "qr_code": "",
      "ticket_url": "",
      "qr_code_base64": "",
      "bank_info": {
        "collector_bank_info": {
          "account_id": null,
          "cbu": null,
          "alias": null,
          "account_holder_name": null,
          "identification": null,
          "branch_id": null
        },
        "is_online": null
      },
      "financial_institution": null,
      "bank_transfer_id": null,
      "transaction_id": null
    }
  }
}
```
