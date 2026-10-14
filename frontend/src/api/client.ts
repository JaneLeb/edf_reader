const BASE = "/api/v1";

export async function uploadEdf(file: File) {
  const fd = new FormData();
  fd.append("edf_file", file);
  const r = await fetch(`${BASE}/holter/`, { method: "POST", body: fd });
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}

export async function fetchSignal(id: string, channel = 0) {
  const r = await fetch(`${BASE}/holter/${id}/signal/?channel=${channel}`);
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}