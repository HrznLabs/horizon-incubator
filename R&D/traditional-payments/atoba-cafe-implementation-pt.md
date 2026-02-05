# 🍵 iTake para Atobá Café

## Guia de Implementação Completo

**Documento preparado para: Atobá Café**  
**Data: Janeiro 2026**  
**Versão: 1.0**

---

## 📋 Índice

1. [O Que é o iTake?](#o-que-é-o-itake)
2. [Como Funciona na Prática](#como-funciona-na-prática)
3. [Benefícios para o Atobá Café](#benefícios-para-o-atobá-café)
4. [O Que é Necessário para Começar](#o-que-é-necessário-para-começar)
5. [Passo a Passo da Implementação](#passo-a-passo-da-implementação)
6. [Como os Clientes Vão Encomendar](#como-os-clientes-vão-encomendar)
7. [Como Receber Pagamentos](#como-receber-pagamentos)
8. [O Painel de Gestão (Dashboard)](#o-painel-de-gestão-dashboard)
9. [Sistema de Entregas](#sistema-de-entregas)
10. [Perguntas Frequentes](#perguntas-frequentes)
11. [Contactos e Suporte](#contactos-e-suporte)

---

## 🎯 O Que é o iTake?

### Explicação Simples

O **iTake** é uma plataforma de encomendas e entregas de comida — semelhante ao Uber Eats ou Glovo — mas com algumas diferenças importantes que beneficiam diretamente os restaurantes:

- **Taxas mais baixas**: O iTake cobra menos comissão do que as grandes plataformas
- **Controlo total**: O restaurante mantém os seus dados e a relação com os clientes
- **Pagamentos seguros**: Os pagamentos são processados de forma segura através de um sistema moderno chamado "escrow" (explicado abaixo)
- **Entregas flexíveis**: Pode usar os seus próprios estafetas ou utilizar a rede de estafetas do iTake

### O Que Significa "Escrow"?

Quando um cliente faz uma encomenda, o dinheiro fica "guardado" num sistema seguro até que a entrega seja confirmada. Isto funciona assim:

```
Cliente paga → Dinheiro fica em "escrow" → Entrega confirmada → Dinheiro vai para o restaurante
```

**Vantagem**: Se algo correr mal (cliente não paga, entrega cancelada), existe um processo justo para resolver a situação.

---

## 🔄 Como Funciona na Prática

### O Ciclo de Uma Encomenda

Imagine que um cliente quer encomendar um café e um pastel de nata do Atobá Café. Eis o que acontece:

```
1. CLIENTE                    2. ATOBÁ CAFÉ                3. ESTAFETA
   ↓                             ↓                            ↓
   Encomenda na app          Recebe notificação           Vê a entrega disponível
   ou website                 ↓                            ↓
   ↓                          Confirma                     Aceita a entrega
   Paga                       ↓                            ↓
   ↓                          Prepara o pedido             Vai buscar
   Recebe confirmação         ↓                            ↓
   ↓                          Marca como pronto            Entrega ao cliente
   Acompanha entrega em       ↓                            ↓
   tempo real                 Recebe pagamento             Recebe pagamento
```

### Tempo Estimado

| Fase | Tempo Típico |
|------|--------------|
| Cliente faz encomenda | 2-3 minutos |
| Confirmação do restaurante | 30 segundos |
| Preparação (depende do pedido) | 5-15 minutos |
| Atribuição do estafeta | 1-5 minutos |
| Entrega | Depende da distância |

---

## ✅ Benefícios para o Atobá Café

### Financeiros

| Benefício | Descrição |
|-----------|-----------|
| **Taxas reduzidas** | Comissões mais baixas que Uber Eats/Glovo |
| **Sem custos mensais fixos** | Só paga quando vende |
| **Pagamentos rápidos** | Recebe o dinheiro automaticamente após cada entrega |

### Operacionais

| Benefício | Descrição |
|-----------|-----------|
| **Painel simples** | Interface fácil de usar para gerir encomendas |
| **Notificações** | Aviso sonoro e visual sempre que há uma nova encomenda |
| **Menu digital** | Atualizar preços e disponibilidade é instantâneo |
| **Horários flexíveis** | Define quando está aberto para entregas |

### De Marketing

| Benefício | Descrição |
|-----------|-----------|
| **Visibilidade** | Aparece no mapa para clientes na zona |
| **Avaliações** | Sistema de estrelas que ajuda a construir reputação |
| **Dados próprios** | Mantém acesso às informações dos seus clientes |

---

## 📦 O Que é Necessário para Começar

### Requisitos Mínimos

1. **Smartphone ou Tablet**
   - Android (versão 10 ou superior) ou iPhone (iOS 14 ou superior)
   - Com acesso à internet (Wi-Fi ou dados móveis)

2. **Impressora de Recibos** (Opcional mas Recomendado)
   - Bluetooth ou Wi-Fi
   - Para imprimir automaticamente os pedidos

3. **Conta Bancária Portuguesa**
   - IBAN para receber os pagamentos
   - O dinheiro é transferido regularmente

### Informações Necessárias

Antes de começar, prepare:

- [ ] **Nome comercial**: "Atobá Café"
- [ ] **Morada completa**: Para os estafetas saberem onde ir buscar
- [ ] **Horário de funcionamento**: Dias e horas de entrega
- [ ] **Menu com preços**: Lista de produtos disponíveis para entrega
- [ ] **IBAN**: Para receber pagamentos
- [ ] **NIF**: Para faturação
- [ ] **Fotografia do estabelecimento**: Para a página do restaurante
- [ ] **Logótipo** (se houver): Para identificação na app

---

## 🛠️ Passo a Passo da Implementação

### Fase 1: Registo (Dia 1)

1. **Criar conta no iTake**
   - Recebe um link de convite por email ou WhatsApp
   - Clica no link e preenche os dados básicos:
     - Nome do restaurante
     - Email de contacto
     - Número de telefone
   - Confirma o email

2. **Verificação**
   - A equipa do iTake verifica os dados
   - Pode demorar até 24 horas (normalmente menos)

### Fase 2: Configuração do Restaurante (Dias 1-2)

1. **Entrar no Painel de Gestão**
   - Vai a: **app.itake.pt/dashboard**
   - Faz login com o email e password

2. **Preencher Perfil do Restaurante**
   - **Nome**: Atobá Café
   - **Descrição**: Breve texto sobre o café (ex: "Café tradicional com pastelaria caseira")
   - **Tipo de cozinha**: Cafetaria, Pastelaria
   - **Morada completa**: Com código postal
   - **Telefone**: Para contacto em caso de problemas
   - **Fotografia**: Carregar imagem do estabelecimento

3. **Definir Horários**
   - Dias da semana abertos
   - Hora de início e fim das entregas
   - Pode ser diferente do horário da loja física

4. **Definir Zona de Entrega**
   - Raio máximo de entrega (ex: 3km)
   - Quanto maior o raio, mais clientes potenciais, mas entregas mais demoradas

### Fase 3: Criar o Menu Digital (Dias 2-3)

1. **Adicionar Categorias**
   - Exemplos: "Cafés", "Pastelaria", "Sandes", "Bebidas"

2. **Adicionar Produtos a Cada Categoria**
   
   Para cada produto, preencher:
   
   | Campo | Exemplo |
   |-------|---------|
   | Nome | Pastel de Nata |
   | Descrição | Pastel de nata tradicional, acabado de fazer |
   | Preço | €1,20 |
   | Fotografia | (opcional mas recomendado) |
   | Tempo de preparação | 2 min |
   | Disponível | Sim/Não |

3. **Opções e Extras** (Opcional)
   - Ex: "Com canela" (+€0,00)
   - Ex: "Café descafeinado" (+€0,20)

### Fase 4: Configuração de Pagamentos (Dia 3)

1. **Introduzir IBAN**
   - O IBAN onde quer receber os pagamentos
   - Verificação pode demorar 1-2 dias úteis

2. **Definir Valor Mínimo de Encomenda** (Opcional)
   - Ex: Mínimo €5,00 para entregas

3. **Taxa de Entrega**
   - Pode definir uma taxa fixa ou por distância
   - Esta taxa vai para o estafeta

### Fase 5: Teste e Lançamento (Dia 4)

1. **Fazer Uma Encomenda de Teste**
   - Usar a sua própria morada
   - Verificar se tudo funciona

2. **Ativar o Restaurante**
   - Clicar em "Ativar para receber encomendas"
   - Feito! O Atobá Café está online!

---

## 📱 Como os Clientes Vão Encomendar

### Opção 1: App iTake

Os clientes descarregam a app iTake (disponível para iPhone e Android) e:

1. Abrem a app
2. Veem o mapa com restaurantes perto deles
3. Clicam no "Atobá Café"
4. Escolhem produtos
5. Adicionam ao carrinho
6. Pagam (cartão, MB Way, ou outro)
7. Acompanham a entrega em tempo real

### Opção 2: Website

Os clientes também podem encomendar através de:
- **itake.pt/r/atoba-cafe** (link direto para o Atobá Café)
- Este link pode ser partilhado nas redes sociais, colocado no balcão, etc.

### Opção 3: QR Code

Pode imprimir um QR Code para colocar:
- No balcão
- Na montra
- Em flyers

Quando o cliente lê o QR Code, vai direto para a página do Atobá no iTake.

---

## 💳 Como Receber Pagamentos

### Fluxo de Pagamento

```
Cliente paga → Sistema guarda → Entrega confirmada → Atobá recebe
```

### Métodos de Pagamento Aceites

| Método | Disponibilidade |
|--------|-----------------|
| Cartão de Crédito/Débito | ✅ Sim |
| MB Way | ✅ Sim |
| Multibanco | ✅ Sim |
| PayPal | ✅ Sim |
| Dinheiro na entrega | ⚠️ Opcional (configurável) |

### Quando Recebe o Dinheiro

- **Por transferência automática**
- Pode escolher frequência:
  - Diária (todos os dias úteis)
  - Semanal (às segundas-feiras)
  - Quando atingir X euros

### O Que Aparece no Extrato

Cada transferência inclui:
- Número de encomendas
- Valor total das vendas
- Taxas cobradas
- Valor líquido recebido

**Exemplo de Extrato Semanal:**

| Item | Valor |
|------|-------|
| Vendas (15 encomendas) | €189,50 |
| Taxa iTake (8%) | -€15,16 |
| Taxa de processamento | -€1,90 |
| **Total Transferido** | **€172,44** |

---

## 🖥️ O Painel de Gestão (Dashboard)

### Página Principal

Quando entrares no painel, vês:

1. **Encomendas Ativas**
   - Lista de pedidos novos e em preparação
   - Cada encomenda mostra:
     - Hora do pedido
     - Itens encomendados
     - Morada de entrega
     - Estado atual

2. **Ações Rápidas**
   - ✅ Aceitar encomenda
   - 🍳 Marcar como "Em preparação"
   - ✅ Marcar como "Pronto para recolha"
   - ❌ Recusar encomenda (com motivo)

3. **Notificações**
   - Som quando chega nova encomenda
   - Alertas visuais no ecrã

### Gestão do Menu

- **Atualizar preços**: Mudar o preço de qualquer item instantaneamente
- **Disponibilidade**: Marcar produtos como "esgotado" temporariamente
- **Adicionar novos**: Criar novos produtos a qualquer momento
- **Fotografias**: Atualizar imagens dos produtos

### Relatórios

O painel mostra:

- **Hoje**: Vendas do dia
- **Esta Semana**: Comparação com semana anterior
- **Este Mês**: Relatório mensal
- **Produtos Populares**: O que mais vende
- **Avaliações**: O que os clientes dizem

---

## 🚴 Sistema de Entregas

### Como Funcionam as Entregas

O iTake liga-se ao **Horizon Protocol** — uma rede de estafetas independentes. Funciona assim:

1. **Encomenda confirmada e marcada como "pronta"**
2. **Sistema procura estafetas disponíveis perto do Atobá**
3. **Estafeta aceita a entrega**
4. **Estafeta vai buscar ao Atobá**
5. **Estafeta entrega ao cliente**
6. **Cliente confirma recepção**
7. **Pagamento distribuído automaticamente**

### Quem São os Estafetas?

Os estafetas são pessoas registadas na rede Horizon que:
- Foram verificadas (identidade confirmada)
- Têm avaliações de entregas anteriores
- Estão disponíveis na zona

O restaurante pode ver:
- Nome do estafeta
- Avaliação média
- Número de entregas feitas
- Localização em tempo real

### Opção: Usar os Seus Próprios Estafetas

Se o Atobá quiser usar os seus próprios funcionários para entregas:
- Pode registá-los como estafetas do restaurante
- As entregas são atribuídas diretamente a eles
- Mantém controlo total

---

## ❓ Perguntas Frequentes

### Sobre Custos

**P: Quanto custa usar o iTake?**
> R: Não há custos fixos. Paga apenas uma percentagem sobre cada venda (cerca de 8-12%, dependendo do plano).

**P: E se não vender nada num mês?**
> R: Não paga nada. Só paga quando vende.

**P: Posso cancelar a qualquer momento?**
> R: Sim, pode desativar o restaurante a qualquer momento, sem penalizações.

### Sobre Encomendas

**P: E se não conseguir preparar uma encomenda?**
> R: Pode recusar ou cancelar, mas tente fazê-lo rapidamente. Cancelamentos frequentes afetam a reputação.

**P: Posso definir um tempo máximo de preparação?**
> R: Sim, define para cada produto quanto tempo demora a preparar.

**P: E se o estafeta não aparecer?**
> R: O sistema automaticamente procura outro estafeta. O cliente e o restaurante são notificados.

### Sobre Pagamentos

**P: Quando recebo o dinheiro?**
> R: Pode escolher: diariamente, semanalmente, ou quando atingir um valor mínimo.

**P: E se um cliente reclamar?**
> R: Existe um sistema de resolução de disputas. Se a reclamação for válida, o dinheiro pode ser reembolsado do "escrow".

### Sobre Problemas

**P: E se a internet falhar?**
> R: As encomendas pendentes são guardadas. Quando voltar online, aparecem novamente.

**P: Preciso de formação para usar isto?**
> R: O sistema é muito simples, mas oferecemos suporte telefónico durante as primeiras semanas.

---

## 📞 Contactos e Suporte

### Suporte iTake

| Canal | Contacto |
|-------|----------|
| Email | suporte@itake.pt |
| WhatsApp | +351 XXX XXX XXX |
| Telefone | +351 XXX XXX XXX |
| Horário | Segunda a Sexta, 9h-18h |

### Suporte Técnico (Horizon)

Para questões técnicas sobre pagamentos e entregas:
| Canal | Contacto |
|-------|----------|
| Email | support@horizon.io |

### Em Caso de Emergência

Se houver um problema urgente durante o serviço:
1. Primeiro: Use o botão "Ajuda" no painel
2. Segundo: Ligue para o número de suporte
3. Terceiro: Pause o restaurante temporariamente (se necessário)

---

## 📊 Resumo: Primeiros Passos para o Atobá Café

| Passo | Ação | Tempo Estimado |
|-------|------|----------------|
| 1 | Registo no iTake | 10 minutos |
| 2 | Preencher perfil do restaurante | 15 minutos |
| 3 | Criar menu digital | 30-60 minutos |
| 4 | Configurar pagamentos | 10 minutos |
| 5 | Fazer teste | 15 minutos |
| 6 | Ativar! | 1 clique |

**Tempo total estimado: 2-3 horas** (pode ser feito ao longo de vários dias)

---

## 📝 Notas Técnicas (Para Referência)

Esta secção é mais técnica e serve como referência para quem for configurar o sistema.

### Arquitetura do Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                    iTake (Interface)                         │
│           App do Cliente · App do Restaurante                │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                     iTake API                                │
│          Encomendas · Restaurantes · Pagamentos              │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                   Horizon Protocol                           │
│    Sistema de Entregas · Escrow · Reputação · Mapa          │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                   Blockchain (Base L2)                       │
│              Contratos Inteligentes · USDC                   │
└─────────────────────────────────────────────────────────────┘
```

### Estrutura de Taxas

| Destinatário | Percentagem | Descrição |
|--------------|-------------|-----------|
| Restaurante | ~85-90% | Valor líquido após taxas |
| Estafeta | Taxa fixa + gorjeta | Pagamento da entrega |
| iTake | 8-12% | Taxa da plataforma |
| Horizon Protocol | ~0.5% | Taxa de processamento blockchain |

### Integrações Utilizadas

| Serviço | Função |
|---------|--------|
| Adyen | Processamento de pagamentos |
| Mapbox | Mapas e cálculo de rotas |
| Twilio | Notificações por SMS (opcional) |
| Base L2 | Blockchain para contratos |

---

**Documento preparado por**: Equipa Horizon  
**Versão**: 1.0  
**Última atualização**: Janeiro 2026

> *Este documento destina-se exclusivamente ao Atobá Café e contém informações sobre a implementação do sistema iTake. Para dúvidas, contacte o suporte.*
