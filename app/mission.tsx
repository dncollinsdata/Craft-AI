import { MaterialIcons } from "@expo/vector-icons";
import { Image } from "expo-image";
import { router } from "expo-router";
import { ScrollView, StyleSheet, Text, View } from "react-native";

import { BottomTabs } from "@/src/components/BottomTabs";
import { CosmicBackground } from "@/src/components/CosmicBackground";
import { CosmicButton } from "@/src/components/CosmicButton";
import { GalaxyHeader } from "@/src/components/GalaxyHeader";
import { GlassPanel } from "@/src/components/GlassPanel";
import { featuredMission } from "@/src/data/crafts";
import { accentColor, colors, radii, spacing } from "@/src/theme";

export default function MissionScreen() {
  return (
    <CosmicBackground>
      <GalaxyHeader active="magic" />
      <ScrollView contentContainerStyle={styles.content}>
        <View style={styles.intro}>
          <Text style={styles.title}>Your Craft Mission Is Ready</Text>
          <Text style={styles.subtitle}>Captain, your crafting blueprints have been calculated.</Text>
        </View>

        <GlassPanel style={styles.card}>
          <Image source={{ uri: featuredMission.imageUrl }} style={styles.image} contentFit="cover" />
          <View style={styles.statsGrid}>
            {featuredMission.stats.map((stat) => (
              <View key={stat.label} style={styles.stat}>
                <MaterialIcons name={stat.icon} color={accentColor(stat.accent)} size={23} />
                <View style={styles.statText}>
                  <Text style={styles.statLabel}>{stat.label}</Text>
                  <Text style={styles.statValue}>{stat.value}</Text>
                </View>
              </View>
            ))}
          </View>

          <Text style={styles.missionTitle}>{featuredMission.title}</Text>
          <Text style={styles.missionCopy}>{featuredMission.subtitle}</Text>

          <SectionTitle icon="shopping-basket" label="Materials Used" />
          <View style={styles.materials}>
            {featuredMission.materials.map((material) => (
              <View key={material} style={styles.materialChip}>
                <MaterialIcons name="star" color={colors.primary} size={13} />
                <Text style={styles.materialText}>{material}</Text>
              </View>
            ))}
          </View>

          <SectionTitle icon="rocket-launch" label="Step-by-Step Mission" />
          <View style={styles.steps}>
            {featuredMission.steps.map((step, index) => (
              <View key={step} style={styles.stepRow}>
                <View style={styles.stepNumber}>
                  <Text style={styles.stepNumberText}>{index + 1}</Text>
                </View>
                <Text style={styles.stepText}>{step}</Text>
              </View>
            ))}
          </View>

          <View style={styles.tips}>
            <Tip icon="shield" title="Safety Protocol" body={featuredMission.safetyTip} tone="error" />
            <Tip icon="auto-awesome" title="Make It Cooler" body={featuredMission.upgradeTip} tone="tertiary" />
          </View>
        </GlassPanel>

        <View style={styles.actions}>
          <CosmicButton icon="draw" onPress={() => router.push("/")}>Make Another Craft</CosmicButton>
          <CosmicButton icon="auto-fix-high" variant="glass" onPress={() => router.push("/plus")}>Make It Cooler</CosmicButton>
          <CosmicButton icon="auto-stories" variant="glass" onPress={() => router.push("/saved")}>Save Craft</CosmicButton>
        </View>
      </ScrollView>
      <BottomTabs active="magic" />
    </CosmicBackground>
  );
}

function SectionTitle({ icon, label }: { icon: "shopping-basket" | "rocket-launch"; label: string }) {
  return (
    <View style={styles.sectionTitle}>
      <MaterialIcons name={icon} color={colors.primary} size={18} />
      <Text style={styles.sectionTitleText}>{label}</Text>
    </View>
  );
}

function Tip({
  icon,
  title,
  body,
  tone
}: {
  icon: "shield" | "auto-awesome";
  title: string;
  body: string;
  tone: "error" | "tertiary";
}) {
  const color = tone === "error" ? colors.error : colors.tertiary;
  const backgroundColor = tone === "error" ? "rgba(147, 0, 10, 0.2)" : "rgba(83, 86, 119, 0.32)";

  return (
    <View style={[styles.tip, { backgroundColor, borderColor: color }]}>
      <MaterialIcons name={icon} color={color} size={23} />
      <View style={styles.tipCopy}>
        <Text style={[styles.tipTitle, { color }]}>{title}</Text>
        <Text style={styles.tipBody}>{body}</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  content: {
    padding: spacing.lg,
    paddingBottom: 132,
    gap: spacing.lg
  },
  intro: {
    alignItems: "center",
    gap: spacing.sm
  },
  title: {
    color: colors.primary,
    fontSize: 34,
    lineHeight: 40,
    fontWeight: "900",
    textAlign: "center"
  },
  subtitle: {
    color: colors.onSurfaceVariant,
    fontSize: 17,
    textAlign: "center",
    fontWeight: "700"
  },
  card: {
    padding: spacing.lg
  },
  image: {
    width: "100%",
    aspectRatio: 1,
    borderRadius: radii.md,
    backgroundColor: colors.surfaceHigh
  },
  statsGrid: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: spacing.sm,
    marginTop: spacing.md
  },
  stat: {
    width: "48%",
    minHeight: 74,
    borderRadius: radii.sm,
    padding: spacing.md,
    flexDirection: "row",
    alignItems: "center",
    gap: spacing.sm,
    backgroundColor: "rgba(39, 42, 44, 0.66)"
  },
  statText: {
    flex: 1
  },
  statLabel: {
    color: colors.onSurfaceVariant,
    fontSize: 10,
    textTransform: "uppercase",
    fontWeight: "900"
  },
  statValue: {
    color: colors.onSurface,
    fontSize: 14,
    fontWeight: "800",
    marginTop: 2
  },
  missionTitle: {
    color: colors.secondary,
    fontSize: 28,
    fontWeight: "900",
    marginTop: spacing.xl
  },
  missionCopy: {
    color: colors.onSurface,
    fontSize: 17,
    lineHeight: 25,
    marginTop: spacing.xs,
    fontWeight: "600"
  },
  sectionTitle: {
    flexDirection: "row",
    alignItems: "center",
    gap: spacing.xs,
    marginTop: spacing.xl,
    marginBottom: spacing.md
  },
  sectionTitleText: {
    color: colors.primary,
    fontSize: 12,
    textTransform: "uppercase",
    fontWeight: "900",
    letterSpacing: 1
  },
  materials: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: spacing.sm
  },
  materialChip: {
    flexDirection: "row",
    gap: spacing.xs,
    alignItems: "center",
    paddingVertical: spacing.xs,
    paddingHorizontal: spacing.sm,
    borderRadius: radii.pill,
    backgroundColor: colors.surfaceHighest
  },
  materialText: {
    color: colors.onSurface,
    fontSize: 13,
    fontWeight: "800"
  },
  steps: {
    gap: spacing.md
  },
  stepRow: {
    flexDirection: "row",
    gap: spacing.md
  },
  stepNumber: {
    width: 26,
    height: 26,
    borderRadius: 13,
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "rgba(211, 187, 255, 0.18)"
  },
  stepNumberText: {
    color: colors.primary,
    fontWeight: "900"
  },
  stepText: {
    flex: 1,
    color: colors.onSurfaceVariant,
    fontSize: 16,
    lineHeight: 23,
    fontWeight: "700"
  },
  tips: {
    gap: spacing.md,
    marginTop: spacing.xl
  },
  tip: {
    borderRadius: radii.sm,
    borderWidth: 1,
    padding: spacing.md,
    flexDirection: "row",
    gap: spacing.md
  },
  tipCopy: {
    flex: 1
  },
  tipTitle: {
    fontSize: 12,
    fontWeight: "900",
    textTransform: "uppercase"
  },
  tipBody: {
    color: colors.onSurface,
    fontSize: 14,
    lineHeight: 20,
    marginTop: 2
  },
  actions: {
    gap: spacing.md
  }
});
