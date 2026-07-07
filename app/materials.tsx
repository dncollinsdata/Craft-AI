import { MaterialIcons } from "@expo/vector-icons";
import { router } from "expo-router";
import { useMemo, useState } from "react";
import { Pressable, ScrollView, StyleSheet, Text, TextInput, View } from "react-native";

import { BottomTabs } from "@/src/components/BottomTabs";
import { CosmicBackground } from "@/src/components/CosmicBackground";
import { CosmicButton } from "@/src/components/CosmicButton";
import { GalaxyHeader } from "@/src/components/GalaxyHeader";
import { GlassPanel } from "@/src/components/GlassPanel";
import { materialSuggestions } from "@/src/data/crafts";
import { colors, radii, spacing } from "@/src/theme";

export default function MaterialsScreen() {
  const [materials, setMaterials] = useState("");
  const [selected, setSelected] = useState<string[]>(["paper", "markers"]);
  const allSelected = useMemo(() => {
    const typed = materials
      .split(",")
      .map((item) => item.trim().toLowerCase())
      .filter(Boolean);
    return Array.from(new Set([...selected, ...typed]));
  }, [materials, selected]);

  const toggleMaterial = (material: string) => {
    setSelected((current) =>
      current.includes(material) ? current.filter((item) => item !== material) : [...current, material]
    );
  };

  return (
    <CosmicBackground>
      <GalaxyHeader active="create" />
      <ScrollView contentContainerStyle={styles.content}>
        <View style={styles.intro}>
          <View style={styles.stepBadge}>
            <MaterialIcons name="rocket-launch" color={colors.primary} size={15} />
            <Text style={styles.stepBadgeText}>Step 2 of 4</Text>
          </View>
          <Text style={styles.title}>What materials do you have?</Text>
          <Text style={styles.subtitle}>Tell us what's in your crafting bin, and we'll conjure up something magical.</Text>
        </View>

        <GlassPanel style={styles.panel}>
          <View style={styles.inputHeader}>
            <Text style={styles.label}>Type Your List</Text>
            <Text style={styles.scan}>Smart Scan Active</Text>
          </View>
          <View style={styles.inputWrap}>
            <TextInput
              multiline
              value={materials}
              onChangeText={setMaterials}
              placeholder="paper, glue, markers, popsicle sticks, tape"
              placeholderTextColor="rgba(204, 195, 215, 0.42)"
              style={styles.input}
            />
            <MaterialIcons name="mic" color={colors.onSurfaceVariant} size={22} style={styles.mic} />
          </View>
          <Text style={styles.helper}>Type the things you already have at home.</Text>

          <Text style={[styles.label, styles.chipLabel]}>Popular Space Gear</Text>
          <View style={styles.chips}>
            {materialSuggestions.map((material) => {
              const active = allSelected.includes(material);
              return (
                <Pressable key={material} onPress={() => toggleMaterial(material)} style={[styles.chip, active && styles.activeChip]}>
                  <MaterialIcons name={material === "markers" ? "edit" : material === "tape" ? "layers" : "auto-awesome"} color={colors.primary} size={18} />
                  <Text style={styles.chipText}>{material}</Text>
                </Pressable>
              );
            })}
          </View>
        </GlassPanel>

        <View style={styles.preview}>
          <View style={styles.previewIcon}>
            <MaterialIcons name="shopping-basket" color="rgba(255,255,255,0.46)" size={30} />
          </View>
          <Text style={styles.previewText}>
            {allSelected.length > 0
              ? `Craft bin loaded: ${allSelected.join(", ")}.`
              : "Your craft bin is empty. Add some items to start the magic."}
          </Text>
        </View>

        <View style={styles.actions}>
          <CosmicButton variant="glass" icon="arrow-back" onPress={() => router.back()}>Go Back</CosmicButton>
          <CosmicButton icon="bolt" onPress={() => router.push("/mission")}>Next</CosmicButton>
        </View>
      </ScrollView>
      <BottomTabs active="create" />
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
  stepBadge: {
    flexDirection: "row",
    alignItems: "center",
    gap: spacing.xs,
    paddingVertical: spacing.xs,
    paddingHorizontal: spacing.md,
    borderRadius: radii.pill,
    backgroundColor: "rgba(255,255,255,0.05)",
    borderWidth: 1,
    borderColor: colors.border
  },
  stepBadgeText: {
    color: colors.primary,
    fontSize: 12,
    fontWeight: "900",
    textTransform: "uppercase"
  },
  title: {
    color: colors.onSurface,
    fontSize: 36,
    lineHeight: 42,
    fontWeight: "900",
    textAlign: "center"
  },
  subtitle: {
    color: colors.onSurfaceVariant,
    fontSize: 17,
    lineHeight: 25,
    textAlign: "center",
    fontWeight: "700"
  },
  panel: {
    padding: spacing.lg
  },
  inputHeader: {
    flexDirection: "row",
    justifyContent: "space-between",
    gap: spacing.md,
    alignItems: "flex-end"
  },
  label: {
    color: colors.primary,
    fontSize: 12,
    fontWeight: "900",
    textTransform: "uppercase",
    letterSpacing: 1
  },
  scan: {
    color: colors.onSurfaceVariant,
    opacity: 0.62,
    fontSize: 11,
    fontWeight: "900",
    textTransform: "uppercase"
  },
  inputWrap: {
    marginTop: spacing.sm
  },
  input: {
    minHeight: 132,
    borderWidth: 2,
    borderColor: colors.border,
    borderRadius: radii.sm,
    padding: spacing.md,
    paddingRight: 48,
    color: colors.onSurface,
    backgroundColor: "rgba(11, 15, 16, 0.55)",
    fontSize: 16,
    lineHeight: 23,
    textAlignVertical: "top"
  },
  mic: {
    position: "absolute",
    right: spacing.md,
    bottom: spacing.md
  },
  helper: {
    color: colors.onSurfaceVariant,
    opacity: 0.7,
    marginTop: spacing.sm,
    fontSize: 12,
    fontWeight: "700"
  },
  chipLabel: {
    marginTop: spacing.xl,
    marginBottom: spacing.md
  },
  chips: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: spacing.sm
  },
  chip: {
    flexDirection: "row",
    alignItems: "center",
    gap: spacing.xs,
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: radii.pill,
    backgroundColor: "rgba(255,255,255,0.05)",
    paddingVertical: spacing.sm,
    paddingHorizontal: spacing.md
  },
  activeChip: {
    borderColor: colors.primary,
    backgroundColor: "rgba(211, 187, 255, 0.18)"
  },
  chipText: {
    color: colors.onSurface,
    fontSize: 15,
    fontWeight: "800"
  },
  preview: {
    alignItems: "center",
    gap: spacing.sm,
    opacity: 0.78
  },
  previewIcon: {
    width: 64,
    height: 64,
    borderRadius: 32,
    borderWidth: 2,
    borderStyle: "dashed",
    borderColor: "rgba(255,255,255,0.22)",
    alignItems: "center",
    justifyContent: "center"
  },
  previewText: {
    color: colors.onSurfaceVariant,
    textAlign: "center",
    fontSize: 15,
    lineHeight: 22,
    fontWeight: "700"
  },
  actions: {
    gap: spacing.md
  }
});
