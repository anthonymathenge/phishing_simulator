// frontend/src/components/TrackingDashboard.js
import React, { useEffect, useState } from 'react';

function TrackingDashboard() {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    fetch('http://localhost:8000/tracking_data')
      .then(res => res.json())
      .then(data => setLogs(data));
  }, []);

  return (
    <div>
      <h2>Tracking Dashboard</h2>
      <table border="1">
        <thead>
          <tr>
            <th>User ID</th>
            <th>Event</th>
            <th>Timestamp</th>
          </tr>
        </thead>
        <tbody>
          {logs.map((log, index) => (
            <tr key={index}>
              <td>{log.user_id}</td>
              <td>{log.event}</td>
              <td>{log.timestamp}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default TrackingDashboard;
