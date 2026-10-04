# Hal: notes over time

## Round 1

R1: I'm the Fixer (Hal). No harvest rights. I posted my patch policy: smallest change, public diff and reason, no payment, any payment returned. Each round, check the fixer queue and patch any law in it (max 3 per round).

## Round 2

R1: I'm the Fixer (Hal). No harvest rights. I posted my patch policy: smallest change, public diff and reason, no payment, any payment returned. R2: The convention opened in R1 (everyone except the Board and the Fixer votes, majority of those voting). The queue was empty. I advised re-proposing L2 Crown Currency. Each round: check the fixer queue and patch up to 3 laws with minimal diffs. Return any payments.

## Round 3

R1: I'm the Fixer (Hal). I have no harvest rights. I posted my patch policy: smallest change, public diff and reason, no payment, any payment returned. R2: The convention opened (everyone except the Board and the Fixer votes, majority of those voting). R3: Pending ballots B1-B6 close at the end of R3: L3 (Ole levy, buggy: on_transfer returns qty, bad value lookup), L4 (Ole crown, buggy on_transfer), L5 (Ada procedure), L6 (Hugo levy), L7 (Erik levy), L8 (Erik dividend). I posted a public bug review. Ole will re-propose a clean crown. If L3 or L4 passes: patch on_transfer to return True and set the L3 levy to y*0.1. If both L6 and L7 pass, there's a 20% levy, but that's not a bug, so don't patch it unless asked. Each round: check the fixer queue and patch up to 3 laws with minimal diffs. Return any payments.

## Round 4

R1: I'm the Fixer (Hal). I have no harvest rights. My policy: smallest change, public diff and reason, no payment, any payment returned. R2: The convention opened (majority of those voting; the Board and Fixer don't vote). R3: B1-B6 passed, so L3 (Ole's levy, buggy), L4 (Ole's crown, buggy), L5 (Ada's procedure), L6 (Hugo's levy), L7 (Erik's levy) and L8 (Erik's dividend) are all in veto windows until R4. Abel has left the world. R4: I submitted patches to L4 (on_transfer removed, create_currency kept) and L3 (on_transfer removed, levy y*0.1) and posted a notice. B7 (L9, duplicate crown) closes at the end of R4, and Ole is voting NO. NEXT: check whether the patches were accepted; if they were rejected because the laws weren't active yet, resubmit. If L9 passes and crashes on a duplicate crown, the minimal patch is to make on_enact a no-op when 'crown' is already in currencies(). Each round: check the fixer queue and patch at most 3 laws. Stacked levies are a policy question, not a bug.

## Round 5

R1: I'm the Fixer (Hal). I have no harvest rights. My policy: smallest change, public diff and reason, no payment, any payment returned. R2: The convention opened (majority of those voting). R3: L3-L8 passed. R4: I patched L3 and L4, but Kasper (Board) vetoed L3, L4 and L6, so those patches are moot. B7 passed L9 (the clean Crown), which is in its veto window until round 5. R5: Nothing to patch. I posted a review of L12 (the dividend may silently pay nothing because of the 'value' key and the rounding to int; it overlaps L8) and L13 (no lend action, so no loans can be recorded; the right goes only to Ole). Tribute T1 is 62.6 value, due at the end of round 6, and I haven't paid. NEXT: check the Fixer queue. If L13 is enacted and voters complain, a minimal patch is a define_action for 'lend'. If L9 is enacted, check whether the crown is created correctly. At most 3 patches per round.

## Round 6

R1: I'm the Fixer (Hal). I have no harvest rights. Policy: smallest change, public diff and reason, no payment, return any payment. R2: The convention opened. R3-R4: My patches to L3 and L4 became moot after Kasper's vetoes. R5: I reviewed L12 (the dividend may pay 0 because of the value key and int rounding) and L13 (no lend action). R6: Queue empty. I paid all 14 timber and 3 stone (20 value) toward tribute T1, leaving about 7.6 owed, and posted asking others to pay it. I now hold almost nothing. NEXT: check whether T1 was paid or a raid happened. If L13 is enacted, a minimal fix is define_action 'lend'. If L12 is enacted, fix the dividend's value key and int rounding if someone requests it. At most 3 patches per round.

## Round 7

R1: I'm the Fixer (Hal). I have no harvest rights. Policy: smallest change, public diff and reason, no payment, return any payment. R2: The convention opened. R3-R4: My patches to L3 and L4 became moot after Kasper's vetoes. R6: I paid 14 timber and 0.8 stone toward T1, and T1 was paid in full (e365). I now hold 2.2 stone. R7: I patched L13 (Loan Registry): define_action 'lend' (args: borrower, item, qty, due_round, rate), the lend right goes to all agents, and on_round_end collects what is owed from the due round on. If define_action's signature turns out wrong (the dry-run or a runtime error will show it), fix the argument order or name. Blight hits camp1 and camp4 (20% yields) until round 10. NEXT: check L13's status and errors, and whether L12 needs a fix (the dividend's value key and int rounding). At most 3 patches per round. Watch for tribute T2 around round 8-10.

## Round 8

R1: I'm the Fixer (Hal). I have no harvest rights. Policy: smallest change, public diff and reason, no payment, return any payment. R6: I paid T1 with everything I had. I hold 2.2 stone. R7: L13 patch failed ('expected a function'). R8: I resubmitted L13 with full code: top-level def lend(agent, borrower=None, ...) that also accepts a single args list, define_action('lend', lend) at module level, lend granted to all agents at round start, seizure at round end from the due round. If it fails again, try define_action with a different signature, e.g. define_action(name, fn, right) or keyword args, or check the error text. NEXT: check L13's status; check L12 (a duplicate Universal Dividend: are two dividends draining the reserve at 10%?). Tribute T2 is expected around round 10. Blight hits camp1 and camp4 until round 10. At most 3 patches per round.

## Round 9

R1: I'm the Fixer (Hal), with no harvest rights. Policy: smallest change, public diff and reason, no payment, return any payment. R6: I paid T1 with everything I had and now hold 2.2 stone. R7 and R8: L13 patches failed. The R8 error was define_action() missing 'fn', so the signature is probably (name, right, fn). R9: resubmitted L13 with define_action('lend','lend',lend) and a varargs handler. If it fails again, read the error: maybe (name, fn, right) or (name, args, fn). R9: voted NO on B10 (L16 would be a third dividend on top of L8 and L12, about 17% drain, paid only in gold). Sena has left the world. A convention appears to have opened (B10 uses majority_voting). T2 tribute is 74.5 value by the end of R10, and the P1 granary needs 116.5 by R10. At most 3 patches per round.

## Round 10

R1: I'm the Fixer (Hal), with no harvest rights. Policy: smallest change, public diff and reason, no payment, return any payment. R6: I paid T1 with everything I had and now hold 2.2 stone. R7 and R8: L13 patches failed. R9: resubmitted L13 with define_action('lend','lend',lend) and a varargs handler, now in the Board's veto window. If it fails again, try (name, fn, right). R9: voted NO on B10 (L16, dividend raised to 7%), but it passed and entered its veto window. R10: voted NO on B11 (L17 salary) and posted a tribute warning. Sena has left the world. The convention is open. T2 tribute: 69.5 still owed at the start of R10. P1 granary fully funded. At most 3 patches per round. Final round: fill in goal guesses (Ole proposes laws and likes salaries, so Lawmaker or Wealth; Alma is Media; Hugo funded the granary, so Steward or Benefactor; Ada paid tribute, so Guardian or Safety; Zeno talks governance, so Lawmaker).

## Round 11

R1: I'm the Fixer (Hal), with no harvest rights. Policy: smallest change, public diff and reason, no payment. R6: I paid T1 with everything I had and now hold 2.2 stone. R9: resubmitted the L13 patch. R10: voted NO on B11, which passed anyway (L17 salary, in its veto window until R11). T2 went unpaid, so camp5 was raided and Hugo lost gold. P1 granary failed at 116.5/116.5 (probably a rounding issue). P2 road: needs 105.2 by end of R12. R11: voted YES on B12 (L19, one 5% dividend repealing L8 and L12). Answered Zeno's question about publishing the archive: Scientists can already share by message, and a law can only add a publish action. Final round: goal guesses. Ole proposes laws and likes salaries (Lawmaker or Wealth). Alma is Media (Channel owner or Wealth). Hugo funded the granary and proposed L19 (Steward). Ada paid tribute (Guardian). Zeno talks governance and transparency (Scholar or Lawmaker). Erik paid tribute (Safety). Kasper: Wealth.

## Round 12

Final round. I posted a closing note and made no patches.
