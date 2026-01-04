import { openDB } from 'idb';
import CryptoJS from 'crypto-js';

class DatabaseService {
  constructor() {
    this.db = null;
    this.encryptionKey = 'user-defined-secret-key';
  }

  async initialize() {
    this.db = await openDB('momentum-db', 1, {
      upgrade(db) {
        const taskStore = db.createObjectStore('tasks', { keyPath: 'id' });
        taskStore.createIndex('by-createdAt', 'createdAt');
      },
    });
  }

  encryptTask(task) {
    const iv = CryptoJS.lib.WordArray.random(128 / 8).toString();
    const encrypted = CryptoJS.AES.encrypt(
      JSON.stringify(task),
      this.encryptionKey,
      { iv: CryptoJS.enc.Hex.parse(iv) }
    );
    return {
      encryptedData: encrypted.toString(),
      iv: iv
    };
  }

  decryptTask(encryptedTask) {
    const decrypted = CryptoJS.AES.decrypt(
      encryptedTask.encryptedData,
      this.encryptionKey,
      { iv: CryptoJS.enc.Hex.parse(encryptedTask.iv) }
    );
    return JSON.parse(decrypted.toString(CryptoJS.enc.Utf8));
  }

  async saveTask(task) {
    if (!this.db) await this.initialize();
    
    const id = task.id || Date.now().toString();
    const { encryptedData, iv } = this.encryptTask(task);
    
    await this.db.put('tasks', {
      id,
      encryptedData,
      iv,
      createdAt: new Date(),
      updatedAt: new Date()
    });
    
    return id;
  }

  async getAllTasks() {
    if (!this.db) await this.initialize();
    
    const encryptedTasks = await this.db.getAll('tasks');
    return encryptedTasks.map(task => this.decryptTask(task));
  }

  async deleteTask(id) {
    if (!this.db) await this.initialize();
    await this.db.delete('tasks', id);
  }
}

export const dbService = new DatabaseService();