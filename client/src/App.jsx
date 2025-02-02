import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";

import Home from "./pages/Home";
import Layout from "./components/Layout";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Orders from "./pages/Orders";
import OrderDetails from "./pages/OrderDetails";
import OrderHistory from "./pages/OrderHistory";
import Profile from "./pages/Profile";
import NotFound from "./pages/NotFound";
import TrackOrder from "./pages/TrackOrder";
import { AuthProvider } from "./context/AuthContext";
function App() {
  return (
    <>
      <BrowserRouter>
        <AuthProvider>
          <Routes>
            <Route path="/" element={<Layout />}>
              <Route index element={<Home />} />
              <Route path="login" element={<Login />} />
              <Route path="signup" element={<Signup />} />
              <Route path="orders" element={<Orders />} />
              <Route path="orderdetails" element={<OrderDetails />} />
              <Route path="sorder-history" element={<OrderHistory />} />
              <Route path="profile" element={<Profile />} />
              <Route path="trackorder" element={<TrackOrder />} />

              <Route path="*" element={<NotFound />} />
            </Route>
          </Routes>
        </AuthProvider>
      </BrowserRouter>
    </>
  );
}

export default App;
