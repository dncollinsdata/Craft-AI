import { describe, expect, it } from "vitest";

import {
  difficultyLevels,
  featuredMission,
  materialSuggestions,
  plusBenefits,
  savedMissions,
  welcomeFeatures
} from "./crafts";

describe("Galaxy Craft content", () => {
  it("defines the welcome feature steps", () => {
    expect(welcomeFeatures.map((feature) => feature.label)).toEqual([
      "Snap Photo",
      "AI Analysis",
      "Make Art"
    ]);
  });

  it("defines a complete featured mission", () => {
    expect(featuredMission.title).toBe("Nebula Nightlight");
    expect(featuredMission.materials).toContain("Glass Jar");
    expect(featuredMission.steps).toHaveLength(4);
    expect(featuredMission.stats.map((stat) => stat.label)).toEqual([
      "Time Needed",
      "Mess Level",
      "Difficulty",
      "Fun Level"
    ]);
    expect(featuredMission.safetyTip).toMatch(/adult/i);
    expect(featuredMission.upgradeTip).toMatch(/constellations/i);
  });

  it("includes saved missions for the saved screen", () => {
    expect(savedMissions).toHaveLength(2);
    expect(savedMissions[0]).toMatchObject({
      title: "Cosmic Cardboard Rocket",
      difficulty: "Explorer (Easy)"
    });
  });

  it("defines the plus upgrade benefits", () => {
    expect(plusBenefits).toContain("Unlimited craft ideas");
    expect(plusBenefits).toContain("Kid-safe step-by-step crafts");
    expect(plusBenefits).toHaveLength(6);
  });

  it("defines selectable craft difficulty levels", () => {
    expect(difficultyLevels.map((level) => level.id)).toEqual(["easy", "medium", "hard"]);
    expect(difficultyLevels[2]).toMatchObject({
      title: "Hard",
      description: "Bigger craft mission",
      stars: 3
    });
  });

  it("defines popular material suggestions", () => {
    expect(materialSuggestions).toEqual([
      "paper",
      "markers",
      "cardboard",
      "tape",
      "popsicle sticks"
    ]);
  });
});
