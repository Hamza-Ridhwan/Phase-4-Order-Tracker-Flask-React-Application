import React from "react";
import Navbar from "./Navbar";
import Footer from "./Footer";
import { Outlet } from "react-router-dom";

export default function Layout() {
  return (
    <div>
      <Navbar />
      <div className="min-h-[92vh] bg-gray-200 container mx-auto p-8">
        <Outlet />
      </div>
      <Footer />
    </div>
  );
}
