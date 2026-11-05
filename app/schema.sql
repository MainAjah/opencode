PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL CHECK (length(trim(name)) > 0),
    total_stock INTEGER NOT NULL CHECK (total_stock >= 0),
    available_stock INTEGER NOT NULL CHECK (
        available_stock >= 0 AND available_stock <= total_stock
    )
);

CREATE TABLE IF NOT EXISTS loans (
    id INTEGER PRIMARY KEY,
    student_id TEXT NOT NULL CHECK (length(trim(student_id)) > 0),
    item_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    status TEXT NOT NULL DEFAULT 'BORROWED' CHECK (
        status IN ('BORROWED', 'RETURNED', 'CANCELLED')
    ),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (item_id) REFERENCES items (id)
);

CREATE INDEX IF NOT EXISTS idx_loans_student_id ON loans (student_id);
CREATE INDEX IF NOT EXISTS idx_loans_item_id ON loans (item_id);
