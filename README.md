<label id="top"></label>

<div align="center">
  <img 
    src="./public/icon.png" 
    alt="Momentum App Icon"
    width="60" 
    height="60" 
  />

  <h1>Momentum</h1>
  <h5>
    A light-weight task management application
  </h5>
</div>

Table of Contents:
- [Introduction](#introduction)
- [How To Install](#how-to-install)
- [How To Use](#how-to-use)
- [Contributing](#contributing)
- [Issues](#issues)

---

## Introduction

Welcome to Momentum, a light-weight Tauri + ReactJS application that assist you in managing your tasks more efficiently

---

## How To Install

1. Clone the Repository
  - `git clone https://github.com/mek0124/momentum`

2. CD into the project and install the dependencies
  - `cd momentum`
  - `pnpm install`

3. Run the application and enjoy!
  - `pnpm tauri dev` for the desktop version in development mode
  - or
  - `pnpm run preview` for the web version in development mode

---

## How To Use

This application is very simple to use. When the application loads and there are no currently stored tasks, the application displays a welcome message. Click the button to create a new task.

When creating a new task, the application requests:
  - Title (required)
  - Details (required)
  - Due Date (optional)
  - Due Time (optional)
  - Priority Level (default 2 for medium)

Upon saving the entry
  - the application checks for duplicate titles and displays an error message if a duplicate is found
  - adds the task to the currently existing list of tasks (if any) and saves the list of tasks to local storage within the application. 

  > NOTE: No permissions and nothing extra is needed from the user as the application coomes pre-setup with local storage ready to go and available.

---

## Contributing

Anyone is welcome to contribute to the application. To contribute

1. Fork the repository
2. Make your changes
3. Push your changes to the forked repository
4. Ensure detailed information as to why you are suggesting your change and how it benefits the application as a whole

---

## Issues

If at any time you come into any issues, please create a new issues on the [issues page](https://github.com/mek0124/momentum/issues)
