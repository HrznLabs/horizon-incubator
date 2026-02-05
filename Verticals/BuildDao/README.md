# BuildDao (Vertical)

**Status**: 📝 Planning Phase

BuildDao is a proposed vertical on the Horizon Protocol focused on physical construction, renovation, and maintenance work.

## 🎯 Objectives

- **Milestone-Based Payments**: Trustless release of funds upon completion of specific construction phases.
- **Expert Dispute Resolution**: Disputes handled by qualified inspectors/architects rather than generic jurors.
- **Permit/License verification**: On-chain verification of contractor licenses.

## 🧩 Architecture (Planned)

### Smart Contracts
- **`ConstructionEscrow`**:
  - Supports multi-stage release (Deposit -> Foundation -> Framing -> Final).
  - Requires sign-off from designated "Inspector" wallet.

### Off-Chain Service
- **Blueprints & Docs**: Secure storage for project documents linked to missions.
- **Inspection Scheduler**: Coordination tool for verifying work.

## 🗺️ Roadmap

1. **Phase 1**: Conceptual Design (Current)
2. **Phase 2**: Smart Contract prototyping (Milestone Escrow)

## 📂 Key Documents

- `BuildDAO_Specification_v1.pdf`: Comprehensive specification PDF.
- `BuildDAO_Specification_v1.docx`: Editable specification document.
- `Diagrams/`: Folder containing architectural diagrams for the vertical.
