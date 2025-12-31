import { dbService } from './database';

export async function migrateFromLocalStorage(): Promise<void> {
  const oldData = localStorage.getItem('tasks');
  if (!oldData) return;

  try {
    const tasks = JSON.parse(oldData);
    for (const task of tasks) {
      await dbService.saveTask(task);
    }
    
    // Clear old data after successful migration
    localStorage.removeItem('tasks');
    console.log('Migration completed successfully');
  } catch (error) {
    console.error('Migration failed:', error);
  }
}