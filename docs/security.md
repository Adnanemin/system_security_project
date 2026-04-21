# Security Analysis

## 1. Overview

This project implements a cryptographic sealed-bid auction using a commit–reveal protocol. The system is designed to ensure confidentiality, integrity, and fairness during the auction process.

---

## 2. Security Properties

### Confidentiality
During the commit phase, bids are hidden by using a cryptographic hash function combined with a random salt. This ensures that no participant can learn other users’ bids before the reveal phase.

### Integrity
The system verifies that bids are not altered after submission by recomputing the hash during the reveal phase and comparing it with the original commitment.

### Fairness
All users submit their commitments before seeing others’ bids. The reveal phase happens only after the commit deadline, ensuring a fair auction process.

---

## 3. Threat Model

The system assumes:
- The server is trusted
- Attackers may try to manipulate bids or gain early access to information
- Users may behave maliciously (e.g., not revealing their bids)

---

## 4. Attack Analysis

### Brute Force Attack
An attacker may try to guess the bid by brute-forcing the hash.
Mitigation:
- Use of salt significantly increases complexity
- SHA-256 is computationally secure

---

### Early Reveal Attack
A user may try to reveal their bid before others.
Mitigation:
- Commit and reveal phases are separated
- Deadline enforcement prevents early reveals

---

### Non-Reveal Attack
A user commits but does not reveal their bid.
Impact:
- The bid is ignored
Mitigation:
- Only revealed and valid bids are considered

---

### Replay Attack
An attacker may try to reuse old data.
Mitigation:
- Each auction has a unique auction_id
- Commitments are tied to specific auctions

---

## 5. Limitations

- The server is assumed to be trusted
- No cryptographic signatures are used
- No penalty system for non-revealing users

---

## 6. Conclusion

The system demonstrates a practical implementation of a secure commit–reveal protocol with basic protections against common attacks, ensuring a fair and reliable auction mechanism.