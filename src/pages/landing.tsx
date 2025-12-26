import { useState, useEffect } from "react";
import toast, { Toaster } from "react-hot-toast";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPencil, faTrashCan } from "@fortawesome/free-solid-svg-icons";

type TaskType = {
  id: number;
  title: string;
  description: string;
  dueDate: string;
  dueTime: string;
  priority: number;
  updatedAt: string;
};

export default function Landing() {
  const [currentTasks, setCurrentTasks] = useState<TaskType[]>([]);
  const [popupOpen, setPopupOpen] = useState(false);
  const [editingTaskId, setEditingTaskId] = useState<number | null>(null);
  const [newTask, setNewTask] = useState({
    title: "",
    content: "",
    dueDate: "",
    dueTime: "",
    priorityLevel: 2
  });

  useEffect(() => {
    try {
      const storedTasks = localStorage.getItem("tasks");
      const parsedTasks = storedTasks ? JSON.parse(storedTasks) : [];
      setCurrentTasks(parsedTasks);
    } catch {
      setCurrentTasks([]);
    }
  }, []);

  const handlePopup = () => {
    if (popupOpen) {
      setEditingTaskId(null);
      setNewTask({
        title: "",
        content: "",
        dueDate: "",
        dueTime: "",
        priorityLevel: 2
      });
    }
    setPopupOpen(!popupOpen);
  };

  const handleEditTask = (task: TaskType) => {
    setEditingTaskId(task.id);
    setNewTask({
      title: task.title,
      content: task.description,
      dueDate: task.dueDate,
      dueTime: task.dueTime,
      priorityLevel: task.priority
    });
    setPopupOpen(true);
  };

  const handleDeleteTask = (id: number) => {
    const updatedTasks = currentTasks.filter(task => task.id !== id);
    setCurrentTasks(updatedTasks);
    localStorage.setItem("tasks", JSON.stringify(updatedTasks));
    toast.success("Task deleted.", {
      style: { background: "#16a34a", color: "#000000" }
    });
  };

  const handleCreateTask = () => {
    const duplicateExists = currentTasks.some(
      task =>
        task.title.toLowerCase().trim() ===
          newTask.title.toLowerCase().trim() &&
        task.id !== editingTaskId
    );

    if (duplicateExists) {
      toast.error("A task with this title already exists.", {
        style: { background: "#dc2626", color: "#000000" }
      });
      return;
    }

    let updatedTasks: TaskType[];

    if (editingTaskId) {
      updatedTasks = currentTasks.map(task =>
        task.id === editingTaskId
          ? {
              ...task,
              title: newTask.title,
              description: newTask.content,
              dueDate: newTask.dueDate,
              dueTime: newTask.dueTime,
              priority: newTask.priorityLevel,
              updatedAt: new Date().toISOString()
            }
          : task
      );

      toast.success("Task updated successfully.", {
        style: { background: "#16a34a", color: "#000000" }
      });
    } else {
      const task: TaskType = {
        id: Date.now(),
        title: newTask.title,
        description: newTask.content,
        dueDate: newTask.dueDate,
        dueTime: newTask.dueTime,
        priority: newTask.priorityLevel,
        updatedAt: new Date().toISOString()
      };

      updatedTasks = [...currentTasks, task];

      toast.success("Task created successfully.", {
        style: { background: "#16a34a", color: "#000000" }
      });
    }

    setCurrentTasks(updatedTasks);
    localStorage.setItem("tasks", JSON.stringify(updatedTasks));

    setEditingTaskId(null);
    setNewTask({
      title: "",
      content: "",
      dueDate: "",
      dueTime: "",
      priorityLevel: 2
    });
    setPopupOpen(false);
  };

  return (
    <div className="flex flex-col items-center justify-center w-full min-h-screen">
      <Toaster position="top-center" />

      {popupOpen && (
        <div className="fixed inset-0 flex items-center justify-center z-50">
          <div
            className="absolute inset-0 bg-black opacity-90"
            onClick={handlePopup}
          ></div>

          <div className="relative bg-gray-900 rounded-2xl shadow-2xl w-full max-w-md mx-4 p-6 z-10">
            <h2 className="text-2xl font-bold text-gray-500 mb-6 text-center">
              {editingTaskId ? "Edit Task" : "Create New Task"}
            </h2>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-500 mb-1">
                  Title <span className="text-gra-500 text-xs">(max 75 chars)</span>
                </label>

                <input
                  type="text"
                  maxLength={75}
                  value={newTask.title}
                  onChange={e =>
                    setNewTask({ ...newTask, title: e.target.value })
                  }
                  className="w-full px-4 py-2 bg-gray-500 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition text-black placeholder-black"
                  placeholder="Enter task title"
                />

                <div className="text-right text-xs text-gray-500 mt-1">
                  {newTask.title.length}/75
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-500 mb-1">
                  Content <span className="text-gray-500 text-xs">(max 275 chars)</span>
                </label>

                <textarea
                  maxLength={275}
                  value={newTask.content}
                  onChange={e =>
                    setNewTask({ ...newTask, content: e.target.value })
                  }
                  className="w-full px-4 py-2 bg-gray-500 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition h-32 resize-none text-black placeholder-black"
                  placeholder="Enter task description"
                />

                <div className="text-right text-xs text-gray-500 mt-1">
                  {newTask.content.length}/275
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-500 mb-1">
                    Due Date
                  </label>

                  <input
                    type="date"
                    value={newTask.dueDate}
                    onChange={e =>
                      setNewTask({ ...newTask, dueDate: e.target.value })
                    }
                    className="w-full px-4 py-2 bg-gray-500 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition text-black"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-500 mb-1">
                    Due Time
                  </label>

                  <input
                    type="time"
                    value={newTask.dueTime}
                    onChange={e =>
                      setNewTask({ ...newTask, dueTime: e.target.value })
                    }
                    className="w-full px-4 py-2 bg-gray-500 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition text-black"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-500 mb-1">
                  Priority Level
                </label>

                <div className="flex space-x-4">
                  {[1, 2, 3].map(level => (
                    <button
                      key={level}
                      type="button"
                      onClick={() =>
                        setNewTask({ ...newTask, priorityLevel: level })
                      }
                      className={`flex-1 py-2 rounded-lg transition ${
                        newTask.priorityLevel === level
                          ? level === 1
                            ? "bg-red-600 text-black"
                            : level === 2
                            ? "bg-yellow-600 text-black"
                            : "bg-green-600 text-black"
                          : "bg-gray-100 text-black hover:bg-gray-200"
                      }`}
                    >
                      Level {level}
                      <span className="block text-xs opacity-90">
                        {level === 1 ? "Highest" : level === 2 ? "Medium" : "Low"}
                      </span>
                    </button>
                  ))}
                </div>
              </div>

              <div className="flex space-x-3 pt-4">
                <button
                  type="button"
                  onClick={handlePopup}
                  className="flex-1 px-4 py-2 border border-gray-300 text-gray-500 rounded-lg hover:bg-gray-50 hover:text-black transition"
                >
                  Cancel
                </button>
                <button
                  type="button"
                  onClick={handleCreateTask}
                  disabled={!newTask.title.trim()}
                  className={`flex-1 px-4 py-2 rounded-lg transition ${
                    !newTask.title.trim()
                      ? "bg-gray-300 text-gray-500 cursor-not-allowed"
                      : "bg-blue-500 text-black hover:bg-blue-600 hover:text-black"
                  }`}
                >
                  {editingTaskId ? "Save Changes" : "Create Task"}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {currentTasks.length === 0 && (
        <div className="flex flex-col items-center justify-center w-full flex-grow">
          <div className="text-center">
            <h1 className="text-4xl md:text-5xl font-bold mb-2 text-gray-500">
              Welcome to Momentum
            </h1>

            <p className="text-lg text-gray-500">
              Your private sanctuary for productivity, living right here in your browser.
            </p>

            <div className="p-6 w-4/5 mx-auto space-y-4 text-left">
              <p className="text-gray-500 leading-relaxed">
                Imagine a personal task manager that <span className="font-semibold text-blue-600">never leaves your computer</span> - no accounts to create, no data in the cloud, just your tasks, stored securely on your own device.
              </p>

              <p className="text-gray-500 leading-relaxed">
                Momentum is a <span className="font-semibold text-green-600">free, open-source companion</span> that helps you capture your goals and track your progress with effortless simplicity. Everything stays local, private, and completely under your control.
              </p>

              <p className="text-gray-500 leading-relaxed">
                It's like having a thoughtful digital notebook that remembers everything for you, working quietly in the background to keep your days flowing smoothly.
              </p>

              <p className="text-gray-500 leading-relaxed text-center">
                ✨ Begin Your Journey
              </p>
            </div>
          </div>

          <button
            type="button"
            onClick={handlePopup}
            className="px-6 py-2 bg-gradient-to-r from-blue-500 to-blue-600 text-white font-semibold rounded-xl shadow-lg hover:shadow-xl hover:from-blue-600 hover:to-blue-700 transition-all duration-300 text-lg transform hover:-translate-y-0.5"
          >
            Create First Task
          </button>
        </div>
      )}

      {currentTasks.length > 0 && (
        <div className="flex flex-col items-center justify-center w-full max-w-4xl">
          <div className="flex flex-col justify-between items-center mb-8">
            <button
              onClick={handlePopup}
              className="px-6 py-3 bg-blue-500 text-white font-medium rounded-lg hover:bg-blue-600 transition-colors"
            >
              + New Task
            </button>
          </div>

          <div className="flex flex-col items-center justify-center w-full">
            <h2 className="text-2xl font-bold text-gray-500 mb-6">Your Tasks</h2>

            <div className="flex flex-row flex-wrap items-center justify-center gap-6 w-full max-w-full px-4">
              {currentTasks.map(task => (
                <div
                  key={task.id}
                  className="flex flex-col items-center w-full sm:w-1/2 lg:w-1/3 h-64 max-h-64 justify-center gap-4 bg-gray-400 rounded-xl p-6 hover:shadow-lg transition-shadow border border-gray-100"
                >
                  <h3 className="font-semibold text-lg text-black border-b-black border-b-2 w-full text-center">
                    {task.title || "Untitled Task"}
                  </h3>

                  {task.description && (
                    <p className="text-black text-sm border-l-2 border-r-2 border-b-2 border-dotted w-full border-black text-center h-20">
                      {task.description}
                    </p>
                  )}

                  {task.dueDate && (
                    <div className="text-xs text-black">
                      Due Date: {task.dueDate}
                    </div>
                  )}

                  {task.dueTime && (
                    <div className="text-xs text-black">
                      Due Time: {task.dueTime}
                    </div>
                  )}

                  <div className="text-xs text-black">
                    Priority:{" "}
                    {task.priority === 1
                      ? "high"
                      : task.priority === 2
                      ? "medium"
                      : "low"}
                  </div>

                  <div className="text-xs text-black">
                    Last updated:{" "}
                    {new Date(task.updatedAt).toLocaleDateString()}
                  </div>

                  <div className="flex gap-4">
                    <button
                      onClick={() => handleEditTask(task)}
                      className="text-black hover:opacity-70 transition"
                    >
                      <FontAwesomeIcon icon={faPencil} />
                    </button>

                    <button
                      onClick={() => handleDeleteTask(task.id)}
                      className="text-black hover:opacity-70 transition"
                    >
                      <FontAwesomeIcon icon={faTrashCan} />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      <div className="text-center text-gray-500 text-sm">
        <p>Your data is stored locally in your browser - private, secure, and always accessible.</p>
      </div>
    </div>
  );
}