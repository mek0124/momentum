import { useState, useEffect } from "react";

export const TaskModal = ({ isVisible, onClose, onCreate, onUpdate, taskId }) => {
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [dueDate, setDueDate] = useState("");
  const [reminder, setReminder] = useState(false);
  const [message, setMessage] = useState({ text: "", isError: false });
  const [isEditing, setIsEditing] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false); // Added to track submission state

  useEffect(() => {
    if (taskId) {
      const existingTasks = JSON.parse(window.localStorage.getItem('tasks') || '[]');
      const taskToEdit = existingTasks.find(task => task.id === taskId);
      
      if (taskToEdit) {
        setTitle(taskToEdit.title || "");
        setContent(taskToEdit.content || "");
        setDueDate(taskToEdit.dueDate || "");
        setReminder(taskToEdit.reminder || false);
        setIsEditing(true);
      }
    } else {
      resetForm();
      setIsEditing(false);
    }
  }, [taskId, isVisible]);

  const resetForm = () => {
    setTitle("");
    setContent("");
    setDueDate("");
    setReminder(false);
    setMessage({ text: "", isError: false });
    setIsSubmitting(false);
  };

  const handleErrorSuccess = (is_error, messageText) => {
    setMessage({ text: messageText, isError: is_error });
    
    setTimeout(() => {
      setMessage({ text: "", isError: false });
      
      if (!is_error) {
        onClose();
        resetForm();
      }
    }, 3000);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (isSubmitting) return; // Prevent multiple submissions
    
    if (!title.trim()) {
      handleErrorSuccess(true, "Title is required");
      return;
    }
    
    setIsSubmitting(true);
    
    const task = {
      id: isEditing ? taskId : Date.now(),
      title: title.trim(),
      content: content.trim(),
      dueDate,
      reminder,
      createdAt: isEditing ? undefined : new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };
    
    try {
      if (isEditing) {
        // Call onUpdate but don't close modal immediately
        await onUpdate(task);
        handleErrorSuccess(false, "Task updated successfully!");
      } else {
        // Call onCreate but don't close modal immediately
        await onCreate(task);
        handleErrorSuccess(false, "Task created successfully!");
      }
    } catch (error) {
      handleErrorSuccess(true, "Failed to save task");
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleOverlayClick = (e) => {
    if (e.target === e.currentTarget && !isSubmitting) {
      onClose();
      resetForm();
    }
  };

  if (!isVisible) return null;

  return (
    <div 
      className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
      onClick={handleOverlayClick}
    >
      <div className="bg-accent rounded-lg w-full max-w-md p-6">
        <h2 className="text-xl font-bold mb-4 text-foreground italic w-full text-center">
          {isEditing ? "Edit Task" : "Create New Task"}
        </h2>
        
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-foreground text-sm font-bold mb-2">
              Title *
            </label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 bg-gray-700 text-foreground rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Enter task title"
              disabled={isSubmitting}
            />
          </div>

          <div className="mb-4">
            <label className="block text-foreground text-sm font-bold mb-2">
              Content
            </label>
            <textarea
              value={content}
              onChange={(e) => setContent(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 bg-gray-700 text-foreground rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              rows="3"
              placeholder="Enter task description"
              disabled={isSubmitting}
            />
          </div>

          <div className="mb-4">
            <label className="block text-foreground text-sm font-bold mb-2">
              Due Date
            </label>
            <input
              type="datetime-local"
              value={dueDate}
              onChange={(e) => setDueDate(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 bg-gray-700 text-foreground rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              disabled={isSubmitting}
            />
          </div>

          <div className="mb-6">
            <label className="flex items-center">
              <input
                type="checkbox"
                checked={reminder}
                onChange={(e) => setReminder(e.target.checked)}
                className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                disabled={isSubmitting}
              />
              <span className="ml-2 text-foreground text-sm">Set Reminder</span>
            </label>
          </div>

          {message.text && (
            <div className={`mb-4 p-2 rounded text-sm text-center ${
              message.isError ? "bg-red-600 text-white" : "bg-green-600 text-white"
            }`}>
              {message.text}
            </div>
          )}

          <div className="flex justify-end space-x-3">
            <button
              type="button"
              onClick={() => {
                if (!isSubmitting) {
                  onClose();
                  resetForm();
                }
              }}
              className="px-4 py-2 text-gray-300 hover:text-white font-medium disabled:opacity-50"
              disabled={isSubmitting}
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 font-medium disabled:opacity-50 disabled:cursor-not-allowed"
              disabled={isSubmitting}
            >
              {isSubmitting ? "Saving..." : (isEditing ? "Update" : "Create")}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};