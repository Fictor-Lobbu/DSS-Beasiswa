from db import connect_db

conn = connect_db()
c = conn.cursor()

# 🔹 TABEL MAHASISWA
c.execute("""
CREATE TABLE IF NOT EXISTS mahasiswa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT,
    prestasi INTEGER,
    surat INTEGER,
    ipk REAL,
    laporan_ipk INTEGER,
    skor REAL,
    ranking INTEGER
)
""")

# 🔹 TABEL USER (UNTUK LOGIN)
c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
)
""")

# 🔹 CEK USER DEFAULT (BIAR TIDAK DUPLIKAT)
c.execute("SELECT * FROM users WHERE username = ?", ("admin",))
user = c.fetchone()

if not user:
    c.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        ("admin", "123")
    )

conn.commit()
conn.close()

print("Database siap dengan tabel mahasiswa & users!")