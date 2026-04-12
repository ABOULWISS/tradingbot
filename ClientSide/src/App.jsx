import { useRef, useState } from "react";
import CandleChart from "./Components/CandlesData/CandleChart";
import CandleData from "./Components/CandlesData/CandlePanel";
import MarketStructure from "./Components/MarketStructure/MarketStructure";
import StructurePanel from "./Components/MarketStructure/StructurePanel";

export default function App() {
  const chartRef = useRef(null);
  const seriesRef = useRef(null);
  const candlesMapRef = useRef(new Map());
  const [timeframe, setTimeframe] = useState("1m");

  return (
    <>
      {/* Chart container */}
      <div>
        <CandleChart
          onReady={({ chart, series, candlesMap }) => {
            chartRef.current = chart;
            seriesRef.current = series;
            candlesMapRef.current = candlesMap;
          }}
          timeframe={timeframe}
          onTimeframeChange={setTimeframe}
        />

        <MarketStructure
          chartRef={chartRef}
          seriesRef={seriesRef}
          candlesMapRef={candlesMapRef}
          timeframe={timeframe}
        />

       
        
      </div>


      <CandleData />
      {/* Right panel */}
      <StructurePanel timeframe={timeframe} />

      
    </>
  );
}