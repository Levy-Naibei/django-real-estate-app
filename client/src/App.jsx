import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { ToastContainer } from "react-toastify";
import Header from "./components/Header";
import LandingPage from "./pages/LandingPage";
import PropertiesList from "./pages/PropertiesList";
import Footer from "./components/Footer";
import NotFound from "./components/NotFound";
import Login from "./pages/Login";

const App = () => {
  return (
    <>
      <Router>
        <Header />
        <Routes>
          {/* <main className="py-3"> */}
            <Route path="/" element={<LandingPage />} />
            <Route path="/properties" element={<PropertiesList />} />
          {/* </main> */}
          <Route path="/login" element={<Login />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
        <ToastContainer theme="dark" />
        <Footer />
      </Router>
    </>
  );
};

export default App;
