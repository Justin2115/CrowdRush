import { MapContainer, TileLayer, CircleMarker, Popup, useMap } from "react-leaflet";
import { useEffect } from "react";


const stations = [
    { name: "Thane", position: [19.186, 72.975] },
    { name: "Dombivli", position: [19.216, 73.086] },
    { name: "Ghatkopar", position: [19.085, 72.908] },
    { name: "Kurla", position: [19.072, 72.879] },
    { name: "Dadar", position: [19.018, 72.843] },
    { name: "Byculla", position: [18.976, 72.833] },
    { name: "CSMT", position: [18.939, 72.835] }
];

const getColor = (level) => {
    if (level === "Low") return "green";
    if (level === "Medium") return "yellow";
    if (level === "High") return "orange";
    if (level === "Extreme") return "red";
    return "blue";
};

function MapView({ crowdData }) {
    return (
        <div style={{
            width: "900px",
            margin: "40px auto",
            borderRadius: "12px",
            overflow: "hidden",
            boxShadow: "0 0 20px rgba(0,0,0,0.4)"
        }}>
            <MapContainer center={[19.076, 72.8777]} zoom={11} scrollWheelZoom={true} style={{ height: "500px", width: "100%" }}>

                <TileLayer
                    attribution='© OpenStreetMap contributors'
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />

                {stations.map((station, index) => (
                    <CircleMarker
                        key={index}
                        center={station.position}
                        radius={10}
                        pathOptions={{
                            color: crowdData?.station === station.name ? getColor(crowdData.crowd_level) : "gray",
                            fillOpacity: 0.8
                        }}
                    >
                        <Popup>
                            <b>{station.name}</b><br />
                            {crowdData?.station === station.name
                                ? `Crowd: ${crowdData.crowd_level}`
                                : "No prediction yet"}
                        </Popup>
                    </CircleMarker>
                ))}
            </MapContainer>
        </div>
    );

}

export default MapView;
