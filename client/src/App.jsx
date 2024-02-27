import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { ToastContainer } from "react-toastify";
import Header from "./components/Header";
import LandingPage from "./pages/LandingPage";
import PropertiesList from "./pages/PropertiesList";
import NotFound from "./components/NotFound";
import Login from "./pages/Login";

const App = () => {
  return (
    <>
      <Router>
        <Header />
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/properties" element={<PropertiesList />} />
          <Route path="/login" element={<Login />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
        <ToastContainer theme="dark" />
      </Router>
    </>
  );
};

export default App;
