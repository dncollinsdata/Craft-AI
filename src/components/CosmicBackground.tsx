import { LinearGradient } from "expo-linear-gradient";
import type { PropsWithChildren } from "react";
import { StyleSheet, View } from "react-native";

import { colors } from "@/src/theme";

export function CosmicBackground({ children }: PropsWithChildren) {
  return (
    <View style={styles.root}>
      <LinearGradient
        colors={["#101415", "#141019", "#101415"]}
        locations={[0, 0.48, 1]}
        style={StyleSheet.absoluteFill}
      />
      <View style={[styles.glow, styles.primaryGlow]} />
      <View style={[styles.glow, styles.secondaryGlow]} />
      <View style={styles.stars} />
      {children}
    </View>
  );
}

const styles = StyleSheet.create({
  root: {
    flex: 1,
    backgroundColor: colors.background
  },
  glow: {
    position: "absolute",
    width: 360,
    height: 360,
    borderRadius: 180,
    opacity: 0.34
  },
  primaryGlow: {
    top: -100,
    left: -120,
    backgroundColor: colors.primaryContainer
  },
  secondaryGlow: {
    right: -140,
    bottom: 40,
    backgroundColor: colors.secondaryContainer
  },
  stars: {
    position: "absolute",
    top: 0,
    right: 0,
    bottom: 0,
    left: 0,
    opacity: 0.18,
    backgroundColor: "transparent"
  }
});
