


// utils/time.js

export function toUnixSeconds(t) {
  if (!t) return null;
  if (typeof t === "number" && t < 1e12) return t; // already seconds
  if (typeof t === "number") return Math.floor(t / 1000); // milliseconds
  const parsed = Date.parse(t);
  if (!isNaN(parsed)) return Math.floor(parsed / 1000); // ISO string
  return null;
}

export function toSafeNumber(n) {
  if (n === null || n === undefined) return null;
  const num = Number(n);
  return isNaN(num) ? null : num;
}
