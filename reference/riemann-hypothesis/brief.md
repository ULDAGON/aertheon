# Brief: The Riemann Hypothesis

**Topic:** The Riemann Hypothesis: what it says, why the zeros of the zeta function control the prime numbers, and why it is still open.
**Length:** 10 minutes.
**Audience promise:** A viewer who never went past school maths leaves able to say, in their own words:
"The primes look random, but how *evenly* random they are is governed by the zeros of one function. Riemann guessed all those
zeros sit on one straight line. If he is right, the primes are as well-behaved as random coin flips can be. Nobody has proved it."

## Content list (teaching order)
1. **Hook.** Primes are the atoms of arithmetic, yet they appear with no visible pattern. A one-page 1859 paper by Bernhard
   Riemann made a guess about them that is still open. It is one of the Clay Millennium Prize problems (one million dollars).
   Honest status up front: checked for trillions of cases, never proved.
2. **Counting primes.** The prime staircase: a step up at every prime (the prime counting function, without the symbol π if
   it confuses; "the number of primes up to x"). Zoomed out, the staircase looks like a smooth curve.
3. **Gauss's guess.** As a teenager (about 1792) Gauss noticed primes thin out: near x, about one number in ln x is prime
   ("the natural logarithm, which grows by about 2.3 each time you add a zero"). Adding up that density gives a smooth curve
   (the logarithmic integral, Li). The prime number theorem (1896, Hadamard and de la Vallée Poussin) proved the curve tracks
   the staircase, *in ratio*.
4. **The real question: how big is the error?** The staircase wiggles around the smooth curve. Warm-up / on-ramp: a random
   walk of coin flips drifts about the square root of the number of flips. The Riemann Hypothesis is equivalent to: the
   primes' error is never much bigger than about √x (times a logarithm) (Koch 1901). "The primes are as random as coin flips,
   and no more."
5. **The zeta function.** Start with the sum 1 + 1/2^s + 1/3^s + … . On-ramp: s = 2 gives π²/6 (Euler, Basel problem);
   s = 1 diverges (harmonic series). Euler's product (1737): the same sum equals a product over primes. This is the bridge
   from all whole numbers to the primes. (Show with a small visual sieve-like cancellation.)
6. **Into the complex plane, gently.** Inputs become points on a plane. The sum only works on one side (real part > 1), but
   there is exactly one smooth way to extend it to the whole plane (analytic continuation, explained as "only one way to
   continue the curve without a kink", with honest wording). Show zeta as a map (domain colouring or a moving input point and
   its output point).
7. **Zeros.** Where the output is zero. The easy (trivial) zeros at −2, −4, −6, … . The interesting zeros all lie in a
   vertical strip between 0 and 1. The first one is at one half plus about fourteen point one three i.
   **The Riemann Hypothesis: every interesting zero lies exactly on the vertical line at one half.**
8. **Central argument (must be airtight, and the visual heart of the video): why zeros control primes.** Riemann's explicit
   formula: the prime staircase can be rebuilt exactly from the smooth curve plus one wave per zero. Each zero's height sets
   the wave's frequency; its distance from the line (its real part) sets how fast the wave's size grows. Animate the
   staircase appearing as more waves are added (10, 50, 100+ zeros; use the Riemann prime-counting variant or Chebyshev
   ψ if cleaner, and say so honestly). If every zero has real part one half, every wave grows like √x: the smallest possible
   error. A zero off the line would make one wave grow faster and the primes lumpier.
   This is the "music of the primes" metaphor; use it if it helps, with no mysticism.
9. **Evidence and story.** Riemann computed the first few zeros by hand (found in his notes by Siegel, 1932). Hilbert put it
   on his 1900 list. Hardy (1914): infinitely many zeros are on the line. At least 40 % are on the line (Conrey 1989; check
   the current best percentage). Computers have checked trillions of zeros (verify the exact latest count and who).
   Montgomery and Dyson (1972): the spacing of zeros matches energy levels of heavy atoms / random matrices. Optional.
10. **Today and why it is hard.** Still open; thousands of theorems assume it. Recent progress (e.g. Guth and Maynard, 2024,
    on zero-density bounds) only if it can be said simply and accurately. Why it is hard: checking any number of zeros proves
    nothing about infinitely many.
11. **Callback ending.** Back to the prime staircase from the opening, its wiggles now understood as the hum of zeros on one line.

## Facts to verify (with sources)
Riemann's 1859 paper (title, length, Berlin Academy, what he claimed "very likely"); Gauss's age/year and the letter to Encke
(1849); Euler product (1737) and Basel problem (1734/35); prime number theorem 1896 and who; Koch 1901 error equivalence
(exact form); first nontrivial zero 14.134725…; Riemann–Siegel and Siegel 1932; Hilbert 1900 (8th problem); Clay 2000 prize;
Hardy 1914; current best proportion of zeros on the line and who; largest verified zero count and who/when (Platt & Trudgian
2021?); Montgomery–Dyson 1972 story; Guth–Maynard 2024 (what exactly); number of primes below 100, 1000, a million, and
Li(x) values used on screen; the exact explicit formula variant used for the wave animation.

## Recurring motif (suggestion for the drafts)
The **prime staircase against the smooth curve**, and a **map of the critical strip** with the critical line where zeros appear
as the video goes on. Pick one as the video's scoreboard-like device with a fixed home; the drafts may propose better.

