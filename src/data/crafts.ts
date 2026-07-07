export type IconName =
  | "add-a-photo"
  | "arrow-back"
  | "arrow-forward"
  | "auto-awesome"
  | "auto-fix-high"
  | "auto-stories"
  | "bolt"
  | "celebration"
  | "check"
  | "cleaning-services"
  | "delete"
  | "draw"
  | "edit"
  | "explore"
  | "family-restroom"
  | "horizontal-rule"
  | "inventory-2"
  | "landscape"
  | "layers"
  | "memory"
  | "mic"
  | "palette"
  | "photo-camera"
  | "rocket-launch"
  | "schedule"
  | "sentiment-very-satisfied"
  | "shield"
  | "shopping-basket"
  | "star";

export type WelcomeFeature = {
  label: string;
  icon: IconName;
  accent: "primary" | "secondary" | "tertiary";
};

export type MissionStat = {
  label: string;
  value: string;
  icon: IconName;
  accent: "primary" | "secondary" | "tertiary";
};

export type CraftMission = {
  title: string;
  subtitle: string;
  imageUrl: string;
  materials: string[];
  steps: string[];
  stats: MissionStat[];
  safetyTip: string;
  upgradeTip: string;
};

export type SavedMission = {
  title: string;
  badge: string;
  imageUrl: string;
  difficulty: string;
  time: string;
  materials: string;
};

export type DifficultyLevel = {
  id: "easy" | "medium" | "hard";
  title: string;
  description: string;
  icon: IconName;
  accent: "primary" | "secondary" | "tertiary";
  stars: 1 | 2 | 3;
};

export const welcomeFeatures: WelcomeFeature[] = [
  { label: "Snap Photo", icon: "photo-camera", accent: "primary" },
  { label: "AI Analysis", icon: "memory", accent: "secondary" },
  { label: "Make Art", icon: "celebration", accent: "tertiary" }
];

export const featuredMission: CraftMission = {
  title: "Nebula Nightlight",
  subtitle: "Capture a piece of the cosmic sky in a jar to light up your spaceship at night.",
  imageUrl:
    "https://lh3.googleusercontent.com/aida-public/AB6AXuDxDf5-t-CJ1f0zK9wbSPNArES8RHRv_b6s6kbZporS1jeWxvRyXH3OCkB8Ovs9wnWKBQl8iPwNRzPUrxBpabLIzRu-tRINOjBgq_DlxFCM1MrtYywlvABKDTfFeQnllWht2Ex4coXSowICO5jcFsBK37PgE9l9UUtvN0zhI4YKPCi0JpHv-6mX_dh-VtIIhHSjGEEca8jeyoRZUaePxTgKWRnI2ilzRo5SnafjOOzzR91N_AEa9VWMq_xWQRwykWtniIsoMZW3h_s",
  materials: ["Glass Jar", "Cotton Wool", "Glitter", "Food Coloring", "LED Tea Light"],
  steps: [
    "Fill one third of your jar with water and add two drops of food coloring.",
    "Pull apart cotton wool balls and tuck them into the colored water.",
    "Sprinkle plenty of stardust glitter on top of the wool.",
    "Repeat layers until full, then place the LED light inside the lid."
  ],
  stats: [
    { label: "Time Needed", value: "25 Mins", icon: "schedule", accent: "primary" },
    { label: "Mess Level", value: "Low Space-Dust", icon: "cleaning-services", accent: "secondary" },
    { label: "Difficulty", value: "Junior Pilot", icon: "star", accent: "tertiary" },
    { label: "Fun Level", value: "Maximum", icon: "sentiment-very-satisfied", accent: "primary" }
  ],
  safetyTip:
    "Ask an adult to help if your glass jar is heavy or if you need to secure the lid with glue.",
  upgradeTip:
    "Add tiny plastic star beads inside the cotton wool to create hidden constellations."
};

export const savedMissions: SavedMission[] = [
  {
    title: "Cosmic Cardboard Rocket",
    badge: "Mission Active",
    imageUrl:
      "https://lh3.googleusercontent.com/aida-public/AB6AXuCC5ozEEQdlX86CcBhaulVpsD_BVT41r8qU6R1hGy-rGyN3XlEI1aVn6njmaqix_u7lN63nqk9CeSCrQeWzeoTmADXWz0yNxZk7-NVWSF-6taCwZN4Rl2k1QXE8dI80mUiiZwtjWhi7VXcafeT8UZQgLNMw7vNXmOdMNCMnhmAnvFDIMusTKGjfDACghZvUVxVFltm7JGVjDcNpa56Vz66l999KfhXliml7FxJ8nW9X4ZRIL6FBzckrMij5ETRtJwt9HDS5BJQREiE",
    difficulty: "Explorer (Easy)",
    time: "45 Minutes",
    materials: "Boxes, Tape, Markers"
  },
  {
    title: "Nebula Cloud Jar",
    badge: "Stardust Series",
    imageUrl:
      "https://lh3.googleusercontent.com/aida-public/AB6AXuBYq4Bi79cKWW8pwVoSbI-DQVrzyQWVGvk9EGiG22zys9ctj2oCV84W-YSdGNqqiJ31bffbflMhlpwfFhRfz_QVQe47PKJP0vv1n3JfiH9TXO5LiAyBHTsnYVH8p3TrfK7Wt9HlePubBU-P_QE6SvRbjwzRGl2262X-FPZs_hn4YkDDi-0eCO3-TVZtufERdVywbEvQW8DopfUxwIPdb3UxtvMvv7oKaE4cRMVhAMLIFITszScU3qqzb3lR8nIxmbgBkYLe7uQRzo4",
    difficulty: "Voyager (Medium)",
    time: "30 Minutes",
    materials: "Jar, Cotton, Glitter"
  }
];

export const plusBenefits = [
  "Unlimited craft ideas",
  "Save more craft missions",
  "Make It Cooler upgrades",
  "Kid-safe step-by-step crafts",
  "New craft themes",
  "More creative craft missions"
];

export const difficultyLevels: DifficultyLevel[] = [
  {
    id: "easy",
    title: "Easy",
    description: "Quick and simple",
    icon: "rocket-launch",
    accent: "primary",
    stars: 1
  },
  {
    id: "medium",
    title: "Medium",
    description: "More creative",
    icon: "landscape",
    accent: "secondary",
    stars: 2
  },
  {
    id: "hard",
    title: "Hard",
    description: "Bigger craft mission",
    icon: "auto-awesome",
    accent: "tertiary",
    stars: 3
  }
];

export const materialSuggestions = ["paper", "markers", "cardboard", "tape", "popsicle sticks"];
