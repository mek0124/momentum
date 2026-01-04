import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPencil, faTrashCan } from "@fortawesome/free-solid-svg-icons";


export default function CurrentTasks({
  handleEditTask,
  handleDeleteTask,
  handlePopup,
  currentTasks
}) {
  return (
        <div className="flex flex-col items-center justify-center w-full max-w-4xl flex-grow">
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

            <div className="flex flex-row flex-wrap items-center justify-center gap-6 w-full max-w-full px-4 mb-5">
              {currentTasks.map(task => (
                <div
                  key={task.id}
                  className="flex flex-col items-center w-full sm:w-1/2 lg:w-1/3 h-64 justify-center gap-4 bg-gray-400 rounded-xl p-6 hover:shadow-lg transition-shadow border border-gray-100"
                >
                  <h3 className="font-semibold text-lg text-black border-b-black border-b-2 w-full text-center">
                    {task.title || "Untitled Task"}
                  </h3>

                  {task.details && (
                    <p className="text-black text-sm border-l-2 border-r-2 border-b-2 border-dotted w-full border-black text-center h-[550px] overflow-y-auto p-1">
                      {task.details}
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
                    Priority: {task.priority === 1 ? "High" : task.priority === 2 ? "Medium" : "Low"}
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
      )
};
