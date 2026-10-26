# Фонетические правила: Quenya / Qenya

Источник: Eldamo 0.8.13 © Paul Strack, CC BY 4.0. Файл создан `scripts/build.py`; не править вручную.

Правил: 387 (с порядком Eldamo: 261); подформул: 1186; засвидетельствованных дериваций: 3957; формулы воспроизводят 94.0% шагов с известной формулой.

Столбец «примеры» — число засвидетельствованных шагов дериваций с этой подформулой / сколько из них формула воспроизводит.

## ✶ Primitive Elvish (поздняя концепция)

### [[lr] became [ll]](https://eldamo.org/content/words/word-4183190863.html)

- порядок 00100

| подформула | вид | примеры |
|---|---|---|
| `lr > ll` | literal | — |

### [[ae], [ao] became [ā]](https://eldamo.org/content/words/word-1056240093.html)

- порядок 00200
- общая формула `a{eo} > ā`

| подформула | вид | примеры |
|---|---|---|
| `ae > ā` | literal | — |
| `ao > ā` | literal | — |

### [[j], [w] became [i], [u] before consonants](https://eldamo.org/content/words/word-113345945.html)

- порядок 00300
- общая формула `V{jw}C > V{iu}C`

| подформула | вид | примеры |
|---|---|---|
| `ajC > aiC` | contextual | 12 / 12 |
| `ejC > eiC` | contextual | 1 / 1 |
| `ojC > oiC` | contextual | 3 / 0 |
| `ujC > uiC` | contextual | — |
| `awC > auC` | contextual | 9 / 9 |
| `ewC > euC` | contextual | — |
| `iwC > iuC` | contextual | — |
| `owC > ouC` | contextual | — |

### [[bm], [dn] became [mb], [nd]](https://eldamo.org/content/words/word-3882201769.html)

- общая формула `bm|dn > mb|nd`

| подформула | вид | примеры |
|---|---|---|
| `bm > mb` | literal | 6 / 6 |
| `dn > nd` | literal | 1 / 1 |

### [[hs] became [ss]](https://eldamo.org/content/words/word-2177009433.html)

- раньше, чем: medial [ɣ]/[h] vanished except before [t]

| подформула | вид | примеры |
|---|---|---|
| `hs > ss` | literal | 3 / 2 |

### [[lɣ] became [lg]](https://eldamo.org/content/words/word-2151845509.html)

| подформула | вид | примеры |
|---|---|---|
| `lɣ > lg` | literal | — |

### [[pw], [pʰw] became [pp], [pʰp]](https://eldamo.org/content/words/word-2859678213.html)

- общая формула `pw|pʰw > pp|pʰpʰ`
- раньше, чем: aspiration moved to end of group of stops

| подформула | вид | примеры |
|---|---|---|
| `pw > pp` | literal | — |
| `pʰw > ppʰ` | literal | — |

### [[s] became [z] before voiced stops](https://eldamo.org/content/words/word-882174441.html)

- общая формула `s{bdg} > z{bdg}`

| подформула | вид | примеры |
|---|---|---|
| `sb > zb` | literal | — |
| `sd > zd` | literal | 1 / 1 |
| `sg > zg` | literal | 1 / 1 |

### [[t+t], [d+d] from suffixion became [st], [zd]](https://eldamo.org/content/words/word-2479050823.html)

- общая формула `{ttʰd}+t|d+d > st|zd`

| подформула | вид | примеры |
|---|---|---|
| `t+t > st` | contextual | 5 / 0 |
| `tʰ+t > st` | contextual | 2 / 0 |
| `d+t > st` | contextual | — |
| `d+d > zd` | contextual | 8 / 0 |

### [[tk] became [kk] or [kt] or [sk]](https://eldamo.org/content/words/word-700934409.html)

- общая формула `tk > kk`

| подформула | вид | примеры |
|---|---|---|
| `tk > kk` | literal | 2 / 2 |
| `tk > kt` | literal | — |
| `tk > sk` | literal | — |
| `tp > pp` | literal | 2 / 2 |

### [[wau] became [au] or [wā]](https://eldamo.org/content/words/word-242344611.html)

- общая формула `wau > au|wā`

| подформула | вид | примеры |
|---|---|---|
| `wau > au` | literal | — |
| `wau > wā` | literal | 1 / 1 |

### [[wou] became [wō]](https://eldamo.org/content/words/word-3116232193.html)

- раньше, чем: stressed [wŏ] became [wa]

| подформула | вид | примеры |
|---|---|---|
| `wou > wō` | literal | — |

### [[ŋs] became [ns]](https://eldamo.org/content/words/word-484908271.html)

- общая формула `ŋs > ns`

| подформула | вид | примеры |
|---|---|---|
| `ŋs > ns` | literal | — |

### [[ŋŋ], [ŋɣ] became [ŋg]](https://eldamo.org/content/words/word-3404492995.html)

- общая формула `ŋ{ŋɣ} > ŋg`

| подформула | вид | примеры |
|---|---|---|
| `ŋŋ > ŋg` | literal | 3 / 3 |
| `ŋɣ > ŋg` | literal | — |

### [aspirate became voiceless stop before [s]](https://eldamo.org/content/words/word-2225058767.html)

- общая формула `{ptk}ʰs > {ptk}s`

| подформула | вид | примеры |
|---|---|---|
| `pʰs > ps` | literal | — |
| `tʰs > ts` | literal | — |
| `kʰs > ks` | literal | — |

### [aspirates became voiceless stops after [s], [h]](https://eldamo.org/content/words/word-3915424757.html)

- общая формула `s{ptk}ʰ|htʰ > s{ptk}|ht`

| подформула | вид | примеры |
|---|---|---|
| `spʰ > sp` | literal | — |
| `stʰ > st` | literal | — |
| `skʰ > sk` | literal | 1 / 1 |
| `htʰ > ht` | literal | — |

### [aspiration moved to end of group of stops](https://eldamo.org/content/words/word-3183451073.html)

- общая формула `{ptk}ʰ{ptk|pʰtʰkʰ} > {ptk}{ptk}ʰ`
- позже, чем: [pw], [pʰw] became [pp], [pʰp]; voiced stops unvoiced after voiceless stops and aspirates

| подформула | вид | примеры |
|---|---|---|
| `pʰt > ptʰ` | literal | — |
| `pʰtʰ > ptʰ` | literal | — |
| `tʰt > ttʰ` | literal | — |
| `tʰk > tkʰ` | literal | 1 / 1 |
| `tʰtʰ > ttʰ` | literal | — |
| `kʰt > ktʰ` | literal | 2 / 2 |
| `kʰk > kkʰ` | literal | 1 / 1 |

### [final [j], [w] became [i], [u]](https://eldamo.org/content/words/word-2641132585.html)

- общая формула `-{jw} > -{iu}`
- позже, чем: final [j], [w] vanished after long vowels in monosyllables

| подформула | вид | примеры |
|---|---|---|
| `-j > -i` | literal | — |
| `-w > -u` | literal | 1 / 1 |

### [final [j], [w] vanished after long vowels in monosyllables](https://eldamo.org/content/words/word-1539930001.html)

- общая формула `CV̄{jw} > CV̄`
- раньше, чем: final [j], [w] became [i], [u]

| подформула | вид | примеры |
|---|---|---|
| `Cāj > Cā` | contextual | 1 / 1 |
| `Cāw > Cā` | contextual | 2 / 2 |

### [final [l] became [r]](https://eldamo.org/content/words/word-3385004377.html)

| подформула | вид | примеры |
|---|---|---|
| `-l > -r` | literal | — |

### [final [m] became [n]](https://eldamo.org/content/words/word-760163573.html)

| подформула | вид | примеры |
|---|---|---|
| `-m > -n` | literal | 1 / 1 |

### [long vowels shortened before consonant clusters](https://eldamo.org/content/words/word-542079381.html)

| подформула | вид | примеры |
|---|---|---|
| `V̄CC > V̆CC` | contextual | 2 / 2 |

### [medial [ŋ] usually became [ɣ]](https://eldamo.org/content/words/word-768986721.html)

- общая формула `VŋV|ŋ{rl}|-ŋ > VɣV|ɣ{rl}|-ɣ`
- раньше, чем: [ɣ] from [g] vanished
- позже, чем: medial [ŋj], [ŋw] became [ŋgj], [ŋgw]; nasals assimilated to following stops and aspirates

| подформула | вид | примеры |
|---|---|---|
| `VŋV > VɣV` | contextual | 12 / 11 |
| `-Vŋ > -Vɣ` | contextual | 1 / 1 |
| `ŋr > ɣr` | literal | — |
| `ŋl > ɣl` | literal | — |
| `-ŋ > -ɣ` | literal | 2 / 2 |

### [medial [ŋj], [ŋw] became [ŋgj], [ŋgw]](https://eldamo.org/content/words/word-2233951333.html)

- общая формула `-ŋ{wj}- > -ŋg{wj}-`
- раньше, чем: medial [ŋ] usually became [ɣ]

| подформула | вид | примеры |
|---|---|---|
| `-ŋw- > -ŋgw-` | literal | 7 / 7 |
| `-ŋj- > -ŋgj-` | literal | — |

### [medial [ɣ]/[h] vanished except before [t]](https://eldamo.org/content/words/word-2690267141.html)

- общая формула `-h-|VhC|ht > -ø-|V̄øC|xt`
- позже, чем: [hs] became [ss]

| подформула | вид | примеры |
|---|---|---|
| `-h- > -ø-` | loss | 2 / 1 |
| `-ɣ- > -ø-` | loss | 23 / 17 |
| `aɣC > āC` | contextual | — |
| `eɣC > ēC` | contextual | 2 / 1 |
| `iɣC > īC` | contextual | 1 / 1 |
| `uɣC > ūC` | contextual | — |
| `ht > xt` | literal | — |

### [medial nasal plus stop after another consonant became simple nasal](https://eldamo.org/content/words/word-4126101193.html)

- общая формула `-C{mnŋ}{bdg}- > -C{mnŋ}-`

| подформула | вид | примеры |
|---|---|---|
| `-Cmb- > -Cm-` | contextual | — |
| `-Cnd- > -Cn-` | contextual | — |
| `-Cŋg- > -Cŋ-` | contextual | — |

### [metathesis](https://eldamo.org/content/words/word-3160359587.html)

- общая формула `km > mk`

| подформула | вид | примеры |
|---|---|---|
| `km > mk` | literal | 1 / 1 |
| `sl > ls` | literal | 1 / 1 |

### [nasals assimilated to following stops and aspirates](https://eldamo.org/content/words/word-2143444883.html)

- общая формула `{nŋ}{ppʰb}|{mŋ}{ttʰd}|{mn}{kkʰg} > m{ppʰb}|n{ttʰd}|ŋ{kkʰg}`
- раньше, чем: medial [ŋ] usually became [ɣ]

| подформула | вид | примеры |
|---|---|---|
| `np > mp` | literal | 5 / 5 |
| `nb > mb` | literal | 2 / 2 |
| `ŋp > mp` | literal | — |
| `mt > nt` | literal | 4 / 4 |
| `md > nd` | literal | 3 / 3 |
| `ŋt > nt` | literal | — |
| `mk > ŋk` | literal | 1 / 1 |
| `nk > ŋk` | literal | 4 / 4 |

### [short final [e], [a], [o] vanished](https://eldamo.org/content/words/word-2794740763.html)

- общая формула `-S{ĕăŏǝ} > -Sø`

| подформула | вид | примеры |
|---|---|---|
| `-Sǝ > -Sø` | contextual | — |
| `-Sĕ > -Sø` | contextual | 15 / 15 |
| `-Să > -Sø` | contextual | 42 / 42 |
| `-Sŏ > -Sø` | contextual | 26 / 26 |

### [short final [i], [u] became [e], [o]](https://eldamo.org/content/words/word-3064357955.html)

- общая формула `-S{ĭŭ} > -S{eo}`

| подформула | вид | примеры |
|---|---|---|
| `-Sĭ > -Se` | contextual | 95 / 91 |
| `-Sŭ > -So` | contextual | 12 / 12 |

### [stressed [wŏ] became [wa]](https://eldamo.org/content/words/word-1475928117.html)

- общая формула `wŏ́ > wa`
- позже, чем: [wou] became [wō]

| подформула | вид | примеры |
|---|---|---|
| `wŏ́ > wa` | literal | 4 / 4 |
| `wa > wo` | literal | 3 / 3 |

### [unstressed long vowels shortened in medial syllables](https://eldamo.org/content/words/word-951924569.html)

| подформула | вид | примеры |
|---|---|---|
| `ˌV̄S > V̆S` | contextual | — |

### [voiced stops unvoiced after voiceless stops and aspirates](https://eldamo.org/content/words/word-2620200719.html)

- общая формула `{pʰtʰkʰptk}{bdg}|{bdg}{pʰtʰkʰptk} > {pʰtʰkʰptk}{ptk}|{ptk}{pʰtʰkʰptk}`
- раньше, чем: aspiration moved to end of group of stops

| подформула | вид | примеры |
|---|---|---|
| `kd > kt` | literal | 1 / 1 |
| `sd > st` | literal | 2 / 2 |

### [voiced stops unvoiced before voiceless consonants](https://eldamo.org/content/words/word-1944249607.html)

- общая формула `{bdg}{ptkpʰtʰkʰs} > {ptk}{ptkpʰtʰkʰs}`

| подформула | вид | примеры |
|---|---|---|
| `bt > pt` | literal | 1 / 1 |
| `bs > ps` | literal | 1 / 1 |
| `dt > tt` | literal | — |
| `ds > ts` | literal | — |
| `gt > kt` | literal | 9 / 9 |
| `gs > ks` | literal | — |
| `ɣk > kk` | literal | — |

## AQ. Ancient Quenya (поздняя концепция)

### [[ms] became [ns]](https://eldamo.org/content/words/word-1399041717.html)

- порядок 00100
- раньше, чем: [ns] became [ss]

| подформула | вид | примеры |
|---|---|---|
| `ms > ns` | literal | — |

### [[ns] became [ss]](https://eldamo.org/content/words/word-2591378297.html)

- порядок 00200
- общая формула `ns > ss`
- позже, чем: [ms] became [ns]

| подформула | вид | примеры |
|---|---|---|
| `ns > ss` | literal | — |
| `nz > ns` | literal | 1 / 1 |

### [second short vowel of same quality lost](https://eldamo.org/content/words/word-3116715705.html)

- порядок 00300
- общая формула `V₁CV̆₁CV > V₁CCV`
- раньше, чем: stops frequently underwent metathesis with nasals and liquids; voiced stops became spirants except after nasals; later [j], [w] became [i], [u] before consonants; medial [s] often became [z]; unstressed medial long vowels shortened; [ln] became [ld]

| подформула | вид | примеры |
|---|---|---|
| `aCaCV > aCCV` | contextual | 51 / 47 |
| `eCeCV > eCCV` | contextual | 41 / 36 |
| `iCiCV > iCCV` | contextual | 7 / 6 |
| `oCoCV > oCCV` | contextual | 15 / 15 |
| `uCuCV > uCCV` | contextual | 4 / 4 |

### [later [j], [w] became [i], [u] before consonants](https://eldamo.org/content/words/word-2232975397.html)

- порядок 00400
- общая формула `VjC|VwC > ViC|VuC`
- раньше, чем: voiced stops became spirants except after nasals
- позже, чем: second short vowel of same quality lost

| подформула | вид | примеры |
|---|---|---|
| `VjC > ViC` | contextual | 3 / 3 |
| `VwC > VuC` | contextual | 5 / 5 |

### [[ls] became [ll] or [ld]](https://eldamo.org/content/words/word-367860887.html)

- порядок 00500
- общая формула `ls > ll`

| подформула | вид | примеры |
|---|---|---|
| `ls > ll` | literal | — |

### [stops frequently underwent metathesis with nasals and liquids](https://eldamo.org/content/words/word-3192302915.html)

- порядок 00600
- общая формула `{ptk}{mnŋlr}|{pʰtʰkʰbdg}{mnŋ}|{tʰd}l > {mnŋlr}{ptk}|{mnŋ}{pʰtʰkʰbdg}|l{tʰd}`
- раньше, чем: [nl], [nr] became [ll], [rr]
- позже, чем: second short vowel of same quality lost

| подформула | вид | примеры |
|---|---|---|
| `kl > lk` | literal | 21 / 21 |
| `ml > lm` | literal | 1 / 1 |
| `pn > np` | literal | 5 / 5 |
| `tn > nt` | literal | — |
| `bm > mb` | literal | 1 / 1 |
| `pm > mp` | literal | — |
| `pn > mp` | literal | — |
| `kn > ŋk` | literal | 1 / 1 |
| `tr > rt` | literal | 4 / 4 |
| `dl > ld` | literal | 2 / 2 |

### [[nl], [nr] became [ll], [rr]](https://eldamo.org/content/words/word-1625553255.html)

- порядок 00700
- общая формула `nl|nr > ll|rr`
- раньше, чем: [r], [l] often became syllabic in clusters
- позже, чем: stops frequently underwent metathesis with nasals and liquids

| подформула | вид | примеры |
|---|---|---|
| `nl > ll` | literal | — |
| `nr > rr` | literal | — |
| `anr > ār` | literal | 1 / 1 |

### [[sr] became [ss]](https://eldamo.org/content/words/word-1606156545.html)

- порядок 00800
- раньше, чем: medial [s] often became [z]

| подформула | вид | примеры |
|---|---|---|
| `sr > ss` | literal | — |

### [[rl] and [lr] became [ll]](https://eldamo.org/content/words/word-1550655669.html)

- порядок 00900
- общая формула `rl|lr > ll|ll`
- раньше, чем: [r], [l] often became syllabic in clusters

| подформула | вид | примеры |
|---|---|---|
| `rl > ll` | literal | 1 / 1 |
| `lr > ll` | literal | — |

### [[r], [l] often became syllabic in clusters](https://eldamo.org/content/words/word-825670671.html)

- порядок 01000
- общая формула `V₁Cḷ|CCr > V₁CV₁l|CCar`
- раньше, чем: [r] became [s] after voiceless stops and aspirates
- позже, чем: [nl], [nr] became [ll], [rr]; [rl] and [lr] became [ll]

| подформула | вид | примеры |
|---|---|---|
| `aCCl > aCCal` | contextual | 4 / 4 |
| `CCr > CCar` | contextual | 3 / 3 |
| `-Cr > -Car` | contextual | — |

### [[r] became [s] after voiceless stops and aspirates](https://eldamo.org/content/words/word-1071202939.html)

- порядок 01100
- общая формула `{ptkpʰtʰkʰ}r > {ptkpʰtʰkʰ}s`
- раньше, чем: aspirates became voiceless spirants
- позже, чем: [r], [l] often became syllabic in clusters

| подформула | вид | примеры |
|---|---|---|
| `pr > ps` | literal | — |
| `tr > ts` | literal | — |
| `kr > ks` | literal | 2 / 2 |
| `pʰr > ps` | literal | — |
| `tʰr > ts` | literal | — |
| `kʰr > ks` | literal | — |
| `ntr > ns` | literal | — |

### [initial [d] assimilated to following nasal](https://eldamo.org/content/words/word-2885687903.html)

- порядок 01200
- раньше, чем: initial [d] became [l]

| подформула | вид | примеры |
|---|---|---|
| `dVXn- > nVXn-` | contextual | 4 / 3 |

### [initial [ɣ] became [h]](https://eldamo.org/content/words/word-3316553555.html)

- порядок 01300
- раньше, чем: voiced stops became spirants except after nasals

| подформула | вид | примеры |
|---|---|---|
| `ɣ- > h-` | literal | — |

### [combinations of voiced stops were unvoiced](https://eldamo.org/content/words/word-1625077395.html)

- порядок 01400
- общая формула `{bdg}{bdg} > {ptk}{ptk}`
- раньше, чем: voiced stops became spirants except after nasals

| подформула | вид | примеры |
|---|---|---|
| `bb > pp` | literal | 1 / 1 |
| `bd > pt` | literal | 1 / 1 |
| `bg > pk` | literal | — |
| `db > tp` | literal | — |
| `dd > tt` | literal | — |
| `dg > tk` | literal | — |
| `gb > kp` | literal | — |
| `gd > kt` | literal | 3 / 3 |
| `gg > kk` | literal | — |

### [[z] plus voiced stop became unvoiced](https://eldamo.org/content/words/word-3279729471.html)

- порядок 01500
- общая формула `z{bdg} > s{ptk}`
- раньше, чем: voiced stops became spirants except after nasals; [sp], [sk] became [ps], [ks]

| подформула | вид | примеры |
|---|---|---|
| `z{bdg} > s{ptk}` | contextual | — |
| `zb > sp` | literal | 1 / 1 |
| `zd > st` | literal | 13 / 12 |
| `zg > sk` | literal | 3 / 3 |

### [[n], [m] became [t], [w] after voiceless stops and aspirates](https://eldamo.org/content/words/word-3418086257.html)

- порядок 01600
- общая формула `{ptk}{nm}|{ptk}ʰ{nm} > {ptk}{tw}|{ptk}ʰ{tw}`
- раньше, чем: aspirates became voiceless spirants; voiced stops became nasals before nasals; [pw] became [pp]

| подформула | вид | примеры |
|---|---|---|
| `pn > pt` | literal | — |
| `tn > tt` | literal | 1 / 1 |
| `kn > kt` | literal | 1 / 1 |
| `pm > pw` | literal | 1 / 1 |
| `tm > tw` | literal | — |
| `km > kw` | literal | 1 / 1 |
| `pʰn > pt` | literal | — |
| `tʰn > tt` | literal | 1 / 1 |
| `kʰn > kt` | literal | — |
| `pʰm > pw` | literal | — |
| `tʰm > tw` | literal | — |
| `kʰm > kw` | literal | — |

### [nasals became voiceless stops before aspirates](https://eldamo.org/content/words/word-3474357431.html)

- порядок 01700
- общая формула `mpʰ|ntʰ|ŋkʰ > ppʰ|ttʰ|kkʰ`
- раньше, чем: aspirates became voiceless spirants; spirants became stops after nasals

| подформула | вид | примеры |
|---|---|---|
| `mpʰ > ppʰ` | literal | 1 / 1 |
| `ntʰ > ttʰ` | literal | 1 / 1 |
| `ŋkʰ > kkʰ` | literal | — |

### [aspirates became voiceless stops after voiceless stops](https://eldamo.org/content/words/word-2190887743.html)

- порядок 01800
- общая формула `{ptk}{ptk}ʰ > {ptk}{ptk}`
- раньше, чем: aspirates became voiceless spirants

| подформула | вид | примеры |
|---|---|---|
| `ppʰ > pp` | literal | 1 / 1 |
| `ptʰ > pt` | literal | — |
| `pkʰ > pk` | literal | — |
| `tpʰ > tp` | literal | — |
| `ttʰ > tt` | literal | 6 / 6 |
| `tkʰ > tk` | literal | 1 / 1 |
| `ktʰ > kt` | literal | 2 / 2 |
| `kpʰ > kp` | literal | — |
| `kkʰ > kk` | literal | 1 / 1 |

### [aspirates became voiceless spirants](https://eldamo.org/content/words/word-3262991621.html)

- порядок 01900
- общая формула `{ptk}ʰ > {ɸθx}`
- раньше, чем: spirants became stops after [r], [l]; [x] unvoiced following [j], [w]; [nm], [ŋm] became [nw], [ŋgw]; [j], [w] often reduced between vowels
- позже, чем: [n], [m] became [t], [w] after voiceless stops and aspirates; [r] became [s] after voiceless stops and aspirates; aspirates became voiceless stops after voiceless stops; nasals became voiceless stops before aspirates

| подформула | вид | примеры |
|---|---|---|
| `pʰ > ɸ` | literal | 71 / 69 |
| `tʰ > θ` | literal | 58 / 54 |
| `kʰ > x` | literal | 46 / 45 |

### [syllabic initial [s] became [is]](https://eldamo.org/content/words/word-785281061.html)

- порядок 02000
- раньше, чем: [sp], [sk] became [ps], [ks]; initial [s] plus voiceless stops became voiceless spirants

| подформула | вид | примеры |
|---|---|---|
| `ṣ- > is-` | literal | 2 / 2 |

### [initial [s] plus voiceless stops became voiceless spirants](https://eldamo.org/content/words/word-1605344503.html)

- порядок 02100
- общая формула `sp-|st-|sk- > ɸ-|θ-|x-`
- раньше, чем: [x] unvoiced following [j], [w]; unstressed medial long vowels shortened
- позже, чем: syllabic initial [s] became [is]

| подформула | вид | примеры |
|---|---|---|
| `sp- > ɸ-` | literal | 5 / 5 |
| `st- > θ-` | literal | 5 / 5 |
| `sk- > x-` | literal | 3 / 3 |

### [initial [s] unvoiced following continuant](https://eldamo.org/content/words/word-1556924193.html)

- порядок 02200
- общая формула `sm-|sn-|sr-|sl-|sj-|sw- > m̥-|n̥-|r̥-|l̥-|j̊-|w̥-`

| подформула | вид | примеры |
|---|---|---|
| `sm- > m̥-` | literal | — |
| `sn- > n̥-` | literal | 2 / 2 |
| `sr- > r̥-` | literal | 25 / 23 |
| `sl- > l̥-` | literal | 14 / 14 |
| `sj- > j̊-` | literal | 3 / 3 |
| `sw- > w̥-` | literal | 2 / 2 |

### [[x] unvoiced following [j], [w]](https://eldamo.org/content/words/word-2963647241.html)

- порядок 02300
- общая формула `xj|xw > j̊|w̥`
- раньше, чем: velars were dentalized before [j]
- позже, чем: aspirates became voiceless spirants; initial [s] plus voiceless stops became voiceless spirants

| подформула | вид | примеры |
|---|---|---|
| `xj > j̊` | literal | 4 / 4 |
| `xw > w̥` | literal | — |

### [voiced stops became nasals before nasals](https://eldamo.org/content/words/word-2830908887.html)

- порядок 02400
- общая формула `{bdg}{mnŋ} > {mnŋ}{mnŋ}`
- раньше, чем: voiced stops became spirants except after nasals; [nm], [ŋm] became [nw], [ŋgw]
- позже, чем: [n], [m] became [t], [w] after voiceless stops and aspirates

| подформула | вид | примеры |
|---|---|---|
| `bm > mm` | literal | — |
| `bn > mn` | literal | 3 / 3 |
| `bŋ > mŋ` | literal | — |
| `dm > nm` | literal | 4 / 4 |
| `dn > nn` | literal | 2 / 2 |
| `dŋ > nŋ` | literal | — |
| `gm > ŋm` | literal | 3 / 3 |
| `gn > ŋn` | literal | 1 / 1 |
| `gŋ > ŋŋ` | literal | — |

### [syllabic nasals developed a preceding vowel of similar quality](https://eldamo.org/content/words/word-4294735057.html)

- порядок 02500
- общая формула `ṃb-|ṇd-|ŋ̣g-|ŋ̣gw-|ŋ̣gj- > umb-|and-|iŋg-|uŋgw-|iŋgj-`
- раньше, чем: velars were dentalized before [j]

| подформула | вид | примеры |
|---|---|---|
| `ṃb- > umb-` | literal | 3 / 3 |
| `ṇd- > and-` | literal | 1 / 1 |
| `ŋ̣g- > iŋg-` | literal | 3 / 3 |
| `ŋ̣gw- > uŋgw-` | literal | — |
| `ŋ̣gj- > iŋgj-` | literal | 1 / 1 |

### [initial [dr-], [dl-] became [r-], [l-]](https://eldamo.org/content/words/word-3688462237.html)

- порядок 02600
- общая формула `dr-|dl- > r-|l-`
- раньше, чем: initial [d] became [l]

| подформула | вид | примеры |
|---|---|---|
| `dr- > r-` | literal | — |
| `dl- > l-` | literal | — |

### [[dj] became [lj]](https://eldamo.org/content/words/word-1574644731.html)

- порядок 02700
- раньше, чем: voiced stops became spirants except after nasals

| подформула | вид | примеры |
|---|---|---|
| `dj > lj` | literal | 1 / 1 |

### [initial [d] became [l]](https://eldamo.org/content/words/word-3325625207.html)

- порядок 02800
- раньше, чем: voiced stops became spirants except after nasals
- позже, чем: initial [d] assimilated to following nasal; initial [dr-], [dl-] became [r-], [l-]

| подформула | вид | примеры |
|---|---|---|
| `d- > l-` | literal | 20 / 20 |

### [voiced stops became spirants except after nasals](https://eldamo.org/content/words/word-1141570065.html)

- порядок 02900
- общая формула `{bdg}|{mnŋ}{bdg} > {βðɣ}|{mnŋ}{bdg}`
- раньше, чем: [z] and [ð] assimilated to following [r], [l]; spirants became stops after [r], [l]; [β], [ɣ] vocalized before voiced consonants; initial [ɣ] before [l], [r] sometimes became a vowel; velars were dentalized before [j]
- позже, чем: [dj] became [lj]; [z] plus voiced stop became unvoiced; combinations of voiced stops were unvoiced; initial [d] became [l]; initial [ɣ] became [h]; later [j], [w] became [i], [u] before consonants; second short vowel of same quality lost; voiced stops became nasals before nasals

| подформула | вид | примеры |
|---|---|---|
| `b > β` | literal | 79 / 76 |
| `mb > mb` | identity | — |
| `d > ð` | literal | 33 / 33 |
| `nd > nd` | identity | — |
| `g > ɣ` | literal | 103 / 101 |
| `ŋg > ŋg` | identity | — |

### [velars were dentalized before [j]](https://eldamo.org/content/words/word-3703720537.html)

- порядок 03000
- общая формула `{kgŋ}j|ŋkj|{rlŋ}gj > {tdn}j|ntj|{rln}dj`
- раньше, чем: initial [ŋ] vanished; initial nasals plus stops reduced to nasals; [w] became [β] initially and between vowels
- позже, чем: [x] unvoiced following [j], [w]; syllabic nasals developed a preceding vowel of similar quality; voiced stops became spirants except after nasals

| подформула | вид | примеры |
|---|---|---|
| `kj > tj` | literal | 18 / 18 |
| `gj > dj` | literal | — |
| `ŋj > nj` | literal | 1 / 1 |
| `ŋkj > ntj` | literal | — |
| `ŋgj > ndj` | literal | 3 / 3 |

### [initial [ɣ] before [l], [r] sometimes became a vowel](https://eldamo.org/content/words/word-1987898661.html)

- порядок 03100
- общая формула `ɣ{rl}V₁- > V₁{rl}V₁-`
- позже, чем: voiced stops became spirants except after nasals

| подформула | вид | примеры |
|---|---|---|
| `ɣla- > ala-` | literal | 1 / 1 |
| `ɣra- > ara-` | literal | 1 / 1 |

### [[j], [w] often became [i], [u] after consonant groups](https://eldamo.org/content/words/word-1408301067.html)

- порядок 03200
- общая формула `CC{jw}|C{td}j|C{kg}w > CC{iu}|C{td}j|C{kg}w`

| подформула | вид | примеры |
|---|---|---|
| `CCj > CCi` | contextual | — |
| `CCw > CCu` | contextual | — |

### [[ę̄], [ǭ] became [ē], [ō]](https://eldamo.org/content/words/word-1363608031.html)

- порядок 03300
- общая формула `ę̄|ǭ > ē|ō`
- раньше, чем: unstressed medial long vowels shortened

| подформула | вид | примеры |
|---|---|---|
| `ę̄ > ē` | literal | 1 / 1 |
| `ǭ > ō` | literal | 3 / 3 |

### [unstressed medial long vowels shortened](https://eldamo.org/content/words/word-1293037291.html)

- порядок 03400
- общая формула `V́CV̄ > V́CV̆`
- раньше, чем: [j], [w] often reduced between vowels
- позже, чем: [ę̄], [ǭ] became [ē], [ō]; initial [s] plus voiceless stops became voiceless spirants; second short vowel of same quality lost

| подформула | вид | примеры |
|---|---|---|
| `V́CV̄ > V́CV̆` | contextual | 10 / 8 |

### [[ɣ] became [j] between liquids and [e], [a]](https://eldamo.org/content/words/word-2619518313.html)

- порядок 03500
- общая формула `{rl}ɣ{ae} > {rl}j{ae}`
- раньше, чем: [lɣ], [rɣ] became [ll], [rr]

| подформула | вид | примеры |
|---|---|---|
| `rɣe > rje` | literal | — |
| `lɣe > lje` | literal | — |
| `rɣa > rja` | literal | — |
| `lɣa > lja` | literal | 1 / 0 |

### [[jei], [wou] became [jē], [wō]](https://eldamo.org/content/words/word-1657301905.html)

- порядок 03600
- общая формула `jei|wou > jē|wō`
- раньше, чем: [j], [w] often reduced between vowels

| подформула | вид | примеры |
|---|---|---|
| `jei > jē` | literal | 2 / 1 |
| `wou > wō` | literal | — |

### [[ɣ] became [j] between [i], [e] and a vowel](https://eldamo.org/content/words/word-1700576467.html)

- порядок 03600
- общая формула `{ie}ɣV > {ie}jV`
- раньше, чем: [j], [w] often reduced between vowels

| подформула | вид | примеры |
|---|---|---|
| `iɣV > ijV` | contextual | — |
| `eɣV > ejV` | contextual | 1 / 1 |

### [[j], [w] often reduced between vowels](https://eldamo.org/content/words/word-3978101829.html)

- порядок 03800
- общая формула `V̆{jw}V > VV`
- раньше, чем: [w] became [β] initially and between vowels; [ji], [wu] became [i], [u]; intervocalic [j] diphthongized after long vowel; [ei], [ou] generally became [ī], [ū]
- позже, чем: [ɣ] became [j] between [i], [e] and a vowel; [jei], [wou] became [jē], [wō]; aspirates became voiceless spirants; unstressed medial long vowels shortened

| подформула | вид | примеры |
|---|---|---|
| `aja > ea` | literal | 27 / 17 |
| `aje > ie` | literal | 3 / 2 |
| `ajo > eo` | literal | — |
| `eja > ia` | literal | 1 / 1 |
| `eje > ie` | literal | 3 / 1 |
| `ija > ia` | literal | — |
| `ije > ie` | literal | — |
| `oja > oia` | literal | 3 / 2 |
| `awa > oa` | literal | 26 / 15 |
| `awi > oi` | literal | 1 / 1 |
| `ewo > eo` | literal | 1 / 1 |
| `owo > uo` | literal | 1 / 0 |
| `awu > au` | literal | 1 / 1 |

### [[ln] became [ld]](https://eldamo.org/content/words/word-1011702125.html)

- порядок 03900
- позже, чем: second short vowel of same quality lost

| подформула | вид | примеры |
|---|---|---|
| `ln > ld` | literal | 11 / 11 |

### [[lɣw], [rɣw] became [lw], [rw]](https://eldamo.org/content/words/word-17019465.html)

- порядок 04000
- общая формула `{lr}ɣw > {lr}w`
- раньше, чем: [lɣ], [rɣ] became [ll], [rr]

| подформула | вид | примеры |
|---|---|---|
| `lɣw > lw` | literal | — |
| `rɣw > rw` | literal | — |

### [[mw] became [nw]](https://eldamo.org/content/words/word-3475705035.html)

- порядок 04100

| подформула | вид | примеры |
|---|---|---|
| `mw > nw` | literal | 2 / 2 |

### [initial [ŋ] vanished](https://eldamo.org/content/words/word-1073157723.html)

- порядок 04200
- общая формула `ŋV-|ŋw- > øV-|w-`
- раньше, чем: initial nasals plus stops reduced to nasals
- позже, чем: velars were dentalized before [j]

| подформула | вид | примеры |
|---|---|---|
| `ŋV- > øV-` | contextual | 2 / 2 |
| `ŋw- > w-` | literal | 1 / 1 |

### [[β], [ɣ] vocalized before voiced consonants](https://eldamo.org/content/words/word-1104502097.html)

- порядок 04300
- общая формула `VβC|VɣC|Vɣj|Vɣw > VuC|V̄øC|Vij|Vuw`
- раньше, чем: [ei], [ou] generally became [ī], [ū]; [ɣ] from [g] vanished; [ɸ], [β] became [f], [v]; initial nasals plus stops reduced to nasals
- позже, чем: voiced stops became spirants except after nasals

| подформула | вид | примеры |
|---|---|---|
| `VβC > VuC` | contextual | — |
| `aɣC > āC` | contextual | 7 / 7 |
| `eɣC > ēC` | contextual | 1 / 1 |
| `oɣC > ōC` | contextual | 1 / 1 |
| `uɣC > ūC` | contextual | 2 / 2 |
| `Vɣj > Vij` | contextual | 4 / 4 |
| `Vɣw > Vuw` | contextual | 1 / 1 |

### [initial nasals plus stops reduced to nasals](https://eldamo.org/content/words/word-2123493145.html)

- порядок 04400
- общая формула `mb-|nd-|ŋg- > m-|n-|ŋ-`
- позже, чем: [β], [ɣ] vocalized before voiced consonants; initial [ŋ] vanished; velars were dentalized before [j]

| подформула | вид | примеры |
|---|---|---|
| `mb- > m-` | literal | 27 / 27 |
| `nd- > n-` | literal | 36 / 36 |
| `ŋg- > ŋ-` | literal | 32 / 32 |
| `mp- > p-` | literal | — |
| `nt- > t-` | literal | — |
| `ŋk- > k-` | literal | — |

### [medial [s] often became [z]](https://eldamo.org/content/words/word-127393503.html)

- порядок 04500
- общая формула `Vs{Vmnrljw} > Vz{Vmnrljw}`
- раньше, чем: [z] and [ð] assimilated to following [r], [l]; short final [a], [e], [o] lost in long compounds
- позже, чем: [sr] became [ss]; second short vowel of same quality lost

| подформула | вид | примеры |
|---|---|---|
| `VsV > VzV` | contextual | 23 / 23 |
| `sm > zm` | literal | 4 / 4 |
| `sn > zn` | literal | — |
| `sr > zr` | literal | 5 / 5 |
| `sl > zl` | literal | 1 / 1 |
| `sj > zj` | literal | 9 / 9 |
| `sw > zw` | literal | 1 / 1 |

### [[z] and [ð] assimilated to following [r], [l]](https://eldamo.org/content/words/word-1472480589.html)

- порядок 04600
- общая формула `{zð}r|{zð}l > rr|ll`
- позже, чем: medial [s] often became [z]; voiced stops became spirants except after nasals

| подформула | вид | примеры |
|---|---|---|
| `ðr > rr` | literal | — |
| `ðl > ll` | literal | — |
| `zr > rr` | literal | 4 / 4 |
| `zl > ll` | literal | 1 / 1 |

### [[z] assimilated to following [m], [n]](https://eldamo.org/content/words/word-10156157.html)

- порядок 04700
- общая формула `zm|zn > mm|nn`
- раньше, чем: [z] became [r]

| подформула | вид | примеры |
|---|---|---|
| `zm > mm` | literal | 1 / 1 |
| `zn > nn` | literal | — |

## Q. Quenya (поздняя концепция)

### [[nm], [ŋm] became [nw], [ŋgw]](https://eldamo.org/content/words/word-1197128543.html)

- порядок 00100
- общая формула `nm|ŋm > nw|ŋgw`
- раньше, чем: [x] became [h] except before [t]
- позже, чем: aspirates became voiceless spirants; voiced stops became nasals before nasals

| подформула | вид | примеры |
|---|---|---|
| `nm > mm` | literal | — |
| `nm > nw` | literal | 11 / 11 |
| `ŋm > ŋgw` | literal | 3 / 3 |

### [[ŋ] vanished between [i], [u] and [n] with compensatory lengthening](https://eldamo.org/content/words/word-2035963219.html)

- порядок 00200
- общая формула `{iu}ŋn > V̄øn`
- раньше, чем: [ŋ] assimilated to following [n] after [e], [a], [o]

| подформула | вид | примеры |
|---|---|---|
| `iŋn > īn` | literal | 1 / 1 |
| `uŋn > ūn` | literal | — |
| `iŋm > īm` | literal | — |
| `eŋm > ēm` | literal | 2 / 2 |
| `aŋm > ām` | literal | — |
| `oŋm > ōm` | literal | — |
| `uŋm > ūm` | literal | — |

### [medial [ŋ] after a [n], [ŋ], [l], [r] became [g]](https://eldamo.org/content/words/word-447633467.html)

- порядок 00300

| подформула | вид | примеры |
|---|---|---|
| `-{nŋlr}ŋ- > -{nŋlr}g-` | contextual | 1 / 1 |

### [[ei], [ou] generally became [ī], [ū]](https://eldamo.org/content/words/word-2315722009.html)

- порядок 00400
- общая формула `ei|ou > ī|ū`
- позже, чем: [j], [w] often reduced between vowels; [β], [ɣ] vocalized before voiced consonants

| подформула | вид | примеры |
|---|---|---|
| `ei > ī` | literal | 7 / 7 |
| `ou > ū` | literal | 2 / 2 |

### [[ji], [wu] became [i], [u]](https://eldamo.org/content/words/word-1167483479.html)

- порядок 00500
- общая формула `ji|wu > i|u`
- позже, чем: [j], [w] often reduced between vowels

| подформула | вид | примеры |
|---|---|---|
| `ji > i` | literal | 1 / 1 |
| `wu > u` | literal | 1 / 1 |

### [intervocalic [j] diphthongized after long vowel](https://eldamo.org/content/words/word-3458631869.html)

- порядок 00600
- общая формула `V̄jV > VijV`
- позже, чем: [j], [w] often reduced between vowels

| подформула | вид | примеры |
|---|---|---|
| `āja > aija` | literal | 8 / 6 |
| `ōja > oija` | literal | 1 / 1 |

### [spirants became stops after [r], [l]](https://eldamo.org/content/words/word-3516399115.html)

- порядок 00700
- общая формула `{rl}{ɸθxð} > {rl}{ptkd}`
- раньше, чем: [β], [ɣ] after [r], [l] usually became stops; [d] vanished between [n], [r], [l] and [j]; [ɣ] from [g] vanished
- позже, чем: aspirates became voiceless spirants; voiced stops became spirants except after nasals

| подформула | вид | примеры |
|---|---|---|
| `lɸ > lp` | literal | — |
| `rɸ > rp` | literal | 1 / 1 |
| `lθ > lt` | literal | — |
| `rθ > rt` | literal | 1 / 1 |
| `lx > lk` | literal | 1 / 1 |
| `rx > rk` | literal | 1 / 1 |
| `lð > ld` | literal | 2 / 2 |
| `rð > rd` | literal | — |
| `lβ > lb` | literal | 1 / 1 |

### [spirants became stops after nasals](https://eldamo.org/content/words/word-545708645.html)

- порядок 00800
- общая формула `mɸ|nθ|ŋx|nð > mp|nt|ŋk|nd`
- позже, чем: nasals became voiceless stops before aspirates

| подформула | вид | примеры |
|---|---|---|
| `mɸ > mp` | literal | — |
| `nθ > nt` | literal | — |
| `ŋx > ŋk` | literal | — |
| `nð > nd` | literal | 1 / 1 |

### [[wo] became [o]](https://eldamo.org/content/words/word-1082322649.html)

- порядок 00900
- раньше, чем: [w] became [β] initially and between vowels

| подформула | вид | примеры |
|---|---|---|
| `wo- > o-` | literal | 6 / 4 |

### [[w] became [β] initially and between vowels](https://eldamo.org/content/words/word-3625908403.html)

- порядок 01000
- общая формула `w-|VwV|aiw > β-|VβV|aiw`
- позже, чем: [j], [w] often reduced between vowels; [wo] became [o]; velars were dentalized before [j]

| подформула | вид | примеры |
|---|---|---|
| `w- > β-` | literal | 37 / 35 |
| `VwV > VβV` | contextual | 14 / 12 |
| `aiw > aiw` | identity | — |

### [[ɣ] from [g] vanished](https://eldamo.org/content/words/word-1833409085.html)

- порядок 01100
- раньше, чем: [ae], [ao] generally became [ē], [ō]
- позже, чем: medial [ŋ] usually became [ɣ]; [β], [ɣ] vocalized before voiced consonants; spirants became stops after [r], [l]

| подформула | вид | примеры |
|---|---|---|
| `ɣ > ø` | loss | 82 / 76 |

### [[ae], [ao] generally became [ē], [ō]](https://eldamo.org/content/words/word-1132141441.html)

- порядок 01200
- общая формула `ae|ao|ā{ĕŏ} > ē|ō|ā`
- раньше, чем: long final vowels were shortened
- позже, чем: [ɣ] from [g] vanished

| подформула | вид | примеры |
|---|---|---|
| `ae > ē` | literal | — |
| `ao > ō` | literal | — |
| `āĕ > ā` | literal | — |
| `āŏ > ā` | literal | — |

### [[ɸu] became [hu]](https://eldamo.org/content/words/word-1102872571.html)

- порядок 01300
- раньше, чем: [ɸ], [β] became [f], [v]

| подформула | вид | примеры |
|---|---|---|
| `ɸu > hu` | literal | 2 / 2 |

### [[β] vanished before [u] after vowels](https://eldamo.org/content/words/word-1771463731.html)

- порядок 01400

| подформула | вид | примеры |
|---|---|---|
| `Vβu > Vu` | contextual | 1 / 1 |

### [[pt], [kt] became [ɸt], [xt]](https://eldamo.org/content/words/word-2265073101.html)

- порядок 01500
- общая формула `{pk}t > {ɸx}t`
- раньше, чем: initial voiceless nasals and liquids were voiced; [ɸt] became [ut]

| подформула | вид | примеры |
|---|---|---|
| `pt > ɸt` | literal | 7 / 4 |
| `kt > xt` | literal | 34 / 33 |
| `tk > θk` | literal | 2 / 2 |

### [[pw] became [pp]](https://eldamo.org/content/words/word-182545135.html)

- порядок 01600
- позже, чем: [n], [m] became [t], [w] after voiceless stops and aspirates

| подформула | вид | примеры |
|---|---|---|
| `pw > pp` | literal | 1 / 1 |

### [initial voiceless nasals and liquids were voiced](https://eldamo.org/content/words/word-3012528347.html)

- порядок 01700
- общая формула `{m̥n̥l̥r̥}- > {mnlr}-`
- позже, чем: [pt], [kt] became [ɸt], [xt]

| подформула | вид | примеры |
|---|---|---|
| `m̥- > m-` | literal | — |
| `n̥- > n-` | literal | 2 / 2 |
| `l̥- > l-` | literal | 1 / 1 |
| `r̥- > r-` | literal | — |

### [[x] became [h] except before [t]](https://eldamo.org/content/words/word-2071843593.html)

- порядок 01800
- общая формула `x|xt|lx|rx > h|xt|l̥l̥|r̥r̥`
- раньше, чем: [z] became [r]
- позже, чем: [nm], [ŋm] became [nw], [ŋgw]

| подформула | вид | примеры |
|---|---|---|
| `x > h` | literal | 46 / 46 |
| `xt > xt` | identity | — |
| `lx > l̥l̥` | literal | — |
| `rx > r̥r̥` | literal | — |

### [medial [ð], [z] dissimilated to [l], [s] after [r]](https://eldamo.org/content/words/word-455699965.html)

- порядок 01900
- общая формула `rVð|rVz|zVr > rVl|rVs|sVr`
- раньше, чем: intervocalic [ð] became [r]; [z] became [r]

| подформула | вид | примеры |
|---|---|---|
| `rVð > rVl` | contextual | 1 / 0 |
| `lVð > lVl` | contextual | 1 / 1 |
| `rVz > rVs` | contextual | — |
| `zVr > sVr` | contextual | 3 / 0 |

### [long vowels shortened before consonant clusters](https://eldamo.org/content/words/word-4125237087.html)

- порядок 02000
- общая формула `V̄CC|V̄tj|V̄kw > V̆CC|V̄tj|V̄kw`

| подформула | вид | примеры |
|---|---|---|
| `āCC > ăCC` | contextual | 2 / 2 |

### [long final vowels were shortened](https://eldamo.org/content/words/word-2821506177.html)

- порядок 02100
- общая формула `-SV̄ > -SV̆`
- раньше, чем: [θ] became [s]; [sp], [sk] became [ps], [ks]; short final [a], [e], [o] lost in long compounds
- позже, чем: [ae], [ao] generally became [ē], [ō]

| подформула | вид | примеры |
|---|---|---|
| `-Sī > -Sĭ` | contextual | 9 / 8 |
| `-Sē > -Sĕ` | contextual | 99 / 98 |
| `-Sā > -Să` | contextual | 192 / 182 |
| `-Sō > -Sŏ` | contextual | 44 / 42 |
| `-Sū > -Sŭ` | contextual | 12 / 11 |
| `-SāC > -SăC` | contextual | 12 / 12 |
| `-SēC > -SĕC` | contextual | — |
| `-SōC > -SŏC` | contextual | 2 / 2 |
| `-SūC > -SŭC` | contextual | 1 / 1 |

### [[ij], [uw] became [i], [u]](https://eldamo.org/content/words/word-1619715205.html)

- порядок 02200
- общая формула `ijV|uwV > iV|uV`

| подформула | вид | примеры |
|---|---|---|
| `ij > i` | literal | 10 / 9 |
| `uw > u` | literal | 1 / 0 |

### [short final [a], [e], [o] lost in long compounds](https://eldamo.org/content/words/word-3904029624.html)

- порядок 02300
- общая формула `-SSS{ăĕŏ} > -SSSø`
- раньше, чем: final consonant clusters reduced
- позже, чем: long final vowels were shortened; medial [s] often became [z]

| подформула | вид | примеры |
|---|---|---|
| `-SSSă > -SSSø` | contextual | 2 / 0 |
| `-SSSĕ > -SSSø` | contextual | — |
| `-SSSŏ > -SSSø` | contextual | 1 / 0 |

### [nasals and liquids often became syllabic after a consonant](https://eldamo.org/content/words/word-613618983.html)

- порядок 02400
- общая формула `ClV₁|ml|Cr|{ptk}{nm} > CV₁lV₁|mul|Car|{ptk}{an|um}`

| подформула | вид | примеры |
|---|---|---|
| `ClV₁ > CV₁lV₁` | contextual | — |
| `ml > mul` | literal | — |
| `Cr > Car` | contextual | — |

### [final consonant clusters reduced](https://eldamo.org/content/words/word-731874859.html)

- порядок 02500
- общая формула `-CC|-{ptk}s|-{xp}t > -C|-s|-t`
- раньше, чем: [z] became [r]
- позже, чем: short final [a], [e], [o] lost in long compounds

| подформула | вид | примеры |
|---|---|---|
| `-CC > -C` | contextual | 18 / 18 |
| `-xt > -t` | literal | — |
| `-pt > -t` | literal | — |
| `-ps > -s` | literal | — |
| `-ts > -s` | literal | — |
| `-ks > -s` | literal | 1 / 1 |

### [final spirants were altered](https://eldamo.org/content/words/word-3424103699.html)

- порядок 02600
- общая формула `-{θð} > -{tr}`
- раньше, чем: [θ] became [s]

| подформула | вид | примеры |
|---|---|---|
| `-θ > -t` | literal | 1 / 1 |
| `-ð > -r` | literal | 14 / 14 |

### [final consonants became dentals](https://eldamo.org/content/words/word-3283441787.html)

- порядок 02700
- общая формула `-{pk}|-{mŋ} > -t|-n`

| подформула | вид | примеры |
|---|---|---|
| `-k > -t` | literal | — |
| `-m > -n` | literal | 4 / 4 |

### [[ŋ] assimilated to following [n] after [e], [a], [o]](https://eldamo.org/content/words/word-368875839.html)

- порядок 02800
- общая формула `{eao}ŋn > {eao}nn`
- позже, чем: [ŋ] vanished between [i], [u] and [n] with compensatory lengthening

| подформула | вид | примеры |
|---|---|---|
| `eŋn > enn` | literal | 2 / 2 |
| `aŋn > ann` | literal | 2 / 2 |
| `oŋn > onn` | literal | — |

### [[ɸ], [β] became [f], [v]](https://eldamo.org/content/words/word-14484545.html)

- порядок 02900
- общая формула `ɸ|β > f|v`
- позже, чем: [ɸu] became [hu]; [β], [ɣ] vocalized before voiced consonants

| подформула | вид | примеры |
|---|---|---|
| `ɸ > f` | literal | 73 / 73 |
| `β > v` | literal | 129 / 128 |

### [[-ai] became [-e]](https://eldamo.org/content/words/word-2761837707.html)

- порядок 03000

| подформула | вид | примеры |
|---|---|---|
| `-ai > -e` | literal | 5 / 5 |

### [[sf] became [f]](https://eldamo.org/content/words/word-946722487.html)

- порядок 03100

| подформула | вид | примеры |
|---|---|---|
| `sf > f` | literal | — |

### [[w] from [gw] became [v] initially and between vowels](https://eldamo.org/content/words/word-385572165.html)

- порядок 03200
- общая формула `w-|VwV > v-|VvV`

| подформула | вид | примеры |
|---|---|---|
| `w- > v-` | literal | 3 / 3 |
| `VwV > VvV` | contextual | 1 / 1 |

### [[lɣ], [rɣ] became [ll], [rr]](https://eldamo.org/content/words/word-2837004771.html)

- порядок 03300
- общая формула `lɣ|rɣ > ll|rr`
- позже, чем: [ɣ] became [j] between liquids and [e], [a]; [lɣw], [rɣw] became [lw], [rw]

| подформула | вид | примеры |
|---|---|---|
| `lɣ > ll` | literal | 1 / 1 |
| `rɣ > rr` | literal | — |

### [[θ] became [s]](https://eldamo.org/content/words/word-3491983963.html)

- порядок 03400
- позже, чем: final spirants were altered; long final vowels were shortened

| подформула | вид | примеры |
|---|---|---|
| `θ > s` | literal | 65 / 64 |

### [[sp], [sk] became [ps], [ks]](https://eldamo.org/content/words/word-2094898289.html)

- порядок 03500
- общая формула `sp|sk|skw > ps|ks|skw`
- раньше, чем: initial [ps], [ks] became [ups], [iks]
- позже, чем: [z] plus voiced stop became unvoiced; long final vowels were shortened; syllabic initial [s] became [is]

| подформула | вид | примеры |
|---|---|---|
| `sp > ps` | literal | 2 / 2 |
| `sk > ks` | literal | 5 / 5 |
| `ts > st` | literal | 1 / 1 |

### [[d] vanished between [n], [r], [l] and [j]](https://eldamo.org/content/words/word-297797679.html)

- порядок 03600
- общая формула `{nrl}dj > {nrl}øj`
- позже, чем: spirants became stops after [r], [l]

| подформула | вид | примеры |
|---|---|---|
| `ldj > lj` | literal | — |
| `ndj > nj` | literal | 3 / 3 |
| `rdj > rj` | literal | — |

### [intervocalic [ð] became [r]](https://eldamo.org/content/words/word-2793529037.html)

- порядок 03700
- общая формула `Vð{Vw} > Vr{Vw}`
- раньше, чем: [z] became [r]
- позже, чем: medial [ð], [z] dissimilated to [l], [s] after [r]

| подформула | вид | примеры |
|---|---|---|
| `VðV > VrV` | contextual | 16 / 14 |
| `Vðw > Vrw` | contextual | — |
| `Vðj > Vrj` | contextual | — |

### [[z] became [r]](https://eldamo.org/content/words/word-3534004155.html)

- порядок 03800
- раньше, чем: unstressed [ir], [ur] sometimes became [er], [or]
- позже, чем: [x] became [h] except before [t]; [z] assimilated to following [m], [n]; final consonant clusters reduced; intervocalic [ð] became [r]; medial [ð], [z] dissimilated to [l], [s] after [r]

| подформула | вид | примеры |
|---|---|---|
| `z > r` | literal | 36 / 33 |

### [[rs] became [ss]](https://eldamo.org/content/words/word-1326730955.html)

- порядок 03900

| подформула | вид | примеры |
|---|---|---|
| `rs > ss` | literal | 1 / 1 |

### [initial [ŋ] became [n]](https://eldamo.org/content/words/word-1073266651.html)

- порядок 04000

| подформула | вид | примеры |
|---|---|---|
| `ŋ- > n-` | literal | 34 / 34 |

### [initial [ps], [ks] became [ups], [iks]](https://eldamo.org/content/words/word-2166344385.html)

- порядок 04100
- общая формула `ps-|ks- > ups-|iks-`
- позже, чем: [sp], [sk] became [ps], [ks]

| подформула | вид | примеры |
|---|---|---|
| `ps- > ups-` | literal | — |
| `ks- > iks-` | literal | — |

### [[ɸt] became [ut]](https://eldamo.org/content/words/word-2497198855.html)

- порядок 04200
- позже, чем: [pt], [kt] became [ɸt], [xt]

| подформула | вид | примеры |
|---|---|---|
| `ɸt > ut` | literal | 1 / 1 |

### [exilic [ts] became [ss]](https://eldamo.org/content/words/word-173969535.html)

- порядок 04300

| подформула | вид | примеры |
|---|---|---|
| `ts > ss` | literal | — |

### [final [t] became [s]](https://eldamo.org/content/words/word-2842904179.html)

- порядок 04400

| подформула | вид | примеры |
|---|---|---|
| `-t > -s` | literal | 1 / 1 |

### [[w] became [v] after [l], [r]](https://eldamo.org/content/words/word-2276015165.html)

- порядок 04500
- общая формула `{lr}w > {lr}v`

| подформула | вид | примеры |
|---|---|---|
| `lw > lv` | literal | 4 / 4 |
| `rw > rv` | literal | — |

### [unstressed [ir], [ur] sometimes became [er], [or]](https://eldamo.org/content/words/word-642778275.html)

- порядок 04600
- общая формула `Ś{ĭŭ}r > Ś{eo}r`
- позже, чем: [z] became [r]

| подформула | вид | примеры |
|---|---|---|
| `Śĭr > Śer` | contextual | 1 / 1 |
| `Śŭr > Śor` | contextual | — |

## ᴹ✶ Middle Primitive Elvish (средняя концепция)

### [[lr] became [ll]](https://eldamo.org/content/words/word-1228325011.html)

- порядок 00100
- вариант правила [[lr] became [ll]](https://eldamo.org/content/words/word-4183190863.html)

| подформула | вид | примеры |
|---|---|---|
| `lr > ll` | literal | 6 / 6 |

### [[ae], [ao] became [ā]](https://eldamo.org/content/words/word-2229536775.html)

- порядок 00200
- общая формула `a{eo} > ā`
- вариант правила [[ae], [ao] became [ā]](https://eldamo.org/content/words/word-1056240093.html)

| подформула | вид | примеры |
|---|---|---|
| `ae > ā` | literal | — |
| `ao > ā` | literal | — |

### [[j], [w] became [i], [u] before consonants](https://eldamo.org/content/words/word-716490961.html)

- порядок 00300
- общая формула `V{jw}C > V{iu}C`
- вариант правила [[j], [w] became [i], [u] before consonants](https://eldamo.org/content/words/word-113345945.html)

| подформула | вид | примеры |
|---|---|---|
| `ajC > aiC` | contextual | 19 / 19 |
| `ejC > eiC` | contextual | — |
| `ojC > oiC` | contextual | 5 / 5 |
| `ujC > uiC` | contextual | 8 / 8 |
| `awC > auC` | contextual | 9 / 9 |
| `ewC > euC` | contextual | 1 / 1 |
| `iwC > iuC` | contextual | 6 / 6 |
| `owC > ouC` | contextual | 2 / 2 |

### [[s] became [z] before voiced stops](https://eldamo.org/content/words/word-2884507077.html)

- порядок 00400
- общая формула `s{bdg} > z{bdg}`
- вариант правила [[s] became [z] before voiced stops](https://eldamo.org/content/words/word-882174441.html)

| подформула | вид | примеры |
|---|---|---|
| `sb > zb` | literal | — |
| `sd > zd` | literal | — |
| `sg > zg` | literal | 4 / 4 |

### [long vowels shortened before consonant clusters](https://eldamo.org/content/words/word-2818407091.html)

- порядок 00500
- вариант правила [long vowels shortened before consonant clusters](https://eldamo.org/content/words/word-542079381.html)

| подформула | вид | примеры |
|---|---|---|
| `V̄CC > V̆CC` | contextual | 1 / 1 |

### [voiced stops unvoiced before voiceless consonants](https://eldamo.org/content/words/word-2905876955.html)

- порядок 00600
- общая формула `{bdg}{ptkpʰtʰkʰs} > {ptk}{ptkpʰtʰkʰs}`
- вариант правила [voiced stops unvoiced before voiceless consonants](https://eldamo.org/content/words/word-1944249607.html)

| подформула | вид | примеры |
|---|---|---|
| `bt > pt` | literal | 2 / 2 |
| `bs > ps` | literal | — |
| `dt > tt` | literal | — |
| `ds > ts` | literal | 2 / 2 |
| `gt > kt` | literal | 2 / 2 |
| `gs > ks` | literal | — |

### [aspirate became voiceless stop before [s]](https://eldamo.org/content/words/word-2678342679.html)

- порядок 00700
- общая формула `{ptk}ʰs > {ptk}s`
- вариант правила [aspirate became voiceless stop before [s]](https://eldamo.org/content/words/word-2225058767.html)

| подформула | вид | примеры |
|---|---|---|
| `pʰs > ps` | literal | — |
| `tʰs > ts` | literal | 1 / 1 |
| `kʰs > ks` | literal | 2 / 2 |

### [aspiration moved to end of group of stops](https://eldamo.org/content/words/word-798737509.html)

- порядок 00800
- общая формула `{ptk}ʰ{ptk|pʰtʰkʰ} > {ptk}{ptk}ʰ`
- позже, чем: voiced stops unvoiced after voiceless stops and aspirates
- вариант правила [aspiration moved to end of group of stops](https://eldamo.org/content/words/word-3183451073.html)

| подформула | вид | примеры |
|---|---|---|
| `pʰt > ptʰ` | literal | — |
| `pʰtʰ > ptʰ` | literal | — |
| `tʰt > ttʰ` | literal | 2 / 2 |
| `tʰtʰ > ttʰ` | literal | — |
| `kʰt > ktʰ` | literal | — |
| `kʰk > kkʰ` | literal | — |

### [[t+t], [d+d] from suffixion became [st], [zd]](https://eldamo.org/content/words/word-2630259491.html)

- порядок 00900
- общая формула `{ttʰd}+t|d+d > st|zd`
- вариант правила [[t+t], [d+d] from suffixion became [st], [zd]](https://eldamo.org/content/words/word-2479050823.html)

| подформула | вид | примеры |
|---|---|---|
| `t+t > st` | contextual | 2 / 0 |
| `tʰ+t > st` | contextual | 3 / 0 |
| `d+t > st` | contextual | 4 / 0 |
| `d+d > zd` | contextual | 2 / 0 |

### [[tk] became [kk] or [kt]](https://eldamo.org/content/words/word-2412660893.html)

- порядок 01000
- общая формула `tk > kk`
- вариант правила [[tk] became [kk] or [kt] or [sk]](https://eldamo.org/content/words/word-700934409.html)

| подформула | вид | примеры |
|---|---|---|
| `tk > kk` | literal | 2 / 2 |
| `tk > kt` | literal | 2 / 2 |
| `tp > pp` | literal | 1 / 1 |

### [nasals assimilated to following stops and aspirates](https://eldamo.org/content/words/word-2390772785.html)

- порядок 01100
- общая формула `{nŋ}{ppʰb}|ŋ{ttʰd}|n{kkʰg} > m{ppʰb}|n{ttʰd}|ŋ{kkʰg}`
- раньше, чем: medial [ŋ] usually became [ɣ]
- вариант правила [nasals assimilated to following stops and aspirates](https://eldamo.org/content/words/word-2143444883.html)

| подформула | вид | примеры |
|---|---|---|
| `np > mp` | literal | 1 / 1 |
| `nb > mb` | literal | 1 / 1 |
| `ŋp > mp` | literal | — |
| `mt > nt` | literal | 1 / 1 |
| `md > nd` | literal | 1 / 1 |
| `ŋt > nt` | literal | — |
| `mk > ŋk` | literal | — |
| `nk > ŋk` | literal | 2 / 2 |

### [medial [ŋj], [ŋw] became [ŋgj], [ŋgw]](https://eldamo.org/content/words/word-1270135967.html)

- порядок 01200
- общая формула `-ŋ{wj}- > -ŋg{wj}-`
- раньше, чем: medial [ŋ] usually became [ɣ]
- вариант правила [medial [ŋj], [ŋw] became [ŋgj], [ŋgw]](https://eldamo.org/content/words/word-2233951333.html)

| подформула | вид | примеры |
|---|---|---|
| `-ŋj- > -ŋgj-` | literal | 2 / 2 |
| `-ŋw- > -ŋgw-` | literal | 11 / 11 |

### [[ŋŋ], [ŋɣ] became [ŋg]](https://eldamo.org/content/words/word-2849203249.html)

- порядок 01300
- общая формула `ŋ{ŋɣ} > ŋg`
- вариант правила [[ŋŋ], [ŋɣ] became [ŋg]](https://eldamo.org/content/words/word-3404492995.html)

| подформула | вид | примеры |
|---|---|---|
| `ŋɣ > ŋg` | literal | 2 / 2 |
| `ŋŋ > ŋg` | literal | 5 / 5 |

### [medial [ŋ] usually became [ɣ]](https://eldamo.org/content/words/word-3915121695.html)

- порядок 01400
- общая формула `VŋV|ŋ{rls} > VɣV|ɣ{rls}`
- раньше, чем: [ɣ] became [h] before voiceless consonants
- позже, чем: medial [ŋj], [ŋw] became [ŋgj], [ŋgw]; nasals assimilated to following stops and aspirates
- вариант правила [medial [ŋ] usually became [ɣ]](https://eldamo.org/content/words/word-768986721.html)

| подформула | вид | примеры |
|---|---|---|
| `VŋV > VɣV` | contextual | 2 / 1 |
| `-Vŋ > -Vɣ` | contextual | — |
| `ŋr > ɣr` | literal | 1 / 1 |
| `ŋl > ɣl` | literal | — |
| `ŋs > ɣs` | literal | — |
| `ŋ- > ɣ-` | literal | 2 / 2 |

### [[ɣ] became [h] before voiceless consonants](https://eldamo.org/content/words/word-2810726977.html)

- порядок 01500
- общая формула `ɣ{ptkpʰtʰkʰs} > h{ptkpʰtʰkʰs}`
- позже, чем: medial [ŋ] usually became [ɣ]
- вариант правила [794129503](https://eldamo.org/content/words/word-794129503.html)

| подформула | вид | примеры |
|---|---|---|
| `ɣs > hs` | literal | 1 / 1 |
| `ɣt > xt` | literal | 3 / 2 |
| `xtʰ > xtʰ` | identity | — |

### [[hs] became [ss]](https://eldamo.org/content/words/word-178282823.html)

- порядок 01600
- раньше, чем: medial [ɣ] vanished except before [t]
- вариант правила [[hs] became [ss]](https://eldamo.org/content/words/word-2177009433.html)

| подформула | вид | примеры |
|---|---|---|
| `hs > ss` | literal | 2 / 1 |

### [unstressed long vowels shortened in medial syllables](https://eldamo.org/content/words/word-3404671151.html)

- порядок 01700
- вариант правила [unstressed long vowels shortened in medial syllables](https://eldamo.org/content/words/word-951924569.html)

| подформула | вид | примеры |
|---|---|---|
| `ˌV̄S > V̆S` | contextual | 4 / 4 |

### [short final [e], [a], [o] vanished](https://eldamo.org/content/words/word-3998109579.html)

- порядок 01800
- общая формула `-S{ĕăŏǝ} > -Sø`
- вариант правила [short final [e], [a], [o] vanished](https://eldamo.org/content/words/word-2794740763.html)

| подформула | вид | примеры |
|---|---|---|
| `-Sǝ > -Sø` | contextual | 10 / 10 |
| `-Sĕ > -Sø` | contextual | 29 / 25 |
| `-Să > -Sø` | contextual | 17 / 17 |
| `-Sŏ > -Sø` | contextual | 16 / 15 |

### [short final [i], [u] became [e], [o]](https://eldamo.org/content/words/word-2698078435.html)

- порядок 01900
- общая формула `-S{ĭŭ} > -S{eo}`
- вариант правила [short final [i], [u] became [e], [o]](https://eldamo.org/content/words/word-3064357955.html)

| подформула | вид | примеры |
|---|---|---|
| `-Sĭ > -Se` | contextual | 70 / 66 |
| `-Sŭ > -So` | contextual | 34 / 34 |

### [final [j], [w] vanished after long vowels in monosyllables](https://eldamo.org/content/words/word-2139290845.html)

- порядок 02000
- общая формула `CV̄{jw} > CV̄`
- вариант правила [final [j], [w] vanished after long vowels in monosyllables](https://eldamo.org/content/words/word-1539930001.html)

| подформула | вид | примеры |
|---|---|---|
| `Cāj > Cā` | contextual | — |
| `Cāw > Cā` | contextual | 2 / 2 |

### [final [j], [w] became [i], [u]](https://eldamo.org/content/words/word-2867358397.html)

- порядок 02100
- общая формула `-{yw} > -{iu}`
- вариант правила [final [j], [w] became [i], [u]](https://eldamo.org/content/words/word-2641132585.html)

| подформула | вид | примеры |
|---|---|---|
| `-j > -i` | literal | 1 / 1 |
| `-w > -u` | literal | — |

### [final [ā] became [ē] after [tw], [tm]](https://eldamo.org/content/words/word-3337453437.html)

- порядок 02200
- общая формула `-t{mw}ā > -t{mw}ē`

| подформула | вид | примеры |
|---|---|---|
| `-tmā > -tmē` | literal | 3 / 3 |
| `-twā > -twē` | literal | 1 / 1 |

### [stressed [wŏ] became [wa]](https://eldamo.org/content/words/word-1415948757.html)

- порядок 02300
- позже, чем: [wou] became [wō]
- вариант правила [stressed [wŏ] became [wa]](https://eldamo.org/content/words/word-1475928117.html)

| подформула | вид | примеры |
|---|---|---|
| `wŏ́ > wa` | literal | 8 / 4 |

### [[bm], [dn] became [mb], [nd]](https://eldamo.org/content/words/word-1390975943.html)

- общая формула `bm|dn > mb|nd`
- вариант правила [[bm], [dn] became [mb], [nd]](https://eldamo.org/content/words/word-3882201769.html)

| подформула | вид | примеры |
|---|---|---|
| `bm > mb` | literal | 1 / 0 |
| `dn > nd` | literal | 2 / 2 |

### [[lɣ] became [lg]](https://eldamo.org/content/words/word-739645275.html)

- вариант правила [[lɣ] became [lg]](https://eldamo.org/content/words/word-2151845509.html)

| подформула | вид | примеры |
|---|---|---|
| `lɣ > lg` | literal | — |

### [[pw], [pʰw] became [pp], [pʰp]](https://eldamo.org/content/words/word-2680378713.html)

- общая формула `pw|pʰw > pp|pʰpʰ`
- вариант правила [[pw], [pʰw] became [pp], [pʰp]](https://eldamo.org/content/words/word-2859678213.html)

| подформула | вид | примеры |
|---|---|---|
| `pw > pp` | literal | — |
| `pʰw > ppʰ` | literal | — |

### [[wau] became [wā]](https://eldamo.org/content/words/word-243516177.html)

- общая формула `wau > wā`
- вариант правила [[wau] became [au] or [wā]](https://eldamo.org/content/words/word-242344611.html)

| подформула | вид | примеры |
|---|---|---|
| `wau > wā` | literal | — |

### [[wou] became [wō]](https://eldamo.org/content/words/word-944679535.html)

- раньше, чем: stressed [wŏ] became [wa]
- вариант правила [[wou] became [wō]](https://eldamo.org/content/words/word-3116232193.html)

### [aspirates became voiceless stops after [s], [h]](https://eldamo.org/content/words/word-2699949575.html)

- общая формула `s{ptk}ʰ|htʰ > s{ptk}|ht`
- вариант правила [aspirates became voiceless stops after [s], [h]](https://eldamo.org/content/words/word-3915424757.html)

| подформула | вид | примеры |
|---|---|---|
| `spʰ > sp` | literal | — |
| `stʰ > st` | literal | — |
| `skʰ > sk` | literal | — |
| `htʰ > ht` | literal | — |

### [medial [ɣ] vanished except before [t]](https://eldamo.org/content/words/word-2639734255.html)

- общая формула `-ɣ-|VɣC|ɣt > -ø-|V̄øC|xt`
- позже, чем: [hs] became [ss]
- вариант правила [medial [ɣ]/[h] vanished except before [t]](https://eldamo.org/content/words/word-2690267141.html)

| подформула | вид | примеры |
|---|---|---|
| `-ɣ- > -ø-` | loss | 6 / 5 |
| `eɣC > ēC` | contextual | 2 / 2 |
| `aɣC > āC` | contextual | 3 / 3 |
| `oɣC > ōC` | contextual | 3 / 2 |
| `uɣC > ūC` | contextual | 1 / 0 |

### [metathesis](https://eldamo.org/content/words/word-1396728225.html)

- вариант правила [metathesis](https://eldamo.org/content/words/word-3160359587.html)

| подформула | вид | примеры |
|---|---|---|
| `pʰm > mpʰ` | literal | — |

### [voiced stops unvoiced after voiceless stops and aspirates](https://eldamo.org/content/words/word-3661438765.html)

- общая формула `{pʰtʰkʰptk}{bdg}|{bdg}{pʰtʰkʰptk} > {pʰtʰkʰptk}{ptk}|{ptk}{pʰtʰkʰptk}`
- раньше, чем: aspiration moved to end of group of stops
- вариант правила [voiced stops unvoiced after voiceless stops and aspirates](https://eldamo.org/content/words/word-2620200719.html)

| подформула | вид | примеры |
|---|---|---|
| `kd > kt` | literal | — |

## ᴹAQ. Middle Ancient Quenya (средняя концепция)

### [[ms] became [ns]](https://eldamo.org/content/words/word-2983162711.html)

- порядок 00100
- раньше, чем: [ns] became [ss] or [nz]
- вариант правила [[ms] became [ns]](https://eldamo.org/content/words/word-1399041717.html)

| подформула | вид | примеры |
|---|---|---|
| `ms > ns` | literal | — |

### [[ns] became [ss] or [nz]](https://eldamo.org/content/words/word-1082153437.html)

- порядок 00200
- позже, чем: [ms] became [ns]
- вариант правила [[ns] became [ss]](https://eldamo.org/content/words/word-2591378297.html)

| подформула | вид | примеры |
|---|---|---|
| `ns > ss` | literal | — |

### [second short vowel of same quality lost](https://eldamo.org/content/words/word-511172017.html)

- порядок 00300
- общая формула `V₁CV̆₁CV > V₁CCV`
- раньше, чем: stops frequently underwent metathesis with nasals and liquids; voiced stops became spirants except after nasals and liquids; medial [s] often became [z]; unstressed medial long vowels shortened
- вариант правила [second short vowel of same quality lost](https://eldamo.org/content/words/word-3116715705.html)

| подформула | вид | примеры |
|---|---|---|
| `aCaCV > aCCV` | contextual | 16 / 14 |
| `eCeCV > eCCV` | contextual | 20 / 17 |
| `iCiCV > iCCV` | contextual | 4 / 4 |
| `oCoCV > oCCV` | contextual | 10 / 10 |
| `uCuCV > uCCV` | contextual | 2 / 2 |

### [later [j], [w] became [i], [u] before consonants](https://eldamo.org/content/words/word-1025863587.html)

- порядок 00400
- общая формула `VjC|VwC > ViC|VuC`
- раньше, чем: voiced stops became spirants except after nasals and liquids
- вариант правила [later [j], [w] became [i], [u] before consonants](https://eldamo.org/content/words/word-2232975397.html)

| подформула | вид | примеры |
|---|---|---|
| `VjC > ViC` | contextual | — |
| `VwC > VuC` | contextual | — |

### [[ls] became [ll] or [ld]](https://eldamo.org/content/words/word-3452831179.html)

- порядок 00500
- общая формула `ls > ll`
- вариант правила [[ls] became [ll] or [ld]](https://eldamo.org/content/words/word-367860887.html)

| подформула | вид | примеры |
|---|---|---|
| `ls > ll` | literal | 2 / 2 |
| `ls > ld` | literal | 1 / 1 |

### [stops frequently underwent metathesis with nasals and liquids](https://eldamo.org/content/words/word-716992289.html)

- порядок 00600
- общая формула `{ptkpʰtʰkʰbdg}{lrmnŋ} > {lrmnŋ}{ptkpʰtʰkʰbdg}`
- раньше, чем: [nl], [nr] became [ll], [rr]
- позже, чем: second short vowel of same quality lost
- вариант правила [stops frequently underwent metathesis with nasals and liquids](https://eldamo.org/content/words/word-3192302915.html)

| подформула | вид | примеры |
|---|---|---|
| `pl > lp` | literal | — |
| `tl > lt` | literal | — |
| `kl > lk` | literal | — |
| `pʰl > lpʰ` | literal | — |
| `tʰl > ltʰ` | literal | — |
| `kʰl > lkʰ` | literal | — |
| `bl > lb` | literal | — |
| `dl > ld` | literal | — |
| `gl > lg` | literal | — |
| `pr > rp` | literal | — |
| `tr > rt` | literal | 1 / 1 |
| `kr > rk` | literal | 3 / 3 |
| `pʰr > rpʰ` | literal | — |
| `tʰr > rtʰ` | literal | — |
| `kʰr > rkʰ` | literal | — |
| `br > rb` | literal | — |
| `dr > rd` | literal | — |
| `gr > rg` | literal | — |
| `ml > lm` | literal | — |
| `mr > rm` | literal | — |
| `nr > rn` | literal | — |
| `pn > np` | literal | 1 / 1 |
| `dl > ld` | literal | — |

### [[nl], [nr] became [ll], [rr]](https://eldamo.org/content/words/word-3167171353.html)

- порядок 00700
- общая формула `nl|nr > ll|rr`
- раньше, чем: [r], [l] often became syllabic in clusters
- позже, чем: stops frequently underwent metathesis with nasals and liquids
- вариант правила [[nl], [nr] became [ll], [rr]](https://eldamo.org/content/words/word-1625553255.html)

| подформула | вид | примеры |
|---|---|---|
| `nl > ll` | literal | 4 / 4 |
| `nr > rr` | literal | — |

### [[sr] became [ss]](https://eldamo.org/content/words/word-3069824903.html)

- порядок 00800
- раньше, чем: medial [s] often became [z]
- вариант правила [[sr] became [ss]](https://eldamo.org/content/words/word-1606156545.html)

| подформула | вид | примеры |
|---|---|---|
| `sr > ss` | literal | — |

### [[rl] and [lr] became [ll]](https://eldamo.org/content/words/word-3234141583.html)

- порядок 00900
- общая формула `rl|lr > ll|ll`
- раньше, чем: [r], [l] often became syllabic in clusters
- вариант правила [[rl] and [lr] became [ll]](https://eldamo.org/content/words/word-1550655669.html)

| подформула | вид | примеры |
|---|---|---|
| `rl > ll` | literal | — |
| `lr > ll` | literal | — |

### [[r], [l] often became syllabic in clusters](https://eldamo.org/content/words/word-720793221.html)

- порядок 01000
- общая формула `V₁Cḷ|CCr > V₁CV₁l|CCar`
- раньше, чем: [r] became [s] after voiceless stops and aspirates
- позже, чем: [nl], [nr] became [ll], [rr]; [rl] and [lr] became [ll]
- вариант правила [[r], [l] often became syllabic in clusters](https://eldamo.org/content/words/word-825670671.html)

| подформула | вид | примеры |
|---|---|---|
| `aCCl > aCCal` | contextual | 4 / 1 |
| `CCl > CCil` | contextual | 2 / 2 |
| `ḷ > il` | literal | 3 / 1 |
| `CCør > CCar` | contextual | 3 / 3 |

### [[r] became [s] after voiceless stops and aspirates](https://eldamo.org/content/words/word-1238072385.html)

- порядок 01100
- общая формула `{ptkpʰtʰkʰ}r > {ptkpʰtʰkʰ}s`
- раньше, чем: aspirates became voiceless spirants
- позже, чем: [r], [l] often became syllabic in clusters
- вариант правила [[r] became [s] after voiceless stops and aspirates](https://eldamo.org/content/words/word-1071202939.html)

| подформула | вид | примеры |
|---|---|---|
| `pr > ps` | literal | — |
| `tr > ts` | literal | 1 / 1 |
| `kr > ks` | literal | — |
| `pʰr > ps` | literal | — |
| `tʰr > ts` | literal | 1 / 1 |
| `kʰr > ks` | literal | — |
| `ntr > ns` | literal | — |

### [initial [d] assimilated to following nasal](https://eldamo.org/content/words/word-4113635787.html)

- порядок 01200
- раньше, чем: initial [d] became [l]
- вариант правила [initial [d] assimilated to following nasal](https://eldamo.org/content/words/word-2885687903.html)

| подформула | вид | примеры |
|---|---|---|
| `dVXn- > nVXn-` | contextual | 2 / 2 |

### [initial [ɣ] became [h]](https://eldamo.org/content/words/word-1968067631.html)

- порядок 01300
- раньше, чем: voiced stops became spirants except after nasals and liquids
- вариант правила [initial [ɣ] became [h]](https://eldamo.org/content/words/word-3316553555.html)

| подформула | вид | примеры |
|---|---|---|
| `ɣ- > h-` | literal | 18 / 18 |

### [combinations of voiced stops were unvoiced](https://eldamo.org/content/words/word-654861237.html)

- порядок 01400
- общая формула `{bdg}{bdg} > {ptk}{ptk}`
- раньше, чем: voiced stops became spirants except after nasals and liquids
- вариант правила [combinations of voiced stops were unvoiced](https://eldamo.org/content/words/word-1625077395.html)

| подформула | вид | примеры |
|---|---|---|
| `bb > pp` | literal | 1 / 1 |
| `bd > pt` | literal | 2 / 2 |
| `bg > pk` | literal | — |
| `db > tp` | literal | — |
| `dd > tt` | literal | — |
| `dg > tk` | literal | — |
| `gb > kp` | literal | — |
| `gd > kt` | literal | 2 / 2 |
| `gg > kk` | literal | — |

### [[z] plus voiced stop became unvoiced](https://eldamo.org/content/words/word-4145487633.html)

- порядок 01500
- общая формула `z{bdg} > s{ptk}`
- раньше, чем: voiced stops became spirants except after nasals and liquids; [sp], [sk] became [ps], [ks]
- вариант правила [[z] plus voiced stop became unvoiced](https://eldamo.org/content/words/word-3279729471.html)

| подформула | вид | примеры |
|---|---|---|
| `zb > sp` | literal | 1 / 1 |
| `zd > st` | literal | 5 / 5 |
| `zg > sk` | literal | 5 / 5 |

### [voiceless stops were voiced before nasals](https://eldamo.org/content/words/word-1324444289.html)

- порядок 01600
- общая формула `{ptk}{nm} > {bdg}{nm}`
- вариант правила [[n], [m] became [t], [w] after voiceless stops and aspirates](https://eldamo.org/content/words/word-3418086257.html)

| подформула | вид | примеры |
|---|---|---|
| `pm > bm` | literal | 1 / 1 |
| `tm > dm` | literal | 3 / 3 |
| `km > gm` | literal | 12 / 12 |
| `pn > bn` | literal | 4 / 4 |
| `tn > dn` | literal | 3 / 3 |
| `kn > gn` | literal | 5 / 5 |

### [[n], [m] became [t], [w] after aspirates](https://eldamo.org/content/words/word-372953021.html)

- порядок 01700
- общая формула `{ptk}ʰ{nm} > {ptk}ʰ{tw}`
- раньше, чем: aspirates became voiceless spirants; voiced stops became nasals before nasals
- вариант правила [[n], [m] became [t], [w] after voiceless stops and aspirates](https://eldamo.org/content/words/word-3418086257.html)

| подформула | вид | примеры |
|---|---|---|
| `pʰn > pt` | literal | — |
| `tʰn > tt` | literal | 1 / 1 |
| `kʰn > kt` | literal | 1 / 1 |
| `pʰm > pʰw` | literal | — |
| `tʰm > tʰw` | literal | 1 / 1 |
| `kʰm > kʰw` | literal | — |

### [nasals became voiceless stops before aspirates](https://eldamo.org/content/words/word-2847294287.html)

- порядок 01800
- общая формула `mpʰ|ntʰ|ŋkʰ > ppʰ|ttʰ|kkʰ`
- раньше, чем: aspirates became voiceless spirants; spirants became stops after nasals
- вариант правила [nasals became voiceless stops before aspirates](https://eldamo.org/content/words/word-3474357431.html)

| подформула | вид | примеры |
|---|---|---|
| `mpʰ > ppʰ` | literal | 1 / 1 |
| `ntʰ > ttʰ` | literal | 1 / 1 |
| `ŋkʰ > kkʰ` | literal | 1 / 1 |

### [aspirates became voiceless stops after voiceless stops](https://eldamo.org/content/words/word-2769500867.html)

- порядок 01900
- общая формула `{ptk}{ptk}ʰ > {ptk}{ptk}`
- раньше, чем: aspirates became voiceless spirants
- вариант правила [aspirates became voiceless stops after voiceless stops](https://eldamo.org/content/words/word-2190887743.html)

| подформула | вид | примеры |
|---|---|---|
| `ppʰ > pp` | literal | 1 / 1 |
| `ptʰ > pt` | literal | — |
| `pkʰ > pk` | literal | — |
| `tpʰ > tp` | literal | — |
| `ttʰ > tt` | literal | 4 / 3 |
| `ktʰ > kt` | literal | — |
| `kpʰ > kp` | literal | — |
| `ktʰ > kt` | literal | — |
| `kkʰ > kk` | literal | 1 / 1 |

### [aspirates became voiceless spirants](https://eldamo.org/content/words/word-3537093625.html)

- порядок 02000
- общая формула `{ptk}ʰ > {ɸθx}`
- раньше, чем: spirants became stops after [r], [l]; [nm], [ŋm] became [nw], [ŋgw]; [j], [w] often reduced between vowels
- позже, чем: [n], [m] became [t], [w] after aspirates; [r] became [s] after voiceless stops and aspirates; aspirates became voiceless stops after voiceless stops; nasals became voiceless stops before aspirates
- вариант правила [aspirates became voiceless spirants](https://eldamo.org/content/words/word-3262991621.html)

| подформула | вид | примеры |
|---|---|---|
| `pʰ > ɸ` | literal | 42 / 42 |
| `tʰ > θ` | literal | 28 / 26 |
| `kʰ > x` | literal | 57 / 56 |

### [syllabic initial [s] became [is]](https://eldamo.org/content/words/word-2033267709.html)

- порядок 02100
- раньше, чем: [sp], [sk] became [ps], [ks]; initial [s] plus voiceless stops became voiceless spirants
- вариант правила [syllabic initial [s] became [is]](https://eldamo.org/content/words/word-785281061.html)

| подформула | вид | примеры |
|---|---|---|
| `ṣ- > is-` | literal | — |

### [initial [s] plus voiceless stops became voiceless spirants](https://eldamo.org/content/words/word-3333849997.html)

- порядок 02200
- общая формула `sp-|st-|sk- > ɸ-|θ-|x-`
- раньше, чем: [x], [s] unvoiced following [j], [w]; unstressed medial long vowels shortened
- позже, чем: syllabic initial [s] became [is]
- вариант правила [initial [s] plus voiceless stops became voiceless spirants](https://eldamo.org/content/words/word-1605344503.html)

| подформула | вид | примеры |
|---|---|---|
| `sp- > ɸ-` | literal | 11 / 11 |
| `st- > θ-` | literal | 16 / 8 |
| `sk- > x-` | literal | 13 / 13 |

### [initial [s] unvoiced following continuant](https://eldamo.org/content/words/word-476591497.html)

- порядок 02300
- общая формула `sm-|sn-|sr-|sl-|sj-|sw- > m̥-|n̥-|r̥-|l̥-|j̊-|w̥-`
- вариант правила [initial [s] unvoiced following continuant](https://eldamo.org/content/words/word-1556924193.html)

| подформула | вид | примеры |
|---|---|---|
| `sm- > m̥-` | literal | 4 / 3 |
| `sn- > n̥-` | literal | 3 / 3 |
| `sr- > r̥-` | literal | — |
| `sl- > l̥-` | literal | 11 / 11 |
| `sj- > j̊-` | literal | 8 / 8 |
| `sw- > w̥-` | literal | 5 / 5 |

### [[x], [s] unvoiced following [j], [w]](https://eldamo.org/content/words/word-3260572145.html)

- порядок 02400
- общая формула `{xs}j|{xs}w > j̊|w̥`
- раньше, чем: velars were dentalized before [j]
- позже, чем: initial [s] plus voiceless stops became voiceless spirants
- вариант правила [[x] unvoiced following [j], [w]](https://eldamo.org/content/words/word-2963647241.html)

| подформула | вид | примеры |
|---|---|---|
| `xj > j̊` | literal | 5 / 5 |
| `sj > j̊` | literal | — |
| `xw > w̥` | literal | 2 / 2 |
| `sw > w̥` | literal | — |

### [voiced stops became nasals before nasals](https://eldamo.org/content/words/word-1312520143.html)

- порядок 02500
- общая формула `{bdg}{mnŋ} > {mnŋ}{mnŋ}`
- раньше, чем: voiced stops became spirants except after nasals and liquids; [nm], [ŋm] became [nw], [ŋgw]
- позже, чем: [n], [m] became [t], [w] after aspirates
- вариант правила [voiced stops became nasals before nasals](https://eldamo.org/content/words/word-2830908887.html)

| подформула | вид | примеры |
|---|---|---|
| `bm > mm` | literal | 1 / 1 |
| `bn > mn` | literal | 12 / 12 |
| `bŋ > mŋ` | literal | — |
| `dm > nm` | literal | 3 / 3 |
| `dn > nn` | literal | 5 / 5 |
| `dŋ > nŋ` | literal | — |
| `gm > ŋm` | literal | 13 / 13 |
| `gn > ŋn` | literal | 9 / 8 |
| `gŋ > ŋŋ` | literal | — |

### [syllabic nasals developed a preceding vowel of similar quality](https://eldamo.org/content/words/word-1953085243.html)

- порядок 02600
- общая формула `ṃb-|ṇd-|ŋ̣g-|ŋ̣gw-|ŋ̣gj- > umb-|and-|iŋg-|uŋgw-|iŋgj-`
- раньше, чем: velars were dentalized before [j]
- вариант правила [syllabic nasals developed a preceding vowel of similar quality](https://eldamo.org/content/words/word-4294735057.html)

| подформула | вид | примеры |
|---|---|---|
| `ṃb- > umb-` | literal | 3 / 3 |
| `ṇd- > and-` | literal | 3 / 3 |
| `ŋ̣g- > iŋg-` | literal | 6 / 6 |
| `ŋ̣gw- > uŋgw-` | literal | 1 / 1 |
| `ŋ̣kw- > uŋkw-` | literal | 4 / 4 |
| `ŋ̣gj- > iŋgj-` | literal | — |

### [initial [dr-], [dl-] became [r-], [l-]](https://eldamo.org/content/words/word-1126123145.html)

- порядок 02700
- общая формула `dr-|dl- > r-|l-`
- раньше, чем: initial [d] became [l]
- вариант правила [initial [dr-], [dl-] became [r-], [l-]](https://eldamo.org/content/words/word-3688462237.html)

| подформула | вид | примеры |
|---|---|---|
| `dr- > r-` | literal | 1 / 1 |
| `dl- > l-` | literal | — |

### [initial [dj] became [j]](https://eldamo.org/content/words/word-4022071203.html)

- порядок 02800
- общая формула `dj- > j-`
- раньше, чем: voiced stops became spirants except after nasals and liquids
- вариант правила [[dj] became [lj]](https://eldamo.org/content/words/word-1574644731.html)

| подформула | вид | примеры |
|---|---|---|
| `dj- > j-` | literal | 3 / 3 |

### [initial [d] became [l]](https://eldamo.org/content/words/word-31048751.html)

- порядок 02900
- раньше, чем: voiced stops became spirants except after nasals and liquids
- позже, чем: initial [d] assimilated to following nasal; initial [dr-], [dl-] became [r-], [l-]
- вариант правила [initial [d] became [l]](https://eldamo.org/content/words/word-3325625207.html)

| подформула | вид | примеры |
|---|---|---|
| `d- > l-` | literal | 25 / 25 |

### [voiced stops became spirants except after nasals and liquids](https://eldamo.org/content/words/word-2772726195.html)

- порядок 03000
- общая формула `{bdg}|{mnŋ}{bdg} > {βðɣ}|{mnŋ}{bdg}`
- раньше, чем: [z] and [ð] assimilated to following [r], [l]; spirants became stops after [r], [l]; [β], [ɣ] vocalized before voiced consonants; initial [ɣ] before [l], [r] sometimes became a vowel; velars were dentalized before [j]
- позже, чем: initial [dj] became [j]; [z] plus voiced stop became unvoiced; combinations of voiced stops were unvoiced; initial [d] became [l]; initial [ɣ] became [h]; later [j], [w] became [i], [u] before consonants; second short vowel of same quality lost; voiced stops became nasals before nasals
- вариант правила [voiced stops became spirants except after nasals](https://eldamo.org/content/words/word-1141570065.html)

| подформула | вид | примеры |
|---|---|---|
| `b > β` | literal | 61 / 55 |
| `mb > mb` | identity | — |
| `d > ð` | literal | 19 / 17 |
| `nd > nd` | identity | — |
| `g > ɣ` | literal | 79 / 79 |
| `ŋg > ŋg` | identity | — |

### [velars were dentalized before [j]](https://eldamo.org/content/words/word-3291729015.html)

- порядок 03100
- общая формула `{kgŋ}j|ŋkj|{rlŋ}gj > {tdn}j|ntj|{rln}dj`
- раньше, чем: initial [ŋ] vanished; initial nasals plus stops reduced to nasals
- позже, чем: [x], [s] unvoiced following [j], [w]; syllabic nasals developed a preceding vowel of similar quality; voiced stops became spirants except after nasals and liquids
- вариант правила [velars were dentalized before [j]](https://eldamo.org/content/words/word-3703720537.html)

| подформула | вид | примеры |
|---|---|---|
| `kj > tj` | literal | 14 / 14 |
| `kʰj > tʰj` | literal | — |
| `gj > dj` | literal | — |
| `ŋj > nj` | literal | — |
| `ŋkj > ntj` | literal | 2 / 2 |
| `ŋgj > ndj` | literal | 2 / 2 |

### [initial [ɣ] before [l], [r] sometimes became a vowel](https://eldamo.org/content/words/word-2093360413.html)

- порядок 03200
- общая формула `ɣ{rl}V₁- > V₁{rl}V₁-`
- позже, чем: voiced stops became spirants except after nasals and liquids
- вариант правила [initial [ɣ] before [l], [r] sometimes became a vowel](https://eldamo.org/content/words/word-1987898661.html)

| подформула | вид | примеры |
|---|---|---|
| `ɣla- > ala-` | literal | — |
| `ɣli- > ili-` | literal | — |

### [[j], [w] often became [i], [u] after consonant groups](https://eldamo.org/content/words/word-1328395873.html)

- порядок 03300
- общая формула `CC{jw}|C{td}j|C{kg}w > CC{iu}|C{td}j|C{kg}w`
- вариант правила [[j], [w] often became [i], [u] after consonant groups](https://eldamo.org/content/words/word-1408301067.html)

| подформула | вид | примеры |
|---|---|---|
| `CCj > CCi` | contextual | 1 / 0 |
| `CCw > CCu` | contextual | 1 / 1 |

### [[ǣ], [ǭ] became [ē], [ō]](https://eldamo.org/content/words/word-2724920753.html)

- порядок 03400
- общая формула `ǣ|ǭ > ē|ō`
- раньше, чем: unstressed medial long vowels shortened
- вариант правила [[ę̄], [ǭ] became [ē], [ō]](https://eldamo.org/content/words/word-1363608031.html)

| подформула | вид | примеры |
|---|---|---|
| `ǣ > ē` | literal | 3 / 3 |
| `ǭ > ō` | literal | 5 / 5 |

### [unstressed medial long vowels shortened](https://eldamo.org/content/words/word-3034061375.html)

- порядок 03500
- общая формула `V́CV̄ > V́CV̆`
- раньше, чем: [j], [w] often reduced between vowels
- позже, чем: [ǣ], [ǭ] became [ē], [ō]; initial [s] plus voiceless stops became voiceless spirants; second short vowel of same quality lost
- вариант правила [unstressed medial long vowels shortened](https://eldamo.org/content/words/word-1293037291.html)

| подформула | вид | примеры |
|---|---|---|
| `V́CV̄ > V́CV̆` | contextual | 21 / 15 |

### [[ɣ] became [j] between liquids and [e], [a]](https://eldamo.org/content/words/word-2224634237.html)

- порядок 03600
- общая формула `{rl}ɣ{ae} > {rl}j{ae}`
- раньше, чем: [lɣ], [rɣ] became [ll], [rr]
- вариант правила [[ɣ] became [j] between liquids and [e], [a]](https://eldamo.org/content/words/word-2619518313.html)

| подформула | вид | примеры |
|---|---|---|
| `rɣe > rje` | literal | — |
| `lɣe > lje` | literal | — |
| `rɣa > rja` | literal | 1 / 0 |
| `lɣa > lja` | literal | 1 / 0 |

### [[jei], [wou] became [jē], [wō]](https://eldamo.org/content/words/word-3981277517.html)

- порядок 03700
- общая формула `jei|wou > jē|wō`
- раньше, чем: [j], [w] often reduced between vowels
- вариант правила [[jei], [wou] became [jē], [wō]](https://eldamo.org/content/words/word-1657301905.html)

| подформула | вид | примеры |
|---|---|---|
| `jei > jē` | literal | — |
| `wou > wō` | literal | — |

### [[ɣ] between a vowel and [e] and became [j]](https://eldamo.org/content/words/word-2632900125.html)

- порядок 03700
- общая формула `Vɣe > Vje`
- раньше, чем: [j], [w] often reduced between vowels
- вариант правила [[ɣ] became [j] between [i], [e] and a vowel](https://eldamo.org/content/words/word-1700576467.html)

| подформула | вид | примеры |
|---|---|---|
| `Vɣe > Vje` | contextual | 2 / 0 |
| `Vɣo > Vwo` | contextual | 1 / 0 |

### [[j], [w] often reduced between vowels](https://eldamo.org/content/words/word-1324632797.html)

- порядок 03900
- общая формула `V̆{jw}V > VV`
- раньше, чем: [w] became [v] initially and between vowels; [ji], [wu] became [i], [u]; intervocalic [j] diphthongized after long vowel; [ei], [ou] generally became [ī], [ū]
- позже, чем: [ɣ] between a vowel and [e] and became [j]; [jei], [wou] became [jē], [wō]; aspirates became voiceless spirants; unstressed medial long vowels shortened
- вариант правила [[j], [w] often reduced between vowels](https://eldamo.org/content/words/word-3978101829.html)

| подформула | вид | примеры |
|---|---|---|
| `aja > ea` | literal | 5 / 3 |
| `aje > ie` | literal | — |
| `ajo > eo` | literal | 1 / 0 |
| `eja > ia` | literal | — |
| `eje > ie` | literal | 3 / 1 |
| `ije > ie` | literal | 2 / 2 |
| `eja > ea` | literal | 1 / 1 |
| `awa > oa` | literal | — |
| `owa > oa` | literal | 1 / 1 |
| `owo > uo` | literal | 1 / 1 |
| `oja > oia` | literal | 2 / 2 |
| `uwa > ua` | literal | 1 / 0 |
| `uja > uia` | literal | 1 / 1 |

### [[ln] became [ld]](https://eldamo.org/content/words/word-1937075927.html)

- порядок 04000
- общая формула `ln > ld`
- вариант правила [[ln] became [ld]](https://eldamo.org/content/words/word-1011702125.html)

| подформула | вид | примеры |
|---|---|---|
| `ln > ld` | literal | 5 / 4 |
| `ln > ll` | literal | — |

### [[lɣw], [rɣw] became [lw], [rw]](https://eldamo.org/content/words/word-3909823069.html)

- порядок 04100
- общая формула `{lr}ɣw > {lr}w`
- раньше, чем: [lɣ], [rɣ] became [ll], [rr]
- вариант правила [[lɣw], [rɣw] became [lw], [rw]](https://eldamo.org/content/words/word-17019465.html)

| подформула | вид | примеры |
|---|---|---|
| `lɣw > lw` | literal | 1 / 0 |
| `rɣw > rw` | literal | — |

### [[mw] became [mm]](https://eldamo.org/content/words/word-1010737209.html)

- порядок 04200
- вариант правила [[mw] became [nw]](https://eldamo.org/content/words/word-3475705035.html)

| подформула | вид | примеры |
|---|---|---|
| `mw > mm` | literal | 1 / 1 |

### [initial [ŋ] vanished](https://eldamo.org/content/words/word-923465271.html)

- порядок 04300
- общая формула `ŋV-|ŋw- > øV-|w-`
- раньше, чем: initial nasals plus stops reduced to nasals
- позже, чем: velars were dentalized before [j]
- вариант правила [initial [ŋ] vanished](https://eldamo.org/content/words/word-1073157723.html)

| подформула | вид | примеры |
|---|---|---|
| `ŋV- > øV-` | contextual | 1 / 0 |
| `ŋw- > w-` | literal | — |

### [[β], [ɣ] vocalized before voiced consonants](https://eldamo.org/content/words/word-641476107.html)

- порядок 04400
- общая формула `VβC|VɣC|Vɣj|Vɣw > VuC|V̄øC|Vij|Vuw`
- раньше, чем: [ɣ] from [g] vanished; [ɸ], [β] became [f], [v]
- позже, чем: voiced stops became spirants except after nasals and liquids
- вариант правила [[β], [ɣ] vocalized before voiced consonants](https://eldamo.org/content/words/word-1104502097.html)

| подформула | вид | примеры |
|---|---|---|
| `VβC > VuC` | contextual | — |
| `aɣC > āC` | contextual | 4 / 4 |
| `eɣC > ēC` | contextual | 1 / 1 |
| `iɣC > īC` | contextual | — |
| `oɣC > ōC` | contextual | 1 / 1 |
| `uɣC > ūC` | contextual | 1 / 1 |
| `Vɣj > Vij` | contextual | 1 / 1 |
| `Vɣw > Vuw` | contextual | 1 / 1 |

### [initial nasals plus stops reduced to nasals](https://eldamo.org/content/words/word-2830500177.html)

- порядок 04500
- общая формула `mb-|nd-|ŋg- > m-|n-|ŋ-`
- позже, чем: initial [ŋ] vanished; velars were dentalized before [j]
- вариант правила [initial nasals plus stops reduced to nasals](https://eldamo.org/content/words/word-2123493145.html)

| подформула | вид | примеры |
|---|---|---|
| `mb- > m-` | literal | 26 / 25 |
| `nd- > n-` | literal | 33 / 30 |
| `ŋg- > ŋ-` | literal | 20 / 20 |
| `mp- > p-` | literal | — |
| `nt- > t-` | literal | — |
| `ŋk- > k-` | literal | — |

### [medial [s] often became [z]](https://eldamo.org/content/words/word-2951986869.html)

- порядок 04600
- общая формула `Vs{Vmnrljw} > Vz{Vmnrljw}`
- раньше, чем: [z] and [ð] assimilated to following [r], [l]
- позже, чем: [sr] became [ss]; second short vowel of same quality lost
- вариант правила [medial [s] often became [z]](https://eldamo.org/content/words/word-127393503.html)

| подформула | вид | примеры |
|---|---|---|
| `VsV > VzV` | contextual | 9 / 8 |
| `sm > zm` | literal | — |
| `sn > zn` | literal | 4 / 4 |
| `sr > zr` | literal | 2 / 2 |
| `sl > zl` | literal | 1 / 1 |
| `sj > zj` | literal | 2 / 1 |
| `sw > zw` | literal | — |

### [[z] and [ð] assimilated to following [r], [l]](https://eldamo.org/content/words/word-98897835.html)

- порядок 04700
- общая формула `{zð}r|{zð}l > rr|ll`
- позже, чем: medial [s] often became [z]; voiced stops became spirants except after nasals and liquids
- вариант правила [[z] and [ð] assimilated to following [r], [l]](https://eldamo.org/content/words/word-1472480589.html)

| подформула | вид | примеры |
|---|---|---|
| `ðr > rr` | literal | 1 / 1 |
| `ðl > ll` | literal | — |
| `zr > rr` | literal | 2 / 2 |
| `zl > ll` | literal | 2 / 2 |

### [[z] assimilated to following [m], [n]](https://eldamo.org/content/words/word-927570507.html)

- порядок 04800
- общая формула `zm|zn > mm|nn`
- раньше, чем: [z] became [r]
- вариант правила [[z] assimilated to following [m], [n]](https://eldamo.org/content/words/word-10156157.html)

| подформула | вид | примеры |
|---|---|---|
| `zm > mm` | literal | — |
| `zn > nn` | literal | 1 / 1 |

## ᴹQ. Middle Quenya (средняя концепция)

### [[nm], [ŋm] became [nw], [ŋgw]](https://eldamo.org/content/words/word-2886094609.html)

- порядок 00100
- общая формула `nm|ŋm > nw|ŋgw`
- раньше, чем: [x] became [h] except before [t]
- позже, чем: aspirates became voiceless spirants; voiced stops became nasals before nasals
- вариант правила [[nm], [ŋm] became [nw], [ŋgw]](https://eldamo.org/content/words/word-1197128543.html)

| подформула | вид | примеры |
|---|---|---|
| `nm > nw` | literal | 5 / 5 |
| `ŋm > ŋgw` | literal | 15 / 13 |

### [[ŋ] vanished between [i], [u] and [n] with compensatory lengthening](https://eldamo.org/content/words/word-423068915.html)

- порядок 00200
- общая формула `{iu}ŋn > V̄øn`
- вариант правила [[ŋ] vanished between [i], [u] and [n] with compensatory lengthening](https://eldamo.org/content/words/word-2035963219.html)

| подформула | вид | примеры |
|---|---|---|
| `iŋn > īn` | literal | 4 / 2 |
| `uŋn > ūn` | literal | 3 / 3 |

### [medial [ŋ] after a [n], [ŋ], [l], [r] became [g]](https://eldamo.org/content/words/word-3554566251.html)

- порядок 00300
- вариант правила [medial [ŋ] after a [n], [ŋ], [l], [r] became [g]](https://eldamo.org/content/words/word-447633467.html)

| подформула | вид | примеры |
|---|---|---|
| `-{nŋlr}ŋ- > -{nŋlr}g-` | contextual | — |

### [[ei], [ou] generally became [ī], [ū]](https://eldamo.org/content/words/word-1123007057.html)

- порядок 00400
- общая формула `ei|ou > ī|ū`
- позже, чем: [j], [w] often reduced between vowels
- вариант правила [[ei], [ou] generally became [ī], [ū]](https://eldamo.org/content/words/word-2315722009.html)

| подформула | вид | примеры |
|---|---|---|
| `ei > ī` | literal | 2 / 2 |
| `ou > ū` | literal | — |
| `éi > ai` | literal | 1 / 1 |
| `éi > ē` | literal | 1 / 1 |
| `óu > au` | literal | 1 / 1 |
| `óu > ō` | literal | 1 / 1 |

### [[ji], [wu] became [i], [u]](https://eldamo.org/content/words/word-4237906131.html)

- порядок 00500
- общая формула `ji|wu > i|u`
- позже, чем: [j], [w] often reduced between vowels
- вариант правила [[ji], [wu] became [i], [u]](https://eldamo.org/content/words/word-1167483479.html)

| подформула | вид | примеры |
|---|---|---|
| `ji > i` | literal | — |
| `wu > u` | literal | — |

### [intervocalic [j] diphthongized after long vowel](https://eldamo.org/content/words/word-3477758271.html)

- порядок 00600
- общая формула `V̄jV > VijV`
- позже, чем: [j], [w] often reduced between vowels
- вариант правила [intervocalic [j] diphthongized after long vowel](https://eldamo.org/content/words/word-3458631869.html)

| подформула | вид | примеры |
|---|---|---|
| `āja > aija` | literal | 4 / 2 |

### [spirants became stops after [r], [l]](https://eldamo.org/content/words/word-556722173.html)

- порядок 00700
- общая формула `{rl}{ðβ} > {rl}{dw}`
- раньше, чем: [d] vanished between [n], [r], [l] and [j]; [ɣ] from [g] vanished
- позже, чем: aspirates became voiceless spirants; voiced stops became spirants except after nasals and liquids
- вариант правила [spirants became stops after [r], [l]](https://eldamo.org/content/words/word-3516399115.html)

| подформула | вид | примеры |
|---|---|---|
| `lð > ld` | literal | — |
| `rð > rd` | literal | — |
| `lβ > lw` | literal | 1 / 1 |

### [spirants became stops after nasals](https://eldamo.org/content/words/word-699730083.html)

- порядок 00800
- общая формула `mɸ|nθ|ŋx|nð > mp|nt|ŋk|nd`
- позже, чем: nasals became voiceless stops before aspirates
- вариант правила [spirants became stops after nasals](https://eldamo.org/content/words/word-545708645.html)

| подформула | вид | примеры |
|---|---|---|
| `mɸ > mp` | literal | — |
| `nθ > nt` | literal | — |
| `ŋx > ŋk` | literal | 1 / 1 |

### [[wo] became [o]](https://eldamo.org/content/words/word-2218848947.html)

- порядок 00900
- раньше, чем: [w] became [v] initially and between vowels
- позже, чем: [ɣ] otherwise vanished
- вариант правила [[wo] became [o]](https://eldamo.org/content/words/word-1082322649.html)

| подформула | вид | примеры |
|---|---|---|
| `wo- > o-` | literal | 4 / 3 |

### [[ɣ] from [g] vanished](https://eldamo.org/content/words/word-3266317297.html)

- порядок 01000
- раньше, чем: [ae], [ao] generally became [ē], [ō]
- позже, чем: [β], [ɣ] vocalized before voiced consonants; spirants became stops after [r], [l]
- вариант правила [[ɣ] from [g] vanished](https://eldamo.org/content/words/word-1833409085.html)

| подформула | вид | примеры |
|---|---|---|
| `ɣ > ø` | loss | 67 / 65 |

### [[ae], [ao] generally became [ē], [ō]](https://eldamo.org/content/words/word-205917541.html)

- порядок 01100
- общая формула `ae|ao|ā{ĕŏ} > ē|ō|ā`
- раньше, чем: long final vowels were shortened
- позже, чем: [ɣ] from [g] vanished
- вариант правила [[ae], [ao] generally became [ē], [ō]](https://eldamo.org/content/words/word-1132141441.html)

| подформула | вид | примеры |
|---|---|---|
| `ae > ē` | literal | — |
| `ao > ō` | literal | — |
| `āĕ > ā` | literal | — |
| `āŏ > ā` | literal | — |

### [[β] vanished before [u] after vowels](https://eldamo.org/content/words/word-2666116821.html)

- порядок 01200
- вариант правила [[β] vanished before [u] after vowels](https://eldamo.org/content/words/word-1771463731.html)

| подформула | вид | примеры |
|---|---|---|
| `Vβu > Vu` | contextual | 1 / 1 |

### [[pt], [kt] became [ps], [xt]](https://eldamo.org/content/words/word-2701010297.html)

- порядок 01300
- общая формула `pt|kt > ps|xt`
- раньше, чем: initial voiceless nasals and liquids were voiced
- вариант правила [[pt], [kt] became [ɸt], [xt]](https://eldamo.org/content/words/word-2265073101.html)

| подформула | вид | примеры |
|---|---|---|
| `pt > ps` | literal | 8 / 8 |
| `kt > xt` | literal | 26 / 26 |
| `pt > xt` | literal | 1 / 1 |

### [[pw] became [pp]](https://eldamo.org/content/words/word-1491842395.html)

- порядок 01400
- вариант правила [[pw] became [pp]](https://eldamo.org/content/words/word-182545135.html)

| подформула | вид | примеры |
|---|---|---|
| `pw > pp` | literal | — |

### [initial voiceless nasals and liquids were voiced](https://eldamo.org/content/words/word-213078681.html)

- порядок 01500
- общая формула `{m̥n̥l̥r̥}- > {mnlr}-`
- позже, чем: [pt], [kt] became [ps], [xt]
- вариант правила [initial voiceless nasals and liquids were voiced](https://eldamo.org/content/words/word-3012528347.html)

| подформула | вид | примеры |
|---|---|---|
| `m̥- > m-` | literal | 4 / 4 |
| `n̥- > n-` | literal | 3 / 3 |
| `l̥- > l-` | literal | 10 / 10 |
| `r̥- > r-` | literal | — |

### [[x] became [h] except before [t]](https://eldamo.org/content/words/word-2800366809.html)

- порядок 01600
- общая формула `x|xt|lx|rx > h|xt|l̥l̥|r̥r̥`
- раньше, чем: [z] became [r]
- позже, чем: [nm], [ŋm] became [nw], [ŋgw]
- вариант правила [[x] became [h] except before [t]](https://eldamo.org/content/words/word-2071843593.html)

| подформула | вид | примеры |
|---|---|---|
| `x > h` | literal | 61 / 59 |
| `xt > xt` | identity | — |
| `lx > l̥l̥` | literal | — |
| `rx > r̥r̥` | literal | — |

### [medial [ð] dissimilated to [l] after [r]](https://eldamo.org/content/words/word-687907123.html)

- порядок 01700
- общая формула `rVð > rVl`
- раньше, чем: intervocalic [ð] became [r]
- вариант правила [medial [ð], [z] dissimilated to [l], [s] after [r]](https://eldamo.org/content/words/word-455699965.html)

| подформула | вид | примеры |
|---|---|---|
| `rVð > rVl` | contextual | — |

### [intervocalic [ð] became [r]](https://eldamo.org/content/words/word-3914129125.html)

- порядок 01800
- общая формула `Vð{Vw} > Vr{Vw}`
- позже, чем: medial [ð] dissimilated to [l] after [r]
- вариант правила [intervocalic [ð] became [r]](https://eldamo.org/content/words/word-2793529037.html)

| подформула | вид | примеры |
|---|---|---|
| `VðV > VrV` | contextual | 10 / 7 |
| `Vðw > Vrw` | contextual | 1 / 1 |
| `Vðj > Vrj` | contextual | 1 / 1 |

### [long vowels shortened before consonant clusters](https://eldamo.org/content/words/word-1524904053.html)

- порядок 01900
- общая формула `V̄CC|V̄tj|V̄kw > V̆CC|V̄tj|V̄kw`
- вариант правила [long vowels shortened before consonant clusters](https://eldamo.org/content/words/word-4125237087.html)

### [long final vowels were shortened](https://eldamo.org/content/words/word-1072764601.html)

- порядок 02000
- общая формула `-SV̄ > -SV̆`
- раньше, чем: [θ] became [s]; short final [a], [e], [o] lost in long compounds; [sp], [sk] became [ps], [ks]
- позже, чем: [ae], [ao] generally became [ē], [ō]
- вариант правила [long final vowels were shortened](https://eldamo.org/content/words/word-2821506177.html)

| подформула | вид | примеры |
|---|---|---|
| `-Sī > -Sĭ` | contextual | 4 / 4 |
| `-Sē > -Sĕ` | contextual | 75 / 73 |
| `-Sā > -Să` | contextual | 130 / 125 |
| `-Sō > -Sŏ` | contextual | 35 / 35 |
| `-Sū > -Sŭ` | contextual | 5 / 5 |
| `-SāC > -SăC` | contextual | 6 / 6 |
| `-SēC > -SĕC` | contextual | 2 / 2 |
| `-SōC > -SŏC` | contextual | 7 / 7 |

### [[-ai] became [-e]](https://eldamo.org/content/words/word-356705051.html)

- порядок 02100
- вариант правила [[-ai] became [-e]](https://eldamo.org/content/words/word-2761837707.html)

| подформула | вид | примеры |
|---|---|---|
| `-ai > -e` | literal | — |

### [[ij], [uw] became [i], [u]](https://eldamo.org/content/words/word-2416213929.html)

- порядок 02200
- общая формула `ijV|uwV > iV|uV`
- вариант правила [[ij], [uw] became [i], [u]](https://eldamo.org/content/words/word-1619715205.html)

| подформула | вид | примеры |
|---|---|---|
| `ij > i` | literal | 6 / 6 |
| `uw > u` | literal | 1 / 1 |

### [short final [a], [e], [o] lost in long compounds](https://eldamo.org/content/words/word-3760896435.html)

- порядок 02300
- общая формула `-SSS{ăĕŏ} > -SSSø`
- раньше, чем: final consonant clusters reduced
- позже, чем: long final vowels were shortened
- вариант правила [short final [a], [e], [o] lost in long compounds](https://eldamo.org/content/words/word-3904029624.html)

| подформула | вид | примеры |
|---|---|---|
| `-SSSă > -SSSø` | contextual | — |
| `-SSSĕ > -SSSø` | contextual | 1 / 1 |
| `-SSSŏ > -SSSø` | contextual | — |

### [nasals and liquids often became syllabic after a consonant](https://eldamo.org/content/words/word-277667125.html)

- порядок 02400
- общая формула `ClV₁|ml|Cr|{ptk}n|{ptk}m > CV₁lV₁|mul|Car|{ptk}an|{ptk}um`
- вариант правила [nasals and liquids often became syllabic after a consonant](https://eldamo.org/content/words/word-613618983.html)

| подформула | вид | примеры |
|---|---|---|
| `-Cl > -Cil` | contextual | — |
| `-aCl > -aCal` | contextual | — |

### [final consonant clusters reduced](https://eldamo.org/content/words/word-4243668855.html)

- порядок 02500
- общая формула `-CC > -C`
- раньше, чем: [z] became [r]
- позже, чем: short final [a], [e], [o] lost in long compounds
- вариант правила [final consonant clusters reduced](https://eldamo.org/content/words/word-731874859.html)

| подформула | вид | примеры |
|---|---|---|
| `-CC > -C` | contextual | 27 / 27 |
| `-xt > -t` | literal | 1 / 1 |
| `-ps > -s` | literal | — |
| `-ts > -s` | literal | — |
| `-ks > -s` | literal | 2 / 2 |

### [final spirants were altered](https://eldamo.org/content/words/word-1377107961.html)

- порядок 02600
- общая формула `-{θðv} > -{trw}`
- раньше, чем: [θ] became [s]
- вариант правила [final spirants were altered](https://eldamo.org/content/words/word-3424103699.html)

| подформула | вид | примеры |
|---|---|---|
| `-θ > -t` | literal | — |
| `-ð > -r` | literal | 6 / 6 |

### [final consonants became dentals](https://eldamo.org/content/words/word-2371293137.html)

- порядок 02700
- общая формула `-{km} > -{tn}`
- вариант правила [final consonants became dentals](https://eldamo.org/content/words/word-3283441787.html)

| подформула | вид | примеры |
|---|---|---|
| `-k > -t` | literal | 3 / 3 |
| `-m > -n` | literal | 5 / 5 |

### [[ŋn] assimilated to following [n] after [e], [a], [o]](https://eldamo.org/content/words/word-4209459411.html)

- порядок 02800
- общая формула `{eao}ŋn > {eao}nn`
- вариант правила [[ŋ] assimilated to following [n] after [e], [a], [o]](https://eldamo.org/content/words/word-368875839.html)

| подформула | вид | примеры |
|---|---|---|
| `eŋn > enn` | literal | 2 / 2 |
| `aŋn > ann` | literal | — |
| `oŋn > onn` | literal | — |

### [[ɸu] became [hu]](https://eldamo.org/content/words/word-223912721.html)

- порядок 02900
- раньше, чем: [ɸ], [β] became [f], [v]
- вариант правила [[ɸu] became [hu]](https://eldamo.org/content/words/word-1102872571.html)

| подформула | вид | примеры |
|---|---|---|
| `ɸu > hu` | literal | 3 / 3 |

### [[ɸ], [β] became [f], [v]](https://eldamo.org/content/words/word-2661449019.html)

- порядок 03000
- общая формула `ɸ|β > f|v`
- позже, чем: [ɸu] became [hu]; [β], [ɣ] vocalized before voiced consonants
- вариант правила [[ɸ], [β] became [f], [v]](https://eldamo.org/content/words/word-14484545.html)

| подформула | вид | примеры |
|---|---|---|
| `ɸ > f` | literal | 49 / 49 |
| `β > v` | literal | 60 / 60 |

### [[sf] became [f]](https://eldamo.org/content/words/word-1165599019.html)

- порядок 03100
- вариант правила [[sf] became [f]](https://eldamo.org/content/words/word-946722487.html)

| подформула | вид | примеры |
|---|---|---|
| `sf > f` | literal | — |

### [[lg], [rg] became [ll], [rr]](https://eldamo.org/content/words/word-1946719133.html)

- порядок 03200
- общая формула `lɣ|rɣ > ll|rr`
- вариант правила [[lɣ], [rɣ] became [ll], [rr]](https://eldamo.org/content/words/word-2837004771.html)

| подформула | вид | примеры |
|---|---|---|
| `rg > rr` | literal | — |
| `lg > ll` | literal | — |

### [[w] became [v] initially and between vowels](https://eldamo.org/content/words/word-1330821765.html)

- порядок 03200
- общая формула `w-|VwV|aiw > v-|VvV|aiw`
- позже, чем: [j], [w] often reduced between vowels; [wo] became [o]
- вариант правила [[w] became [β] initially and between vowels](https://eldamo.org/content/words/word-3625908403.html)

| подформула | вид | примеры |
|---|---|---|
| `w- > v-` | literal | 28 / 27 |
| `VwV > VvV` | contextual | 9 / 9 |
| `aiw > aiw` | identity | 2 / 0 |

### [[θ] became [s]](https://eldamo.org/content/words/word-3006504693.html)

- порядок 03400
- позже, чем: final spirants were altered; long final vowels were shortened
- вариант правила [[θ] became [s]](https://eldamo.org/content/words/word-3491983963.html)

| подформула | вид | примеры |
|---|---|---|
| `θ > s` | literal | 44 / 43 |

### [[sp], [sk] became [ps], [ks]](https://eldamo.org/content/words/word-3499874945.html)

- порядок 03500
- общая формула `sp|sk|skw > ps|ks|skw`
- раньше, чем: initial [ps], [ks] became [s]
- позже, чем: [z] plus voiced stop became unvoiced; long final vowels were shortened; syllabic initial [s] became [is]
- вариант правила [[sp], [sk] became [ps], [ks]](https://eldamo.org/content/words/word-2094898289.html)

| подформула | вид | примеры |
|---|---|---|
| `sp > ps` | literal | 1 / 1 |
| `sk > ks` | literal | 5 / 5 |

### [[d] vanished between [n], [r], [l] and [j]](https://eldamo.org/content/words/word-2488350997.html)

- порядок 03600
- общая формула `{nrl}dj > {nrl}øj`
- позже, чем: spirants became stops after [r], [l]
- вариант правила [[d] vanished between [n], [r], [l] and [j]](https://eldamo.org/content/words/word-297797679.html)

| подформула | вид | примеры |
|---|---|---|
| `ldj > lj` | literal | — |
| `ndj > nj` | literal | 4 / 4 |
| `rdj > rj` | literal | — |

### [[z] became [r]](https://eldamo.org/content/words/word-14189179.html)

- порядок 03700
- позже, чем: [x] became [h] except before [t]; [z] assimilated to following [m], [n]; final consonant clusters reduced
- вариант правила [[z] became [r]](https://eldamo.org/content/words/word-3534004155.html)

| подформула | вид | примеры |
|---|---|---|
| `z > r` | literal | 13 / 13 |

### [[rs] became [ss]](https://eldamo.org/content/words/word-2756914109.html)

- порядок 03800
- вариант правила [[rs] became [ss]](https://eldamo.org/content/words/word-1326730955.html)

| подформула | вид | примеры |
|---|---|---|
| `rs > ss` | literal | 1 / 0 |

### [initial [ŋ] became [n]](https://eldamo.org/content/words/word-1117953113.html)

- порядок 03900
- вариант правила [initial [ŋ] became [n]](https://eldamo.org/content/words/word-1073266651.html)

| подформула | вид | примеры |
|---|---|---|
| `ŋ- > n-` | literal | 19 / 19 |

### [initial [ps], [ks] became [s]](https://eldamo.org/content/words/word-93837315.html)

- порядок 04000
- общая формула `{pk}s- > s-`
- позже, чем: [sp], [sk] became [ps], [ks]
- вариант правила [initial [ps], [ks] became [ups], [iks]](https://eldamo.org/content/words/word-2166344385.html)

| подформула | вид | примеры |
|---|---|---|
| `ps- > s-` | literal | — |
| `ks- > s-` | literal | — |
| `ts- > s-` | literal | — |

### [exilic [ts] became [ss]](https://eldamo.org/content/words/word-4002555499.html)

- порядок 04100
- вариант правила [exilic [ts] became [ss]](https://eldamo.org/content/words/word-173969535.html)

| подформула | вид | примеры |
|---|---|---|
| `ts > ss` | literal | 1 / 1 |

### [final [t] became [s]](https://eldamo.org/content/words/word-539818035.html)

- порядок 04200
- вариант правила [final [t] became [s]](https://eldamo.org/content/words/word-2842904179.html)

| подформула | вид | примеры |
|---|---|---|
| `-t > -s` | literal | — |

### [[v] became [w] after [l], [r]](https://eldamo.org/content/words/word-1677814291.html)

- порядок 04300
- общая формула `{lr}v > {lr}w`
- вариант правила [[w] became [v] after [l], [r]](https://eldamo.org/content/words/word-2276015165.html)

### [unstressed [ir], [ur] sometimes became [er], [or]](https://eldamo.org/content/words/word-2540314691.html)

- порядок 04400
- общая формула `Ś{ĭŭ}r > Ś{eo}r`
- вариант правила [unstressed [ir], [ur] sometimes became [er], [or]](https://eldamo.org/content/words/word-642778275.html)

| подформула | вид | примеры |
|---|---|---|
| `Śĭr > Śer` | contextual | 2 / 2 |
| `Śŭr > Śor` | contextual | — |

## ᴱ✶ Early Primitive Elvish (ранняя концепция)

### [intervocalic [l] may have had different developments by position](https://eldamo.org/content/words/word-1942014713.html)

- порядок 00100

### [nasals assimilated to following consonant](https://eldamo.org/content/words/word-2698200055.html)

- порядок 00200
- общая формула `{mnŋ}{pb}|{mnŋ}{td}|{mnŋ}{kg} > m{pb}|n{td}|ŋ{kg}`
- вариант правила [nasals assimilated to following stops and aspirates](https://eldamo.org/content/words/word-2390772785.html)

| подформула | вид | примеры |
|---|---|---|
| `nb > mb` | literal | 2 / 2 |
| `nk > ŋk` | literal | 2 / 2 |
| `mk > ŋk` | literal | 1 / 0 |
| `md > nd` | literal | 1 / 1 |
| `mt > nt` | literal | 3 / 3 |
| `ṃt > ṇt` | literal | 4 / 2 |

### [short final [e], [a], [o] became [ǝ]](https://eldamo.org/content/words/word-2954387961.html)

- порядок 00300
- общая формула `-S{ĕăŏ} > -Sǝ`
- раньше, чем: final [ǝ] vanished
- вариант правила [short final [e], [a], [o] vanished](https://eldamo.org/content/words/word-3998109579.html)

| подформула | вид | примеры |
|---|---|---|
| `-Sĕ > -Sǝ` | contextual | 3 / 1 |
| `-Să > -Sǝ` | contextual | 11 / 11 |
| `-Sŏ > -Sǝ` | contextual | 1 / 1 |

### [final [ǝ] vanished](https://eldamo.org/content/words/word-1398002213.html)

- порядок 00400
- раньше, чем: short final [i], [u] became [e], [o]
- позже, чем: short final [e], [a], [o] became [ǝ]
- вариант правила [short final [e], [a], [o] vanished](https://eldamo.org/content/words/word-3998109579.html)

| подформула | вид | примеры |
|---|---|---|
| `-ǝ > -ø` | loss | 80 / 72 |

### [final [j], [w] became [i], [u]](https://eldamo.org/content/words/word-2186610087.html)

- порядок 00500
- общая формула `-{jw} > -{iu}`
- раньше, чем: short final [i], [u] became [e], [o]; final [l], [r], [n] became syllabic after a consonant
- вариант правила [short final [e], [a], [o] vanished](https://eldamo.org/content/words/word-3998109579.html)

| подформула | вид | примеры |
|---|---|---|
| `-j > -i` | literal | 6 / 6 |
| `-w > -u` | literal | 2 / 2 |

### [short final [i], [u] became [e], [o]](https://eldamo.org/content/words/word-4062489737.html)

- порядок 00600
- общая формула `-{ĭŭ} > -{eo}`
- позже, чем: final [ǝ] vanished; final [j], [w] became [i], [u]
- вариант правила [short final [i], [u] became [e], [o]](https://eldamo.org/content/words/word-2698078435.html)

| подформула | вид | примеры |
|---|---|---|
| `-Sĭ > -Se` | contextual | 85 / 75 |
| `-Sŭ > -So` | contextual | 19 / 12 |

### [long vowels shortened before consonant groups and in diphthongs](https://eldamo.org/content/words/word-2461772055.html)

- порядок 00700
- общая формула `V̄CC|V̄V > V̆CC|V̆V`
- вариант правила [long vowels shortened before consonant clusters](https://eldamo.org/content/words/word-2818407091.html)

### [[kʷu] became [ku]](https://eldamo.org/content/words/word-666754093.html)

| подформула | вид | примеры |
|---|---|---|
| `kʷu > ku` | literal | — |

### [final [ai] became [ī]](https://eldamo.org/content/words/word-2628655373.html)

| подформула | вид | примеры |
|---|---|---|
| `-ai > -ī` | literal | 1 / 1 |

### [final [l], [r], [n] became syllabic after a consonant](https://eldamo.org/content/words/word-3594765139.html)

- общая формула `-C{lrn} > -C{ḷṛṇ}`
- позже, чем: final [j], [w] became [i], [u]

| подформула | вид | примеры |
|---|---|---|
| `-Cl > -Cḷ` | contextual | 26 / 26 |
| `-Cr > -Cṛ` | contextual | — |
| `-Cn > -Cṇ` | contextual | — |

### [initial nasalized voiced stops reduced to stops](https://eldamo.org/content/words/word-3141061005.html)

- общая формула `{ŋgʷ|ŋg|nd|ndʲ|mb}- > {gʷ|g|d|dʲ|b}-`

| подформула | вид | примеры |
|---|---|---|
| `mb- > b-` | literal | — |

### [voiced stops became nasals before nasals](https://eldamo.org/content/words/word-2168100881.html)

- общая формула `{bdg}{mn} > {mnŋ}{mn}`

| подформула | вид | примеры |
|---|---|---|
| `bm > mm` | literal | — |
| `bn > mn` | literal | 2 / 2 |
| `dm > nm` | literal | — |
| `dn > nn` | literal | — |
| `gm > ŋm` | literal | — |
| `gn > ŋn` | literal | — |

### [voiced stops unvoiced before voiceless consonants](https://eldamo.org/content/words/word-4185647833.html)

- общая формула `{bdg}{ptks} > {ptk}{ptks}`
- вариант правила [voiced stops unvoiced before voiceless consonants](https://eldamo.org/content/words/word-2905876955.html)

| подформула | вид | примеры |
|---|---|---|
| `gt > kt` | literal | 1 / 1 |

## ᴱQ. Early Quenya (ранняя концепция)

### [long final vowels were shortened](https://eldamo.org/content/words/word-504909023.html)

- порядок 00100
- общая формула `-SV̄ > -SV̆`
- вариант правила [long final vowels were shortened](https://eldamo.org/content/words/word-1072764601.html)

| подформула | вид | примеры |
|---|---|---|
| `-Sī > -Sĭ` | contextual | 39 / 33 |
| `-Sē > -Sĕ` | contextual | 282 / 268 |
| `-Sā > -Să` | contextual | 455 / 395 |
| `-Sō > -Sŏ` | contextual | 64 / 57 |
| `-Sū > -Sŭ` | contextual | 39 / 35 |

### [long syllabic [ḹ], [ṝ] became [al], [ar]](https://eldamo.org/content/words/word-3968461507.html)

- порядок 00200
- общая формула `ḹ|ṝ > al|ar`

| подформула | вид | примеры |
|---|---|---|
| `ḹ > al` | literal | 49 / 49 |
| `-ḹ > -āl` | literal | — |
| `ṝ > ar` | literal | 15 / 15 |
| `-ṝ > -ār` | literal | — |

### [long syllabic [ṇ̄] became [a] + homorganic nasal](https://eldamo.org/content/words/word-406180735.html)

- порядок 00300
- общая формула `ṇ̄ > an`

| подформула | вид | примеры |
|---|---|---|
| `ṇ̄ > an` | literal | 8 / 7 |
| `ṇ̄k > aŋk` | literal | — |
| `ṇ̄kʷ > aŋkʷ` | literal | 8 / 8 |
| `ṇ̄p > amp` | literal | 4 / 1 |
| `-ṇ̄ > -ān` | literal | — |

### [short syllabic [ḷ] became [il], or [ul] before labials](https://eldamo.org/content/words/word-1720939405.html)

- порядок 00400
- общая формула `ḷ|ḷ{pbɸmw}|ḷCʷ > il|ul{pbɸmw}|ulCʷ`
- вариант правила [[r], [l] often became syllabic in clusters](https://eldamo.org/content/words/word-720793221.html)

| подформула | вид | примеры |
|---|---|---|
| `ḷ > il` | literal | 36 / 35 |
| `ḷp > ulp` | literal | 9 / 9 |
| `ḷb > ulb` | literal | 1 / 1 |
| `ḷɸ > ulɸ` | literal | 1 / 1 |
| `ḷm > ulm` | literal | 1 / 1 |
| `ḷw > ulw` | literal | — |
| `ḷkʷ > ulkʷ` | literal | 2 / 2 |
| `-Cḷ > -Cḷ` | contextual | 26 / 0 |

### [short syllabic [ṇ] became [a] + homorganic nasal, [i] before palatals or [u] before labials](https://eldamo.org/content/words/word-2670096403.html)

- порядок 00500
- общая формула `ṇ|ṇCj|ṇ{kg}|ṇp|ṇCw > an|inCj|aŋ{kg}|ump|uŋCw`

| подформула | вид | примеры |
|---|---|---|
| `ṇ > an` | literal | 36 / 33 |
| `ṇCʲ > inCʲ` | contextual | 7 / 0 |
| `ṇk > aŋk` | literal | 4 / 3 |
| `ṇg > aŋg` | literal | 3 / 3 |
| `ṇp > ump` | literal | 1 / 1 |
| `ṇCʷ > uŋCʷ` | contextual | 9 / 0 |
| `kʷṇ > kun` | literal | 1 / 1 |
| `-Cn > -Ca` | contextual | 1 / 1 |

### [short syllabic [ṛ] became [ar], [ir] before palatalized consonants or [ur] after [w] and [kʷ]](https://eldamo.org/content/words/word-2915077261.html)

- порядок 00600
- общая формула `ṛ|ṛCʲ|wṛ > ar|irCʲ|ur`
- вариант правила [[r], [l] often became syllabic in clusters](https://eldamo.org/content/words/word-720793221.html)

| подформула | вид | примеры |
|---|---|---|
| `ṛ > ar` | literal | 42 / 42 |
| `ṛCʲ > irCʲ` | contextual | 6 / 0 |
| `wṛ > ur` | literal | 2 / 2 |
| `kʷṛ > kur` | literal | 1 / 1 |

### [syllabic [s] developed a vowel](https://eldamo.org/content/words/word-967048541.html)

- порядок 00700
- общая формула `ṣ|ṣCʷ|ṣ̄|ẓ > is|usCʷ|as|iz`
- вариант правила [syllabic initial [s] became [is]](https://eldamo.org/content/words/word-2033267709.html)

| подформула | вид | примеры |
|---|---|---|
| `ṣ > is` | literal | 5 / 5 |
| `ṣCʷ > usCʷ` | contextual | 1 / 0 |
| `ṣ̄ > as` | literal | 3 / 3 |
| `ẓ > iz` | literal | 1 / 1 |

### [[θʲi] became [xi]](https://eldamo.org/content/words/word-1652146593.html)

- порядок 00800
- раньше, чем: palatals became dentals before [i]
- позже, чем: voiceless spirants became stops after nasals

| подформула | вид | примеры |
|---|---|---|
| `θʲi > xi` | literal | 1 / 0 |

### [[θʲ] became [θ] before stops](https://eldamo.org/content/words/word-3802989615.html)

- порядок 00900
- раньше, чем: [θ] became [s]

| подформула | вид | примеры |
|---|---|---|
| `θʲ{ptk} > θ{ptk}` | contextual | — |

### [initial [θʲ] became [sj]](https://eldamo.org/content/words/word-2921880273.html)

- порядок 00900
- раньше, чем: initial [sw] and [sβ] became [f], [sj] became [j̊]

| подформула | вид | примеры |
|---|---|---|
| `θʲ- > sj-` | literal | 6 / 6 |

### [[θ] became [s]](https://eldamo.org/content/words/word-281616373.html)

- порядок 01100
- раньше, чем: initial [sw] and [sβ] became [f], [sj] became [j̊]; [s] became [z] before nasals and voiced spirants; voiceless spirants became stops before stops, [s] or [z]; [tʲ], [kʷ] became [t], [k] before [t], [s]
- позже, чем: [θ] became [ð] after voiced spirants and stops; [θʲ] became [θ] before stops; [xs] became [xx]; voiceless spirants became stops after nasals; voiceless spirant combinations assimilated except to [θ]; voiceless spirants voiced after liquids
- вариант правила [[θ] became [s]](https://eldamo.org/content/words/word-3006504693.html)

| подформула | вид | примеры |
|---|---|---|
| `θ > s` | literal | 46 / 46 |

### [[xʷu] became [xu]](https://eldamo.org/content/words/word-4101283277.html)

- порядок 01200
- раньше, чем: initial and intervocalic [xʷ] became [f]; voiceless spirants became stops after nasals; voiceless spirants voiced after liquids

| подформула | вид | примеры |
|---|---|---|
| `xʷu > xu` | literal | 5 / 5 |

### [initial and intervocalic [xʷ] became [f]](https://eldamo.org/content/words/word-3717166775.html)

- порядок 01300
- общая формула `xʷ-|VxʷV > f-|VfV`
- раньше, чем: intervocalic voiceless spirants became voiced
- позже, чем: [xʷu] became [xu]

| подформула | вид | примеры |
|---|---|---|
| `xʷ- > f-` | literal | 2 / 2 |
| `VxʷV > VfV` | contextual | — |

### [[ɸ] usually became [f]](https://eldamo.org/content/words/word-1670039283.html)

- порядок 01400
- общая формула `ɸ|ɸɣʷ|ɸðʲ|ɸu > f|f|j̊|βu`
- раньше, чем: intervocalic voiceless spirants became voiced; geminate voiceless spirants reduced; [β] vanished before [u]
- позже, чем: voiceless spirants became stops before stops, [s] or [z]
- вариант правила [[ɸ], [β] became [f], [v]](https://eldamo.org/content/words/word-2661449019.html)

| подформула | вид | примеры |
|---|---|---|
| `ɸ > f` | literal | 52 / 52 |
| `ɸɣʷ > f` | literal | — |
| `ɸðʲ > j̊` | literal | — |
| `ɸu > βu` | literal | — |

### [final [s] became [r]](https://eldamo.org/content/words/word-3490136699.html)

- порядок 01500
- раньше, чем: final [ss], [st], [ps], [ts], [ks] became [s]

| подформула | вид | примеры |
|---|---|---|
| `-Vs > -Vr` | contextual | 15 / 15 |

### [final [sk] became [ss]](https://eldamo.org/content/words/word-2789267955.html)

- порядок 01600
- раньше, чем: final [ss], [st], [ps], [ts], [ks] became [s]

| подформула | вид | примеры |
|---|---|---|
| `-sk > -ss` | literal | 1 / 1 |

### [final [ss], [st], [ps], [ts], [ks] became [s]](https://eldamo.org/content/words/word-2485190991.html)

- порядок 01700
- общая формула `-s{st}|-{ptk}s > -s|-s`
- позже, чем: final [s] became [r]; final [sk] became [ss]

| подформула | вид | примеры |
|---|---|---|
| `-ss > -s` | literal | 14 / 14 |
| `-ps > -s` | literal | — |
| `-ts > -s` | literal | 2 / 2 |
| `-ks > -s` | literal | 3 / 3 |
| `-st > -s` | literal | 27 / 27 |

### [final consonant clusters simplified](https://eldamo.org/content/words/word-4175300709.html)

- порядок 01800
- общая формула `-CC > -C`
- вариант правила [final consonant clusters reduced](https://eldamo.org/content/words/word-4243668855.html)

| подформула | вид | примеры |
|---|---|---|
| `-ld > -l` | literal | 5 / 5 |
| `-ll > -l` | literal | 2 / 2 |
| `-ln > -l` | literal | 1 / 1 |
| `-lp > -lt` | literal | 2 / 2 |
| `-nd > -n` | literal | 39 / 38 |
| `-nn > -n` | literal | 1 / 1 |
| `-mp > -nt` | literal | 3 / 3 |
| `-ŋkʷ > -ŋk` | literal | 3 / 3 |
| `-rt > -r` | literal | 2 / 2 |
| `-rd > -r` | literal | 13 / 13 |
| `-rm > -r` | literal | 1 / 1 |
| `-rn > -r` | literal | 6 / 6 |
| `-rr > -r` | literal | 1 / 1 |
| `-rp > -rt` | literal | 1 / 1 |
| `-tt > -t` | literal | 8 / 8 |
| `-tʲ > -t` | literal | 12 / 12 |
| `-kḷ > -tḷ` | literal | 5 / 5 |
| `-pḷ > -tḷ` | literal | 3 / 3 |
| `-mpḷ > -ntḷ` | literal | 1 / 1 |
| `-kt > -tt` | literal | 1 / 1 |
| `-kt > -t` | literal | 10 / 10 |
| `-pt > -t` | literal | 4 / 4 |

### [final [nt] became [n] in polysyllables](https://eldamo.org/content/words/word-1312700867.html)

- порядок 01900

| подформула | вид | примеры |
|---|---|---|
| `-SSnt > -SSn` | contextual | 1 / 1 |

### [intervocalic voiceless spirants became voiced](https://eldamo.org/content/words/word-110060203.html)

- порядок 02000
- общая формула `V{fθθʲx}V > V{vððʲɣ}V`
- раньше, чем: [ɣ] otherwise vanished
- позже, чем: [ɸ] usually became [f]; initial and intervocalic [xʷ] became [f]

| подформула | вид | примеры |
|---|---|---|
| `VfV > VvV` | contextual | 6 / 6 |
| `VθV > VðV` | contextual | — |
| `VθʲV > VðʲV` | contextual | 2 / 2 |
| `VxV > VɣV` | contextual | 18 / 17 |
| `VxʷV > VɣʷV` | contextual | — |

### [between vowels and consonants [ɣ] vanished with compensatory lengthening](https://eldamo.org/content/words/word-3676149149.html)

- порядок 02100
- раньше, чем: middle consonant lost in three-consonant cluster
- позже, чем: voiceless spirants voiced before voiced continuants
- вариант правила [[β], [ɣ] vocalized before voiced consonants](https://eldamo.org/content/words/word-641476107.html)

| подформула | вид | примеры |
|---|---|---|
| `VɣC > V̄øC` | contextual | 28 / 28 |

### [final [ɣ] vanished with compensatory lengthening](https://eldamo.org/content/words/word-3415804419.html)

- порядок 02200
- позже, чем: final voiceless spirants were weakened and voiced

| подформула | вид | примеры |
|---|---|---|
| `-Vɣ > -V̄ø` | contextual | 14 / 14 |

### [initial [ɣ] vanished or became [h]](https://eldamo.org/content/words/word-3275368525.html)

- порядок 02300
- общая формула `ɣ-|ɣ- > ø-|h-`
- вариант правила [initial [ɣ] became [h]](https://eldamo.org/content/words/word-1968067631.html)

| подформула | вид | примеры |
|---|---|---|
| `ɣ- > ø-` | loss | 15 / 15 |
| `ɣ- > h-` | literal | 3 / 3 |

### [[ɣ] otherwise vanished](https://eldamo.org/content/words/word-71510193.html)

- порядок 02400
- раньше, чем: [wo] became [o]
- позже, чем: intervocalic voiceless spirants became voiced; voiced stops became spirants after vowels
- вариант правила [[ɣ] from [g] vanished](https://eldamo.org/content/words/word-3266317297.html)

| подформула | вид | примеры |
|---|---|---|
| `ɣ > ø` | loss | 33 / 32 |

### [[ij], [uw] became [i], [u]](https://eldamo.org/content/words/word-2796400083.html)

- порядок 02500
- общая формула `ij|uw > i|u`
- раньше, чем: [j], [w] became [i], [u] after a vowel
- вариант правила [[ij], [uw] became [i], [u]](https://eldamo.org/content/words/word-2416213929.html)

| подформула | вид | примеры |
|---|---|---|
| `ij > i` | literal | 6 / 6 |
| `uw > u` | literal | 1 / 1 |
| `ejV > eV` | contextual | — |
| `owV > oV` | contextual | — |

### [[ji], [wu] became [i], [u] after a vowel](https://eldamo.org/content/words/word-609719289.html)

- порядок 02600
- общая формула `Vji|Vwu > Vi|Vu`
- раньше, чем: [ei], [ou] became [ai], [au]; [ðʲ] became [j]

| подформула | вид | примеры |
|---|---|---|
| `aji > ai` | literal | — |
| `eji > ei` | literal | — |
| `awu > au` | literal | — |
| `owu > ou` | literal | — |

### [[jǝ], [wǝ] became [je], [wo] after a vowel](https://eldamo.org/content/words/word-1017982247.html)

- порядок 02700
- общая формула `Vjǝ|Vwǝ > Vje|Vwo`
- раньше, чем: [aie] became [aije]; [ei] became [e] before [a], [o] or [u], but [i] before [e]; [au] became [o] before unstressed vowel, but [aw] before stressed vowel; [ou] became [u] before [e] and [o], but [o] before [i] and [a]

| подформула | вид | примеры |
|---|---|---|
| `ajǝ > aje` | literal | — |
| `ejǝ > eje` | literal | — |
| `awǝ > awo` | literal | — |
| `owǝ > owo` | literal | — |

### [short [i], [u] became [j], [w] between a consonant and vowel](https://eldamo.org/content/words/word-3171133497.html)

- порядок 02800
- общая формула `V{ĭŭ}C > V{jw}C`

| подформула | вид | примеры |
|---|---|---|
| `CĭV > CjV` | contextual | — |
| `CŭV > CwV` | contextual | 2 / 2 |

### [[j], [w] became [i], [u] after a vowel](https://eldamo.org/content/words/word-2868696637.html)

- порядок 02900
- общая формула `V{jw} > V{iu}`
- позже, чем: [ij], [uw] became [i], [u]

| подформула | вид | примеры |
|---|---|---|
| `Vj > Vi` | contextual | 44 / 44 |
| `Vw > Vu` | contextual | 43 / 42 |

### [[aie] became [aije]](https://eldamo.org/content/words/word-93891029.html)

- порядок 03000
- общая формула `aie > aije`
- позже, чем: [jǝ], [wǝ] became [je], [wo] after a vowel

| подформула | вид | примеры |
|---|---|---|
| `aie > aije` | literal | 1 / 1 |

### [[ai] became [e] before unstressed [a], [o] or [u], but [aj] before stressed [a], [o] or [u]](https://eldamo.org/content/words/word-3015430929.html)

- порядок 03100
- общая формула `ai{auo}|ai{áóú} > eø{auo}|aj{áóú}`
- вариант правила [[j], [w] often reduced between vowels](https://eldamo.org/content/words/word-1324632797.html)

| подформула | вид | примеры |
|---|---|---|
| `aia > ea` | literal | — |
| `aio > eo` | literal | — |
| `aiu > eu` | literal | — |
| `aiá > ajá` | literal | — |
| `aió > ajó` | literal | — |
| `aiú > ajú` | literal | — |

### [[ei] became [e] before [a], [o] or [u], but [i] before [e]](https://eldamo.org/content/words/word-3875992065.html)

- порядок 03200
- общая формула `ei{auo} > eø{auo}`
- позже, чем: [jǝ], [wǝ] became [je], [wo] after a vowel

| подформула | вид | примеры |
|---|---|---|
| `eia > ea` | literal | 3 / 3 |
| `eio > eo` | literal | — |
| `eiu > eu` | literal | — |
| `eie > ie` | literal | 9 / 8 |

### [[au] became [o] before unstressed vowel, but [aw] before stressed vowel](https://eldamo.org/content/words/word-964124395.html)

- порядок 03300
- общая формула `au{ieao}|au{íéáó} > oø{ieao}|aw{íéáó}`
- раньше, чем: [oe] became [oa]
- позже, чем: [jǝ], [wǝ] became [je], [wo] after a vowel
- вариант правила [[j], [w] often reduced between vowels](https://eldamo.org/content/words/word-1324632797.html)

| подформула | вид | примеры |
|---|---|---|
| `aui > oi` | literal | 2 / 2 |
| `aue > oe` | literal | — |
| `aua > oa` | literal | 4 / 4 |
| `auo > ō` | literal | — |
| `auí > awí` | literal | — |
| `aué > awé` | literal | 2 / 2 |
| `auá > awá` | literal | 2 / 2 |
| `auó > awó` | literal | — |

### [[ou] became [u] before [e] and [o], but [o] before [i] and [a]](https://eldamo.org/content/words/word-2475648287.html)

- порядок 03400
- общая формула `ou{eo}|ou{ia} > uø{eo}|oø{ia}`
- раньше, чем: [ei], [ou] became [ai], [au]
- позже, чем: [jǝ], [wǝ] became [je], [wo] after a vowel
- вариант правила [[j], [w] often reduced between vowels](https://eldamo.org/content/words/word-1324632797.html)

| подформула | вид | примеры |
|---|---|---|
| `oue > ue` | literal | 1 / 1 |
| `ouo > uo` | literal | 2 / 2 |
| `oui > oi` | literal | 2 / 2 |
| `oua > oa` | literal | 4 / 3 |

### [[oi], [ui] became [oij], [uij] before unstressed vowel, [oj], [uj] before stressed vowel](https://eldamo.org/content/words/word-554348879.html)

- порядок 03500
- общая формула `{ou}iV|{ou}iV́ > {ou}ijV|{ou}jV́`

| подформула | вид | примеры |
|---|---|---|
| `oiV > oijV` | contextual | — |
| `uiV > uijV` | contextual | — |
| `oiV́ > ojV́` | contextual | — |
| `uiV́ > ujV́` | contextual | — |

### [[eu], [iu] became [euw], [iuw] before unstressed vowel, [ew], [iw] before stressed vowel](https://eldamo.org/content/words/word-1625996953.html)

- порядок 03600
- общая формула `{ei}uV|{ei}uV́ > {ei}uwV|{ei}wV́`

| подформула | вид | примеры |
|---|---|---|
| `euV > euwV` | contextual | — |
| `iuV > iuwV` | contextual | — |
| `euV́ > ewV́` | contextual | — |
| `iuV́ > iwV́` | contextual | 1 / 0 |

### [intervocalic [ū], [ī] became [uw], [ij]](https://eldamo.org/content/words/word-834390781.html)

- порядок 03700
- общая формула `VūV|VīV > VuwV|VijV`
- раньше, чем: [w] became [v] after [u] and [o] and before [o]; [ei], [ou] became [ai], [au]
- вариант правила [intervocalic [j] diphthongized after long vowel](https://eldamo.org/content/words/word-3477758271.html)

| подформула | вид | примеры |
|---|---|---|
| `VūV > VuwV` | contextual | 1 / 1 |
| `VīV > VijV` | contextual | 1 / 1 |

### [[ae], [ao] generally became [ā]](https://eldamo.org/content/words/word-794699965.html)

- порядок 03800
- общая формула `a{eo}|ăō > ā|ō`
- вариант правила [[ae], [ao] generally became [ē], [ō]](https://eldamo.org/content/words/word-205917541.html)

| подформула | вид | примеры |
|---|---|---|
| `ae > ā` | literal | — |
| `ao > ā` | literal | — |
| `ăō > ō` | literal | 1 / 0 |

### [[oe] became [oa]](https://eldamo.org/content/words/word-1504974675.html)

- порядок 03900
- позже, чем: [au] became [o] before unstressed vowel, but [aw] before stressed vowel

| подформула | вид | примеры |
|---|---|---|
| `oe > oa` | literal | — |

### [[ǝ] assimilated to preceding vowel](https://eldamo.org/content/words/word-774448523.html)

- порядок 04000
- общая формула `Vǝ > V̄`

| подформула | вид | примеры |
|---|---|---|
| `eǝ > ē` | literal | — |
| `aǝ > ā` | literal | — |
| `oǝ > ō` | literal | — |

### [vowels in hiatus reduced](https://eldamo.org/content/words/word-1124989585.html)

- порядок 04100
- общая формула `V̄̆V̄̆ > V̆V̆`

| подформула | вид | примеры |
|---|---|---|
| `ī̆ō̆ > io` | literal | 1 / 0 |
| `ē̆ē̆ > ē` | literal | — |
| `ē̆ā̆ > ea` | literal | — |
| `ē̆ō̆ > eo` | literal | — |
| `ā̆ā̆ > ā` | literal | — |
| `ō̆ā̆ > oa` | literal | — |
| `ō̆ō̆ > ō` | literal | — |
| `ū̆ī̆ > ui` | literal | 1 / 0 |

### [diphthongs usually reduced before consonant clusters](https://eldamo.org/content/words/word-3634388709.html)

- порядок 04200
- общая формула `{ei|ai|oi|ui|au|eu|ou|iu}CC > {i|e|e|wi|o|o|u|ju}CC`

| подформула | вид | примеры |
|---|---|---|
| `aiCC > aCC` | contextual | 1 / 1 |

### [[w] became [v] after [u] and [o] and before [o]](https://eldamo.org/content/words/word-1557215875.html)

- порядок 04300
- общая формула `{uo}w|wo > v{uo}|ov`
- раньше, чем: initial [gʷ] became [w]
- позже, чем: intervocalic [ū], [ī] became [uw], [ij]

| подформула | вид | примеры |
|---|---|---|
| `uw > uv` | literal | 1 / 1 |
| `ow > ov` | literal | — |
| `wo > vo` | literal | — |

### [[dʲ] became [j]](https://eldamo.org/content/words/word-1926351487.html)

- позже, чем: palatals became dentals before [i]; voiced spirants becames stops after liquids, nasals and [z]
- вариант правила [[d] vanished between [n], [r], [l] and [j]](https://eldamo.org/content/words/word-2488350997.html)

| подформула | вид | примеры |
|---|---|---|
| `dʲ > j` | literal | 14 / 14 |

### [[ei], [ou] became [ai], [au]](https://eldamo.org/content/words/word-1865495919.html)

- общая формула `ei|ou > ai|au`
- позже, чем: [ðʲ] became [j]; [ou] became [u] before [e] and [o], but [o] before [i] and [a]; [ji], [wu] became [i], [u] after a vowel; intervocalic [ū], [ī] became [uw], [ij]
- вариант правила [[ei], [ou] generally became [ī], [ū]](https://eldamo.org/content/words/word-1123007057.html)

| подформула | вид | примеры |
|---|---|---|
| `ei > ai` | literal | 3 / 3 |
| `ou > au` | literal | 8 / 8 |
| `ēi > ei` | literal | 1 / 1 |

### [[f] became [v] except before stressed vowel](https://eldamo.org/content/words/word-3263617489.html)

- позже, чем: geminate voiceless spirants reduced; geminate voiceless spirants reduced

| подформула | вид | примеры |
|---|---|---|
| `VfV\|VfV́ > VvV\|VfV́` | contextual | — |

### [[kt] became [xt]](https://eldamo.org/content/words/word-2805959101.html)

- вариант правила [[pt], [kt] became [ps], [xt]](https://eldamo.org/content/words/word-2701010297.html)

| подформула | вид | примеры |
|---|---|---|
| `kt > xt` | literal | 4 / 4 |

### [[kw] became [kʷ]](https://eldamo.org/content/words/word-3664845381.html)

| подформула | вид | примеры |
|---|---|---|
| `kw > kʷ` | literal | 10 / 10 |

### [[kʷkʷ] became [kʷ]](https://eldamo.org/content/words/word-2229352317.html)

- позже, чем: voiceless stop assimilated to following voiceless stop except [t]

| подформула | вид | примеры |
|---|---|---|
| `kʷkʷ > kʷ` | literal | 3 / 3 |

### [[mn] became [nm]](https://eldamo.org/content/words/word-1979851293.html)

| подформула | вид | примеры |
|---|---|---|
| `nm > mn` | literal | 1 / 1 |

### [[mw] became [nw]](https://eldamo.org/content/words/word-3713651241.html)

- вариант правила [[mw] became [mm]](https://eldamo.org/content/words/word-1010737209.html)

| подформула | вид | примеры |
|---|---|---|
| `mw > nw` | literal | 3 / 3 |

### [[ndj] became [nj] in Inwelin](https://eldamo.org/content/words/word-3086270501.html)

| подформула | вид | примеры |
|---|---|---|
| `ndʲ > nʲ` | literal | — |

### [[pj], [kj] became [tj]](https://eldamo.org/content/words/word-858042645.html)

- общая формула `{pk}j > tj`
- вариант правила [velars were dentalized before [j]](https://eldamo.org/content/words/word-3291729015.html)

| подформула | вид | примеры |
|---|---|---|
| `pj > tj` | literal | 1 / 1 |
| `kj > tj` | literal | 9 / 9 |

### [[pp] became [pt]](https://eldamo.org/content/words/word-1728242171.html)

- позже, чем: [x] assimilated to preceding stop; voiceless stop assimilated to following voiceless stop except [t]

| подформула | вид | примеры |
|---|---|---|
| `pp > pt` | literal | — |

### [[pw] became [tw]](https://eldamo.org/content/words/word-3476641749.html)

| подформула | вид | примеры |
|---|---|---|
| `pw > tw` | literal | 1 / 1 |

### [[r] dissimilated to [l]](https://eldamo.org/content/words/word-2661447495.html)

- общая формула `rVr|rCVr > lVr|rCVl`

| подформула | вид | примеры |
|---|---|---|
| `rVr > lVr` | contextual | 3 / 2 |
| `rCVr > rCVl` | contextual | 1 / 1 |

### [[rg] became [rk]](https://eldamo.org/content/words/word-3720428755.html)

- вариант правила [[lg], [rg] became [ll], [rr]](https://eldamo.org/content/words/word-1946719133.html)

| подформула | вид | примеры |
|---|---|---|
| `rg > rk` | literal | 1 / 1 |

### [[rl] became [ll]](https://eldamo.org/content/words/word-3780248481.html)

- позже, чем: [z] became [r]
- вариант правила [[z] and [ð] assimilated to following [r], [l]](https://eldamo.org/content/words/word-98897835.html)

| подформула | вид | примеры |
|---|---|---|
| `rl > ll` | literal | 1 / 1 |

### [[s] became [z] before nasals and voiced spirants](https://eldamo.org/content/words/word-1821618891.html)

- общая формула `s{lrmnβðʲðɣɣʷ} > z{lrmnβðʲðɣɣʷ}`
- раньше, чем: [z] became [r]; voiced spirants becames stops after liquids, nasals and [z]
- позже, чем: [θ] became [s]
- вариант правила [medial [s] often became [z]](https://eldamo.org/content/words/word-2951986869.html)

| подформула | вид | примеры |
|---|---|---|
| `sl > zl` | literal | 1 / 1 |
| `sm > zm` | literal | 2 / 2 |
| `sr > zr` | literal | 1 / 1 |

### [[sf] became [ff]](https://eldamo.org/content/words/word-3935033455.html)

- раньше, чем: geminate voiceless spirants reduced
- вариант правила [[sf] became [f]](https://eldamo.org/content/words/word-1165599019.html)

| подформула | вид | примеры |
|---|---|---|
| `sf > ff` | literal | — |

### [[sp] became [ps], [sk] sometimes [ks]](https://eldamo.org/content/words/word-3881401387.html)

- общая формула `sp|sk > ps|ks`
- вариант правила [[sp], [sk] became [ps], [ks]](https://eldamo.org/content/words/word-3499874945.html)

| подформула | вид | примеры |
|---|---|---|
| `sp > ps` | literal | — |
| `sk > ks` | literal | 3 / 3 |

### [[sx] became [ss]](https://eldamo.org/content/words/word-3702117245.html)

| подформула | вид | примеры |
|---|---|---|
| `sx > ss` | literal | — |

### [[sxʷ] became [sw]](https://eldamo.org/content/words/word-1439505743.html)

| подформула | вид | примеры |
|---|---|---|
| `sxʷ > sw` | literal | — |

### [[ti] became [tsi]](https://eldamo.org/content/words/word-1784632669.html)

- раньше, чем: [ts] became [s] after diphthong; palatals became dentals before [i]

| подформула | вид | примеры |
|---|---|---|
| `ti > tsi` | literal | 16 / 16 |

### [[ts] became [s] after diphthong](https://eldamo.org/content/words/word-1142199593.html)

- позже, чем: [ti] became [tsi]

| подформула | вид | примеры |
|---|---|---|
| `VVts > VVs` | contextual | 4 / 3 |

### [[tʲ], [kʷ] became [t], [k] before [t], [s]](https://eldamo.org/content/words/word-2101627003.html)

- общая формула `{tʲkʷ}{ts} > {tk}`
- позже, чем: [θ] became [s]; voiceless spirants became stops before stops, [s] or [z]

| подформула | вид | примеры |
|---|---|---|
| `tʲt > tt` | literal | — |
| `tʲs > ts` | literal | — |
| `kʷt > kt` | literal | 1 / 1 |
| `kʷs > ks` | literal | — |

### [[w] became [v] in Cortirion](https://eldamo.org/content/words/word-2529974525.html)

- общая формула `VwV|w- > VvV|v-`

| подформула | вид | примеры |
|---|---|---|
| `VwV > VvV` | contextual | 2 / 2 |
| `w- > v-` | literal | 2 / 2 |

### [[x] assimilated to preceding stop](https://eldamo.org/content/words/word-574672121.html)

- общая формула `px|tx|tʲx|kx|kʷx > pp|tt|tt|kk|kk`
- раньше, чем: [pp] became [pt]

| подформула | вид | примеры |
|---|---|---|
| `px > pp` | literal | — |
| `tx > tt` | literal | — |
| `tʲx > tt` | literal | — |
| `kx > kk` | literal | — |
| `kʷx > kk` | literal | — |

### [[xs] became [xx]](https://eldamo.org/content/words/word-3235607655.html)

- раньше, чем: [θ] became [s]; geminate voiceless spirants reduced

| подформула | вид | примеры |
|---|---|---|
| `xs > xx` | literal | — |

### [[xʷ] became [kʷ] after voiceless stops](https://eldamo.org/content/words/word-1950246799.html)

| подформула | вид | примеры |
|---|---|---|
| `{tʲptk}xʷ > {tʲptk}kʷ` | contextual | — |

### [[xʷ] became [x] before consonants](https://eldamo.org/content/words/word-4193614505.html)

- общая формула `xʷC|xʷ{βðɣɣʷjw} > xC|w{βðɣɣʷjw}`
- позже, чем: voiceless spirants voiced before voiced continuants

| подформула | вид | примеры |
|---|---|---|
| `xʷC > xC` | contextual | — |

### [[z] became [r]](https://eldamo.org/content/words/word-1584268155.html)

- раньше, чем: [rl] became [ll]
- позже, чем: [z] vanished between a vowel and [m] after a preceding [z], [r]; [ð] became [z]; [s] became [z] before nasals and voiced spirants; nasals assimilated to preceding [z]
- вариант правила [[z] became [r]](https://eldamo.org/content/words/word-14189179.html)

| подформула | вид | примеры |
|---|---|---|
| `z > r` | literal | 66 / 66 |

### [[z] vanished between a vowel and [m] after a preceding [z], [r]](https://eldamo.org/content/words/word-1025055523.html)

- раньше, чем: [z] became [r]

| подформула | вид | примеры |
|---|---|---|
| `zVzm > zVm` | contextual | 1 / 1 |

### [[ð] became [z]](https://eldamo.org/content/words/word-1053361623.html)

- раньше, чем: [z] became [r]
- позже, чем: [ð] became [θ] before voiceless stops and [s]; final voiceless spirants were weakened and voiced; voiced stops became spirants after vowels
- вариант правила [intervocalic [ð] became [r]](https://eldamo.org/content/words/word-3914129125.html)

| подформула | вид | примеры |
|---|---|---|
| `ð > z` | literal | 63 / 61 |

### [[ð] became [θ] before voiceless stops and [s]](https://eldamo.org/content/words/word-3589750713.html)

- общая формула `ð{ptks} > θ{ptks}`
- раньше, чем: [ð] became [z]
- позже, чем: voiced stops became spirants after vowels

| подформула | вид | примеры |
|---|---|---|
| `ðt > θt` | literal | 16 / 15 |
| `ðs > θs` | literal | 4 / 4 |

### [[ðʲ] became [j]](https://eldamo.org/content/words/word-2901784817.html)

- раньше, чем: later [j], [w] became [i], [u] finally or between a vowel and a consonant; [ei], [ou] became [ai], [au]
- позже, чем: [ðʲi] became [ī] and [ɣʷu] became [ū]; [ji], [wu] became [i], [u] after a vowel; voiceless spirants voiced before voiced continuants

| подформула | вид | примеры |
|---|---|---|
| `ðʲ > j` | literal | 71 / 70 |

### [[ðʲi] became [ī] and [ɣʷu] became [ū]](https://eldamo.org/content/words/word-2107569835.html)

- общая формула `ðʲi|ɣʷu > ī|ū`
- раньше, чем: [ðʲ] became [j]; [ɣʷ] became [w]

| подформула | вид | примеры |
|---|---|---|
| `ðʲi > ī` | literal | 1 / 1 |
| `ɣʷu > ū` | literal | — |

### [[ðθ] became [θθ]](https://eldamo.org/content/words/word-593991133.html)

- раньше, чем: [θ] became [ð] after voiced spirants and stops

| подформула | вид | примеры |
|---|---|---|
| `ðθ > θθ` | literal | — |

### [[ɣʷ] became [w]](https://eldamo.org/content/words/word-1501380803.html)

- раньше, чем: later [j], [w] became [i], [u] finally or between a vowel and a consonant; [ou] became [au]
- позже, чем: [ðʲi] became [ī] and [ɣʷu] became [ū]; voiceless spirants voiced after liquids; voiceless spirants voiced before voiced continuants

| подформула | вид | примеры |
|---|---|---|
| `ɣʷ > w` | literal | 17 / 17 |

### [[ɸx] became [f]](https://eldamo.org/content/words/word-4047708457.html)

- раньше, чем: voiceless spirant combinations assimilated except to [θ]

| подформула | вид | примеры |
|---|---|---|
| `ɸx > f` | literal | — |

### [[β] became [u] before consonants and finally](https://eldamo.org/content/words/word-2080125305.html)

- общая формула `-β|VβC > -u|VuC`
- вариант правила [[β], [ɣ] vocalized before voiced consonants](https://eldamo.org/content/words/word-641476107.html)

| подформула | вид | примеры |
|---|---|---|
| `-β > -u` | literal | 3 / 3 |
| `VβC > VuC` | contextual | 22 / 20 |

### [[β] became [v]](https://eldamo.org/content/words/word-1245311459.html)

- вариант правила [[ɸ], [β] became [f], [v]](https://eldamo.org/content/words/word-2661449019.html)

| подформула | вид | примеры |
|---|---|---|
| `β > v` | literal | 109 / 107 |

### [[β] vanished before [u]](https://eldamo.org/content/words/word-3496955393.html)

- позже, чем: [ɸ] usually became [f]

| подформула | вид | примеры |
|---|---|---|
| `βu > øu` | contextual | — |

### [[θ] became [ð] after voiced spirants and stops](https://eldamo.org/content/words/word-3536671329.html)

- раньше, чем: [θ] became [s]
- позже, чем: [ðθ] became [θθ]

| подформула | вид | примеры |
|---|---|---|
| `{βɣɣʷbdg}θ > {βɣɣʷbdg}ð` | contextual | — |

### [final [t] became [s]](https://eldamo.org/content/words/word-3850922299.html)

- вариант правила [final [t] became [s]](https://eldamo.org/content/words/word-539818035.html)

| подформула | вид | примеры |
|---|---|---|
| `-t > -s` | literal | — |

### [final [ɸ] became [xʷ]](https://eldamo.org/content/words/word-2038949399.html)

- раньше, чем: final voiceless spirants were weakened and voiced

| подформула | вид | примеры |
|---|---|---|
| `-ɸ > -xʷ` | literal | — |

### [final consonants often became dentals](https://eldamo.org/content/words/word-884464849.html)

- общая формула `-{km}|-ŋg > -{tn}|-n`
- вариант правила [final consonants became dentals](https://eldamo.org/content/words/word-2371293137.html)

| подформула | вид | примеры |
|---|---|---|
| `-kʷ > -k` | literal | 5 / 5 |
| `-k > -t` | literal | 1 / 1 |
| `-p > -t` | literal | 1 / 1 |
| `-m > -n` | literal | 7 / 6 |
| `-mb > -n` | literal | 6 / 6 |
| `-ŋg > -n` | literal | 2 / 2 |

### [final nasal + [ḷ] became [ndḷ]](https://eldamo.org/content/words/word-3633742017.html)

- общая формула `-{mnŋ}ḷ > -ndl`

| подформула | вид | примеры |
|---|---|---|
| `-mḷ > -ndl` | literal | 2 / 0 |
| `-nḷ > -ndl` | literal | 1 / 0 |
| `-ŋḷ > -ndl` | literal | 1 / 0 |

### [final voiceless spirants were weakened and voiced](https://eldamo.org/content/words/word-1161720749.html)

- общая формула `-xw|-θj|-{xθs} > -w|-j|-{ɣðz}`
- раньше, чем: later [j], [w] became [i], [u] finally or between a vowel and a consonant; final [ɣ] vanished with compensatory lengthening; [ð] became [z]
- позже, чем: final [ɸ] became [xʷ]

| подформула | вид | примеры |
|---|---|---|
| `-xw > -w` | literal | — |
| `-x > -ɣ` | literal | 12 / 12 |
| `-θ > -ð` | literal | — |
| `-θj > -j` | literal | — |
| `-s > -z` | literal | 1 / 1 |

### [geminate voiceless spirants reduced](https://eldamo.org/content/words/word-3931943725.html)

- общая формула `ff|xʷxʷ|xx|θʲθʲ > f|f|h|θʲ`
- раньше, чем: [f] became [v] except before stressed vowel; [f] became [v] except before stressed vowel
- позже, чем: [sf] became [ff]; [xs] became [xx]; [ɸ] usually became [f]; voiceless spirant combinations assimilated except to [θ]

| подформула | вид | примеры |
|---|---|---|
| `ff > f` | literal | — |
| `xʷxʷ > f` | literal | — |
| `xx > h` | literal | 4 / 4 |
| `θʲθʲ > θʲ` | literal | — |

### [initial [gʷ] became [w]](https://eldamo.org/content/words/word-1196923337.html)

- общая формула `gʷ- > w-`
- раньше, чем: initial voiced stops were unvoiced
- позже, чем: [w] became [v] after [u] and [o] and before [o]

| подформула | вид | примеры |
|---|---|---|
| `gʷ- > w-` | literal | 39 / 39 |

### [initial [s] plus voiceless stops became voiceless spirants](https://eldamo.org/content/words/word-95585617.html)

- общая формула `s{pɸ}-|s{tθ}-|s{kx}- > ɸ-|θ-|x-`
- вариант правила [initial [s] plus voiceless stops became voiceless spirants](https://eldamo.org/content/words/word-3333849997.html)

| подформула | вид | примеры |
|---|---|---|
| `sp- > ɸ-` | literal | — |
| `st- > θ-` | literal | 2 / 2 |
| `sk- > x-` | literal | 4 / 4 |

### [initial [s] vanished before liquids and nasals](https://eldamo.org/content/words/word-1793089541.html)

- общая формула `s{lrmnŋ}- > {lrmnŋ}-`
- вариант правила [initial [s] unvoiced following continuant](https://eldamo.org/content/words/word-476591497.html)

| подформула | вид | примеры |
|---|---|---|
| `sl- > l-` | literal | 1 / 1 |
| `sr- > r-` | literal | — |
| `sm- > m-` | literal | 1 / 1 |
| `sn- > n-` | literal | — |
| `sŋ- > ŋ-` | literal | — |

### [initial [sw] and [sβ] became [f], [sj] became [j̊]](https://eldamo.org/content/words/word-3922871059.html)

- общая формула `s{wβ}-|sj- > f-|j̊-`
- позже, чем: [θ] became [s]; initial [θʲ] became [sj]
- вариант правила [initial [s] unvoiced following continuant](https://eldamo.org/content/words/word-476591497.html)

| подформула | вид | примеры |
|---|---|---|
| `sw- > f-` | literal | 3 / 3 |
| `sβ- > f-` | literal | — |
| `sj- > j̊-` | literal | 7 / 7 |

### [initial [x-] became [h-]](https://eldamo.org/content/words/word-777007581.html)

| подформула | вид | примеры |
|---|---|---|
| `x- > h-` | literal | 54 / 54 |

### [initial [ð] became [d]](https://eldamo.org/content/words/word-3626017139.html)

- вариант правила [initial [ð] became [s]](https://eldamo.org/content/words/word-1417666947.html)

| подформула | вид | примеры |
|---|---|---|
| `ð- > d-` | literal | — |

### [initial [ð] became [s]](https://eldamo.org/content/words/word-1417666947.html)

| подформула | вид | примеры |
|---|---|---|
| `ð- > s-` | literal | 5 / 5 |

### [initial [ŋ] became [n]](https://eldamo.org/content/words/word-331431039.html)

- вариант правила [initial [ŋ] became [n]](https://eldamo.org/content/words/word-1117953113.html)

| подформула | вид | примеры |
|---|---|---|
| `ŋ- > n-` | literal | 9 / 9 |

### [initial [ŋʷ] became [m]](https://eldamo.org/content/words/word-2133998255.html)

- позже, чем: initial nasalized stops became nasals

| подформула | вид | примеры |
|---|---|---|
| `ŋʷ- > m-` | literal | 6 / 6 |

### [initial nasalized stops became nasals](https://eldamo.org/content/words/word-4287379737.html)

- общая формула `{mb|nd|ndʲ|ŋg|ŋgʷ}- > {mnnʲŋŋʷ}-`
- раньше, чем: initial [ŋʷ] became [m]
- вариант правила [initial nasals plus stops reduced to nasals](https://eldamo.org/content/words/word-2830500177.html)

| подформула | вид | примеры |
|---|---|---|
| `mb- > m-` | literal | 13 / 12 |
| `nd- > n-` | literal | 7 / 7 |
| `ndʲ- > nʲ-` | literal | — |
| `ŋg- > ŋ-` | literal | — |
| `ŋgʷ- > ŋʷ-` | literal | 2 / 2 |

### [initial voiced stops were unvoiced](https://eldamo.org/content/words/word-630957615.html)

- общая формула `{bdggʷ}- > {ptkkʷ}-`
- позже, чем: initial [gʷ] became [w]; palatals became dentals before [i]
- вариант правила [voiced stops became spirants except after nasals and liquids](https://eldamo.org/content/words/word-2772726195.html)

| подформула | вид | примеры |
|---|---|---|
| `b- > p-` | literal | 17 / 17 |
| `d- > t-` | literal | 10 / 10 |
| `g- > k-` | literal | 20 / 20 |
| `gʷ- > kʷ-` | literal | 2 / 1 |

### [intervocalic [ŋ], [ŋʷ] became [ŋg], [ŋgʷ]](https://eldamo.org/content/words/word-4001161343.html)

- общая формула `V{ŋ|ŋʷ}V > V{ŋg|ŋgʷ}V`
- вариант правила [medial [ŋ] usually became [ɣ]](https://eldamo.org/content/words/word-3915121695.html)

| подформула | вид | примеры |
|---|---|---|
| `VŋV > VŋgV` | contextual | 15 / 15 |
| `VŋʷV > VŋgʷV` | contextual | — |

### [later [j], [w] became [i], [u] finally or between a vowel and a consonant](https://eldamo.org/content/words/word-451471319.html)

- общая формула `VjC|VwC|-j|-w > ViC|VuC|-i|-u`
- позже, чем: [ðʲ] became [j]; [ɣʷ] became [w]; final voiceless spirants were weakened and voiced
- вариант правила [later [j], [w] became [i], [u] before consonants](https://eldamo.org/content/words/word-1025863587.html)

| подформула | вид | примеры |
|---|---|---|
| `VjC > ViC` | contextual | 50 / 50 |
| `VwC > VuC` | contextual | 12 / 9 |
| `-j > -i` | literal | 6 / 6 |
| `-w > -u` | literal | 1 / 1 |

### [long vowels shortened before consonant clusters](https://eldamo.org/content/words/word-3237906463.html)

- вариант правила [long vowels shortened before consonant clusters](https://eldamo.org/content/words/word-1524904053.html)

| подформула | вид | примеры |
|---|---|---|
| `V̄CC > V̆CC` | contextual | 8 / 8 |

### [medial [sj] became [j̊]](https://eldamo.org/content/words/word-1971369121.html)

- вариант правила [initial [s] unvoiced following continuant](https://eldamo.org/content/words/word-476591497.html)

| подформула | вид | примеры |
|---|---|---|
| `sj > j̊` | literal | 1 / 1 |

### [medial nasal plus [w] became [ŋgw]](https://eldamo.org/content/words/word-2457955191.html)

- общая формула `{nʲmnŋ}w > ŋgw`
- вариант правила [[nm], [ŋm] became [nw], [ŋgw]](https://eldamo.org/content/words/word-2886094609.html)

| подформула | вид | примеры |
|---|---|---|
| `ŋw > ŋgw` | literal | 5 / 5 |

### [middle consonant lost in three-consonant cluster](https://eldamo.org/content/words/word-2705037297.html)

- общая формула `CCC > CC`
- позже, чем: between vowels and consonants [ɣ] vanished with compensatory lengthening

| подформула | вид | примеры |
|---|---|---|
| `kts > ks` | literal | 2 / 2 |
| `kws > ks` | literal | 1 / 0 |
| `kwt > kt` | literal | 1 / 0 |
| `ldl > ll` | literal | 1 / 0 |
| `lts > ls` | literal | 2 / 2 |
| `ndw > nw` | literal | 1 / 1 |
| `nts > ns` | literal | 2 / 2 |
| `ŋkwk > ŋk` | literal | 1 / 0 |
| `ŋgj > ŋj` | literal | 1 / 1 |
| `pts > ps` | literal | 1 / 1 |
| `rdk > rk` | literal | 1 / 1 |
| `rdm > rm` | literal | 1 / 1 |
| `rdn > rn` | literal | 1 / 1 |
| `rgw > rw` | literal | 1 / 1 |
| `rdw > rw` | literal | 2 / 2 |
| `sst > st` | literal | 1 / 1 |

### [nasals assimilated to preceding [z]](https://eldamo.org/content/words/word-2012556159.html)

- общая формула `z{ŋʷ|ŋ|nʲ} > z{nu|n|ni}`
- раньше, чем: [z] became [r]

| подформула | вид | примеры |
|---|---|---|
| `zŋʷ > znu` | literal | — |
| `zŋ > zn` | literal | — |
| `znʲ > zni` | literal | — |

### [nasals became [n] before [j]](https://eldamo.org/content/words/word-2394802469.html)

- общая формула `{mŋnʲ}j > nj`

| подформула | вид | примеры |
|---|---|---|
| `mj > nj` | literal | 1 / 1 |
| `ŋj > nj` | literal | 1 / 1 |
| `nʲj > nj` | literal | — |

### [palatals became dentals before [i]](https://eldamo.org/content/words/word-3480191301.html)

- общая формула `{tdnθ}ʲi > {tdnθ}i`
- раньше, чем: [dʲ] became [j]; initial voiced stops were unvoiced
- позже, чем: [ti] became [tsi]; [θʲi] became [xi]

| подформула | вид | примеры |
|---|---|---|
| `tʲi > ti` | literal | 10 / 10 |
| `dʲi > di` | literal | 3 / 3 |
| `nʲi > ni` | literal | 3 / 3 |

### [second short vowel of same quality lost](https://eldamo.org/content/words/word-2030742295.html)

- общая формула `V₁CV̆₁CV > V₁CCV`
- вариант правила [second short vowel of same quality lost](https://eldamo.org/content/words/word-511172017.html)

| подформула | вид | примеры |
|---|---|---|
| `aCaCV > aCCV` | contextual | 1 / 1 |
| `eCeCV > eCCV` | contextual | 5 / 5 |
| `iCiCV > iCCV` | contextual | 3 / 3 |
| `oCoCV > oCCV` | contextual | 2 / 2 |
| `uCuCV > uCCV` | contextual | 4 / 4 |

### [stops frequently underwent metathesis with nasals and liquids](https://eldamo.org/content/words/word-231729157.html)

- общая формула `{ptk}{rl} > {rl}{ptk}`
- вариант правила [stops frequently underwent metathesis with nasals and liquids](https://eldamo.org/content/words/word-716992289.html)

| подформула | вид | примеры |
|---|---|---|
| `tr > rt` | literal | 2 / 2 |
| `kl > lk` | literal | 1 / 1 |

### [stops unvoiced before liquids](https://eldamo.org/content/words/word-475956217.html)

| подформула | вид | примеры |
|---|---|---|
| `dr > tr` | literal | 1 / 1 |

### [unstressed long vowels usually shortened](https://eldamo.org/content/words/word-1954971469.html)

| подформула | вид | примеры |
|---|---|---|
| `ˌV̄ > V̆` | contextual | — |

### [voiced spirants becames stops after liquids, nasals and [z]](https://eldamo.org/content/words/word-1497556499.html)

- общая формула `{lrmnŋz}{βððʲɣɣʷ} > {lrmnŋz}{bddʲggʷ}`
- раньше, чем: [dʲ] became [j]
- позже, чем: [s] became [z] before nasals and voiced spirants; voiceless spirants voiced after liquids
- вариант правила [spirants became stops after [r], [l]](https://eldamo.org/content/words/word-556722173.html)

| подформула | вид | примеры |
|---|---|---|
| `lβ > lb` | literal | — |
| `rβ > rb` | literal | — |
| `mβ > mb` | literal | 11 / 11 |
| `zβ > zb` | literal | — |
| `lð > ld` | literal | 14 / 14 |
| `rð > rd` | literal | 24 / 23 |
| `nð > nd` | literal | 45 / 45 |
| `zð > zd` | literal | 1 / 1 |
| `lɣ > lg` | literal | 1 / 1 |
| `rɣ > rg` | literal | 1 / 1 |
| `ŋɣ > ŋg` | literal | 1 / 1 |
| `zɣ > zg` | literal | — |
| `lβ > lw` | literal | 2 / 2 |
| `ŋɣʷ > ŋgʷ` | literal | 1 / 1 |

### [voiced stops became spirants after vowels](https://eldamo.org/content/words/word-3179825887.html)

- общая формула `V{bddʲggʷ} > V{βððʲɣɣʷ}`
- раньше, чем: [ð] became [θ] before voiceless stops and [s]; [ð] became [z]; [ɣ] otherwise vanished
- вариант правила [voiced stops became spirants except after nasals and liquids](https://eldamo.org/content/words/word-2772726195.html)

| подформула | вид | примеры |
|---|---|---|
| `Vb > Vβ` | contextual | — |
| `Vd > Vð` | contextual | 2 / 2 |
| `Vdʲ > Vðʲ` | contextual | — |
| `Vg > Vɣ` | contextual | 5 / 4 |
| `Vgʷ > Vɣʷ` | contextual | — |

### [voiceless and voiced [w] became [f], [v] in Inwelin](https://eldamo.org/content/words/word-3562966925.html)

- общая формула `w̥|w > f|v`

| подформула | вид | примеры |
|---|---|---|
| `w̥ > f` | literal | — |
| `w > v` | literal | — |

### [voiceless spirant combinations assimilated except to [θ]](https://eldamo.org/content/words/word-169515023.html)

- общая формула `{ɸθθʲxxʷ}₁{ɸθʲxxʷ}₂ > {ɸθʲxxʷ}₂{ɸθʲxxʷ}₂`
- раньше, чем: [θ] became [s]; geminate voiceless spirants reduced
- позже, чем: [ɸx] became [f]

| подформула | вид | примеры |
|---|---|---|
| `xʷx > xx` | literal | — |
| `θʲx > xx` | literal | — |
| `θx > xx` | literal | 1 / 1 |
| `ɸxʷ > xʷxʷ` | literal | — |
| `θʲxʷ > xʷxʷ` | literal | — |
| `xʷxʷ > xʷxʷ` | identity | — |
| `θxʷ > xʷxʷ` | literal | — |
| `{ɸθθʲxxʷ}θʲ > θʲθʲ` | contextual | — |
| `xʷɸ > ɸɸ` | literal | — |
| `θʲɸ > ɸɸ` | literal | — |
| `xɸ > ɸɸ` | literal | — |
| `θɸ > ɸɸ` | literal | — |

### [voiceless spirants became stops after nasals](https://eldamo.org/content/words/word-3654836095.html)

- общая формула `mɸ|nθ|nθʲ|ŋx|ŋxʷ > mp|nt|ntʲ|ŋk|ŋkʷ`
- раньше, чем: [θ] became [s]; [θʲi] became [xi]
- позже, чем: [xʷu] became [xu]
- вариант правила [spirants became stops after nasals](https://eldamo.org/content/words/word-699730083.html)

| подформула | вид | примеры |
|---|---|---|
| `mɸ > mp` | literal | 4 / 4 |
| `nθ > nt` | literal | 2 / 2 |
| `nθʲ > ntʲ` | literal | — |
| `ŋx > ŋk` | literal | 1 / 1 |
| `ŋxʷ > ŋkʷ` | literal | — |

### [voiceless spirants became stops before stops, [s] or [z]](https://eldamo.org/content/words/word-3362555183.html)

- общая формула `{ɸxxʷθʲ}{ptkbdgsz} > {pkkk}{ptkbdgsz}`
- раньше, чем: [ɸ] usually became [f]; [tʲ], [kʷ] became [t], [k] before [t], [s]
- позже, чем: [θ] became [s]

| подформула | вид | примеры |
|---|---|---|
| `xs > ks` | literal | 3 / 3 |
| `xt > kt` | literal | 9 / 8 |
| `xk > kk` | literal | 1 / 1 |
| `xkʷ > kkʷ` | literal | 1 / 1 |
| `ɸs > ps` | literal | 2 / 2 |
| `ɸt > pt` | literal | 3 / 3 |
| `xs > h` | literal | 2 / 2 |

### [voiceless spirants voiced after liquids](https://eldamo.org/content/words/word-1412754393.html)

- общая формула `{lr}{ɸθθʲxxʷ} > {lr}{βððʲɣɣʷ}`
- раньше, чем: voiced spirants becames stops after liquids, nasals and [z]; [θ] became [s]; [ɣʷ] became [w]
- позже, чем: [xʷu] became [xu]

| подформула | вид | примеры |
|---|---|---|
| `lɸ > lβ` | literal | 2 / 2 |
| `rɸ > rβ` | literal | — |
| `lθ > lð` | literal | 1 / 1 |
| `rθ > rð` | literal | 9 / 9 |
| `lx > lɣ` | literal | 1 / 1 |
| `rx > rɣ` | literal | 1 / 1 |
| `lθʲ > lðʲ` | literal | — |
| `rθʲ > rðʲ` | literal | — |
| `lxʷ > lɣʷ` | literal | — |
| `rxʷ > rɣʷ` | literal | — |

### [voiceless spirants voiced before voiced continuants](https://eldamo.org/content/words/word-579131439.html)

- общая формула `{ɸxxʷθʲ}{βɣmnŋrljw} > {βɣxʷðʲ}{βɣmnŋrljw}`
- раньше, чем: [xʷ] became [x] before consonants; between vowels and consonants [ɣ] vanished with compensatory lengthening; [ɣʷ] became [w]; [ðʲ] became [j]

| подформула | вид | примеры |
|---|---|---|
| `ɸ{βmnŋrljw} > β{βmnŋrljw}` | contextual | — |
| `xʷ{βmnŋrljw} > ɣʷ{βmnŋrljw}` | contextual | — |
| `θʲ{βðɣɣʷjw} > ðʲ{βðɣɣʷjw}` | contextual | 3 / 2 |
| `xj > ɣj` | literal | 1 / 1 |
| `xl > ɣl` | literal | 3 / 3 |
| `xm > ɣm` | literal | 7 / 7 |
| `xn > ɣn` | literal | 4 / 4 |
| `xŋ > ɣŋ` | literal | 2 / 2 |
| `xr > ɣr` | literal | 5 / 5 |

### [voiceless stop assimilated to following voiceless stop except [t]](https://eldamo.org/content/words/word-3099273747.html)

- общая формула `{ttʲkkʷ}p|{ttʲkʷ}k|{ttʲk}kʷ > pp|kk|kʷkʷ`
- раньше, чем: [kʷkʷ] became [kʷ]; [pp] became [pt]

| подформула | вид | примеры |
|---|---|---|
| `kp > pp` | literal | — |
| `tp > pp` | literal | — |
| `tk > kk` | literal | — |
| `tʲk > kk` | literal | — |
| `kʷk > kk` | literal | 2 / 2 |
| `tkʷ > kʷkʷ` | literal | 2 / 2 |
| `tʲkʷ > kʷkʷ` | literal | — |
| `kkʷ > kʷkʷ` | literal | 1 / 1 |

## Цепочки с оценками A и B

### A — засвидетельствована в одной деривации

- рання. `ð → z → r` (ᴱQ., ᴱQ.) — 61 дерив.
- рання. `rθ → rð → rd` (ᴱQ., ᴱQ.) — 9 дерив.
- рання. `ðʲ → j → i` (ᴱQ., ᴱQ.) — 6 дерив.
- рання. `θʲ → sj → j̊` (ᴱQ., ᴱQ.) — 6 дерив.
- рання. `nð → nd → n` (ᴱQ., ᴱQ.) — 5 дерив.
- рання. `sk → x → h` (ᴱQ., ᴱQ.) — 4 дерив.
- рання. `rð → rd → r` (ᴱQ., ᴱQ.) — 3 дерив.
- рання. `lɸ → lβ → lw` (ᴱQ., ᴱQ.) — 2 дерив.
- рання. `st → θ → s` (ᴱQ., ᴱQ.) — 2 дерив.
- рання. `tkʷ → kʷkʷ → kʷ` (ᴱQ., ᴱQ.) — 2 дерив.
- рання. `ŋgʷ → ŋʷ → m` (ᴱQ., ᴱQ.) — 2 дерив.
- рання. `dr → tr → rt` (ᴱQ., ᴱQ.) — 1 дерив.
- рання. `gt → kt → xt` (ᴱ✶, ᴱQ.) — 1 дерив.
- рання. `kkʷ → kʷkʷ → kʷ` (ᴱQ., ᴱQ.) — 1 дерив.
- рання. `lx → lɣ → lg` (ᴱQ., ᴱQ.) — 1 дерив.
- рання. `lð → ld → l` (ᴱQ., ᴱQ.) — 1 дерив.
- рання. `lθ → lð → ld` (ᴱQ., ᴱQ.) — 1 дерив.
- рання. `rx → rɣ → rg` (ᴱQ., ᴱQ.) — 1 дерив.
- рання. `s → z → r` (ᴱQ., ᴱQ.) — 1 дерив.
- рання. `sk → ss → s` (ᴱQ., ᴱQ.) — 1 дерив.
- рання. `xkʷ → kkʷ → kʷkʷ` (ᴱQ., ᴱQ.) — 1 дерив.
- рання. `ŋgj → ŋj → nj` (ᴱQ., ᴱQ.) — 1 дерив.
- рання. `ɣʷ → w → u` (ᴱQ., ᴱQ.) — 1 дерив.
- рання. `θx → xx → h` (ᴱQ., ᴱQ.) — 1 дерив.
- рання. `rθ → rð → rd → r` (ᴱQ., ᴱQ., ᴱQ.) — 1 дерив.
- рання. `xkʷ → kkʷ → kʷkʷ → kʷ` (ᴱQ., ᴱQ., ᴱQ.) — 1 дерив.
- поздн. `g → ɣ → ø` (AQ., Q.) — 76 дерив.
- поздн. `b → β → v` (AQ., Q.) — 74 дерив.
- поздн. `pʰ → ɸ → f` (AQ., Q.) — 66 дерив.
- поздн. `tʰ → θ → s` (AQ., Q.) — 53 дерив.
- поздн. `kʰ → x → h` (AQ., Q.) — 39 дерив.
- поздн. `w → β → v` (Q., Q.) — 35 дерив.
- поздн. `ŋg → ŋ → n` (AQ., Q.) — 32 дерив.
- поздн. `d → ð → r` (AQ., Q.) — 14 дерив.
- поздн. `gt → kt → xt` (✶, Q.) — 6 дерив.
- поздн. `sp → ɸ → f` (AQ., Q.) — 5 дерив.
- поздн. `dm → nm → nw` (AQ., Q.) — 4 дерив.
- поздн. `sr → zr → rr` (AQ., AQ.) — 4 дерив.
- поздн. `st → θ → s` (AQ., Q.) — 4 дерив.
- поздн. `sk → x → h` (AQ., Q.) — 3 дерив.
- поздн. `gd → kt → xt` (AQ., Q.) — 2 дерив.
- поздн. `gm → ŋm → ŋgw` (AQ., Q.) — 2 дерив.
- поздн. `ktʰ → kt → xt` (AQ., Q.) — 2 дерив.
- поздн. `kʰt → ktʰ → kt` (✶, AQ.) — 2 дерив.
- поздн. `sn → n̥ → n` (AQ., Q.) — 2 дерив.
- поздн. `wa → wo → o` (✶, Q.) — 2 дерив.
- поздн. `zg → sk → ks` (AQ., Q.) — 2 дерив.
- поздн. `kʰt → ktʰ → kt → xt` (✶, AQ., Q.) — 2 дерив.
- поздн. `bd → pt → ɸt` (AQ., Q.) — 1 дерив.
- поздн. `bt → pt → ɸt` (✶, Q.) — 1 дерив.
- поздн. `kd → kt → xt` (✶, Q.) — 1 дерив.
- поздн. `km → mk → ŋk` (✶, ✶) — 1 дерив.
- поздн. `kn → kt → xt` (AQ., Q.) — 1 дерив.
- поздн. `kʰk → kkʰ → kk` (✶, AQ.) — 1 дерив.
- поздн. `mpʰ → ppʰ → pp` (AQ., AQ.) — 1 дерив.
- поздн. `ntʰ → ttʰ → tt` (AQ., AQ.) — 1 дерив.
- поздн. `pm → pw → pp` (AQ., Q.) — 1 дерив.
- поздн. `pt → ɸt → ut` (Q., Q.) — 1 дерив.
- поздн. `sl → l̥ → l` (AQ., Q.) — 1 дерив.
- поздн. `sl → zl → ll` (AQ., AQ.) — 1 дерив.
- поздн. `sm → zm → mm` (AQ., AQ.) — 1 дерив.
- поздн. `tkʰ → tk → θk` (AQ., Q.) — 1 дерив.
- поздн. `tʰk → tkʰ → tk` (✶, AQ.) — 1 дерив.
- поздн. `zb → sp → ps` (AQ., Q.) — 1 дерив.
- поздн. `θ → t → s` (Q., Q.) — 1 дерив.
- поздн. `tʰk → tkʰ → tk → θk` (✶, AQ., Q.) — 1 дерив.
- средн. `g → ɣ → ø` (ᴹAQ., ᴹQ.) — 63 дерив.
- средн. `b → β → v` (ᴹAQ., ᴹQ.) — 54 дерив.
- средн. `kʰ → x → h` (ᴹAQ., ᴹQ.) — 49 дерив.
- средн. `pʰ → ɸ → f` (ᴹAQ., ᴹQ.) — 38 дерив.
- средн. `tʰ → θ → s` (ᴹAQ., ᴹQ.) — 26 дерив.
- средн. `ŋg → ŋ → n` (ᴹAQ., ᴹQ.) — 19 дерив.
- средн. `gm → ŋm → ŋgw` (ᴹAQ., ᴹQ.) — 13 дерив.
- средн. `km → gm → ŋm` (ᴹAQ., ᴹAQ.) — 12 дерив.
- средн. `km → gm → ŋm → ŋgw` (ᴹAQ., ᴹAQ., ᴹQ.) — 12 дерив.
- средн. `sp → ɸ → f` (ᴹAQ., ᴹQ.) — 11 дерив.
- средн. `sk → x → h` (ᴹAQ., ᴹQ.) — 10 дерив.
- средн. `sl → l̥ → l` (ᴹAQ., ᴹQ.) — 10 дерив.
- средн. `st → θ → s` (ᴹAQ., ᴹQ.) — 7 дерив.
- средн. `d → ð → r` (ᴹAQ., ᴹQ.) — 6 дерив.
- средн. `kn → gn → ŋn` (ᴹAQ., ᴹAQ.) — 5 дерив.
- средн. `pn → bn → mn` (ᴹAQ., ᴹAQ.) — 4 дерив.
- средн. `zg → sk → ks` (ᴹAQ., ᴹQ.) — 4 дерив.
- средн. `dm → nm → nw` (ᴹAQ., ᴹQ.) — 3 дерив.
- средн. `sm → m̥ → m` (ᴹAQ., ᴹQ.) — 3 дерив.
- средн. `sn → n̥ → n` (ᴹAQ., ᴹQ.) — 3 дерив.
- средн. `tm → dm → nm` (ᴹAQ., ᴹAQ.) — 3 дерив.
- средн. `tn → dn → nn` (ᴹAQ., ᴹAQ.) — 3 дерив.
- средн. `tm → dm → nm → nw` (ᴹAQ., ᴹAQ., ᴹQ.) — 3 дерив.
- средн. `bd → pt → ps` (ᴹAQ., ᴹQ.) — 2 дерив.
- средн. `bt → pt → ps` (ᴹ✶, ᴹQ.) — 2 дерив.
- средн. `gd → kt → xt` (ᴹAQ., ᴹQ.) — 2 дерив.
- средн. `sr → zr → rr` (ᴹAQ., ᴹAQ.) — 2 дерив.
- средн. `tʰt → ttʰ → tt` (ᴹ✶, ᴹAQ.) — 2 дерив.
- средн. `ŋ → ɣ → h` (ᴹ✶, ᴹAQ.) — 2 дерив.
- средн. `gt → kt → xt` (ᴹ✶, ᴹQ.) — 1 дерив.
- средн. `kt → xt → t` (ᴹQ., ᴹQ.) — 1 дерив.
- средн. `kʰn → kt → xt` (ᴹAQ., ᴹQ.) — 1 дерив.
- средн. `mpʰ → ppʰ → pp` (ᴹAQ., ᴹAQ.) — 1 дерив.
- средн. `ntʰ → ttʰ → tt` (ᴹAQ., ᴹAQ.) — 1 дерив.
- средн. `pm → bm → mm` (ᴹAQ., ᴹAQ.) — 1 дерив.
- средн. `sg → zg → sk` (ᴹ✶, ᴹAQ.) — 1 дерив.
- средн. `sl → zl → ll` (ᴹAQ., ᴹAQ.) — 1 дерив.
- средн. `sn → zn → nn` (ᴹAQ., ᴹAQ.) — 1 дерив.
- средн. `tk → kt → xt` (ᴹ✶, ᴹQ.) — 1 дерив.
- средн. `tʰr → ts → ss` (ᴹAQ., ᴹQ.) — 1 дерив.
- средн. `zb → sp → ps` (ᴹAQ., ᴹQ.) — 1 дерив.
- средн. `ŋkʰ → kkʰ → kk` (ᴹAQ., ᴹAQ.) — 1 дерив.
- средн. `ɣs → hs → ss` (ᴹ✶, ᴹ✶) — 1 дерив.

### B — шаги засвидетельствованы, порядок подтверждён

- рання. `gt → kt → t` (ᴱ✶, ᴱQ.)
- рання. `gt → kt → tt` (ᴱ✶, ᴱQ.)
- рання. `md → nd → n` (ᴱ✶, ᴱQ.)
- рання. `nb → mb → m` (ᴱ✶, ᴱQ.)
- рання. `nb → mb → n` (ᴱ✶, ᴱQ.)
- поздн. `bm → mb → m` (✶, AQ.)
- поздн. `dn → nd → n` (✶, AQ.)
- поздн. `kr → ks → s` (AQ., Q.)
- поздн. `md → nd → n` (✶, AQ.)
- поздн. `nb → mb → m` (✶, AQ.)
- поздн. `sd → st → θ` (✶, AQ.)
- поздн. `sd → zd → st` (✶, AQ.)
- поздн. `sg → zg → sk` (✶, AQ.)
- поздн. `skʰ → sk → ks` (AQ., Q.)
- поздн. `tʰ → θ → t` (AQ., Q.)
- поздн. `zb → sp → ɸ` (AQ., AQ.)
- поздн. `zd → st → θ` (AQ., AQ.)
- поздн. `zg → sk → x` (AQ., AQ.)
- поздн. `ŋ → ɣ → ø` (✶, Q.)
- поздн. `ŋgj → ndj → nj` (AQ., Q.)
- поздн. `ŋw → w → v` (AQ., Q.)
- поздн. `ŋw → w → β` (AQ., Q.)
- поздн. `ŋŋ → ŋg → ŋ` (✶, AQ.)
- поздн. `bd → pt → ɸt → ut` (AQ., Q., Q.)
- поздн. `bt → pt → ɸt → ut` (✶, Q., Q.)
- поздн. `sd → st → θ → s` (✶, AQ., Q.)
- поздн. `sd → zd → st → θ` (✶, AQ., AQ.)
- поздн. `sg → zg → sk → ks` (✶, AQ., Q.)
- поздн. `sg → zg → sk → x` (✶, AQ., AQ.)
- поздн. `tʰ → θ → t → s` (AQ., Q., Q.)
- поздн. `zb → sp → ɸ → f` (AQ., AQ., Q.)
- поздн. `zd → st → θ → s` (AQ., AQ., Q.)
- поздн. `zg → sk → x → h` (AQ., AQ., Q.)
- поздн. `ŋw → w → β → v` (AQ., Q., Q.)
- поздн. `ŋŋ → ŋg → ŋ → n` (✶, AQ., Q.)
- средн. `bd → pt → xt` (ᴹAQ., ᴹQ.)
- средн. `bt → pt → xt` (ᴹ✶, ᴹQ.)
- средн. `dn → nd → n` (ᴹ✶, ᴹAQ.)
- средн. `ds → ts → ss` (ᴹ✶, ᴹQ.)
- средн. `kʰs → ks → s` (ᴹ✶, ᴹQ.)
- средн. `md → nd → n` (ᴹ✶, ᴹAQ.)
- средн. `nb → mb → m` (ᴹ✶, ᴹAQ.)
- средн. `pt → xt → t` (ᴹQ., ᴹQ.)
- средн. `tr → ts → ss` (ᴹAQ., ᴹQ.)
- средн. `tʰs → ts → ss` (ᴹ✶, ᴹQ.)
- средн. `zb → sp → ɸ` (ᴹAQ., ᴹAQ.)
- средн. `zd → st → θ` (ᴹAQ., ᴹAQ.)
- средн. `zg → sk → x` (ᴹAQ., ᴹAQ.)
- средн. `ŋ → ɣ → ø` (ᴹ✶, ᴹQ.)
- средн. `ŋgj → ndj → nj` (ᴹAQ., ᴹQ.)
- средн. `ŋj → ŋgj → ndj` (ᴹ✶, ᴹAQ.)
- средн. `ŋŋ → ŋg → ŋ` (ᴹ✶, ᴹAQ.)
- средн. `ŋɣ → ŋg → ŋ` (ᴹ✶, ᴹAQ.)
- средн. `ɣt → xt → t` (ᴹ✶, ᴹQ.)
- средн. `bd → pt → xt → t` (ᴹAQ., ᴹQ., ᴹQ.)
- средн. `bt → pt → xt → t` (ᴹ✶, ᴹQ., ᴹQ.)
- средн. `gd → kt → xt → t` (ᴹAQ., ᴹQ., ᴹQ.)
- средн. `gt → kt → xt → t` (ᴹ✶, ᴹQ., ᴹQ.)
- средн. `kʰn → kt → xt → t` (ᴹAQ., ᴹQ., ᴹQ.)
- средн. `sg → zg → sk → ks` (ᴹ✶, ᴹAQ., ᴹQ.)
- средн. `sg → zg → sk → x` (ᴹ✶, ᴹAQ., ᴹAQ.)
- средн. `tk → kt → xt → t` (ᴹ✶, ᴹQ., ᴹQ.)
- средн. `zb → sp → ɸ → f` (ᴹAQ., ᴹAQ., ᴹQ.)
- средн. `zd → st → θ → s` (ᴹAQ., ᴹAQ., ᴹQ.)
- средн. `zg → sk → x → h` (ᴹAQ., ᴹAQ., ᴹQ.)
- средн. `ŋj → ŋgj → ndj → nj` (ᴹ✶, ᴹAQ., ᴹQ.)
- средн. `ŋŋ → ŋg → ŋ → n` (ᴹ✶, ᴹAQ., ᴹQ.)
- средн. `ŋɣ → ŋg → ŋ → n` (ᴹ✶, ᴹAQ., ᴹQ.)
