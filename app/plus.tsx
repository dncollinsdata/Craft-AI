import { MaterialIcons } from "@expo/vector-icons";
import { router } from "expo-router";
import { ScrollView, StyleSheet, Text, View } from "react-native";

import { CosmicBackground } from "@/src/components/CosmicBackground";
import { CosmicButton } from "@/src/components/CosmicButton";
import { GlassPanel } from "@/src/components/GlassPanel";
import { plusBenefits } from "@/src/data/crafts";
import { colors, radii, spacing } from "@/src/theme";

export default function PlusScreen() {
  return (
    <CosmicBackground>
      <ScrollView contentContainerStyle={styles.content}>
        <View style={styles.header}>
          <View style={styles.iconHalo}>
            <MaterialIcons name="rocket-launch" color={colors.primary} size={40} />
          </View>
          <Text style={styles.title}>Unlock Galaxy Craft AI Plus</Text>
          <Text style={styles.subtitle}>Unlimited craft missions for only $2.00/month.</Text>
        </View>

        <GlassPanel style={styles.card}>
          <View style={styles.planHeader}>
            <Text style={styles.badge}>Premium Upgrade</Text>
            <Text style={styles.planName}>Galaxy Craft AI Plus</Text>
            <View style={styles.priceRow}>
              <Text style={styles.price}>$2.00</Text>
              <Text style={styles.period}>/month</Text>
            </View>
          </View>

          <View style={styles.benefits}>
            {plusBenefits.map((benefit, index) => (
              <View key={benefit} style={styles.benefitRow}>
                <View style={styles.check}>
                  <MaterialIcons
                    name={index === 2 ? "auto-fix-high" : index === 3 ? "shield" : index === 4 ? "palette" : "check"}
                    color={colors.primary}
                    size={17}
                  />
                </View>
                <Text style={styles.benefitText}>{benefit}</Text>
              </View>
            ))}
          </View>

          <View style={styles.parentNote}>
            <MaterialIcons name="family-restroom" color={colors.secondary} size={24} />
            <Text style={styles.parentText}>
              <Text style={styles.parentStrong}>Parent Note: </Text>
              Ask a grown-up before starting a subscription.
            </Text>
          </View>

          <CosmicButton icon="arrow-forward">Start for $2.00/month</CosmicButton>
          <CosmicButton variant="glass" onPress={() => router.back()}>Maybe Later</CosmicButton>
        </GlassPanel>

        <Text style={styles.footer}>Cancel anytime. Parent approval required. Secure payment processed by Space Pay.</Text>
      </ScrollView>
    </CosmicBackground>
  );
}

const styles = StyleSheet.create({
  content: {
    flexGrow: 1,
    justifyContent: "center",
    padding: spacing.lg,
    gap: spacing.lg
  },
  header: {
    alignItems: "center",
    gap: spacing.sm
  },
  iconHalo: {
    width: 78,
    height: 78,
    borderRadius: 39,
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "rgba(211, 187, 255, 0.18)",
    borderWidth: 1,
    borderColor: "rgba(211, 187, 255, 0.3)"
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
    fontSize: 18,
    lineHeight: 26,
    textAlign: "center",
    fontWeight: "700"
  },
  card: {
    padding: spacing.xl,
    gap: spacing.lg
  },
  planHeader: {
    alignItems: "center",
    gap: spacing.sm
  },
  badge: {
    color: colors.secondary,
    backgroundColor: "rgba(255, 177, 199, 0.1)",
    borderRadius: radii.pill,
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.xs,
    overflow: "hidden",
    fontSize: 12,
    fontWeight: "900",
    textTransform: "uppercase"
  },
  planName: {
    color: colors.primary,
    fontSize: 25,
    fontWeight: "900"
  },
  priceRow: {
    flexDirection: "row",
    alignItems: "flex-end"
  },
  price: {
    color: "#ffffff",
    fontSize: 42,
    fontWeight: "900"
  },
  period: {
    color: colors.onSurfaceVariant,
    fontSize: 17,
    marginBottom: 7,
    fontWeight: "700"
  },
  benefits: {
    gap: spacing.md
  },
  benefitRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: spacing.md
  },
  check: {
    width: 28,
    height: 28,
    borderRadius: 14,
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "rgba(211, 187, 255, 0.18)"
  },
  benefitText: {
    color: colors.onSurface,
    fontSize: 16,
    fontWeight: "700",
    flex: 1
  },
  parentNote: {
    flexDirection: "row",
    gap: spacing.md,
    backgroundColor: "rgba(255, 255, 255, 0.05)",
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: radii.sm,
    padding: spacing.md
  },
  parentText: {
    color: colors.onSurfaceVariant,
    flex: 1,
    fontSize: 14,
    lineHeight: 20
  },
  parentStrong: {
    color: colors.secondary,
    fontWeight: "900"
  },
  footer: {
    color: colors.onSurfaceVariant,
    textAlign: "center",
    opacity: 0.7,
    fontSize: 13,
    lineHeight: 19,
    paddingHorizontal: spacing.xl
  }
});
