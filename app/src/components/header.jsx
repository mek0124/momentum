import { useState, useEffect } from "react";

import AppIcon from '../assets/original.png';


export default function Header() {
  const [currentTime, setCurrentTime] = useState('');
  const [currentDate, setCurrentDate] = useState('');

  useEffect(() => {
    async function updateClock() {
      const now = new Date();

      const timeOptions = {
        hour12: false,
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
      };

      const dateOptions = {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
      };

      const userLocation = navigator.language || 'en-US';

      const time = now.toLocaleTimeString(userLocation, timeOptions);
      const date = now.toLocaleDateString(userLocation, dateOptions);

      setCurrentTime(time);
      setCurrentDate(date);
    };

    updateClock();

    const intervalId = setInterval(updateClock, 1000);
    return () => clearInterval(intervalId);
  }, []);

  return (
    <div className="flex flex-row items-center justify-center w-full border-b-2 border-b-accent">
      <div className="flex flex-row items-center justify-start w-full">
        <img
          src={AppIcon}
          alt="app icon"
          width="40"
          height="40"
          className="m-1"
        />

        <h1 className="font-bold italic text-md text-start w-full text-foreground">
          Task Manager
        </h1>
      </div>

      <div className="flex flex-col items-center justify-end w-full mr-2">
        <span className="italic text-xs text-end w-full text-foreground">
          {currentTime}
        </span>

        <span className="italic text-xs text-end w-full text-foreground">
          {currentDate}
        </span>
      </div>
    </div>
  );
};
