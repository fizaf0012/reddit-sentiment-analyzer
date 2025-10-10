// src/components/Sidebar.jsx
import React from "react";
import { FaHome, FaChartBar, FaCog, FaSignOutAlt } from "react-icons/fa";

const Sidebar = ({ activeTab, onSelect }) => {
  const menuItems = [
  { label: "Overview", icon: <FaHome /> },
  /*{ label: "Sentiment Analysis", icon: <FaChartBar /> }, // renamed */
];

  return (
    <div className="h-screen w-64 bg-gray-900 text-white flex flex-col justify-between">
      <div>
        <div className="p-6 text-2xl font-bold border-b border-gray-700">
          Reddit Sentiment
        </div>

        <nav className="mt-6">
          <ul>
            {menuItems.map((item) => (
              <li
                key={item.label}
                onClick={() => onSelect(item.label)}
                className={`px-6 py-3 flex items-center gap-3 cursor-pointer hover:bg-gray-700 ${
                  activeTab === item.label ? "bg-gray-700" : ""
                }`}
              >
                {item.icon} {item.label}
              </li>
            ))}
          </ul>
        </nav>
      </div>

      <div
        className="p-6 border-t border-gray-700 hover:bg-gray-700 cursor-pointer flex items-center gap-3"
        onClick={() => {
          localStorage.removeItem("token");
          localStorage.removeItem("role");
          window.location.reload();
        }}
      >
        <FaSignOutAlt /> Logout
      </div>
    </div>
  );
};

export default Sidebar;
