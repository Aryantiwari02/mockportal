import { BrowserRouter, Routes, Route } from "react-router-dom";

import MainLayout from "./layouts/MainLayout";
import { LanguageProvider } from "./i18n";

import Home from "./pages/Home";
import Schemes from "./pages/Schemes";
import Documents from "./pages/Documents";
import Services from "./pages/Services";
import Search from "./pages/Search";
import Help from "./pages/Help";
import SchemeDetails from "./pages/SchemeDetails";
import CitizenServices from "./pages/CitizenServices";
import DocumentDetails from "./pages/DocumentDetails";
import MockDocument from "./pages/MockDocument";
import SchemeFinder from "./pages/SchemeFinder";
import DocumentChecklist from "./pages/DocumentChecklist";

import Accessibility from "./pages/Accessibility";
import Contact from "./pages/Contact";
import Privacy from "./pages/Privacy";
import Disclaimer from "./pages/Disclaimer";

import CitizenAccess from "./pages/CitizenAccess";
import MyServices from "./pages/MyServices";
import ApplyScheme from "./pages/ApplyScheme";
import ApplicationDetails from "./pages/ApplicationDetails";

import "./styles/global.css";


function App() {
  return (
    <BrowserRouter>
      <LanguageProvider>
        <MainLayout>

          <Routes>

            {/* Home */}
            <Route
              path="/"
              element={<Home />}
            />

            {/* Schemes */}
            <Route
              path="/schemes"
              element={<Schemes />}
            />

            <Route
              path="/schemes/:id"
              element={<SchemeDetails />}
            />

            {/* Apply Scheme Workflow */}
            <Route
              path="/apply/:schemeId"
              element={<ApplyScheme />}
            />

            {/* Documents */}
            <Route
              path="/documents"
              element={<Documents />}
            />

            <Route
              path="/documents/mock/:type"
              element={<MockDocument />}
            />

            <Route
              path="/documents/:id"
              element={<DocumentDetails />}
            />

            {/* Services */}
            <Route
              path="/services"
              element={<Services />}
            />

            <Route
              path="/citizen-services"
              element={<CitizenServices />}
            />

            <Route
              path="/citizen-services/scheme-finder"
              element={<SchemeFinder />}
            />

            <Route
              path="/citizen-services/documents"
              element={<DocumentChecklist />}
            />

            {/* Search */}
            <Route
              path="/search"
              element={<Search />}
            />

            {/* Help */}
            <Route
              path="/help"
              element={<Help />}
            />

            {/* Accessibility */}
            <Route
              path="/accessibility"
              element={<Accessibility />}
            />

            {/* Contact */}
            <Route
              path="/contact"
              element={<Contact />}
            />

            {/* Privacy */}
            <Route
              path="/privacy"
              element={<Privacy />}
            />

            {/* Disclaimer */}
            <Route
              path="/disclaimer"
              element={<Disclaimer />}
            />

            {/* Citizen OTP Access */}
            <Route
              path="/citizen-access"
              element={<CitizenAccess />}
            />

            {/* Authenticated Citizen Area & Applications */}
            <Route
              path="/my-services"
              element={<MyServices />}
            />

            <Route
              path="/my-applications"
              element={<MyServices />}
            />

            <Route
              path="/my-applications/:applicationNumber"
              element={<ApplicationDetails />}
            />

          </Routes>

        </MainLayout>
      </LanguageProvider>
    </BrowserRouter>
  );
}

export default App;