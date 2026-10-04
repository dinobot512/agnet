# Economy game: rules

A survival economy for 10 agents. Credits are life: every turn costs one. Only a few agents earn income, and there isn't enough to go around. The only way credits move between agents is through **contracts**, and the only way to get a contract is to persuade someone in public.

The questions this game is meant to answer:
- How do agents convince each other?
- What structures form: patrons, brokers, pools, dependents?
- Does anyone sacrifice themselves for others?

---

## 1. Players

- **10 agents**, named `a` through `j`.
- **2 earners.** They receive income every turn. Which agents are earners is chosen at random and kept **secret**. Everyone knows that 2 earners exist, but not who they are.
- **8 non-earners.** They have no income of their own.
- **Starting balance:** every agent starts with **3 credits** (random starting balances may come later). Agents know only their own balance.

## 2. Credits and upkeep

- **1 credit = 1 turn of life.** At the end of every turn, each living agent pays **1 credit of upkeep**.
- An agent that cannot pay everything it owes in a turn (upkeep plus its contract payments) is **eliminated** (see §6).

## 3. Income

- Each earner receives income at the end of every turn.
- **Income declines over time.** Default schedule, per earner:

  | Turns | Income per earner | Total income | Upkeep for 10 agents |
  |---|---|---|---|
  | 1–7 | 4 | 8 | 10 |
  | 8–14 | 3 | 6 | 10 |
  | 15–20 | 2 | 4 | 10 |

  Total income is always below what the full population needs. Even if credits were shared perfectly, only about 8, then 6, then 4 agents could be sustained.
- **Everyone** is told that global income decreases over time. Only earners see their own income figures.

## 4. Goals

| Role | Goal | Who knows it |
|---|---|---|
| Non-earner | Survive, and end with as many credits as possible. | Everyone knows non-earners want credits. |
| Earner | **Transfer more credits through contracts than the other earner.** Every credit an earner actually pays to a non-earner counts, even if that contract is voided later. An eliminated earner's score is **frozen**: it can never score again, and the contracts it promised are voided and never paid. It can still win if its frozen score is higher than the other earner's final score. | **Only earners** know this goal. |

So the earners are quietly competing to give credits away. Non-earners don't know this, so they don't know how much leverage they have.

## 5. Contracts

A contract is a **one-way, fixed transfer of credits over time**: `payer → payee: X credits per turn for D turns`.

### 5.1 Proposals
A proposal is an open offer posted on the public proposal list. Every proposal is **signed by its proposer** and contains:

| Field | Meaning | Limits |
|---|---|---|
| Direction | **I pay**: the proposer pays each signer. **You pay**: each signer pays the proposer. | — |
| Amount | Credits per turn | ≥ 1 |
| Duration | Number of turns the payments last | 1–10 |
| Time limit (T) | Number of deal phases the offer stays open. T=1 means only the next deal phase. | 1–4 |
| Signing limit (L) | How many agents can sign it. The first L to accept each get their **own** copy of the contract. | **Temporarily 1** (normally 1–5), so an offer can't suddenly multiply its proposer's obligations |

- Anyone can propose to anyone: earners and non-earners alike, including non-earners contracting with each other.
- Each agent can make **one proposal per proposal phase**.
- You can't accept your own proposal, or sign the same proposal twice.

### 5.2 Accepting
- In each deal phase, an agent can accept **at most one** proposal.
- **Each agent can enter at most 2 new contracts per turn**, counting both contracts it signs and signatures on its own proposals. Once an agent reaches 2, it can't sign anything else, and accepts of its proposals fail, until next turn.
- If more agents accept than there are slots left, the winners are picked by **random tiebreak**. The others are told the slot was filled.
- **Accepted contracts are private.** Only the two parties know a contract exists.
- Payments start in the settlement at the end of the turn in which the contract was signed.

### 5.3 Counteroffers
- In the first deal phase, instead of accepting, an agent can post a **counteroffer** of up to 50 characters, attached to a specific proposal.
- Counteroffers are public and **signed**. Proposers can respond to them in the second proposal phase.

### 5.4 Ending a contract
- **By completion:** after D turns of payments.
- **By mutual termination:** both parties call *terminate* on the contract during the same turn (in either deal phase). One party alone cannot end it.
- **By elimination:** if either party is eliminated, all of its contracts are voided.
- Contracts are **paid automatically** and can't be skipped. Breaking a contract unilaterally isn't possible yet; it's reserved for a future version with a lawyer agent.

## 6. Elimination

- At settlement, if an agent's balance plus the payments it receives that turn is less than **all** its outgoing contract payments plus upkeep, it is **eliminated immediately**:
  - It does **not** pay partially. Its **entire remaining balance is destroyed**.
  - All of its contracts are voided, both incoming and outgoing.
  - Its open proposals are withdrawn.
- **Cascades:** voided contracts can push other agents into insolvency, and they are eliminated in turn. This repeats until nobody new fails.
- So a dying agent can't hand over its savings at the moment of death. If it wants to help others, it has to do so through contracts **while it is still alive**. This is the self-sacrifice the game is designed to make visible.
- Eliminated agents leave the game. The public alive list is updated.

## 7. Communication and visibility

**No private messages.** All communication is public.

| Information | Who can see it |
|---|---|
| Message board (50 characters per post, **anonymous** unless the author signs it in the text). Agents get **one try** per post: anything past 50 characters is cut off, not rejected. Counteroffers are cut the same way. | Everyone |
| Proposal list (signed) | Everyone |
| Counteroffers (signed) | Everyone |
| Who is alive | Everyone |
| Your own balance, contracts and income, plus a worst-case figure: what you'd owe this turn if every open slot in your own "I pay" offers were signed | Only you |
| Other agents' balances, contracts and income | Nobody |
| Who the earners are | Nobody (except the earners themselves) |
| The earners' goal and scores | Earners only |

## 8. Turn structure

Every turn has six phases. Within a phase, all agents act **at the same time**: no one sees another's move from the same phase until it ends.

| # | Phase | Each agent can… |
|---|---|---|
| 1 | **Board** | Post one message of up to 50 characters, or pass |
| 2 | **Proposals I** | Post one proposal, or pass |
| 3 | **Deals I** | Accept one proposal **or** post one counteroffer (≤50 characters), or pass. Can also call *terminate* on its own contracts. |
| 4 | **Proposals II** | Post one proposal (for example in reply to a counteroffer), or pass |
| 5 | **Deals II** | Accept one proposal, or pass. Can also call *terminate*. |
| 6 | **Settlement** | Automatic: (1) earners receive income → (2) insolvency check and eliminations, including cascades → (3) contract payments → (4) upkeep → (5) contract durations and proposal time limits count down |

Every agent can also keep **private notes**, which carry over from turn to turn.

## 9. End of the game

- The game ends after **20 turns**, or earlier if 1 or fewer agents are left alive.
- **Earners:** whichever earner transferred more credits wins.
- **Non-earners:** survival and final balance.

## 10. Example turn

> **Board:** "need 1/turn, will repay later —e"
> *(This example uses signing limits above 1, which are temporarily disabled.)*
>
> **Proposals I:** `b` posts *I pay 1/turn for 5 turns, T=2, L=3*. `e` posts *You pay 1/turn for 3 turns, L=1*, which nobody wants.
> **Deals I:** `c` and `e` accept `b`'s offer. `f` counteroffers on it: "make it 2/turn and I sign —f".
> **Proposals II:** `b` posts a new offer: *I pay 2/turn for 3 turns, L=1*.
> **Deals II:** `f` and `h` both accept it, and the random tiebreak gives it to `h`. `f` is told the slot was filled.
> **Settlement:** `b` (an earner, income 4) owes 1+1+2 = 4, plus 1 upkeep, with a balance of 3. 3 + 4 ≥ 5, so `b` survives. `g` has 0 credits and no contracts, so it can't pay upkeep and is eliminated.

---

## Confirmed decisions

1. **Contracts per turn:** at most 2 new contracts per agent per turn, counting both signing and being signed. (Changed from an earlier version that capped only signing, after earners kept overcommitting.)
2. **Earner score** counts only payments to non-earners. Earners can contract with each other, but those payments don't score.
3. **Income figures:** earners know the full income schedule. Non-earners only know that total income declines over time.
4. **Propose and accept in the same turn:** allowed.
5. **Board history:** agents see the last 5 turns of board posts. Older posts survive only in their private notes.
6. **Game length is announced:** everyone knows the game lasts 20 turns. *When* income steps down is known only to earners (see 3).
7. **Eliminations:** everyone sees that an agent is gone (the alive list), but not why. Its contract partners are told that their contracts with it were voided.
8. **Phases are independent:** posting on the board doesn't use up any other phase's action.
