import React, { useState, useEffect } from 'react';
import ReactQuill from 'react-quill';

function EmailTemplateEditor({ onTemplateUpdate }) {
  const [subject, setSubject] = useState('');
  const [body, setBody] = useState('');
  const [saved, setSaved] = useState(false);

  const handleSave = async () => {
  console.log("Saving template...", { subject, body });

  try {
    const response = await fetch("http://localhost:8000/template/save", {
      method: "POST",
      body: new URLSearchParams({ subject, body }),
    });

    console.log("Response status:", response.status);

    if (response.ok) {
      const data = await response.json();
      console.log("Response data:", data);
      onTemplateUpdate({ subject, body });
      setSaved(true);
      setTimeout(() => setSaved(false), 2000);
    } else {
      console.error("Failed to save template. Server responded with status:", response.status);
    }
  } catch (error) {
    console.error("Error saving template:", error);
  }
};

  useEffect(() => {
    // Load template on mount
    fetch("http://localhost:8000/template/load")
      .then((res) => res.json())
      .then((data) => {
        setSubject(data.subject);
        setBody(data.body);
      });
  }, []);

  return (
    <div style={{ padding: '1rem' }}>
      <h2>Email Template Editor</h2>

      <div>
        <label><strong>Subject:</strong></label>
        <input
          type="text"
          value={subject}
          onChange={(e) => setSubject(e.target.value)}
          style={{ width: '100%', padding: '8px', marginBottom: '1rem' }}
        />
      </div>

      <div>
        <label><strong>Email Body:</strong></label>
        <ReactQuill value={body} onChange={setBody} style={{ height: '200px', marginBottom: '1rem' }} />
      </div>

      {saved && <span style={{ marginLeft: '1rem', color: 'green' }}>✓ Template Saved!</span>}
     
      <hr />
      <h3>📧 Preview</h3>
      <h4><strong>{subject}</strong></h4>
      <div dangerouslySetInnerHTML={{ __html: body }} />

      <button onClick={handleSave}>Save Template</button>
    </div>
      
    

  );
}

export default EmailTemplateEditor;
