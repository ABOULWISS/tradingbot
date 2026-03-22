import { useRef, useState } from "react";
import CandleChart from "./Components/CandleChart";
import MarketStructure from "./Components/MarketStructure";

export default function App() {
  const chartRef = useRef(null);
  const seriesRef = useRef(null);
  const candlesMapRef = useRef(new Map());

  // ✅ Track selected timeframe
  const [timeframe, setTimeframe] = useState("1m");

  return (
    <>
      <CandleChart
        onReady={({ chart, series, candlesMap }) => {
          chartRef.current = chart;
          seriesRef.current = series;
          candlesMapRef.current = candlesMap;
        }}
        timeframe={timeframe}       // optional if you lift state
        onTimeframeChange={setTimeframe} // optional if you lift state
      />

      <MarketStructure
        chartRef={chartRef}
        seriesRef={seriesRef}
        candlesMapRef={candlesMapRef}
        timeframe={timeframe}       // ✅ pass selected timeframe
      />
    </>
  );
}
