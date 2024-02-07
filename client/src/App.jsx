import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { ToastContainer } from "react-toastify";
import Header from "./components/Header";
import LandingPage from "./pages/LandingPage";
import Property from "./pages/Property";
import Footer from "./components/Footer";

const App = () => {
  return (
    <>
      <Router>
        <Header />
        <Routes>
          {/* <main className="py-3"> */}
            <Route path="/" element={<LandingPage />} />
            <Route path="/properties" element={<Property />} />
          {/* </main> */}
        </Routes>
        <ToastContainer theme="dark" />
        <Footer />
      </Router>
    </>
  );
};

export default App;
