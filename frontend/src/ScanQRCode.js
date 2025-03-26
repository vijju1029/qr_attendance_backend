import React, { useState, useEffect } from "react";
import { Html5QrcodeScanner, Html5Qrcode } from "html5-qrcode";
import axios from "axios";

const ScanQRCode = () => {
  const [scannedId, setScannedId] = useState("");
  const [message, setMessage] = useState("");
  const [scanning, setScanning] = useState(false);
  let scanner = null; // Store the scanner instance

  useEffect(() => {
    return () => {
      if (scanner) {
        scanner.clear();
      }
    };
  }, []);

  const startScanner = () => {
    setScanning(true);
    setMessage("");

    setTimeout(() => {
      const readerElement = document.getElementById("qr-reader");
      if (!readerElement) {
        console.error("QR Scanner Error: Element not found.");
        setMessage("Error: Scanner element not found.");
        setScanning(false);
        return;
      }

      scanner = new Html5QrcodeScanner("qr-reader", {
        fps: 10,
        qrbox: { width: 250, height: 250 },
      });

      scanner.render(
        async (decodedText) => {
          setScannedId(decodedText);
          try {
            const response = await axios.post(
              "http://127.0.0.1:8000/api/mark_attendance/",
              { employee_id: decodedText }
            );
            setMessage(response.data.message);
          } catch (error) {
            setMessage("Error marking attendance");
          }
          scanner.clear();
          setScanning(false);
        },
        (error) => console.log("QR Scanner Error:", error)
      );
    }, 500); // Delay to ensure the div is rendered
  };

  const stopScanner = () => {
    if (scanner) {
      scanner.clear();
    }
    setScanning(false);
    setMessage("Scanner stopped.");
  };

  return (
    <div>
      <h2>Scan QR Code</h2>
      {!scanning && <button onClick={startScanner}>Start Scanning</button>}
      {scanning && (
        <>
          <div id="qr-reader"></div>
          <button onClick={stopScanner}>Stop Scanning</button>
        </>
      )}
      {scannedId && <p>Scanned Employee ID: {scannedId}</p>}
      <p>{message}</p>
    </div>
  );
};

export default ScanQRCode;
