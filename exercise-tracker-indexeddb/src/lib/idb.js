import { openDB } from 'idb';

const DB_NAME = 'exercise-db';
const STORE_USERS = 'users';
const STORE_PROGRESS = 'progress';
const STORE_CONFIG = 'config';

export async function initDB() {
  const db = await openDB(DB_NAME, 1, {
    upgrade(db) {
      if (!db.objectStoreNames.contains(STORE_USERS)) {
        const u = db.createObjectStore(STORE_USERS, { keyPath: 'id', autoIncrement: true });
        u.createIndex('username', 'username', { unique: true });
      }
      if (!db.objectStoreNames.contains(STORE_PROGRESS)) {
        const p = db.createObjectStore(STORE_PROGRESS, { keyPath: 'id', autoIncrement: true });
        p.createIndex('user_id', 'user_id');
        p.createIndex('date', 'date');
      }
      if (!db.objectStoreNames.contains(STORE_CONFIG)) {
        db.createObjectStore(STORE_CONFIG, { keyPath: 'key' });
      }
    }
  });

  // ✅ Create default admin if not exists
  const adminUser = await db.getFromIndex(STORE_USERS, 'username', 'admin');
  if (!adminUser) {
    await db.add(STORE_USERS, { username: 'admin', password: 'admin123', role: 'admin' });
    console.log('Default admin created: admin / admin123');
  }

  // ensure default config exists
  const cfg = await db.get(STORE_CONFIG, 'challenges');
  if (!cfg) {
    await db.put(STORE_CONFIG, { key: 'challenges', value: { total_challenges: 10, minutes_per_day: 20 } });
  }

  return db;
}

// Users
export async function createUser(db, username, password, role='user') {
  // simple password storage (not hashed) - for demo only
  try {
    const id = await db.add(STORE_USERS, { username, password, role });
    return { id, username, role };
  } catch (err) {
    throw new Error('Username already exists');
  }
}

export async function getUserByUsername(db, username) {
  return await db.getFromIndex(STORE_USERS, 'username', username);
}

// Progress
export async function saveProgress(db, progress) {
  // progress: { user_id, date, challenge, minutes, params: {p1..p5} }
  const entry = {
    user_id: progress.user_id,
    date: progress.date,
    challenge: progress.challenge,
    minutes: progress.minutes,
    param1: progress.params.p1,
    param2: progress.params.p2,
    param3: progress.params.p3,
    param4: progress.params.p4,
    param5: progress.params.p5
  };
  const id = await db.add(STORE_PROGRESS, entry);
  return id;
}

export async function getProgressByUser(db, user_id) {
  return await db.getAllFromIndex(STORE_PROGRESS, 'user_id', IDBKeyRange.only(Number(user_id)));
}

export async function getAllUsers(db) {
  return await db.getAll(STORE_USERS);
}

export async function getConfig(db) {
  const c = await db.get(STORE_CONFIG, 'challenges');
  return c ? c.value : null;
}

export async function setConfig(db, cfg) {
  await db.put(STORE_CONFIG, { key: 'challenges', value: cfg });
}
