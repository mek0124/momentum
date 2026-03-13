import { useState, useEffect } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPencil, faTrashCan, faSave, faRefresh, faExclamationTriangle } from "@fortawesome/free-solid-svg-icons";
import { addTask, getAllTasks, deleteTask, type Task } from "../utils/idb";

export default function Dashboard() {
  const [taskItemData, setTaskItemData] = useState({
    title: '',
    content: '',
    priority: '3', // Default to low priority
    dueTime: '',
    dueDate: ''
  });

  const [allTasks, setAllTasks] = useState<Task[]>([]);
  const [error, setError] = useState<string>('');
  const [editingId, setEditingId] = useState<number | null>(null);

  const loadTasks = async () => {
    try {
      const tasks = await getAllTasks();
      setAllTasks(tasks);
    } catch (err) {
      console.error('Failed to load tasks:', err);
      setError('Failed to load tasks');
    }
  };

  // Load tasks from IndexedDB on component mount
  useEffect(() => {
    loadTasks();
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setTaskItemData({
      ...taskItemData,
      [name]: value,
    });
    setError('');
  };

  const clearForm = () => {
    setTaskItemData({
      title: '',
      content: '',
      priority: '3',
      dueTime: '',
      dueDate: ''
    });
    setEditingId(null);
    setError('');
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    // Validate title and content are not empty
    if (!taskItemData.title.trim()) {
      setError('Title is required');
      return;
    }

    if (!taskItemData.content.trim()) {
      setError('Content is required');
      return;
    }

    try {
      if (editingId !== null) {
        // Update existing task by deleting and re-adding
        await deleteTask(editingId);
        const newTask = await addTask({
          title: taskItemData.title,
          content: taskItemData.content,
          priority: taskItemData.priority,
          dueTime: taskItemData.dueTime,
          dueDate: taskItemData.dueDate
        });
        setAllTasks(prev => prev.map(t => t.id === editingId ? newTask : t));
      } else {
        // Save new task to IndexedDB
        const newTask = await addTask({
          title: taskItemData.title,
          content: taskItemData.content,
          priority: taskItemData.priority,
          dueTime: taskItemData.dueTime,
          dueDate: taskItemData.dueDate
        });
        
        // Update list state
        setAllTasks(prev => [...prev, newTask]);
      }

      // Refresh UI
      clearForm();
    } catch (err) {
      console.error('Failed to save task:', err);
      setError('Failed to save task');
    }
  };

  const handleEdit = (task: Task) => {
    setTaskItemData({
      title: task.title,
      content: task.content,
      priority: task.priority,
      dueTime: task.dueTime,
      dueDate: task.dueDate
    });
    setEditingId(task.id || null);
    setError('');
  };

  const handleDelete = async (id: number) => {
    try {
      await deleteTask(id);
      setAllTasks(prev => prev.filter(t => t.id !== id));
    } catch (err) {
      console.error('Failed to delete task:', err);
      setError('Failed to delete task');
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case '1': return 'text-error'; // High
      case '2': return 'text-warning'; // Medium
      case '3': return 'text-success'; // Low
      default: return 'text-text_primary';
    }
  };

  const getPriorityLabel = (priority: string) => {
    switch (priority) {
      case '1': return 'High';
      case '2': return 'Medium';
      case '3': return 'Low';
      default: return 'Unknown';
    }
  };

  const displayCurrentTasks = () => {
    return allTasks.map((task) => {
      return (
        <div key={task.id} className="flex flex-row items-center justify-between w-full p-4 border-b border-accent hover:bg-secondary/50 transition-colors">
          <div className="flex flex-col flex-grow pr-4">
            <h3 className="font-bold text-lg text-text_primary">{task.title}</h3>
            <p className="text-sm text-text_secondary mt-1">{task.content}</p>
            <div className="flex flex-row items-center gap-4 mt-2 text-sm">
              <span className={`font-semibold ${getPriorityColor(task.priority)}`}>
                {getPriorityLabel(task.priority)}
              </span>
              {task.dueDate && (
                <span className="text-text_secondary">
                  Due: {new Date(task.dueDate).toLocaleDateString()}
                  {task.dueTime && ` at ${task.dueTime}`}
                </span>
              )}
            </div>
          </div>
          
          <div className="flex flex-row items-center gap-2">
            <button
              onClick={() => handleEdit(task)}
              className="p-2 text-primary hover:text-primary_hover transition-colors"
              title="Edit task"
            >
              <FontAwesomeIcon icon={faPencil} />
            </button>
            <button
              onClick={() => task.id && handleDelete(task.id)}
              className="p-2 text-error hover:text-error_hover transition-colors"
              title="Delete task"
            >
              <FontAwesomeIcon icon={faTrashCan} />
            </button>
          </div>
        </div>
      );
    });
  };

  return (
    <div className="flex flex-col items-center justify-center w-full flex-grow p-4 bg-gradient-to-br from-secondary to-teritary min-h-screen">
      <div className="w-full max-w-[65vw] flex flex-col lg:flex-row gap-6">
        {/* Task List Section */}
        <div className="flex flex-col flex-grow lg:w-[55%] bg-white/10 backdrop-blur-sm rounded-2xl border border-accent shadow-xl overflow-hidden">
          <div className="p-4 border-b border-accent bg-secondary/50">
            <h2 className="text-xl font-bold text-text_primary flex items-center gap-2">
              <FontAwesomeIcon icon={faPencil} />
              Tasks
            </h2>
          </div>
          
          <div className="flex flex-col flex-grow overflow-y-auto h-[768px]">
            {allTasks.length === 0 ? (
              <div className="flex flex-col items-center justify-center w-full flex-grow p-8 text-center">
                <FontAwesomeIcon icon={faExclamationTriangle} className="text-4xl text-text_secondary mb-4" />
                <span className="font-bold italic text-xl text-text_secondary">
                  No Tasks Currently Exist...
                </span>
                <span className="text-text_secondary mt-2">
                  Create your first task using the form on the right.
                </span>
              </div>
            ) : (
              <div className="flex flex-col">
                {displayCurrentTasks()}
              </div>
            )}
          </div>
        </div>

        {/* Task Form Section */}
        <form
          onSubmit={handleSubmit}
          className="flex flex-row flex-grow lg:w-[55%] bg-white/10 backdrop-blur-sm rounded-2xl border border-accent shadow-xl overflow-hidden"
        >
          <div className="flex flex-col justify-start gap-16 flex-grow w-1/2 p-6 border-r border-accent overflow-y-auto h-[768px]">
            <h3 className="text-lg font-bold text-text_primary mb-4">Task Details</h3>
            
            {/* Title */}
            <div className="mb-4">
              <label
                htmlFor="title"
                className="block text-sm font-medium text-text_primary mb-1"
              >
                Title *
              </label>
              <input
                type="text"
                id="title"
                name="title"
                value={taskItemData.title}
                onChange={handleChange}
                placeholder="Enter task title"
                className="w-full px-3 py-2 border-2 border-accent rounded-xl outline-none bg-secondary hover:bg-accent_hover hover:outline-none focus:outline-none focus:bg-teritary text-text_primary"
              />
            </div>

            {/* Priority */}
            <div className="mb-4">
              <label
                htmlFor="priority"
                className="block text-sm font-medium text-text_primary mb-1"
              >
                Priority
              </label>
              <select
                id="priority"
                name="priority"
                value={taskItemData.priority}
                onChange={handleChange}
                className="w-full px-3 py-2 border-2 border-accent rounded-xl outline-none bg-secondary hover:bg-accent_hover hover:outline-none focus:outline-none focus:bg-teritary text-text_primary"
              >
                <option value="1">High</option>
                <option value="2">Medium</option>
                <option value="3">Low</option>
              </select>
            </div>

            {/* Due Time */}
            <div className="mb-4">
              <label
                htmlFor="dueTime"
                className="block text-sm font-medium text-text_primary mb-1"
              >
                Due Time
              </label>
              <input
                type="time"
                id="dueTime"
                name="dueTime"
                value={taskItemData.dueTime}
                onChange={handleChange}
                className="w-full px-3 py-2 border-2 border-accent rounded-xl outline-none bg-secondary hover:bg-accent_hover hover:outline-none focus:outline-none focus:bg-teritary text-text_primary"
              />
            </div>

            {/* Due Date */}
            <div className="mb-4">
              <label
                htmlFor="dueDate"
                className="block text-sm font-medium text-text_primary mb-1"
              >
                Due Date
              </label>
              <input
                type="date"
                id="dueDate"
                name="dueDate"
                value={taskItemData.dueDate}
                onChange={handleChange}
                className="w-full px-3 py-2 border-2 border-accent rounded-xl outline-none bg-secondary hover:bg-accent_hover hover:outline-none focus:outline-none focus:bg-teritary text-text_primary"
              />
            </div>
          </div>

          <div className="flex flex-col flex-grow w-1/2 p-6 overflow-y-auto max-h-[1008px]">
            {/* Content */}
            <div className="flex flex-col flex-grow mb-4">
              <label
                htmlFor="content"
                className="block text-sm font-medium text-text_primary mb-1"
              >
                Content *
              </label>
              <textarea
                id="content"
                name="content"
                value={taskItemData.content}
                onChange={handleChange}
                placeholder="Enter task description"
                className="flex-grow px-3 py-2 border-2 border-accent rounded-xl outline-none bg-secondary hover:bg-accent_hover hover:outline-none focus:outline-none focus:bg-teritary text-text_primary resize-none"
              />
            </div>

            {/* Error Message */}
            {error && (
              <div className="mb-4 p-3 bg-error/20 border border-error rounded-lg text-error text-sm flex items-center gap-2">
                <FontAwesomeIcon icon={faExclamationTriangle} />
                {error}
              </div>
            )}

            {/* Buttons */}
            <div className="flex flex-row items-center justify-between gap-4 mt-auto">
              <button
                type="button"
                onClick={clearForm}
                className="flex-1 px-4 py-3 border-2 border-error rounded-xl outline-none text-error hover:bg-error/20 transition-colors flex items-center justify-center gap-2"
              >
                <FontAwesomeIcon icon={faRefresh} />
                Reset
              </button>
              
              <button
                type="submit"
                className="flex-1 px-4 py-3 border-2 border-success rounded-xl outline-none text-success hover:bg-success/20 transition-colors flex items-center justify-center gap-2"
              >
                <FontAwesomeIcon icon={faSave} />
                {editingId ? 'Update' : 'Save'}
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
};
