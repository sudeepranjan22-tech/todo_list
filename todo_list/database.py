import aiosqlite
from datetime import datetime

DATABASE = "todo.db"

# Create the todos table
async def init_db():
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS todos (
                task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_name TEXT NOT NULL,
                description TEXT,
                person TEXT,
                status TEXT DEFAULT 'pending',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()

# Add a new task to the todos table
async def add_task(task_name, description, person, status="pending"):
    now = datetime.utcnow().isoformat()
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute("""
            INSERT INTO todos (task_name, description, person, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (task_name, description, person, status, now, now))
        await db.commit()

# Get all tasks
async def get_all_tasks():
    async with aiosqlite.connect(DATABASE) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM todos ORDER BY created_at DESC")
        tasks = await cursor.fetchall()
        return [dict(task) for task in tasks]

# Update a task
async def update_task(task_id, task_name, description, person, status):
    now = datetime.utcnow().isoformat()
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute("""
            UPDATE todos
            SET task_name = ?, description = ?, person = ?, status = ?, updated_at = ?
            WHERE task_id = ?
        """, (task_name, description, person, status, now, task_id))
        await db.commit()

# Delete a task
async def delete_task(task_id):
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute("DELETE FROM todos WHERE task_id = ?", (task_id,))
        await db.commit()
# Get task by id
async def get_task_by_id(task_id):
    async with aiosqlite.connect(DATABASE) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM todos WHERE task_id = ?", (task_id,))
        task = await cursor.fetchone()
        return dict(task) if task else None
