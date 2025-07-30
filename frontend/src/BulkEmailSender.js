// frontend/src/components/BulkEmailSender.js
import React, { useState } from 'react';

function BulkEmailSender({ onSend }) {
  // Use "emailInput" consistently as the state variable.
  const [emailInput, setEmailInput] = useState('');
  const [emails, setEmails] = useState([]);         // Array of valid emails (as objects)
  const [invalidEmails, setInvalidEmails] = useState([]); // Array of invalid email strings

  // Validate the textarea input
  const validateEmails = (input) => {
    const lines = input.split(/[\n]+/).map(line => line.trim()).filter(Boolean);
    const valid = [];
    const invalid = [];

    lines.forEach(line => {
      // Allow a comma-separated pair: email, name
      const [email, name = "User"] = line.split(',').map(part => part.trim());
      const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (regex.test(email)) {
        valid.push({ email, name });
      } else {
        invalid.push(email);
      }
    });

    setEmails(valid);
    setInvalidEmails(invalid);
  };

  // Handle changes in the textarea input
  const handleChange = (e) => {
    const value = e.target.value;
    setEmailInput(value);
    validateEmails(value);
  };

  // When the user clicks "Send", call the parent's onSend prop with an array of email strings.
  const handleSend = () => {
    const emailList = emails.map(item => item.email);
    onSend(emailList);
  };

  return (
    <div>
      <h2>Send Bulk Phishing Email</h2>
      <textarea
        value={emailInput}
        onChange={handleChange}
        rows={5}
      ></textarea>
      <p>✅ Valid Emails: {emails.length}</p>
      <p>❌ Invalid Emails: {invalidEmails.length}</p>
      {invalidEmails.length > 0 && (
        <ul style={{ color: 'red' }}>
          {invalidEmails.map((e, i) => (
            <li key={i}>{e}</li>
          ))}
        </ul>
      )}
      <button onClick={handleSend} disabled={emails.length === 0}>
        Send Email to {emails.length} user{emails.length > 1 ? 's' : ''}
      </button>
    </div>
  );
}

export default BulkEmailSender;
