import React from "react";
import GenerateQRCode from "./GenerateQRCode";
import ScanQRCode from "./ScanQRCode";

function App() {
  return (
    <div>
      <h1>QR Code Attendance System</h1>
      <GenerateQRCode />
      <ScanQRCode />
    </div>
  );
}

export default App;
