import { createRoot } from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import "./index.css";
import App from "./App";

import { CoursesPage } from "./pages/CoursesPage";
import { ProfilePage } from "./pages/ProfilePage";
import { CourseDetailPage } from "./pages/CourseDetailPage";

import { EnrollmentProvider } from './context/EnrollmentContext';

createRoot(document.getElementById("root")).render(
  <EnrollmentProvider>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/courses" element={<CoursesPage />} />
        <Route path="/profile" element={<ProfilePage />} />
        <Route path="/courses/:courseId" element={<CourseDetailPage />} />
      </Routes>
    </BrowserRouter>
  </EnrollmentProvider>
);  
