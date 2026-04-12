




import { useEffect, useState } from "react";

export default function StructurePanel() {
    const [mode, setMode] = useState("choch");
    const [data, setData] = useState([]);

    const fetchData = () => {
        const url =
            mode === "choch"
                ? "https://serverside-98cu.onrender.com/market-structure/allchoch"
                : "https://serverside-98cu.onrender.com/market-structure/allbos";

        fetch(url)
            .then(res => res.json())
            .then(setData)
            .catch(console.error);
    };

    useEffect(() => {
        fetchData();
    }, [mode]);

    return (
        <div style={{
            position: "absolute",
            top: "0px",
            right: "-60px",
            width: "1020px",       // fixed width
            height: "2650px",      // fixed height
            overflowY: "auto",
            background: "#0d0d0d",
            color: "#fff",
            padding: "12px",
            borderRadius: "12px",
            fontSize: "50px",
            boxShadow: "0 0 25px rgba(0,0,0,0.7)"
        }}>

 
            
            
            <div style={{
                display: "flex",
                gap: "6px",
                marginBottom: "12px",
                background: "#1a1a1a",
                padding: "4px",
                borderRadius: "8px"
            }}> 



                <button
                    onClick={() => setMode("choch")}
                    style={{
                        flex: 1,
                        background: mode === "choch" ? "#4caf50" : "transparent",
                        color: "#fff",
                        border: "none",
                        borderRadius: "6px",
                        padding: "6px",
                        cursor: "pointer",
                        fontSize: "50px",
                        transition: "0.2s"
                    }}
                >
                    CHOCH
                </button>

                <button
                    onClick={() => setMode("bos")}
                    style={{
                        flex: 1,
                        background: mode === "bos" ? "#2196f3" : "transparent",
                        color: "#fff",
                        border: "none",
                        borderRadius: "6px",
                        padding: "6px",
                        cursor: "pointer",
                        fontSize: "50px",
                        transition: "0.2s"
                    }}
                >
                    BOS
                </button>
            </div>

            {/* 🔥 Data */}
            {data.length === 0 ? (
                <div>No signals...</div>
            ) : (
                data.map(item => {
                    const isBullish = item.direction === "bullish";

                    return (
                        <div
                            key={item.id}
                            style={{
                                background: "#141414",
                                borderRadius: "10px",
                                padding: "10px",
                                marginBottom: "8px",
                                borderLeft: `4px solid ${isBullish ? "#4caf50" : "#f44336"}`,
                                transition: "0.2s"
                            }}
                            onMouseEnter={(e) => e.currentTarget.style.background = "#1c1c1c"}
                            onMouseLeave={(e) => e.currentTarget.style.background = "#141414"}
                        >
                            {/* Top Row */}
                            <div style={{
                                display: "flex",
                                justifyContent: "space-between",
                                marginBottom: "5px",
                                fontWeight: "bold"
                            }}>
                                <span>{item.type}</span>
                                <span style={{
                                    color: isBullish ? "#4caf50" : "#f44336"
                                }}>
                                    {item.direction.toUpperCase()}
                                </span>
                            </div>

                            {/* Time */}
                            <div style={{
                                fontSize: "50px",
                                color: "#aaa"
                            }}>
                                {new Date(item.created_at * 1000).toLocaleTimeString()}
                            </div>
                        </div>
                    );
                })
            )}

        </div>
    );
}