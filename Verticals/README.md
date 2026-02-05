# Horizon Verticals

Horizon is designed as a modular protocol that can support various real-world "verticals"—specialized applications built on top of the generic mission coordination layer.

This directory contains the implementations and design documents for specific verticals.

## 🏗️ Architecture

Each vertical typically consists of:

1. **Smart Contract Extensions**: Custom logic that inherits from or interacts with core Horizon contracts (e.g., `DeliveryEscrow` vs standard `MissionEscrow`).
2. **Specialized Service Modules**: Backend logic for domain-specific problems (e.g., routing for rides, menu parsing for food).
3. **Custom Clients**: Specialized interfaces for the target user base.

## 🚀 Active Verticals

### 1. **iTake** (Food Delivery)
*Status: In Development (Alpha)*
- **Location**: Implementation lives in `horizon/packages/service/src/itake`
- **Contracts**: Uses `DeliveriesDAO` and `DeliveryEscrow` (V2 Contracts)
- **Goal**: Decentralized food delivery platform to compete with UberEats/DoorDash.

### 2. **[ridesDAO](./ridesDAO)** (Ride Sharing)
*Status: Design Phase*
- **Goal**: Decentralized ride-hailing network.
- **Key Challenge**: Real-time matching and high-trust reputation systems.

### 3. **[BuildDao](./BuildDao)** (Construction & Maintenance)
*Status: Planning Phase*
- **Goal**: Coordination for physical construction and maintenance tasks.
- **Key Challenge**: High-value escrow, milestone-based releases, and specialized dispute resolution (construction experts).

## 🛠️ Creating a New Vertical

1. **Define the Mission Lifecycle**: Does it fit the Open -> Submit -> Verify flow?
2. **Identify Data Needs**: What structured data is needed? (Pickup/Dropoff, blueprints, menu items)
3. **Determine Escrow Logic**: Do you need custom release conditions?
4. **Create Vertical Service Module**: Add a new module in `packages/service/src/my-vertical`.
