const hues = [225, 262, 172, 24, 340, 200, 140, 40];

export default function Avatar({ name = '?', size = 28 }) {
  const hue = hues[[...name].reduce((a, c) => a + c.charCodeAt(0), 0) % hues.length];
  return (
    <span
      className="avatar"
      title={name}
      style={{
        width: size,
        height: size,
        fontSize: size * 0.42,
        background: `hsl(${hue} 70% 94%)`,
        color: `hsl(${hue} 55% 32%)`,
      }}
    >
      {name.slice(0, 2).toUpperCase()}
    </span>
  );
}
