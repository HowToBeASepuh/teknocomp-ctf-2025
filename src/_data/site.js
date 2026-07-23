import fs from "node:fs";

let description = "";
try {
  description = fs.readFileSync("./description.txt", "utf-8").trim();
} catch {
  description = "";
}

export default {
  title: "Teknocom 2025 CTF",
  team: "HowToBeASepuh",
  event: "TeknoCom International Competition 2025",
  institution: "Institut Teknologi Bandung",
  description,
  // Teknocom's description.txt is already in English, so reuse it in the hero.
  descriptionEn: description,
  intro:
    "TeknoCom International Competition 2025 is a fully online international competition hosted by Universitas Teknokrat Indonesia. HowToBeASepuh placed 3rd in the Cyber Security (CTF) branch — below are our write-ups for every challenge we solved.",
  repo: "https://github.com/HowToBeASepuh/teknocomp-ctf-2025",
};
