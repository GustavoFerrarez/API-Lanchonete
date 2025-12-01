# BurguerHouse - Sistema de Gestão de Lanchonete

Foram implementadas funcionalidades completas para uma lanchonete online, integrando um Back-end robusto em **FastAPI** com um Front-end responsivo em **HTML/CSS/JS**. O sistema permite gestão de cardápio, usuários, carrinho de compras e pedidos.

## Regras de Negócio e Decisões de Projeto

### 1. Integridade Financeira (Cálculo no Backend)
Conforme as boas práticas de segurança, a regra de negócio mais importante implementada na API **impede que o Front-end defina o preço dos itens**. O valor total do pedido é calculado exclusivamente pelo Back-end (`quantidade * preço_unitario_do_banco`), garantindo que não haja manipulação de valores por parte do cliente.

### 2. Validação de Produtos
O sistema possui travas de segurança que **bloqueiam o cadastro de produtos com preço negativo ou igual a zero**, garantindo a consistência dos dados comerciais.

## Funcionalidades do Sistema

* **Gestão de Usuários:** Cadastro e Login (com validação de e-mail).
* **Catálogo:** Listagem de produtos separados por categorias (Clássicos, Gourmet, Acompanhamentos).
* **Carrinho de Compras:** Adicionar/Remover itens e controle de quantidade em tempo real.
* **Pedidos:** Finalização de compra com cálculo automático de totais.
* **Endereço:** Validação de campos obrigatórios para entrega.

## Pontos Positivos e Limitações

###  Pontos Positivos
* **Arquitetura Organizada:** Código separado em Camadas (Models, Schemas, Repositories, Services, Routes).
* **UX (Experiência do Usuário):** Frontend não recarrega a página (SPA - Single Page Application feel), uso de "Toasts" (notificações visuais) e Modais responsivos.
* **Performance:** Uso de chamadas assíncronas (`async/await`) no Front e no Back.

###  Limitações (O que falta)
* **Pagamento Real:** A etapa de pagamento é apenas visual (simulação), sem integração com gateways bancários.
* **Segurança:** Devido à decisão didática, a falta de criptografia de senha não é adequada para um ambiente de produção real.

## Como Executar a Aplicação

1.  **Instale as dependências:**
    Certifique-se de ter o Python instalado e o PostgreSQL rodando.
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configure o Banco de Dados:**
    Crie um arquivo `.env` na raiz com suas credenciais do PostgreSQL:
    ```bash
    PG_HOST=localhost
    PG_PORT=5432
    PG_DB=lanchonete
    PG_USER=seu_usuario
    PG_PASSWORD=sua_senha
    ```

3.  **Execute o servidor:**
    A partir da raiz do projeto, execute o seguinte comando:
    ```bash
    uvicorn app.main:app --reload
    ```

4.  **Acesse a Aplicação:**
    * **Frontend (Cliente):** Abra o arquivo `frontend/index.html` no seu navegador.
    * **Documentação API:** Acesse `http://127.0.0.1:8000/docs`.

### Observações

PARA O FUNCIONAR TODAS AS SUAS FUNCIONALIDADES DO CÓGIGO VOCÊ PRECISA ESTAR DENTRO DA PASTA 'RAIZ' DO PROJETO E REALIZAR O PASSO A PASSO NECESSÁRIO!

```bash
4° Período de Sistemas 
Feito por 'Gustavo Ferrarez Gonçalves -- 007260'
          'Rafael Vinicius dos Santos -- 007202'
```
