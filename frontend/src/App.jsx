import { useState } from "react";
import "./App.css";
import MapView from "./components/MapView";

function App() {
  const [station, setStation] = useState("Dadar");
  const [hour, setHour] = useState(8);
  const [result, setResult] = useState(null);

  const predictCrowd = async () => {
    const response = await fetch(
      `http://127.0.0.1:8000/predict?day=12&hour=${hour}&station=${station}&rain=10&delay=5&temp=30&weekend=0`
    );

    const data = await response.json();
    setResult(data);
  };

  return (
    <div style={{ textAlign: "center", fontFamily: "Arial", minHeight: "100vh" }}>
      <h1>Mumbai CrowdRush Predictor</h1>

      <div>
        <label>Station: </label>
        <select value={station} onChange={(e) => setStation(e.target.value)}>
          <option>Thane</option>
          <option>Dombivli</option>
          <option>Ghatkopar</option>
          <option>Kurla</option>
          <option>Dadar</option>
          <option>Byculla</option>
          <option>CSMT</option>
        </select>
      </div>

      <br />

      <div>
        <label>Hour (5-23): </label>
        <input
          type="number"
          value={hour}
          onChange={(e) => setHour(e.target.value)}
        />
      </div>

      <br />

      <button onClick={predictCrowd}>Predict Crowd</button>

      {result && (
        <div style={{ marginTop: "30px" }}>
          <h2>Crowd Level: {result.crowd_level}</h2>
          <h3>{result.recommendation}</h3>
          {result.transport_recommendation && result.transport_recommendation !== "Train" && (
            <div style={{ marginTop: "15px" }}>
              <strong>Recommended Transport: </strong> {result.transport_recommendation}
            </div>
          )}
        </div>
      )}

      <MapView crowdData={result} />
    </div>
  );
}

export default App;
