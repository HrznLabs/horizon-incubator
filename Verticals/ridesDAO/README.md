# ridesDAO (Vertical)

**Status**: 🎨 Design Phase

ridesDAO is a proposed vertical on the Horizon Protocol focused on decentralized ride-sharing. It aims to replace centralized intermediaries like Uber and Lyft with a protocol-based coordination layer.

## 🎯 Objectives

- **Lower Fees**: Eliminate the ~25-30% take rate of centralized platforms.
- **Driver Ownership**: Drivers own a stake in the network (via Guilds).
- **Censorship Resistance**: Open access for any qualified driver.

## 🧩 Architecture (Planned)

### Smart Contracts
- **`RideEscrow`**: Specialized escrow that handles:
  - Dynamic pricing (surge handled via oracle/agreement)
  - Cancellation policies
  - Incident insurance pools
- **`DriverGuild`**: A specialized `GuildDAO` for vetting drivers (handling licenses, background checks).

### Off-Chain Service
- **Matching Engine**: Real-time distinct matching logic (different from generic mission discovery).
- **Route Optimization**: Integration with advanced routing services.

## 🗺️ Roadmap

1. **Phase 1**: Market Research & Spec (Current)
2. **Phase 2**: PoC on Base Sepolia
3. **Phase 3**: Driver app prototype

## 📂 Key Documents

- `RidesVertical_Analysis_v1.md`: Initial market analysis and feasibility study.
- `RidesVertical_MatchingEngine.md`: Technical deep dive into the decentralized matching logic.
- `RidesVertical_Complete_Spec.html`: HTML export of the full vertical specification.
- `RidesDAO_Specification_v1.docx`: Original specification document.
