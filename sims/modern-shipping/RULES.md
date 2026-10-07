# Modern shipping: rules

A fleet of independent shipping captains trades across today's world: 31 real ports, 29 goods, 13 multi-step supply chains, real sea lanes and the Suez and Panama canals.

Unlike the Bronze Age game, **market information is perfect**: every captain sees every port's live prices and stock. What captains **don't** know is anything about each other: where other ships are, what they carry, or how much money they have. There is no communication.

For now, all captains follow **predetermined strategies** (no AI agents) while the game mechanics are being worked out.

---

## 1. Captains and ships

- **Fleet:** 150 captains by default (configurable), each owning one ship for the whole game. Port production and consumption grow with the fleet, so the world stays proportionate at any size.
- **Mix:** about 40% bulk carriers, 25% tankers and 35% container ships. Half the captains are *greedy*, a quarter *liners* and a quarter *random* (§8).
- **Start:** 6,000 cash and a full fuel tank, at a random port (liners start at their loading port).

### 1.1 Ship types
Each type can only carry its own class of cargo:

| Type | Carries | Hold | Speed | Fuel burn at sea | Tank | Crew / day |
|---|---|---|---|---|---|---|
| ● Bulk carrier | iron ore, coal, copper ore, bauxite, lithium ore, nickel ore, lumber, grain, soybeans, rice, sugar, steel | 400 | 13 kn | 1.0 / day | 40 days | 2.0 |
| ◆ Tanker | crude, LNG, fuel | 150 | 14 kn | 1.2 / day | 48 days | 2.5 |
| ■ Container ship | coffee, cocoa, cotton, plastics, aluminium, copper, chips, batteries, cars, electronics, clothing, furniture, meat, chocolate | 100 | 18 kn | 1.8 / day | 72 days | 3.0 |

## 2. Costs
| Cost | When |
|---|---|
| **Crew** | Every day, at sea or in port (see the table above) |
| **Harbor dues** | 5 on every arrival |
| **Canal tolls** | Suez: 40 bulk / 50 tanker / 60 container. Panama: 30 / 40 / 50. Paid on departure if the route uses the canal. |
| **Fuel** | Bought at ports (§3) and burned at sea |

A captain with negative cash and an empty hold is **bankrupt** and leaves the game.

## 3. Fuel
- Fuel is a real good. **Refineries** (Houston, Rotterdam, Jamnagar, Singapore) make it from crude, and every port uses some.
- Ships buy fuel into their **tank** (`refuel`). A ship **can't set sail** without enough fuel for the whole voyage (days at sea × burn).
- Each port sells fuel from its own stock at its market price. **If the stock runs out**, bunker suppliers still deliver, but at a steep **emergency price** (2.5× fuel's base price). Nobody is ever stranded, but fuel at remote ports can be expensive.
- Tankers can also carry fuel as cargo and sell it to ports that need it.

## 4. The world

### 4.1 Ports (31)
| Region | Ports |
|---|---|
| Americas | Houston, New Orleans, Los Angeles, New York, Vancouver, Santos, Tubarão, Antofagasta |
| Europe | Rotterdam, Hamburg, Piraeus, Novorossiysk |
| Africa | Bonny, Abidjan, Richards Bay, Kamsar |
| Middle East | Ras Tanura, Ras Laffan, Jebel Ali |
| South Asia | Jamnagar, Mumbai, Chittagong |
| East and South-East Asia | Shanghai, Busan, Yokohama, Kaohsiung, Singapore, Ho Chi Minh City, Balikpapan |
| Oceania | Port Hedland, Newcastle |

### 4.2 Raw materials (where they come from)
| Good | Produced at |
|---|---|
| Crude | Ras Tanura (largest), Houston, Novorossiysk, Bonny |
| LNG | Ras Laffan, Houston |
| Iron ore | Port Hedland, Tubarão |
| Coal | Newcastle, Balikpapan, Richards Bay, Vancouver |
| Copper ore | Antofagasta |
| Lithium ore | Port Hedland, Antofagasta |
| Nickel ore | Balikpapan |
| Bauxite | Kamsar |
| Lumber | Vancouver |
| Grain | New Orleans, Novorossiysk, Vancouver |
| Soybeans | Santos, New Orleans |
| Rice | Ho Chi Minh City, Mumbai |
| Sugar | Santos, Mumbai |
| Coffee | Santos, Ho Chi Minh City |
| Cocoa | Abidjan |
| Cotton | Mumbai, Houston |

### 4.3 Supply chains
Factories run their recipe every day, as many batches as their capacity allows, **only while they have every input and room to store the output**. A factory with a missing input simply stops until a ship delivers.

| Product | Recipe | Made at |
|---|---|---|
| Fuel | 1 crude → 1 fuel | Houston, Rotterdam, Jamnagar, Singapore |
| Plastics | 1 crude → 1 plastics | Houston, Singapore |
| Steel | 2 iron ore + 1 coal → 1 steel | Shanghai, Busan |
| Aluminium | 2 bauxite + 1 LNG → 1 aluminium | Jebel Ali |
| Copper | 2 copper ore → 1 copper | Shanghai, Hamburg |
| Chips | 1 copper + 1 plastics → 2 chips | Kaohsiung, Busan |
| Batteries | 1 lithium ore + 1 nickel ore → 1 battery | Busan, Shanghai |
| Cars | 2 steel + 1 chips + 1 battery → 1 car | Yokohama, Hamburg, Busan |
| Electronics | 1 chips + 1 plastics + 1 aluminium → 2 electronics | Shanghai, Ho Chi Minh City |
| Clothing | 1 cotton → 1 clothing | Chittagong, Ho Chi Minh City |
| Furniture | 2 lumber → 1 furniture | Ho Chi Minh City |
| Meat | 2 soybeans + 1 grain → 1 meat | Shanghai |
| Chocolate | 1 cocoa + 1 sugar → 1 chocolate | Hamburg, Rotterdam |

So a car needs iron ore from Australia or Brazil, coal from Australia, Indonesia or South Africa, copper from Chile, crude from the Gulf, and lithium and nickel from Australia, Chile and Indonesia. All of that has to reach the right factories in East Asia or Germany before a single car ships.

### 4.4 Consumers
Final goods (cars, electronics, clothing, furniture, meat, chocolate, coffee, rice, grain…) are consumed at the big markets: Los Angeles, New York, Rotterdam, Hamburg, Piraeus, Shanghai, Yokohama, Jebel Ali and Mumbai. Every port also uses fuel. How much each port wants **drifts** up and down day to day.

## 5. Markets
Same model as the Bronze Age game:
- **Prices follow stock:** `price = base × (target / stock)^0.7`, kept between 0.4× and 4× base. A port's target stock is about 60 days of its flow.
- Captains **buy at price + 10%** and **sell at price − 10%**.
- **Every unit traded moves the price,** so big cargoes push prices against you, and so do other captains who got there first.
- Producers stop producing when their warehouses are full (3× target). Consumers stop consuming at 0. Neither is penalised.

## 6. Sea lanes and canals
- Ships follow a network of real sea lanes: 31 ports plus about 100 waypoints such as Gibraltar, Bab-el-Mandeb, Hormuz, Malacca, the Cape of Good Hope and Cape Horn. No lane crosses land.
- Distances are within about 12% of real sailing distances (e.g. Shanghai → Rotterdam about 11,100 nm via Suez, about 15,200 nm around the Cape).
- Each voyage takes the **shortest** route, or the shortest route **avoiding the canals** if the captain prefers to skip the tolls. Sailing days = distance ÷ (speed × 24), rounded up.

## 7. Time and turns
- The game is a **calendar of days** (default 365). There are no turns.
- A captain acts only when it **wakes**: when it arrives somewhere, or when a wait it chose ends. At sea it can do nothing and costs nothing to simulate.
- When several captains wake at the same port on the same day, they act **one at a time in random order**. First come, first served on the stock.
- **In port a captain can:** buy, sell, refuel, then **sail** (to any port, by the shortest or canal-free route) or **wait** (1–30 days).
- **What a captain sees** (its *view*): its own cash, fuel, hold and position; every port's live market; and the route, days, fuel and tolls to every port. Nothing about other captains.

## 8. Predetermined strategies
| Strategy | What it does |
|---|---|
| **Greedy** | Uses perfect information. At each port it sells cargo that pays well here. Then for every destination it estimates the profit per day of sailing there: cargo it holds, plus the best good to buy here, minus fuel, tolls, crew and dues, allowing for its own price impact. It sails the best option, or repositions empty toward the best trade elsewhere. It waits only when every option loses more per day than its crew's wages. |
| **Liner** | A fixed shuttle on one lane for its ship type: iron ore Port Hedland → Shanghai, crude Ras Tanura → Singapore, or electronics Shanghai → Los Angeles. It loads only when the lane pays (expected sale covers the purchase and both legs' costs); otherwise it waits at the loading port. |
| **Random** | Sells what it can, buys a random cargo, and sails somewhere random. The baseline. |

## 9. Score
Score = cash + cargo + tank fuel, valued at the sell prices where the ship is (or at its destination, if at sea).

## 10. How the numbers were chosen
Tuned with `sweep.py` (free, no AI). The aim was a world where every supply chain runs, skill clearly pays, and all three ship types are viable. On fresh test games of 60 ships:
- **Greedy:** about 17,000 (from 6,000), similar across ship types
- **Liners:** about break-even
- **Random:** loses most of its money

Things the tuning uncovered:
- **Remote ports used to strand ships for lack of fuel,** which is why the emergency bunker supply exists.
- **Markets need to be deep** (about 60 days of stock), or a single bulk cargo crashes the price.
- **Bigger fleets keep more chains running:** on average, factories ran at 18% of capacity with 30 ships, 32% with 60 and 74% with 150, which is why 150 is the default.
