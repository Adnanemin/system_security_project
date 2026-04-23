

# 🔐 Secure Auction System (Commit–Reveal Protocol)

This project implements a secure auction system using a **commit–reveal protocol** combined with **cryptographic hashing and digital signatures**.

## 🎯 Objective

The goal is to ensure:

- Fair bidding (no early disclosure of bids)
- Data integrity
- User authenticity
- Prevention of cheating or manipulation

---

## ⚙️ How It Works

### 1. Commit Phase
- User submits a bid in a **hidden form**
- A **salt value** is generated
- System computes:

```
commitment = hash(bid + salt)
```

- The commitment is signed using the user's private key
- Only the commitment (not the actual bid) is stored

---

### 2. Reveal Phase
- User submits:
  - bid
  - salt

- System verifies:
  - hash matches stored commitment
  - digital signature is valid

---

### 3. Winner Selection
- Only **valid revealed bids** are considered
- Highest bid wins

---

## 🔐 Security Features

- **Hashing (SHA-256)** → ensures data integrity  
- **Salt** → prevents brute-force attacks  
- **Digital Signature (RSA)** → ensures authenticity  
- **Commit–Reveal Protocol** → ensures fairness  
- **One Commit per User** → prevents manipulation  

---

## 🧑‍💻 Technologies Used

- **Backend:** Python (Flask)
- **Database:** SQLite
- **Frontend:** HTML, CSS, JavaScript
- **Cryptography:** RSA, SHA-256

---

## 🚀 How to Run

### 1. Start Backend

```bash
cd backend
python app.py
```

---

### 2. Open Frontend

Use a local server (recommended):

```bash
cd frontend
python -m http.server 8000
```

Then open:

```
http://localhost:8000
```

---

## 🧪 Demo Flow

1. Register two users  
2. Login  
3. Generate salt  
4. Commit bids  
5. Reveal bids  
6. View winner  

---

## ⚠️ Notes

- Users must **save their salt** after commit  
- Without salt, reveal is not possible  
- Each user can only commit once per auction  

---

## 🔮 Future Improvements

- Server-side salt generation  
- Multi-auction support  
- UI enhancements  
- Better session management (JWT / tokens)  

---

## 👨‍🎓 Project Context

This project was developed as part of a **System Security course**, focusing on practical implementation of cryptographic protocols.