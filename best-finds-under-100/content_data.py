"""Original content pools used by the template-based (demo mode) generators.

All copy here is original — nothing is scraped or copied from retailers.
Products are stored as concepts + search terms, never exact URLs, so the
system works before any affiliate accounts exist.
"""

# Each concept: (name, price_lo, price_hi, why_people_care, problem_solved, target_audience)
PRODUCT_POOL = {
    "Home finds": [
        ("Motion sensor under-cabinet lights", 20, 40, "Instant high-end kitchen glow with zero wiring", "Dark counters and fumbling for switches at night", "Renters and homeowners who want an easy upgrade"),
        ("Peel-and-stick marble contact paper", 15, 30, "A counter or shelf makeover for the price of lunch", "Dated surfaces you can't renovate in a rental", "Renters who want a designer look without commitment"),
        ("Sunset projection lamp", 18, 35, "Turns any wall into golden-hour lighting for photos and mood", "Flat, boring overhead lighting", "Anyone who wants cozy ambiance on a budget"),
        ("Slim rolling storage cart", 25, 45, "Uses the dead space between appliances people forget exists", "No storage in small kitchens and bathrooms", "Small-space dwellers"),
        ("Cordless rechargeable lamp", 30, 60, "Puts light anywhere without an outlet or electrician", "Rooms with terrible outlet placement", "Renters and dorm dwellers"),
        ("Weighted draft stopper", 12, 25, "Blocks cold air and hallway noise instantly", "Drafty doors that leak heat and sound", "Apartment dwellers with noisy hallways"),
        ("Glass spray bottles with labels set", 15, 28, "Makes cleaning supplies look intentional instead of cluttered", "A messy jumble of plastic bottles under the sink", "Organization lovers"),
        ("Doorway over-the-door mirror", 25, 50, "A full-length mirror with zero drilling", "No wall space or landlord rules against mounting", "Renters"),
        ("Smart LED light strip", 20, 45, "Color-changing accent lighting controlled from your phone", "Flat lighting that makes rooms feel lifeless", "Anyone upgrading a bedroom or TV wall"),
        ("Automatic soap dispenser", 18, 35, "Touch-free soap feels like a hotel bathroom", "Grimy soap pumps everyone touches", "Households that want cleaner countertops"),
    ],
    "Apartment upgrades": [
        ("Removable wallpaper panels", 25, 60, "A statement wall you can take down when you move out", "Plain white rental walls", "Renters who want personality without losing a deposit"),
        ("Curtain room divider kit", 30, 60, "Creates a bedroom or office zone in a studio", "One room that has to be everything", "Studio apartment dwellers"),
        ("Rechargeable picture lights", 20, 40, "Gallery-style art lighting with no wiring", "Art that disappears into a dark wall", "Renters who love a gallery wall"),
        ("Faucet swivel aerator", 10, 20, "Turns a basic faucet into a flexible spray head", "Splashy, rigid kitchen faucets", "Anyone with a builder-grade kitchen"),
        ("Adhesive shower shelf set", 15, 30, "Doubles shower storage with zero drilling", "Bottles crowding the shower floor", "Renters with tiny bathrooms"),
        ("Peel-and-stick backsplash tiles", 25, 50, "A kitchen facelift you can do in an afternoon", "Ugly or plain backsplashes you can't retile", "Renters and first-time buyers"),
        ("Dimmer smart plug", 15, 25, "Adds dimming to any lamp for instant mood control", "Harsh all-or-nothing lamp lighting", "Anyone building a cozy setup"),
        ("Door draft and soundproofing seal kit", 12, 25, "Cuts hallway noise dramatically for a few dollars", "Thin apartment doors that let in every sound", "Light sleepers in apartments"),
        ("Floating headboard cushion", 40, 80, "A real headboard look that mounts with straps, not bolts", "Beds that look unfinished against a bare wall", "Renters upgrading a bedroom"),
        ("Cable management raceway kit", 12, 25, "Hides TV and desk cables inside paintable channels", "Cable spaghetti ruining a clean wall", "Anyone with a wall-mounted TV"),
    ],
    "Tech accessories": [
        ("3-in-1 foldable charging station", 25, 55, "One tidy pad charges phone, watch, and earbuds", "A nightstand covered in cables", "Apple and Android ecosystem users"),
        ("Phone camera lens kit", 20, 45, "Macro and wide-angle shots straight from a phone", "Phone cameras that can't get creative shots", "Content creators on a budget"),
        ("Magnetic power bank", 25, 50, "Snap-on battery that charges while you scroll", "Dead phone anxiety with no cables around", "Commuters and travelers"),
        ("Mini capsule projector", 60, 100, "A movie wall in any room or backyard", "Small TVs and expensive home theaters", "Movie fans and renters"),
        ("Smart tracker tag 4-pack", 20, 40, "Never lose keys, wallets, or luggage again", "The daily hunt for lost essentials", "Forgetful people and travelers"),
        ("Laptop privacy screen filter", 20, 40, "Work in public without shoulder-surfers", "Screens visible to everyone at a cafe", "Remote workers"),
        ("USB-C multiport hub", 20, 45, "Restores every port your slim laptop dropped", "One-port laptops that can't connect anything", "Laptop users"),
        ("Bluetooth audio transmitter for TV", 20, 40, "Late-night TV through headphones without waking anyone", "Thin-wall living with a loud TV", "Apartment dwellers and parents"),
        ("E-reader style paper screen protector", 12, 25, "Makes writing on a tablet feel like real paper", "Slippery glass that's awkward to draw on", "Note-takers and digital artists"),
        ("Webcam light ring with mount", 18, 35, "Instantly better lighting on every video call", "Dark, unflattering webcam video", "Remote workers and streamers"),
    ],
    "Car gadgets": [
        ("Headrest hook set", 8, 15, "Keeps bags off the dirty floorboard", "Groceries rolling around the back seat", "Commuters and parents"),
        ("Magnetic phone mount", 12, 25, "One-hand phone docking that actually holds", "Phones sliding around while navigating", "Anyone who drives with GPS"),
        ("Car seat gap organizer", 15, 30, "Ends the black hole between seat and console", "Phones and fries vanishing into the seat gap", "Every driver alive"),
        ("Cordless handheld car vacuum", 25, 55, "Detail-level clean without the car wash line", "Crumbs and sand that never leave the carpet", "Parents and pet owners"),
        ("LED interior light strips", 15, 30, "Ambient footwell lighting that upgrades any interior", "Dark, dated car interiors", "Younger drivers who love a glow-up"),
        ("Windshield sun shade umbrella", 20, 35, "Folds like an umbrella, cools the whole cabin", "Steering wheels too hot to touch", "Drivers in hot climates"),
        ("Tire pressure gauge with inflator", 30, 60, "Tops off tires at home in minutes", "Gas station air pumps that eat quarters", "Anyone who drives"),
        ("Trunk collapsible organizer", 20, 40, "Groceries stay upright, trunk stays tidy", "Rolling bottles and crushed bags in the trunk", "Grocery shoppers and road trippers"),
        ("Dash camera compact", 40, 90, "A silent witness that protects you in disputes", "He-said-she-said after a fender bender", "Daily drivers"),
        ("Car trash can with lid", 10, 20, "A real lidded bin instead of a sad plastic bag", "Wrappers collecting in the door pockets", "Commuters"),
    ],
    "Pet products": [
        ("Slow feeder dog bowl", 10, 25, "Turns speed-eating into a puzzle game", "Dogs inhaling food and getting sick", "Dog owners"),
        ("Automatic cat laser toy", 15, 35, "Keeps cats hunting while you work", "Bored cats destroying furniture", "Busy cat owners"),
        ("Pet hair remover roller", 15, 25, "Pulls fur off couches with no refills ever", "Furniture wearing a coat of pet hair", "Anyone with a shedding pet"),
        ("Dog paw cleaner cup", 12, 25, "Muddy paws cleaned before they hit the floor", "Paw prints across clean floors", "Dog owners in rainy places"),
        ("Cat window hammock", 15, 30, "A sunny lookout perch cats actually use", "Cats crowding your keyboard for window views", "Cat owners"),
        ("Pet water fountain", 20, 40, "Flowing water that gets pets drinking more", "Pets ignoring stale water bowls", "Cat and small-dog owners"),
        ("No-pull dog harness", 15, 35, "Walks that don't feel like water skiing", "Dogs dragging their owners down the block", "Owners of strong pullers"),
        ("Interactive treat puzzle", 12, 30, "Mental exercise that tires pets out", "Destructive boredom when home alone", "Owners of high-energy pets"),
        ("Pet camera with treat toss", 40, 90, "Check in and toss a treat from anywhere", "Guilt and worry while away at work", "Pet parents who work away from home"),
        ("Grooming glove set", 10, 20, "Petting that doubles as de-shedding", "Brushes pets run away from", "Owners of brush-hating pets"),
    ],
    "Travel essentials": [
        ("Compression packing cubes", 20, 40, "Fits a week of clothes in a carry-on", "Overstuffed luggage and checked-bag fees", "Carry-on-only travelers"),
        ("Portable luggage scale", 10, 20, "Know your bag's weight before the counter does", "Surprise overweight fees at check-in", "Frequent flyers"),
        ("Universal travel adapter", 15, 30, "One plug that works in 150+ countries", "A drawer of single-country adapters", "International travelers"),
        ("Trtl-style neck support pillow", 30, 60, "Actual neck support that fits in a pocket", "Waking up mid-flight with a wrecked neck", "Long-haul flyers"),
        ("Toiletry hanging kit bag", 15, 35, "A whole bathroom shelf that hangs on any hook", "No counter space in hotel bathrooms", "Anyone who travels"),
        ("Portable door lock", 10, 20, "Extra hotel-room security in seconds", "Sketchy locks in unfamiliar rooms", "Solo travelers"),
        ("Collapsible water bottle", 12, 25, "Full-size hydration that flattens when empty", "Bulky bottles taking up bag space", "Hikers and flyers"),
        ("Anti-theft crossbody sling", 25, 50, "Essentials stay zipped against your body", "Pickpockets in crowded tourist spots", "City travelers"),
        ("Power bank with built-in cables", 25, 45, "Charging with zero cables to forget", "Dead devices and missing cords mid-trip", "Every traveler"),
        ("Packable duffel bag", 15, 35, "An extra bag that hides inside your suitcase", "Souvenirs that don't fit on the way home", "Overpackers and shoppers"),
    ],
    "Gift ideas": [
        ("Custom star map print kit", 25, 50, "The night sky from a date that matters", "Gifts that feel generic and forgettable", "Couples and sentimental gifters"),
        ("Smart mug warmer", 15, 30, "Coffee stays hot through every meeting", "Cold coffee abandoned on a desk", "Coffee-drinking desk workers"),
        ("Digital photo frame", 40, 80, "Family photos that update from anywhere", "Grandparents missing everyday moments", "Families living apart"),
        ("Mini waffle maker", 12, 25, "Single waffles with zero cleanup drama", "Breakfast boredom in small kitchens", "Students and brunch lovers"),
        ("Heated eye massager", 40, 90, "Spa-level relief after screen-heavy days", "Tired, strained eyes from screens", "Anyone glued to a monitor"),
        ("Whiskey smoker kit", 25, 50, "Cocktail-bar theatrics at home", "Home drinks that feel ordinary", "Cocktail enthusiasts"),
        ("Sherpa wearable blanket", 25, 45, "A blanket you never have to put down", "Choosing between cozy and functional", "Homebodies"),
        ("Instant print camera", 60, 100, "Photos you can hold, straight from the party", "Phone photos nobody ever looks at again", "Teens and party hosts"),
        ("Sunrise alarm clock", 25, 50, "Waking up to light instead of alarm panic", "Brutal dark-morning wakeups", "Anyone who hates their alarm"),
        ("Self-heating coffee tumbler", 30, 60, "Temperature-controlled sips for hours", "Lukewarm coffee on long commutes", "Commuters"),
    ],
    "Desk setup": [
        ("Monitor stand with drawer", 20, 40, "Lifts the screen and hides the clutter", "Neck strain and desk mess in one", "Remote workers"),
        ("Under-desk cable tray", 15, 30, "Every cable vanishes under the desk", "A visible nest of power strips and cords", "Clean-setup lovers"),
        ("Desk pad extended mat", 15, 35, "One clean surface that ties the setup together", "Scratched desks and mismatched mousepads", "Anyone with a desk"),
        ("Laptop stand ergonomic", 20, 45, "Eye-level screen, cooler laptop, better posture", "Hunching over a laptop for hours", "Laptop workers"),
        ("Mechanical keyboard budget", 40, 80, "The typing feel everyone raves about, affordably", "Mushy laptop keys all day", "Typists and gamers"),
        ("Desk shelf riser system", 30, 60, "A second level that doubles usable desk space", "No room for monitor, notes, and coffee", "Small-desk owners"),
        ("Anti-fatigue standing mat", 25, 50, "Makes standing desks actually usable", "Aching feet ending standing sessions early", "Standing desk users"),
        ("Clip-on desk lamp with color modes", 18, 35, "Warm-to-cool light without desk footprint", "Harsh room light and zero desk space", "Late-night workers"),
        ("Headphone hook with USB hub", 12, 25, "Headphones stored, ports added, desk cleared", "Headphones flung on the desk daily", "Anyone with headphones"),
        ("Footrest under-desk", 20, 40, "The posture fix nobody knows they need", "Dangling feet and lower-back fatigue", "Shorter desk workers"),
    ],
    "Kitchen gadgets": [
        ("Rapid electric egg cooker", 15, 25, "Perfect eggs with a button press", "Ruined eggs and dirty pans every morning", "Busy breakfast people"),
        ("Vegetable chopper with containers", 20, 40, "Meal-prep chopping in one press", "Slow, tearful knife work every dinner", "Meal preppers"),
        ("Cold brew maker pitcher", 15, 30, "Cafe-priced cold brew for pennies a glass", "Five-dollar daily coffee runs", "Iced coffee fans"),
        ("Silicone stretch lid set", 10, 20, "Reusable lids that fit any bowl", "Cling wrap that never cooperates", "Leftover savers"),
        ("Electric milk frother wand", 10, 20, "Coffee-shop foam in fifteen seconds", "Flat lattes at home", "Home baristas"),
        ("Adjustable rolling pin with rings", 15, 25, "Even dough thickness every single time", "Lopsided cookies and uneven crusts", "Home bakers"),
        ("Magnetic knife strip", 15, 30, "Knives on display, counter space back", "Bulky knife blocks hogging counters", "Small-kitchen cooks"),
        ("Air fryer silicone liners", 10, 18, "Air fryer cleanup drops to zero", "Scrubbing baskets after every batch", "Air fryer owners"),
        ("Digital food scale", 12, 25, "Baking accuracy and portion control in one", "Recipes that flop from eyeballed measures", "Bakers and macro trackers"),
        ("Over-sink dish drying rack", 30, 60, "A whole drying station floating over the sink", "Dish racks eating half the counter", "Small-kitchen households"),
    ],
    "Fitness accessories": [
        ("Resistance bands set with handles", 20, 40, "A full gym that fits in a drawer", "No space or budget for equipment", "Home workout beginners"),
        ("Massage gun compact", 40, 90, "Recovery-day relief without a masseuse", "Sore muscles that slow training", "Regular exercisers"),
        ("Adjustable jump rope weighted", 15, 30, "Cardio that torches calories in ten minutes", "Boring cardio routines", "Busy people"),
        ("Yoga mat thick non-slip", 20, 40, "Joint-friendly cushioning that stays put", "Sliding mats and bruised knees", "Yoga and floor-workout fans"),
        ("Grip strengthener set", 10, 20, "Train forearms while watching TV", "Weak grip limiting lifts", "Lifters and climbers"),
        ("Core sliders discs", 10, 18, "Planks that suddenly work everything", "Plateaued ab routines", "Home core trainers"),
        ("Ankle weights adjustable pair", 15, 30, "Turns walks into workouts", "Easy workouts that stopped delivering", "Walkers and pilates fans"),
        ("Foam roller textured", 15, 35, "Deep-tissue release before and after workouts", "Tight muscles that never loosen", "Runners and lifters"),
        ("Push-up board system", 20, 40, "Color-coded targeting for every chest angle", "Push-ups that stopped progressing", "Home strength trainers"),
        ("Under-desk pedal exerciser", 30, 60, "Burn calories during meetings", "Sitting motionless for eight hours", "Desk workers"),
    ],
}

# Punchy but honest hook templates. {name} product, {cat} category word, {hi} top price, {problem} problem.
HOOK_TEMPLATES = [
    "This {name_lower} might be the smartest thing under ${hi} right now",
    "Your {cat_space} is missing this and it costs less than ${hi}",
    "Stop scrolling if {problem_lower}",
    "POV: you finally found the {name_lower} everyone keeps talking about",
    "Nobody talks about this ${lo}-${hi} {cat_lower} upgrade",
    "3 seconds to show you why this {name_lower} is worth every dollar",
    "If {problem_lower}, watch this",
    "The under-${hi} find that makes your {cat_space} look expensive",
    "I ranked this #1 in {cat_lower} finds under $100 — here's why",
    "This is your sign to fix {problem_lower} for under ${hi}",
]

CATEGORY_SPACE = {
    "Home finds": "home",
    "Apartment upgrades": "apartment",
    "Tech accessories": "tech setup",
    "Car gadgets": "car",
    "Pet products": "pet's routine",
    "Travel essentials": "travel bag",
    "Gift ideas": "gift list",
    "Desk setup": "desk",
    "Kitchen gadgets": "kitchen",
    "Fitness accessories": "workout routine",
}

CATEGORY_HASHTAGS = {
    "Home finds": ["#homefinds", "#homedecor", "#homehacks"],
    "Apartment upgrades": ["#apartmenttherapy", "#rentalfriendly", "#apartmentfinds"],
    "Tech accessories": ["#techfinds", "#techtok", "#gadgets"],
    "Car gadgets": ["#cargadgets", "#carhacks", "#caraccessories"],
    "Pet products": ["#petfinds", "#pettok", "#dogsoftiktok"],
    "Travel essentials": ["#travelfinds", "#travelhacks", "#packwithme"],
    "Gift ideas": ["#giftideas", "#giftguide", "#giftsforher"],
    "Desk setup": ["#desksetup", "#deskgoals", "#workfromhome"],
    "Kitchen gadgets": ["#kitchengadgets", "#kitchenfinds", "#cookinghacks"],
    "Fitness accessories": ["#fitnessfinds", "#homeworkout", "#gymtok"],
}

GENERIC_HASHTAGS = ["#under100", "#budgetfinds", "#producttok", "#musthaves"]

VIDEO_ANGLES = [
    "{category} that make your {space} look expensive",
    "Under-$100 {category_lower} you didn't know you needed",
    "{category} worth buying before they blow up",
    "The {category_lower} upgrade everyone asks about",
    "Small-budget, big-difference {category_lower}",
]

BACKGROUND_STYLES = [
    "Clean bright countertop with soft natural window light",
    "Cozy warm-lit room with blurred fairy lights in the background",
    "Minimal neutral tabletop with a single plant for depth",
    "Modern apartment corner with soft daylight and neutral tones",
    "Dark moody surface with a single warm key light on the product",
]

EDITING_STYLES = [
    "Fast-cut showcase: 1-2 second clips, punch-in zooms on key features",
    "Smooth cinematic: slow push-ins, match cuts between angles",
    "Satisfying ASMR-style: close-ups, natural sound emphasized",
    "Before/after transformation: problem shot, whip-pan, solution shot",
    "List countdown: numbered on-screen text, quick transitions per item",
]

MUSIC_MOODS = [
    "Upbeat lo-fi with a light percussive bounce",
    "Trending minimal house beat, low intensity",
    "Warm acoustic chill, cozy and unhurried",
    "Clean electronic pulse that builds to the reveal",
    "Soft jazzy background that keeps voiceover front and center",
]

PACING_OPTIONS = [
    "Fast: new visual every 1-2 seconds, hook resolved by second 3",
    "Medium: 2-3 second scenes with one slow reveal moment",
    "Relaxed: 3-4 second scenes, let the visuals breathe",
]

CTA_OPTIONS = [
    "Follow for a new under-$100 find every day.",
    "Save this so you don't forget it exists.",
    "Send this to someone whose {space} needs it.",
    "Comment the category you want covered next.",
    "Follow — tomorrow's find is even better.",
]

PLACEHOLDER_LINK_TEMPLATES = [
    # (label, url_template) — plain search links, no scraping, no affiliate params.
    ("Google Shopping search", "https://www.google.com/search?tbm=shop&q={q}"),
    ("Amazon search", "https://www.amazon.com/s?k={q}"),
]
