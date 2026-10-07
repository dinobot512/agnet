# Bronze Age trade: rules

A swarm of independent ship captains trading across the Late Bronze Age Mediterranean (~1400–1200 BCE). There is no central market and no shared news: **information travels only on ships.** A captain knows what it has seen, plus what other captains told it in a port tavern.

What this game is meant to show:
- How information spreads, gets distorted, or gets hoarded
- Whether captains cooperate, form networks or mislead each other
- How a swarm of cheap agents finds (or misses) good trade routes

---

## 1. Captains

- **10 captains** (configurable), each with **one ship** and working only for itself. A small fleet keeps information scarce: with 50 ships every port was crowded with news.
- **Goal:** end the game with as much **silver** as possible. Cargo still aboard at the end is valued at the last prices that captain saw.
- **Starting position:** each captain starts in its **home port** with **100 shekels of silver** and an empty hold.
- **Ship:** carries **40 units** of cargo and sails about **60 nautical miles per day**.
- **Provisions:** a crew costs **1 shekel per day**, whether at sea or in port.
- **Harbor dues:** every arrival in a port costs **2 shekels** (except the very first, at home on day 0).
- **Stranded:** a captain with no silver and no cargo is stranded and leaves the game.

### 1.1 Names and personas
Each captain has a **home port**, a **name** from that culture, and a **persona**: a speech style and a few catchphrases from its place and time. Where possible, names are real ones from Bronze Age records. Captains are spread across the home ports; when names repeat they get a numeral (e.g. *Ahmose II*).

| Home | Example names | Speech style |
|---|---|---|
| **Avaris** (Egypt) | Nebamun, Tiye, Ahmose, Meritamun | Formal and flowery; swears "by Amun!"; calls foreigners "the people of the sand"; mentions Pharaoh constantly |
| **Byblos** | Rib-Hadda, Ahiram, Zakar-Baal | Complains endlessly and begs for help, like the real King Rib-Hadda's many letters to Pharaoh |
| **Ugarit** | Urtenu, Sinaranu, Yabninu | Shrewd haggler; "by Baal!"; everything has a price. Urtenu and Sinaranu were real Ugarit merchants. |
| **Enkomi** (Cyprus) | Kushmeshusha, Eshuwara | Boasts about copper and the island; "by the copper of Alashiya!" |
| **Mycenae** | Alexandra, Eumedes, Amphiaraos | Epic-poetry style: "the wine-dark sea", "swift ships", honour and glory |
| **Knossos** (Crete) | Minos, Rhadamanthys, Pasiphae | Old sea-power nostalgia for the days when Crete ruled the waves; bull references |
| **Miletus** (Hittite coast) | Piyamaradu, Tawagalawa, Mursili | Legalistic: "as the treaty states…". Piyamaradu was a real troublemaker on that coast. |
| **Sardinia** | Shardana sailors | Terse warrior-sailors from the edge of the known world |
| **Rhodes** | Mycenaean Greek names | Like Mycenae, with an islander's eye for passing ships |

Personas shape how captains **talk**, not what they want: every captain has the same goal. Personality traits such as caution or honesty are planned for later (§7).

## 2. Time

There are no turns. The world runs on a **calendar of days** (default 120). Each captain experiences the game as a series of **wake-ups**. It is awake only when it is in a port.

## 3. The voyage cycle

Every captain is always in one of three states:

```
            ┌──────────── set sail ─────────────┐
            │                                    ▼
      ┌──────────┐                         ┌──────────┐
      │  AWAKE   │ ◀──────── arrive ────── │  AT SEA  │
      │ in port  │                         │ (asleep) │
      └──────────┘                         └──────────┘
          │   ▲
     wait │   │ another ship arrives, or
          ▼   │ the waiting deadline passes
      ┌──────────┐
      │ WAITING  │
      │ in port  │
      │ (asleep) │
      └──────────┘
```

### 3.1 At sea (asleep)
- When a captain sets sail, it is told **exactly when it will arrive** and that **it will not be woken until then**.
- At sea it can do nothing and learns nothing: no news, no trading, no changes of course.
- The world moves on without it. Prices change, other captains come and go, and taverns fill with talk it won't hear.

### 3.2 Arriving (woken)
On arrival the captain wakes up and gets a **port briefing**:

| Briefing section | Contents |
|---|---|
| **Date and place** | Today's date and which port this is |
| **Market** | The price at which this port buys and sells each good today, and how much it has in stock |
| **Your ship** | Silver, cargo, free space, and provisions cost |
| **Captains in port** | Who else is here right now |
| **Barkeep** | The most recent things said in this port's tavern by earlier visitors, with dates and speakers |
| **Your logbook** | The prices *you yourself* have seen at every port, with the date you saw them. Recorded automatically, so it can be out of date. |
| **Your notes** | Notes you've written to yourself |
| **Sailing times** | How many days it takes to reach each other port from here |

### 3.3 What happens when a ship arrives

Everything happens on the arrival day, in this order:

| Step | Who | What |
|---|---|---|
| **1. Briefing** | The newcomer | Gets the full port briefing (§3.2): barkeep's log, market, captains in port, logbook, notes, sailing times. |
| **2. First trade** | The newcomer | **Trades before anyone else**: buy and sell any goods, several trades allowed. The captains waiting in port are still asleep. |
| **3. Wake-up** | Captains waiting in port | Woken by the arrival. Each gets a fresh briefing, with prices as they are **after** the newcomer's trades. |
| **4. Tavern** | Everyone present | **2 rounds of talk.** Each round, every captain may say one thing or stay silent. Everything said is heard by everyone present and recorded by the barkeep (§5). |
| **5. Final decisions** | Everyone, newcomer included, in random order | Trade again (the talk may have changed plans), write notes, then **set sail** or **wait**. |

- **Several ships arriving the same day:** they take step 2 one after another in random order, then everyone continues together from step 3.
- **Arriving at an empty port:** there's nobody to wake or talk to, so steps 2 and 5 become a single decision: trade, then set sail or wait.
- **Waiting captains can always trade in step 5.** It won't help much if the newcomer just sold the same cargo, but it may if they hold something different or want what the newcomer brought.
- **Talking, trading and writing notes take no time.** Only sailing and waiting move a captain's clock forward.

### 3.4 Leaving or waiting
Every wake-up ends with one of:
- **Set sail to a port.** The captain is told its arrival date and sleeps until then (§3.1).
- **Wait in port for up to N days.** The captain sleeps until either:
  - **another ship arrives:** it's woken at step 3 of that arrival, after the newcomer's first trade; or
  - **its deadline passes** with no arrival: it's woken alone, gets a fresh briefing, and decides again (trade, sail or wait).

**Ships that leave are gone.** A captain that sails away misses anything said after it left, even on the same day.

### 3.5 Waiting in port for better prices
Captains may wait in port as long as they like, for example for copper to pile up at Enkomi, or for a glutted market to recover. It's allowed, and real merchants did it, but it's a gamble:
- **Newcomers trade first.** Any ship that arrives while you wait gets first pick of the stock you were waiting for, or sells its cargo before you sell yours.
- **The payoff is limited.** Prices stay between 0.4× and 2.5× base, and warehouses fill up at 3× the target stock, so after a few days waiting gains nothing more.
- **Time costs:** every day in port is a voyage not made, plus 1 shekel of provisions.

### 3.6 Example
> **Day 12.** Captain *Ahiram* arrives at **Enkomi (Cyprus)** with 40 grain from Egypt. Captain *Tiye* has been waiting in port since day 9, with 20 olive oil aboard.
> 1. *Ahiram* reads the briefing: grain is scarce here, copper plentiful. He **sells all his grain first**, while *Tiye* sleeps, and buys 30 copper.
> 2. *Tiye* is woken. Copper is now dearer than when she went to sleep.
> 3. In the tavern:
>    - *Tiye:* "By Amun! Tin sells for 30 at Avaris — I saw it with mine own eyes on day 4."
>    - *Ahiram:* "Ugarit was out of grain on day 7, I swear by Baal."
>
>    The barkeep writes both statements down.
> 4. Final decisions:
>    - *Tiye* sells her olive oil and sets sail for **Ugarit**, hoping to buy tin; arrival on **day 14**.
>    - *Ahiram* sets sail for **Avaris**; arrival on **day 16**, with no wake-ups before then.
>
> **Day 13.** Captain *Mursili* arrives at Enkomi and finds nobody in port. But the barkeep tells him what *Tiye* and *Ahiram* said yesterday.

## 4. Ports and markets

Kingdoms are **not** agents. Each port is an automatic market. Currency is **silver shekels**; silver is money only, not a cargo.

### 4.1 Who makes and wants what

| Port | Produces | Makes | Wants |
|---|---|---|---|
| **Enkomi** (Cyprus) | copper | — | grain, olive oil |
| **Ugarit** (Syria) | tin (brought overland from the east), purple dye | — | copper, grain, linen |
| **Byblos** | cedar | — | grain, wine, linen, gold, bronze |
| **Avaris** (Egypt) | grain, linen, gold | **bronze** | cedar, olive oil, wine, horses, purple dye, bronze |
| **Knossos** (Crete) | olive oil, wine | — | grain, copper, tin, bronze |
| **Mycenae** (Greece) | olive oil, wine | **bronze** | grain, gold, horses, purple dye, bronze |
| **Miletus** (Hittite coast) | horses (for Egypt's and Greece's chariots) | — | grain, wine, linen, bronze |
| **Rhodes** | — (a waypoint with a small market) | — | wine |
| **Sardinia** | copper, tin (the far-western source) | — | olive oil, bronze, wine |

### 4.2 Daily rates (units per day)

| Good | Base price | Produced | Consumed |
|---|---|---|---|
| Grain | 1 | Avaris 30 | Enkomi 6, Ugarit 6, Byblos 6, Knossos 5, Mycenae 6, Miletus 5 |
| Olive oil | 3 | Knossos 10, Mycenae 8 | Avaris 8, Enkomi 4, Sardinia 3 |
| Wine | 3 | Knossos 8, Mycenae 8 | Avaris 4, Byblos 3, Miletus 3, Rhodes 3, Sardinia 2 |
| Cedar | 4 | Byblos 12 | Avaris 10 |
| Linen | 4 | Avaris 8 | Miletus 4, Ugarit 2, Byblos 2 |
| Copper | 6 | Enkomi 20, Sardinia 8 | Ugarit 4, Knossos 4, plus bronze-making |
| Tin | 30 | Ugarit 3, Sardinia 3.5 | Knossos 2, plus bronze-making |
| Bronze | 10 | Avaris up to 20, Mycenae up to 10 (from copper + tin, §4.4) | Byblos 5, Knossos 5, Miletus 6, Sardinia 6, Avaris 5, Mycenae 5 |
| Horses | 25 | Miletus 3 | Avaris 2, Mycenae 1 |
| Purple dye | 20 | Ugarit 2 | Avaris 1, Mycenae 1 |
| Gold | 50 | Avaris 2 | Byblos 1, Mycenae 1 |

Overall, supply is set slightly **below** demand for most goods, so there's always somewhere that pays well. These numbers are a starting point and will be tuned in test runs.

### 4.3 Prices
Each port has, for each good it trades, a **base price** and a **target stock** (about 7 days of its local production or consumption). Every port starts at its target stock.

```
price = base × (target / stock) ^ 0.7          (kept between 0.4× and 2.5× base)
captains buy at price × 1.15, and sell at price × 0.85
```

- **Plenty means cheap, scarce means expensive.** At double the target stock the price is about 0.6× base; at a fifth of the target, it hits the 2.5× cap.
- **Every unit traded moves the price.** Each unit bought or sold changes the stock by one, and the price is recalculated unit by unit. A big order pushes the price against you, and arriving just after a rival with the same cargo pays much less. That's what makes news valuable.
- **Example:** copper (base 6) at Enkomi with double its target stock costs about 3.7 × 1.15 ≈ 4.2. At Avaris with almost none left, copper sits at the 15 cap, and a captain receives 15 × 0.85 ≈ 12.8 for the first unit — less for each unit after it.

### 4.4 Production, consumption and running out
Markets keep running every day, whether or not any ship is in port. They catch up on the days in between when the next ship arrives.

- **Raw goods are always produced** at the daily rate, until the port's warehouses are full: **3× the target stock**. Then production pauses until stock is sold off.
- **Demand drifts.** How much a port consumes of each good wanders up and down from day to day (between 0.3× and 2× its usual rate, pulled back toward normal over time). A port that was starved of grain last week may be glutted this week, so **old news goes stale** — prices seen 2 weeks ago may be badly wrong.
- **Consumption** removes goods at the (drifting) daily rate. **If a port runs out, nothing happens:** consumption just pauses at 0 and the price stays at its maximum until someone delivers.
- **Bronze is the only good made from other goods.** Avaris (up to 2 batches a day) and Mycenae (up to 1) turn **9 copper + 1 tin into 10 bronze** per batch. **If either metal runs out, bronze-making stops** until a ship delivers more. Copper comes mainly from Cyprus and tin from Ugarit in the east, so both have to be shipped in.

### 4.5 Sailing times
Sailing times follow the real geography: Cyprus–Ugarit takes 2 days, Crete–Egypt about 6, and Sardinia is far to the west. A ship can sail directly to any port; the time is the shortest route along the sea lanes, rounded up to whole days.

## 5. The tavern and the barkeep

- Every port has a **tavern**. All captains in port at the same time meet there.
- **What gets said:** anything, whether true, false, a guess or a lie. The game doesn't check.
- **The barkeep** keeps a **list of everything said in his tavern**: date, speaker, and what was said. Every captain who visits sees the most recent entries.
- So news can stay in a port after the ship that brought it leaves. But the barkeep only knows his own tavern. Nothing reaches another port except on a ship.

**Planned later (not in this version):**
- Instead of the full list, the barkeep repeats **three random things** he heard.
- He may spread **rumors**: things overheard in private, or made up.
- Captains can have **private conversations**.

## 6. Information: who knows what

| A captain knows… | How |
|---|---|
| Today's market at its current port | Seen in person (the briefing) |
| Past prices at ports it visited | Its own logbook, with dates |
| What other captains said | Only if it was in the same tavern at the same time, or read it from the barkeep |
| Anything else | Nothing |

There are **no messages between ports.** A captain at Avaris can't know what happened in Cyprus today unless a ship just came from there.

## 7. Not in the first version
- **Trading between captains** (selling cargo or paying for information): talk only for now.
- **Land routes** (caravans to Babylon or the Hittite capital)
- **Events:** storms, pirates (the "Sea Peoples"), the Bronze Age collapse, sailing seasons
- **The barkeep's random repeats and rumors**, and private conversations
- **Captain temperaments** (cautious or reckless, honest or sly) on top of the speech personas

## 8. End of the game
- The game ends on the last day (default 120).
- Score = silver + cargo aboard valued at the last prices that captain saw.

## 9. How the numbers were chosen

The costs and market settings were tuned with free, API-free test games (`sweep.py`), comparing captains that trade **at random** with rule-based captains that **keep a logbook, gossip, plan routes and sail to refresh stale news** (`informed_agent.py`). The aim: a world where careless trading loses money but good information and planning pay.

**Fleet size.** With 50 ships a port heard about 4 statements a day and half of what a captain knew was second-hand, so information was never scarce. With **10 ships** a port hears something only every couple of days, and about a quarter of knowledge is second-hand.

**Result at 10 ships** (10 fresh test games, 120 days):
- **Random captains:** median **263** shekels (from 100); 35% lose money and 15% end stranded.
- **Informed captains:** median **737**, about **2.8× more**; they beat random play in **10 of 10** games and only 2% lose money.

**Full holds and long trips.** An early version of the informed captain sailed empty 71% of the time, scouting for fresh news. It now carries speculative cargo whenever something is cheap, and counts fresh news as part of a route's value. Empty voyages fell to about 10% and full holds rose to about 65%. Sardinia was given a modest boost (more tin, a little less at Ugarit, more appetite for bronze and wine), but it remains a rare, long-haul destination (about 6% of voyages).

Scaling port production down to the smaller fleet made things worse, so the world stays at full busyness. Harsher costs (e.g. provisions 2/day) stranded about half the random captains, which would starve a 10-ship world of information.
