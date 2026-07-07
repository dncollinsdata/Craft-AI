import { BlurView } from "expo-blur";
import type { PropsWithChildren } from "react";
import { StyleSheet, ViewStyle } from "react-native";

import { colors, radii } from "@/src/theme";

type GlassPanelProps = PropsWithChildren<{
  style?: ViewStyle | ViewStyle[];
  intensity?: number;
}>;

export function GlassPanel({ children, style, intensity = 24 }: GlassPanelProps) {
  return (
    <BlurView intensity={intensity} tint="dark" style={[styles.panel, style]}>
      {children}
    </BlurView>
  );
}

const styles = StyleSheet.create({
  panel: {
    overflow: "hidden",
    borderRadius: radii.md,
    borderWidth: 1,
    borderColor: colors.border,
    backgroundColor: colors.whiteGlass
  }
});
