import { uploadEdf, fetchSignal } from "./api/client";
import { createEcgChart, renderSignal } from "./charts/ecgChart";

const fileInput = document.getElementById("edf-file") as HTMLInputElement;
const uploadBtn = document.getElementById("upload-btn") as HTMLButtonElement;
const statusEl = document.getElementById("status") as HTMLSpanElement;
const chartEl = document.getElementById("chart") as HTMLDivElement;

const chart = createEcgChart(chartEl);

fileInput.addEventListener("change", () => {
  uploadBtn.disabled = !fileInput.files?.length;
});

uploadBtn.addEventListener("click", async () => {
  const file = fileInput.files?.[0];
  if (!file) return;
  statusEl.textContent = "Загрузка…";
  try {
    const record = await uploadEdf(file);
    statusEl.textContent = `Загружено: ${record.id} (${record.status})`;
    if (record.status !== "ready") {
      statusEl.textContent += ` — ошибка: ${record.error_message}`;
      return;
    }
    statusEl.textContent += " — читаю сигнал…";
    const signal = await fetchSignal(record.id, 0);
    renderSignal(chart, signal);
    statusEl.textContent += " — готово";
  } catch (e: any) {
    statusEl.textContent = "Ошибка: " + e.message;
  }
});