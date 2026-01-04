


export default function NoTasks({ handlePopup }) {
  return (
    <div className="flex flex-col items-center justify-center w-full flex-grow mt-10">
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
  );
};
