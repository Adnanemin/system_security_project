

# Cryptographic Sealed-Bid Auction Protocol

## 1. System Overview

This project implements a cryptographic sealed-bid auction using a commit–reveal protocol. Users first submit a commitment (hash of bid + salt), and later reveal their bid. The system verifies correctness and selects the highest valid bid.

---

## 2. Entities

- User: submits bids  
- Server: verifies commitments and selects winner  
- Database: stores commits and reveals  

---

## 3. Phases

### Phase 1 — Commit

User computes:

commitment = H(bid || salt)

User sends:

(user_id, auction_id, commitment)

Server:
- checks deadline  
- stores commitment in database  

---

### Phase 2 — Reveal

User sends:

(user_id, bid, salt)

Server:
- retrieves stored commitment  
- computes H(bid || salt)  
- compares with stored commitment  
- marks bid as valid/invalid  

---

### Phase 3 — Winner Selection

Server:
- selects highest valid bid  
- returns winner  

---

## 4. Security Properties

- Confidentiality: bids are hidden during commit phase  
- Integrity: bids cannot be changed after commit  
- Fairness: all bids are revealed after deadline  

---

## 5. Assumptions

- Hash function is secure (SHA-256)  
- Server is trusted  