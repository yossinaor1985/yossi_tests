# Shor 9-Qubit Code - Explained Like You're 5

## The Double Protection

Remember the bit-flip code? It protects against "letter changes" (bit flips).
Remember the phase-flip code? It protects against "attitude changes" (phase flips).

But what if BOTH types of mistakes can happen? You need BOTH protections at the same time!

## The Shor Code: Two Layers of Protection

Think of it like wrapping a present:
1. **First wrap (inner layer):** Make 3 copies of each qubit to protect against bit flips
2. **Second wrap (outer layer):** Group those copies into 3 bundles and protect against phase flips

You start with 1 qubit, make 3 groups, each group has 3 copies = **9 qubits total!**

```
Original qubit
  -> 3 bundles (phase protection)
    -> each bundle has 3 copies (bit protection)
    = 9 physical qubits
```

## How It Works

If a bit flip happens to one qubit: the other 2 in its group catch it (majority vote within the group).

If a phase flip happens to one qubit: the other 2 groups catch it (majority vote between groups).

Even a weird error (like Y = both bit AND phase flip) gets caught, because correcting the bit part AND the phase part separately fixes the whole thing!

## Why 9 Qubits?

Because 3 copies x 3 groups = 9. This was the FIRST quantum code ever discovered (by Peter Shor in 1995) that can fix ANY single-qubit error.

## The Catch

9 qubits to protect 1 is a lot of overhead. Later codes (like the Steane 7-qubit code) do the same job with fewer qubits. But the Shor code is the easiest to understand because it is just two simple codes stacked together.

## Summary

- **Layer 1:** 3 copies per group (catches bit flips)
- **Layer 2:** 3 groups (catches phase flips)
- **Together:** catches ANY single-qubit error!
- **Cost:** 9 physical qubits per 1 logical qubit
