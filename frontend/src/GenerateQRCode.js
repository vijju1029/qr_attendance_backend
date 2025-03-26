import React, { useState } from "react";
import axios from "axios";
import "./styles.css"; // Import the CSS file

const GenerateQRCode = () => {
  const [employeeId, setEmployeeId] = useState("");
  const [name, setName] = useState("");
  const [department, setDepartment] = useState("");
  const [qrUrl, setQrUrl] = useState("");

  const handleGenerateQR = async () => {
    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/api/register/",
        {
          employee_id: employeeId,
          name: name,
          department: department,
        },
        {
          headers: { "Content-Type": "application/json" },
        }
      );

      if (response.data.qr_code) {
        setQrUrl(`http://127.0.0.1:8000${response.data.qr_code}`);
      } else {
        console.error("QR Code not received");
      }
    } catch (error) {
      console.error("Error generating QR:", error.message);
    }
  };

  return (
    <div className="container">
      <h2>Generate QR Code</h2>
      <input
        type="text"
        placeholder="Employee ID"
        value={employeeId}
        onChange={(e) => setEmployeeId(e.target.value)}
      />
      <input
        type="text"
        placeholder="Name"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />
      <input
        type="text"
        placeholder="Department"
        value={department}
        onChange={(e) => setDepartment(e.target.value)}
      />
      <button onClick={handleGenerateQR}>Generate QR Code</button>
      {qrUrl && <img src={qrUrl} alt="QR Code" />}
    </div>
  );
};

export default GenerateQRCode;
