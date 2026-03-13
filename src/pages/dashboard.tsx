import { useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPencil, faTrashCan, faSave, faRefresh } from "@fortawesome/free-solid-svg-icons";


export default function Dashboard() {
  const [taskItemData, setTaskItemData] = useState({
    title: '',
    content: '',
    priority: '',
    dueTime: '',
    dueDate: ''
  });

  const [allTasks, setAllTasks] = useState([]);

  const handleChange = (e) => {
    const { name, value } = e.target;

    setTaskItemData({
      ...taskItemData,
      [name]: value,
    });
  };

  const clearForm = () => {};

  const handleSubmit = async(e) => {
    e.preventDefault();

    // instantiate db
    // validate title and content are not empty, error if so
    // save data to indexDB
    // update list state
    // refresh ui
  };

  const displayCurrentTasks = () => {
    return allTasks.map((task) => {
      return (
        <div className="">
          {/* left side - 2/3's width */}
          <div className=""></div>

          {/* task buttons - 1/3's width */}
          <div className="">
            <button>
              <FontAwesomeIcon icon={faPencil} />
            </button>

            <button>
              <FontAwesomeIcon icon={faTrashCan} />
            </button>
          </div>
        </div>
      );
    });
  };

  return (
    <div className="flex xl:flex-row lg:flex-col items-center justify-center lg:justify-evenly w-full flex-grow">
      <div className="flex flex-col items-center justify-center xl:w-[800px] lg:w-[80%] xl:h-[750px] lg:h-[550px] border-2 border-2-accent rounded-2xl overflow-y-auto">
        {allTasks.length === 0 && (
          <div className="flex flex-col items-center justify-center w-full flex-grow">
            <span className="font-bold italic text-xl text-center w-full text-primary">
              No Tasks Currectly Exists...
            </span>
          </div>
        )}

        {allTasks.length >= 1 && (
          <div className="flex flex-col items-center justify-center w-full flex-grow overflow-y-auto">
            { displayCurrentTasks() }
          </div>
        )}
      </div>

      <form
        onSubmit={handleSubmit} 
        className="flex flex-col items-center justify-evenly xl:w-[800px] lg:w-[80%] xl:h-[750px] lg:h-[550px] border-2 border-2-accent rounded-2xl"
      >
        <div className="flex flex-row items-center justify-center xl:w-4/5 lg:w-1/3">
          <label
            htmlFor="title"
            className="italic text-lg text-text_primary xl:w-1/5 lg:w-full xl:text-start md:text-center lg:text-start"
          >
            Title
          </label>

          <input
            type="text"
            id="title"
            name="title"
            value={taskItemData.title}
            onChange={handleChange}
            className="border-2 border-accent rounded-xl outline-none bg-secondary hover:bg-accent_hover hover:outline-none focus:outline-none focus:bg-teritary text-text_secondary text-center text-lg xl:w-96"
          />
        </div>

        <div className="flex xl:flex-row lg:flex-col items-center justify-center xl:w-[515px] lg:w-1/3 lg:gap-1">
          <label 
            htmlFor="priority"
            className="italic text-lg text-text_primary xl:w-1/3 lg:w-full xl:text-start xl:ml-1 lg:text-center"
          >
            Priority
          </label>

          <div className="flex flex-row items-center justify-evenly w-full">
            <div className="flex flex-row items-center justify-center w-full xl:m-1 m-2 xl:gap-0 lg:gap-1">
              <input 
                type="radio" 
                id="radio_low" 
                name="radio_low" 
                value="3"
                onChange={handleChange}
                checked={true}
                className="border-2 border-success rounded-xl outline-none bg-secondary hover:bg-success hover:outline-none focus:outline-none focus:bg-success" 
              />
              
              <label 
                htmlFor="radio_low"
                className="italic text-md text-success ml-2"
              >
                Low
              </label>
            </div>

            <div className="flex flex-row items-center justify-center w-full xl:m-1 m-2 xl:gap-0 lg:gap-1">
              <input 
                type="radio" 
                id="radio_low" 
                name="radio_low" 
                value="2"
                onChange={handleChange}
                className="border-2 border-warning rounded-xl outline-none bg-secondary hover:bg-accent_hover hover:outline-none focus:outline-none focus:bg-warning" 
              />
              
              <label 
                htmlFor="radio_low"
                className="italic text-md text-warning ml-2"
              >
                Medium
              </label>
            </div>

            <div className="flex flex-row items-center justify-center w-full xl:m-1 m-2 xl:gap-0 lg:gap-1">
              <input 
                type="radio" 
                id="radio_low" 
                name="radio_low" 
                value="1"
                onChange={handleChange}
                className="border-2 border-error rounded-xl outline-none bg-secondary hover:bg-error hover:outline-none focus:outline-none focus:bg-err" 
              />
              
              <label 
                htmlFor="radio_low"
                className="italic text-md text-error ml-2"
              >
                High
              </label>
            </div>
          </div>
        </div>

        <div className="flex xl:flex-row lg:flex-col items-center justify-center xl:w-4/5 lg:w-1/3">
          <div className="flex flex-col items-center justify-center w-full lg:gap-1">
            <label 
              htmlFor="dueTime"
              className="italic text-lg text-text_primary w-full text-center"
            >
              Due Time
            </label>
            
            <input 
              type="time" 
              id="dueTime" 
              name="dueTime" 
              onChange={handleChange}
              value={taskItemData.dueTime} 
              className="border-2 border-accent rounded-xl outline-none bg-secondary hover:bg-accent_hover hover:outline-none focus:outline-none focus:bg-teritary text-text_secondary text-center text-lg py-1 w-4/5"
            />
          </div>

          <div className="flex flex-col items-center justify-center w-full lg:gap-1">
            <label 
              htmlFor="dueDate"
              className="italic text-lg text-text_primary w-full text-center"
            >
              Due Date
            </label>
            
            <input 
              type="date" 
              id="dueDate" 
              name="dueDate" 
              value={taskItemData.dueDate}
              onChange={handleChange}
              className="border-2 border-accent rounded-xl outline-none bg-secondary hover:bg-accent_hover hover:outline-none focus:outline-none focus:bg-teritary text-text_secondary text-center text-lg py-1 w-4/5"
            />
          </div>
        </div>

        <div className="flex flex-col items-center justify-center w-[80%] lg:gap-1">
          <label 
            htmlFor="content"
            className="italic text-lg text-text_primary w-full text-center"
          >
            Content
          </label>

          <textarea 
            id="content" 
            name="content" 
            value={taskItemData.content} 
            onChange={handleChange}
            className="border-2 border-accent rounded-xl outline-none bg-secondary hover:bg-accent_hover hover:outline-none focus:outline-none focus:bg-teritary text-text_secondary text-center text-lg w-[60%] h-[150px]"
          />
        </div>

        <div className="flex flex-row items-center justify-evenly xl:w-4/5 lg:w-1/3">
          <button
            type="button"
            onClick={clearForm}
            className="border-2 border-primary rounded-2xl outline-none text-error hover:outline-none hover:bg-accent_hover w-1/3 py-2"
          >
            <FontAwesomeIcon icon={faRefresh} />
          </button>

          <button
            type="submit"
            className="border-2 border-primary rounded-2xl outline-none text-success hover:outline-none hover:bg-accent_hover w-1/3 py-2"
          >
            <FontAwesomeIcon icon={faSave} />
          </button>
        </div>
      </form>
    </div>
  );
};
