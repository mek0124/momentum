/**
 * Momentum - Task Manager Application
 * Frontend JavaScript for task management
 */

// ==================== State ====================

let tasks = [];
let currentFilter = 'all';
let editingTaskId = null;

// ==================== DOM Elements ====================

const elements = {
    taskForm: document.getElementById('task-form'),
    taskTitle: document.getElementById('task-title'),
    taskContent: document.getElementById('task-content'),
    tasksList: document.getElementById('tasks-list'),
    tasksCount: document.getElementById('tasks-count'),
    emptyState: document.getElementById('empty-state'),
    loadingState: document.getElementById('loading-state'),
    filterTabs: document.querySelectorAll('.filter-tab'),
    editModal: document.getElementById('edit-modal'),
    editForm: document.getElementById('edit-form'),
    editTaskId: document.getElementById('edit-task-id'),
    editTitle: document.getElementById('edit-title'),
    editContent: document.getElementById('edit-content'),
    modalClose: document.getElementById('modal-close'),
    cancelEdit: document.getElementById('cancel-edit'),
    toast: document.getElementById('toast'),
    toastMessage: document.getElementById('toast-message'),
};

// ==================== API Functions ====================

async function api(endpoint, options = {}) {
    const response = await fetch(`/api${endpoint}`, {
        ...options,
        headers: {
            'Content-Type': 'application/json',
            ...options.headers,
        },
    });
    
    const data = await response.json();
    
    if (!response.ok) {
        throw new Error(data.error || 'Something went wrong');
    }
    
    return data;
}

async function fetchTasks(filter = 'all') {
    try {
        showLoading();
        let url = '/tasks';
        
        if (filter !== 'all') {
            url += `?status=${filter}`;
        }
        
        const data = await api(url);
        tasks = data.tasks;
        renderTasks();
    } catch (error) {
        showToast(error.message, 'error');
    }
}

async function createTask(title, content) {
    try {
        const data = await api('/tasks', {
            method: 'POST',
            body: JSON.stringify({ title, content }),
        });
        
        showToast('Task created successfully', 'success');
        elements.taskForm.reset();
        fetchTasks(currentFilter);
    } catch (error) {
        showToast(error.message, 'error');
    }
}

async function updateTask(taskId, updates) {
    try {
        const data = await api(`/tasks/${taskId}`, {
            method: 'PUT',
            body: JSON.stringify(updates),
        });
        
        showToast('Task updated successfully', 'success');
        fetchTasks(currentFilter);
    } catch (error) {
        showToast(error.message, 'error');
    }
}

async function deleteTask(taskId) {
    try {
        await api(`/tasks/${taskId}`, {
            method: 'DELETE',
        });
        
        showToast('Task deleted successfully', 'success');
        fetchTasks(currentFilter);
    } catch (error) {
        showToast(error.message, 'error');
    }
}

async function toggleTask(taskId) {
    try {
        await api(`/tasks/toggle/${taskId}`, {
            method: 'POST',
        });
        
        fetchTasks(currentFilter);
    } catch (error) {
        showToast(error.message, 'error');
    }
}

// ==================== Render Functions ====================

function showLoading() {
    elements.loadingState.classList.remove('hidden');
    elements.emptyState.classList.add('hidden');
    elements.tasksList.innerHTML = '';
}

function hideLoading() {
    elements.loadingState.classList.add('hidden');
}

function renderTasks() {
    hideLoading();
    
    if (tasks.length === 0) {
        elements.emptyState.classList.remove('hidden');
        elements.tasksList.innerHTML = '';
    } else {
        elements.emptyState.classList.add('hidden');
        elements.tasksList.innerHTML = tasks.map(task => renderTask(task)).join('');
        attachTaskListeners();
    }
    
    updateTasksCount();
}

function renderTask(task) {
    const createdDate = new Date(task.created_at).toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
    });
    
    return `
        <div class="task-item ${task.completed ? 'completed' : ''}" data-id="${task.id}">
            <input 
                type="checkbox" 
                class="task-checkbox" 
                ${task.completed ? 'checked' : ''}
                title="Mark as ${task.completed ? 'incomplete' : 'complete'}"
            >
            <div class="task-content">
                <div class="task-title">${escapeHtml(task.title)}</div>
                ${task.content ? `<div class="task-description">${escapeHtml(task.content)}</div>` : ''}
                <div class="task-meta">
                    <span class="task-date">
                        <svg width="12" height="12" viewBox="0 0 20 20" fill="currentColor">
                            <path fill-rule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clip-rule="evenodd"/>
                        </svg>
                        ${createdDate}
                    </span>
                </div>
            </div>
            <div class="task-actions">
                <button class="btn btn-ghost btn-sm edit-btn" title="Edit task">
                    <svg width="16" height="16" viewBox="0 0 20 20" fill="currentColor">
                        <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z"/>
                    </svg>
                </button>
                <button class="btn btn-ghost btn-sm delete-btn" title="Delete task">
                    <svg width="16" height="16" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd"/>
                    </svg>
                </button>
            </div>
        </div>
    `;
}

function updateTasksCount() {
    const count = tasks.length;
    const taskWord = count === 1 ? 'task' : 'tasks';
    elements.tasksCount.textContent = `${count} ${taskWord}`;
}

function attachTaskListeners() {
    // Checkbox listeners
    document.querySelectorAll('.task-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', (e) => {
            const taskId = parseInt(e.target.closest('.task-item').dataset.id);
            toggleTask(taskId);
        });
    });
    
    // Edit button listeners
    document.querySelectorAll('.edit-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const taskId = parseInt(e.target.closest('.task-item').dataset.id);
            openEditModal(taskId);
        });
    });
    
    // Delete button listeners
    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const taskId = parseInt(e.target.closest('.task-item').dataset.id);
            if (confirm('Are you sure you want to delete this task?')) {
                deleteTask(taskId);
            }
        });
    });
}

// ==================== Modal Functions ====================

function openEditModal(taskId) {
    const task = tasks.find(t => t.id === taskId);
    if (!task) return;
    
    editingTaskId = taskId;
    elements.editTaskId.value = taskId;
    elements.editTitle.value = task.title;
    elements.editContent.value = task.content || '';
    
    elements.editModal.classList.remove('hidden');
    elements.editTitle.focus();
}

function closeEditModal() {
    elements.editModal.classList.add('hidden');
    editingTaskId = null;
    elements.editForm.reset();
}

// ==================== Toast Notifications ====================

function showToast(message, type = 'success') {
    elements.toastMessage.textContent = message;
    elements.toast.className = `toast ${type}`;
    elements.toast.classList.remove('hidden');
    
    setTimeout(() => {
        elements.toast.classList.add('hidden');
    }, 3000);
}

// ==================== Utility Functions ====================

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// ==================== Event Listeners ====================

// Form submission
elements.taskForm.addEventListener('submit', (e) => {
    e.preventDefault();
    
    const title = elements.taskTitle.value.trim();
    const content = elements.taskContent.value.trim();
    
    if (!title) {
        showToast('Title is required', 'error');
        return;
    }
    
    createTask(title, content);
});

// Filter tabs
elements.filterTabs.forEach(tab => {
    tab.addEventListener('click', () => {
        elements.filterTabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        
        currentFilter = tab.dataset.filter;
        fetchTasks(currentFilter);
    });
});

// Edit modal
elements.modalClose.addEventListener('click', closeEditModal);
elements.cancelEdit.addEventListener('click', closeEditModal);
elements.editModal.querySelector('.modal-backdrop').addEventListener('click', closeEditModal);

elements.editForm.addEventListener('submit', (e) => {
    e.preventDefault();
    
    const title = elements.editTitle.value.trim();
    const content = elements.editContent.value.trim();
    
    if (!title) {
        showToast('Title is required', 'error');
        return;
    }
    
    updateTask(editingTaskId, { title, content });
    closeEditModal();
});

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Close modal on Escape
    if (e.key === 'Escape' && !elements.editModal.classList.contains('hidden')) {
        closeEditModal();
    }
    
    // Focus title input on '/'
    if (e.key === '/' && document.activeElement !== elements.taskTitle) {
        e.preventDefault();
        elements.taskTitle.focus();
    }
});

// Close modal on outside click
elements.editModal.addEventListener('click', (e) => {
    if (e.target === elements.editModal) {
        closeEditModal();
    }
});

// ==================== Initialization ====================

document.addEventListener('DOMContentLoaded', () => {
    fetchTasks();
});
