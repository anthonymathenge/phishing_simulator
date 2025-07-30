// src/App.js
import './app.css'; // Capitalized to match file name
import 'react-quill/dist/quill.snow.css';
import React, { useState } from 'react';
import BulkEmailSender from './BulkEmailSender';
import EmailTemplateEditor from './EmailTemplateEditor';
import './app.css';

function App() {
  const [status, setStatus] = useState('');
  const [templateHTML, setTemplateHTML] = useState('');

  const handleTemplateUpdate = (template) => {
    const { subject, body } = template;
    const html = `<h2>${subject}</h2>${body}`;
    setTemplateHTML(html);
  };

const sendEmail = async (emails) => {
  const formData = new FormData();
  emails.forEach((email) => {
    formData.append("email_list", email); // repeatable key
  });

  // Add the saved template from state (object with subject & body)
  formData.append("template_html", templateHTML);

  try {
    const response = await fetch("http://localhost:8000/send_campaign/", {
      method: "POST",
      body: formData,
    });

    if (response.ok) {
      const data = await response.json();
      setStatus(`✅ Sent: ${data.sent.length}, ❌ Failed: ${data.failed.length}`);
    } else {
      const errText = await response.text();
      console.error("❌ Failed to send:", errText);
      setStatus('❌ Failed to send email.');
    }
  } catch (err) {
    console.error("❌ Network error:", err);
    setStatus('❌ Failed to send email.');
  }
};

  return (
    <div className="App">
      <h1>Simulation Panel</h1>
      <EmailTemplateEditor onTemplateUpdate={handleTemplateUpdate} />
      <BulkEmailSender onSend={sendEmail} />
      <p>{status}</p>
    </div>
  );
}

export default App;

