import { useEffect, useState } from "react";

import AppIcon from '../assets/icon.png';


export default function Header() {
  const [cTime, setCTime] = useState('');
  const [cDate, setCDate] = useState('');

  useEffect(() => {
    const updateClock = () => {
      const now = new Date();
      const userLange = navigator.language || 'en-US';

      const timeOptions: Intl.DateTimeFormatOptions = {
        hour12: false,
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
      };

      const dateOptions: Intl.DateTimeFormatOptions = {
        year: 'numeric',
        day: 'numeric',
        month: 'long',
        weekday: 'long'
      };

      const time = now.toLocaleTimeString(userLange, timeOptions);
      const date = now.toLocaleDateString(userLange, dateOptions);

      setCTime(time);
      setCDate(date);
    };

    updateClock();

    const intervalId = setInterval(updateClock, 1000);
    return () => clearInterval(intervalId);
  }, []);

  return (
    <div className="flex flex-row items-center justify-center w-full border-b-2 border-b-primary">
      <img
        src={AppIcon}
        alt="Momentum App Icon"
        width="80"
        height="80"
        className="m-1 rounded-2xl"
      />

      <h1 className="font-bold italic text-2xl text-center w-full text-text_primary">
        Momentum
      </h1>

      <div className="flex flex-col items-center justify-center w-[20%] gap-3 mr-3">
        <span className="italic text-xs text-text_primary w-full text-end">
          {cTime}
        </span>

        <span className="italic text-xs text-text_primary w-full text-end">
          {cDate}
        </span>
      </div>
    </div>
  );
};
