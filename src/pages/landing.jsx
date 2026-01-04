import { useState, useEffect } from "react";
import toast, { Toaster } from "react-hot-toast";
import { taskService } from '../lib/taskService';

import PopUp from "../components/popUp";
import CurrentTasks from "../components/currTask";
import NoTasks from "../components/noTasks";


export default function Landing() {
  const [currentTasks, setCurrentTasks] = useState([]);
  const [popupOpen, setPopupOpen] = useState(false);
  const [editingTaskId, setEditingTaskId] = useState(null);
  const [newTask, setNewTask] = useState({
    title: "",
    details: "",
    dueDate: "",
    dueTime: "",
    priority: 2,
    completed: false
  });

  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const tasks = await taskService.getAllTasks();
        setCurrentTasks(tasks);
      } catch (error) {
        console.error("Failed to fetch tasks:", error);
      };
    };

    fetchTasks();
  }, []);

  const handlePopup = () => {
    if (popupOpen) {
      setEditingTaskId(null);
      setNewTask({
        title: "",
        details: "",
        dueDate: "",
        dueTime: "",
        priority: 2,
        completed: false
      });
    }
    setPopupOpen(!popupOpen);
  };

  const handleEditTask = (task) => {
    setEditingTaskId(task.id);
    setNewTask({
      title: task.title,
      details: task.details,
      dueDate: task.dueDate || "",
      dueTime: task.dueTime || "",
      priority: task.priority,
      completed: task.completed
    });
    setPopupOpen(true);
  };

  const handleDeleteTask = async (id) => {
    try {
      await taskService.deleteTask(id);
      setCurrentTasks(currentTasks.filter(task => task.id !== id));
      toast.success("Task deleted.", {
        style: { background: "#16a34a", color: "#000000" }
      });
    } catch (error) {
      toast.error("Failed to delete task.", {
        style: { background: "#dc2626", color: "#000000" }
      });
    }
  };

  const handleCreateOrUpdateTask = async () => {
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

    try {
      if (editingTaskId) {
        await taskService.updateTask(editingTaskId, {
          title: newTask.title,
          details: newTask.details,
          dueDate: newTask.dueDate,
          dueTime: newTask.dueTime,
          priority: newTask.priority,
          completed: newTask.completed
        });

        setCurrentTasks(currentTasks.map(task =>
          task.id === editingTaskId
            ? { ...task, ...newTask, id: editingTaskId }
            : task
        ));

        toast.success("Task updated successfully.", {
          style: { background: "#16a34a", color: "#000000" }
        });
      } else {
        const newTaskData = {
          id: await taskService.saveTask({
            ...newTask,
            id: ""
          }),
          ...newTask
        };

        setCurrentTasks([...currentTasks, newTaskData]);

        toast.success("Task created successfully.", {
          style: { background: "#16a34a", color: "#000000" }
        });
      }

      setEditingTaskId(null);
      setNewTask({
        title: "",
        details: "",
        dueDate: "",
        dueTime: "",
        priority: 2,
        completed: false
      });
      setPopupOpen(false);
    } catch (error) {
      toast.error("Failed to save task.", {
        style: { background: "#dc2626", color: "#000000" }
      });
    }
  };

  return (
    <div className="flex flex-col items-center justify-center w-full min-h-screen">
      <Toaster position="top-center" />

      {
        popupOpen && 
        <PopUp 
          handlePopup={handlePopup}
          newTask={newTask}
          setNewTask={setNewTask}
          handleCreateOrUpdateTask={handleCreateOrUpdateTask}
          editingTaskId={editingTaskId}
        />
      }

      {
        currentTasks.length > 0 && 
        <CurrentTasks
          handleEditTask={handleEditTask}
          handleDeleteTask={handleDeleteTask}
          handlePopup={handlePopup}
          currentTasks={currentTasks}
        />
      }

      {
        currentTasks.length === 0 && 
        <NoTasks
          handlePopup={handlePopup}
        />
      }
    </div>
  );
}