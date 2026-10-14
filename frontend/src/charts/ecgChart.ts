import * as echarts from "echarts";

export function createEcgChart(el: HTMLElement) {
  const chart = echarts.init(el);
  chart.setOption({
    animation: false,
    tooltip: { trigger: "axis" },
    grid: { left: 60, right: 20, top: 30, bottom: 60 },
    xAxis: { type: "value", name: "Время, с" },
    yAxis: { type: "value", name: "мВ", scale: true },
    dataZoom: [
      { type: "inside", start: 0, end: 5 },
      { type: "slider", start: 0, end: 5, bottom: 10 },
    ],
    series: [{
      name: "ECG",
      type: "line",
      showSymbol: false,
      sampling: "lttb",
      lineStyle: { width: 1, color: "#00da3c" },
      data: [],
    }],
  });
  return chart;
}

export function renderSignal(chart: echarts.ECharts, payload: any) {
  const data = payload.times.map((t: number, i: number) => [t, payload.values[i]]);
  chart.setOption({ series: [{ data }] });
}