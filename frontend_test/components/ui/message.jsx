import React from 'react';
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar";

const Message = ({ avatar, name, message, isSender }) => {
  return (
    <div className={`flex items-start mb-4 ${isSender ? 'flex-row-reverse' : ''}`}>
      <Avatar>
        <AvatarImage src={avatar} alt={`${name}'s avatar`} />
        <AvatarFallback>{name.charAt(0)}</AvatarFallback>
      </Avatar>
      <div className={`ml-3 ${isSender ? 'mr-3 text-right' : ''}`}>
        <div className="text-sm font-semibold">{name}</div>
        <div className="bg-gray-800 text-white p-2 rounded-lg">{message}</div>
      </div>
    </div>
  );
};

export default Message;