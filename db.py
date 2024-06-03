import aiosqlite


async def check_user(telegram_id: int):
    async with aiosqlite.connect('users.db') as db:
        cursor = await db.execute("SELECT telegram_id FROM users WHERE telegram_id = ?", (telegram_id,))
        user_exist = await cursor.fetchone()
        await db.commit()
        return bool(user_exist)

async def add_user(telegram_id: int, username: str):
    async with aiosqlite.connect('users.db') as db:
        await db.execute('''
            INSERT INTO users (telegram_id, username)
            VALUES (?, ?)
        ''', (telegram_id, username))
        await db.commit()

async def create_db():
    try:
        async with aiosqlite.connect('users.db') as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    telegram_id INTEGER UNIQUE,
                    username TEXT   )
                             """)
            await db.commit()
        return bool(True)
    finally:
        return bool(False)

async def drop_db_USER():
    try:
        async with aiosqlite.connect('users.db') as db:
            await db.execute("""
                DROP TABLE users 
                """)
            await db.commit()
        return bool(True)
    finally:
        return bool(False)

async def drop_db_question():
    try:
        async with aiosqlite.connect('users.db') as db:
            await db.execute("""
                DROP TABLE questions 
                """)
            await db.commit()
        return bool(True)
    finally:
        return bool(False)

async def export_users():
    async with aiosqlite.connect('users.db') as db:
        cursor = await db.execute("SELECT telegram_id FROM users")
        users = await cursor.fetchall()
        await db.commit()
        return users



async def init_db():
    async with aiosqlite.connect('support_bot.db') as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                question TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending'
            )
        ''')
        await db.commit()

async def add_question(user_id: int, question: str):
    async with aiosqlite.connect('support_bot.db') as db:
        await db.execute('''
            INSERT INTO questions (user_id, question)
            VALUES (?, ?)
        ''', (user_id, question))
        await db.commit()

async def get_pending_questions():
    async with aiosqlite.connect('support_bot.db') as db:
        cursor = await db.execute('''
            SELECT id, user_id, question
            FROM questions
            WHERE status = 'pending'
        ''')
        return await cursor.fetchall()

async def update_question_status(question_id: int, status: str):
    async with aiosqlite.connect('support_bot.db') as db:
        await db.execute('''
            UPDATE questions
            SET status = ?
            WHERE id = ?
        ''', (status, question_id))
        await db.commit()
