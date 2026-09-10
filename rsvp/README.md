# Rock N Fifty — Confirmação de presença

Site independente para confirmação de presença no aniversário de 50 anos do Demetrius. Usa apenas a biblioteca padrão do Python e armazena as respostas em `data/rsvp.sqlite3`.

## Executar localmente

```bash
python3 app.py
```

Abra <http://127.0.0.1:8797>.

## Dados

A tabela `rsvps` armazena:

- nome
- WhatsApp opcional
- presença ou ausência
- número de pessoas
- mensagem opcional
- data e hora do envio

## Hospedagem em produção

O site foi configurado para funcionar atrás do Caddy em `rsvp.demetriusnunes.com`, encaminhando para `127.0.0.1:8797`.
