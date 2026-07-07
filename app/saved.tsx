import { MaterialIcons } from "@expo/vector-icons";
import { Image } from "expo-image";
import { ScrollView, StyleSheet, Text, View } from "react-native";

import { BottomTabs } from "@/src/components/BottomTabs";
import { CosmicBackground } from "@/src/components/CosmicBackground";
import { CosmicButton } from "@/src/components/CosmicButton";
import { GalaxyHeader } from "@/src/components/GalaxyHeader";
import { GlassPanel } from "@/src/components/GlassPanel";
import { savedMissions } from "@/src/data/crafts";
import { colors, radii, spacing } from "@/src/theme";

export default function SavedScreen() {
  return (
    <CosmicBackground>
      <GalaxyHeader active="saved" />
      <ScrollView contentContainerStyle={styles.content}>
        <View style={styles.intro}>
          <Text style={styles.title}>My Craft Missions</Text>
          <Text style={styles.subtitle}>Your stellar collection of creative blueprints and interstellar projects.</Text>
        </View>

        {savedMissions.map((mission) => (
          <GlassPanel key={mission.title} style={styles.card}>
            <View>
              <Image source={{ uri: mission.imageUrl }} style={styles.image} contentFit="cover" />
              <View style={styles.badge}>
                <Text style={styles.badgeText}>{mission.badge}</Text>
              </View>
            </View>
            <View style={styles.cardBody}>
              <Text style={styles.cardTitle}>{mission.title}</Text>
              <InfoRow icon="star" label={`Difficulty: ${mission.difficulty}`} />
              <InfoRow icon="schedule" label={`Time: ${mission.time}`} />
              <InfoRow icon="inventory-2" label={`Materials: ${mission.materials}`} />
              <View style={styles.cardActions}>
                <CosmicButton icon="rocket-launch" style={styles.openButton}>Open Craft</CosmicButton>
                <View style={styles.deleteButton}>
                  <MaterialIcons name="delete" color={colors.error} size={22} />
                </View>
              </View>
            </View>
          </GlassPanel>
        ))}
      </ScrollView>
      <BottomTabs active="saved" />
    </CosmicBackground>
  );
}

function InfoRow({ icon, label }: { icon: "star" | "schedule" | "inventory-2"; label: string }) {
  return (
    <View style={styles.infoRow}>
      <MaterialIcons name={icon} color={colors.secondary} size={20} />
      <Text style={styles.infoLabel}>{label}</Text>
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
    gap: spacing.xs
  },
  title: {
    color: colors.onSurface,
    fontSize: 36,
    lineHeight: 42,
    fontWeight: "900"
  },
  subtitle: {
    color: colors.onSurfaceVariant,
    fontSize: 17,
    lineHeight: 25,
    fontWeight: "700"
  },
  card: {
    overflow: "hidden"
  },
  image: {
    height: 190,
    width: "100%",
    backgroundColor: colors.surfaceHigh
  },
  badge: {
    position: "absolute",
    left: spacing.md,
    top: spacing.md,
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.xs,
    borderRadius: radii.pill,
    backgroundColor: "rgba(16, 20, 21, 0.78)",
    borderWidth: 1,
    borderColor: colors.border
  },
  badgeText: {
    color: colors.primary,
    fontSize: 11,
    fontWeight: "900",
    textTransform: "uppercase"
  },
  cardBody: {
    padding: spacing.lg,
    gap: spacing.md
  },
  cardTitle: {
    color: colors.onSurface,
    fontSize: 25,
    fontWeight: "900"
  },
  infoRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: spacing.sm
  },
  infoLabel: {
    color: colors.onSurfaceVariant,
    fontSize: 15,
    fontWeight: "700",
    flex: 1
  },
  cardActions: {
    flexDirection: "row",
    gap: spacing.sm,
    alignItems: "center",
    marginTop: spacing.sm
  },
  openButton: {
    flex: 1
  },
  deleteButton: {
    width: 54,
    height: 54,
    borderRadius: 27,
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "rgba(255, 180, 171, 0.1)",
    borderWidth: 1,
    borderColor: "rgba(255, 180, 171, 0.24)"
  }
});
