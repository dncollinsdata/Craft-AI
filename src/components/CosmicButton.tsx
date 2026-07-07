import { MaterialIcons } from "@expo/vector-icons";
import * as Haptics from "expo-haptics";
import { LinearGradient } from "expo-linear-gradient";
import type { PropsWithChildren } from "react";
import { Pressable, StyleSheet, Text, ViewStyle } from "react-native";

import type { IconName } from "@/src/data/crafts";
import { colors, radii, spacing } from "@/src/theme";

type CosmicButtonProps = PropsWithChildren<{
  icon?: IconName;
  onPress?: () => void;
  style?: ViewStyle | ViewStyle[];
  variant?: "filled" | "glass";
}>;

export function CosmicButton({ children, icon, onPress, style, variant = "filled" }: CosmicButtonProps) {
  const handlePress = () => {
    Haptics.selectionAsync().catch(() => undefined);
    onPress?.();
  };

  if (variant === "glass") {
    return (
      <Pressable onPress={handlePress} style={({ pressed }) => [styles.glass, pressed && styles.pressed, style]}>
        {icon ? <MaterialIcons name={icon} color={colors.primary} size={21} /> : null}
        <Text style={styles.glassLabel}>{children}</Text>
      </Pressable>
    );
  }

  return (
    <Pressable onPress={handlePress} style={({ pressed }) => [pressed && styles.pressed, style]}>
      <LinearGradient colors={[colors.primaryContainer, colors.secondaryContainer]} style={styles.filled}>
        {icon ? <MaterialIcons name={icon} color="#ffffff" size={22} /> : null}
        <Text style={styles.filledLabel}>{children}</Text>
      </LinearGradient>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  filled: {
    minHeight: 56,
    paddingHorizontal: spacing.lg,
    borderRadius: radii.pill,
    alignItems: "center",
    justifyContent: "center",
    flexDirection: "row",
    gap: spacing.sm
  },
  filledLabel: {
    color: "#ffffff",
    fontSize: 17,
    fontWeight: "800"
  },
  glass: {
    minHeight: 56,
    paddingHorizontal: spacing.lg,
    borderRadius: radii.pill,
    borderWidth: 1,
    borderColor: colors.border,
    backgroundColor: colors.whiteGlass,
    alignItems: "center",
    justifyContent: "center",
    flexDirection: "row",
    gap: spacing.sm
  },
  glassLabel: {
    color: colors.primary,
    fontSize: 17,
    fontWeight: "800"
  },
  pressed: {
    transform: [{ scale: 0.97 }],
    opacity: 0.86
  }
});
