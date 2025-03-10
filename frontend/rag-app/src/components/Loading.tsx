import React from "react";

interface LoadingProps {
  loadingText?: string; // custom loading text
}

const Loading: React.FC<LoadingProps> = ({ loadingText = "Loading" }) => {
  return (
    <div className="flex justify-center items-center mt-2 text-gray-500 text-lg">
      <span className="animate-pulse">
        {loadingText} • • •
      </span>
    </div>
  );
};

export default Loading;
