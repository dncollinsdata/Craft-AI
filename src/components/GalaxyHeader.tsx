import { MaterialIcons } from "@expo/vector-icons";
import { Link } from "expo-router";
import { StyleSheet, Text, View } from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";

import { GlassPanel } from "@/src/components/GlassPanel";
import { colors, spacing } from "@/src/theme";

type GalaxyHeaderProps = {
  active: "create" | "saved" | "magic";
};

export function GalaxyHeader({ active }: GalaxyHeaderProps) {
  const insets = useSafeAreaInsets();

  return (
    <GlassPanel style={[styles.header, { paddingTop: insets.top + spacing.sm }]}>
      <View style={styles.brand}>
        <MaterialIcons name="auto-awesome" color={colors.primary} size={24} />
        <Text style={styles.title}>Galaxy Craft AI</Text>
      </View>
      <View style={styles.links}>
        <NavLink href="/" label="Create" active={active === "create"} />
        <NavLink href="/saved" label="Saved" active={active === "saved"} />
        <NavLink href="/difficulty" label="Magic" active={active === "magic"} />
      </View>
    </GlassPanel>
  );
}

function NavLink({ href, label, active }: { href: "/" | "/saved" | "/difficulty"; label: string; active: boolean }) {
  return (
    <Link href={href} style={[styles.navLabel, active && styles.navLabelActive]}>
      {label}
    </Link>
  );
}

const styles = StyleSheet.create({
  header: {
    borderRadius: 0,
    paddingHorizontal: spacing.lg,
    paddingBottom: spacing.md,
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center"
  },
  brand: {
    flexDirection: "row",
    alignItems: "center",
    gap: spacing.sm,
    flexShrink: 1
  },
  title: {
    color: colors.primary,
    fontSize: 23,
    fontWeight: "900"
  },
  links: {
    flexDirection: "row",
    gap: spacing.md
  },
  navLabel: {
    color: colors.onSurfaceVariant,
    fontSize: 12,
    fontWeight: "800",
    textTransform: "uppercase"
  },
  navLabelActive: {
    color: colors.primary
  }
});
