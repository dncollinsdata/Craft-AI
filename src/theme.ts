export const colors = {
  background: "#101415",
  surface: "#1d2022",
  surfaceHigh: "#272a2c",
  surfaceHighest: "#323537",
  onSurface: "#e0e3e5",
  onSurfaceVariant: "#ccc3d7",
  primary: "#d3bbff",
  primaryContainer: "#6d28d9",
  secondary: "#ffb1c7",
  secondaryContainer: "#be0062",
  tertiary: "#c2c4eb",
  tertiaryContainer: "#535677",
  error: "#ffb4ab",
  errorContainer: "#93000a",
  blackGlass: "rgba(16, 20, 21, 0.58)",
  whiteGlass: "rgba(255, 255, 255, 0.07)",
  border: "rgba(255, 255, 255, 0.13)"
};

export const spacing = {
  xs: 6,
  sm: 10,
  md: 16,
  lg: 24,
  xl: 32,
  section: 40
};

export const radii = {
  sm: 12,
  md: 18,
  lg: 28,
  pill: 999
};

export const font = {
  display: "System",
  body: "System"
};

export function accentColor(accent: "primary" | "secondary" | "tertiary") {
  return colors[accent];
}
