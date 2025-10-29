// Furby Songs Database
// All singing actions and musical sequences Furby can perform

const FURBY_SONGS = [
    // Octave Scale (Musical Notes)
    {
        name: "Musical Scale (Do-Re-Mi-Fa-Sol-La-Ti-Do)",
        category: "Musical Notes",
        description: "Complete octave scale from Do to Do",
        sequence: [
            { input: 71, index: 0, subindex: 0, specific: 0 },  // Do
            { input: 71, index: 0, subindex: 0, specific: 1 },  // Re
            { input: 71, index: 0, subindex: 0, specific: 2 },  // Mi
            { input: 71, index: 0, subindex: 0, specific: 3 },  // Fa
            { input: 71, index: 0, subindex: 0, specific: 4 },  // Sol
            { input: 71, index: 0, subindex: 0, specific: 5 },  // La
            { input: 71, index: 0, subindex: 0, specific: 6 },  // Ti
            { input: 71, index: 0, subindex: 0, specific: 7 },  // Do
        ],
        delay: 1.5
    },
    {
        name: "Do (Single Note)",
        category: "Musical Notes",
        description: "Single Do note",
        sequence: [{ input: 71, index: 0, subindex: 0, specific: 0 }],
        delay: 1.0
    },
    {
        name: "Re (Single Note)",
        category: "Musical Notes",
        description: "Single Re note",
        sequence: [{ input: 71, index: 0, subindex: 0, specific: 1 }],
        delay: 1.0
    },
    {
        name: "Mi (Single Note)",
        category: "Musical Notes",
        description: "Single Mi note",
        sequence: [{ input: 71, index: 0, subindex: 0, specific: 2 }],
        delay: 1.0
    },
    {
        name: "Fa (Single Note)",
        category: "Musical Notes",
        description: "Single Fa note",
        sequence: [{ input: 71, index: 0, subindex: 0, specific: 3 }],
        delay: 1.0
    },
    {
        name: "Sol (Single Note)",
        category: "Musical Notes",
        description: "Single Sol note",
        sequence: [{ input: 71, index: 0, subindex: 0, specific: 4 }],
        delay: 1.0
    },
    {
        name: "La (Single Note)",
        category: "Musical Notes",
        description: "Single La note",
        sequence: [{ input: 71, index: 0, subindex: 0, specific: 5 }],
        delay: 1.0
    },
    {
        name: "Ti (Single Note)",
        category: "Musical Notes",
        description: "Single Ti note",
        sequence: [{ input: 71, index: 0, subindex: 0, specific: 6 }],
        delay: 1.0
    },

    // Singing Category (Input 17)
    {
        name: "Boo Boo Believe In",
        category: "Songs",
        description: "Furby's signature song",
        sequence: [{ input: 17, index: 0, subindex: 0, specific: 0 }],
        delay: 1.0
    },
    {
        name: "No Lah Fever (Catch It!)",
        category: "Songs",
        description: "Energetic fever song",
        sequence: [{ input: 17, index: 0, subindex: 0, specific: 1 }],
        delay: 1.0
    },
    {
        name: "Woo! (Laughing Song)",
        category: "Songs",
        description: "Happy laughing tune",
        sequence: [{ input: 17, index: 0, subindex: 0, specific: 2 }],
        delay: 1.0
    },
    {
        name: "Wah Do Do Do Do",
        category: "Songs",
        description: "Repetitive melody",
        sequence: [{ input: 17, index: 0, subindex: 0, specific: 3 }],
        delay: 1.0
    },
    {
        name: "Check Out Kah Moves",
        category: "Songs",
        description: "Dance song with moves",
        sequence: [{ input: 17, index: 0, subindex: 0, specific: 4 }],
        delay: 1.0
    },
    {
        name: "Beatboxing",
        category: "Songs",
        description: "Furby beatbox performance",
        sequence: [{ input: 17, index: 0, subindex: 0, specific: 5 }],
        delay: 1.0
    },
    {
        name: "Kah Need This!",
        category: "Songs",
        description: "Enthusiastic song",
        sequence: [{ input: 17, index: 0, subindex: 1, specific: 1 }],
        delay: 1.0
    },
    {
        name: "This Kah Jam!",
        category: "Songs",
        description: "Party jam",
        sequence: [{ input: 17, index: 0, subindex: 1, specific: 3 }],
        delay: 1.0
    },
    {
        name: "Nyah Nee Nee",
        category: "Songs",
        description: "Playful melody",
        sequence: [{ input: 17, index: 1, subindex: 0, specific: 0 }],
        delay: 1.0
    },
    {
        name: "Too Gassy For No Lah",
        category: "Songs",
        description: "Silly song with fart",
        sequence: [{ input: 17, index: 1, subindex: 0, specific: 1 }],
        delay: 1.0
    },
    {
        name: "Stubby Legs",
        category: "Songs",
        description: "Song about stubby legs",
        sequence: [{ input: 17, index: 1, subindex: 0, specific: 2 }],
        delay: 1.0
    },
    {
        name: "Dance Magic Low",
        category: "Songs",
        description: "Magical dance song",
        sequence: [{ input: 17, index: 1, subindex: 0, specific: 3 }],
        delay: 1.0
    },
    {
        name: "Is Kah Furby or Dancer",
        category: "Songs",
        description: "Identity crisis song",
        sequence: [{ input: 17, index: 1, subindex: 0, specific: 4 }],
        delay: 1.0
    },
    {
        name: "Alright OK Uh Huh",
        category: "Songs",
        description: "Casual approval song",
        sequence: [{ input: 17, index: 2, subindex: 0, specific: 0 }],
        delay: 1.0
    },
    {
        name: "Here Go Nothing",
        category: "Songs",
        description: "Let's do this!",
        sequence: [{ input: 17, index: 2, subindex: 0, specific: 1 }],
        delay: 1.0
    },
    {
        name: "Show Kah Whatchu Got",
        category: "Songs",
        description: "Challenge song",
        sequence: [{ input: 17, index: 2, subindex: 0, specific: 2 }],
        delay: 1.0
    },
    {
        name: "Dance With Kah?",
        category: "Songs",
        description: "Dance invitation",
        sequence: [{ input: 17, index: 2, subindex: 0, specific: 3 }],
        delay: 1.0
    },
    {
        name: "Do The Furb! (Hustle)",
        category: "Songs",
        description: "Electric slide style dance",
        sequence: [{ input: 17, index: 2, subindex: 0, specific: 4 }],
        delay: 1.0
    },
    {
        name: "Pots and Pans",
        category: "Songs",
        description: "Kitchen percussion song",
        sequence: [{ input: 17, index: 3, subindex: 0, specific: 0 }],
        delay: 1.0
    },
    {
        name: "Wanna Dance?",
        category: "Songs",
        description: "Dance request",
        sequence: [{ input: 17, index: 3, subindex: 0, specific: 1 }],
        delay: 1.0
    },
    {
        name: "These Moves Though",
        category: "Songs",
        description: "Showing off dance moves",
        sequence: [{ input: 17, index: 3, subindex: 0, specific: 3 }],
        delay: 1.0
    },
    {
        name: "Furbarini",
        category: "Songs",
        description: "Exotic Furby song",
        sequence: [{ input: 17, index: 3, subindex: 0, specific: 4 }],
        delay: 1.0
    },
    {
        name: "May Kah Have This Dance",
        category: "Songs",
        description: "Polite dance request",
        sequence: [{ input: 17, index: 3, subindex: 0, specific: 5 }],
        delay: 1.0
    },
    {
        name: "Yippie!",
        category: "Songs",
        description: "Excited celebration",
        sequence: [{ input: 17, index: 3, subindex: 0, specific: 6 }],
        delay: 1.0
    },

    // Other Singing Actions
    {
        name: "Lovely Lovely Love Ly",
        category: "Songs",
        description: "Love song",
        sequence: [{ input: 1, index: 3, subindex: 0, specific: 3 }],
        delay: 1.0
    },
    {
        name: "La La La La",
        category: "Songs",
        description: "Simple singing",
        sequence: [{ input: 6, index: 3, subindex: 0, specific: 1 }],
        delay: 1.0
    },
    {
        name: "Sleep Singing",
        category: "Songs",
        description: "Sleepy lullaby",
        sequence: [{ input: 12, index: 3, subindex: 0, specific: 1 }],
        delay: 1.0
    },
    {
        name: "Musical Fart",
        category: "Silly Songs",
        description: "Fart with laugh",
        sequence: [{ input: 7, index: 0, subindex: 0, specific: 0 }],
        delay: 1.0
    },
    {
        name: "Triple Threat (Musical Fart)",
        category: "Silly Songs",
        description: "Epic musical fart",
        sequence: [{ input: 7, index: 0, subindex: 0, specific: 4 }],
        delay: 1.0
    },

    // DLC Songs (Input 75 - App Videos)
    // These songs vary based on what DLC content is installed on the Furby
    // Default DLC songs from the Furby Connect World app
    {
        name: "DLC Song 1",
        category: "DLC Songs",
        description: "App video song (requires DLC)",
        sequence: [{ input: 75, index: 0, subindex: 0, specific: 0 }],
        delay: 1.0
    },
    {
        name: "DLC Song 2",
        category: "DLC Songs",
        description: "App video song (requires DLC)",
        sequence: [{ input: 75, index: 0, subindex: 0, specific: 1 }],
        delay: 1.0
    },
    {
        name: "DLC Song 3",
        category: "DLC Songs",
        description: "App video song (requires DLC)",
        sequence: [{ input: 75, index: 0, subindex: 0, specific: 2 }],
        delay: 1.0
    },
    {
        name: "DLC Song 4",
        category: "DLC Songs",
        description: "App video song (requires DLC)",
        sequence: [{ input: 75, index: 0, subindex: 0, specific: 3 }],
        delay: 1.0
    },
    {
        name: "DLC Song 5",
        category: "DLC Songs",
        description: "App video song (requires DLC)",
        sequence: [{ input: 75, index: 0, subindex: 0, specific: 4 }],
        delay: 1.0
    },
    {
        name: "DLC Song 6",
        category: "DLC Songs",
        description: "App video song (requires DLC)",
        sequence: [{ input: 75, index: 0, subindex: 0, specific: 5 }],
        delay: 1.0
    },
    {
        name: "DLC Song 7",
        category: "DLC Songs",
        description: "App video song (requires DLC)",
        sequence: [{ input: 75, index: 0, subindex: 0, specific: 6 }],
        delay: 1.0
    },
    {
        name: "DLC Song 8",
        category: "DLC Songs",
        description: "App video song (requires DLC)",
        sequence: [{ input: 75, index: 0, subindex: 0, specific: 7 }],
        delay: 1.0
    },
    {
        name: "DLC Song 9",
        category: "DLC Songs",
        description: "App video song (requires DLC)",
        sequence: [{ input: 75, index: 0, subindex: 0, specific: 8 }],
        delay: 1.0
    },
    {
        name: "DLC Song 10",
        category: "DLC Songs",
        description: "App video song (requires DLC)",
        sequence: [{ input: 75, index: 0, subindex: 0, specific: 9 }],
        delay: 1.0
    },
    {
        name: "DLC Video 1 (Index 1)",
        category: "DLC Songs",
        description: "App video song variation (requires DLC)",
        sequence: [{ input: 75, index: 1, subindex: 0, specific: 0 }],
        delay: 1.0
    },
    {
        name: "DLC Video 2 (Index 1)",
        category: "DLC Songs",
        description: "App video song variation (requires DLC)",
        sequence: [{ input: 75, index: 1, subindex: 0, specific: 1 }],
        delay: 1.0
    },
    {
        name: "DLC Video 3 (Index 1)",
        category: "DLC Songs",
        description: "App video song variation (requires DLC)",
        sequence: [{ input: 75, index: 1, subindex: 0, specific: 2 }],
        delay: 1.0
    },
    {
        name: "DLC Video 4 (Index 1)",
        category: "DLC Songs",
        description: "App video song variation (requires DLC)",
        sequence: [{ input: 75, index: 1, subindex: 0, specific: 3 }],
        delay: 1.0
    },
    {
        name: "DLC Video 5 (Index 1)",
        category: "DLC Songs",
        description: "App video song variation (requires DLC)",
        sequence: [{ input: 75, index: 1, subindex: 0, specific: 4 }],
        delay: 1.0
    },
];

// Get all songs
function getAllSongs() {
    return FURBY_SONGS;
}

// Get songs by category
function getSongsByCategory(category) {
    if (!category) return FURBY_SONGS;
    return FURBY_SONGS.filter(song => song.category === category);
}

// Get all categories
function getSongCategories() {
    const categories = new Set(FURBY_SONGS.map(song => song.category));
    return Array.from(categories).sort();
}

// Get song by name
function getSongByName(name) {
    return FURBY_SONGS.find(song => song.name === name);
}
