// Jednoduché ikony (vlastní SVG, bez externích knihoven a licencí).
const PATHS: Record<string, string> = {
  target: "M12 3a9 9 0 1 0 9 9M12 7a5 5 0 1 0 5 5M12 11a1 1 0 1 0 1 1M13 11l7-7M17 4h3v3",
  steps: "M4 18h4v-4h4v-4h4V6h4",
  print: "M7 8V3h10v5M7 17H4v-7h16v7h-3M7 14h10v7H7z",
  calendar: "M4 6h16v14H4zM4 10h16M8 3v5M16 3v5M8 14h3v3H8z",
};
export default function Icon({ name }: { name: keyof typeof PATHS | string }) {
  return (
    <svg className="icon" viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" strokeWidth="1.8"
         strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d={PATHS[name]} />
    </svg>
  );
}
