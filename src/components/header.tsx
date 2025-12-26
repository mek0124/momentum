import { useEffect, useState } from "react";

import AppIcon from '../assets/icon.png';


export default function Header() {
  const [cTime, setCTime] = useState('');
  const [cDate, setCDate] = useState('');
  
  const userLocation = window.navigator.language || 'en-US';

  useEffect(() => {
    const updateClock = async () => {
      const now = new Date();

      const timeOptions: Intl.DateTimeFormatOptions = {
        hour12: false,
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
      };
      
      const dateOptions: Intl.DateTimeFormatOptions = {
        year: 'numeric',
        day: 'numeric',
        month: 'numeric'
      };

      const time = now.toLocaleTimeString(userLocation, timeOptions);
      const date = now.toLocaleDateString(userLocation, dateOptions);

      setCTime(time);
      setCDate(date);
    };

    updateClock();

    const intervalId = setInterval(updateClock, 1000);
    return () => clearInterval(intervalId);
  }, [userLocation]);

  return (
    <div className="flex flex-row items-center justify-center w-full border-b-2 border-b-gray-500">
      <div className="flex flex-row items-center justify-start w-full">
        <img
          src={AppIcon}
          alt="Momentum App Icon"
          width="40"
          height="40"
          className="rounded-full m-1"
        />

        <h1 className="font-bold italic text-sm">
          Momentum
        </h1>
      </div>

      <div className="flex flex-col items-end justify-center mr-3">
        <span className="italic text-sm">
          {cTime}
        </span>

        <span className="italic text-sm">
          {cDate}
        </span>
      </div>
    </div>
  );
};
