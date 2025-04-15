import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import StudentDashboard from './pages/StudentDashboard';
import TeacherDashboard from './pages/TeacherDashboard';
// import AdminDashboard from './pages/AdminDashboard';

const ProtectedRoute = ({ element, role: requiredRole }) => {
  const userRole = localStorage.getItem("role");
  return userRole === requiredRole ? element : <Navigate to="/login" />;
};


function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/student" element={<ProtectedRoute role="student" element={<StudentDashboard />} />} />
        <Route path="/teacher" element={<ProtectedRoute role="teacher" element={<TeacherDashboard />} />} />

        {/* <Route path="/admin" element={<AdminDashboard />} /> */}
      </Routes>
    </Router>
  );
}

export default App;
