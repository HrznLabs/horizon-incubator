# Adyen Payment Integration Guide

## R&D Documentation for Traditional Payments in Horizon/iTake

> **Purpose**: This document preserves the Adyen payment integration patterns from the legacy iTake vertical, for future reference when implementing traditional payments in the mini-app or other Horizon verticals.

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Environment Variables](#environment-variables)
4. [Core Components](#core-components)
5. [Code Implementation](#code-implementation)
6. [Webhook Handling](#webhook-handling)
7. [Zod Schemas](#zod-schemas)
8. [Integration with NestJS](#integration-with-nestjs)
9. [Future Considerations](#future-considerations)

---

## Overview

**Adyen** is a payment platform that supports:
- Credit/Debit cards (Visa, Mastercard, Amex)
- Local payment methods (MB Way in Portugal, iDEAL in NL, etc.)
- Google Pay / Apple Pay
- Buy now, pay later (Klarna, etc.)

### Why Adyen vs Stripe?

| Feature | Adyen | Stripe |
|---------|-------|--------|
| Portuguese market | ✅ Excellent (MB Way) | ⚠️ Limited MB Way support |
| Enterprise focus | ✅ Yes | More SMB focused |
| Pricing | Fixed per transaction | % + fixed fee |
| Complexity | Higher | Lower |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Frontend                                │
│     (Customer initiates payment → gets checkout URL)         │
└──────────────────────────┬──────────────────────────────────┘
                           │ POST /payments
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                   NestJS Backend                             │
│                                                              │
│  ┌─────────────────┐    ┌─────────────────┐                 │
│  │ PaymentsService │◄───│  AdyenService   │                 │
│  │                 │    │                 │                 │
│  │ - create()      │    │ - createSession │                 │
│  │ - handleWebhook │    │ - verifyWebhook │                 │
│  └─────────────────┘    └────────┬────────┘                 │
│                                  │                           │
└──────────────────────────────────┼──────────────────────────┘
                                   │ HTTPS API
                                   ▼
┌─────────────────────────────────────────────────────────────┐
│                     Adyen API                                │
│                                                              │
│  - Creating checkout sessions                                │
│  - Processing payments                                       │
│  - Sending webhooks on status changes                        │
└──────────────────────────────────────────────────────────────┘
                           │
                           │ POST /webhooks/adyen
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                   NestJS Webhooks                            │
│                                                              │
│  - Verify signature                                          │
│  - Update payment status                                     │
│  - Update order status                                       │
└─────────────────────────────────────────────────────────────┘
```

---

## Environment Variables

```bash
# Adyen Configuration
ADYEN_API_KEY=AQEyhmfxK4P...          # API key from Adyen dashboard
ADYEN_MERCHANT_ACCOUNT=YourMerchant    # Merchant account name
ADYEN_CLIENT_KEY=live_XXXX            # Client-side key for frontend
ADYEN_HMAC_KEY=XXXX                   # For webhook signature verification
ADYEN_LIVE_URL_PREFIX=1234abcd         # Only for production (optional in test)
```

### Getting These Credentials

1. Sign up at [Adyen Customer Area](https://ca-live.adyen.com/)
2. API Key: **Settings → API Credentials → Generate API Key**
3. Client Key: **Settings → API Credentials → Client Key**
4. HMAC Key: **Developers → Webhooks → Configure → HMAC Key**
5. Merchant Account: Shown in dashboard header

---

## Core Components

### File Structure

```
src/
├── payments/
│   ├── payments.module.ts      # NestJS module
│   ├── payments.controller.ts   # REST endpoints
│   ├── payments.service.ts      # Business logic
│   └── adyen.service.ts         # Adyen API wrapper
├── webhooks/
│   ├── webhooks.module.ts
│   ├── webhooks.controller.ts   # POST /webhooks/adyen
│   └── webhooks.service.ts      # Webhook processing
└── schemas/
    └── payment.ts               # Zod validation schemas
```

---

## Code Implementation

### 1. AdyenService (adyen.service.ts)

This is the core wrapper around Adyen's API:

```typescript
import { Injectable } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';

@Injectable()
export class AdyenService {
  private readonly apiKey: string;
  private readonly merchantAccount: string;
  private readonly clientKey: string;
  private readonly hmacKey: string;
  private readonly liveUrlPrefix: string;

  constructor(private configService: ConfigService) {
    this.apiKey = this.configService.get<string>('ADYEN_API_KEY') || '';
    this.merchantAccount = this.configService.get<string>('ADYEN_MERCHANT_ACCOUNT') || '';
    this.clientKey = this.configService.get<string>('ADYEN_CLIENT_KEY') || '';
    this.hmacKey = this.configService.get<string>('ADYEN_HMAC_KEY') || '';
    this.liveUrlPrefix = this.configService.get<string>('ADYEN_LIVE_URL_PREFIX') || '';
  }

  /**
   * Create a checkout session for the customer
   * Returns a URL where the customer completes payment
   */
  async createCheckoutSession(
    amount: number, 
    currency: string, 
    reference: string, 
    returnUrl: string
  ) {
    // Determine endpoint (test vs live)
    const checkoutUrl = this.liveUrlPrefix 
      ? `https://${this.liveUrlPrefix}-checkout-live.adyenpayments.com/checkout/v71/sessions`
      : 'https://checkout-test.adyen.com/v71/sessions';

    const payload = {
      amount: {
        value: Math.round(amount * 100), // Convert EUR to cents
        currency: currency.toUpperCase(),
      },
      reference,          // Your order ID
      returnUrl,          // Where to redirect after payment
      merchantAccount: this.merchantAccount,
      countryCode: 'PT',  // Portugal
      shopperLocale: 'pt-PT',
      lineItems: [
        {
          quantity: 1,
          description: `iTake Order ${reference}`,
          amountIncludingTax: Math.round(amount * 100),
        },
      ],
    };

    const response = await fetch(checkoutUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': this.apiKey,
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error(`Adyen API error: ${response.status}`);
    }

    return response.json();
  }

  /**
   * Verify webhook signature for security
   */
  async verifyWebhook(payload: any, signature: string): Promise<boolean> {
    if (!this.hmacKey) {
      console.warn('HMAC key not configured');
      return true; // Skip in development
    }
    
    // In production, implement HMAC-SHA256 verification
    // See: https://docs.adyen.com/development-resources/webhooks/verify-hmac-signatures
    return true;
  }
}
```

### 2. PaymentsService (payments.service.ts)

Orchestrates payment creation and status updates:

```typescript
import { Injectable } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { AdyenService } from './adyen.service';

@Injectable()
export class PaymentsService {
  constructor(
    private prisma: PrismaService,
    private adyenService: AdyenService,
  ) {}

  /**
   * Create a new payment for an order
   */
  async create(data: {
    orderId: string;
    amount: number;
    currency: string;
    returnUrl: string;
  }) {
    // Get order details
    const order = await this.prisma.order.findUnique({
      where: { id: data.orderId },
    });

    if (!order) {
      throw new Error('Order not found');
    }

    // Create Adyen checkout session
    const reference = `order-${order.id}`;
    const checkoutSession = await this.adyenService.createCheckoutSession(
      data.amount,
      data.currency,
      reference,
      data.returnUrl,
    );

    // Save payment record to database
    const payment = await this.prisma.payment.create({
      data: {
        orderId: data.orderId,
        provider: 'adyen',
        providerPaymentId: checkoutSession.id,
        amount: data.amount,
        currency: data.currency,
        status: 'pending',
        metadata: {
          sessionId: checkoutSession.id,
          sessionData: checkoutSession.sessionData,
        },
      },
    });

    return {
      payment,
      checkoutUrl: checkoutSession.url,
      sessionData: checkoutSession.sessionData,
    };
  }

  /**
   * Handle incoming webhook from Adyen
   */
  async handleWebhook(webhookData: any) {
    const { eventCode, merchantReference, pspReference, success } = webhookData;

    // Find payment by reference
    const payment = await this.prisma.payment.findFirst({
      where: {
        OR: [
          { providerPaymentId: pspReference },
          { metadata: { path: ['reference'], equals: merchantReference } },
        ],
      },
      include: { order: true },
    });

    if (!payment) {
      console.warn(`Payment not found: ${merchantReference}`);
      return;
    }

    // Map Adyen event to status
    let newStatus: string;
    let orderStatus: string | undefined;

    switch (eventCode) {
      case 'AUTHORISATION':
        if (success === 'true') {
          newStatus = 'completed';
          orderStatus = 'confirmed';
        } else {
          newStatus = 'failed';
          orderStatus = 'cancelled';
        }
        break;
      case 'CANCELLATION':
        newStatus = 'cancelled';
        orderStatus = 'cancelled';
        break;
      case 'REFUND':
        newStatus = 'refunded';
        break;
      default:
        console.log(`Unhandled event: ${eventCode}`);
        return;
    }

    // Update payment status
    await this.prisma.payment.update({
      where: { id: payment.id },
      data: { status: newStatus },
    });

    // Update order status
    if (orderStatus && payment.order) {
      await this.prisma.order.update({
        where: { id: payment.order.id },
        data: { 
          status: orderStatus,
          paymentStatus: newStatus,
        },
      });
    }

    return { processed: true, paymentId: payment.id, newStatus };
  }
}
```

### 3. PaymentsController (payments.controller.ts)

REST API endpoints:

```typescript
import { Controller, Get, Post, Body, Param } from '@nestjs/common';
import { ApiTags, ApiOperation } from '@nestjs/swagger';
import { PaymentsService } from './payments.service';

@ApiTags('payments')
@Controller('payments')
export class PaymentsController {
  constructor(private readonly paymentsService: PaymentsService) {}

  @Post()
  @ApiOperation({ summary: 'Create payment' })
  create(@Body() dto: {
    orderId: string;
    amount: number;
    currency: string;
    returnUrl: string;
  }) {
    return this.paymentsService.create(dto);
  }

  @Get('order/:orderId')
  @ApiOperation({ summary: 'Get payments for order' })
  findByOrder(@Param('orderId') orderId: string) {
    return this.paymentsService.findByOrder(orderId);
  }

  @Get(':id')
  @ApiOperation({ summary: 'Get payment by ID' })
  findOne(@Param('id') id: string) {
    return this.paymentsService.findOne(id);
  }
}
```

---

## Webhook Handling

### WebhooksController

```typescript
import { Controller, Post, Body } from '@nestjs/common';
import { ApiTags, ApiOperation } from '@nestjs/swagger';
import { WebhooksService } from './webhooks.service';

@ApiTags('webhooks')
@Controller('webhooks')
export class WebhooksController {
  constructor(private readonly webhooksService: WebhooksService) {}

  @Post('adyen')
  @ApiOperation({ summary: 'Handle Adyen payment webhooks' })
  handleAdyenWebhook(@Body() payload: any) {
    return this.webhooksService.handlePaymentWebhook(payload);
  }
}
```

### Adyen Webhook Events

| Event Code | Meaning | Action |
|------------|---------|--------|
| `AUTHORISATION` | Payment approved/declined | Update to completed/failed |
| `CANCELLATION` | Payment cancelled | Update to cancelled |
| `REFUND` | Refund processed | Update to refunded |
| `CAPTURE` | Funds captured | Log only (already authorized) |
| `CHARGEBACK` | Customer disputed | Handle dispute |

### Setting Up Webhooks in Adyen

1. Go to **Developers → Webhooks → + Webhook**
2. Set URL: `https://your-api.com/webhooks/adyen`
3. Enable **HMAC verification**
4. Select events: AUTHORISATION, CANCELLATION, REFUND

---

## Zod Schemas

```typescript
import { z } from 'zod';

// Payment provider enum
export const PaymentProvider = z.enum(['adyen', 'stripe']);

// Payment status enum
export const PaymentStatus = z.enum([
  'pending',
  'processing',
  'completed',
  'failed',
  'cancelled',
  'refunded',
]);

// Full payment record
export const PaymentSchema = z.object({
  id: z.string().uuid(),
  orderId: z.string().uuid(),
  provider: PaymentProvider,
  providerPaymentId: z.string(),
  amount: z.number().min(0),
  currency: z.string().length(3), // ISO 4217 (EUR, USD, etc.)
  status: PaymentStatus,
  paymentMethod: z.string().optional(),
  metadata: z.record(z.any()).optional(),
  createdAt: z.date(),
  updatedAt: z.date(),
});

// Create payment request
export const CreatePaymentSchema = z.object({
  orderId: z.string().uuid(),
  amount: z.number().min(0),
  currency: z.string().length(3),
  returnUrl: z.string().url(),
  metadata: z.record(z.any()).optional(),
});

// Adyen checkout session structure
export const AdyenCheckoutSchema = z.object({
  amount: z.object({
    value: z.number(),     // In cents
    currency: z.string(),
  }),
  reference: z.string(),   // Your order ID
  returnUrl: z.string(),   // Redirect after payment
  merchantAccount: z.string(),
  countryCode: z.string().optional(),
  shopperLocale: z.string().optional(),
});

// Types
export type Payment = z.infer<typeof PaymentSchema>;
export type CreatePayment = z.infer<typeof CreatePaymentSchema>;
export type PaymentStatusType = z.infer<typeof PaymentStatus>;
```

---

## Integration with NestJS

### PaymentsModule

```typescript
import { Module } from '@nestjs/common';
import { PaymentsController } from './payments.controller';
import { PaymentsService } from './payments.service';
import { AdyenService } from './adyen.service';

@Module({
  controllers: [PaymentsController],
  providers: [PaymentsService, AdyenService],
  exports: [PaymentsService, AdyenService],
})
export class PaymentsModule {}
```

### Prisma Schema Addition

```prisma
model Payment {
  id                String   @id @default(uuid())
  orderId           String
  order             Order    @relation(fields: [orderId], references: [id])
  provider          String   // 'adyen' | 'stripe'
  providerPaymentId String
  amount            Float
  currency          String   @db.VarChar(3)
  status            String   @default("pending")
  paymentMethod     String?
  metadata          Json?
  createdAt         DateTime @default(now())
  updatedAt         DateTime @updatedAt
}
```

---

## Future Considerations

### Integrating with Horizon Mobile App

To add traditional payments to the iTake mini-app:

1. **Backend Changes** (horizon/packages/service):
   - Add `PaymentsModule` with `AdyenService`
   - Create `/api/v1/itake/payments/checkout` endpoint
   - Add webhook endpoint `/webhooks/adyen`

2. **Mobile App Changes** (horizon/packages/mobile):
   - Add "Card Payment" option in checkout
   - Open Adyen checkout URL in WebView or browser
   - Handle return URL redirect

3. **Database** (prisma/schema.prisma):
   - Add `Payment` model if not exists
   - Link to orders/missions

### Coinbase Commerce Alternative

For a hybrid approach (traditional + crypto):

```typescript
async createPayment(order, method: 'card' | 'crypto') {
  if (method === 'crypto') {
    return this.coinbaseService.createCharge({
      amount: order.total,
      currency: 'USDC',
    });
  }
  return this.adyenService.createCheckoutSession(...);
}
```

### MB Way Specific Configuration

For Portugal, enable MB Way in Adyen:

```typescript
const payload = {
  // ... other fields
  allowedPaymentMethods: ['scheme', 'mbway', 'multibanco'],
  shopperLocale: 'pt-PT',
  countryCode: 'PT',
};
```

---

## Resources

- [Adyen API Documentation](https://docs.adyen.com/)
- [Adyen Test Cards](https://docs.adyen.com/development-resources/testing/test-card-numbers)
- [Webhooks Guide](https://docs.adyen.com/development-resources/webhooks/)
- [HMAC Signature Verification](https://docs.adyen.com/development-resources/webhooks/verify-hmac-signatures)

---

**Original Source**: `/Verticals/iTake/apps/api/src/payments/`  
**Archive Date**: January 2026  
**Author**: Horizon Team
