import React from "react";

const MainBackground = () => {
  return (
    <div className="absolute inset-0 pointer-events-none overflow-hidden select-none">
      <div className="absolute top-[-100px] left-[-100px] w-[350px] h-[350px] bg-red-200/25 blur-[100px] rounded-full" />
      <div className="absolute bottom-[-100px] right-[-100px] w-[350px] h-[350px] bg-gray-300/35 blur-[100px] rounded-full" />
      <div className="absolute top-[-60px] right-[30%] w-[250px] h-[250px] bg-amber-200/20 blur-[90px] rounded-full" />
      <div className="absolute top-20 left-8 text-black/5 text-7xl rotate-12">♠</div>
      <div className="absolute bottom-20 right-8 text-red-300/20 text-7xl -rotate-12">♥</div>
      <div className="absolute top-1/2 right-16 text-red-300/10 text-6xl rotate-6">♦</div>
      <div className="absolute top-1/3 left-16 text-black/5 text-6xl -rotate-6">♣</div>
    </div>
  );
};

export default MainBackground;
