export function dt2hhmmss(dt: Date) {
  return dt.toISOString().substr(11, 8);
}

export function s2hhmmss(s: number) {
  return dt2hhmmss(new Date(s * 1000));
}
