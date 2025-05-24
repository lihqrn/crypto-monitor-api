# 🚀 Crypto Monitor API

Uma aplicação Python que consome dados de trades da Binance via WebSocket e exibe preços em tempo real.

---

## 📝 Descrição

Este repositório contém um componentes principal:

1. **Monitor em tempo real** (`ws_streaming.py`):  
   Conecta-se ao WebSocket da Binance e imprime no console cada trade para os pares configurados.

Também há um frontend **estático** (`index.html`) que permite visualizar os preços em um navegador.

---

## 🎯 Funcionalidades

- Streaming de trades “ao vivo” da Binance (via WebSocket).  
- Log em tempo real dos preços e volumes negociados.  
- Gatilho programável para ordens de mercado (BUY/SELL).  
- Frontend simples para visualização no navegador.  

---

