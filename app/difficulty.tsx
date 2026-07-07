import { MaterialIcons } from "@expo/vector-icons";
import { router } from "expo-router";
import { useState } from "react";
import { Pressable, ScrollView, StyleSheet, Text, View } from "react-native";

import { BottomTabs } from "@/src/components/BottomTabs";
import { CosmicBackground } from "@/src/components/CosmicBackground";
import { CosmicButton } from "@/src/components/CosmicButton";
import { GalaxyHeader } from "@/src/components/GalaxyHeader";
import { GlassPanel } from "@/src/components/GlassPanel";
import { difficultyLevels } from "@/src/data/crafts";
import { accentColor, colors, radii, spacing } from "@/src/theme";

export default function DifficultyScreen() {
  const [selected, setSelected] = useState("medium");

  return (
    <CosmicBackground>
      <GalaxyHeader active="magic" />
      <ScrollView contentContainerStyle={styles.content}>
        <View style={styles.intro}>
          <Text style={styles.title}>Choose your craft level</Text>
          <Text style={styles.subtitle}>How much of a cosmic mission are you ready for today?</Text>
        </View>

        <View style={styles.grid}>
          {difficultyLevels.map((level) => {
            const active = selected === level.id;
            const color = accentColor(level.accent);
            return (
              <Pressable key={level.id} onPress={() => setSelected(level.id)} style={({ pressed }) => [pressed && styles.pressed]}>
                <GlassPanel
                  style={[
                    styles.levelCard,
                    active ? { borderColor: color, backgroundColor: "rgba(255,255,255,0.1)" } : {}
                  ]}
                >
                  <View style={[styles.levelIcon, { backgroundColor: `${color}24` }]}>
                    <MaterialIcons name={level.icon} color={color} size={38} />
                  </View>
                  <Text style={styles.levelTitle}>{level.title}</Text>
                  <Text style={styles.levelDescription}>{level.description}</Text>
                  <View style={styles.stars}>
                    {[1, 2, 3].map((star) => (
                      <MaterialIcons
                        key={star}
                        name="star"
                        color={star <= level.stars ? color : "rgba(204, 195, 215, 0.28)"}
                        size={18}
                      />
                    ))}
                  </View>
                </GlassPanel>
              </Pressable>
            );
          })}
        </View>

        <CosmicButton icon="auto-fix-high" onPress={() => router.push("/materials")} style={styles.action}>
          Make My Craft
        </CosmicButton>
      </ScrollView>
      <BottomTabs active="magic" />
    </CosmicBackground>
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
    fontSize: 36,
    lineHeight: 42,
    fontWeight: "900",
    textAlign: "center"
  },
  subtitle: {
    color: colors.onSurfaceVariant,
    fontSize: 18,
    lineHeight: 26,
    textAlign: "center",
    fontWeight: "700"
  },
  grid: {
    gap: spacing.md
  },
  levelCard: {
    padding: spacing.xl,
    alignItems: "center",
    gap: spacing.sm
  },
  levelIcon: {
    width: 82,
    height: 82,
    borderRadius: 41,
    alignItems: "center",
    justifyContent: "center",
    marginBottom: spacing.sm
  },
  levelTitle: {
    color: colors.onSurface,
    fontSize: 25,
    fontWeight: "900"
  },
  levelDescription: {
    color: colors.onSurfaceVariant,
    fontSize: 16,
    fontWeight: "700"
  },
  stars: {
    flexDirection: "row",
    gap: 2,
    marginTop: spacing.sm
  },
  action: {
    marginTop: spacing.md
  },
  pressed: {
    transform: [{ scale: 0.98 }]
  }
});
