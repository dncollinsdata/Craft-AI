import { MaterialIcons } from "@expo/vector-icons";
import { Link } from "expo-router";
import { StyleSheet, Text, View } from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";

import { colors, radii, spacing } from "@/src/theme";

type BottomTabsProps = {
  active: "create" | "saved" | "magic";
};

export function BottomTabs({ active }: BottomTabsProps) {
  const insets = useSafeAreaInsets();

  return (
    <View style={[styles.tabs, { paddingBottom: Math.max(insets.bottom, spacing.md) }]}>
      <Tab href="/" icon="draw" label="Create" active={active === "create"} />
      <Tab href="/saved" icon="auto-stories" label="Saved" active={active === "saved"} />
      <Tab href="/difficulty" icon="auto-fix-high" label="Magic" active={active === "magic"} />
    </View>
  );
}

function Tab({
  href,
  icon,
  label,
  active
}: {
  href: "/" | "/saved" | "/difficulty";
  icon: "draw" | "auto-stories" | "auto-fix-high";
  label: string;
  active: boolean;
}) {
  return (
    <Link href={href} style={[styles.tab, active && styles.activeTab]}>
      <MaterialIcons name={icon} color={active ? colors.secondary : colors.onSurfaceVariant} size={22} />
      <Text style={[styles.label, active && styles.activeLabel]}>{label}</Text>
    </Link>
  );
}

const styles = StyleSheet.create({
  tabs: {
    position: "absolute",
    left: 0,
    right: 0,
    bottom: 0,
    paddingTop: spacing.sm,
    paddingHorizontal: spacing.lg,
    backgroundColor: "rgba(25, 28, 30, 0.84)",
    borderTopWidth: 1,
    borderColor: colors.border,
    flexDirection: "row",
    justifyContent: "space-around"
  },
  tab: {
    minWidth: 84,
    alignItems: "center",
    justifyContent: "center",
    paddingVertical: spacing.sm,
    borderRadius: radii.pill
  },
  activeTab: {
    backgroundColor: "rgba(190, 0, 98, 0.28)"
  },
  label: {
    marginTop: 2,
    color: colors.onSurfaceVariant,
    fontSize: 11,
    fontWeight: "800",
    textTransform: "uppercase"
  },
  activeLabel: {
    color: colors.secondary
  }
});
