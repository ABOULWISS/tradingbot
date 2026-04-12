import { useEffect, useState } from "react";

export default function CandlesDataPanel() {

    const [data, setData] = useState([]);

    const fetchData = () => {
        const url = "https://serverside-98cu.onrender.com/getall";
        fetch(url)
            .then(res => res.json())
            .then(setData)
            .catch(console.error);
    };

    useEffect(() => {
        fetchData();
    }, []);

    return (
        <div style={{
            width: "4000px",        // ✅ FIXED
            height: "470px",       // ✅ FIXED
            overflowY: "auto",
            background: "#111",
            color: "#eae5e5",
            padding: "12px",
            borderRadius: "12px",
            fontSize: "50px",
            boxShadow: "0 0 20px rgba(0,0,0,0.6)"
        }}>

            {/* Header */}
            <div style={{
                display: "grid",
                gridTemplateColumns: "repeat(5, 1fr)",
                padding: "8px 10px",
                borderBottom: "2px solid #444",
                fontWeight: "bold"
            }}>
                <div>Time</div>
                <div>Open</div>
                <div>Close</div>
                <div>High</div>
                <div>Low</div>
            </div>

            {/* Data */}
            {data.length === 0 ? (
                <div style={{ padding: "10px" }}>No data...</div>
            ) : (
                data.map((item, index) => (
                    <div
                        key={index}
                        style={{
                            display: "grid",
                            gridTemplateColumns: "repeat(5, 1fr)",
                            gap: "10px",
                            padding: "8px 10px",
                            borderBottom: "1px solid #222",
                            alignItems: "center",
                            transition: "0.2s"
                        }}
                        onMouseEnter={(e) => e.currentTarget.style.background = "#1a1a1a"}
                        onMouseLeave={(e) => e.currentTarget.style.background = "transparent"}
                    >
                        <div style={{ color: "#aaa" }}>
                            {new Date(item.time * 1000).toLocaleTimeString()}
                        </div>
                        <div style={{ color: "#4caf50" }}>{item.open}</div>
                        <div style={{ color: "#f44336" }}>{item.close}</div>
                        <div style={{ color: "#2196f3" }}>{item.high}</div>
                        <div style={{ color: "#ff9800" }}>{item.low}</div>
                    </div>
                ))
            )}

        </div>
    );
}