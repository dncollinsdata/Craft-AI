import { MaterialIcons } from "@expo/vector-icons";
import { router } from "expo-router";
import { LinearGradient } from "expo-linear-gradient";
import { Pressable, ScrollView, StyleSheet, Text, View } from "react-native";

import { BottomTabs } from "@/src/components/BottomTabs";
import { CosmicBackground } from "@/src/components/CosmicBackground";
import { CosmicButton } from "@/src/components/CosmicButton";
import { GalaxyHeader } from "@/src/components/GalaxyHeader";
import { GlassPanel } from "@/src/components/GlassPanel";
import { welcomeFeatures } from "@/src/data/crafts";
import { accentColor, colors, radii, spacing } from "@/src/theme";

export default function WelcomeScreen() {
  return (
    <CosmicBackground>
      <GalaxyHeader active="create" />
      <ScrollView contentContainerStyle={styles.content}>
        <GlassPanel style={styles.hero}>
          <View style={styles.badge}>
            <MaterialIcons name="rocket-launch" color={colors.primary} size={16} />
            <Text style={styles.badgeText}>Space Camp Open For Adventure</Text>
          </View>
          <Text style={styles.headline}>Turn your stuff into magical crafts.</Text>
          <Text style={styles.copy}>
            Grab paper, tape, glue, and odd little supplies. Galaxy Craft AI turns what you have into a playful mission.
          </Text>
          <CosmicButton icon="auto-fix-high" onPress={() => router.push("/difficulty")} style={styles.cta}>
            Start Crafting
          </CosmicButton>
          <View style={styles.steps}>
            {welcomeFeatures.map((feature) => (
              <View key={feature.label} style={styles.step}>
                <View style={styles.stepIcon}>
                  <MaterialIcons name={feature.icon} color={accentColor(feature.accent)} size={24} />
                </View>
                <Text style={styles.stepLabel}>{feature.label}</Text>
              </View>
            ))}
          </View>
        </GlassPanel>

        <View style={styles.featureGrid}>
          <GlassPanel style={styles.challenge}>
            <LinearGradient colors={["rgba(109,40,217,0.72)", "rgba(190,0,98,0.28)"]} style={StyleSheet.absoluteFill} />
            <Text style={styles.challengeLabel}>Weekly Challenge</Text>
            <Text style={styles.challengeTitle}>Cardboard Star Cruiser</Text>
          </GlassPanel>
          <MiniCard icon="auto-awesome" title="Magic Ideas" body="Get surprise prompts." />
          <MiniCard icon="draw" title="Blueprints" body="Step-by-step guides." />
        </View>
      </ScrollView>
      <Pressable style={styles.fab} onPress={() => router.push("/materials")}>
        <MaterialIcons name="add-a-photo" color="#ffffff" size={30} />
      </Pressable>
      <BottomTabs active="create" />
    </CosmicBackground>
  );
}

function MiniCard({ icon, title, body }: { icon: "auto-awesome" | "draw"; title: string; body: string }) {
  return (
    <GlassPanel style={styles.miniCard}>
      <MaterialIcons name={icon} color={colors.tertiary} size={34} />
      <Text style={styles.miniTitle}>{title}</Text>
      <Text style={styles.miniBody}>{body}</Text>
    </GlassPanel>
  );
}

const styles = StyleSheet.create({
  content: {
    padding: spacing.lg,
    paddingBottom: 132,
    gap: spacing.lg
  },
  hero: {
    padding: spacing.xl,
    alignItems: "center"
  },
  badge: {
    flexDirection: "row",
    alignItems: "center",
    gap: spacing.xs,
    borderRadius: radii.pill,
    borderWidth: 1,
    borderColor: "rgba(211, 187, 255, 0.22)",
    backgroundColor: "rgba(211, 187, 255, 0.1)",
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.xs,
    marginBottom: spacing.lg
  },
  badgeText: {
    color: colors.primary,
    fontSize: 11,
    fontWeight: "900",
    textTransform: "uppercase"
  },
  headline: {
    color: colors.onSurface,
    fontSize: 39,
    lineHeight: 44,
    fontWeight: "900",
    textAlign: "center"
  },
  copy: {
    color: colors.onSurfaceVariant,
    fontSize: 18,
    lineHeight: 27,
    textAlign: "center",
    marginTop: spacing.md
  },
  cta: {
    marginTop: spacing.xl
  },
  steps: {
    flexDirection: "row",
    gap: spacing.md,
    marginTop: spacing.xl
  },
  step: {
    flex: 1,
    alignItems: "center",
    gap: spacing.sm
  },
  stepIcon: {
    width: 52,
    height: 52,
    borderRadius: 26,
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "rgba(39, 42, 44, 0.72)"
  },
  stepLabel: {
    color: colors.onSurfaceVariant,
    fontSize: 12,
    fontWeight: "900",
    textTransform: "uppercase",
    textAlign: "center"
  },
  featureGrid: {
    gap: spacing.md
  },
  challenge: {
    minHeight: 184,
    justifyContent: "flex-end",
    padding: spacing.lg
  },
  challengeLabel: {
    color: colors.secondary,
    fontSize: 12,
    fontWeight: "900",
    textTransform: "uppercase"
  },
  challengeTitle: {
    color: "#ffffff",
    fontSize: 24,
    fontWeight: "900",
    marginTop: spacing.xs
  },
  miniCard: {
    padding: spacing.lg,
    alignItems: "center",
    gap: spacing.sm
  },
  miniTitle: {
    color: colors.onSurface,
    fontSize: 22,
    fontWeight: "900"
  },
  miniBody: {
    color: colors.onSurfaceVariant,
    fontSize: 15,
    fontWeight: "700"
  },
  fab: {
    position: "absolute",
    right: spacing.lg,
    bottom: 112,
    width: 62,
    height: 62,
    borderRadius: 31,
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: colors.primaryContainer
  }
});
