
import { useEffect, useRef, useState } from "react";
import { createChart, CandlestickSeries } from "lightweight-charts";
import { toUnixSeconds, toSafeNumber } from "../../utils/time";

const MAX_VISIBLE_BARS = 300;
const LOAD_MORE_STEP = 3000;


  const API_URL = import.meta.env.VITE_API_URL;
  const WS_URL = import.meta.env.VITE_WS_URL;

// 🔥 ADD: Timeframes
const TIMEFRAMES = [
  { label: "1 Min", value: "1m" },
  { label: "5 Min", value: "5m" },
  { label: "15 Min", value: "15m" },
  { label: "1 Hour", value: "1h" },
  { label: "4 Hour", value: "4h" },
  { label: "1 Day", value: "1d" },
];

export default function CandleChart({ onReady   ,  timeframe, onTimeframeChange}) {

  const containerRef = useRef(null);
  const chartRef = useRef(null);
  const seriesRef = useRef(null);

  const candlesMapRef = useRef(new Map());
  const allDataRef = useRef([]);
  const windowRef = useRef({ start: 0, end: 0 });

  // 🔥 ADD: timeframe state
  //const [timeframe, setTimeframe] = useState("1m");




  // ======================
  // CREATE CHART (ONCE)
  // ======================
  useEffect(() => {
    if (!containerRef.current) return;

    const chart = createChart(containerRef.current, {
      width: 4000,
      height: 2100,

      layout: {
        background: { color: "#0f172a" },
        textColor: "#cbd5e1",
        fontSize: 40,
      },

      grid: {
        vertLines: { visible: false },
        horzLines: { visible: false },
      },

      timeScale: {
        timeVisible: true,
        secondsVisible: false,
        rightBarStaysOnScroll: true,
        fixLeftEdge: true,
      },

      rightPriceScale: {
        borderVisible: false,
      },

      crosshair: {
        mode: 0,
      },
    });

    const series = chart.addSeries(CandlestickSeries, {
      upColor: "#22c55e",
      downColor: "#ef4444",
      wickUpColor: "#22c55e",
      wickDownColor: "#ef4444",
      borderVisible: false,
    });

    chartRef.current = chart;
    seriesRef.current = series;

    if (onReady) {
      onReady({
        chart,
        series,
        candlesMap: candlesMapRef.current,
      });
    }

    // LOAD MORE DATA WHEN SCROLLING LEFT
    chart.timeScale().subscribeVisibleLogicalRangeChange(range => {
      if (!range) return;

      const { start, end } = windowRef.current;
      if (start === 0) return;

      if (range.from < 50) {
        const newStart = Math.max(0, start - LOAD_MORE_STEP);
        windowRef.current.start = newStart;
        series.setData(allDataRef.current.slice(newStart, end));
      }
    });

    return () => chart.remove();
  }, []);


  useEffect(() => {
    if (!seriesRef.current || !chartRef.current) return;

    fetch(`https://serverside-98cu.onrender.com/getallpertf?tf=${timeframe}`)
      .then(res => res.json())
      .then(raw => {
        const data = raw
          .map(c => ({
            id : toSafeNumber(c.id ?? c.MarketDataID),
            time: toUnixSeconds(c.time ?? c.Timestamp),
            open: toSafeNumber(c.open ?? c.Open),
            high: toSafeNumber(c.high ?? c.High),
            low: toSafeNumber(c.low ?? c.Low),
            close: toSafeNumber(c.close ?? c.Close),
          }))
          .filter(c => c.time)
          .sort((a, b) => a.time - b.time);

        allDataRef.current = data;

        candlesMapRef.current.clear();
        data.forEach(candle => {
          candlesMapRef.current.set(candle.id, candle);
        });

        const end = data.length;
        const start = Math.max(0, end - LOAD_MORE_STEP);
        windowRef.current = { start, end };

        // 🔥 RESET SERIES DATA
        seriesRef.current.setData(data.slice(start, end));

        // 🔥 RESET VIEW
        chartRef.current.timeScale().setVisibleLogicalRange({
          from: Math.max(0, end - MAX_VISIBLE_BARS),
          to: end,
        });
      })
      .catch(console.error);
  }, [timeframe]);


  useEffect(() => {
    if (!seriesRef.current) return;

    const ws = new WebSocket(`wss://serverside-98cu.onrender.com/ws/price`);

    ws.onopen = () => {
      console.log("✅ WS connected");
    };

    ws.onmessage = (event) => {
      try {
        const msg = JSON.parse(event.data);

        // 🔥 normalize data (same as REST)
        const candle = {
          id: toSafeNumber(msg.id ?? msg.MarketDataID),
          time: toUnixSeconds(msg.time ?? msg.Timestamp),
          open: toSafeNumber(msg.open ?? msg.Open),
          high: toSafeNumber(msg.high ?? msg.High),
          low: toSafeNumber(msg.low ?? msg.Low),
          close: toSafeNumber(msg.close ?? msg.Close),
        };

        if (!candle.time) return;

        // 🔥 update map
        candlesMapRef.current.set(candle.id, candle);

        // 🔥 update chart (REAL-TIME)
        seriesRef.current.update(candle);

      } catch (err) {
        console.error("WS parse error:", err);
      }
    };

    ws.onerror = (err) => {
      console.error("WS error:", err);
    };

    ws.onclose = () => {
      console.log("❌ WS disconnected");
    };

    return () => {
      ws.close();
    };
  }, [timeframe]);

  

  // ======================
  // RENDER
  // ======================
  return (
    <div
      style={{
        width: "79.5%",
        height: "80vh",
        overflow: "auto",
        background: "#020617",
        padding: "20px",
      }}
    >


       {/* 🔥 ADD: TIMEFRAME COMBOBOX */}
      <div style={{ marginBottom: "12px" }}>
        <select
          value={timeframe}
          //onChange={e => setTimeframe(e.target.value)}
            onChange={e => onTimeframeChange(e.target.value)}


          style={{
            padding: "8px 12px",
            background: "#020617",
            color: "#cbd5e1",
            border: "1px solid #334155",
            borderRadius: "6px",
            fontSize: "40px",
          }}
        >  
          {TIMEFRAMES.map(tf => (
            <option key={tf.value} value={tf.value}>
              {tf.label}
            </option>
          ))}
        </select>
      </div>

             {/*  
      <div style={{ marginBottom: "12px" }}>
        <select
          value={timeframe}
          //onChange={e => setTimeframe(e.target.value)}
            onChange={e => onTimeframeChange(e.target.value)}


          style={{
            padding: "8px 12px",
            background: "#020617",
            color: "#cbd5e1",
            border: "1px solid #334155",
            borderRadius: "6px",
            fontSize: "40px",
          }}
        >  
          {TIMEFRAMES.map(tf => (
            <option key={tf.value} value={tf.value}>
              {tf.label}
            </option>
          ))}
        </select>
      </div>
        */}
      
      <div
        ref={containerRef}
        style={{
          width: "1000px",
          height: "600px",
        }}
      />
    </div>
  );
}



