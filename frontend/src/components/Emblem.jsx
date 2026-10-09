function Emblem({ size = 56, className = "" }) {
  const spokes = Array.from({ length: 24 }, (_, i) => i);

  return (
    <svg
      className={`emblem-svg ${className}`.trim()}
      width={size}
      height={size}
      viewBox="0 0 100 100"
      role="img"
      aria-label="YojanaSaathi emblem"
    >
      <circle cx="50" cy="50" r="48" fill="#ffffff" stroke="#0f3460" strokeWidth="2" />

      {/* Saffron (top) and green (bottom) accent arcs */}
      <path
        d="M50 4 A46 46 0 0 1 96 50"
        fill="none"
        stroke="#e67e22"
        strokeWidth="4"
        strokeLinecap="round"
      />
      <path
        d="M50 96 A46 46 0 0 1 4 50"
        fill="none"
        stroke="#1a7a4a"
        strokeWidth="4"
        strokeLinecap="round"
      />

      {/* Wheel (chakra) */}
      <circle cx="50" cy="50" r="36" fill="none" stroke="#0f3460" strokeWidth="2.5" />
      <g stroke="#0f3460" strokeWidth="1.4">
        {spokes.map((i) => (
          <line
            key={i}
            x1="50"
            y1="50"
            x2="50"
            y2="17"
            transform={`rotate(${(i * 360) / 24} 50 50)`}
          />
        ))}
      </g>
      <circle cx="50" cy="50" r="4.5" fill="#0f3460" />
    </svg>
  );
}

export default Emblem;
