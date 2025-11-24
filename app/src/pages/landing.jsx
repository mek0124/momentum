import { useState, useEffect } from "react";
import { TaskModal } from "../components/taskModal";

export default function Landing() {
  const [currentTasks, setCurrentTasks] = useState([]); // Changed from null to []
  const [showModal, setShowModal] = useState(false);
  const [editingTaskId, setEditingTaskId] = useState(null); // Added for edit functionality

  async function fetchTasks() {
    try {
      const storedTasks = window.localStorage.getItem("tasks");
      const parsedTasks = storedTasks ? JSON.parse(storedTasks) : [];

      setCurrentTasks(parsedTasks);
    } catch (err) {
      console.error(err);
      setCurrentTasks([]);
    }
  }

  useEffect(() => {
    fetchTasks();
  }, []);

  const handlePopupShowHide = (taskId = null) => {
    setEditingTaskId(taskId);
    setShowModal(!showModal);
  };

  const handleCreateTask = async (task) => {
    const existingTasks = JSON.parse(window.localStorage.getItem("tasks") || "[]");
    const updatedTasks = [...existingTasks, task];
    
    window.localStorage.setItem("tasks", JSON.stringify(updatedTasks));
    setCurrentTasks(updatedTasks);
  };

  const handleUpdateTask = async (updatedTask) => {
    const existingTasks = JSON.parse(window.localStorage.getItem("tasks") || "[]");
    const updatedTasks = existingTasks.map(task => 
      task.id === updatedTask.id ? updatedTask : task
    );
    
    window.localStorage.setItem("tasks", JSON.stringify(updatedTasks));
    setCurrentTasks(updatedTasks);
    setEditingTaskId(null);
  };

  const handleDeleteTask = (taskId) => {
    const existingTasks = JSON.parse(window.localStorage.getItem("tasks") || "[]");
    const updatedTasks = existingTasks.filter(task => task.id !== taskId);
    
    window.localStorage.setItem("tasks", JSON.stringify(updatedTasks));
    setCurrentTasks(updatedTasks);
    fetchTasks();
  };

  const displayTasks = () => {
    if (!currentTasks || currentTasks.length === 0) {
      return (
        <div className="flex flex-col items-center justify-center w-full flex-grow">
          <h3 className="font-bold italic text-xl text-foreground mb-4">
            No Tasks Found
          </h3>
          <span className="italic text-sm text-foreground text-center w-2/3">
            To get started, click the '+' button to create a new task
          </span>
        </div>
      );
    }

    return currentTasks.map((task) => {
      const dueDate = task.dueDate ? new Date(task.dueDate).toLocaleString() : 'No due date';
      
      return (
        <div
          key={task.id}
          className="border-2 border-accent rounded-xl w-[95%] p-4 bg-accent m-2 cursor-pointer hover:bg-accent-dark transition-colors"
        >
          <div className="flex justify-between items-start">
            <div className="flex-1">
              <h3 className="font-bold text-foreground text-lg">{task.title}</h3>
              {task.content && (
                <p className="text-foreground mt-2 text-sm">{task.content}</p>
              )}
              <p className="text-foreground text-xs mt-2 opacity-75">
                Due: {dueDate}
              </p>
              {task.reminder && (
                <span className="inline-block bg-yellow-500 text-black text-xs px-2 py-1 rounded mt-2">
                  Reminder Set
                </span>
              )}
            </div>
            <div className="flex space-x-2 ml-4">
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  handlePopupShowHide(task.id);
                }}
                className="px-3 py-1 bg-blue-500 text-white text-sm rounded hover:bg-blue-600"
              >
                Edit
              </button>
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  handleDeleteTask(task.id);
                }}
                className="px-3 py-1 bg-red-500 text-white text-sm rounded hover:bg-red-600"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      );
    });
  };

  return (
    <div className="flex flex-col items-center justify-start w-full flex-grow">
      <TaskModal
        isVisible={showModal}
        onClose={() => {
          setShowModal(false);
          setEditingTaskId(null);
        }}
        onCreate={handleCreateTask}
        onUpdate={handleUpdateTask}
        taskId={editingTaskId}
      />

      <div className="flex flex-row items-center justify-between w-full p-4">
        <h1 className="font-bold text-2xl text-foreground">My Tasks</h1>
        <button
          type="button"
          onClick={() => handlePopupShowHide()}
          className="font-bold text-2xl text-foreground bg-blue-500 w-10 h-10 rounded-full flex items-center justify-center hover:bg-blue-600 transition-colors"
        >
          +
        </button>
      </div>

      <div className="flex flex-col items-center justify-start w-full flex-grow overflow-y-auto">
        {displayTasks()}
      </div>
    </div>
  );
}