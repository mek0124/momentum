import { useEffect, useState } from "react";



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
    
  );
};
