import React, { useState, useEffect } from 'react';

export default function TeacherDashboard() {
  const teacherId = 2; // Hardcoded for now
  const [classes, setClasses] = useState([]);
  const [selectedClassId, setSelectedClassId] = useState(null);
  const [students, setStudents] = useState([]);

  useEffect(() => {
    fetch(`http://localhost:5000/api/teacher/${teacherId}/classes`)
      .then(res => res.json())
      .then(data => setClasses(data));
  }, []);

  const handleClassSelect = (classId) => {
    setSelectedClassId(classId);
    fetch(`http://localhost:5000/api/class/${classId}/students`)
      .then(res => res.json())
      .then(data => setStudents(data));
  };

  const handleGradeChange = (studentId, newGrade) => {
    if (!newGrade || newGrade.trim() === '') {
      alert("Please enter a valid grade.");
      return;
    }
  
    fetch(`http://localhost:5000/api/class/${selectedClassId}/student/${studentId}/grade`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ grade: newGrade })
    })
      .then(res => res.json())
      .then(() => {
        return fetch(`http://localhost:5000/api/class/${selectedClassId}/students`);
      })
      .then(res => res.json())
      .then(data => setStudents(data));
  };  

  return (
    <div style={styles.page}>
      <div style={styles.header}>
        <h1>Teacher Dashboard</h1>
        <a href="/login" style={styles.logout}>Sign Out</a>
      </div>

      <div style={styles.container}>
        <div style={styles.sidebar}>
          <h3>Your Classes</h3>
          {classes.map(c => (
            <button
              key={c.id}
              style={styles.classButton}
              onClick={() => handleClassSelect(c.id)}
            >
              {c.name}
            </button>
          ))}
        </div>

        <div style={styles.main}>
          {selectedClassId ? (
            <>
              <h3>Enrolled Students</h3>
              <table style={styles.table}>
                <thead>
                  <tr>
                    <th style={styles.th}>Email</th>
                    <th style={styles.th}>Grade</th>
                    <th style={styles.th}>Edit</th>
                  </tr>
                </thead>
                <tbody>
                  {students.map((s) => (
                    <tr key={s.student_id}>
                      <td style={styles.td}>{s.email}</td>
                      <td style={styles.td}>{s.grade || 'N/A'}</td>
                      <td style={styles.td}>
                        <input
                          type="text"
                          value={s.newGrade || ''}
                          onChange={(e) => {
                            const updated = students.map(stu =>
                              stu.student_id === s.student_id
                                ? { ...stu, newGrade: e.target.value }
                                : stu
                            );
                            setStudents(updated);
                          }}
                          style={styles.input}
                        />
                        <button
                          onClick={() => handleGradeChange(s.student_id, s.newGrade)}
                          style={styles.gradeButton}
                        >
                          Change Grade
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </>
          ) : (
            <p>Select a class to view students.</p>
          )}
        </div>
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
    margin: 0,
    padding: 0,
    boxSizing: 'border-box',
    fontFamily: 'Arial, sans-serif',
    display: 'flex',
    flexDirection: 'column',
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    marginBottom: '20px'
  },
  logout: {
    color: '#99ccff',
    textDecoration: 'none'
  },
  container: {
    display: 'flex',
    flexGrow: 1,
    width: '100%',
    height: '100%',
  },
  sidebar: {
    width: '200px',
    marginRight: '30px'
  },
  classButton: {
    width: '100%',
    padding: '10px',
    marginBottom: '10px',
    backgroundColor: '#3f61d0',
    color: 'white',
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer'
  },
  main: {
    flexGrow: 1
  },
  table: {
    width: '100%',
    borderCollapse: 'collapse',
    backgroundColor: '#2e2e48',
    borderRadius: '8px',
    overflow: 'hidden'
  },
  th: {
    padding: '10px',
    backgroundColor: '#444',
    borderBottom: '1px solid #666'
  },
  td: {
    padding: '10px',
    borderBottom: '1px solid #444',
    color: '#ddd'
  },
  input: {
    padding: '6px',
    borderRadius: '4px',
    border: '1px solid #888',
    backgroundColor: '#1e1e2f',
    color: '#fff',
    width: '60px'
  },
  gradeButton: {
    marginLeft: '10px',
    padding: '6px 10px',
    backgroundColor: '#3f61d0',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontWeight: 'bold'
  }  
};
