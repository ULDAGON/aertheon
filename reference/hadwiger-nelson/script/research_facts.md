# Hadwiger–Nelson video v2: verified fact sheet

Verified on 2026-09-27 against primary or high-trust sources (arXiv papers, the original de Grey paper, Soifer's essay, Quanta, the Polymath16 wiki and blog, MathWorld, and Wikipedia plus the sources it cites).
Confidence levels: **high** means a primary source was read directly, or several independent sources agree. **medium** means one good source, a secondary source, or a recent preprint. **low** means unconfirmed. Do not narrate low-confidence facts.

---

## 0. Quick reference: numbers for the script, with spoken forms

| Item | Value | Spoken form |
|---|---|---|
| Problem posed (Nelson) | 1950, November, age 18, University of Chicago student | "nineteen fifty" |
| Isbell's 7-coloring | 1950, age 20 | "nineteen fifty" |
| Hadwiger's related papers | 1945 and 1961 | "nineteen forty-five", "nineteen sixty-one" |
| Gardner's column | October 1960, *Scientific American* | "nineteen sixty" |
| de Bruijn–Erdős theorem | 1951 | "nineteen fifty-one" |
| Moser spindle | 1961; 7 points, 11 sticks | "seven points and eleven sticks" |
| Golomb graph | 10 points, 18 sticks, 4 colors needed | "ten points" |
| Years with no change in either bound | 1950 to 2018, i.e. 68 years | "sixty-eight years" |
| de Grey's first big graph (N) | 20,425 points | "twenty thousand four hundred and twenty-five" |
| de Grey's published graph (G) | 1,581 points, 7,877 edges | "fifteen hundred and eighty-one" |
| arXiv posting | 8 April 2018 | "April twenty eighteen" |
| Heule's first reduction | 874 points (14 April 2018) | "eight hundred and seventy-four" |
| Current smallest known 5-color graph | 509 points, 2,442 edges (Jaan Parts; found by March 2020; published 2020) | "five hundred and nine" |
| Proven minimum size of any 5-color graph | at least 28 points (lower bound) | "at least twenty-eight" |
| Status today | 5 ≤ χ ≤ 7 | "five, six, or seven" |
| Line | exactly 2 | "two" |
| Three dimensions | 6 ≤ χ ≤ 15 | "between six and fifteen" |
| Measurable colorings (Falconer 1981) | ≥ 5 | "at least five" |
| Valid hexagon side s (7-coloring) | 1/√7 ≈ 0.378 < s < 1/2 | (animator only) |

---

## 1. The problem and who posed it

### 1.1 The question
- **Statement:** What is the smallest number of colors needed to color every point of the plane so that no two points *exactly* one unit apart have the same color? This number is the "chromatic number of the plane," written χ (chi). Other names are the Hadwiger–Nelson problem and CNP.
- **Graph form:** Take every point of the plane as a vertex. Join two points by an edge ("stick") when they are exactly distance 1 apart. χ is the chromatic number of this infinite graph. Its finite subgraphs are called **unit-distance graphs**.
- **Sources:** https://en.wikipedia.org/wiki/Hadwiger%E2%80%93Nelson_problem ; de Grey 2018, §1: https://arxiv.org/abs/1804.02385
- **Confidence:** high.

### 1.2 Why only the exact distance 1 matters, and why the value "1" is arbitrary
- **Fact:** Points closer than 1 or farther than 1 may share a color. Only the exact distance is forbidden.
- **Fact (a simple consequence of scaling):** The choice of unit does not matter. If you forbid distance d instead of 1, scale the whole plane by d. The answer stays the same. "One centimeter" or "one mile" gives the same number.
- **Fact (strong on-ramp for "why it is hard"):** If you also forbid distances in a whole thin band around 1, from 1 − ε to 1 + ε, the answer is known. For every ε > 0 you need at least 7 colors, and for ε small enough exactly 7 colors are enough (the hexagons from section 5 still work). Exoo conjectured this in 2004, and Voronov proved it in a preprint (v1 2023, v3 April 2025). So the "fuzzy" version is settled at 7. Only the razor-sharp exact version is open.
  - Source: Voronov, "The chromatic number of the plane with an interval of forbidden distances is at least 7": https://arxiv.org/abs/2304.10163
  - Confidence: **medium-high**. It is a preprint, revised three times, and a later peer-reviewed paper by the same author uses its techniques. Suggested wording: "mathematicians have shown…", not "it was proven in year X".
- **Misconception to avoid:** "The rule is that nearby points must differ." Wrong. Only pairs at exactly distance 1 must differ.

### 1.3 Edward Nelson, 1950
- **Fact:** Edward Nelson created the problem in **November 1950 at age 18**. At the time he was a student at the University of Chicago. Nelson also noted the lower bound of 4 at that time.
- **Details:** Nelson was born 4 May 1932 and died 10 September 2014. He later became a Princeton mathematician.
- **Sources:** Soifer, "Breakthrough in My Favorite Open Problem of Mathematics" (Geombinatorics 28(1), 2018, concise version): https://www.cs.umd.edu/~gasarch/BLOGPAPERS/soifer.pdf ; Quanta, "then a student at the University of Chicago": https://www.quantamagazine.org/decades-old-graph-problem-yields-to-amateur-mathematician-20180417/ ; de Grey 2018 §1: "first discussed (though not in print) by Nelson in 1950"; https://en.wikipedia.org/wiki/Edward_Nelson
- **Confidence:** high for 1950 and Nelson. The month (November) and the age (18) rest on Soifer, who was Nelson's friend: medium-high.

### 1.4 John Isbell's 7-coloring, 1950
- **Fact:** John R. Isbell, Nelson's 20-year-old friend, found the upper bound of 7 in 1950 with the hexagon coloring. Isbell was born 27 October 1930 (Henriksen gives 1931) and died 6 August 2005.
- **Sources:** Soifer essay (link above): "his 20-year old friend John Isbell … figured out the upper bound of 7"; de Grey 2018 §1: "as first observed by Isbell also in 1950 (see [Soi])"; https://en.wikipedia.org/wiki/John_R._Isbell ; MathWorld: https://mathworld.wolfram.com/Hadwiger-NelsonProblem.html
- **Confidence:** high.

### 1.5 Hugo Hadwiger
- **Facts:** Hugo Hadwiger (23 Dec 1908 – 29 Oct 1981) was a Swiss geometer, born in Karlsruhe, Germany, and professor at Bern.
  - **1945:** In "Überdeckung des euklidischen Raumes durch kongruente Mengen," *Portugaliae Math.* 4 (1945) 238–242, he published a related result: any cover of the plane by **five congruent closed sets** has a unit distance inside one of the sets. The same paper also discussed the hexagon 7-coloring, "though in another context" (de Grey 2018; MathWorld).
  - **1961:** In "Ungelöste Probleme No. 40," *Elemente der Mathematik* 16 (1961) 103–104, he published the problem and made it widely known. Per Soifer, in 1961 Hadwiger said he was not the problem's author.
- **Sources:** https://en.wikipedia.org/wiki/Hugo_Hadwiger ; https://en.wikipedia.org/wiki/Hadwiger%E2%80%93Nelson_problem ; de Grey 2018 §1 ; Soifer essay.
- **Confidence:** high for the years and papers. Medium for the exact content of the 1945 paper, which we did not read directly.
- **Misconception to avoid:** "Hadwiger posed the problem in 1944/1945." He posed a *related* covering question. Nelson posed this problem. The double name came from Hadwiger's related work and his 1961 publication. If the video names the problem, a safe phrasing is: "It is named after Edward Nelson, who asked it, and Hugo Hadwiger, who worked on closely related questions and helped spread it."

### 1.6 First in print: Martin Gardner, October 1960
- **Fact:** The problem first appeared in print in Martin Gardner's "Mathematical Games" column, *Scientific American*, **October 1960**, vol. 203, no. 4, p. 180 ("A new collection of 'brain-teasers'").
- **Sources:** Wikipedia (citing Jensen & Toft 1995, pp. 150–152): https://en.wikipedia.org/wiki/Hadwiger%E2%80%93Nelson_problem ; https://en.wikipedia.org/wiki/Edward_Nelson
- **Confidence:** high for the month and year. Whom Gardner credited is **unverified** (low), so do not narrate it.

### 1.7 Erdős, prizes, opinions (optional color)
- Paul Erdős often posed this problem in his talks. Per Soifer, Erdős thought χ ≥ 5. Soifer conjectures χ = 7.
- Ronald Graham offered prizes: $1000 in 2002 for proving or disproving 4-colorability, $1000 in 2003 for finding the value, and later $100 for showing χ ≥ 5 and $250 for showing χ ≤ 6.
- At a 2009 DIMACS workshop, Soifer took a vote. Apart from one vote for 6 and his own vote for 7, the room split evenly between 4 and 5, which gave a "democratic value" of 4.5.
- Klee & Wagon (1991) quipped that if the problem takes as long as the Four Color Conjecture, "we should know the answer by the year 2084."
- Source: Soifer essay, https://www.cs.umd.edu/~gasarch/BLOGPAPERS/soifer.pdf
- Confidence: medium-high. This is Soifer's first-hand account. Use it only as a light aside.

---

## 2. The one-dimensional warm-up: a line needs exactly 2 colors
- **Fact:** χ(line) = 2. At least 2, because the points 0 and 1 must differ. At most 2, because you can color the half-open intervals [n, n+1) alternately red, blue, red, blue. Any x and x+1 fall in neighboring intervals, which have different colors.
- **Animator note:** Use half-open blocks of length exactly 1. Each boundary point (an integer) belongs to the block on its right. Closed blocks of length 1 would fail, because both ends of one block would be exactly 1 apart.
- **Sources:** Polymath16 wiki table, "ℝ¹: lower 2, upper 2" (archived): https://web.archive.org/web/20220216001534/https://asone.ai/polymath/index.php?title=Hadwiger-Nelson_problem ; the argument above is elementary.
- **Confidence:** high.

---

## 3. Lower bound 3: the unit triangle
- **Fact:** An equilateral triangle with side 1 has three corners that are pairwise 1 apart, so they need 3 different colors. So χ ≥ 3, and 2 colors can never color the plane.
- **Fact:** The smallest graph that needs 3 colors has 3 points: v₃ = 3 (de Grey & Parts 2023).
- **Source:** de Grey & Parts, "On lower bounds of the order of k-chromatic unit distance graphs," Geombinatorics 32(2) (2022), https://arxiv.org/abs/2303.14714
- **Confidence:** high.

---

## 4. Lower bound 4: the Moser spindle (the heart of the video)

### 4.1 Facts
- **Who and when:** The brothers **Leo and William Moser**, published **1961**: L. Moser and W. Moser, "Solution to problem 10," *Canadian Mathematical Bulletin* 4 (1961) 187–189, doi:10.1017/S0008439500025753.
- **Size:** **7 vertices, 11 edges.** It needs 4 colors, and 4 colors are enough for it.
- **Construction:** Take two rhombi with 60° and 120° angles. Each rhombus is two unit equilateral triangles glued along an edge, so its long diagonal is √3. The two rhombi share one acute tip. Rotate one rhombus until its far tip is exactly 1 from the other rhombus's far tip. The edges are 8 rhombus sides, 2 short diagonals, and 1 edge joining the two far tips, for 11 in total.
- **Airtight argument with 3 colors:** In one rhombus, the two middle points are 1 apart, so they take two different colors. Each tip is 1 away from *both* middle points, so each tip must take the third color. So in any 3-coloring, the two tips of a rhombus have the **same** color. Apply this to both rhombi that share the bottom tip A: far tip 1 = color of A, and far tip 2 = color of A. But the far tips are exactly 1 apart, which is a contradiction. So 3 colors fail, and χ ≥ 4.
- **Alternative one-line argument:** No 3 points of the spindle are pairwise non-adjacent (the largest independent set has size 2). With 3 colors, each color could cover at most 2 points, so at most 6 of the 7 points. Checked by computer, see §4.3.
- **Minimality:** 7 is the fewest points possible for a graph that needs 4 colors: v₄ = 7 (de Grey & Parts 2023).
- **Also rigid:** The spindle is a Laman graph (minimally rigid). This is a fun aside and not needed.
- **Sources:** https://en.wikipedia.org/wiki/Moser_spindle ; Soifer, *The Mathematical Coloring Book* (2008) pp. 14–15 ; de Grey 2018 §1 ; https://arxiv.org/abs/2303.14714
- **Confidence:** high.
- **Misconceptions to avoid:**
  - The two rhombi *overlap* and some sticks *cross* in the unit-distance drawing. That is fine, because crossings do not matter. Only the lengths of the sticks matter.
  - The spindle alone does not prove "at least 4" for "all shapes". It proves it for the whole plane, because the spindle sits somewhere in any coloring of the plane (any placement, any rotation).
  - Nelson already knew χ ≥ 4 in 1950. The *spindle* is the famous 1961 witness. Do not say "nobody knew 4 until 1961".

### 4.2 The Golomb graph (optional mention)
- **Fact:** Solomon W. Golomb found a 10-vertex, 18-edge unit-distance graph that also needs 4 colors, at about the same time as the spindle. It is a hexagon with its center, plus an inner equilateral triangle.
- **Sources:** https://en.wikipedia.org/wiki/Golomb_graph ; https://en.wikipedia.org/wiki/Hadwiger%E2%80%93Nelson_problem (citing Soifer 2008 p. 19)
- **Confidence:** high for its size. "Around the same time" is medium, because we have no exact year.

### 4.3 Exact spindle coordinates for the animator (checked numerically)
A symmetric embedding with the shared tip A at the origin and the far tips at the top. With s₃ = √3:
- Rotation angle between the two rhombi: **θ = 2·arcsin(1/(2√3)) ≈ 33.557°** (0.58569 rad).
- A = (0, 0)
- Rhombus 1: B1 ≈ (−0.228714, 0.973494), C1 ≈ (0.728714, 0.684819), far tip **D1 = (1/2, √11/2) ≈ (0.5, 1.658312)**
- Rhombus 2: B2 ≈ (−0.728714, 0.684819), C2 ≈ (0.228714, 0.973494), far tip **D2 = (−1/2, √11/2)**
- Distance from A to each far tip = √3 ≈ 1.732, and D1–D2 = 1.
- Script check (`script/checks/spindle_check.py`): exactly 11 pairs are at distance 1, and there are no accidental extra unit pairs. The closest non-edge pair is B1–C2 at 0.457. The graph is not 3-colorable, is 4-colorable, and its largest independent set has size 2.
- To show "rotate until the tips are one apart," animate rhombus 2 rotating about A from 0° to 33.557°. The tip-to-tip distance is 2√3·sin(φ/2), which passes through exactly 1 at the final angle.

---

## 5. Upper bound 7: the hexagon coloring (Isbell, 1950)

### 5.1 The construction
- **Fact:** Tile the plane with congruent regular hexagons. Use 7 colors in a repeating "flower" pattern: one center hexagon and its 6 neighbors, all different colors. The flower tiles the plane by translation. Every point inside a hexagon gets that hexagon's color.
- **Why it works:**
  1. **Inside one hexagon:** The hexagon's diameter (vertex to opposite vertex) = 2s < 1, so no two points in one hexagon are 1 apart.
  2. **Between same-colored hexagons:** They are separated by **more than 1**, so no two points in different same-colored hexagons are exactly 1 apart either.
- **Exact parameters (checked numerically in `script/checks/hexagon_check.py`):** Regular hexagon with side s.
  - Diameter (vertex to vertex) = **2s**. Width across flats = **√3·s**. Center-to-center spacing of neighboring hexagons = √3·s.
  - In the standard 7-color pattern, the closest same-colored hexagons have centers **√21·s** apart. The minimum gap between their closed regions is **√7·s**.
  - Conditions: 2s < 1 and √7·s > 1, so **1/√7 ≈ 0.37796 < s < 1/2**. Equivalently, diameter 2/√7 ≈ 0.756 < d < 1.
  - Good animation value: **s = 0.45**, giving diameter 0.90, same-color gap ≈ 1.19, and across flats ≈ 0.78. A random test with 200,000 unit segments found no same-colored pair at s = 0.45, but did find violations at s = 0.37 and s = 0.52.
  - Color formula for axial coordinates (q, r) of a pointy-top hex grid with center (√3·s·(q + r/2), 1.5·s·r): **color = (q + 3r) mod 7**. The six neighbors then get the six other colors. The nearest same-color offsets are (1, 2), (3, −1), (2, −3) and their negatives.
- **Sources:** de Grey 2018 §1 ("congruent regular hexagons tiling the plane can be assigned seven colours in a pattern that separates all same-coloured pairs of tiles by more than their diameter"): https://arxiv.org/abs/1804.02385 ; https://en.wikipedia.org/wiki/Hadwiger%E2%80%93Nelson_problem ("diameter slightly less than one"). The numbers were computed and checked for this sheet.
- **Confidence:** high.

### 5.2 The honest note about borders
- Points on a border between hexagons (edges and corners) must still get exactly one color. **Fix:** give each border point the color of *any one* of the hexagons it touches. Because the inequalities are strict (a closed hexagon, border included, still has diameter 2s < 1, and closed same-color hexagons are still √7·s > 1 apart), this never creates a violation. A standard tidy convention is to let each hexagon own half of its border, for example its three "upper" edges and two of its corners.
- **Misconceptions to avoid:**
  - "Hexagons one unit across." The constraint is the **vertex-to-vertex diameter < 1**. With side exactly 1/2, opposite corners of a single hexagon are exactly 1 apart.
  - Do not narrate "each hexagon is one unit wide". Say "just under one unit across, corner to corner."
- Suggested spoken line: "Points on the borders need a tiny bit of bookkeeping. Each one just borrows the color of a neighboring hexagon, and because we left a little room to spare, nothing breaks."

### 5.3 Related facts about "nice" colorings (good for "why it's hard")
- **Tile-style colorings need at least 6.** If every color region is a "tile" (bounded by a Jordan curve, with area bounded below), then at least 6 colors are needed. Woodall proved this in 1973 with a minor error, which Townsend corrected in 2005. Coulson (2004) gave an independent proof. Thomassen (1999) showed that any tile-based 6-coloring would have to be "unscaleable": the largest tile diameter and the smallest same-color separation would both be exactly 1, with no wiggle room.
  - Source: Polymath16 wiki, section "Tile-based colourings" (archived): https://web.archive.org/web/20220216001534/https://asone.ai/polymath/index.php?title=Hadwiger-Nelson_problem ; Wikipedia HN page ("regions bounded by Jordan curves, then at least six colors are required" — Woodall 1973).
  - Confidence: high.
- **Polygon colorings need all 7.** At least 7 colors are needed when the regions are **arbitrary polygons**, and more generally for maps where boundaries are not arcs of unit circles and three boundaries meet at each vertex. This is Sokolov & Voronov: arXiv Feb 2025, published in *Discrete Mathematics* 2026.
  - Source: https://arxiv.org/abs/2502.01958 ; journal listing https://www.sciencedirect.com/science/article/pii/S0012365X26003456
  - Confidence: medium-high. It is recent, the conditions matter, and we saw the journal listing only through a search result.
  - Safe spoken version: "If you insist on coloring with ordinary polygon-shaped patches, you can prove that seven is the best you can do. So if the true answer is five or six, the coloring must be strange in some way."

---

## 6. The long stall, 1950 to 2018
- **Fact:** The bounds 4 ≤ χ ≤ 7 date from 1950. **Neither bound improved until April 2018, a gap of 68 years.** De Grey writes: "Since 1950, no improvement has been made to either bound." Soifer writes: "In 68 years of the problem's life, … no progress has occurred in the general case."
- **Sources:** de Grey 2018 §1 ; Soifer essay ; Aaronson blog, "the first significant progress on the Hadwiger-Nelson problem since 1950": https://scottaaronson.blog/?p=3697
- **Confidence:** high.
- **Nuance:** During the stall there were many results on *restricted* versions: measurable colorings (§9), tile colorings (§5.3), and fractional versions. Say "the main question did not budge", not "nobody made any progress on anything."
- **Spoken options:** "almost seventy years", "sixty-eight years". Quanta and de Grey himself said "60-year-old problem", which is loose.

---

## 7. Aubrey de Grey's 2018 breakthrough: at least 5

### 7.1 Who and when
- **Who:** Aubrey de Grey (born 1963), an English biomedical gerontologist best known for research and advocacy on aging. He was an amateur mathematician with a BA in computer science and a PhD by publication in biology, both from Cambridge. He came into contact with graph theory decades earlier through competitive Othello players who were mathematicians. Quanta says so, and his paper thanks Imre Leader and Graham Brightwell "for their role in germinating my interest in graph theory fully thirty years ago." Soifer's 2008/2009 book inspired him to work on the problem.
- **When:**
  - He worked on it over Christmas 2017 (Quanta).
  - **16 January 2018:** first version emailed to Soifer. That graph later turned out to be 4-colorable, because of a bug in his code. Robert Hochberg's program found the 4-coloring.
  - **7 April 2018:** corrected version.
  - **8 April 2018:** arXiv v1 posted. v2 followed on 11 April and v3 on 30 May 2018.
  - Published in *Geombinatorics* 28(1), July 2018, pp. 18–31 (special issue).
- **Sources:** https://arxiv.org/abs/1804.02385 ; Quanta (Evelyn Lamb, 17 April 2018): https://www.quantamagazine.org/decades-old-graph-problem-yields-to-amateur-mathematician-20180417/ ; Soifer essay ; MathWorld de Grey graphs: https://mathworld.wolfram.com/deGreyGraphs.html ; https://en.wikipedia.org/wiki/Aubrey_de_Grey
- **Confidence:** high.
- **Sensitivity note:** In 2021 de Grey left SENS Research Foundation amid a misconduct investigation. For the video, describe him neutrally and in the past tense ("a biologist best known for his work on aging"). Do not name a current employer.

### 7.2 What it is built from (a faithful, simplified version for narration)
From the paper, §1–§4:
1. **H** = a regular unit hexagon plus its center: **7 points, 12 sticks**. Up to symmetry, H has only **four** essentially different 4-colorings. Two of them contain a **monochromatic triple**: three alternate rim points of one color, forming an equilateral triangle of side √3. The other two do not.
2. **L** (121 points, containing 52 copies of H) is built so that **every 4-coloring forces at least one copy of H to contain a monochromatic triple**.
   - Built as J (31 points = 13 copies of H) → K (61 points = two copies of J, one rotated by 2·arcsin(1/4)) → L (two copies of K, one rotated by 2·arcsin(1/8)).
   - This is a spindle-style trick again: rotate a copy so that a key pair of points lands exactly 1 apart.
3. **M** (1,345 points), built from many interlocking **Moser spindles**, is built so that **no 4-coloring lets its central H contain a monochromatic triple**.
4. **N** = 52 copies of M, one sitting on each copy of H inside L, giving **20,425 points** after merging. L forces a monochromatic triple somewhere, and M forbids it everywhere. So N cannot be 4-colored, and **χ ≥ 5**.
5. He then shrank N by a factor of nearly 13, to the **1,581-point graph G with 7,877 edges**.
- **Narration-friendly summary (accurate):** "It is the spindle's trick scaled up. One structure forces a certain color pattern to appear somewhere. Another structure forbids that pattern. Glue them together, and four colors run out of room."
- **Sources:** de Grey 2018 (read in full, v3) ; Polymath16 wiki table of notable graphs (vertex and edge counts for H, J, K, L, M, N, G).
- **Confidence:** high.

### 7.3 How it was checked
- de Grey wrote a **custom depth-first-search program in Mathematica 11 on a standard MacBook Air**. It exploits "forced" colors: once about 20 colors are fixed, almost all others are forced. It ran "in only a few minutes" for M.
- The 1,581-point graph was small enough for **standard SAT solvers**. "Others have now confirmed its chromatic number to be 5 without the need to resort to using custom code" (de Grey §5.1).
- Scott Aaronson (11 April 2018) reported that the result was "independently verified, using different SAT-solvers," and that Paul Phillips independently checked that all edges really have length 1. Aaronson concluded: "I think it's time to declare the result correct."
- The paper thanks Boris Alexeev, Rob Hochberg, Brendan McKay, Dustin Mixon, Paul Phillips, Landon Rabern and Gordon Royle for testing graphs with independent code.
- **Sources:** https://arxiv.org/abs/1804.02385 §4.3 and §5.1 ; https://scottaaronson.blog/?p=3697 ; Gil Kalai's post: https://gilkalai.wordpress.com/2018/04/10/aubrey-de-grey-the-chromatic-number-of-the-plane-is-at-least-5/
- **Confidence:** high.
- **Misconceptions to avoid:**
  - "The first arXiv version had 1,581 vertices." Per Aaronson, v1 had a **1,567**-vertex graph with a bug, which was fixed to **1,585**. The paper's final record is **1,581**, obtained by deleting 4 more vertices. Use **1,581**. It is the number in the paper, on MathWorld, and on Wikipedia.
  - "A computer found the graph." A human designed it, and computers checked it.
  - Wikipedia's reference list gives the journal pages as 5–18. MathWorld gives **28(1), 18–31**, and Soifer's own essay occupies pp. 5–17 of the same issue, so 18–31 is right. Not narrated anyway.

### 7.4 Independent result: Exoo & Ismailescu
- Geoffrey Exoo and Dan Ismailescu independently proved χ ≥ 5 with different graphs. arXiv 1 May 2018: "The chromatic number of the plane is at least 5 – a new proof." Published in *Discrete & Computational Geometry* 64 (2020) 216–226, doi:10.1007/s00454-019-00058-1. Per Soifer, Exoo said they had their graph "at about the same time as Aubrey de Grey, in January 2018," but took time to polish it, and they acknowledge de Grey's priority.
- **Sources:** https://arxiv.org/abs/1805.00157 ; https://link.springer.com/article/10.1007/s00454-019-00058-1 ; Soifer essay.
- **Confidence:** high for the paper. The January 2018 timing is medium, since it is Soifer relaying Exoo.

---

## 8. Shrinking the graph: Polymath16 and the 509-point record

### 8.1 Polymath16
- **Proposed** by de Grey on 10 April 2018 (polymathprojects.org). Research threads ran on **Dustin Mixon's** blog from 14 April 2018. The project was **declared concluded on 1 February 2021**, after about 1,000 days.
- **Goals:** (1) find smaller 5-chromatic unit-distance graphs; (2) reduce reliance on computers.
- **Participants:** professionals, including **Terence Tao**, per de Grey's closing note, and "at least half a dozen" significant amateur contributors, including de Grey and Jaan Parts.
- **Joint paper:** the one paper under the collective name "D.H.J. Polymath" was about chromatic numbers of disks and strips, in Geombinatorics.
- **Sources:** https://dustingmixon.wordpress.com/2021/02/01/polymath16-seventeenth-thread-declaring-victory/ ; https://polymathprojects.org/2018/04/10/polymath-proposal-finding-simpler-unit-distance-graphs-of-chromatic-number-5/ ; Polymath wiki (archived link in §2).
- **Confidence:** high.

### 8.2 The record, step by step (vertex counts)
| Vertices (edges) | Who | Date | Source |
|---|---|---|---|
| 20,425 (151,311) | de Grey (N) | early 2018 | de Grey 2018; Polymath wiki |
| 1,581 (7,877) | de Grey (G) | Apr 2018 | de Grey 2018 |
| 1,577 | Mixon & Alexeev | Apr 2018 | Quanta; Polymath wiki |
| 874 (4,461) | Marijn Heule | 14 Apr 2018 | Soifer essay; Polymath wiki |
| 826 (4,273) | Heule | 16 Apr 2018 | Soifer essay |
| 803 (4,144) | Heule | 30 Apr 2018 | Soifer essay |
| 633 (3,166) | Heule | 6 May 2018 | Soifer essay |
| 610 (3,000) | Heule | 14 May 2018 | Soifer essay |
| **553** (2,722) | Heule | 18 May 2018 (arXiv 30 May 2018) | https://arxiv.org/abs/1805.12181 |
| 529 | Jaan Parts | 4 Jul 2019 | MathWorld Parts graphs; Polymath wiki |
| 525 / 517 / 510 | Parts and others | Jul–Aug 2019 | MathWorld; Polymath wiki |
| **509 (2,442)** | **Jaan Parts** | found before 7 Mar 2020; paper *Geombinatorics* 29(4) (2020) 137–166; arXiv 23 Oct 2020 | https://arxiv.org/abs/2010.12665 ; https://mathworld.wolfram.com/PartsGraphs.html |

- **Still the record (Sept 2026):** MathWorld's Hadwiger–Nelson page (updated 2 Sept 2026) still lists the 509-vertex Parts graph as the smallest known. Later work by Voronov et al. (2022, 64,513 vertices) and Haugland (Aug 2026, 2,131 vertices) targets graphs *without* Moser spindles and does not beat 509.
  - Sources: https://mathworld.wolfram.com/Hadwiger-NelsonProblem.html ; https://arxiv.org/abs/2106.11824 ; https://arxiv.org/abs/2608.04542
- **Edge note:** The 509-vertex graph is not edge-minimal. de Grey & Parts removed 36 edges, giving 2,406 (https://arxiv.org/abs/2303.14714).
- **Heule's method:** SAT-based "clausal proof minimization." His 553-vertex graphs "can be mechanically validated in a second" (abstract).
- **Human-verifiable proof:** Jaan Parts, "The chromatic number of the plane is at least 5 – a human-verifiable proof," *Geombinatorics* 30(2) (2020) 77–102, arXiv 23 Oct 2020: https://arxiv.org/abs/2010.12661 . de Grey said it could be checked by hand "in no more than a week or two" by someone diligent.
- **Who is Parts:** Jaan Parts is an amateur mathematician (per de Grey's Polymath16 note) based in Kazan, Tatarstan, Russia (per his paper affiliation).
- **Confidence:** high for the counts and dates. Medium for Parts's location and amateur status.
- **Misconceptions to avoid:**
  - Soifer's essay prints Heule's record as "533 vertices". Heule's own abstract says **553**, so 533 is a typo.
  - "509 is the smallest possible." Wrong. It is the smallest *known*. The true minimum is somewhere **between 28 and 509** (§8.3).
  - "Polymath16 found the 509 graph." It came from Parts, who was part of the Polymath16 community. Say "collaborators around the world, working together online, shrank it to five hundred and nine."

### 8.3 How small could they be? (proven lower limits)
- Any unit-distance graph that needs 5 colors must have **at least 28 vertices** (de Grey & Parts 2023, improving Pritikin's > 12 and Gwyn–Stavrianos's ≥ 22).
- A 6-color one would need at least **42** vertices, and a 7-color one more than **6,992** vertices, so at least 6,993 (de Grey & Parts; Parts 2020).
- **Source:** https://arxiv.org/abs/2303.14714 (Geombinatorics 32(2), 2022, 72–74)
- **Confidence:** high, since the paper was read directly.
- **Nice spoken line:** "If the answer is seven, the picture that proves it needs at least about seven thousand points."

---

## 9. Dots and sticks, finite configurations, and axioms

### 9.1 de Bruijn–Erdős theorem (1951)
- **Statement:** For any infinite graph, if every *finite* subgraph can be colored with k colors, then the whole graph can be colored with k colors. So **χ(plane) = the largest chromatic number of any finite unit-distance graph**. If the plane truly needs 6 or 7 colors, some *finite* dots-and-sticks picture proves it.
- **Citation:** N. G. de Bruijn & P. Erdős, "A colour problem for infinite graphs and a problem in the theory of relations," *Nederl. Akad. Wetensch. Proc. Ser. A* 54 (1951) 371–373 (Indagationes Math. 13), doi:10.1016/S1385-7258(51)50053-7.
- **Needs the axiom of choice (in a weak form):** All proofs use some choice principle. The theorem is equivalent to the Boolean prime ideal theorem (Mycielski 1961; Läuchli 1971), which is weaker than full choice. Without some choice it can fail.
- **Sources:** https://en.wikipedia.org/wiki/De_Bruijn%E2%80%93Erd%C5%91s_theorem_(graph_theory) ; Aaronson blog update.
- **Confidence:** high.
- **Important nuance (commonly garbled):** The direction needed for **lower bounds** needs *no* axiom of choice. A finite graph that cannot be 4-colored rules out every 4-coloring of the plane outright. Choice is needed only for the converse: "if the plane needs k colors, some finite picture already needs k."

### 9.2 Could the answer depend on the axioms of set theory? (state cautiously)
- **Fact:** Shelah & Soifer (2003) built distance graphs (not the plane's unit-distance graph itself) whose chromatic number is small (e.g. 2) under ZFC. Under ZF + dependent choice + "every set of reals is Lebesgue measurable" (a system whose consistency Solovay established relative to an inaccessible cardinal), the same graphs need uncountably many colors.
  - They stated a *conditional* theorem: *if* every finite unit-distance graph were 4-colorable, then χ(plane) would be 4 in ZFC but ≥ 5 in ZF + DC + LM, using Falconer's theorem (§9.3).
  - **After de Grey 2018 this particular condition is known to be false**, so that specific scenario is moot.
- **Current accurate status:** It is an **open possibility, not a theorem**, that the answer depends on the axioms. The bounds 5 ≤ χ ≤ 7 hold in both settings: the finite 5-chromatic graph needs no choice, and the hexagon coloring is explicit. The values could differ only if, for example, finite graphs top out at 5 or 6 while colorings with measurable color classes need more.
- **Sources:** Shelah & Soifer, "Axiom of choice and chromatic number of the plane," *J. Combin. Theory Ser. A* 103 (2003) 387–391, doi:10.1016/S0097-3165(03)00102-X ; Wikipedia HN page ("The correct value may depend on the choice of axioms for set theory") ; Wikipedia de Bruijn–Erdős page (the √2 + ℚ example in the Solovay model) ; Aaronson blog ("raises the strange possibility that the chromatic number of the plane could be smaller assuming AC than not assuming it").
- **Confidence:** medium-high for the statements above. We saw the paper's abstract only through secondary sources.
- **Safe spoken version, if used at all:** "There is even a strange possibility, not proven, that the answer could depend on which basic rules of logic you accept for infinite sets." **Do not** say "the answer depends on the axioms" or "it is unprovable".

### 9.3 Measurable colorings: Falconer (1981)
- **Fact:** If every color class must be Lebesgue measurable (roughly, a set whose "area" makes sense), then **at least 5 colors** are needed. K. J. Falconer, "The realization of distances in measurable subsets covering ℝⁿ," *J. Combin. Theory Ser. A* 31 (1981) 184–189. The hexagon coloring is measurable, so the measurable version is also in {5, 6, 7}.
- **Sources:** https://arxiv.org/abs/2502.01958 (intro) ; search-verified citation ; Wikipedia HN "Variations" (Croft–Falconer–Guy 1991).
- **Confidence:** high.
- **Related (optional, advanced):** In 2022–2023, Ambrus, Csiszárik, Matolcsi, Varga and Zsámboki proved Erdős's conjecture that a measurable planar set with no two points at distance 1 has density < 1/4, with upper bound 0.2470 (https://arxiv.org/abs/2207.14179). A June 2026 preprint by Dúcz & Varga claims a finite unit-distance graph with independence ratio < 1/4, which would imply fractional chromatic number > 4 (https://arxiv.org/abs/2606.28157). That claim is unrefereed: **do not narrate**.

---

## 10. Three dimensions and beyond
- **Line:** exactly 2. **Plane:** 5, 6 or 7. **Space (3D): between 6 and 15.**
  - Lower bound 6: O. Nechushtan, "On the space chromatic number," *Discrete Mathematics* 256 (2002). Polymath16 later found a 59-vertex, 183-edge 6-chromatic unit-distance graph in 3D.
  - Upper bound 15: D. Coulson, "A 15-colouring of 3-space omitting distance one," *Discrete Math.* 256 (2002) 83–90 ; independently Radoičić & Tóth (2003), https://www.cs.bme.hu/~geza/chromatic.pdf
  - No improvement to either 3D bound has been found as of Sept 2026. Searches turned up only results for variants such as "slices".
- **High dimensions:** growth is exponential. Frankl & Wilson (1981) proved an exponential lower bound. The known range is roughly (1.239…)ⁿ to (3 + o(1))ⁿ.
- **Sources:** https://en.wikipedia.org/wiki/Hadwiger%E2%80%93Nelson_problem (Variations) ; Polymath wiki higher-dimension table (archived) ; https://www.researchgate.net/publication/220188330_On_the_space_chromatic_number
- **Confidence:** high for 6 and 15.
- **Misconception:** "3D is 15." It is only an upper bound. Soifer *conjectures* 15.

---

## 11. Status today (as of September 2026)
- **5 ≤ χ ≤ 7.** No unit-distance graph needing 6 colors is known. No 6-coloring of the plane is known.
- The smallest known 5-chromatic graph has **509** points (Parts).
- The "fuzzy" version (forbidding a thin band of distances) is settled at exactly 7 (Voronov preprint; §1.2).
- Polygon-patch colorings need 7 (Sokolov–Voronov 2025/2026; §5.3).
- A 2025 ICML paper (Mundinger, Zimmer, Kiem, Spiegel, Pokutta) used neural networks to find two new 6-colorings for an "off-diagonal" *variant*, the first improvement on that variant in 30 years. This is optional, and it must be called a variant, not progress on the main problem (https://arxiv.org/abs/2501.18527).
- **Sources:** MathWorld (updated 2 Sep 2026): https://mathworld.wolfram.com/Hadwiger-NelsonProblem.html ; Wikipedia HN.
- **Confidence:** high for the bounds.

---

## 12. Why it is hard (claims that are safe to say)
1. **Lower bounds need a finite "certificate"**: a specific configuration of points that cannot be colored. These are hard to design, and checking them needs heavy computation (SAT solvers). No 6-color configuration is known, and one would need at least 42 points. A 7-color one would need at least 6,993.
2. **Upper bounds need a coloring of the entire infinite plane.** Every "nice" coloring (tiles or polygons) provably needs 6 or 7. So a 5- or 6-coloring, if one exists, must be irregular.
3. **The exact distance is razor-thin.** Blur the rule even slightly and the answer snaps to 7. The open question lives entirely in the exactness.
4. **Infinity and logic:** reducing the problem to finite pictures already uses a (weak) axiom of choice, and it is conceivable, though unproven, that the answer depends on set-theoretic axioms.

---

## 13. Timeline (for an on-screen strip)
- 1945: Hadwiger's related covering result, which includes the hexagon 7-coloring in another context.
- Nov 1950: Nelson (18) asks the question and notes χ ≥ 4. Isbell (20) finds χ ≤ 7.
- 1951: de Bruijn–Erdős theorem.
- Oct 1960: first in print (Gardner, *Scientific American*).
- 1961: Moser spindle published. Hadwiger's "Ungelöste Probleme No. 40".
- 1981: Falconer, measurable colorings ≥ 5.
- 2002/2003: 3D bounds 6 (Nechushtan) and 15 (Coulson; Radoičić–Tóth).
- 2003: Shelah–Soifer on the axiom of choice.
- 8 Apr 2018: de Grey on arXiv, χ ≥ 5 (1,581 points).
- 10–14 Apr 2018: Polymath16 begins. 14 Apr: Heule 874.
- 1 May 2018: Exoo–Ismailescu independent proof.
- 18 May 2018: Heule 553.
- 2019–2020: Parts 529 → 510 → **509**. Parts's human-verifiable proof (2020).
- 1 Feb 2021: Polymath16 declares victory.
- 2025: map/polygon colorings need 7 (Sokolov–Voronov). Neural-network 6-colorings for a variant.
- Sept 2026: still 5, 6 or 7.

---

## 14. Pronunciation notes (for TTS)
- Hadwiger: HAHD-vig-er (Swiss German; the engine fixes this).
- Nelson: NEL-sun. Isbell: IZ-bel.
- Moser: MOH-zer. Golomb: GOL-um.
- Aubrey de Grey: AW-bree duh GRAY.
- Erdős: AIR-dush. de Bruijn: duh BROWN (Dutch "bruyn").
- Marijn Heule: mah-RINE HER-luh (approximate).
- Jaan Parts: YAHN PARTS (Estonian first name).
- Exoo: EK-soh. Ismailescu: ish-mah-yee-LES-koo.
- Soifer: SOY-fer. Falconer: FAL-kun-er (British "FAWL-kner" also used). Polymath: POL-ee-math.

---

## 15. Do-not-say list (common errors)
- "Nobody has made progress since 1950." Wrong: de Grey did in 2018. The bounds were only *frozen* until then.
- "The answer is 4, 5, 6 or 7." That is out of date since 2018. It is now **5, 6 or 7**.
- "Two points close together can't share a color." Wrong: only *exactly* distance 1 matters.
- "Hexagons one unit wide." Wrong: the corner-to-corner diameter must be *less than* 1, and the side between about 0.378 and 0.5.
- "de Grey's graph has 1,567 / 1,585 points." Use **1,581**, the published graph.
- "Heule found a 533-point graph." Wrong: **553**.
- "509 is the minimum possible." Wrong: it is the smallest *known*. The true minimum is between 28 and 509.
- "A computer solved it." Wrong: a human construction, with computer *verification*.
- "The problem is proven to depend on the axioms / to be unprovable." Wrong: that is only an open possibility.
- "Hadwiger posed the problem." Nelson posed it. Hadwiger worked on related questions and spread it.
- "The Moser spindle has 7 points and 12 sticks." It has **11**. (H, the hexagon plus center, has 12.)
- "3D needs 15 colors." That is only an upper bound. The known range is 6 to 15.

---

## 16. Source list
- Wikipedia, Hadwiger–Nelson problem (wikitext read in full): https://en.wikipedia.org/wiki/Hadwiger%E2%80%93Nelson_problem
- de Grey, "The chromatic number of the plane is at least 5," arXiv:1804.02385 (v3 read in full): https://arxiv.org/abs/1804.02385
- Soifer, "Breakthrough in My Favorite Open Problem of Mathematics: Chromatic Number of the Plane" (read in full): https://www.cs.umd.edu/~gasarch/BLOGPAPERS/soifer.pdf
- Quanta, Evelyn Lamb, 17 Apr 2018: https://www.quantamagazine.org/decades-old-graph-problem-yields-to-amateur-mathematician-20180417/
- Scott Aaronson, 11 Apr 2018: https://scottaaronson.blog/?p=3697
- Gil Kalai, 10 Apr 2018: https://gilkalai.wordpress.com/2018/04/10/aubrey-de-grey-the-chromatic-number-of-the-plane-is-at-least-5/
- Polymath16 wiki (archived Feb 2022): https://web.archive.org/web/20220216001534/https://asone.ai/polymath/index.php?title=Hadwiger-Nelson_problem
- Mixon, "Polymath16, seventeenth thread: Declaring victory," 1 Feb 2021: https://dustingmixon.wordpress.com/2021/02/01/polymath16-seventeenth-thread-declaring-victory/
- Heule, arXiv:1805.12181: https://arxiv.org/abs/1805.12181
- Exoo & Ismailescu, arXiv:1805.00157 / DCG 64 (2020): https://arxiv.org/abs/1805.00157
- Parts, 509-vertex graph, arXiv:2010.12665: https://arxiv.org/abs/2010.12665
- Parts, human-verifiable proof, arXiv:2010.12661: https://arxiv.org/abs/2010.12661
- de Grey & Parts, lower bounds on order, arXiv:2303.14714 (read in full): https://arxiv.org/abs/2303.14714
- MathWorld, Hadwiger–Nelson problem (updated 2 Sep 2026): https://mathworld.wolfram.com/Hadwiger-NelsonProblem.html ; Parts graphs: https://mathworld.wolfram.com/PartsGraphs.html ; de Grey graphs: https://mathworld.wolfram.com/deGreyGraphs.html
- Wikipedia: Moser spindle https://en.wikipedia.org/wiki/Moser_spindle ; Golomb graph https://en.wikipedia.org/wiki/Golomb_graph ; de Bruijn–Erdős theorem https://en.wikipedia.org/wiki/De_Bruijn%E2%80%93Erd%C5%91s_theorem_(graph_theory) ; Edward Nelson https://en.wikipedia.org/wiki/Edward_Nelson ; John R. Isbell https://en.wikipedia.org/wiki/John_R._Isbell ; Hugo Hadwiger https://en.wikipedia.org/wiki/Hugo_Hadwiger ; Aubrey de Grey https://en.wikipedia.org/wiki/Aubrey_de_Grey
- Voronov, forbidden interval ≥ 7: https://arxiv.org/abs/2304.10163
- Sokolov & Voronov, map-type colorings ≥ 7: https://arxiv.org/abs/2502.01958
- Voronov, Neopryatnaya, Dergachev (spindle-free 5-chromatic, Discrete Math 2022): https://arxiv.org/abs/2106.11824
- Haugland (spindle-free, 2,131 vertices, Aug 2026): https://arxiv.org/abs/2608.04542
- Cranston & Rabern, fractional chromatic number ≥ 76/21: https://arxiv.org/abs/1501.01647
- Ambrus et al., density < 1/4: https://arxiv.org/abs/2207.14179
- Mundinger et al., neural 6-colorings (ICML 2025): https://arxiv.org/abs/2501.18527
- Radoičić & Tóth, 3-space: https://www.cs.bme.hu/~geza/chromatic.pdf
- Nechushtan, 3-space ≥ 6: https://www.researchgate.net/publication/220188330_On_the_space_chromatic_number
- Verification scripts (spindle and hexagon numerics): `script/checks/spindle_check.py` and `hexagon_check.py` in the original build (not kept in this reference)

