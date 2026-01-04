


export default function PopUp({
  handlePopup,
  newTask,
  setNewTask,
  handleCreateOrUpdateTask,
  editingTaskId
}) {
  return (
    <div className="fixed inset-0 flex items-center justify-center z-50 overflow-hidden">
      <div
        className="absolute inset-0 bg-black opacity-90"
        onClick={handlePopup}
      ></div>

      <div className="relative bg-gray-900 rounded-2xl shadow-2xl w-full max-w-md mx-4 p-6 z-10 overflow-hidden">
        <h2 className="text-2xl font-bold text-gray-500 mb-6 text-center">
          {editingTaskId ? "Edit Task" : "Create New Task"}
        </h2>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-500 mb-1">
              Title <span className="text-gray-500 text-xs">(max 75 chars)</span>
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
              value={newTask.details}
              onChange={e =>
                setNewTask({ ...newTask, details: e.target.value })
              }
              className="w-full px-4 py-2 bg-gray-500 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition h-32 resize-none text-black placeholder-black"
              placeholder="Enter task description"
            />

            <div className="text-right text-xs text-gray-500 mt-1">
              {newTask.details.length}/275
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
                    setNewTask({ ...newTask, priority: level })
                  }
                  className={`flex-1 py-2 rounded-lg transition ${
                    newTask.priority === level
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
              onClick={handleCreateOrUpdateTask}
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
  );
};
