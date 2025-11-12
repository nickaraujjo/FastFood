# Sistema de Gerenciamento de Fast Food

Sistema completo de gerenciamento para restaurantes fast food desenvolvido em Django.

## Funcionalidades

### 1. Gerenciamento de Pedidos
- CRUD completo de itens do cardápio
- Criação e gerenciamento de pedidos de clientes
- Status de pedidos: Pendente, Em Preparação, Pronto para Entrega, Entregue, Cancelado
- Cálculo automático de totais

### 2. Sistema de Entregas
- Gerenciamento de entregadores
- Atribuição de entregas a entregadores
- Rastreamento de status de entrega em tempo real
- Controle de disponibilidade de entregadores

### 3. Relatórios de Vendas
- Relatórios diários, semanais e mensais
- Filtros por período e entregador
- Cálculo de receita total e número de pedidos
- Itens mais vendidos
- Vendas por categoria

### 4. Gerenciamento de Clientes
- Cadastro completo de clientes
- Histórico de pedidos por cliente
- Sistema de pontos de fidelidade
- Programa de indicações

### 5. Programa de Fidelidade e Indicações
- Pontos acumulados por valor de compra
- Resgate de pontos para descontos
- Bônus por indicação de novos clientes

### 6. Sistema Multilíngue
- Interface completamente em Português (pt-BR)
- Todos os labels, botões e templates traduzidos

## Tecnologias Utilizadas

- **Backend**: Django 5.0
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Banco de Dados**: SQLite (pode ser alterado para PostgreSQL)
- **Ícones**: Bootstrap Icons

## Estrutura do Projeto

\`\`\`
fastfood/
├── core/           # Configurações do sistema
├── menu/           # Gerenciamento do cardápio
├── orders/         # Gerenciamento de pedidos
├── delivery/       # Sistema de entregas
├── customers/      # Gerenciamento de clientes
├── reports/        # Relatórios e estatísticas
└── templates/      # Templates HTML
\`\`\`

## Instalação

1. Instale as dependências:
\`\`\`bash
pip install -r requirements.txt
\`\`\`

2. Execute as migrações:
\`\`\`bash
python manage.py makemigrations
python manage.py migrate
\`\`\`

3. Crie um superusuário:
\`\`\`bash
python manage.py createsuperuser
\`\`\`

4. Execute o servidor:
\`\`\`bash
python manage.py runserver
\`\`\`

5. Acesse o sistema:
- Interface principal: http://localhost:8000/
- Painel administrativo: http://localhost:8000/admin/

## Configurações

### Programa de Fidelidade

No arquivo `fastfood/settings.py`, você pode configurar:

\`\`\`python
LOYALTY_POINTS_PER_REAL = 10  # 10 pontos por R$ 1,00
REFERRAL_BONUS_POINTS = 100   # Pontos de bônus por indicação
\`\`\`

## Uso

### Criar um Pedido

1. Acesse "Pedidos" > "Novo Pedido"
2. Selecione o cliente
3. Adicione itens do cardápio
4. Confirme o pedido

### Gerenciar Entregas

1. Acesse "Entregas"
2. Atribua um entregador disponível
3. Atualize o status conforme a entrega progride

### Visualizar Relatórios

1. Acesse "Relatórios" > "Vendas"
2. Selecione o período desejado
3. Filtre por entregador se necessário

## Painel Administrativo

O Django Admin está configurado para gerenciar:
- Itens do cardápio
- Pedidos e itens de pedidos
- Entregadores e entregas
- Clientes e indicações

## Licença

Este projeto é de código aberto e está disponível para uso educacional e comercial.
