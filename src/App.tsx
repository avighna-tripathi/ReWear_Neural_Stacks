import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import Landing from "./pages/Landing";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Dashboard from "./pages/Dashboard";
import Browse from "./pages/Browse";
import ItemDetail from "./pages/ItemDetail";
import AddItem from "./pages/AddItem";
import Admin from "./pages/Admin";
import NotFound from "./pages/NotFound";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Define all routes here */}
        <Route path="/" element={<Layout><Landing /></Layout>} />
        <Route path="/login" element={<Layout><Login /></Layout>} />
        <Route path="/signup" element={<Layout><Signup /></Layout>} />
        <Route path="/dashboard" element={<Layout><Dashboard /></Layout>} />
        <Route path="/browse" element={<Layout><Browse /></Layout>} />
        <Route path="/item/:id" element={<Layout><ItemDetail /></Layout>} />
        <Route path="/add-item" element={<Layout><AddItem /></Layout>} />
        <Route path="/admin" element={<Layout><Admin /></Layout>} />

        {/* IMPORTANT: DO NOT place any routes below this. */}
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App; 