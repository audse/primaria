# TODO


## Fixes

### Github
- [x] Unarchive repo
- [x] Create gitignore
- [ ] Add screenshots
- [ ] Re-export `db.json`

### Development
- [ ] Replace `input type="hidden"` with a more secure form field method
- [x] Split up views further
- [ ] Split up models further
- [ ] Remove jQuery dependency
- [ ] Remove Remodal dependency
- [ ] Upgrade to newest Django version
- [ ] Model managers
- [x] Add search etc. to admin

### Design
- [ ] Make night mode better
- [ ] Create component library
- [ ] ...Do we need so many modals?
- [x] Fix CSS issues: sticky footer, full width, etc.
- [ ] Create logo/favicon
- [ ] Redesign user profile
- [x] Remove animal field on sidebar
- [x] Add more spacing between sections: bank, gallery, shop, etc

### Users
- [ ] Add `block user` function to settings page
- [ ] Add stats for users and pets
- [ ] Login after registration
- [ ] What happens if you try to claim your daily item, but your inventory is full?
- [ ] Banning

### Social
- [x] Mark unread messages as read upon viewing messages page
- [x] Add "Hi I'm New" avatar to list
- [ ] Add bbcode support to homepage
- [ ] Add `send message` feature to messages page
- [ ] FB-style reactions
- [x] Friends

### World
- [x] Check out vending machine problem
- [ ] Dailies checklist
- [x] Reduce cost of fishing/dowsing?
- [ ] Add hint to Restricted Area page
- [ ] Rename animals...fantasy/Pokemon names
- [x] Increase chances of getting stuff from dailies

    #### Shops
    - [x] Remove the weird price/quantity thing... just create a relationship table
    - [x] Change Alchemist shop to stock fewer items
    - [x] Make shops restock more often with fewer items
    - [x] Shop search returns both user shops and world shops results

    #### User Shops
    - [x] Switch to relational table
    - [x] Press enter to add
    - [ ] Quick stock
    - [ ] Multi-add to gallery and shops
    - [ ] No buying from your own shop

    #### Wheels
    - [ ] Make wheels stop faster
    - [ ] Change button to "stopping..."
    - [ ] Submit on change, rather then with hidden input
    - [ ] Log entry upon button press. If there is no button press, but a score submitted, then that means they're cheating. Can we calculate what the end result should be?

    #### Games
    - [x] Migrate to new app
    - [ ] Make TicTacToe AI smarter
    - [ ] Fix issues with Pyramid Solitaire
    - [ ] Implement cheating detection: log each move in a game, check that game logs match to score sent
    - [ ] Say what you got from the wheel of plush

    #### Quests
    - [ ] Upon quest completion, you don't need "check your inventory for a reward" when you receive points
    - [ ] Bonus for quick quest completion
    - [ ] `In progress` quick links identifier
    - [ ] Quests automatically cancel if you don't complete them within a day
    - [ ] Disable button if you don't have the item on hand

### Inventory
- [ ] Make inventory modal messages more specific
- [ ] More options on use item modal


## Features

### Primaria World: Domination!
Primaria: World Domination! (or PWD for short) is the collectible trading card game popular throughout Primaria. Play with other people or against an AI using the cards you've collected.

#### How To Play
- Collect cards from around the site, or buy some from `Basement Games`.
- Play against an AI or a friend in the `Games Room`.

#### TODO
- [x] Find a game designer
- [ ] Finalize ruleset
- [ ] Design interface
- [ ] Develop mechanics
- [ ] Develop AI
- [ ] Redesign admin


## Ideas

### Animal Names
- Disoar (dino)
- Scutzel (lizard)
- Trilofly (bird)
- Babone (monkey)
- Roroo (mouse)
- Snoopir (tapir)
- Clampod (crab)
- Wolup (dog)
- Garlair (gargoyle)
- Pingo (penguin)

### Features
- [ ] Bookmarks (for dailies)
- [ ] Random events
- [ ] Inventory increase
- [ ] Haggling
- [ ] User shop offers

### Items
- [ ] Coins
- [ ] Movies (Borders)

### World
- [ ] School w/ report card (suburbs)
- [ ] Personal garden
- [ ] "Petpet" farm- use petsim game mechanics? Breeding, etc.?

### Dailies
- [ ] Shrine (Outland Reservoir)
- [ ] Metal detector (Beach)

### Games
- [ ] Slot Machine, returns random keychain or coin
- [ ] Guess the weight/number
- [ ] Higher/lower

### Shops
- [ ] Hygiene
- [ ] Gemstones
- [ ] Plants/seeds/succulents
- [ ] Primaria objects: inventory upgrade, name change license, etc

### Gallery
- [ ] Send cards and plushies to PSA grading for better scores (call it PCGG? "Primaria Card Game Grading")
- [ ] Earn something from your gallery... need to think about this

### Pets
- [ ] Hyena
- [ ] Plant
- [ ] Cow/sheep
- [ ] Crocodile
- [ ] Anteater/armadillo
- [ ] Horse/donkey

### Pet Colors
- [ ] Gemstone (all 12 birthstones)
- [ ] Cartoon
- [ ] Pixel
- [ ] Pinstripe
- [ ] Wooden
- [ ] Paisley
- [ ] Tie dye
- [ ] Cupid
- [ ] Chromatic aberration
- [ ] Vampire
- [ ] Dragon
- [ ] Baby
- [ ] Electric
- [ ] Binary/ASCII?
- [ ] Fire
- [ ] Pinata
- [ ] Clown
- [ ] Patchwork (all colors)

### Avatars
- [ ] It's not easy being green (switch your pet from green to another color)
- [ ] Living like a bandit (attempt to withdraw more from the bank than your current balance)
- [ ] Lab rat (unlock 10 different colors of mouse)
- [ ] woooof (use a dog morphing potion)
- [ ] Early Adopter (given to everyone until I decide not to anymore)
- [ ] Shhhh!! (attempt to visit secrets page when not a moderator)
