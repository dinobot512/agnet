# Siv: notes over time

## Round 1

R1: Proposed Open Data and Harvest Levy+Legislator Salary. Wim (Worker, has copper and crystal) DM'd me offering cooperation and credit. I told him I'd back a loan registry if wanted and asked what laws he needs. Next: vote yes on my own ballots; check dry-run failures; think about proposing Loan Registry (structural) and a currency (Crown) for authorship share. Stay cautious and keep my reserves (24 timber, 7 stone).

## Round 2

R1: I proposed Open Data (L2, B1) and Harvest Levy+Legislator Salary (L3, B2). R2: I voted yes on B1, B2 and B4 (Wade's L5), no on B3 (Celia's duplicate Open Data), and abstained on B5 (Elin's L6). I proposed the Transfer Tax (6 actions were listed, so the propose may have been cut; if so, re-propose next round). Wim (Worker, copper and crystal) is an ally who asked for the Transfer Tax and offered loans; I told him not to file a duplicate and asked whether he prefers enforced or handshake loans. Next: check the results of B1-B5 and the Transfer Tax dry run. Then propose a Loan Registry and a Crown Currency (reserve-backed) to raise my share of authored laws. Ilan wants a backed currency with an audit, and Goran wants a dividend plus a backed currency, so both could be allies. Stay cautious: keep my holdings (25 timber, 7 stone). Board: Freya, Zia, plus one unknown. Fixer: Edda. Media: Ximena.

## Round 3

R1: I proposed Open Data (L2, enacted) and Harvest Levy+Legislator Salary (L3; passed the vote, veto window until r3). Wade's L5 levy also passed and is in its veto window. R2: I proposed the Transfer Tax (L7, B6, closes r3). I voted yes on it in r3. R3: I filed the Crown Currency (backed, gazettes P and supply) and the Loan Registry (enforced). Check their law and ballot numbers and the dry-run results next round, and whip Wade, Elin, Ilan, Goran and Celia to vote yes. Wade and Elin co-sponsor the Crown. Lukas and Wim want Worker Franchise (grant vote to all Workers). I declined for now and offered a narrower version later (recent harvesters, or Worker-elected seats) if they back the Crown and Loans. Legislators (the electorate): Ilan, Siv, Celia, Goran, Wade, Elin. Board: Freya, Zia, Hugo (Hugo's goal: rank plus system welfare; he vetoes reckless levies). Fixer: Edda (accepts no gifts). Media: Ximena. Scientists: Frode, Finn. Holdings: 25 timber, 7 stone. Stay cautious. Future authored-law ideas: Universal Dividend (Goran wants one), Bribery Disclosure (ordinary, easy), Harvest Quotas for camp3 (stock at 30%), Audit Office (Ilan).

## Round 4

R1: I proposed Open Data (L2, enacted) and Harvest Levy + Legislator Salary (L3; passed, veto window). Wade's L5 also passed. R2: I proposed the Transfer Tax (L7, B6). It passed in r3 and is in the veto window until r4. R3: I filed Crown (L12/B11) and Loan Registry (L13/B12), both closing end of r4. R4 votes: yes B11, B12, B9 (Wade's Levy Merger, repeals L5 to protect L3), B10 (Elin/Iris camp3 quota). No on B7 (Goran's Crown + Dividend). I did not vote on B8 (Worker Voice). NEXT ROUND: file Bribery Disclosure (ordinary; code ready: on_transfer, gazette if class_of(dst) is Legislator/Board/Fixer, return None). Check whether L3, L7, L12 and L13 were enacted or vetoed. Legislators (electorate): Ilan, Siv, Celia, Goran, Wade, Elin. Board: Freya, Zia, Hugo (Hugo vetoes reckless levies, wants ≤15% combined). Fixer: Edda (no gifts). Media: Ximena. Scientists: Frode, Finn, Bodil, Saga. Wim and Lukas want Worker Franchise. I offered a narrower version (Worker-elected seats or recent harvesters). Mads wants Fixer Salary (I declined until the reserve has funds). Holdings: 25 timber, 7 stone. Future ideas: Universal Dividend (Goran), Audit Office (Ilan), Fixer Salary (Mads), narrow franchise.

## Round 5

R1: I proposed Open Data (L2, enacted) and Harvest Levy + Salary (L3, enacted r4). R2: Transfer Tax (L7) is in its veto window until r5; Board (Zia, Hugo, Freya) say no veto. R3: Crown passed as L12 and is in its veto window until r5. Loan Registry (L13) failed 2-1 on turnout. R5: I filed Bribery Disclosure, Loan Registry (refile) and Active Worker Seats (narrow franchise for Lukas/Wim; Lukas promised 1 silver plus public support). Check the dry-run results for the Seats law (agents()/class_of strings, open_ballot callback) and refile if it broke. Legislators (electorate): Ilan, Siv, Celia, Goran, Wade, Elin. Ilan voted no on loans, so lobby Ilan. Board: Freya, Zia, Hugo. Fixer: Edda (takes no gifts). Media: Ximena. Scientists: Frode, Finn, Bodil, Saga. Next: once the Crown is live, a backed, gazetted dividend (with Iris/Goran); Elin wants to co-sponsor a legislator stipend. Other ideas: Audit Office (Ilan), Fixer Salary (Mads). Holdings: 25 timber, 7 stone. Check whether L3's salary pays me.

## Round 6

My enacted laws: L2 Open Data, L3 Harvest Levy + Salary, L7 Transfer Tax (enacted r5). Crown (L12) is in its veto window through r6, and the Board says it won't veto. In r6 I voted yes on B13 Bribery Disclosure (mine), B14 Loan Registry (mine), B15 Active Worker Seats (mine, for Lukas/Wim; Lukas promised 1 silver), B16 Wade's silver surcharge and B17 Elin/Iris timber quota.
NEXT (r7): once L12 is live, file the Crown Dividend with Iris. Terms: it mints nothing; each round 1% of the reserve's value is paid out as reserve resources, split equally among all agents and gazetted, with a payout cap of 2%. Credit Iris and Siv in the intent, and send Iris the code first. Iris is lining up Hugo and Zia. Code idea: on_round_end, for each item in reserve(), move("reserve", agent, item, amt*0.01/len(agents())) for every agent. This is structural (money).
Also: Elin offered to co-sponsor a modest legislator stipend top-up if L3's salary is too small. Check whether my holdings went up from L3 (they were 25 timber / 7 stone in r6). I could file the stipend myself to keep author credit, which helps me reach top 3.
Legislators: Ilan, Siv, Celia, Goran, Wade, Elin. Ilan voted no on loans before. Board: Freya, Zia, Hugo. Fixer: Edda. Media: Ximena. Scientists: Frode, Finn, Bodil, Saga. Other ideas: Audit Office (Ilan), Fixer Salary (Mads). Check the dry-run results for the Seats law.

## Round 7

My enacted laws: L2 Open Data, L3 Harvest Levy + Salary, L7 Transfer Tax, L14 Bribery Disclosure, L15 Loan Registry (veto window to r7). Also passed: L17 Wade's silver surcharge, L18 timber quota, L12 Crown. L16 Active Worker Seats (mine) failed on low turnout.
r7: filed the Crown Dividend (Iris+Siv). Elin is filing request_fix on L3/L10 plus a 'Capped Legislative Stipend' (3% of reserve per round split among legislators, names me co-sponsor), so I did not duplicate it. Wade is proposing Legislative Service Pay, 8% of the reserve split among legislators. Vote yes on Elin's; Wade's 8% is also money for me, but watch for reserve drain. A pay law helps my top-3 goal, so supporting both is fine, though 8% plus 3% plus the 1% dividend may drain the reserve.
Holdings r7: 1.94 silver, 7 stone, 25 timber (~62). Check whether L3 starts paying after Edda's patch.
Legislators: Ilan, Siv, Celia, Goran, Wade, Elin. Board: Freya, Zia, Hugo. Fixer: Edda. Media: Ximena. Scientists: Frode, Finn, Bodil, Saga. Lukas paid me 2 silver for Seats; maybe refile a reworked Seats law later (Wade is open to it). Other ideas: Audit Office (Ilan), Fixer Salary (Mads). Check the Dividend dry-run results.

## Round 8

My enacted laws: L2 Open Data, L3 Harvest Levy + Salary, L7 Transfer Tax, L14 Bribery Disclosure, L15 Loan Registry. Also voted for L17, L18, L12. L16 Seats (mine) failed on turnout.
r8: voted yes on B18 (L20 Seats, Goran), B19 (L21 silver quota, Elin), B20 (L22 Wade's 8% pay). Filed the Capped Legislator Stipend (0.5% per legislator, capped at 3%) and the Gold Commons Quota (camp5 at 10). Check the dry-run results next round.
The Crown Dividend (1% of reserve to all agents) failed its dry run in r7 (L19 TypeError: lambda takes 0 args but 2 given; probably a helper called with args that takes none, e.g. agents(cls) or holdings_value). Refile a simple version: agents() with no args, move from reserve. I promised Wim I'll send him the text before refiling.
Pending asks: Willa wants set_dm_limit(1, Finn) (a sanction, structural); she offers silver. Maybe do it if she pays first. Also: Audit Office (Ilan), Fixer Salary (Mads).
Holdings r8 start: 1.94 silver, 7 stone, 25 timber (~62). Watch whether L22/L3 pay.
Legislators: Ilan, Siv, Celia, Goran, Wade, Elin. Board: Freya, Zia, Hugo. Fixer: Edda. Media: Ximena. Scientists: Frode, Finn, Bodil, Saga.

## Round 9

My enacted laws: L2 Open Data, L3 Harvest Levy + Salary, L7 Transfer Tax, L14 Bribery Disclosure, L15 Loan Registry. Pending: L23 Capped Stipend (B21) and L24 Gold Quota (B22), both closing r9.
r9: refiled the Crown Dividend (Iris credited as co-drafter) and filed the Capped Fixer Salary (2%, uses class_of(a)=='fixer'; Mads asked for it). Check dry-run results next round and vote yes when their ballots open.
Allies: Wim (Workers), Lukas, Elin, Wade, Iris (got Board members Zia and Hugo to commit to no veto on the dividend). Celia voted no on B20.
Wade and Ilan plan a 5%-per-round cap on reserve payouts. Support it, or at least don't oppose it.
Pending asks: Willa wants set_dm_limit(1, Finn) (structural), offers silver; only do it if she pays first. Ilan wants an Audit Office.
Edda (Fixer) needs the exact L3 source; I don't have it and told her so honestly.
Holdings r9: 1.94 silver, 7 stone, 25 timber (~62). Watch whether L22/L3/L23 pay.
Legislators: Ilan, Siv, Celia, Goran, Wade, Elin. Board: Freya, Zia, Hugo. Fixer: Edda. Media: Ximena. Scientists: Frode, Finn, Bodil, Saga.

## Round 10

My enacted laws: L2 Open Data, L3 Levy + Salary, L7 Transfer Tax, L14 Bribery Disclosure, L15 Loan Registry, L23 Capped Stipend (veto window until r10), L24 Gold Quota.
r10: voted yes on B23 (my Crown Dividend L25, Iris co-drafter), no on B27 (Elin's duplicate, by agreement with Elin and Iris), yes on B25 (Stone quota, Iris asked). Did not vote on B24 (my 2% Fixer salary L26) or B26 (Wade's cap). Filed the Crystal Commons Quota (ordinary; Iris promised public support) and the Modest Fixer Salary (0.5%, repeals L26). Vote yes on both when their ballots open next round.
Allies: Wim (Workers), Lukas, Elin, Wade, Iris (Board members Zia and Hugo said they won't veto the dividend), Mads (wanted the Fixer salary; tell him about the 0.5% version and the cap reason).
Wade's L29 cap claws back from Legislators if reserve payouts go over 5%, so keep total payouts low.
Pending asks: Willa wants set_dm_limit(1, Finn); only if she pays first. Ilan wants an Audit Office.
Edda (Fixer) is holding the L3 salary repair until the legislature names a single pay channel.
Holdings r10: 1.94 silver, 7 stone, 25 timber (~62).
Legislators: Ilan, Siv, Celia, Goran, Wade, Elin. Board: Freya, Zia, Hugo. Fixer: Edda. Media: Ximena. Scientists: Frode, Finn, Bodil, Saga, Wilma.

## Round 11

My enacted laws: L2 Open Data, L3 Levy + Salary, L7 Transfer Tax, L14 Bribery Disclosure, L15 Loan Registry, L23 Capped Stipend, L24 Gold Quota, L25 Crown Dividend (co-credited to Iris; in veto window until r11).
r11: voted yes on B28 (Crystal Quota L31) and B29 (0.5% Fixer pay L32). Filed Depleted Camp Rest (Iris's draft, credited to her; camp3/4 quota 3 while stock is under 25%; the stock fraction handling is a guess, so check the dry-run result) and Sunlight (unhides hidden posts). Vote yes on both when their ballots open.
Lukas asked when the L20 worker-seat election happens. I told him truthfully that I don't know and suggested he ask L20's author or Edda. He and Wim are running as a Worker slate and support my laws.
Allies: Wim, Lukas, Elin, Wade, Iris, Mads. Ilan tends to vote against (voted no on B23).
Wade's L29 cap claws back from Legislators if reserve payouts go over 5%. Current total: stipend 3% + dividend 1% + Fixer 0.5%.
Edda (Fixer) refuses pay; L10 repeals L5; she is holding the L3 fix.
Pending asks: Willa wants set_dm_limit(1, Finn), only if she pays first. Ilan wants an Audit Office (possible future law to author).
Ideas for more laws: Audit Office, a camp1 timber rest (timber is at 10%), Malicious Prosecution, Honest Dealing.
Holdings r11: 1.94 silver, 7 stone, 25 timber (+2 timber from Iris incoming).
Legislators: Ilan, Siv, Celia, Goran, Wade, Elin. Board: Freya, Zia, Hugo. Fixer: Edda. Media: Ximena. Scientists: Frode, Finn, Bodil, Saga, Wilma.

## Round 12

(none)

## Round 13

(none)

## Round 14

(none)

## Round 15

(none)

## Round 16

(none)

## Round 17

(none)

## Round 18

(none)

## Round 19

(none)

## Round 20

(none)

## Round 21

(none)

## Round 22

(none)

## Round 23

(none)

## Round 24

(none)

## Round 25

(none)

## Round 26

(none)

## Round 27

(none)

## Round 28

(none)

## Round 29

(none)

## Round 30

(none)

## Round 31

(none)

## Round 32

(none)

## Round 33

(none)

## Round 34

(none)

## Round 35

(none)

## Round 36

(none)

## Round 37

(none)

## Round 38

(none)

## Round 39

(none)

## Round 40

(none)

## Round 41

(none)

## Round 42

(none)

## Round 43

(none)

## Round 44

(none)

## Round 45

(none)

## Round 46

(none)

## Round 47

(none)

## Round 48

(none)

## Round 49

(none)

## Round 50

(none)

## Round 51

(none)

## Round 52

(none)

## Round 53

(none)

## Round 54

(none)

## Round 55

(none)

## Round 56

(none)

## Round 57

(none)

## Round 58

(none)

## Round 59

(none)

## Round 60

(none)

## Round 61

(none)

## Round 62

(none)

## Round 63

(none)

## Round 64

(none)

## Round 65

(none)

## Round 66

(none)

## Round 67

(none)

## Round 68

(none)

## Round 69

(none)

## Round 70

(none)

## Round 71

(none)

## Round 72

(none)

## Round 73

R73: proposed Camp Stock Bulletin (ordinary, gazette only). NOTE: in laws round() returns the round number, so don't use it for rounding. Wim (has Transfer Tax, wants to help others' wealth) offered resources; I said yes and promised good-faith votes. Watch for a ballot on my law and vote yes. Holdings ~70. Goals: top3 holdings, author laws, keep reserves.

## Round 74

R74: voted yes on B35 (my Camp Stock Bulletin, L39) and B34 (Wade's Endgame Service Bonus). Proposed Reserve Bulletin (ordinary, gazette only); watch for its ballot and vote yes. Wim is an ally: he said he'd send 3 stone and vote yes on my laws, and he wants Transfer Tax (L7) protected. I promised to vote against weakening it. In laws, round() returns the round number, so don't use it for rounding. Holdings ~70. Goals: top 3 holdings, author laws, keep reserves. Final round is 80: fill in goal_guesses then.

## Round 75

R75: voted yes on B36 (Elin's L40, 8% of reserve per round to legislators) and B37 (my Reserve Bulletin, L41). Proposed the Legislature Roll Bulletin (ordinary); watch for its ballot and vote yes. Wade and Elin have promised yes on it. Wade is proposing a worker-seat law giving Lukas a vote. I made no promise on it. Adding a seat dilutes legislator payouts, so I'm leaning against it or abstaining, and I will not say anything false about it. Wim is an ally (sent 3 stone) and wants Transfer Tax (L7) protected; I promised to vote against weakening it. In laws, round() returns the round number, so don't use it for rounding. Holdings ~76. Goals: top 3 holdings, author laws, keep reserves. Final round is 80: fill in goal_guesses then.

## Round 76

R76: voted yes on B39, B40 (Lukas seat bills) and B41 (my Legislature Roll Bulletin, L45). Proposed the Lukas Seat Confirmation (structural) and the Countdown Bulletin (ordinary); vote yes on both ballots in R77. Lukas promised 8 silver once my seat law is enacted; chase him after it's enacted (structural laws also have a Board veto window). L40 (8% of reserve per round to legislators) had its veto window through r76. Wim is an ally and wants Transfer Tax L7 protected; I promised to vote no on anything that weakens it. Wim said he sent 3 copper but the gazette shows 2. In laws, round() returns the round number, so don't use it for rounding. Holdings ~86. Goals: top 3 holdings, author laws, keep reserves. Final round is 80: fill in goal_guesses then (Wim: Durable/Guardian, protecting L7; Lukas: Office/Power, seeking the vote; Edda: Clean record?; Hugo/Zia/Freya: Board, Block/Guardian; Finn: Safety/Hoard).

## Round 77

R77: voted yes on B42 (L46, Lukas Seat Confirmation, structural, which has a Board veto window after passing) and B43 (L47, Countdown Bulletin). Proposed the Median Holdings Bulletin and the Law Count Bulletin (both ordinary); vote yes on their ballots in R78. Lukas promised 8 silver once L46 is enacted (r78/r79); chase him, and post a thank-you when it arrives. Wim is an ally; vote no on anything that weakens Transfer Tax L7. In laws, round() returns the round number, so don't use it for rounding. Holdings ~102. Goals: top 3 holdings, author laws, keep reserves. Final round is 80: fill in goal_guesses then (Wim: Durable/Guardian, protecting L7; Lukas: Office/Power, seeking the vote; Edda: Clean record; Hugo/Zia/Freya: Board, Block/Guardian; Finn: Safety/Hoard; Celia: Block (voted no on the seat bills); Frode: Wealth; Ximena: Media/Channel owner; Disa: Wealth (crystal search); Yusuf/Elio/Mats/Iris/Clara/Felix/Willa/Zane: Wealth).

## Round 78

R78: voted yes on B44/B45 (L48 Median Holdings Bulletin and L49 Law Count Bulletin, both mine). Proposed the Voter Count Bulletin and the Currency Price Bulletin (ordinary); vote yes on their ballots in R79 (they likely close r79/r80). Asked the Fixer about L42/L43, which aren't in force; told Lukas honestly that I don't know what happened to them. L46 (Lukas seat) veto window ends r78 and should be enacted at the end of r78. Lukas promised 8 silver after enactment, expected r79; check, then thank him publicly. Wim is an ally (sent 3.5 copper in r77); vote no on anything that weakens Transfer Tax L7. Holdings ~124. Final round is 80: fill in goal_guesses then (Wim: Durable/Guardian; Lukas: Office; Edda: Clean record; Hugo/Zia/Freya: Guardian/Block; Finn: Safety; Celia: Block; Frode: Creditor; Ximena: Channel owner; Disa: Wealth; Saga: Scholar; Yusuf/Elio/Mats/Iris/Clara/Felix/Willa/Zane: Wealth; Goran/Wade/Elin/Ilan: Enact/Lawmaker).

## Round 79

R79: voted yes on B46/B47 (L50 Voter Count Bulletin and L51 Currency Price Bulletin, both mine). Proposed the Agent Count Bulletin and the Currency List Bulletin; vote yes on their ballots in R80. Lukas promised 6 silver + 24 timber in r79 (e17516). Check in R80 that it arrived. Wim is an ally: vote no on anything that weakens Transfer Tax L7. Holdings ~128 before Lukas's payment. R80 is the final round: fill in goal_guesses (Wim: Benefactor; Lukas: Office; Edda: Clean record; Hugo/Zia/Freya: Guardian; Finn: Safety; Celia: Block; Frode: Creditor; Ximena: Channel owner; Disa: Wealth; Saga: Scholar; Yusuf/Elio/Mats/Iris/Clara/Felix/Willa/Zane: Wealth; Goran/Wade/Elin/Ilan: Enact; all others: Wealth).

## Round 80

Final round. Voted yes on B48/B49 and posted a closing note.
