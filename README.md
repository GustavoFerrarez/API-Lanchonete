# BurguerHouse - Sistema de Gestão de Lanchonete

Foram implementadas funcionalidades completas para uma lanchonete online, integrando um Back-end robusto em **FastAPI** com um Front-end responsivo em **HTML/CSS/JS**. O sistema permite gestão de cardápio, usuários, carrinho de compras e pedidos.

## Regras de Negócio e Decisões de Projeto

A lógica do sistema garante que os dados permaneçam consistentes e seguros, independentemente da interface utilizada.

### 1. Integridade Financeira (Anti-Fraude)
O preço dos produtos **nunca** é confiado ao Front-end.
* **Como funciona:** Quando um item é adicionado ao pedido (`POST /item_pedido`), a API ignora qualquer preço enviado pelo cliente. Ela busca o valor atual diretamente na tabela de `Produtos` no banco de dados e o utiliza para o registro.
* **Benefício:** Impede que usuários mal-intencionados alterem o preço do hambúrguer no HTML/JS para pagar menos.

### 2. Atualização em Cascata de Totais (Trigger via Código)
O sistema recalcula automaticamente o valor total do pedido sempre que há uma alteração nos seus itens.
* **Implementação:** No repositório (`repositories/item_pedido.py`), as funções `create`, `update` e `delete` acionam automaticamente o método `atualizar_total_pedido`.
* **Lógica:** O sistema soma `(quantidade * preco_unitario)` de todos os itens vinculados àquele pedido e atualiza a tabela `Pedidos`. Isso elimina erros de cálculo manual.

### 3. Validação de Preços e Produtos
* **Consistência de Dados:** O serviço de domínio (`services/produto.py`) impede o cadastro de produtos com valor negativo ou igual a zero, garantindo a integridade do catálogo.
* **Dependência Obrigatória:** Não é possível criar um item de pedido para um produto ou usuário inexistente (validação de Chaves Estrangeiras e verificação prévia no Repository).

### 4. Fluxo de Quantidade Restrito
* **Mínimo de 1:** O *Schema* de validação (`Pydantic`) garante que a quantidade de um item no pedido seja sempre um número inteiro positivo (`gt=0`).
* **Exclusão Automática:** Se a quantidade de um item for reduzida a zero pelo usuário, o sistema interpreta como uma intenção de remoção e deleta o item do pedido.

## Funcionalidades Principais

O sistema foi projetado para atender tanto o fluxo do cliente final quanto a integridade dos dados via API.

### Gestão de Usuários
* **Cadastro de Clientes:** Criação de conta com validação de e-mail único.
* **Autenticação:** Sistema de Login que valida credenciais e mantém a sessão do usuário no Front-end (via LocalStorage/Memória).
* **Recuperação de Acesso:** Simulação de fluxo de "Esqueci minha senha".

### Catálogo e Produtos
* **Visualização por Categorias:** O cardápio é organizado dinamicamente em seções (Hambúrgueres Clássicos, Gourmet, Acompanhamentos) baseadas no cadastro do banco de dados.
* **Busca em Tempo Real:** Barra de pesquisa no Front-end para filtrar produtos por nome ou ingredientes instantaneamente.
* **Detalhes do Produto:** Exibição de foto, descrição, ingredientes e preço formatado.

### Carrinho de Compras Inteligente
* **Gestão de Itens:** Adicionar produtos, incrementar ou decrementar quantidades diretamente no modal do carrinho.
* **Remoção Segura:** Modal de confirmação personalizado antes de remover itens, evitando cliques acidentais.
* **Cálculo Instantâneo:** O subtotal de cada item e o total geral do pedido são atualizados a cada interação.

### Gestão de Pedidos
* **Checkout Completo:** Formulário para inserção de endereço de entrega com validação de campos obrigatórios.
* **Opções de Pagamento:** Interface para seleção de método de pagamento (Dinheiro, PIX, Cartão).
* **Feedback Visual:** Notificações (Toasts) não intrusivas para confirmar ações (ex: "Item adicionado", "Pedido realizado") e modais de sucesso.

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
  
## Análise do Projeto: Pontos Positivos e Negativos

### Pontos Positivos (Destaques Técnicos)

1.  **Arquitetura em Camadas (Clean Architecture):**
    * O projeto não mistura lógica de banco de dados com lógica de rotas. O código foi desacoplado em pastas específicas:
        * `schemas/`: Validação de dados (Pydantic).
        * `models/`: Mapeamento Objeto-Relacional.
        * `repositories/`: Acesso direto ao banco (CRUD).
        * `api/`: Definição de endpoints.

2.  **Segurança de Integridade de Dados:**
    * Diferente de sistemas iniciantes que confiam no preço enviado pelo Frontend, o **BurguerHouse** recalcula todo o valor do pedido no Backend.
    * Isso impede ataques comuns de manipulação de parâmetros (onde o usuário altera o HTML para pagar R$ 0,01 em um lanche).

3.  **Experiência do Usuário (UX) Fluida:**
    * O Frontend utiliza JavaScript (`Fetch API`) para atualizar o carrinho e enviar pedidos sem recarregar a página.
    * Uso de **Feedback Visual** imediato: Notificações do tipo "Toast" (avisos flutuantes) substituem os `alerts` nativos do navegador, proporcionando uma navegação melhor.

---

### Limitações e Melhorias Futuras

Embora funcional, o projeto possui simplificações adotadas para atender ao prazo acadêmico:

1.  **Autenticação Simplificada:**
    * **Limitação:** O sistema não utiliza *JSON Web Tokens (JWT)* ou OAuth2. O login é baseado em verificação simples de banco de dados.
    * **Impacto:** Em um cenário real, isso não seria seguro para manter sessões persistentes entre recargas de página.
    * **Melhoria Futura:** Implementar `FastAPI Security` com tokens JWT e expiração de sessão.

2.  **Simulação de Pagamento:**
    * **Limitação:** A etapa de pagamento é apenas visual. Não há integração com gateways reais (Stripe, Mercado Pago, etc.).
    * **Melhoria Futura:** Integrar uma API de pagamento real ou gerar QR Codes Pix dinâmicos.

3.  **Limitações:**
    * **Limitação:** O projeto foi testado manualmente. Mesmo completo tudo nele é apenas uma simulação.
    * **Melhoria Futura:** Os endereços não ficam salvo no teste, eles precisam ser inseridos novamente caso necessário.
    * **Melhoria Entrega:** Opção de entrega inválida, nele você não consegue escolher a sua forma de entrega.

### Observações

PARA O FUNCIONAR TODAS AS SUAS FUNCIONALIDADES DO CÓGIGO VOCÊ PRECISA ESTAR DENTRO DA PASTA 'RAIZ' DO PROJETO E REALIZAR O PASSO A PASSO NECESSÁRIO!

```bash
4° Período de Sistemas 
Feito por 'Gustavo Ferrarez Gonçalves -- 007260'
          'Rafael Vinicius dos Santos -- 007202'
```
