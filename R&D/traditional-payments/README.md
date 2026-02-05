# Traditional Payments R&D

**Status**: 🧪 Experimental

Research and Reference implementations for integrating traditional fiat payment rails into the Horizon ecosystem, specifically for user on-ramping and potential off-ramping for workers.

## 🎯 Goals

1. **Seamless On-ramp**: Allow mission creators to fund escrows using Credit Cards (via Coinbase Onramp, MoonPay, or Stripe).
2. **Worker Off-ramp**: Allow workers to easily cash out USDC to their bank accounts.
3. **Stablecoin integration**: Focus on USDC/EURC compatibility.

## 📚 References

- **Coinbase Onramp**: `horizon/packages/mobile` currently integrates Coinbase Onramp.
- **Stripe Crypto**: Investigating Stripe Connect for crypto payouts.
- **MB Way**: Researching integration for localized payments in Portugal (via payment gateways).

## 📝 Notes

- Current focus is leveraging the **Coinbase CDP Onramp** as the primary solution due to its native integration with Base.
- Custom fiat rails are considered high-effort and low-priority compared to integrating existing providers.

## 📂 Key Documents

- `ADYEN_INTEGRATION_GUIDE.md`: Guide for integrating Adyen payments (research).
- `atoba-cafe-implementation-pt.md`: Specific implementation details for the Atobá Café pilot (Portuguese).
