import { openDB, DBSchema, IDBPDatabase } from 'idb';
import CryptoJS from 'crypto-js';

interface EncryptedTask {
  id: string;
  encryptedData: string; // Encrypted JSON string
  iv: string; // Initialization vector for AES
  createdAt: Date;
  updatedAt: Date;
}

interface MomentumDB extends DBSchema {
  tasks: {
    key: string;
    value: EncryptedTask;
    indexes: { 'by-createdAt': Date };
  };
}

class DatabaseService {
  private db: IDBPDatabase<MomentumDB> | null = null;
  private encryptionKey: string = 'user-defined-secret-key'; // Should be user-provided!

  async initialize() {
    this.db = await openDB<MomentumDB>('momentum-db', 1, {
      upgrade(db) {
        const taskStore = db.createObjectStore('tasks', { keyPath: 'id' });
        taskStore.createIndex('by-createdAt', 'createdAt');
      },
    });
  }

  // Encryption methods
  encryptTask(task: any): { encryptedData: string; iv: string } {
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

  decryptTask(encryptedTask: EncryptedTask): any {
    const decrypted = CryptoJS.AES.decrypt(
      encryptedTask.encryptedData,
      this.encryptionKey,
      { iv: CryptoJS.enc.Hex.parse(encryptedTask.iv) }
    );
    return JSON.parse(decrypted.toString(CryptoJS.enc.Utf8));
  }

  // CRUD operations
  async saveTask(task: any): Promise<string> {
    if (!this.db) await this.initialize();
    
    const id = task.id || Date.now().toString();
    const { encryptedData, iv } = this.encryptTask(task);
    
    await this.db!.put('tasks', {
      id,
      encryptedData,
      iv,
      createdAt: new Date(),
      updatedAt: new Date()
    });
    
    return id;
  }

  async getAllTasks(): Promise<any[]> {
    if (!this.db) await this.initialize();
    
    const encryptedTasks = await this.db!.getAll('tasks');
    return encryptedTasks.map(task => this.decryptTask(task));
  }

  async deleteTask(id: string): Promise<void> {
    if (!this.db) await this.initialize();
    await this.db!.delete('tasks', id);
  }
}

export const dbService = new DatabaseService();