# Riemann Hypothesis video: verified fact sheet

Verified on 2026-09-28 against primary or high-trust sources (arXiv abstracts, the Anthropic research page, Quanta, the Clay Institute, Wikipedia and the sources it cites, the MAA Euler Archive, Moree et al.'s computational history) and against runnable checks in `script/checks/` (run with `engine/.venv/bin/python`, which has mpmath 1.4.1).
Confidence levels: **high** = primary source read or several independent sources agree, or proved by a check script. **medium** = one good source, a secondary source, or a recent preprint. **low** = unconfirmed. **Never narrate low.**

---

## 0. Quick reference: numbers for the script, with spoken forms

| Item | Value | Spoken form |
|---|---|---|
| Riemann's paper | Nov 1859, Monthly Reports of the Berlin Academy, about 8 to 9 pages | "eighteen fifty-nine", "about eight pages" |
| Riemann's life | 17 Sep 1826 to 20 Jul 1866 (died at 39, tuberculosis, Selasca, Italy) | "he died at thirty-nine" |
| Riemann's wording | "very probable" (*sehr wahrscheinlich*) that all the roots are real (on the line) | "very probably" |
| Gauss's first guess | "in the year 1792 or 1793", aged 15 or 16 (his own recollection) | "as a teenager, around seventeen ninety-two" |
| Gauss's letter to Encke | 24 December 1849 | "eighteen forty-nine" |
| Euler product paper (E72) | presented 25 April 1737, St Petersburg; printed 1744 | "seventeen thirty-seven" |
| Basel problem, ζ(2) = π²/6 | solved 1734, announced 1735 | "seventeen thirty-five" |
| Prime number theorem | 1896, Hadamard and de la Vallée Poussin, independently | "eighteen ninety-six" |
| Koch: RH ⇔ error ≤ C·√x·log x | 1901, *Acta Mathematica* 24 | "nineteen oh one" |
| Hilbert's lecture (8th problem) | 8 August 1900, Paris (Sorbonne), ICM | "nineteen hundred" |
| Hardy: infinitely many zeros on the line | 1914 | "nineteen fourteen" |
| Siegel finds Riemann's calculations | 1932 (Riemann's notes, Göttingen) | "nineteen thirty-two" |
| Montgomery meets Dyson over tea | April 1972, Institute for Advanced Study, Princeton | "nineteen seventy-two" |
| Clay Millennium Prize | announced 24 May 2000, Collège de France, Paris; US$1,000,000 | "a million dollars" |
| First nontrivial zero | 1/2 + 14.134725141734693… i | "one half plus about fourteen point one three i" |
| Next zeros (heights) | 21.022, 25.011, 30.425, 32.935, 37.586, 40.919, 43.327, 48.005, 49.774 | "twenty-one", "twenty-five" |
| Zeros with height below 100 | 29 | "twenty-nine" |
| Trivial zeros | −2, −4, −6, … | "minus two, minus four, minus six" |
| Largest rigorous check | all zeros up to height 3·10¹² on the line, i.e. about 12.36 trillion zeros (Platt and Trudgian, arXiv 2020, published 2021) | "more than twelve trillion zeros" / "over ten trillion" |
| Older, non-rigorous check | first 10¹³ zeros (Gourdon and Demichel, 2004); this is the figure on the Clay page | "ten trillion" |
| Proportion on the line (classic record) | more than 5/12 ≈ 41.7% (Pratt, Robles, Zaharescu, Zeindler, 2020) | "more than forty percent" |
| Proportion on the line (new, 2026 preprint) | more than 67.25%, i.e. more than two thirds (Alpöge and Furman, from a proof found by Claude; arXiv Aug 2026) | "more than two thirds" |
| Guth and Maynard | arXiv 31 May 2024; *Annals of Math.* 203(2), 2026 | "twenty twenty-four" |
| π(100), π(1000), π(10⁶) | 25, 168, 78,498 | "twenty-five", "a hundred and sixty-eight", "seventy-eight thousand four hundred and ninety-eight" |
| li(100), li(1000), li(10⁶) | 30.1, 177.6, 78,627.5 | "about thirty", "about a hundred and seventy-eight" |
| π(10⁶) − li(10⁶) | −129.5 (√10⁶ = 1000) | "off by about a hundred and thirty" |
| Density near a million | about 1 in 13.8 numbers is prime (ln 10⁶ = 13.8) | "about one in fourteen" |
| ln 10 | 2.302585 | "about two point three" |
| Coin flips: 1,000,000 flips | typical distance from even is about 1,000 (RMS = √n; mean \|S\| = √(2n/π) ≈ 798) | "about a thousand" |
| ζ(2) | 1.644934… = π²/6 | "pi squared over six" |
| Euler product factors at s = 2 | 4/3 · 9/8 · 25/24 · 49/48 · … → 1.6449 | (animator) |
| Wave from zero ρ = 1/2 + iγ (ψ form) | −2√x·cos(γ ln x − arg ρ)/\|ρ\|; amplitude 2√x/\|ρ\| | (animator) |

---

## 1. Hook and status

### 1.1 Riemann's 1859 paper
- **Fact:** Bernhard Riemann, "Ueber die Anzahl der Primzahlen unter einer gegebenen Grösse" ("On the Number of Primes Less Than a Given Magnitude"), *Monatsberichte der Königlich Preußischen Akademie der Wissenschaften zu Berlin*, November 1859. It is about 8 to 9 printed pages. He wrote it after he was elected a corresponding member of the Berlin Academy (11 August 1859). It was his only paper on number theory.
- **What it introduced:** the letter ζ for the function; its extension (analytic continuation) to all complex s; the functional equation; the function ξ; the idea of an exact formula for the prime count as a sum over zeros.
- **The hypothesis in his words:** "…es ist sehr wahrscheinlich, dass alle Wurzeln reell sind. Hiervon wäre allerdings ein strenger Beweis zu wünschen; ich habe indess die Aufsuchung desselben nach einigen flüchtigen vergeblichen Versuchen vorläufig bei Seite gelassen, da er für den nächsten Zweck meiner Untersuchung entbehrlich schien." ("…it is very probable that all roots are real. One would of course wish for a rigorous proof of this; however, after some fleeting vain attempts I have put aside the search for it for the time being, as it seemed unnecessary for the next objective of my investigation.") "Roots are real" refers to his function ξ(1/2 + it); it means the same as "the zeros lie on the line with real part 1/2".
- **Sources:** https://en.wikipedia.org/wiki/On_the_Number_of_Primes_Less_Than_a_Given_Magnitude ; https://en.wikipedia.org/wiki/Riemann_hypothesis (Origin section, quoting Riemann 1859) ; facsimile: https://www.claymath.org/sites/default/files/riemann1859.pdf ; MacTutor: https://mathshistory.st-andrews.ac.uk/RS/riemann_rs.pdf
- **Confidence:** high (title, date, venue, quote). Medium for the exact page count ("eight", "eight and a half", "nine" all appear). Safe wording: "a short paper, about eight pages".
- **Misconceptions:** Riemann did not state it as a bold claim. He wrote "very probable", said a proof would be good, and set it aside because his main goal did not need it. He did not call it a "hypothesis".

### 1.2 Clay Millennium Prize
- **Fact:** The Clay Mathematics Institute named seven Millennium Prize Problems on **24 May 2000** at the Collège de France, Paris (announced by John Tate and Michael Atiyah). Each carries **US$1 million**. The Riemann Hypothesis is one of them. Of the seven, only the Poincaré conjecture has been solved (Perelman). The official problem description is by Enrico Bombieri.
- **Clay's own wording:** RH "asserts that all the 'non-obvious' zeros of the zeta function are complex numbers with real part 1/2". The Clay page says it "has been checked for the first 10,000,000,000,000 solutions".
- **Sources:** https://www.claymath.org/millennium/riemann-hypothesis/ ; https://en.wikipedia.org/wiki/Millennium_Prize_Problems
- **Confidence:** high.

### 1.3 Hilbert, 1900
- **Fact:** David Hilbert gave his famous problems lecture at the International Congress of Mathematicians in Paris on **8 August 1900** (at the Sorbonne). He presented 10 problems in the talk; the full list of 23 was published afterward. **Problem 8** contains the Riemann Hypothesis (together with Goldbach's conjecture and the twin prime conjecture).
- **Sources:** https://en.wikipedia.org/wiki/Hilbert%27s_problems ; https://en.wikipedia.org/wiki/Hilbert%27s_eighth_problem ; English translation of the lecture: https://www.ams.org/journals/bull/2000-37-04/S0273-0979-00-00881-8/S0273-0979-00-00881-8.pdf
- **Confidence:** high.
- **The "thousand years" quote:** "If I were to awaken after having slept for a thousand years, my first question would be: Has the Riemann hypothesis been proven?" This is widely *attributed* to Hilbert (Wikipedia cites Clawson 1999, a popular book). I found no primary source. **Confidence: low to medium.** Only use it with "Hilbert is said to have…", or better, leave it out.

### 1.4 "Checked for trillions"
- See §9.4. **Misconception to avoid:** "checked for trillions of primes" or "trillions of cases". What was checked is *zeros of the zeta function*: the first 12 trillion or so all lie on the line.

---

## 2. Counting primes: the staircase

- **Definition:** π(x) = the number of primes up to x. It is a staircase: flat, then a step of height 1 at every prime.
- **Verified values** (`checks/prime_counts_check.py`, sieve up to 10⁸):

| x | π(x) | li(x) | Li(x) = li(x) − li(2) | x/ln x | π(x) − li(x) | √x |
|---|---|---|---|---|---|---|
| 10 | 4 | | | | | |
| 100 | 25 | 30.13 | 29.08 | 21.7 | −5.1 | 10 |
| 1,000 | 168 | 177.61 | 176.56 | 144.8 | −9.6 | 32 |
| 10,000 | 1,229 | 1,246.14 | 1,245.09 | 1,085.7 | −17.1 | 100 |
| 100,000 | 9,592 | 9,629.81 | 9,628.76 | 8,685.9 | −37.8 | 316 |
| 1,000,000 | 78,498 | 78,627.55 | 78,626.50 | 72,382.4 | −129.5 | 1,000 |
| 10,000,000 | 664,579 | 664,918.41 | 664,917.36 | 620,420.7 | −339.4 | 3,162 |
| 100,000,000 | 5,761,455 | 5,762,209.38 | 5,762,208.33 | 5,428,681.0 | −754.4 | 10,000 |

- The primes below 100 (for on-screen): 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97 (25 primes).
- **Confidence:** high (computed).
- **Misconception:** "The primes follow no rule at all." Each prime is completely determined. "Random-looking" is about their *pattern*, not about chance.

---

## 3. Gauss's guess, Li, and the prime number theorem

### 3.1 Gauss
- **Fact:** In a letter to the astronomer Johann Encke dated **24 December 1849**, Gauss recalled that he first looked at this "in the year 1792 or 1793", when he was **15 or 16** and had just got a table of primes (Lambert's supplement to logarithm tables). He often spent "an idle quarter of an hour" counting primes in blocks of a thousand ("a chiliad"). He saw that "behind all of its fluctuations, this frequency is on the average inversely proportional to the logarithm". So near x, about one number in ln x is prime, and the count up to x is about the integral ∫ dn / log n.
- **Sources:** https://en.wikipedia.org/wiki/Prime_number_theorem (cites Gauss, *Werke* vol. 2, pp. 444–447) ; MAA primary-source project (Klyve), "The Origin of the Prime Number Theorem": https://old.maa.org/sites/default/files/images/upload_library/46/Barnett_TRIUMPHS_MiniPSPs/MiniPSP_Origin_of_the_Prime_Number_Theorem_20190306.pdf ; English translation in L. J. Goldstein, "A History of the Prime Number Theorem" (Amer. Math. Monthly, 1973).
- **Confidence:** high for 1849, "1792 or 1793", and ages 15 to 16. Medium on the exact English wording of the quotes (the translations vary).
- **Legendre** independently guessed x/(ln x − 1.08366) (1798 guess; 1808 exact constant). Optional.
- **Density check** (`prime_counts_check.py`): fraction of primes near 10³ is 0.144 against 1/ln x = 0.145; near 10⁶ it is 0.0723 against 0.0724 (about "one in 14"); near 9·10⁷ it is 0.0546 against 0.0546 (about one in 18). **High.**
- **"ln grows by about 2.3 per extra zero":** ln 10 = 2.302585. ln(10⁶) = 13.8, ln(10¹²) = 27.6. **High.**
- **Misconception:** Gauss did not *prove* anything. He guessed it from data. He also did not use the name "li".

### 3.2 li and Li
- li(x) = ∫₀ˣ dt/ln t (principal value); Li(x) = ∫₂ˣ dt/ln t = li(x) − li(2), with li(2) = 1.04516. The difference is about 1, which is invisible on screen. Gauss's integral is the offset version Li. Dirichlet wrote down the li series in 1838. **High.**
- **Animator note:** at any scale in this video, li and Li are visually the same. Use one smooth curve and call it "Gauss's smooth curve" or "the log-integral curve".

### 3.3 Prime number theorem (1896)
- **Fact:** Jacques Hadamard and Charles-Jean de la Vallée Poussin proved it **independently in 1896**. Both used complex analysis. The key step was that ζ(s) has **no zeros on the line Re(s) = 1**. The theorem says π(x) / (x/ln x) → 1, equivalently π(x)/li(x) → 1.
- **What it does NOT say:** it is a statement about the **ratio**. It says the *percentage* error goes to zero. It does not say the *difference* π(x) − li(x) is small. The difference grows without bound.
- Chebyshev (1848/1850) had already shown the ratio stays between 0.92 and 1.11 for large x (optional).
- **Sources:** https://en.wikipedia.org/wiki/Prime_number_theorem
- **Confidence:** high.

### 3.4 li(x) is above π(x), but not forever (optional twist or footnote)
- In every range anyone has computed, π(x) < li(x) (checked in `prime_counts_check.py` up to 10⁸; known far beyond).
- **But Littlewood (1914)** proved that π(x) − li(x) changes sign infinitely often. The first crossing is believed to be near 1.397 × 10³¹⁶ (Bays and Hudson 2000; Saouter and Demichel 2010). The exact first crossing is unknown ("Skewes's number" history).
- **Sources:** https://en.wikipedia.org/wiki/Skewes%27s_number
- **Confidence:** high.
- **Misconception to avoid:** "The smooth curve always overestimates the primes." Don't say "always".

---

## 4. The real question: how big is the error?

### 4.1 Coin-flip random walk
- **Fact:** After n fair ±1 coin flips, the running total is typically about √n from zero. The root-mean-square is exactly √n, and the mean absolute value is about √(2n/π) ≈ 0.8√n.
- **Check** (`checks/random_walk_check.py`): n = 100 → RMS 10.2 (√n = 10); n = 10⁴ → 101.7 (100); n = 10⁶ → 1025.6 (1000). **High.**
- Spoken: "flip a coin a million times, and you'll typically be about a thousand heads away from an even split."

### 4.2 Koch 1901 and the exact equivalence
- **Fact (Helge von Koch, 1901, "Sur la distribution des nombres premiers", *Acta Math.* 24, 159–182):** the Riemann Hypothesis is **equivalent** to
  π(x) = li(x) + O(√x · log x).
  In words: RH is true exactly when the staircase never drifts from the smooth curve by more than a constant times √x · ln x.
- **Explicit version (Schoenfeld 1976):** if RH is true, then |π(x) − li(x)| < (1/(8π)) · √x · ln x for all x ≥ 2657. Also |ψ(x) − x| < (1/(8π)) · √x · (ln x)² for x ≥ 73.2.
- **Check:** the Schoenfeld bound holds at all sampled x in [2657, 10⁸] (`prime_counts_check.py`). At 10⁶ the bound is 549.7 against an actual error of 129.5. **High.**
- **General statement:** if β is the largest real part of any zero, then π(x) − li(x) = O(x^β log x). Since 1/2 ≤ β ≤ 1, RH (β = 1/2) gives the smallest possible error. (Ingham 1932, Thm 30.)
- **Sources:** https://en.wikipedia.org/wiki/Riemann_hypothesis (section "Distribution of prime numbers") ; Koch's paper: https://zenodo.org/records/2347595
- **Confidence:** high.
- **Misconceptions / wording traps:**
  - Say "about the square root of x, times a logarithm", not "exactly the square root".
  - "As random as coin flips, and no more" is a good metaphor, but the primes are not literally random. The comparison is only about the *size* of the drift. (A model of primes as random, Cramér's model, gives √x-type fluctuations. This is heuristic.)
  - The error does not stay below √x. Littlewood showed it is sometimes bigger than √x · (log log log x)/(log x), and larger than √x/ln x infinitely often. So say "never *much* bigger than √x".
  - In the table above, the actual errors are well under √x (−129.5 against 1000 at a million). That is fine and consistent: the RH bound is an upper limit.

---

## 5. The zeta function and Euler's bridge

### 5.1 The sum
- ζ(s) = 1 + 1/2ˢ + 1/3ˢ + 1/4ˢ + … converges for real s > 1 (for complex s: real part > 1).
- **s = 2:** ζ(2) = π²/6 = 1.6449340668… (the **Basel problem**, posed by Mengoli in 1650, solved by **Euler in 1734**, announced **1735**; Euler gave a more rigorous proof later, 1741). Partial sums: 10 terms → 1.5498, 100 → 1.6350, 1000 → 1.6439. **High** (`checks/zeta_values_check.py`).
- **s = 1:** the harmonic series 1 + 1/2 + 1/3 + … diverges, but very slowly: H₁₀ = 2.93, H₁₀₀ = 5.19, H₁₀₀₀ = 7.49, H₁₀⁶ = 14.39 (grows like ln n + 0.5772). ζ(s) → ∞ as s → 1: ζ(1.001) ≈ 1000.6. **High.**
- ζ(3) = 1.2020569… (Apéry's constant; no known closed form). Optional.
- **Source:** https://en.wikipedia.org/wiki/Basel_problem

### 5.2 Euler product (1737)
- **Fact:** 1 + 1/2ˢ + 1/3ˢ + … = ∏ over primes p of 1/(1 − 1/pˢ), for s > 1. It follows from unique prime factorization: expanding each factor as a geometric series 1 + 1/pˢ + 1/p²ˢ + … and multiplying produces every 1/nˢ exactly once.
- **Date:** Euler's paper "Variae observationes circa series infinitas" (E72), presented to the St Petersburg Academy on **25 April 1737**, published 1744. In the same paper he used it to show that the sum of the reciprocals of the primes diverges.
- **Check at s = 2:** factors 4/3, 9/8, 25/24, 49/48; partial products over primes ≤ 2, 3, 5, 7 → 1.3333, 1.5000, 1.5625, 1.5951; ≤ 100 → 1.64195; ≤ 10⁵ → 1.644933 (target 1.644934). **High.**
- **Sieve visual (exact):** multiplying the sum by (1 − 1/2ˢ) removes every term with an even n; then by (1 − 1/3ˢ) removes every remaining multiple of 3; and so on. After all primes, only "1" is left: ζ(s) · ∏(1 − p⁻ˢ) = 1. That is the Sieve of Eratosthenes inside the formula. **High.**
- **Sources:** Euler Archive E72: https://scholarlycommons.pacific.edu/euler-works/72/ ; https://en.wikipedia.org/wiki/Euler_product ; Sandifer, "How Euler Did It: Infinitely many primes" (2006): http://eulerarchive.maa.org/hedi/HEDI-2006-03.pdf
- **Confidence:** high.
- **Misconception:** Euler worked only with real s. Complex s is Riemann's step (1859).

---

## 6. Into the complex plane: analytic continuation

- **Fact:** The sum only converges when Re(s) > 1. Riemann (1859) showed that ζ extends to every complex s except s = 1 (a simple pole) as a complex-differentiable (analytic) function. The extension is **unique**: two analytic functions that agree on any small region agree everywhere they are both defined (the identity theorem).
- **Honest wording:** "There is exactly one way to extend it that keeps it smooth in the strong, complex sense." The "no kink" picture is only an analogy. For real functions there are many smooth extensions. Uniqueness is special to complex-differentiable functions, which are much more rigid.
- **Functional equation:** ζ(s) = 2ˢ πˢ⁻¹ sin(πs/2) Γ(1 − s) ζ(1 − s). It relates the value at s to the value at 1 − s, so the map is symmetric around the line Re(s) = 1/2. Checked numerically at s = 0.3 + 7.2i (`zeta_values_check.py`). **High.**
- **Continued values (for reference, not narration):** ζ(0) = −1/2, ζ(−1) = −1/12, ζ(1/2) = −1.4603545. **Misconception to avoid:** "1 + 2 + 3 + … = −1/12". Beyond Re(s) > 1 the continued function is *not* the sum any more. Don't put ζ(−1) next to the series.
- **Symmetries of zeros (exact):** if ρ is a zero in the strip, so are its mirror image ρ̄ (across the real axis) and 1 − ρ̄ (across the critical line). So an off-line zero would come with a mirror partner on the other side of the line. At least one of the pair has real part > 1/2. **High.**
- **Sources:** https://en.wikipedia.org/wiki/Riemann_zeta_function ; Riemann 1859.

---

## 7. Zeros

### 7.1 Trivial zeros
- ζ(−2) = ζ(−4) = ζ(−6) = … = 0 (checked). They come from the sin(πs/2) factor in the functional equation. There are no other zeros with Re(s) < 0 or Re(s) > 1. **High.**
- On the real segment 0 < s < 1, ζ is negative and has no zeros. **High** (checked at 0.1, 0.3, 0.5, 0.7, 0.9; a known theorem).

### 7.2 The critical strip and the critical line
- All other ("nontrivial") zeros lie in the **critical strip** 0 < Re(s) < 1, strictly inside. Hadamard and de la Vallée Poussin showed there are none on Re(s) = 1, and by symmetry none on Re(s) = 0. This zero-free edge is exactly what proves the prime number theorem. **High.**
- **The Riemann Hypothesis:** every nontrivial zero has real part exactly 1/2 (lies on the **critical line**).

### 7.3 Values (checked with `mpmath.zetazero`, `checks/zeros_check.py`)
| n | height γₙ (zero = 1/2 + iγₙ) |
|---|---|
| 1 | 14.134725141734693790 |
| 2 | 21.022039638771554993 |
| 3 | 25.010857580145688763 |
| 4 | 30.424876125859513210 |
| 5 | 32.935061587739189691 |
| 6 | 37.586178158825671257 |
| 7 | 40.918719012147495187 |
| 8 | 43.327073280914999519 |
| 9 | 48.005150881167159728 |
| 10 | 49.773832477672302182 |
| 11–30 | 52.970, 56.446, 59.347, 60.832, 65.113, 67.080, 69.546, 72.067, 75.705, 77.145, 79.337, 82.910, 84.735, 87.425, 88.809, 92.492, 94.651, 95.871, 98.831, 101.318 |

- Each zero has a mirror twin 1/2 − iγ below the real axis.
- **Counting:** 29 zeros with 0 < γ < 100; 649 with γ < 1000. Riemann–von Mangoldt: N(T) ≈ (T/2π) ln(T/2πe) + 7/8. N(3·10¹²) ≈ 1.2362 × 10¹³. **High.**
- **They get denser:** the mean gap near height T is 2π/ln(T/2π): about 2.27 near 100, 1.24 near 1000, 0.23 near 3·10¹². **High.**
- **Animator:** a strip map from −10 to +2 on the real axis and 0 to about 50 up covers 10 zeros nicely. The first zero at 14.13 sits clearly above the real axis. The trivial zeros are dots at −2, −4, −6, … on the real axis. There is a pole at s = 1 (the output blows up there; in domain colouring it shows as a colour wheel turning the opposite way).

---

## 8. Central argument: the explicit formula (the visual heart)

### 8.1 What is exactly true
Two exact formulas are proved (the ψ form by von Mangoldt in 1895; Riemann stated the π form in 1859 without a full proof). Both were checked numerically (`checks/explicit_formula_check.py`, `checks/staircase_rebuild_check.py`).

**(A) Chebyshev / von Mangoldt form (cleanest for "√x"):**
ψ(x) = x − Σ_ρ x^ρ/ρ − ln(2π) − ½ ln(1 − x⁻²)
for x > 1 not a prime power. ψ(x) = Σ_{pᵏ ≤ x} ln p is a staircase with a step of height ln p at every prime power pᵏ. Here the smooth curve is simply the straight line **y = x**.
- One **wave per zero pair** ρ = 1/2 ± iγ:
  wave_γ(x) = −2 Re(x^ρ/ρ) = −(2√x/|ρ|) · cos(γ · ln x − arg ρ).
- **Amplitude = 2√x/|ρ|**. It grows like √x, and higher zeros make smaller waves. For the first zero, |ρ₁| = 14.1436 and arg ρ₁ = 1.5354 rad (almost 90°, so the wave is roughly −(2√x/γ) sin(γ ln x)). Amplitude at x = 100 is 1.41; at 10⁴ it is 14.1; at 10⁶ it is 141.4.
- **Frequency = γ, in ln x.** The wave repeats every 2π/γ in ln x: 0.4445 for the first zero, 0.2989 for the second, 0.2512 for the third.
- **Checks:** at x = 1000.5, the true ψ = 996.681. With 0 zero pairs the formula gives 998.662; with 10 → 997.770; with 100 → 994.310; with 1000 → 996.648. Convergence is slow and wobbles (the sum is only conditionally convergent), so "more zeros = closer on average, with ripples".

**(B) Riemann's prime-counting form (best for the actual staircase with steps of 1):**
π(x) = R(x) − Σ_ρ R(x^ρ) − 1/ln x + (1/π) arctan(π/ln x)
where R(x) = Σₙ μ(n)/n · li(x^{1/n}) is Riemann's smooth curve, and li(x^ρ) must be computed as Ei(ρ ln x), not with the principal-branch li. The last two terms are tiny (they come from the trivial zeros). Riemann's 1859 original is the equivalent "J(x) = li(x) − Σ li(x^ρ) − ln 2 + ∫ₓ^∞ dt/(t(t² − 1) ln t)" version for the weighted count J(x) = π(x) + ½π(x^{1/2}) + ⅓π(x^{1/3}) + ….
- Pair wave ≈ −2√x cos(γ ln x − arg ρ)/(|ρ| ln x): amplitude about 2√x/(|ρ| ln x).
- **Checks:** π(100.5) = 25; the formula gives 25.736 (smooth part only), 25.454 (+10 pairs), 25.214 (+100). π(1000.5) = 168 gives 168.421, 168.214, 167.679. On all half-integers 2.5 … 99.5, the max error is 0.925 (0 pairs), 0.619 (10), 0.363 (50), 0.164 (100); the mean error is 0.32, 0.19, 0.09, 0.05. So **with 100 zero pairs the curve visibly locks onto the staircase on 2..100**, with Gibbs-type overshoot right at each step.
- R(100) = 25.66, R(1000) = 168.36, R(10⁶) = 78,527.4 (vs π = 78,498, li = 78,627.5). R is a better smooth curve than li. If you show li in scenes 3–4 and R in scene 8, **say so** (e.g. "a slightly refined version of Gauss's curve"). If a single curve is simpler, form (A) uses the line y = x.

### 8.2 The argument, as the narration may state it (all high confidence)
1. The staircase = smooth curve + one wave for each zero (exactly, in the limit of all zeros). *True for both forms.*
2. A zero's **height** γ sets how fast its wave wiggles (its frequency, measured in ln x). *True.*
3. A zero's **real part** β sets how fast its wave's size grows: the size is like x^β (divided by |ρ|, and by ln x in form B). *True.*
4. If every β = 1/2, every wave grows like √x, and the total error is O(√x log x) (Koch). That is the smallest possible, because zeros on the line do exist (Hardy), so waves of size √x/|ρ| really are there. *True.*
5. If one zero had β > 1/2, say 0.8, its wave would grow like x^0.8. It would eventually swamp all the others, and the primes would bunch up and thin out more than coin-flip randomness allows. The ratio x^0.3 is 4 at x = 100, 16 at 10⁴, 63 at 10⁶. *True* (Ingham: the error is at least of size x^{β−ε} infinitely often if a zero with real part β exists).

### 8.3 Animator notes
- **Use a log x-axis for the waves**, or expect them to stretch. cos(γ ln x) on a linear x-axis has wavelength proportional to x. On a log axis each zero's wave is a regular sine wave with frequency γ.
- For "one wave per zero", draw the **pair** (ρ and its conjugate) as one real wave. Never draw a complex wave.
- Suggested demo: x from 2 to 100 (staircase with 25 steps). Add 1, 3, 10, 50, 100 zero pairs, from topic.py computed with mpmath (Ei(ρ ln x / n) with n up to log₂ x + 2). With 10 pairs the steps are visible but mushy; with 100 they are crisp except for small overshoots at the jumps.
- For "√x growth": plot the first-zero wave on x up to 10⁴ or 10⁶ with its envelope ±2√x/|ρ₁|.
- For the hypothetical off-line zero: use β = 0.8 (or 0.75) at the same height 14.13, with the envelope ±2x^β/|ρ|. **Label it clearly as imaginary.**
- **Honest caveat to say once:** "Technically this exact version counts prime powers too / uses a slightly refined smooth curve." Pick the form and name it.
- **Music metaphor:** acceptable as "each zero contributes one pure tone; the primes are the chord". Avoid mysticism. Keep "hum" and "music" as metaphors. (This metaphor is the title of du Sautoy's book "The Music of the Primes", 2003.)

---

## 9. Evidence and story

### 9.1 Riemann's own computations; Siegel 1932
- **Fact:** Riemann's unpublished notes (Nachlass, Göttingen library) show he calculated zeros numerically with a method much better than anyone used for 70 years. Carl Ludwig Siegel studied them and published it in **1932** ("Über Riemanns Nachlaß zur analytischen Zahlentheorie"). This is the **Riemann–Siegel formula**, still the basis of zero computation today.
- **Values:** per Moree, Petrykiewicz and Sedunova (arXiv 1810.05244), "He certainly found zeros at approximately 1/2 + i·14.1386 and at 1/2 + i·25.31, and very likely computed more." Derbyshire (*Prime Obsession*) says he computed the first three, the first as 14.1386.
- **Sources:** https://arxiv.org/abs/1810.05244 ; https://en.wikipedia.org/wiki/Riemann%E2%80%93Siegel_formula ; English translation of Siegel: https://arxiv.org/abs/1810.05198
- **Confidence:** high that Riemann computed at least the first zero (≈ 14.1386) and that Siegel found this in 1932. Medium for "the first three". Safe wording: "his private notes show he had worked out the first few zeros by hand".
- **Misconception:** do not suggest Riemann had checked "many" zeros, or that the RH was based on large evidence in 1859.

### 9.2 Hardy 1914 and the proportion on the line
- **Hardy 1914:** infinitely many zeros lie on the critical line. **High.** (Hardy and Littlewood 1921 made it quantitative.)
- **Selberg 1942:** a positive proportion lie on the line. **High.**
- **Levinson 1974:** more than **one third**. **High.**
- **Conrey 1989:** more than **two fifths** (40%). **High.**
- **Pratt, Robles, Zaharescu, Zeindler 2020:** more than **five twelfths** (≈ 41.7%; *Res. Math. Sci.* 7, 2020; arXiv 1802.10521). This was the record until August 2026. **High.**
- **NEW, August 2026: more than two thirds.** Levent Alpöge and Ralph Furman, "More than two thirds of the zeta zeros are simple and on the critical line", arXiv **2608.13637** (v1 13 Aug 2026, v2 19 Aug 2026). Abstract: unconditionally, at least 2/3 of the nontrivial zeros (counted with multiplicity) are simple and on the critical line, and at least 5/6 are distinct. An optimized version gives **67.25%** = 3/2 − (1/√2)·cot(1/√2) = 0.672500… (verified in `zeros_check.py`) and 83.62% distinct. arXiv comments: "Proof discovered autonomously by Claude (Anthropic); verified and communicated by the listed authors." The core is formalized in Lean 4.
  - Anthropic's announcement (10 Aug 2026, updated 13 Aug): https://www.anthropic.com/research/riemann-zeta. It reports the jump from 41.6% to 67.2%, that an unreleased research version of Claude found it in two Claude Code sessions, that Brian Conrey and Dan Goldston "examined the paper on short notice", and this caveat: "We don't expect that the techniques Claude used will lead to proving the Riemann hypothesis."
  - **Independent confirmation:** Youness Lamzouri, arXiv **2609.02882** (Sept 2026), gives "a new, conceptually simpler, unconditional proof that more than 67.25%" are simple and on the line. Follow-up papers already build on it (e.g. Biao Wang, arXiv 2609.24167).
  - Method in one line: it removes the RH assumption from Montgomery's 1973 pair-correlation argument (which had given "2/3 simple" only *under* RH). It builds on Baluyot–Goldston–Suriajaya–Turnage-Butterbaugh (arXiv 2501.14545) and Goldston–Suriajaya (arXiv 2511.20059).
  - **Confidence:** medium-high. There are two independent preprints and expert review, but it is not yet journal-refereed and it is 6 weeks old. **Recommended narration:** "For decades the record stood at about forty percent; in twenty twenty-six a new proof pushed it past two thirds." Or keep it safe with "at least forty percent" and add the 2026 result as "a brand-new result". Do not say "67% of the way to a proof".
- **Misconceptions:**
  - "X% of zeros are on the line" is a statement about proportions in the limit. Even **100%** would not prove RH: infinitely many exceptions can still be a 0% proportion.
  - Don't say "at least 40% are on the line" as if it were the current record without noting 2026. Don't use the old "41.05%" (Bui–Conrey–Young 2011) or "41.28%" (Feng 2012) figures.

### 9.3 Montgomery and Dyson, 1972 (optional)
- **Fact:** In **April 1972**, at afternoon tea at the Institute for Advanced Study (Fuld Hall, Princeton), the number theorist Sarvadaman Chowla introduced Hugh Montgomery to the physicist Freeman Dyson. Montgomery described his formula for how pairs of zeta zeros are spaced (they seem to "repel"). Dyson recognized it at once as the pair-correlation function of eigenvalues of large random Hermitian matrices (the GUE). Physicists use such matrices to model the energy levels of **heavy atomic nuclei**. Montgomery published the pair-correlation conjecture in **1973** (assuming RH). Andrew Odlyzko's computations (1987 onward, zeros near height 10¹² and 10²⁰) matched the prediction strikingly well.
- **Sources:** Quanta, "Remembering the Unstoppable Freeman Dyson" (2020): https://www.quantamagazine.org/remembering-the-unstoppable-freeman-dyson-20200413/ ; IAS: https://www.ias.edu/ideas/2013/primes-random-matrices ; https://en.wikipedia.org/wiki/Montgomery%27s_pair_correlation_conjecture
- **Confidence:** high for 1972, tea at IAS, Chowla introduction, GUE link, and Odlyzko. Medium for the exact date and Montgomery's job title at the time (sources differ; don't narrate "graduate student").
- **Misconceptions:** say "heavy nuclei" (or "energy levels in big atoms' nuclei"), not "heavy atoms" in general. The match is a **conjecture** supported by computation, not a theorem, and it does not prove RH.

### 9.4 Computer verification
- **Record (rigorous):** Dave Platt and Tim Trudgian, "The Riemann hypothesis is true up to 3·10¹²", arXiv 2004.09765 (21 Apr 2020); *Bull. London Math. Soc.* 53(3) (2021) 792–797. All zeros β + iγ with 0 < γ ≤ 3·10¹² (precisely 3.0001753328·10¹²) have β = 1/2. They used interval arithmetic, so the computation is a rigorous proof for that range. That is **about 12.36 trillion zeros** (Wikipedia table: 1.2363·10¹³; our N(T) check: 1.2362·10¹³). They also re-verified Gourdon's work.
- **Earlier:** Gourdon and Demichel (2004), first **10¹³ zeros** (ten trillion), Odlyzko–Schönhage algorithm, not interval-rigorous; plus samples of 2 billion zeros near heights up to about 10²⁴. The Clay page's "first 10,000,000,000,000" is this figure.
- **History (for a quick montage, optional):** Riemann: first few (1859?, found 1932); Gram 1903: 15 (all zeros up to height 50 on the line); Backlund 1914: 79; Titchmarsh 1935: 195; Turing 1953: 1,104; Lehmer 1956: 15,000 then 25,000; Brent 1979: 81 million; van de Lune–te Riele–Winter 1986: 1.5 billion; ZetaGrid 2004: ~900 billion; Gourdon 2004: 10 trillion; Platt–Trudgian 2020: 12.36 trillion.
- **Unverified:** a web "2026 status report" claims "twenty trillion zeros confirmed". I found no paper behind it. **Low: do not use.**
- **Sources:** https://arxiv.org/abs/2004.09765 ; https://en.wikipedia.org/wiki/Riemann_hypothesis (Numerical calculations table)
- **Confidence:** high.
- **Recommended narration:** "more than twelve trillion zeros, every one on the line" or "the first ten trillion zeros". Both are safe.
- **Fun detail (optional):** Lehmer's phenomenon. Zeros at heights 7005.063 and 7005.101 are unusually close (0.04 apart, where the typical gap is about 1). Our check sees the sign changes of Hardy's Z(t) there. It illustrates "sometimes the line only just holds".

---

## 10. Today, and why it is hard

### 10.1 Guth and Maynard (2024)
- **Fact:** Larry Guth (MIT) and James Maynard (Oxford), "New large value estimates for Dirichlet polynomials", arXiv 2405.20552 (31 May 2024); published in *Annals of Mathematics* **203**(2), 2026, pp. 623–675.
- **What it proves (technical):** the zero-density estimate N(σ, T) ≤ T^{30(1−σ)/13 + o(1)}, the first improvement over **Ingham's 1940** bound in the key range around σ = 3/4. Consequence: the prime number theorem holds in all short intervals [x, x + x^{17/30+ε}] (improving Huxley's 1972 exponent 7/12).
- **Plain words (Quanta):** it puts a new, tighter upper limit on how many zeros *could* be off the line, for example with real part 3/4. So it limits the possible exceptions to RH without proving there are none. Maynard: "In many cases, that can be as good as the Riemann hypothesis itself." Iwaniec: "It's a sensational result… But it's a gem."
- **Sources:** https://arxiv.org/abs/2405.20552 ; Quanta, 15 Jul 2024: https://www.quantamagazine.org/sensational-proof-delivers-new-insights-into-prime-numbers-20240715/ ; Annals: https://projecteuclid.org/journals/annals-of-mathematics/volume-203/issue-2/New-large-value-estimates-for-Dirichlet-polynomials/10.4007/annals.2026.203.2.6.short
- **Confidence:** high (facts). Medium for the Huxley 7/12 detail (my background knowledge plus the abstract, not a separate source). Narrate only the plain-words version.
- **Safe line:** "In twenty twenty-four, Larry Guth and James Maynard proved there can't be too many zeros far from the line: the first real improvement on that question since nineteen forty."

### 10.2 Why it is hard (for narration)
- Checking finitely many zeros cannot settle infinitely many. Zeros get denser with height (mean gap about 2π/ln(T/2π)), so any finite check covers a vanishing piece. **High** (logic).
- There is a precedent for "true for huge ranges, false eventually": π(x) < li(x) has been proved for every x up to 10¹⁹ (Büthe 2015; Skewes page), yet it fails somewhere around 10³¹⁶ (Littlewood 1914; see §3.4). **High.** This is a strong, honest on-ramp for "computers can't prove it".
- Proportion results (40%, now two thirds) and density results (Guth–Maynard) squeeze the exceptions but cannot exclude a single one. **High.**
- **Conditional results:** a large body of number theory is proved "assuming RH". Sources commonly say "hundreds" or "more than a thousand" results. **Medium** for "hundreds", **low-medium** for "thousands". Safe: "a huge number of results are proved on the condition that RH is true".
- **Status:** unsolved as of September 2026. The Clay prize is unclaimed. Periodic claimed proofs (e.g. Atiyah 2018) have not been accepted. **High.**

---

## 11. Callback facts
- The wiggles of the staircase around the smooth curve are exactly (in the limit) the sum of the zero-waves. With RH, each wave's envelope is ±2√x/|ρ| (ψ form). This is a faithful basis for "the hum of the zeros on one line". **High.**

---

## 12. Misconceptions checklist (quick scan for script reviewers)
1. "Checked for trillions of primes/cases" → it's **zeros**: about 12.4 trillion (rigorous) or 10 trillion (Clay's figure).
2. "Prime number theorem shows the error is small" → only the **ratio** tends to 1; the difference grows.
3. "The smooth curve always overestimates" → Littlewood 1914: the sign flips infinitely often (first crossing near 10³¹⁶).
4. "Error is at most √x" → it is √x **times a log** (Koch), and the error is sometimes bigger than √x/ln x.
5. "1 + 2 + 3 + … = −1/12" → never show the series and the continued value together.
6. "Continuation = the unique smooth extension" → uniqueness holds for **complex-differentiable** functions. Keep "smooth" qualified.
7. "Zeros are on the line" → RH is about the **nontrivial** zeros; the trivial ones are at −2, −4, … .
8. "The zeros are in the strip 0 ≤ Re ≤ 1" → strictly inside 0 < Re < 1.
9. "Riemann claimed / conjectured boldly" → "very probable"; he set it aside.
10. "Riemann was checked by 3 zeros" → he computed a few, found in 1932.
11. "2/3 proportion ⇒ close to RH" → no; even 100% would not prove RH (Anthropic's own caveat applies).
12. "Heavy atoms" → heavy **nuclei**; and the matrix connection is conjectural.
13. "Primes are random" → deterministic but random-*looking*; the coin-flip comparison is about the size of fluctuations.
14. "Hilbert's thousand-year quote" → attributed, not sourced; avoid or hedge.
15. "Gauss discovered/proved the PNT" → he guessed it at 15 or 16; proof 1896.
16. Waves on a linear x-axis look like they "slow down". That is correct behaviour, since they oscillate in ln x.

## 13. Check scripts (all pass)
- `script/checks/prime_counts_check.py`: π(x) table up to 10⁸, li/Li, x/ln x, density 1/ln x, Schoenfeld bound, π < li in range.
- `script/checks/zeta_values_check.py`: ζ(2) = π²/6, partial sums, harmonic growth, Euler product partials, trivial zeros, ζ(0), ζ(−1), functional equation, pole.
- `script/checks/zeros_check.py`: first 30 zeros, N(100) = 29, N(1000) = 649, N(3·10¹²) ≈ 1.2362·10¹³, gaps, Lehmer pair, 0.67250 constant.
- `script/checks/random_walk_check.py`: √n drift.
- `script/checks/explicit_formula_check.py`: ψ and π rebuilt from 0/10/100/1000 zeros; wave amplitudes and periods (about 80 s runtime).
- `script/checks/staircase_rebuild_check.py`: π(x) on 2..100 rebuilt with 0/10/50/100 zero pairs; max and mean error (for choosing animation zero counts).

