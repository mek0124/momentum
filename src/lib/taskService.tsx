import { dbService } from './database';

export interface Task {
  id: string;
  title: string;
  details: string;
  dueDate?: string;
  dueTime?: string;
  priority: number;
  completed: boolean;
  updatedAt?: string;
}

export const taskService = {
  async saveTask(task: Task): Promise<string> {
    // Check for duplicates (decrypt and compare in memory)
    const allTasks = await this.getAllTasks();
    const duplicate = allTasks.find(t => 
      t.id !== task.id && t.title.toLowerCase() === task.title.toLowerCase()
    );
    
    if (duplicate) {
      throw new Error('Task with this title already exists');
    }
    
    return await dbService.saveTask(task);
  },

  async getAllTasks(): Promise<Task[]> {
    return await dbService.getAllTasks();
  },

  async deleteTask(id: string): Promise<void> {
    await dbService.deleteTask(id);
  },

  async updateTask(id: string, updates: Partial<Task>): Promise<void> {
    const allTasks = await this.getAllTasks();
    const taskIndex = allTasks.findIndex(t => t.id === id);
    
    if (taskIndex === -1) throw new Error('Task not found');
    
    const updatedTask = { ...allTasks[taskIndex], ...updates };
    await dbService.saveTask(updatedTask);
  }
};