from flask import Flask, request, jsonify
from database import init_db, get_db
from crypto import commit_hash, hash_password
from datetime import datetime

app = Flask(__name__)

init_db()

# helper to check deadlines
def check_commit_deadline(auction_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT commit_deadline FROM auctions WHERE id=?", (auction_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return True  # no auction found, allow for now

    deadline = row[0]
    if deadline:
        deadline = datetime.fromisoformat(deadline)
        return datetime.now() <= deadline

    return True
    
def check_reveal_deadline(auction_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT reveal_deadline FROM auctions WHERE id=?", (auction_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return True  # no auction found, allow for now

    deadline = row[0]
    if deadline:
        deadline = datetime.fromisoformat(deadline)
        return datetime.now() <= deadline

    return True

#TEST endpoint
@app.route("/")
def home():
    return "Auction API is running"

#REGIRSTER
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    
    username = data["username"]
    password = data["password"]
    
    hashed = hash_password(password)
    
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
        INSERT INTO users (username, password)
        VALUES (?, ?)
        """, (username, hashed))

        conn.commit()
        return jsonify({"message": "User created"})
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        conn.close()
        
#LOGIN
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    
    username = data["username"]
    password = data["password"]
    
    hashed = hash_password(password)
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT id FROM users
    WHERE username=? AND password=?
    """, (username, hashed))

    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return jsonify({"error": "Invalid credentials"}), 401
    
    return jsonify({
        "message": "Login successful",
        "user_id": row["id"]
    })

#COMMIT
@app.route("/commit", methods=["POST"])
def commit():
    data = request.json
    
    user_id = data["user_id"]
    auction_id = data["auction_id"]
    bid = data["bid"]
    salt = data["salt"]

    if not all([user_id, auction_id, bid, salt]):
        return jsonify({"error": "Missing fields"}), 400

    commitment = commit_hash(bid, salt)
    
    # deadline check
    if not check_commit_deadline(auction_id):
        return jsonify({"error": "Commit phase ended"}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
        INSERT INTO commits (user_id, auction_id, commitment, timestamp)
        VALUES (?, ?, ?, datetime('now'))
        """, (user_id, auction_id, commitment))
        
        conn.commit()
        return jsonify({"message": "Commit stored"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()
    

#REVEAL
@app.route("/reveal", methods=["POST"])
def reveal():
    data = request.json
    
    user_id = data["user_id"]
    auction_id = data["auction_id"]
    bid = data["bid"]
    salt = data["salt"]

    if not all([user_id, auction_id, bid, salt]):
        return jsonify({"error": "Missing fields"}), 400
    
    # deadline check
    if not check_reveal_deadline(auction_id):
        return jsonify({"error": "Reveal phase ended"}), 400
    
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id FROM reveals
    WHERE user_id=? AND auction_id=?
    """, (user_id, auction_id))
    
    existing = cursor.fetchone()
    if existing:
        return jsonify({"error": "Reveal already submitted"}), 400
    
    try:
        cursor.execute("""
        SELECT commitment FROM commits
        WHERE user_id=? AND auction_id=?
        """, (user_id, auction_id))
        
        row = cursor.fetchone()
        
        if not row:
            return jsonify({"error": "No commit found"}), 400
        
        stored_commitment = row["commitment"]
        computed = commit_hash(bid, salt)

        valid = int(computed == stored_commitment)

        cursor.execute("""
        INSERT INTO reveals (user_id, auction_id, bid, salt, valid)
        VALUES (?, ?, ?, ?, ?)
        """, (user_id, auction_id, bid, salt, valid))

        conn.commit()
        
        return jsonify({"valid": bool(valid)})
    finally:
        conn.close()

#WINNER
@app.route("/winner/<int:auction_id>")
def winner(auction_id):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        SELECT user_id, bid FROM reveals
        WHERE auction_id=? AND valid=1
        ORDER BY bid DESC
        LIMIT 1
        """, (auction_id,))
        
        row = cursor.fetchone()

        if not row:
            return jsonify({"message": "No valid bids"})
        return jsonify({
            "winner_user_id": row["user_id"],
            "bid": row["bid"]
        })
    finally:
        conn.close()
    
    
if __name__ == "__main__":
    app.run(debug=False)