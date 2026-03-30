






import { useEffect, useRef } from "react";
import { LineSeries } from "lightweight-charts";

export default function MarketStructure({
    chartRef,
    seriesRef,
    candlesMapRef,
    timeframe
}) {
    const drawnRef = useRef(new Set());
    const linesRef = useRef([]);

    useEffect(() => {
        if (!chartRef.current || !seriesRef.current) return;

        // 🔥 CLEAN OLD STRUCTURES WHEN TIMEFRAME CHANGES
        linesRef.current.forEach(line => {
            chartRef.current.removeSeries(line);
        });

        linesRef.current = [];
        drawnRef.current.clear();

        const interval = setInterval(() => {
            if (!candlesMapRef.current?.size) return;

            fetch(`https://serverside-98cu.onrender.com/market-structure/allPertimeframe?timeframe=${timeframe}`)
                .then(res => res.json())
                .then(structures => {

                    structures.forEach(ms => {

                        if (drawnRef.current.has(ms.id)) return;

                        const candle = candlesMapRef.current.get(ms.market_data_id);
                        if (!candle) return;

                        const isHigh = ms.type === "HH" || ms.type === "LH";
                        const basePrice = isHigh ? candle.high : candle.low;
                        const price = isHigh ? basePrice + 10 : basePrice - 10;

                        const time =
                            candle.time > 9999999999
                                ? Math.floor(candle.time / 1000)
                                : candle.time;

                        const line = chartRef.current.addSeries(LineSeries, {
                            color: "#f9faf6",
                            lineWidth: 1,
                            lastValueVisible: false,
                            priceLineVisible: false,
                        });

                        line.setData([
                            { time: time, value: price },
                            { time: time + 300, value: price },
                        ]);

                        // 🔥 STORE LINE REFERENCE
                        linesRef.current.push(line);

                        drawnRef.current.add(ms.id);

                    });

                })
                .catch(console.error);

        }, 300);

        return () => {
            clearInterval(interval);

            // Cleanup when component unmounts or timeframe changes
            linesRef.current.forEach(line => {
                chartRef.current.removeSeries(line);
            });

            linesRef.current = [];
            drawnRef.current.clear();
        };

    }, [timeframe]); // 🔥 Only depend on timeframe

    return null;
}

