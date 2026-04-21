from flask import Flask, request, jsonify
from database import init_db, get_db
from crypto import commit_hash
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
    
    if row and row[0]:
        deadline = datetime.fromisoformat(row[0])
        if datetime.now() > deadline:
            return False
        return True
    return True
    
def check_reveal_deadline(auction_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT reveal_deadline FROM auctions WHERE id=?", (auction_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row and row[0]:
        deadline = datetime.fromisoformat(row[0])
        if datetime.now() > deadline:
            return False
        return True
    return True

#TEST endpoint
@app.route("/")
def home():
    return "Auction API is running"

#COMMIT
@app.route("/commit", methods=["POST"])
def commit():
    data = request.json
    
    user_id = data["user_id"]
    auction_id = data["auction_id"]
    commitment = data["commitment"]
    
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
    
    # deadline check
    if not check_reveal_deadline(auction_id):
        return jsonify({"error": "Reveal phase ended"}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    
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