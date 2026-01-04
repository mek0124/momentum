import { dbService } from './database';

export const taskService = {
  async saveTask(task) {
    const allTasks = await this.getAllTasks();
    const duplicate = allTasks.find(t => 
      t.id !== task.id && t.title.toLowerCase() === task.title.toLowerCase()
    );
    
    if (duplicate) {
      throw new Error('Task with this title already exists');
    }
    
    return await dbService.saveTask(task);
  },

  async getAllTasks() {
    return await dbService.getAllTasks();
  },

  async deleteTask(id) {
    await dbService.deleteTask(id);
  },

  async updateTask(id, updates) {
    const allTasks = await this.getAllTasks();
    const taskIndex = allTasks.findIndex(t => t.id === id);
    
    if (taskIndex === -1) throw new Error('Task not found');
    
    const updatedTask = { ...allTasks[taskIndex], ...updates };
    await dbService.saveTask(updatedTask);
  }
};