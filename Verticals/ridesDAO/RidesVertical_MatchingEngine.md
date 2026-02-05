# 🎯 HORIZON RIDES MATCHING ENGINE

**Version:** 1.0  
**Date:** December 2025  
**Status:** Specification

---

## Table of Contents

- [1. OVERVIEW](#1-overview)
  - [1.1 Key Differences from Feed Engine](#11-key-differences-from-feed-engine)
  - [1.2 Design Goals](#12-design-goals)
- [2. ARCHITECTURE](#2-architecture)
- [3. DRIVER STATE MANAGEMENT](#3-driver-state-management)
  - [3.1 Driver Status States](#31-driver-status-states)
  - [3.2 Driver State Object (Redis)](#32-driver-state-object-redis)
  - [3.3 Driver Pool Index (Redis Geo)](#33-driver-pool-index-redis-geo)
- [4. MATCHING MODES](#4-matching-modes)
  - [4.1 Standard Match (Rider-Initiated)](#41-standard-match-rider-initiated)
  - [4.2 Driver-Initiated (Occasional Rides)](#42-driver-initiated-occasional-rides)
  - [4.3 Scheduled Match](#43-scheduled-match)
  - [4.4 Shared Ride Match](#44-shared-ride-match)
- [5. MATCHING ALGORITHM](#5-matching-algorithm)
  - [5.1 Candidate Filtering (Phase 1)](#51-candidate-filtering-phase-1)
  - [5.2 Match Scoring (Phase 2)](#52-match-scoring-phase-2)
  - [5.3 Factor Calculations](#53-factor-calculations)
  - [5.4 Match Selection (Phase 3)](#54-match-selection-phase-3)
- [6. OFFER MANAGEMENT](#6-offer-management)
  - [6.1 Offer Flow](#61-offer-flow)
  - [6.2 Offer Object](#62-offer-object)
  - [6.3 Acceptance Criteria](#63-acceptance-criteria)
- [7. ETA CALCULATION](#7-eta-calculation)
  - [7.1 ETA Service Architecture](#71-eta-service-architecture)
  - [7.2 ETA Caching Strategy](#72-eta-caching-strategy)
- [8. SHARED RIDES MATCHING](#8-shared-rides-matching)
  - [8.1 Route Compatibility Check](#81-route-compatibility-check)
  - [8.2 Shared Ride Pricing (Hybrid Distance + Time)](#82-shared-ride-pricing-hybrid-distance--time)
- [9. SURGE PRICING INTEGRATION](#9-surge-pricing-integration)
  - [9.1 Demand Analysis](#91-demand-analysis)
  - [9.2 Guild Surge Configuration](#92-guild-surge-configuration)
- [10. DRIVER-INITIATED MATCHING](#10-driver-initiated-matching)
  - [10.1 Driver Route Posting](#101-driver-route-posting)
  - [10.2 Rider Matching to Posted Routes](#102-rider-matching-to-posted-routes)
- [11. GUILD ACTIVITY REQUIREMENTS](#11-guild-activity-requirements)
  - [11.1 Activity Tracking](#111-activity-tracking)
  - [11.2 Multi-Guild Activity Distribution](#112-multi-guild-activity-distribution)
- [12. API SPECIFICATION](#12-api-specification)
  - [12.1 Ride Request Endpoints](#121-ride-request-endpoints)
  - [12.2 WebSocket Events](#122-websocket-events)
- [13. PERFORMANCE REQUIREMENTS](#13-performance-requirements)
- [14. MONITORING & METRICS](#14-monitoring--metrics)

---

## 1. OVERVIEW

The Rides Matching Engine is a specialized, real-time system that pairs riders with drivers. Unlike the general Feed Engine (which presents ranked options for users to browse), the Matching Engine must make **instant decisions** under time pressure while balancing fairness, efficiency, and quality.

### 1.1 Key Differences from Feed Engine

| Aspect | Feed Engine | Rides Matching Engine |
|--------|-------------|----------------------|
| Time Sensitivity | Async, user browses | Real-time, seconds matter |
| Decision Maker | User selects | Algorithm matches |
| Location Updates | Static mission location | Moving drivers |
| Matching Direction | User → Mission | Bidirectional (Rider ↔ Driver) |
| Availability | Missions are available until accepted | Drivers go online/offline dynamically |
| Capacity | Mission has 1 slot | Shared rides have multiple slots |

### 1.2 Design Goals

1. **Speed:** Match within 10-30 seconds
2. **Fairness:** Distribute rides fairly among drivers
3. **Quality:** Match based on reputation and preferences
4. **Efficiency:** Minimize pickup time (ETA)
5. **Flexibility:** Support multiple matching modes

---

## 2. ARCHITECTURE

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                         RIDES MATCHING ENGINE                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐         │
│  │  Request Queue  │  │  Driver Pool    │  │  Match Scorer   │         │
│  │  (Redis)        │  │  (Real-time)    │  │  (Algorithm)    │         │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘         │
│           │                    │                    │                   │
│           └────────────────────┼────────────────────┘                   │
│                                │                                        │
│                     ┌──────────▼──────────┐                            │
│                     │   MATCH ORCHESTRATOR │                            │
│                     │   ─────────────────  │                            │
│                     │   • Candidate Filter │                            │
│                     │   • Score Calculator │                            │
│                     │   • Match Selector   │                            │
│                     │   • Offer Manager    │                            │
│                     └──────────┬──────────┘                            │
│                                │                                        │
│           ┌────────────────────┼────────────────────┐                   │
│           │                    │                    │                   │
│  ┌────────▼────────┐  ┌────────▼────────┐  ┌───────▼─────────┐         │
│  │  ETA Calculator │  │ Eligibility Svc │  │ Reputation Svc  │         │
│  │  (PostGIS+OSRM) │  │ (XP, Guild)     │  │ (Bidirectional) │         │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘         │
│                                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│                           DATA LAYER                                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                  │
│  │ Driver State │  │ Rider State  │  │ Guild Config │                  │
│  │ (Redis)      │  │ (Redis)      │  │ (PostgreSQL) │                  │
│  └──────────────┘  └──────────────┘  └──────────────┘                  │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 3. DRIVER STATE MANAGEMENT

### 3.1 Driver Status States

```typescript
enum DriverStatus {
  OFFLINE = 'offline',        // Not available
  ONLINE = 'online',          // Available for rides
  EN_ROUTE_PICKUP = 'en_route_pickup',  // Heading to pickup
  WAITING_RIDER = 'waiting_rider',      // At pickup location
  ON_RIDE = 'on_ride',        // Currently giving a ride
  COMPLETING = 'completing',  // Finishing ride (rating)
}
```

### 3.2 Driver State Object (Redis)

```typescript
interface DriverState {
  driverId: string;
  walletAddress: string;
  status: DriverStatus;
  
  // Real-time location
  location: {
    lat: number;
    lng: number;
    accuracy: number;
    heading: number;      // Direction of travel
    speed: number;        // km/h
    updatedAt: number;    // Unix timestamp
  };
  
  // Current ride (if any)
  currentRideId: string | null;
  
  // Availability preferences
  preferences: {
    maxPickupDistance: number;  // km, driver's preference
    acceptsSharedRides: boolean;
    acceptsLongDistance: boolean;  // >30km
    preferredZones: string[];      // Geohash prefixes
  };
  
  // Capacity (for shared rides)
  capacity: {
    totalSeats: number;      // Vehicle capacity
    availableSeats: number;  // Current availability
  };
  
  // Performance metrics (cached)
  metrics: {
    rating: number;
    completionRate: number;
    acceptanceRate: number;
    ridesXP: number;
    tier: DriverTier;
  };
  
  // Guild memberships
  guilds: string[];
  
  // Session info
  onlineSince: number;
  lastRideCompletedAt: number;
  ridesToday: number;
  
  // Activity requirement tracking (for guild membership)
  activityByGuild: Record<string, {
    ridesThisWeek: number;
    ridesThisMonth: number;
  }>;
}
```

### 3.3 Driver Pool Index (Redis Geo)

```typescript
// Store driver locations in Redis GeoSet for fast proximity queries
// Key: drivers:online:{geohash_prefix}
// Score: driver's current timestamp
// Member: driverId

// Example commands:
// GEOADD drivers:online:eyckp 38.7223 -9.1393 driver_123
// GEORADIUS drivers:online:eyckp 38.7223 -9.1393 5 km WITHDIST
```

---

## 4. MATCHING MODES

### 4.1 Standard Match (Rider-Initiated)

The primary flow where rider requests and algorithm finds best driver.

```text
Rider Request → Filter Candidates → Score → Select → Offer → Accept/Decline
```

### 4.2 Driver-Initiated (Occasional Rides)

Driver posts availability, riders can request to join.

```text
Driver Posts Route → Visible to Riders → Rider Requests → Driver Accepts
```

### 4.3 Scheduled Match

Pre-booked rides matched closer to pickup time.

```text
Rider Schedules → Queue for Later → T-30min: Begin Matching → Confirm
```

### 4.4 Shared Ride Match

Multiple riders matched to same driver's route.

```text
Rider 1 Matched → Route Active → Rider 2 Request → 
Check Route Compatibility → Add to Ride
```

---

## 5. MATCHING ALGORITHM

### 5.1 Candidate Filtering (Phase 1)

Fast filtering to reduce candidate pool. Must be O(1) or O(log n).

```typescript
interface CandidateFilter {
  // Hard filters (must pass all)
  filters: {
    status: DriverStatus.ONLINE;
    maxDistance: number;          // From pickup
    hasCapacity: boolean;         // Available seats
    meetsRiderGuildReqs: boolean; // If rider in guild
    meetsDriverEligibility: boolean; // Driver XP/rep
    meetsRiderEligibility: boolean;  // BIDIRECTIONAL: Rider must qualify
    notBlacklisted: boolean;      // Rider hasn't blocked driver & vice versa
  };
}

// Implementation using Redis
async function filterCandidates(request: RideRequest): Promise<string[]> {
  // 1. Get drivers within radius using Redis GEORADIUS
  const nearbyDrivers = await redis.georadius(
    `drivers:online:${geohashPrefix}`,
    request.pickup.lng,
    request.pickup.lat,
    request.maxPickupRadius,
    'km',
    'WITHDIST'
  );
  
  // 2. Filter by status and capacity (batch fetch from Redis)
  const driverStates = await redis.mget(
    nearbyDrivers.map(d => `driver:state:${d.member}`)
  );
  
  // 3. Apply hard filters
  return driverStates
    .filter(state => state.status === 'online')
    .filter(state => state.capacity.availableSeats >= request.passengers)
    .filter(state => checkBidirectionalEligibility(state, request))
    .map(state => state.driverId);
}
```

### 5.2 Match Scoring (Phase 2)

Score each candidate on multiple factors. Weights are configurable.

```typescript
interface MatchScore {
  driverId: string;
  totalScore: number;
  factors: {
    etaScore: number;           // Lower ETA = higher score
    ratingScore: number;        // Driver rating
    riderRatingScore: number;   // BIDIRECTIONAL: Rider's rating (driver POV)
    fairnessScore: number;      // Time since last ride
    guildScore: number;         // Guild alignment
    priceScore: number;         // If driver accepts the price
    preferenceScore: number;    // Route matches driver's preferences
    streakScore: number;        // Bonus for active streaks
  };
}

// Scoring weights (total = 1.0)
const MATCH_WEIGHTS = {
  eta: 0.30,              // 30% - Pickup time is critical
  driverRating: 0.15,     // 15% - Quality matters
  riderRating: 0.10,      // 10% - Rider quality matters too
  fairness: 0.15,         // 15% - Distribute rides fairly
  guild: 0.10,            // 10% - Guild alignment
  price: 0.10,            // 10% - Economic match
  preference: 0.05,       // 5%  - Driver preferences
  streak: 0.05,           // 5%  - Reward active drivers
};
```

### 5.3 Factor Calculations

#### ETA Score (0-100)

```typescript
function calculateETAScore(etaMinutes: number): number {
  // Perfect score if under 3 minutes
  if (etaMinutes <= 3) return 100;
  
  // Linear decay from 3 to 15 minutes
  if (etaMinutes <= 15) {
    return 100 - ((etaMinutes - 3) / 12) * 80;  // 100 → 20
  }
  
  // Heavily penalized above 15 minutes
  if (etaMinutes <= 30) {
    return 20 - ((etaMinutes - 15) / 15) * 15;  // 20 → 5
  }
  
  return 5;  // Minimum score for very far drivers
}
```

#### Fairness Score (0-100)

Prevents drivers from being starved of rides.

```typescript
function calculateFairnessScore(driver: DriverState): number {
  const minutesSinceLastRide = 
    (Date.now() - driver.lastRideCompletedAt) / 60000;
  const minutesOnline = 
    (Date.now() - driver.onlineSince) / 60000;
  
  // Ratio of online time to productive time
  const idleRatio = minutesSinceLastRide / Math.max(minutesOnline, 1);
  
  // Higher score for drivers who've been waiting longer
  if (minutesSinceLastRide <= 5) return 50;   // Just completed, neutral
  if (minutesSinceLastRide <= 15) return 60;
  if (minutesSinceLastRide <= 30) return 75;
  if (minutesSinceLastRide <= 60) return 90;
  return 100;  // Been waiting over an hour, prioritize
}
```

#### Guild Score (0-100)

```typescript
function calculateGuildScore(
  driver: DriverState, 
  rider: RiderState,
  rideGuild: string | null
): number {
  let score = 50;  // Neutral baseline
  
  // Same guild bonus
  const sharedGuilds = driver.guilds.filter(g => rider.guilds.includes(g));
  if (sharedGuilds.length > 0) {
    score += 20;
  }
  
  // Ride posted to specific guild
  if (rideGuild && driver.guilds.includes(rideGuild)) {
    score += 30;
  }
  
  // Premium guild membership
  if (driver.guilds.includes('PremiumRidesGuild')) {
    score += 10;
  }
  
  return Math.min(score, 100);
}
```

#### Bidirectional Rating Score

```typescript
function calculateRiderRatingScore(rider: RiderState): number {
  // From driver's perspective - is this a good rider?
  const riderRating = rider.metrics.averageRatingGiven;  // How they rate others
  const cancellationRate = rider.metrics.cancellationRate;
  const disputeRate = rider.metrics.disputeRate;
  
  let score = riderRating * 20;  // 0-100 scale
  
  // Penalize high cancellation
  if (cancellationRate > 10) score -= 20;
  else if (cancellationRate > 5) score -= 10;
  
  // Penalize disputes
  if (disputeRate > 5) score -= 30;
  else if (disputeRate > 2) score -= 15;
  
  return Math.max(0, Math.min(100, score));
}
```

### 5.4 Match Selection (Phase 3)

```typescript
interface MatchSelectionConfig {
  mode: 'best' | 'weighted_random' | 'round_robin';
  topN: number;          // Consider top N candidates
  offerTimeout: number;  // Seconds to accept
  maxRetries: number;    // How many drivers to try
}

async function selectMatch(
  candidates: MatchScore[],
  config: MatchSelectionConfig
): Promise<string> {
  // Sort by score
  const sorted = candidates.sort((a, b) => b.totalScore - a.totalScore);
  
  switch (config.mode) {
    case 'best':
      // Simply pick the highest score
      return sorted[0].driverId;
      
    case 'weighted_random':
      // Weighted random among top N (prevents same driver always winning)
      const topN = sorted.slice(0, config.topN);
      const totalWeight = topN.reduce((sum, c) => sum + c.totalScore, 0);
      let random = Math.random() * totalWeight;
      
      for (const candidate of topN) {
        random -= candidate.totalScore;
        if (random <= 0) return candidate.driverId;
      }
      return topN[0].driverId;
      
    case 'round_robin':
      // For testing/fairness experiments
      return sorted[Date.now() % sorted.length].driverId;
  }
}
```

---

## 6. OFFER MANAGEMENT

### 6.1 Offer Flow

```text
┌──────────────────────────────────────────────────────────────────┐
│                        OFFER LIFECYCLE                            │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│   SELECT        SEND           WAIT          RESULT              │
│   DRIVER   →    OFFER    →    RESPONSE  →   OUTCOME             │
│                                                                  │
│   ┌─────┐      ┌─────┐       ┌─────┐       ┌─────────┐          │
│   │Score│ ───► │Push │ ───► │Timer│ ───► │Accept   │ → MATCHED │
│   │Top  │      │Notif│      │15sec│      │         │           │
│   └─────┘      └─────┘      └─────┘      │Decline  │ → RETRY   │
│                                          │         │           │
│                                          │Timeout  │ → RETRY   │
│                                          │         │           │
│                                          │Offline  │ → RETRY   │
│                                          └─────────┘           │
│                                                                  │
│   RETRY: Remove driver from pool, select next best               │
│   MAX_RETRIES: 5 drivers before failing the match               │
└──────────────────────────────────────────────────────────────────┘
```

### 6.2 Offer Object

```typescript
interface RideOffer {
  offerId: string;
  rideRequestId: string;
  driverId: string;
  
  // What driver sees
  rideDetails: {
    pickup: {
      approximate: LatLng;     // ~500m accuracy before accept
      addressHint: string;     // "Near Rossio Square"
    };
    dropoff: {
      approximate: LatLng;
      addressHint: string;
    };
    estimatedDistance: number;
    estimatedDuration: number;
    estimatedReward: number;
    passengers: number;
    isSharedRide: boolean;
    rideType: 'standard' | 'premium' | 'accessibility';
  };
  
  // Rider info (bidirectional transparency)
  riderInfo: {
    rating: number;
    ridesCompleted: number;
    cancellationRate: number;
    guilds: string[];
    memberSince: Date;
  };
  
  // Offer metadata
  createdAt: number;
  expiresAt: number;
  status: 'pending' | 'accepted' | 'declined' | 'expired';
}
```

### 6.3 Acceptance Criteria

Drivers can set auto-accept rules:

```typescript
interface DriverAutoAcceptRules {
  enabled: boolean;
  conditions: {
    minReward: number;            // Only auto-accept above this
    maxPickupDistance: number;    // Only auto-accept within this
    minRiderRating: number;       // Only auto-accept above this
    preferredGuilds: string[];    // Only auto-accept from these guilds
    preferredZones: string[];     // Only auto-accept in these areas
    excludeSharedRides: boolean;
    excludeLongDistance: boolean;
  };
}
```

---

## 7. ETA CALCULATION

### 7.1 ETA Service Architecture

```typescript
interface ETAService {
  // Real-time ETA using OSRM or similar
  calculateETA(
    driverLocation: LatLng,
    pickupLocation: LatLng,
    options?: {
      trafficAware: boolean;
      routeType: 'fastest' | 'shortest';
    }
  ): Promise<ETAResult>;
  
  // Batch ETA for multiple drivers
  calculateBatchETA(
    drivers: Array<{ id: string; location: LatLng }>,
    pickupLocation: LatLng
  ): Promise<Map<string, ETAResult>>;
}

interface ETAResult {
  durationSeconds: number;
  distanceMeters: number;
  route: LatLng[];  // For visualization
  confidence: number;  // 0-1, lower if traffic data unavailable
}
```

### 7.2 ETA Caching Strategy

```typescript
// Cache ETAs for common routes (geohash pairs)
// Key: eta:{pickup_geohash}:{driver_geohash}
// TTL: 5 minutes (traffic changes)

async function getCachedETA(
  driverGeohash: string,
  pickupGeohash: string
): Promise<number | null> {
  const cached = await redis.get(`eta:${pickupGeohash}:${driverGeohash}`);
  return cached ? parseInt(cached) : null;
}
```

---

## 8. SHARED RIDES MATCHING

### 8.1 Route Compatibility Check

```typescript
interface RouteCompatibility {
  isCompatible: boolean;
  detourMinutes: number;      // Added time for existing rider
  detourPercent: number;      // % increase in existing ride time
  newRiderETA: number;        // Pickup time for new rider
  mergedRoute: LatLng[];      // Combined route
  priceAdjustment: {
    existingRiderDiscount: number;  // % discount for existing
    newRiderPrice: number;          // Price for new rider
  };
}

async function checkRouteCompatibility(
  existingRide: ActiveRide,
  newRequest: RideRequest,
  config: SharedRideConfig
): Promise<RouteCompatibility> {
  // Calculate optimal merged route
  const mergedRoute = await routeService.calculateMultiStop([
    existingRide.currentLocation,
    newRequest.pickup,
    existingRide.dropoff,  // or newRequest.dropoff if closer
    newRequest.dropoff,    // or existingRide.dropoff
  ]);
  
  // Check detour limits
  const originalDuration = existingRide.estimatedRemainingMinutes;
  const newDuration = mergedRoute.durationMinutes;
  const detourMinutes = newDuration - originalDuration;
  const detourPercent = (detourMinutes / originalDuration) * 100;
  
  // Config: max 30% detour or 10 minutes, whichever is less
  const isCompatible = 
    detourPercent <= config.maxDetourPercent &&
    detourMinutes <= config.maxDetourMinutes;
  
  return {
    isCompatible,
    detourMinutes,
    detourPercent,
    newRiderETA: mergedRoute.legs[0].durationMinutes,
    mergedRoute: mergedRoute.coordinates,
    priceAdjustment: calculateSharedPricing(existingRide, newRequest, mergedRoute),
  };
}
```

### 8.2 Shared Ride Pricing (Hybrid Distance + Time)

```typescript
interface SharedPricing {
  // Fair hybrid formula
  calculateRiderShare(
    rider: RiderInSharedRide,
    totalRoute: RouteInfo,
    allRiders: RiderInSharedRide[]
  ): number;
}

function calculateSharedRiderPrice(
  rider: RiderInSharedRide,
  allRiders: RiderInSharedRide[],
  totalFare: number
): number {
  // Calculate each rider's contribution
  
  // DISTANCE COMPONENT (60% weight)
  // Rider pays for solo segments + (shared segments / num riders)
  const distanceShare = calculateDistanceShare(rider, allRiders);
  
  // TIME COMPONENT (40% weight)
  // Rider pays proportional to time in vehicle
  const timeShare = calculateTimeShare(rider, allRiders);
  
  // Weighted combination
  const combinedShare = (distanceShare * 0.6) + (timeShare * 0.4);
  
  // Normalize so all shares sum to 1
  const totalShares = allRiders.reduce((sum, r) => 
    sum + (calculateDistanceShare(r, allRiders) * 0.6) + 
          (calculateTimeShare(r, allRiders) * 0.4), 0);
  
  const normalizedShare = combinedShare / totalShares;
  
  // Apply to total fare
  return totalFare * normalizedShare;
}

function calculateDistanceShare(
  rider: RiderInSharedRide,
  allRiders: RiderInSharedRide[]
): number {
  let share = 0;
  
  for (const segment of rider.segments) {
    const ridersInSegment = allRiders.filter(r => 
      r.segments.some(s => segmentsOverlap(s, segment))
    ).length;
    
    share += segment.distanceKm / ridersInSegment;
  }
  
  return share;
}

function calculateTimeShare(
  rider: RiderInSharedRide,
  allRiders: RiderInSharedRide[]
): number {
  // Time from pickup to dropoff
  const riderTimeMinutes = rider.dropoffTime - rider.pickupTime;
  const totalTimeMinutes = allRiders.reduce((sum, r) => 
    sum + (r.dropoffTime - r.pickupTime), 0);
  
  return riderTimeMinutes / totalTimeMinutes;
}
```

---

## 9. SURGE PRICING INTEGRATION

### 9.1 Demand Analysis

```typescript
interface DemandMetrics {
  geohash: string;
  timestamp: number;
  
  // Supply
  onlineDrivers: number;
  availableDrivers: number;  // Online but not on ride
  
  // Demand
  activeRequests: number;
  requestsLast5Min: number;
  requestsLast15Min: number;
  
  // Computed
  supplyDemandRatio: number;  // <1 means undersupply
  suggestedMultiplier: number;
}

function calculateSurgeMultiplier(metrics: DemandMetrics): number {
  const ratio = metrics.availableDrivers / Math.max(metrics.activeRequests, 1);
  
  // No surge if supply >= demand
  if (ratio >= 1.0) return 1.0;
  
  // Graduated surge
  if (ratio >= 0.7) return 1.2;
  if (ratio >= 0.5) return 1.5;
  if (ratio >= 0.3) return 1.8;
  if (ratio >= 0.2) return 2.2;
  return 2.5;  // Max surge (configurable by guild)
}
```

### 9.2 Guild Surge Configuration

```typescript
interface GuildSurgeConfig {
  guildId: string;
  
  // Surge limits
  maxMultiplier: number;       // Guild can cap at 2.0x, 3.0x, etc.
  minMultiplier: number;       // Usually 1.0
  
  // Surge triggers
  enableAutoSurge: boolean;
  surgeThreshold: number;      // Supply/demand ratio to trigger
  
  // Revenue split during surge
  surgeRevenueShare: {
    driver: number;            // % of surge premium to driver (e.g., 80%)
    guild: number;             // % to guild treasury (e.g., 20%)
  };
  
  // Rider notification
  requireSurgeConfirmation: boolean;  // Rider must accept surge
}
```

---

## 10. DRIVER-INITIATED MATCHING

### 10.1 Driver Route Posting

```typescript
interface DriverRoutePost {
  driverId: string;
  routeType: 'commute' | 'destination' | 'area';
  
  // For commute/destination
  origin?: LatLng;
  destination?: LatLng;
  departureTime?: Date;
  flexibilityMinutes?: number;  // Can leave +/- this many minutes
  
  // For area patrol
  patrolArea?: {
    center: LatLng;
    radiusKm: number;
  };
  
  // Preferences
  maxPassengers: number;
  acceptsDetour: boolean;
  maxDetourMinutes: number;
  minPrice: number;
  
  // Expiry
  expiresAt: Date;
}
```

### 10.2 Rider Matching to Posted Routes

```typescript
async function matchRiderToDriverRoutes(
  riderRequest: RideRequest
): Promise<DriverRouteMatch[]> {
  // Find driver routes that pass near rider's pickup
  const nearbyRoutes = await findRoutesNearPickup(
    riderRequest.pickup,
    5  // km radius
  );
  
  // Score each route
  const matches = nearbyRoutes.map(route => ({
    route,
    score: scoreRouteMatch(route, riderRequest),
    detour: calculateDetour(route, riderRequest),
    price: calculateRoutePrice(route, riderRequest),
  }));
  
  // Filter and sort
  return matches
    .filter(m => m.detour.minutes <= m.route.maxDetourMinutes)
    .filter(m => m.price >= m.route.minPrice)
    .sort((a, b) => b.score - a.score);
}
```

---

## 11. GUILD ACTIVITY REQUIREMENTS

### 11.1 Activity Tracking

```typescript
interface GuildActivityRequirement {
  guildId: string;
  
  // Minimum activity to maintain membership
  requirements: {
    minRidesPerWeek?: number;
    minRidesPerMonth?: number;
    minHoursOnlinePerWeek?: number;
    minAcceptanceRate?: number;
    minCompletionRate?: number;
  };
  
  // Grace period before removal
  gracePeriodDays: number;
  
  // Warning thresholds
  warningAt: number;  // % of requirement (e.g., 50%)
}
```

### 11.2 Multi-Guild Activity Distribution

```typescript
// Driver in multiple geographic guilds needs activity in each
async function checkGuildActivityCompliance(
  driver: DriverState
): Promise<GuildComplianceStatus[]> {
  const results: GuildComplianceStatus[] = [];
  
  for (const guildId of driver.guilds) {
    const guild = await getGuild(guildId);
    const activity = driver.activityByGuild[guildId];
    
    const weeklyMet = !guild.requirements.minRidesPerWeek || 
      activity.ridesThisWeek >= guild.requirements.minRidesPerWeek;
    
    const monthlyMet = !guild.requirements.minRidesPerMonth ||
      activity.ridesThisMonth >= guild.requirements.minRidesPerMonth;
    
    results.push({
      guildId,
      compliant: weeklyMet && monthlyMet,
      weeklyProgress: activity.ridesThisWeek / (guild.requirements.minRidesPerWeek || 1),
      monthlyProgress: activity.ridesThisMonth / (guild.requirements.minRidesPerMonth || 1),
      warningLevel: calculateWarningLevel(activity, guild.requirements),
    });
  }
  
  return results;
}
```

---

## 12. API SPECIFICATION

### 12.1 Ride Request Endpoints

```typescript
// POST /rides/request
// Create a new ride request
interface CreateRideRequest {
  pickup: {
    lat: number;
    lng: number;
    address?: string;
  };
  dropoff: {
    lat: number;
    lng: number;
    address?: string;
  };
  passengers: number;
  rideType: 'standard' | 'premium' | 'accessibility' | 'shared';
  guildPreference?: string;    // Prefer drivers from this guild
  maxPrice?: number;           // Rider's max willingness to pay
  scheduledAt?: Date;          // For scheduled rides
}

// Response
interface RideRequestResponse {
  requestId: string;
  status: 'matching' | 'matched' | 'no_drivers';
  estimatedMatchTime: number;  // seconds
  priceEstimate: {
    min: number;
    max: number;
    surgeMultiplier: number;
  };
}
```

### 12.2 WebSocket Events

```typescript
// Client → Server
interface WSClientEvents {
  'driver:go_online': { preferences: DriverPreferences };
  'driver:go_offline': {};
  'driver:update_location': { lat: number; lng: number; accuracy: number };
  'driver:accept_offer': { offerId: string };
  'driver:decline_offer': { offerId: string; reason?: string };
  'rider:cancel_request': { requestId: string };
}

// Server → Client
interface WSServerEvents {
  'match:offer': RideOffer;
  'match:found': { rideId: string; driver: DriverInfo };
  'match:failed': { reason: string };
  'match:cancelled': { reason: string };
  'ride:driver_en_route': { eta: number; location: LatLng };
  'ride:driver_arrived': {};
  'ride:started': {};
  'ride:completed': { fare: number };
  'surge:update': { multiplier: number; expiresAt: number };
}
```

---

## 13. PERFORMANCE REQUIREMENTS

| Metric | Target | Notes |
|--------|--------|-------|
| Match Latency (p50) | <5 seconds | From request to driver offer |
| Match Latency (p95) | <15 seconds | Including retries |
| Driver Pool Query | <50ms | Redis GEORADIUS |
| ETA Calculation (single) | <100ms | OSRM query |
| ETA Calculation (batch 20) | <500ms | Parallelized |
| Scoring (100 candidates) | <200ms | In-memory |
| WebSocket Latency | <100ms | Location updates |

---

## 14. MONITORING & METRICS

```typescript
interface MatchingMetrics {
  // Efficiency
  averageMatchTime: number;
  matchSuccessRate: number;
  averageRetriesPerMatch: number;
  
  // Quality
  averagePickupETA: number;
  actualVsEstimatedETA: number;
  postRideRating: number;
  
  // Fairness
  ridesPerDriverStdDev: number;  // Lower = more fair
  driverIdleTimeP50: number;
  driverIdleTimeP95: number;
  
  // Economic
  surgeFrequency: number;
  averageSurgeMultiplier: number;
  driverEarningsPerHour: number;
}
```

---

*Matching Engine Specification v1.0 — Ready for implementation review*
