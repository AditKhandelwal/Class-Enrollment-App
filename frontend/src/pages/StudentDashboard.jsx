import React, { useEffect, useState } from 'react';

export default function StudentDashboard() {
  const [activeTab, setActiveTab] = useState('your');
  const [yourCourses, setYourCourses] = useState([]);
  const [allCourses, setAllCourses] = useState([]);
  const studentId = 1; // eventually replace with dynamic ID

  const fetchStudentClasses = () => {
    fetch(`http://localhost:5000/api/student/${studentId}/classes`)
      .then(res => res.json())
      .then(data => setYourCourses(data));
  };
  
  const fetchAllClasses = () => {
    fetch('http://localhost:5000/api/classes')
      .then(res => res.json())
      .then(data => setAllCourses(data));
  };

  useEffect(() => {
    fetchStudentClasses();
    fetchAllClasses();
  }, []);
  
  const handleJoin = async (classId) => {
    try {
      const res = await fetch('http://localhost:5000/api/student/enroll', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ student_id: studentId, class_id: classId })
      });
  
      const data = await res.json();
  
      if (res.ok) {
        alert('Enrolled!');
        fetchStudentClasses();
        fetchAllClasses();
      } else {
        alert(data.message || 'Failed to enroll.');
      }
    } catch (err) {
      alert('Error enrolling.');
    }
  };

  const handleUnenroll = async (classId) => {
    try {
      const res = await fetch('http://localhost:5000/api/student/unenroll', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ student_id: studentId, class_id: classId })
      });
  
      const data = await res.json();
  
      if (res.ok) {
        alert('Unenrolled.');
        fetchStudentClasses();
        fetchAllClasses();
      } else {
        alert(data.message || 'Failed to unenroll.');
      }
    } catch (err) {
      alert('Error unenrolling.');
    }
  };
  

  const isEnrolled = (classId) => {
    return yourCourses.some(c => c.id === classId);
  };
  

  const renderTable = (courses, showJoin = false) => (
    <table style={styles.table}>
      <thead style={styles.tableHead}>
        <tr>
          <th style={styles.th}>Course Name</th>
          <th style={styles.th}>Teacher</th>
          <th style={styles.th}>Time</th>
          <th style={styles.th}>Students Enrolled</th>
          {showJoin === false && <th style={styles.th}>Grade</th>}
          {showJoin && <th style={styles.th}>Action</th>}
        </tr>
      </thead>
      <tbody>
        {courses.map(course => (
          <tr key={course.id}>
            <td style={styles.td}>{course.name}</td>
            <td style={styles.td}>{course.teacher}</td>
            <td style={styles.td}>{course.time}</td>
            <td style={styles.td}>{`${course.enrolled}/${course.capacity}`}</td>

            {/* 🔹 Grade column if NOT in "Add Courses" view */}
            {showJoin === false && (
              <td style={styles.td}>
                {course.grade || "N/A"}
              </td>
            )}

            {/* 🔹 Action buttons if in "Add Courses" tab */}
            {showJoin && (
              <td style={styles.td}>
                {isEnrolled(course.id) ? (
                  <button
                    onClick={() => handleUnenroll(course.id)}
                    style={{
                      padding: '5px 10px',
                      backgroundColor: '#d9534f',
                      color: 'white',
                      border: 'none',
                      borderRadius: '4px',
                      cursor: 'pointer'
                    }}
                  >
                    Unenroll
                  </button>
                ) : (
                  <button
                    onClick={() => handleJoin(course.id)}
                    disabled={course.enrolled >= course.capacity}
                    style={{
                      padding: '5px 10px',
                      backgroundColor: '#4caf50',
                      color: 'white',
                      border: 'none',
                      borderRadius: '4px',
                      cursor: 'pointer'
                    }}
                  >
                    {course.enrolled >= course.capacity ? 'Full' : 'Join'}
                  </button>
                )}
              </td>
            )}
          </tr>
        ))}
      </tbody>
    </table>
  );
  

  return (
    <div style={styles.page}>
      <div style={styles.header}>
        <span style={styles.welcome}>Welcome, Student!</span>
        <a href="/login" style={styles.logout}>Sign out</a>
      </div>

      <h1 style={styles.title}>Student Dashboard</h1>

      <div style={styles.tabs}>
        <button onClick={() => setActiveTab('your')} style={tabStyle(activeTab === 'your')}>Your Courses</button>
        <button onClick={() => setActiveTab('all')} style={tabStyle(activeTab === 'all')}>Add Courses</button>
      </div>

      <div style={styles.tableWrapper}>
        {activeTab === 'your'
          ? renderTable(yourCourses)
          : renderTable(allCourses, true)}
      </div>

    </div>
  );
}

const styles = {
  page: {
    backgroundColor: '#1e1e2f',
    color: '#fff',
    width: '100vw',
    height: '100vh',
    boxSizing: 'border-box',
    fontFamily: 'Arial, sans-serif',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'flex-start',
    padding: '30px'
  },  
  header: {
    width: '100%',
    display: 'flex',
    justifyContent: 'space-between',
    marginBottom: '10px'
  },
  welcome: {
    fontSize: '16px',
    color: '#bbb'
  },
  logout: {
    color: '#99ccff',
    textDecoration: 'none'
  },
  title: {
    fontSize: '28px',
    marginBottom: '30px',
    color: '#ffffff'
  },
  tabs: {
    display: 'flex',
    marginBottom: '20px'
  },
  tableWrapper: {
    width: '90%',
    maxWidth: '900px',
    backgroundColor: '#2e2e48',
    borderRadius: '8px',
    padding: '20px',
    boxShadow: '0 0 10px rgba(0, 0, 0, 0.4)'
  },  
  table: {
    width: '100%',
    borderCollapse: 'collapse'
  },
  tableHead: {
    backgroundColor: '#444'
  },
  th: {
    padding: '10px',
    textAlign: 'left',
    color: '#fff',
    borderBottom: '1px solid #666'
  },
  td: {
    padding: '10px',
    borderBottom: '1px solid #444',
    color: '#ddd'
  }
};

function tabStyle(active) {
  return {
    backgroundColor: active ? '#3f61d0' : '#555',
    color: '#fff',
    border: 'none',
    padding: '10px 20px',
    marginRight: '10px',
    borderRadius: '5px',
    cursor: 'pointer'
  };
}
