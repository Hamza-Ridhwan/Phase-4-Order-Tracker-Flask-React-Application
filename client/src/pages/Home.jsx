import React, { useContext } from "react";
import { Link } from "react-router-dom"; // Import Link for navigation
import { AuthContext } from "../context/AuthContext"; // Import the AuthContext

export default function Home() {
  const { user, logout } = useContext(AuthContext); // Access the user data and logout function from AuthContext

  return (
    <div className="text-center mt-10">
      <h1 className="text-3xl font-semibold text-gray-800 mb-4">
        Welcome to Order Tracker
      </h1>
      {user ? (
        <p className="text-xl text-gray-600 mb-6">
          Hello, {user.email}! Manage and track your orders effortlessly.
        </p>
      ) : (
        <p className="text-xl text-gray-600 mb-6">
          Easily track, manage, and update your orders in one place.
        </p>
      )}
      {/* Show either the logout button or the Get Started button */}
      {user ? (
        <button
          onClick={logout} // If the user is logged in, trigger logout
          className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
        >
          Logout
        </button>
      ) : (
        <Link to="/login">
          <button className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 mt-4">
            Get Started
          </button>
        </Link>
      )}
    </div>
  );
}
