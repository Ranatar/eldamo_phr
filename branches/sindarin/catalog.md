# Фонетические правила: Sindarin / Noldorin

Источник: Eldamo 0.8.13 © Paul Strack, CC BY 4.0. Файл создан `scripts/build.py`; не править вручную.

Правил: 384 (с порядком Eldamo: 338); подформул: 1098; засвидетельствованных дериваций: 3175; формулы воспроизводят 94.4% шагов с известной формулой.

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
| `skʰ > sk` | literal | — |
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

## AT. Ancient Telerin (поздняя концепция)

### [unstressed initial syllables reduced to favored clusters](https://eldamo.org/content/words/word-3648128347.html)

- порядок 00100
- общая формула `{ptkpʰkʰbdgm}V₁{rl}V́₁- > {ptkpʰkʰbdgm}ø{rl}V́₁-`

| подформула | вид | примеры |
|---|---|---|
| `bará- > bra-` | literal | 5 / 5 |
| `kalá- > kla-` | literal | 2 / 1 |
| `kirí- > kri-` | literal | 2 / 2 |
| `pʰilí- > pʰli-` | literal | 2 / 2 |
| `palá- > pla-` | literal | 1 / 1 |
| `turú- > tru-` | literal | 1 / 1 |

### [labialized velars became labials](https://eldamo.org/content/words/word-171120983.html)

- порядок 00200
- общая формула `kw|kʰw|gw|ŋgw|ŋkw|ŋw- > p|pʰ|b|mb|mp|m-`

| подформула | вид | примеры |
|---|---|---|
| `kw > p` | literal | 26 / 26 |
| `kʰw > pʰ` | literal | — |
| `gw > b` | literal | 3 / 3 |
| `ŋgw > mb` | literal | 2 / 2 |
| `ŋkw > mp` | literal | 4 / 3 |
| `ŋw- > m-` | literal | — |

### [[j] was lost after initial dentals](https://eldamo.org/content/words/word-1532676669.html)

- порядок 00300
- общая формула `{ttʰdnl}j- > {ttʰdnl}-`

| подформула | вид | примеры |
|---|---|---|
| `tj- > t-` | literal | — |
| `tʰj- > tʰ-` | literal | — |
| `dj- > d-` | literal | — |
| `nj- > n-` | literal | — |
| `lj- > l-` | literal | — |

### [[ln] became [ll]](https://eldamo.org/content/words/word-1062284643.html)

- порядок 00400

| подформула | вид | примеры |
|---|---|---|
| `ln > ll` | literal | 2 / 2 |

### [final voiceless stops and [s] vanished in polysyllables](https://eldamo.org/content/words/word-981459769.html)

- порядок 00500
- общая формула `-SV{ptks} > -SVø`

| подформула | вид | примеры |
|---|---|---|
| `-SVp > -SVø` | contextual | 1 / 1 |
| `-SVt > -SVø` | contextual | — |
| `-SVk > -SVø` | contextual | 3 / 3 |
| `-SVs > -SVø` | contextual | 1 / 1 |

### [[ms], [ns] became [ss]](https://eldamo.org/content/words/word-1254562549.html)

- порядок 00600
- общая формула `{mn}s > ss`

| подформула | вид | примеры |
|---|---|---|
| `ms > ss` | literal | — |
| `ns > ss` | literal | 1 / 1 |

## OS. Old Sindarin (поздняя концепция)

### [final i-diphthongs became long [ī] in polysyllables](https://eldamo.org/content/words/word-71909447.html)

- порядок 00100
- общая формула `-SVi > -Sī`
- раньше, чем: long final vowels were shortened

| подформула | вид | примеры |
|---|---|---|
| `-Sai > -Sī` | contextual | 4 / 2 |
| `-Sei > -Sī` | contextual | 1 / 0 |
| `-Soi > -Sī` | contextual | 2 / 0 |

### [initial [ŋ] became [ŋg] or [g]](https://eldamo.org/content/words/word-1989991061.html)

- порядок 00200
- общая формула `ŋ- > ŋg-`

| подформула | вид | примеры |
|---|---|---|
| `ŋ- > g-` | literal | — |

### [first in pair of voiced stops vocalized](https://eldamo.org/content/words/word-4282797219.html)

- порядок 00300
- общая формула `Vb{bdg}|Vg{bdg} > Vu{bdg}|Vi{bdg}`
- раньше, чем: [ā], [au] became [ǭ]; [ei], [ou] became [ī], [ū]

| подформула | вид | примеры |
|---|---|---|
| `Vbd > Vud` | contextual | 2 / 2 |
| `Vgd > Vid` | contextual | 3 / 3 |

### [[ɣ] became [g] before nasals and liquids](https://eldamo.org/content/words/word-107931923.html)

- порядок 00400
- общая формула `ɣ{mnlr} > g{mnlr}`

| подформула | вид | примеры |
|---|---|---|
| `ɣr > gr` | literal | 1 / 1 |

### [initial [ɣ]/[h] vanished](https://eldamo.org/content/words/word-1117448055.html)

- порядок 00500
- общая формула `{ɣh}- > ø-`

| подформула | вид | примеры |
|---|---|---|
| `ɣ- > ø-` | loss | 8 / 8 |

### [[j] was lost after initial velars](https://eldamo.org/content/words/word-345959193.html)

- порядок 00600
- общая формула `{kkʰg}j-|skj-|ŋgj > {kkʰg}-|sk-|ŋg`
- раньше, чем: intervocalic [s] became [h]

| подформула | вид | примеры |
|---|---|---|
| `kj- > k-` | literal | 10 / 9 |
| `kʰj- > kʰ-` | literal | 1 / 1 |
| `gj- > g-` | literal | — |
| `skj- > sk-` | literal | — |
| `ŋgj > ŋg` | literal | — |

### [medial [m] became [n] before [j], [w]](https://eldamo.org/content/words/word-1484184939.html)

- порядок 00700
- общая формула `m{jw}|-mw > n{jw}|-mm`

| подформула | вид | примеры |
|---|---|---|
| `mj > nj` | literal | 1 / 1 |
| `mw > nw` | literal | — |
| `-mw > -mm` | literal | — |

### [initial [ml], [mr] became [bl], [br]](https://eldamo.org/content/words/word-1955360003.html)

- порядок 00800
- общая формула `m{lr}- > b{lr}-`

| подформула | вид | примеры |
|---|---|---|
| `ml- > bl-` | literal | — |
| `mr- > br-` | literal | — |

### [initial syllabic [m], [n], [ŋ] became [am], [an], [aŋ]](https://eldamo.org/content/words/word-1024355367.html)

- порядок 00900
- общая формула `{ṃṇŋ̣}- > a{mnŋ}-`

| подформула | вид | примеры |
|---|---|---|
| `ṃ- > am-` | literal | 6 / 6 |
| `ṇ- > an-` | literal | 1 / 1 |
| `ŋ̣- > aŋ-` | literal | 1 / 0 |

### [voiceless stops were voiced before nasals](https://eldamo.org/content/words/word-3463937975.html)

- порядок 01000
- общая формула `{ptk}{mn} > {bdg}{mnŋ}`
- раньше, чем: [bm], [dn] became [mm], [nn]

| подформула | вид | примеры |
|---|---|---|
| `pn > bn` | literal | — |
| `tn > dn` | literal | — |
| `kn > gn` | literal | — |
| `pm > bm` | literal | — |
| `tm > dm` | literal | — |
| `km > gm` | literal | 6 / 6 |

### [[m] became [w] after aspirates](https://eldamo.org/content/words/word-3883770909.html)

- порядок 01100
- общая формула `{ptk}ʰm > {ptk}ʰw`

| подформула | вид | примеры |
|---|---|---|
| `pʰm > pʰw` | literal | — |
| `tʰm > tʰw` | literal | — |
| `kʰm > kʰw` | literal | — |

### [[tʰn] became [ttʰ]](https://eldamo.org/content/words/word-1757900715.html)

- порядок 01200

| подформула | вид | примеры |
|---|---|---|
| `tʰn > ttʰ` | literal | — |

### [final [d] spirantalized and vanished](https://eldamo.org/content/words/word-1789116309.html)

- порядок 01300
- общая формула `-Vd > -V̄ø`

| подформула | вид | примеры |
|---|---|---|
| `-ad > -ā` | literal | 1 / 1 |

### [final [tʰ] became [t]](https://eldamo.org/content/words/word-300026073.html)

- порядок 01400

| подформула | вид | примеры |
|---|---|---|
| `-tʰ > -t` | literal | — |

### [medial [sj], [sw] became [xʲ], [xʷ]](https://eldamo.org/content/words/word-3229649933.html)

- порядок 01500
- общая формула `-sj-|-sw- > -xʲ-|-xʷ-`
- раньше, чем: long final vowels were shortened

| подформула | вид | примеры |
|---|---|---|
| `-sj- > -xʲ-` | literal | 2 / 2 |
| `-sw- > -xʷ-` | literal | 1 / 1 |

### [long final vowels were shortened](https://eldamo.org/content/words/word-2753394075.html)

- порядок 01600
- общая формула `-SV̄ > -SV̆`
- раньше, чем: [ā], [au] became [ǭ]; voiceless stops aspirated after consonants except [s]; [ē], [ō] became [ī], [ū]; intervocalic [s] became [h]; [oi], [ǭi] became [ui], [oi]; [z] vanished before [d] lengthening preceding vowel
- позже, чем: final i-diphthongs became long [ī] in polysyllables; medial [sj], [sw] became [xʲ], [xʷ]

| подформула | вид | примеры |
|---|---|---|
| `-Sī > -Sĭ` | contextual | 35 / 34 |
| `-Sē > -Sĕ` | contextual | 86 / 80 |
| `-Sā > -Să` | contextual | 190 / 187 |
| `-Sō > -Sŏ` | contextual | 37 / 36 |
| `-Sū > -Sŭ` | contextual | 4 / 4 |

### [[z] vanished before [d] lengthening preceding vowel](https://eldamo.org/content/words/word-1249932447.html)

- порядок 01700
- раньше, чем: [ē], [ō] became [ī], [ū]
- позже, чем: long final vowels were shortened

| подформула | вид | примеры |
|---|---|---|
| `Vzd > V̄d` | contextual | 5 / 5 |

### [syllabic initial [s] became [es]](https://eldamo.org/content/words/word-2107885715.html)

- порядок 01800
- раньше, чем: voiceless stops became spirants after initial [s]

| подформула | вид | примеры |
|---|---|---|
| `ṣ- > es-` | literal | 5 / 5 |

### [initial [s] unvoiced following consonants](https://eldamo.org/content/words/word-3923357111.html)

- порядок 01900
- общая формула `s{jwmnrl}- > {j̊w̥m̥n̥l̥r̥}-`

| подформула | вид | примеры |
|---|---|---|
| `sj- > j̊-` | literal | 3 / 3 |
| `sw- > w̥-` | literal | 2 / 2 |
| `sm- > m̥-` | literal | — |
| `sn- > n̥-` | literal | 1 / 1 |
| `sr- > r̥-` | literal | 11 / 11 |
| `sl- > l̥-` | literal | 9 / 8 |

### [final [e] became [a] after single [s] and [st]](https://eldamo.org/content/words/word-1763851339.html)

- порядок 02000
- общая формула `-se|-ste|-sse > -sa|-sta|-sse`
- раньше, чем: intervocalic [s] became [h]; [p], [t], [k] spirantalized before [s]

| подформула | вид | примеры |
|---|---|---|
| `-se > -sa` | literal | — |
| `-ste > -sta` | literal | — |
| `-rte > -rta` | literal | 1 / 1 |
| `-sse > -sse` | identity | — |

### [voiceless stops became spirants after initial [s]](https://eldamo.org/content/words/word-798037075.html)

- порядок 02100
- общая формула `s{ptk}- > s{ɸθx}-`
- позже, чем: syllabic initial [s] became [es]

| подформула | вид | примеры |
|---|---|---|
| `sp- > sɸ-` | literal | 5 / 5 |
| `st- > sθ-` | literal | 5 / 5 |
| `sk- > sx-` | literal | — |

### [voiceless stops aspirated after consonants except [s]](https://eldamo.org/content/words/word-1683955225.html)

- порядок 02200
- общая формула `{ptkmnŋlr}{ptk} > {ptkmnŋlr}{ptk}ʰ`
- раньше, чем: aspirates became voiceless spirants
- позже, чем: long final vowels were shortened

| подформула | вид | примеры |
|---|---|---|
| `pp > ppʰ` | literal | 4 / 4 |
| `pt > ptʰ` | literal | 1 / 1 |
| `tt > ttʰ` | literal | 16 / 16 |
| `tp > tpʰ` | literal | — |
| `kk > kkʰ` | literal | 3 / 3 |
| `kt > ktʰ` | literal | 18 / 17 |
| `gt > gtʰ` | literal | — |
| `np > npʰ` | literal | 1 / 1 |
| `mp > mpʰ` | literal | 7 / 7 |
| `nt > ntʰ` | literal | 14 / 14 |
| `ŋk > ŋkʰ` | literal | 9 / 9 |
| `lp > lpʰ` | literal | 4 / 4 |
| `lt > ltʰ` | literal | 4 / 3 |
| `lk > lkʰ` | literal | 1 / 1 |
| `rp > rpʰ` | literal | — |
| `rt > rtʰ` | literal | 10 / 9 |
| `rk > rkʰ` | literal | 6 / 5 |
| `xt > xtʰ` | literal | 1 / 1 |

### [aspirates became voiceless spirants](https://eldamo.org/content/words/word-883570327.html)

- порядок 02300
- общая формула `{ptk}ʰ|{ptk}{ptk}ʰ > {ɸθx}|{ɸθx}{ɸθx}`
- раньше, чем: [ē], [ō] became [ī], [ū]; [ā], [au] became [ǭ]; [ei], [ou] became [ī], [ū]
- позже, чем: voiceless stops aspirated after consonants except [s]

| подформула | вид | примеры |
|---|---|---|
| `pʰ > ɸ` | literal | 55 / 55 |
| `tʰ > θ` | literal | 93 / 87 |
| `kʰ > x` | literal | 38 / 38 |
| `ppʰ > ɸɸ` | literal | 4 / 4 |
| `ptʰ > ɸθ` | literal | 1 / 1 |
| `ttʰ > θθ` | literal | 18 / 18 |
| `tkʰ > xx` | literal | — |
| `ktʰ > xθ` | literal | 17 / 17 |
| `kkʰ > xx` | literal | 3 / 3 |

### [[eu] became [iu]](https://eldamo.org/content/words/word-2662025405.html)

- порядок 02400

| подформула | вид | примеры |
|---|---|---|
| `eu > iu` | literal | 8 / 8 |

### [[ā], [au] became [ǭ]](https://eldamo.org/content/words/word-2858643115.html)

- порядок 02500
- общая формула `ā|au > ǭ`
- раньше, чем: [oi], [ǭi] became [ui], [oi]; [w] vanished before [u]
- позже, чем: aspirates became voiceless spirants; first in pair of voiced stops vocalized; long final vowels were shortened

| подформула | вид | примеры |
|---|---|---|
| `ā > ǭ` | literal | 74 / 74 |
| `au > ǭ` | literal | — |

### [[j] became [i] after vowels](https://eldamo.org/content/words/word-161840619.html)

- порядок 02600
- общая формула `VjV|-Vj > ViV|-Vi`
- раньше, чем: [oi], [ǭi] became [ui], [oi]

| подформула | вид | примеры |
|---|---|---|
| `VjV > ViV` | contextual | 20 / 15 |
| `-Vj > -Vi` | contextual | — |

### [[ei], [ou] became [ī], [ū]](https://eldamo.org/content/words/word-1942848653.html)

- порядок 02700
- общая формула `ei|ou > ī|ū`
- раньше, чем: [ē], [ō] became [ī], [ū]
- позже, чем: aspirates became voiceless spirants; first in pair of voiced stops vocalized

| подформула | вид | примеры |
|---|---|---|
| `ei > ī` | literal | 2 / 1 |
| `ou > ū` | literal | 2 / 2 |

### [[oi], [ǭi] became [ui], [oi]](https://eldamo.org/content/words/word-2010669085.html)

- порядок 02800
- общая формула `oi|ǭi > ui|oi`
- позже, чем: [ā], [au] became [ǭ]; [j] became [i] after vowels; long final vowels were shortened

| подформула | вид | примеры |
|---|---|---|
| `oi > ui` | literal | 4 / 4 |
| `ǭi > oi` | literal | 7 / 7 |

### [medial [s] assimilated to following nasal](https://eldamo.org/content/words/word-1716741635.html)

- порядок 02900

| подформула | вид | примеры |
|---|---|---|
| `-{sm\|sn}- > -{mm\|nn}-` | contextual | — |

### [intervocalic [s] became [h]](https://eldamo.org/content/words/word-3388236413.html)

- порядок 03000
- общая формула `VsV|-Vs > VhV|-Vh`
- позже, чем: [j] was lost after initial velars; final [e] became [a] after single [s] and [st]; long final vowels were shortened

| подформула | вид | примеры |
|---|---|---|
| `VsV > VhV` | contextual | 14 / 14 |

### [[p], [t], [k] spirantalized before [s]](https://eldamo.org/content/words/word-1516403107.html)

- порядок 03100
- общая формула `ps|ts|ks > ɸɸ|θθ|xx`
- позже, чем: final [e] became [a] after single [s] and [st]

| подформула | вид | примеры |
|---|---|---|
| `ps > ɸɸ` | literal | — |
| `ks > xx` | literal | 1 / 1 |
| `ts > θθ` | literal | 2 / 2 |

### [[rl] became [ll]](https://eldamo.org/content/words/word-1288402337.html)

- порядок 03200

| подформула | вид | примеры |
|---|---|---|
| `rl > ll` | literal | 1 / 1 |

### [[j] vanished before [i], [ui]](https://eldamo.org/content/words/word-2851583127.html)

- порядок 03300
- общая формула `{ji|jui}- > {i|ui}-`

| подформула | вид | примеры |
|---|---|---|
| `ji- > i-` | literal | — |
| `jui- > ui-` | literal | 1 / 1 |

### [[w] vanished before [u]](https://eldamo.org/content/words/word-2167009353.html)

- порядок 03400
- общая формула `{uw|wu} > u`
- позже, чем: [ā], [au] became [ǭ]

| подформула | вид | примеры |
|---|---|---|
| `uw > u` | literal | — |
| `wu > u` | literal | — |

### [[bm], [dn] became [mm], [nn]](https://eldamo.org/content/words/word-2615312913.html)

- порядок 03500
- общая формула `bm|dn > mm|nn`
- позже, чем: voiceless stops were voiced before nasals

| подформула | вид | примеры |
|---|---|---|
| `bm > mm` | literal | — |
| `dn > nn` | literal | — |

## S. Sindarin (поздняя концепция)

### [initial [w] became [gw]](https://eldamo.org/content/words/word-2002760597.html)

- порядок 00100
- раньше, чем: initial nasals vanished before stops; [wo] became [o]; voiced stops became spirants after vowels; [mb], [nd] became [mm], [nn]

| подформула | вид | примеры |
|---|---|---|
| `w- > gw-` | literal | 36 / 35 |

### [initial nasals vanished before stops](https://eldamo.org/content/words/word-3057844573.html)

- порядок 00200
- общая формула `{mb|nd|ŋg}- > {bdg}-`
- раньше, чем: [mb], [nd] became [mm], [nn]; final [l], [r] usually became syllabic; [œ] became [e]
- позже, чем: initial [w] became [gw]

| подформула | вид | примеры |
|---|---|---|
| `mb- > b-` | literal | 17 / 17 |
| `nd- > d-` | literal | 14 / 14 |
| `ŋg- > g-` | literal | 25 / 24 |
| `mf- > f-` | literal | — |
| `nθ- > θ-` | literal | — |
| `ŋx- > x-` | literal | — |

### [final nasals vanished after vowels](https://eldamo.org/content/words/word-876455981.html)

- порядок 00300
- общая формула `-V{mn} > -Vø`
- раньше, чем: short final vowels vanished

| подформула | вид | примеры |
|---|---|---|
| `-Vm > -Vø` | contextual | — |
| `-Vn > -Vø` | contextual | 8 / 8 |

### [initial [s] vanished before spirants](https://eldamo.org/content/words/word-3841187313.html)

- порядок 00400
- общая формула `s{ɸθx}- > {ɸθx}-`
- раньше, чем: [mb], [nd] became [mm], [nn]; initial [x-] became [h-]

| подформула | вид | примеры |
|---|---|---|
| `sɸ- > ɸ-` | literal | 5 / 5 |
| `sθ- > θ-` | literal | 5 / 5 |
| `sx- > x-` | literal | — |

### [initial voiceless [j̊] became [x]](https://eldamo.org/content/words/word-2178021811.html)

- порядок 00500
- раньше, чем: initial [x-] became [h-]

| подформула | вид | примеры |
|---|---|---|
| `j̊- > x-` | literal | 3 / 3 |

### [voiced stops became spirants after liquids](https://eldamo.org/content/words/word-1590520649.html)

- порядок 00600
- общая формула `{rl}{bdg} > {rl}{vðɣ}`
- раньше, чем: [lð] became [ll]; [ɣ] became [i] between sonants and vowels; middle consonants frequently vanished in clusters

| подформула | вид | примеры |
|---|---|---|
| `lb > lv` | literal | — |
| `rb > rv` | literal | — |
| `ld > lð` | literal | 8 / 8 |
| `rd > rð` | literal | 4 / 4 |
| `lg > lɣ` | literal | 3 / 3 |
| `rg > rɣ` | literal | — |

### [[zb], [zg] became [ðβ], [ðɣ]](https://eldamo.org/content/words/word-1951748921.html)

- порядок 00700
- общая формула `z{bg} > ð{βɣ}`
- раньше, чем: final [ɣ] became [a] after a consonant

| подформула | вид | примеры |
|---|---|---|
| `zb > ðβ` | literal | 1 / 1 |
| `zg > ðɣ` | literal | 2 / 2 |

### [short [i], [u] became [e], [o] preceding final [a]](https://eldamo.org/content/words/word-1593810649.html)

- порядок 00800
- общая формула `-{ĭŭ}{C|CC}a > -{eo}{C|CC}a`
- раньше, чем: short [u] often became [o]; voiced stops became spirants after vowels; [x], [ɸ] vocalized between a vowel and [θ]; medial [mf], [nθ], [ŋx], [lθ] became [mm], [nn], [ŋg], [ll]; short final vowels vanished; [h] vanished after vowels; [lð] became [ll]; [mb], [nd] became [mm], [nn]; [œ] became [e]; final [i] intruded into preceding syllable

| подформула | вид | примеры |
|---|---|---|
| `-ĭCa > -eCa` | contextual | 33 / 31 |
| `-ĭCCa > -eCCa` | contextual | 11 / 10 |
| `-ŭCa > -oCa` | contextual | 6 / 5 |
| `-ŭCCa > -oCCa` | contextual | 7 / 5 |

### [voiced stops became spirants after vowels](https://eldamo.org/content/words/word-1726791627.html)

- порядок 00900
- общая формула `V{bdg} > V{vðɣ}`
- раньше, чем: voiceless stops voiced after vowels; short final vowels vanished; [ɣ] vocalized before [l], [r], [m], [n]; final [l], [r] usually became syllabic; [mb], [nd] became [mm], [nn]
- позже, чем: initial [w] became [gw]; short [i], [u] became [e], [o] preceding final [a]

| подформула | вид | примеры |
|---|---|---|
| `Vb > Vv` | contextual | 23 / 22 |
| `Vd > Vð` | contextual | 60 / 57 |
| `Vg > Vɣ` | contextual | 30 / 30 |

### [[ɸ], [β] became [f], [v]](https://eldamo.org/content/words/word-890563133.html)

- порядок 01000
- общая формула `ɸ|β > f|v`
- раньше, чем: [mb], [nd] became [mm], [nn]; [œ] became [e]; short [e], [o] became [i], [u] in syllable before final [i]

| подформула | вид | примеры |
|---|---|---|
| `ɸ > f` | literal | 63 / 58 |
| `β > v` | literal | 1 / 1 |

### [medial [j] became [i]](https://eldamo.org/content/words/word-1679623085.html)

- порядок 01100
- раньше, чем: short [a], [o], [u] became [e], [œ], [y] preceding [i]

| подформула | вид | примеры |
|---|---|---|
| `CjV > CiV` | contextual | 46 / 35 |

### [short [e], [o] became [i], [u] in syllable before final [i]](https://eldamo.org/content/words/word-2646655607.html)

- порядок 01200
- общая формула `-{ĕŏ}{C|CC}i > -{iu}{C|CC}i`
- раньше, чем: short [a], [o], [u] became [e], [œ], [y] preceding [i]
- позже, чем: [ɸ], [β] became [f], [v]

| подформула | вид | примеры |
|---|---|---|
| `-ĕCi > -iCi` | contextual | 8 / 7 |
| `-ĕCCi > -iCCi` | contextual | 5 / 4 |
| `-ŏCi > -uCi` | contextual | 9 / 9 |
| `-ŏCCi > -uCCi` | contextual | 8 / 8 |

### [short [a], [o], [u] became [e], [œ], [y] preceding [i]](https://eldamo.org/content/words/word-3958031275.html)

- порядок 01300
- общая формула `{ăŏŭ}{C|CC}i > {eœy}{C|CC}i`
- раньше, чем: final [i], [u] generally vanished; short vowels vanished before morpheme boundaries; [mb], [nd] became [mm], [nn]; [œ] became [e]; [ē], [ō] became [ī], [ū]
- позже, чем: medial [j] became [i]; short [e], [o] became [i], [u] in syllable before final [i]

| подформула | вид | примеры |
|---|---|---|
| `ăCi > eCi` | contextual | 25 / 25 |
| `ăCCi > eCCi` | contextual | 8 / 7 |
| `ăCăCi > eCeCi` | contextual | 13 / 7 |
| `ăCŭCi > eCyCi` | contextual | 1 / 0 |
| `ŏCi > œCi` | contextual | 3 / 1 |
| `ŏCŭCi > œCyCi` | contextual | 6 / 6 |
| `ŏCŏCi > œCœCi` | contextual | 1 / 1 |
| `ŭCi > yCi` | contextual | 1 / 1 |
| `ŭCCi > yCCi` | contextual | 8 / 8 |

### [[ē], [ō] became [ī], [ū]](https://eldamo.org/content/words/word-3889365613.html)

- порядок 01400
- общая формула `ē|ō > ī|ū`
- раньше, чем: [ŋ] vanished with compensatory lengthening
- позже, чем: short [a], [o], [u] became [e], [œ], [y] preceding [i]; [ei], [ou] became [ī], [ū]; [z] vanished before [d] lengthening preceding vowel; aspirates became voiceless spirants; long final vowels were shortened

| подформула | вид | примеры |
|---|---|---|
| `ē > ī` | literal | 17 / 17 |
| `ō > ū` | literal | 18 / 15 |

### [[ɣ] vocalized before [l], [r], [m], [n]](https://eldamo.org/content/words/word-539122737.html)

- порядок 01500
- общая формула `V{ɣ}{lrmn} > Vi{lrmn}`
- раньше, чем: [ai], [oi] became [ae], [oe]; later [ei] became [ai] in final syllables
- позже, чем: voiced stops became spirants after vowels

| подформула | вид | примеры |
|---|---|---|
| `aɣl > ail` | literal | 1 / 1 |
| `aɣr > air` | literal | 2 / 2 |
| `aɣm > aim` | literal | 2 / 2 |
| `aɣn > ain` | literal | — |
| `eɣl > eil` | literal | 1 / 1 |
| `oɣr > oir` | literal | 1 / 1 |
| `oɣm > oim` | literal | 1 / 1 |
| `oɣn > oin` | literal | 1 / 1 |

### [[x], [ɸ] vocalized between a vowel and [θ]](https://eldamo.org/content/words/word-4002924749.html)

- порядок 01600
- общая формула `Vx{θ}|Vɸ{θ} > Vi{θ}|Vu{θ}`
- раньше, чем: [ai], [oi] became [ae], [oe]
- позже, чем: short [i], [u] became [e], [o] preceding final [a]

| подформула | вид | примеры |
|---|---|---|
| `eɸθ > euθ` | literal | 1 / 1 |
| `exθ > eiθ` | literal | 10 / 10 |
| `axθ > aiθ` | literal | 5 / 4 |
| `ixθ > īθ` | literal | 1 / 1 |
| `uxθ > uiθ` | literal | 2 / 2 |

### [non-initial [xʲ] vocalized to [ix]](https://eldamo.org/content/words/word-2422841513.html)

- порядок 01700
- общая формула `xʲ > ix`

| подформула | вид | примеры |
|---|---|---|
| `xʲ > ix` | literal | 2 / 2 |

### [[iu] and [ju] became [ȳ]](https://eldamo.org/content/words/word-659168127.html)

- порядок 01800
- общая формула `{ij}u|jui > ȳ|jui`
- раньше, чем: [au], [ae] became [o], [e] in polysyllables

| подформула | вид | примеры |
|---|---|---|
| `iu > ȳ` | literal | 8 / 8 |
| `ju > ȳ` | literal | 2 / 1 |
| `jui > jui` | identity | — |

### [short [u] often became [o]](https://eldamo.org/content/words/word-2740073851.html)

- порядок 01900
- общая формула `ŭ|uC{uwv}|u{mnŋ} > o|uC{uwv}|u{mnŋ}`
- раньше, чем: [h] vanished after vowels
- позже, чем: short [i], [u] became [e], [o] preceding final [a]

| подформула | вид | примеры |
|---|---|---|
| `ŭ > o` | literal | 10 / 10 |
| `uCu > uCu` | contextual | 6 / 0 |
| `uCw > uCw` | contextual | 1 / 0 |
| `uCv > uCv` | contextual | 1 / 0 |
| `um > um` | identity | 1 / 0 |
| `un > un` | identity | 1 / 0 |
| `uŋ > uŋ` | identity | 1 / 0 |

### [[nm], [ŋm] became [nw], [ŋw]](https://eldamo.org/content/words/word-3258926163.html)

- порядок 02000
- общая формула `{nŋ}m > {nŋ}w`
- раньше, чем: [ŋ] vanished with compensatory lengthening; short final vowels vanished

| подформула | вид | примеры |
|---|---|---|
| `nm > nw` | literal | 1 / 1 |
| `ŋm > ŋw` | literal | 6 / 6 |

### [[ŋ] vanished with compensatory lengthening](https://eldamo.org/content/words/word-3707785609.html)

- порядок 02100
- общая формула `Vŋ{nw} > V̄{nw}`
- раньше, чем: short final vowels vanished
- позже, чем: [ē], [ō] became [ī], [ū]; [nm], [ŋm] became [nw], [ŋw]

| подформула | вид | примеры |
|---|---|---|
| `Vŋw > V̄w` | contextual | 8 / 8 |
| `Vŋn > V̄n` | contextual | — |

### [[ǭ] became [au]](https://eldamo.org/content/words/word-558704171.html)

- порядок 02200
- раньше, чем: short final vowels vanished; [au], [ae] became [o], [e] in polysyllables; non-initial [m] usually became [v]; initial [x-] became [h-]; [h] vanished after vowels; [mb], [nd] became [mm], [nn]; final [w], [v] vanished after [u]

| подформула | вид | примеры |
|---|---|---|
| `ǭ > au` | literal | 66 / 66 |

### [[ę̄] became [ai]](https://eldamo.org/content/words/word-2387695245.html)

- порядок 02300

| подформула | вид | примеры |
|---|---|---|
| `ę̄ > ai` | literal | — |

### [short final vowels vanished](https://eldamo.org/content/words/word-813787869.html)

- порядок 02400
- общая формула `-S{ĕăŏ} > -Sø`
- раньше, чем: final [i] intruded into preceding syllable; [n] assimilated to following labial; short vowels generally lengthened in monosyllables; final [ll], [nn], [ss] shortened in polysyllables; voiceless stops voiced after vowels; [h] vanished after vowels; short vowels vanished before morpheme boundaries; final [mf], [nθ], [ŋx], [lθ] became [mp], [nt], [ŋk], [lt]; final [ɣ] became [a] after a consonant; [ɣ] otherwise vanished; final [w], [v] vanished after [u]; [lð] became [ll]; [mb], [nd] became [mm], [nn]; [ls], [rs] became [lθ], [ss]; [œ] became [e]; final [l], [r] usually became syllabic; final [w] usually became [u]; final [vn] sometimes became [von]
- позже, чем: [ŋ] vanished with compensatory lengthening; [nm], [ŋm] became [nw], [ŋw]; [ǭ] became [au]; final nasals vanished after vowels; short [i], [u] became [e], [o] preceding final [a]; voiced stops became spirants after vowels

| подформула | вид | примеры |
|---|---|---|
| `-Sĕ > -Sø` | contextual | 213 / 204 |
| `-Să > -Sø` | contextual | 327 / 317 |
| `-Sŏ > -Sø` | contextual | 82 / 82 |

### [final [i] intruded into preceding syllable](https://eldamo.org/content/words/word-2399289739.html)

- порядок 02500
- общая формула `-VCi > -ViC`
- раньше, чем: final [i], [u] generally vanished; later [ei] became [ai] in final syllables; [œ] became [e]
- позже, чем: short [i], [u] became [e], [o] preceding final [a]; short final vowels vanished

| подформула | вид | примеры |
|---|---|---|
| `-iCi > -iC` | contextual | 20 / 15 |
| `-ĕCi > -eiC` | contextual | 40 / 34 |
| `-yCi > -yC` | contextual | 6 / 6 |
| `-œCi > -œiC` | contextual | 1 / 1 |
| `-ǭCi > -oiC` | contextual | — |
| `-ūCi > -uiC` | contextual | 5 / 2 |

### [final [w] sometimes intruded into preceding syllables](https://eldamo.org/content/words/word-4211011237.html)

- порядок 02600
- общая формула `-xw > -ux`

| подформула | вид | примеры |
|---|---|---|
| `-ăCw > -auC` | contextual | 3 / 3 |
| `-ĕCw > -euC` | contextual | 1 / 0 |

### [initial [x-] became [h-]](https://eldamo.org/content/words/word-4287595571.html)

- порядок 02700
- общая формула `x-|x{lr}- > h-|{l̥r̥}-`
- раньше, чем: [ðv] became [ðw]; [mb], [nd] became [mm], [nn]; non-initial [m] usually became [v]
- позже, чем: [ǭ] became [au]; initial [s] vanished before spirants; initial voiceless [j̊] became [x]

| подформула | вид | примеры |
|---|---|---|
| `x- > h-` | literal | 24 / 24 |
| `xl- > l̥-` | literal | — |
| `xr- > r̥-` | literal | — |

### [voiceless stops voiced after vowels](https://eldamo.org/content/words/word-2240258959.html)

- порядок 02800
- общая формула `V{ptk} > V{bdg}`
- раньше, чем: final [w] usually became [u]; final [i], [u] generally vanished; short vowels vanished before morpheme boundaries; final [l], [r] usually became syllabic; [au], [ae] became [o], [e] in polysyllables
- позже, чем: short final vowels vanished; voiced stops became spirants after vowels

| подформула | вид | примеры |
|---|---|---|
| `Vp > Vb` | contextual | 31 / 30 |
| `Vt > Vd` | contextual | 83 / 80 |
| `Vk > Vg` | contextual | 69 / 66 |

### [short vowels generally lengthened in monosyllables](https://eldamo.org/content/words/word-1053424933.html)

- порядок 02900
- общая формула `C*V̆C > C*V̄C`
- позже, чем: short final vowels vanished

| подформула | вид | примеры |
|---|---|---|
| `C*ĭC > C*īC` | contextual | 10 / 9 |
| `C*ĕC > C*ēC` | contextual | 1 / 1 |
| `C*ăC > C*āC` | contextual | 19 / 17 |
| `C*ŏC > C*ōC` | contextual | 17 / 9 |
| `C*yC > C*ȳC` | contextual | — |

### [final [ɣ] became [a] after a consonant](https://eldamo.org/content/words/word-916418731.html)

- порядок 03000
- общая формула `-Cɣ|-Cɣi > -Ca|-Cī`
- раньше, чем: [ɣ] otherwise vanished; non-initial [m] usually became [v]
- позже, чем: [zb], [zg] became [ðβ], [ðɣ]; short final vowels vanished

| подформула | вид | примеры |
|---|---|---|
| `-Cɣ > -Ca` | contextual | 4 / 4 |
| `-Cɣi > -Cī` | contextual | 1 / 1 |

### [[ɣ] became [i] between sonants and vowels](https://eldamo.org/content/words/word-2139740021.html)

- порядок 03100
- общая формула `{lrð}ɣV > {lrð}iV`
- раньше, чем: [ɣ] otherwise vanished
- позже, чем: voiced stops became spirants after liquids

| подформула | вид | примеры |
|---|---|---|
| `lɣV > liV` | contextual | — |
| `rɣV > riV` | contextual | — |

### [[ɣ] otherwise vanished](https://eldamo.org/content/words/word-4164672875.html)

- порядок 03200
- раньше, чем: [ai], [oi] became [ae], [oe]
- позже, чем: [ɣ] became [i] between sonants and vowels; final [ɣ] became [a] after a consonant; short final vowels vanished

| подформула | вид | примеры |
|---|---|---|
| `ɣ > ø` | loss | 22 / 21 |

### [final [-wi] became [-y]](https://eldamo.org/content/words/word-677308549.html)

- порядок 03300
- раньше, чем: final [i], [u] generally vanished

| подформула | вид | примеры |
|---|---|---|
| `-wi > -y` | literal | 1 / 1 |

### [[ls], [rs] became [lθ], [ss]](https://eldamo.org/content/words/word-298324969.html)

- порядок 03400
- общая формула `ls|rs > lθ|ss`
- позже, чем: short final vowels vanished

| подформула | вид | примеры |
|---|---|---|
| `rs > ss` | literal | — |
| `ls > lθ` | literal | — |

### [[h] vanished after vowels](https://eldamo.org/content/words/word-875184187.html)

- порядок 03500
- раньше, чем: final [i], [u] generally vanished; short vowels vanished before morpheme boundaries
- позже, чем: [ǭ] became [au]; short [i], [u] became [e], [o] preceding final [a]; short [u] often became [o]; short final vowels vanished

| подформула | вид | примеры |
|---|---|---|
| `Vh > Vø` | contextual | 14 / 12 |

### [final [i], [u] generally vanished](https://eldamo.org/content/words/word-1815401039.html)

- порядок 03600
- общая формула `-S{ĭŭ}|-uCu|-Sī > -Sø|-uCu|-Sĭ`
- позже, чем: [h] vanished after vowels; final [i] intruded into preceding syllable; final [-wi] became [-y]; short [a], [o], [u] became [e], [œ], [y] preceding [i]; voiceless stops voiced after vowels

| подформула | вид | примеры |
|---|---|---|
| `-Sĭ > -Sø` | contextual | 19 / 19 |
| `-Sŭ > -Sø` | contextual | 1 / 1 |
| `-uCu > -uCu` | contextual | 1 / 0 |
| `-Sī > -Sĭ` | contextual | 2 / 2 |

### [short vowels vanished before morpheme boundaries](https://eldamo.org/content/words/word-2749565259.html)

- порядок 03700
- общая формула `C{ĭĕăŏŭ}+C > Cø+C`
- раньше, чем: [ð] vanished before nasals at morpheme boundaries; long vowels shortened before clusters
- позже, чем: [h] vanished after vowels; short [a], [o], [u] became [e], [œ], [y] preceding [i]; short final vowels vanished; voiceless stops voiced after vowels

| подформула | вид | примеры |
|---|---|---|
| `Cĭ+C > Cø+C` | contextual | 5 / 0 |
| `Cĕ+C > Cø+C` | contextual | 8 / 0 |
| `Că+C > Cø+C` | contextual | 21 / 0 |
| `Cŏ+C > Cø+C` | contextual | 4 / 0 |
| `Cŭ+C > Cø+C` | contextual | 2 / 0 |

### [[ai], [oi] became [ae], [oe]](https://eldamo.org/content/words/word-941153689.html)

- порядок 03800
- общая формула `ai|oi > ae|oe`
- раньше, чем: later [ei] became [ai] in final syllables; final [v] became [w] after [ae], [oe], and sometimes [i]
- позже, чем: [ɣ] otherwise vanished; [ɣ] vocalized before [l], [r], [m], [n]; [x], [ɸ] vocalized between a vowel and [θ]

| подформула | вид | примеры |
|---|---|---|
| `ai > ae` | literal | 59 / 58 |
| `oi > oe` | literal | 10 / 10 |

### [later [ei] became [ai] in final syllables](https://eldamo.org/content/words/word-1660291111.html)

- порядок 03900
- общая формула `-eiC|-ei > -aiC|-ai`
- позже, чем: [ai], [oi] became [ae], [oe]; [ɣ] vocalized before [l], [r], [m], [n]; final [i] intruded into preceding syllable

| подформула | вид | примеры |
|---|---|---|
| `-eiC > -aiC` | contextual | 41 / 39 |
| `-ei > -ai` | literal | — |

### [diphthongs [yi], [yu] became [ui]](https://eldamo.org/content/words/word-3257758901.html)

- порядок 04000
- общая формула `y{iu} > ui`

### [[œi] became [ui] or [y]](https://eldamo.org/content/words/word-1787434575.html)

- порядок 04100
- общая формула `œi > ui|y`

| подформула | вид | примеры |
|---|---|---|
| `œi > y` | literal | 1 / 1 |
| `œi > ui` | literal | — |

### [[nr] became [ðr]](https://eldamo.org/content/words/word-1105959911.html)

- порядок 04200
- раньше, чем: middle consonants frequently vanished in clusters

| подформула | вид | примеры |
|---|---|---|
| `nr > ðr` | literal | 4 / 4 |

### [dissimilation of dental spirants](https://eldamo.org/content/words/word-2090293737.html)

- порядок 04300
- общая формула `{θð}Sθ > {θð}Ss`
- раньше, чем: medial [mf], [nθ], [ŋx], [lθ] became [mm], [nn], [ŋg], [ll]

| подформула | вид | примеры |
|---|---|---|
| `θSθ > sSθ` | contextual | — |
| `θSθ > θSs` | contextual | 1 / 1 |

### [final [mf], [nθ], [ŋx], [lθ] became [mp], [nt], [ŋk], [lt]](https://eldamo.org/content/words/word-1531741019.html)

- порядок 04400
- общая формула `-{mf|nθ|ŋx|lθ} > -{mp|nt|ŋk|lt}`
- раньше, чем: nasals vanished before morpheme boundaries
- позже, чем: short final vowels vanished

| подформула | вид | примеры |
|---|---|---|
| `-mf > -mp` | literal | 4 / 4 |
| `-nθ > -nt` | literal | 5 / 5 |
| `-ŋx > -ŋk` | literal | 5 / 5 |
| `-lθ > -lt` | literal | — |

### [nasals vanished before spirantal clusters](https://eldamo.org/content/words/word-1856165973.html)

- порядок 04500
- общая формула `{mnŋ}{fθxs}{lr} > ø{fθxs}{lr}`
- раньше, чем: middle consonants frequently vanished in clusters; [au], [ae] became [o], [e] in polysyllables; final [l], [r] usually became syllabic; medial [s] became [θ] before [l], [r]

| подформула | вид | примеры |
|---|---|---|
| `mf{lr} > øf{lr}` | contextual | 2 / 2 |
| `nθ{lr} > øθ{lr}` | contextual | 2 / 2 |
| `ns{lr} > øs{lr}` | contextual | — |
| `ŋx{lr} > øx{lr}` | contextual | 2 / 2 |
| `nf > ff` | literal | — |

### [nasals vanished before morpheme boundaries](https://eldamo.org/content/words/word-3282356701.html)

- порядок 04600
- общая формула `-{mnŋ}·{fθxsmnŋl}- > -ø·{fθxsmnŋl}-`
- позже, чем: final [mf], [nθ], [ŋx], [lθ] became [mp], [nt], [ŋk], [lt]

| подформула | вид | примеры |
|---|---|---|
| `nf > øf` | contextual | 1 / 0 |

### [[ð] vanished before nasals at morpheme boundaries](https://eldamo.org/content/words/word-3841960279.html)

- порядок 04700
- общая формула `ð{mnŋ} > ø{mnŋ}`
- раньше, чем: middle consonants frequently vanished in clusters
- позже, чем: short vowels vanished before morpheme boundaries

| подформула | вид | примеры |
|---|---|---|
| `ðm > m` | literal | 1 / 1 |
| `ðn > n` | literal | 1 / 1 |
| `ðŋ > ŋ` | literal | — |

### [voiced spirants restopped after nasals](https://eldamo.org/content/words/word-3123278727.html)

- порядок 04800
- общая формула `-{mnŋ}{vðɣ}- > -{mnŋ}{bdg}-`

### [medial [mf], [nθ], [ŋx], [lθ] became [mm], [nn], [ŋg], [ll]](https://eldamo.org/content/words/word-2996915415.html)

- порядок 04900
- общая формула `-{mf|nθ|ŋx|lθ}- > -{mm|nn|ŋg|l̥l̥}-`
- позже, чем: dissimilation of dental spirants; short [i], [u] became [e], [o] preceding final [a]

| подформула | вид | примеры |
|---|---|---|
| `-mf- > -mm-` | literal | — |
| `-nθ- > -nn-` | literal | 6 / 6 |
| `-ŋx- > -ŋg-` | literal | 2 / 2 |
| `-lθ- > -ll-` | literal | 3 / 3 |

### [voiceless nasals were voiced](https://eldamo.org/content/words/word-725943271.html)

- порядок 05000
- общая формула `m̥|n̥ > m|n`

| подформула | вид | примеры |
|---|---|---|
| `m̥ > m` | literal | — |
| `n̥ > n` | literal | 1 / 1 |

### [long vowels shortened before clusters](https://eldamo.org/content/words/word-2083930569.html)

- порядок 05100
- общая формула `V̄CC > V̆CC`
- раньше, чем: final [w], [v] vanished after [u]
- позже, чем: short vowels vanished before morpheme boundaries

| подформула | вид | примеры |
|---|---|---|
| `īCC > ĭCC` | contextual | 6 / 6 |
| `ūCC > ŭCC` | contextual | 1 / 1 |
| `ȳCC > y̆CC` | contextual | 1 / 1 |

### [[ī], [ū] often shortened in polysyllables](https://eldamo.org/content/words/word-302560565.html)

- порядок 05200
- общая формула `ī|ū > ĭ|ŭ`

| подформула | вид | примеры |
|---|---|---|
| `ī > ĭ` | literal | 4 / 4 |
| `ū > ŭ` | literal | 1 / 1 |

### [[awa] sometimes became [au]](https://eldamo.org/content/words/word-671129175.html)

- порядок 05300
- раньше, чем: [au], [ae] became [o], [e] in polysyllables

| подформула | вид | примеры |
|---|---|---|
| `awa > au` | literal | 1 / 1 |

### [[au], [ae] became [o], [e] in polysyllables](https://eldamo.org/content/words/word-567222053.html)

- порядок 05400
- общая формула `ˌau|ˌae > o|e`
- раньше, чем: middle consonants frequently vanished in clusters; [mb], [nd] became [mm], [nn]
- позже, чем: [awa] sometimes became [au]; [iu] and [ju] became [ȳ]; [ǭ] became [au]; nasals vanished before spirantal clusters; voiceless stops voiced after vowels

| подформула | вид | примеры |
|---|---|---|
| `ˌau > o` | literal | 38 / 38 |
| `ˌae > e` | literal | 1 / 1 |

### [[lð] became [ll]](https://eldamo.org/content/words/word-226282629.html)

- порядок 05500
- раньше, чем: [mb], [nd] became [mm], [nn]
- позже, чем: short [i], [u] became [e], [o] preceding final [a]; short final vowels vanished; voiced stops became spirants after liquids

| подформула | вид | примеры |
|---|---|---|
| `lð > ll` | literal | 8 / 8 |

### [[nl] became [ll]](https://eldamo.org/content/words/word-2759811879.html)

- порядок 05600

| подформула | вид | примеры |
|---|---|---|
| `nl > ll` | literal | — |

### [[mb], [nd] became [mm], [nn]](https://eldamo.org/content/words/word-868023175.html)

- порядок 05700
- общая формула `mb|nd > mm|nn`
- раньше, чем: [n] assimilated to following labial; [mm] shortened; [œ] became [e]; final [ll], [nn], [ss] shortened in polysyllables
- позже, чем: [au], [ae] became [o], [e] in polysyllables; [lð] became [ll]; [ǭ] became [au]; [ɸ], [β] became [f], [v]; initial [s] vanished before spirants; initial [w] became [gw]; initial [x-] became [h-]; initial nasals vanished before stops; short [a], [o], [u] became [e], [œ], [y] preceding [i]; short [i], [u] became [e], [o] preceding final [a]; short final vowels vanished; voiced stops became spirants after vowels

| подформула | вид | примеры |
|---|---|---|
| `mb > mm` | literal | 28 / 28 |
| `nd > nn` | literal | 63 / 63 |

### [middle consonants frequently vanished in clusters](https://eldamo.org/content/words/word-3868328117.html)

- порядок 05800
- раньше, чем: medial [s] became [θ] before [l], [r]
- позже, чем: [au], [ae] became [o], [e] in polysyllables; [ð] vanished before nasals at morpheme boundaries; [nr] became [ðr]; nasals vanished before spirantal clusters; voiced stops became spirants after liquids

| подформула | вид | примеры |
|---|---|---|
| `CCC > CC` | contextual | 19 / 17 |

### [medial [s] became [θ] before [l], [r]](https://eldamo.org/content/words/word-3736793827.html)

- порядок 05900
- общая формула `Vs{lr} > Vθ{lr}`
- позже, чем: middle consonants frequently vanished in clusters; nasals vanished before spirantal clusters

| подформула | вид | примеры |
|---|---|---|
| `Vsl > Vθl` | contextual | — |
| `Vsr > Vθr` | contextual | 2 / 2 |

### [[wo] became [o]](https://eldamo.org/content/words/word-586391091.html)

- порядок 06000
- позже, чем: initial [w] became [gw]

| подформула | вид | примеры |
|---|---|---|
| `wo > o` | literal | 7 / 7 |

### [[n] assimilated to following labial](https://eldamo.org/content/words/word-1126284559.html)

- порядок 06100
- общая формула `n+{mb} > m+{mb}`
- раньше, чем: non-initial [m] usually became [v]; [mm] shortened
- позже, чем: [mb], [nd] became [mm], [nn]; short final vowels vanished

| подформула | вид | примеры |
|---|---|---|
| `n+m > m+m` | contextual | 1 / 0 |
| `n+b > m+b` | contextual | 7 / 0 |

### [[œ] became [e]](https://eldamo.org/content/words/word-1838610927.html)

- порядок 06200
- раньше, чем: final [ll], [nn], [ss] shortened in polysyllables
- позже, чем: [mb], [nd] became [mm], [nn]; [ɸ], [β] became [f], [v]; final [i] intruded into preceding syllable; initial nasals vanished before stops; short [a], [o], [u] became [e], [œ], [y] preceding [i]; short [i], [u] became [e], [o] preceding final [a]; short final vowels vanished

| подформула | вид | примеры |
|---|---|---|
| `œ > e` | literal | 10 / 10 |

### [final [ll], [nn], [ss] shortened in polysyllables](https://eldamo.org/content/words/word-1742178057.html)

- порядок 06300
- общая формула `-SS{ll|nn|ss} > -SS{l|n|s}`
- раньше, чем: [mm] shortened
- позже, чем: [mb], [nd] became [mm], [nn]; [œ] became [e]; short final vowels vanished

| подформула | вид | примеры |
|---|---|---|
| `-SSll > -SSl` | contextual | 9 / 8 |
| `-SSnn > -SSn` | contextual | 28 / 28 |
| `-SSss > -SSs` | contextual | 12 / 12 |

### [final and initial [ŋg] became [ŋ]](https://eldamo.org/content/words/word-311523279.html)

- порядок 06400
- общая формула `ŋg-|-ŋg > ŋ-|-ŋ`

| подформула | вид | примеры |
|---|---|---|
| `ŋg- > ŋ-` | literal | — |
| `-ŋg > -ŋ` | literal | 3 / 3 |

### [non-initial [m] usually became [v]](https://eldamo.org/content/words/word-1951379117.html)

- порядок 06500
- общая формула `Vm|{lr}m|m{mbp} > Vv|{lr}v|m{mbp}`
- раньше, чем: [ðv] became [ðw]; final [l], [r] usually became syllabic; final [vn] sometimes became [von]; final [v] became [w] after [ae], [oe], and sometimes [i]; [ou] became [au]; final [w], [v] vanished after [u]; [mm] shortened
- позже, чем: [n] assimilated to following labial; [ǭ] became [au]; final [ɣ] became [a] after a consonant; initial [x-] became [h-]

| подформула | вид | примеры |
|---|---|---|
| `Vm > Vv` | contextual | 30 / 30 |
| `lm > lv` | literal | 3 / 3 |
| `rm > rv` | literal | — |
| `ðm > ðv` | literal | 2 / 2 |
| `mm > mm` | identity | 17 / 0 |
| `mb > mb` | identity | — |
| `mp > mp` | identity | 2 / 0 |

### [[ðv] became [ðw]](https://eldamo.org/content/words/word-2192660503.html)

- порядок 06600
- позже, чем: initial [x-] became [h-]; non-initial [m] usually became [v]

| подформула | вид | примеры |
|---|---|---|
| `ðv > ðw` | literal | 3 / 3 |

### [[mm] shortened](https://eldamo.org/content/words/word-3689144303.html)

- порядок 06700
- раньше, чем: final [l], [r] usually became syllabic
- позже, чем: [mb], [nd] became [mm], [nn]; [n] assimilated to following labial; final [ll], [nn], [ss] shortened in polysyllables; non-initial [m] usually became [v]

| подформула | вид | примеры |
|---|---|---|
| `mm > m` | literal | 29 / 29 |

### [final [v] became [w] after [ae], [oe], and sometimes [i]](https://eldamo.org/content/words/word-3909760699.html)

- порядок 06800
- общая формула `-{ae|oe}v > -{ae|oe}w`
- позже, чем: [ai], [oi] became [ae], [oe]; non-initial [m] usually became [v]

| подформула | вид | примеры |
|---|---|---|
| `-aev > -aew` | literal | 3 / 3 |
| `-oev > -oew` | literal | 2 / 2 |

### [final [w], [v] vanished after [u]](https://eldamo.org/content/words/word-70600889.html)

- порядок 06900
- общая формула `-u{vw} > -u`
- раньше, чем: [ou] became [au]
- позже, чем: [ǭ] became [au]; long vowels shortened before clusters; non-initial [m] usually became [v]; short final vowels vanished

| подформула | вид | примеры |
|---|---|---|
| `-uv > -u` | literal | 13 / 8 |
| `-uw > -u` | literal | 1 / 1 |
| `-ov > -ou` | literal | 1 / 1 |

### [[ou] became [au]](https://eldamo.org/content/words/word-2476983755.html)

- порядок 07000
- позже, чем: final [w], [v] vanished after [u]; non-initial [m] usually became [v]

| подформула | вид | примеры |
|---|---|---|
| `ou > au` | literal | 3 / 1 |

### [long voiceless spirants shortened](https://eldamo.org/content/words/word-1206014597.html)

- порядок 07100
- общая формула `θθ|xx > θ|x`

| подформула | вид | примеры |
|---|---|---|
| `θθ > θ` | literal | 20 / 20 |
| `xx > x` | literal | 4 / 4 |

### [final [l], [r] usually became syllabic](https://eldamo.org/content/words/word-1942165347.html)

- порядок 07200
- общая формула `-C{lr} > -Co{lr}`
- позже, чем: [mm] shortened; initial nasals vanished before stops; nasals vanished before spirantal clusters; non-initial [m] usually became [v]; short final vowels vanished; voiced stops became spirants after vowels; voiceless stops voiced after vowels

| подформула | вид | примеры |
|---|---|---|
| `-Cl > -Col` | contextual | 11 / 10 |
| `-Cr > -Cor` | contextual | 3 / 3 |

### [final [vn] sometimes became [von]](https://eldamo.org/content/words/word-2569469231.html)

- порядок 07300
- позже, чем: non-initial [m] usually became [v]; short final vowels vanished

| подформула | вид | примеры |
|---|---|---|
| `-vn > -von` | literal | — |

### [final [w] usually became [u]](https://eldamo.org/content/words/word-798091205.html)

- порядок 07400
- общая формула `-Cw|-aw > -Cu|-au`
- позже, чем: short final vowels vanished; voiceless stops voiced after vowels

| подформула | вид | примеры |
|---|---|---|
| `-Cw > -Cu` | contextual | 9 / 8 |
| `-aw > -au` | literal | 4 / 4 |

### [final [rr] became [r]](https://eldamo.org/content/words/word-1254294665.html)

- порядок 07500

| подформула | вид | примеры |
|---|---|---|
| `-rr > -r` | literal | — |

### [[sk], [sp] usually became [sg], [sb]](https://eldamo.org/content/words/word-1759587217.html)

- порядок 07600
- общая формула `s{pk} > s{bg}`

| подформула | вид | примеры |
|---|---|---|
| `sk > sg` | literal | 1 / 1 |
| `sp > sb` | literal | 2 / 2 |

### [medial [x] became [h] in Gondorian pronunciation](https://eldamo.org/content/words/word-4188321265.html)

- порядок 07700
- общая формула `-x- > -h-`

| подформула | вид | примеры |
|---|---|---|
| `-x- > -h-` | literal | — |

### [voiced spirants unvoiced before voiceless spirants](https://eldamo.org/content/words/word-132402625.html)

- порядок 07800
- общая формула `{vð}{hx} > {fθ}`

| подформула | вид | примеры |
|---|---|---|
| `vh > f` | literal | — |
| `ðh > θ` | literal | — |

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

## ON. Old Noldorin (средняя концепция)

### [unstressed initial syllables reduced to favored clusters](https://eldamo.org/content/words/word-341640763.html)

- порядок 00100
- общая формула `{ptkpʰtʰkʰbdgm}V₁{rl}V́₁- > {ptkpʰtʰkʰbdgm}ø{rl}V́₁-`
- вариант правила [unstressed initial syllables reduced to favored clusters](https://eldamo.org/content/words/word-3648128347.html)

| подформула | вид | примеры |
|---|---|---|
| `bará- > bra-` | literal | 2 / 2 |
| `beré- > bre-` | literal | 5 / 4 |
| `boró- > bro-` | literal | 3 / 2 |
| `dará- > dra-` | literal | 4 / 3 |
| `kará- > kra-` | literal | 1 / 0 |
| `kirí- > kri-` | literal | 3 / 3 |
| `kurú- > kru-` | literal | 2 / 1 |
| `kʰará- > kʰra` | contextual | 1 / 0 |
| `galá- > gla-` | literal | 2 / 2 |
| `goló- > glo-` | literal | 2 / 2 |
| `meré- > mre-` | literal | — |
| `moró- > mro-` | literal | 1 / 1 |
| `ŋgalá- > ŋgla-` | literal | 1 / 1 |
| `palá- > pla-` | literal | 1 / 1 |
| `peré- > pre-` | literal | 1 / 1 |
| `pʰilí- > pʰli-` | literal | 1 / 0 |
| `tará- > tra-` | literal | 1 / 1 |
| `teré- > tre-` | literal | 1 / 0 |
| `turú- > tru-` | literal | — |

### [[ms], [ns] became [ss]](https://eldamo.org/content/words/word-1571970483.html)

- порядок 00200
- вариант правила [[ms], [ns] became [ss]](https://eldamo.org/content/words/word-1254562549.html)

| подформула | вид | примеры |
|---|---|---|
| `ns > ss` | literal | — |

### [labialized velars became labials](https://eldamo.org/content/words/word-3214863235.html)

- порядок 00300
- общая формула `kw|kʰw-|gw|ŋgw > p|pʰ-|b|mb`
- вариант правила [labialized velars became labials](https://eldamo.org/content/words/word-171120983.html)

| подформула | вид | примеры |
|---|---|---|
| `kw > p` | literal | 25 / 25 |
| `kʰw- > pʰ-` | literal | — |
| `gw > b` | literal | 1 / 1 |
| `ŋgw > mb` | literal | 10 / 10 |
| `ŋkw > mp` | literal | 4 / 4 |
| `ŋw- > m-` | literal | — |

### [[j] was lost after initial dentals](https://eldamo.org/content/words/word-4016444069.html)

- порядок 00400
- общая формула `{ttʰdnl}j- > {ttʰdnl}-`
- вариант правила [[j] was lost after initial dentals](https://eldamo.org/content/words/word-1532676669.html)

| подформула | вид | примеры |
|---|---|---|
| `tj- > t-` | literal | 6 / 6 |
| `tʰj- > tʰ-` | literal | — |
| `dj- > d-` | literal | 3 / 3 |
| `nj- > n-` | literal | 5 / 5 |
| `lj- > l-` | literal | — |

### [[ln] became [ll]](https://eldamo.org/content/words/word-1894885075.html)

- порядок 00500
- вариант правила [[ln] became [ll]](https://eldamo.org/content/words/word-1062284643.html)

| подформула | вид | примеры |
|---|---|---|
| `ln > ll` | literal | 4 / 4 |

### [final voiceless stops and [s] vanished in polysyllables](https://eldamo.org/content/words/word-2708853431.html)

- порядок 00600
- общая формула `-{ptks} > -ø`
- раньше, чем: final [ǝ] was lost after [l, r, n, s], otherwise it became [a]
- вариант правила [final voiceless stops and [s] vanished in polysyllables](https://eldamo.org/content/words/word-981459769.html)

| подформула | вид | примеры |
|---|---|---|
| `-SVp > -SVø` | contextual | — |
| `-SVt > -SVø` | contextual | 2 / 2 |
| `-SVk > -SVø` | contextual | 1 / 1 |
| `-SVs > -SVø` | contextual | 6 / 5 |

### [final i-diphthongs became long [ī] in polysyllables](https://eldamo.org/content/words/word-2717423421.html)

- порядок 00700
- общая формула `-SVi|-Sui > -Sī|-Sui`
- вариант правила [final i-diphthongs became long [ī] in polysyllables](https://eldamo.org/content/words/word-71909447.html)

| подформула | вид | примеры |
|---|---|---|
| `-Sai > -Sī` | contextual | 1 / 1 |
| `-Soi > -Sī` | contextual | 1 / 0 |
| `-Sui > -Sui` | contextual | 3 / 0 |

### [initial and intervocalic [ŋ] vanished](https://eldamo.org/content/words/word-552653835.html)

- порядок 00800
- общая формула `ŋ-|VŋV > ø-|VøV`
- раньше, чем: [j] was lost after initial velars
- вариант правила [initial [ŋ] became [ŋg] or [g]](https://eldamo.org/content/words/word-1989991061.html)

| подформула | вид | примеры |
|---|---|---|
| `ŋ- > ø-` | loss | 3 / 3 |
| `VŋV > VøV` | contextual | — |

### [first in pair of voiced stops vocalized](https://eldamo.org/content/words/word-4135939067.html)

- порядок 00900
- общая формула `Vb{bdg}|Vg{bdg} > Vu{bdg}|V̄ø{bdg}`
- раньше, чем: [ā], [au] became [ǭ]; [ē], [ō] became [ī], [ū]; [eu], [iu] became [ū]
- вариант правила [first in pair of voiced stops vocalized](https://eldamo.org/content/words/word-4282797219.html)

| подформула | вид | примеры |
|---|---|---|
| `Vbd > Vud` | contextual | 2 / 2 |
| `egd > ēd` | literal | 1 / 1 |
| `agd > ād` | literal | 1 / 1 |

### [[ɣ] and [ŋ] became [g] before nasals](https://eldamo.org/content/words/word-657157649.html)

- порядок 01000
- общая формула `ɣ{mn} > g{mn}`
- раньше, чем: [ɣ] vanished
- вариант правила [[ɣ] became [g] before nasals and liquids](https://eldamo.org/content/words/word-107931923.html)

| подформула | вид | примеры |
|---|---|---|
| `ɣm > gm` | literal | 1 / 1 |
| `ɣn > gn` | literal | 2 / 2 |

### [[ē], [ō] became [ī], [ū]](https://eldamo.org/content/words/word-390078853.html)

- порядок 01100
- общая формула `ē|ō > ī|ū`
- раньше, чем: [j] vanished before [i], [ui]; [ɣ] vanished
- позже, чем: first in pair of voiced stops vocalized
- вариант правила [[ē], [ō] became [ī], [ū]](https://eldamo.org/content/words/word-3889365613.html)

| подформула | вид | примеры |
|---|---|---|
| `ē > ī` | literal | 25 / 25 |
| `ō > ū` | literal | 31 / 31 |

### [[ɣ] vanished](https://eldamo.org/content/words/word-3657372981.html)

- порядок 01200
- общая формула `ɣ|VɣC > ø|V̄øC`
- позже, чем: [ē], [ō] became [ī], [ū]; [ɣ] and [ŋ] became [g] before nasals
- вариант правила [initial [ɣ]/[h] vanished](https://eldamo.org/content/words/word-1117448055.html)

| подформула | вид | примеры |
|---|---|---|
| `ɣ > ø` | loss | 7 / 6 |
| `ɣ- > ø-` | loss | 8 / 8 |

### [[j] was lost after initial velars](https://eldamo.org/content/words/word-4025342543.html)

- порядок 01300
- общая формула `{kkʰg}j-|skj-|ŋgj > {kkʰg}-|sk-|ŋg`
- раньше, чем: intervocalic [s] became [h]
- позже, чем: initial and intervocalic [ŋ] vanished
- вариант правила [[j] was lost after initial velars](https://eldamo.org/content/words/word-345959193.html)

| подформула | вид | примеры |
|---|---|---|
| `kj- > k-` | literal | 2 / 2 |
| `kʰj- > kʰ-` | literal | 5 / 5 |
| `gj- > g-` | literal | 2 / 2 |
| `skj- > sk-` | literal | 1 / 1 |
| `ŋgj > ŋg` | literal | 2 / 1 |

### [medial [m] became [n] before [j], [w]](https://eldamo.org/content/words/word-4127853699.html)

- порядок 01400
- общая формула `m{jw} > n{jw}`
- вариант правила [medial [m] became [n] before [j], [w]](https://eldamo.org/content/words/word-1484184939.html)

| подформула | вид | примеры |
|---|---|---|
| `mj > nj` | literal | 1 / 1 |
| `mw > nw` | literal | 1 / 1 |

### [initial [ml], [mr] became [bl], [br]](https://eldamo.org/content/words/word-1353747713.html)

- порядок 01500
- общая формула `m{lr}- > b{lr}-`
- вариант правила [initial [ml], [mr] became [bl], [br]](https://eldamo.org/content/words/word-1955360003.html)

| подформула | вид | примеры |
|---|---|---|
| `ml- > bl-` | literal | — |
| `mr- > br-` | literal | 1 / 1 |

### [initial syllabic [m], [n], [ŋ] became [am], [an], [aŋ]](https://eldamo.org/content/words/word-1642455461.html)

- порядок 01600
- общая формула `{ṃṇŋ̣}- > a{mnŋ}-`
- вариант правила [initial syllabic [m], [n], [ŋ] became [am], [an], [aŋ]](https://eldamo.org/content/words/word-1024355367.html)

| подформула | вид | примеры |
|---|---|---|
| `ṃ- > am-` | literal | — |
| `ṇ- > an-` | literal | 1 / 1 |
| `ŋ̣- > aŋ-` | literal | 3 / 3 |

### [voiceless stops were voiced before nasals](https://eldamo.org/content/words/word-534625167.html)

- порядок 01700
- общая формула `{ptk}{mn} > {bdg}{mn}`
- раньше, чем: voiced stops became nasals before nasals
- вариант правила [voiceless stops were voiced before nasals](https://eldamo.org/content/words/word-3463937975.html)

| подформула | вид | примеры |
|---|---|---|
| `pn > bn` | literal | 2 / 2 |
| `tn > dn` | literal | 2 / 2 |
| `kn > gn` | literal | 2 / 2 |
| `pm > bm` | literal | — |
| `tm > dm` | literal | 2 / 2 |
| `km > gm` | literal | 5 / 5 |

### [[m] became [w] after aspirates](https://eldamo.org/content/words/word-2312265205.html)

- порядок 01800
- общая формула `{ptk}ʰm > {ptk}ʰw`
- вариант правила [[m] became [w] after aspirates](https://eldamo.org/content/words/word-3883770909.html)

| подформула | вид | примеры |
|---|---|---|
| `pʰm > pʰw` | literal | — |
| `tʰm > tʰw` | literal | 2 / 2 |
| `kʰm > kʰw` | literal | — |

### [[tʰn] became [ttʰ]](https://eldamo.org/content/words/word-2999363625.html)

- порядок 01900
- вариант правила [[tʰn] became [ttʰ]](https://eldamo.org/content/words/word-1757900715.html)

| подформула | вид | примеры |
|---|---|---|
| `tʰn > ttʰ` | literal | 1 / 1 |

### [final [d] spirantalized and vanished](https://eldamo.org/content/words/word-3744491855.html)

- порядок 02000
- общая формула `-Vd > -V̄ø`
- вариант правила [final [d] spirantalized and vanished](https://eldamo.org/content/words/word-1789116309.html)

| подформула | вид | примеры |
|---|---|---|
| `-ad > -ā` | literal | 3 / 3 |

### [final [tʰ] became [t]](https://eldamo.org/content/words/word-337780183.html)

- порядок 02100
- раньше, чем: aspirates became voiceless spirants
- вариант правила [final [tʰ] became [t]](https://eldamo.org/content/words/word-300026073.html)

| подформула | вид | примеры |
|---|---|---|
| `-tʰ > -t` | literal | 1 / 1 |

### [[ht] became [tt]](https://eldamo.org/content/words/word-4165007913.html)

- порядок 02200

| подформула | вид | примеры |
|---|---|---|
| `ht > tt` | literal | 3 / 3 |

### [medial [sj], [sw] became [xʲ], [xʷ]](https://eldamo.org/content/words/word-688973797.html)

- порядок 02300
- общая формула `-s{jw}- > -x{jw}-`
- вариант правила [medial [sj], [sw] became [xʲ], [xʷ]](https://eldamo.org/content/words/word-3229649933.html)

| подформула | вид | примеры |
|---|---|---|
| `-sj- > -xʲ-` | literal | 1 / 0 |
| `-sw- > -xʷ-` | literal | — |

### [long final vowels were shortened](https://eldamo.org/content/words/word-1410098833.html)

- порядок 02400
- общая формула `-SV̄ > -SV̆`
- раньше, чем: [z] became [i] before [d], [g] and [u] before [b]; initial [s] became [θ] before [l], [r]; [oi], [ǭi] became [ui]; intervocalic [s] became [h]; medial [s] assimilated to following nasal or liquid
- вариант правила [long final vowels were shortened](https://eldamo.org/content/words/word-2753394075.html)

| подформула | вид | примеры |
|---|---|---|
| `-Sī > -Sĭ` | contextual | 16 / 16 |
| `-Sē > -Sĕ` | contextual | 76 / 76 |
| `-Sā > -Să` | contextual | 129 / 124 |
| `-Sō > -Sŏ` | contextual | 29 / 28 |
| `-Sū > -Sŭ` | contextual | 7 / 6 |

### [[z] became [i] before [d], [g] and [u] before [b]](https://eldamo.org/content/words/word-754619767.html)

- порядок 02500
- общая формула `z{bdg} > i{bdg}`
- раньше, чем: [ei], [ou] became [ī], [ou]
- позже, чем: long final vowels were shortened
- вариант правила [[z] vanished before [d] lengthening preceding vowel](https://eldamo.org/content/words/word-1249932447.html)

| подформула | вид | примеры |
|---|---|---|
| `zb > ub` | literal | — |
| `zd > id` | literal | 4 / 4 |
| `zg > ig` | literal | 1 / 1 |

### [final [e] became [a] after single [s] and [st]](https://eldamo.org/content/words/word-3342233157.html)

- порядок 02600
- общая формула `-se|-ste|-sse > -sa|-sta|-sse`
- раньше, чем: intervocalic [s] became [h]; [p], [t], [k] spirantalized before [s]
- вариант правила [final [e] became [a] after single [s] and [st]](https://eldamo.org/content/words/word-1763851339.html)

| подформула | вид | примеры |
|---|---|---|
| `-se > -sa` | literal | 10 / 10 |
| `-ste > -sta` | literal | 1 / 1 |
| `-sse > -sse` | identity | 7 / 0 |

### [[eu], [iu] became [ū]](https://eldamo.org/content/words/word-1713708009.html)

- порядок 02700
- общая формула `{eu|iu} > ū`
- позже, чем: first in pair of voiced stops vocalized
- вариант правила [[eu] became [iu]](https://eldamo.org/content/words/word-2662025405.html)

| подформула | вид | примеры |
|---|---|---|
| `eu > ū` | literal | 3 / 3 |
| `iu > ū` | literal | 6 / 6 |
| `ˌeu > io` | literal | 3 / 3 |

### [[ā], [au] became [ǭ]](https://eldamo.org/content/words/word-2790556075.html)

- порядок 02800
- общая формула `ā|au > ǭ`
- раньше, чем: [oi], [ǭi] became [ui]; [w] vanished before [u]; final [ǝ] was lost after [l, r, n, s], otherwise it became [a]
- позже, чем: first in pair of voiced stops vocalized
- вариант правила [[ā], [au] became [ǭ]](https://eldamo.org/content/words/word-2858643115.html)

| подформула | вид | примеры |
|---|---|---|
| `ā > ǭ` | literal | 56 / 55 |
| `au > ǭ` | literal | 24 / 21 |

### [final [ǝ] was lost after [l, r, n, s], otherwise it became [a]](https://eldamo.org/content/words/word-278926673.html)

- порядок 02900
- общая формула `-ǝ|-{lrns}ǝ > -a|-{lrns}ø`
- позже, чем: [ā], [au] became [ǭ]; final voiceless stops and [s] vanished in polysyllables
- вариант правила [final [e] became [a] after single [s] and [st]](https://eldamo.org/content/words/word-1763851339.html)

| подформула | вид | примеры |
|---|---|---|
| `-ǝ > -a` | literal | — |
| `-{lrns}ǝ > -{lrns}ø` | contextual | 1 / 0 |

### [[ǣ] became [ai]](https://eldamo.org/content/words/word-1460547013.html)

- порядок 03000
- вариант правила [[ę̄] became [ai]](https://eldamo.org/content/words/word-2387695245.html)

| подформула | вид | примеры |
|---|---|---|
| `ǣ > ai` | literal | 6 / 6 |

### [[ǣ], [ai] became [ę̄]](https://eldamo.org/content/words/word-3619603651.html)

- порядок 03100
- общая формула `ǣ|ai > ę̄`
- вариант правила [[ǣ] became [ai]](https://eldamo.org/content/words/word-1460547013.html)

| подформула | вид | примеры |
|---|---|---|
| `ǣ > ę̄` | literal | — |
| `ai > ę̄` | literal | 1 / 1 |

### [[j] became [i] after vowels](https://eldamo.org/content/words/word-2164754435.html)

- порядок 03200
- общая формула `VjV|-Vj > ViV|-Vi`
- раньше, чем: [oi], [ǭi] became [ui]; [w] vanished before [u]
- вариант правила [[j] became [i] after vowels](https://eldamo.org/content/words/word-161840619.html)

| подформула | вид | примеры |
|---|---|---|
| `VjV > ViV` | contextual | 12 / 6 |
| `-Vj > -Vi` | contextual | 2 / 2 |

### [[ei], [ou] became [ī], [ou]](https://eldamo.org/content/words/word-2853733721.html)

- порядок 03300
- общая формула `ei|ou > ī|ou`
- позже, чем: [z] became [i] before [d], [g] and [u] before [b]
- вариант правила [[ei], [ou] became [ī], [ū]](https://eldamo.org/content/words/word-1942848653.html)

| подформула | вид | примеры |
|---|---|---|
| `ei > ī` | literal | 9 / 9 |
| `ou > ou` | identity | 3 / 0 |

### [[oi], [ǭi] became [ui]](https://eldamo.org/content/words/word-2826795683.html)

- порядок 03500
- общая формула `{oǭ}i > ui`
- позже, чем: [ā], [au] became [ǭ]; [j] became [i] after vowels; long final vowels were shortened
- вариант правила [[oi], [ǭi] became [ui], [oi]](https://eldamo.org/content/words/word-2010669085.html)

| подформула | вид | примеры |
|---|---|---|
| `oi > ui` | literal | 6 / 6 |
| `ǭi > ui` | literal | 5 / 5 |

### [voiceless stops aspirated after consonants except [s]](https://eldamo.org/content/words/word-1775884631.html)

- порядок 03600
- общая формула `{ptkmnŋlr}{ptk} > {ptkmnŋlr}{ptk}ʰ`
- раньше, чем: voiceless stops became spirants after initial [s]
- вариант правила [voiceless stops aspirated after consonants except [s]](https://eldamo.org/content/words/word-1683955225.html)

| подформула | вид | примеры |
|---|---|---|
| `pp > ppʰ` | literal | 2 / 2 |
| `pt > ptʰ` | literal | — |
| `tt > ttʰ` | literal | 26 / 26 |
| `kk > kkʰ` | literal | 5 / 5 |
| `kt > ktʰ` | literal | 23 / 23 |
| `np > npʰ` | literal | 1 / 1 |
| `mp > mpʰ` | literal | 10 / 10 |
| `nt > ntʰ` | literal | 30 / 30 |
| `ŋk > ŋkʰ` | literal | 15 / 15 |
| `lp > lpʰ` | literal | 4 / 4 |
| `lt > ltʰ` | literal | 7 / 7 |
| `lk > lkʰ` | literal | 7 / 7 |
| `rp > rpʰ` | literal | — |
| `rt > rtʰ` | literal | 19 / 19 |
| `rk > rkʰ` | literal | 10 / 10 |

### [aspirates became voiceless spirants](https://eldamo.org/content/words/word-1770347191.html)

- порядок 03700
- общая формула `{ptk}ʰ|{ptk}{ptk}ʰ > {ɸθx}|{ɸθx}{ɸθx}`
- позже, чем: final [tʰ] became [t]
- вариант правила [aspirates became voiceless spirants](https://eldamo.org/content/words/word-883570327.html)

| подформула | вид | примеры |
|---|---|---|
| `pʰ > ɸ` | literal | 50 / 49 |
| `tʰ > θ` | literal | 106 / 104 |
| `kʰ > x` | literal | 92 / 91 |
| `ppʰ > ɸɸ` | literal | 2 / 2 |
| `ttʰ > θθ` | literal | 31 / 31 |
| `ktʰ > xθ` | literal | 24 / 24 |
| `ptʰ > ɸθ` | literal | — |
| `kkʰ > xx` | literal | 5 / 5 |

### [voiceless stops became spirants after initial [s]](https://eldamo.org/content/words/word-948882833.html)

- порядок 03800
- общая формула `s{ptk}- > s{ɸθx}-`
- позже, чем: voiceless stops aspirated after consonants except [s]
- вариант правила [voiceless stops became spirants after initial [s]](https://eldamo.org/content/words/word-798037075.html)

| подформула | вид | примеры |
|---|---|---|
| `sp- > sɸ-` | literal | 11 / 11 |
| `st- > sθ-` | literal | 15 / 14 |
| `sk- > sx-` | literal | 11 / 11 |

### [initial [s] unvoiced following [m], [n], [j], [w]](https://eldamo.org/content/words/word-3693878703.html)

- порядок 03900
- общая формула `s{jwmn}- > {j̊w̥m̥n̥}-`
- вариант правила [initial [s] unvoiced following consonants](https://eldamo.org/content/words/word-3923357111.html)

| подформула | вид | примеры |
|---|---|---|
| `sm- > m̥-` | literal | 9 / 8 |
| `sn- > n̥-` | literal | 6 / 6 |
| `sj- > j̊-` | literal | 5 / 5 |
| `sw- > w̥-` | literal | 5 / 5 |

### [medial [s] assimilated to following nasal or liquid](https://eldamo.org/content/words/word-2619226303.html)

- порядок 04000
- общая формула `-V{sm|sn|sl|sr}- > -V{mm|nn|ll|rr}-`
- позже, чем: long final vowels were shortened
- вариант правила [medial [s] assimilated to following nasal](https://eldamo.org/content/words/word-1716741635.html)

| подформула | вид | примеры |
|---|---|---|
| `-sm- > -mm-` | literal | 3 / 3 |
| `-sn- > -nn-` | literal | 2 / 2 |
| `-sr- > -rr-` | literal | 1 / 1 |

### [intervocalic [s] became [h]](https://eldamo.org/content/words/word-4036446677.html)

- порядок 04100
- позже, чем: [j] was lost after initial velars; final [e] became [a] after single [s] and [st]; long final vowels were shortened
- вариант правила [intervocalic [s] became [h]](https://eldamo.org/content/words/word-3388236413.html)

| подформула | вид | примеры |
|---|---|---|
| `VsV > VhV` | contextual | 21 / 18 |

### [initial [s] became [θ] before [l], [r]](https://eldamo.org/content/words/word-2075290201.html)

- порядок 04200
- общая формула `s{lr}- > θ{lr}-`
- позже, чем: long final vowels were shortened
- вариант правила [initial [s] unvoiced following consonants](https://eldamo.org/content/words/word-3923357111.html)

| подформула | вид | примеры |
|---|---|---|
| `sl- > θl-` | literal | 8 / 8 |
| `sr- > θr-` | literal | 2 / 2 |

### [[p], [t], [k] spirantalized before [s]](https://eldamo.org/content/words/word-1682758275.html)

- порядок 04400
- общая формула `ps|ts|ks > ɸs|θθ|xs`
- позже, чем: final [e] became [a] after single [s] and [st]
- вариант правила [[p], [t], [k] spirantalized before [s]](https://eldamo.org/content/words/word-1516403107.html)

| подформула | вид | примеры |
|---|---|---|
| `ps > ɸs` | literal | 3 / 3 |
| `ks > xs` | literal | 5 / 5 |
| `ts > θθ` | literal | 9 / 9 |

### [[j] vanished before [i], [ui]](https://eldamo.org/content/words/word-4029245039.html)

- порядок 04500
- общая формула `ji|jui > i|ui`
- позже, чем: [ē], [ō] became [ī], [ū]
- вариант правила [[j] vanished before [i], [ui]](https://eldamo.org/content/words/word-2851583127.html)

| подформула | вид | примеры |
|---|---|---|
| `ji > i` | literal | 8 / 1 |
| `jui > ui` | literal | 2 / 2 |

### [[w] vanished before [u]](https://eldamo.org/content/words/word-169887913.html)

- порядок 04600
- общая формула `{uw|wu} > u`
- позже, чем: [ā], [au] became [ǭ]; [j] became [i] after vowels
- вариант правила [[w] vanished before [u]](https://eldamo.org/content/words/word-2167009353.html)

| подформула | вид | примеры |
|---|---|---|
| `uw > u` | literal | 1 / 0 |
| `wu > u` | literal | 3 / 3 |

### [voiced stops became nasals before nasals](https://eldamo.org/content/words/word-1598588387.html)

- порядок 04700
- общая формула `{bdg}{mn} > {mnŋ}{mn}`
- позже, чем: voiceless stops were voiced before nasals
- вариант правила [[bm], [dn] became [mm], [nn]](https://eldamo.org/content/words/word-2615312913.html)

| подформула | вид | примеры |
|---|---|---|
| `bm > mm` | literal | — |
| `bn > mn` | literal | 6 / 6 |
| `dm > nm` | literal | 5 / 5 |
| `dn > nn` | literal | 2 / 2 |
| `gm > ŋm` | literal | 13 / 13 |
| `gn > ŋn` | literal | 10 / 10 |

## N. Noldorin (средняя концепция)

### [initial nasals vanished before stops](https://eldamo.org/content/words/word-956128961.html)

- порядок 00100
- общая формула `{mb|nd|ŋg}- > {bdg}-`
- раньше, чем: [mb], [nd] became [mm], [nn]; final [l], [r] usually became syllabic; [œ] became [e]
- вариант правила [initial nasals vanished before stops](https://eldamo.org/content/words/word-3057844573.html)

| подформула | вид | примеры |
|---|---|---|
| `mb- > b-` | literal | 20 / 20 |
| `nd- > d-` | literal | 28 / 28 |
| `ŋg- > g-` | literal | 21 / 18 |

### [final nasals vanished after vowels](https://eldamo.org/content/words/word-2852345203.html)

- порядок 00200
- общая формула `-V{mn} > -Vø`
- раньше, чем: short final vowels vanished
- вариант правила [final nasals vanished after vowels](https://eldamo.org/content/words/word-876455981.html)

| подформула | вид | примеры |
|---|---|---|
| `-Vm > -Vø` | contextual | 1 / 1 |
| `-Vn > -Vø` | contextual | 8 / 8 |

### [[ǭ] became [ou]](https://eldamo.org/content/words/word-4073827619.html)

- порядок 00300
- раньше, чем: [ou] became [au]
- вариант правила [[ǭ] became [au]](https://eldamo.org/content/words/word-558704171.html)

| подформула | вид | примеры |
|---|---|---|
| `ǭ > ou` | literal | 77 / 75 |

### [initial [s] vanished before spirants](https://eldamo.org/content/words/word-2061688473.html)

- порядок 00400
- общая формула `s{ɸθx}- > {ɸθx}-`
- раньше, чем: initial [x-] became [h-]; [mb], [nd] became [mm], [nn]
- вариант правила [initial [s] vanished before spirants](https://eldamo.org/content/words/word-3841187313.html)

| подформула | вид | примеры |
|---|---|---|
| `sɸ- > ɸ-` | literal | 11 / 11 |
| `sθ- > θ-` | literal | 15 / 15 |
| `sx- > x-` | literal | 12 / 12 |

### [voiceless [j̊], [w̥] became [x], [xw]](https://eldamo.org/content/words/word-1284301541.html)

- порядок 00500
- общая формула `{j̊|w̥} > {x|xw̥}`
- раньше, чем: [mb], [nd] became [mm], [nn]; initial [x-] became [h-]
- вариант правила [initial voiceless [j̊] became [x]](https://eldamo.org/content/words/word-2178021811.html)

| подформула | вид | примеры |
|---|---|---|
| `j̊- > x-` | literal | 5 / 5 |
| `w̥- > xw-` | literal | 5 / 5 |

### [voiced stops became spirants after liquids](https://eldamo.org/content/words/word-1001382095.html)

- порядок 00600
- общая формула `{rl}{bdg} > {rl}{vðɣ}`
- раньше, чем: [lð] became [ll] or [lt]; [ɣ] became [i] between sonants and vowels
- вариант правила [voiced stops became spirants after liquids](https://eldamo.org/content/words/word-1590520649.html)

| подформула | вид | примеры |
|---|---|---|
| `lb > lv` | literal | 1 / 1 |
| `rb > rv` | literal | 2 / 2 |
| `ld > lð` | literal | 12 / 12 |
| `rd > rð` | literal | 4 / 4 |
| `lg > lɣ` | literal | 8 / 8 |
| `rg > rɣ` | literal | 4 / 4 |

### [[zb], [zg] became [ðβ], [ðɣ]](https://eldamo.org/content/words/word-2258500825.html)

- порядок 00700
- общая формула `z{bg} > ð{βɣ}`
- вариант правила [[zb], [zg] became [ðβ], [ðɣ]](https://eldamo.org/content/words/word-1951748921.html)

| подформула | вид | примеры |
|---|---|---|
| `zb > ðβ` | literal | — |
| `zg > ðɣ` | literal | — |

### [initial [w] became [gw]](https://eldamo.org/content/words/word-2451728863.html)

- порядок 00800
- раньше, чем: voiced stops became spirants after vowels; [mb], [nd] became [mm], [nn]
- вариант правила [initial [w] became [gw]](https://eldamo.org/content/words/word-2002760597.html)

| подформула | вид | примеры |
|---|---|---|
| `w- > gw-` | literal | 40 / 40 |

### [voiced stops became spirants after vowels](https://eldamo.org/content/words/word-8115507.html)

- порядок 00900
- общая формула `V{bdg} > V{vðɣ}`
- раньше, чем: [ɣ], [ŋ] vocalized before [l], [r], [m], [n]; final [l], [r] usually became syllabic; [mb], [nd] became [mm], [nn]
- позже, чем: initial [w] became [gw]
- вариант правила [voiced stops became spirants after vowels](https://eldamo.org/content/words/word-1726791627.html)

| подформула | вид | примеры |
|---|---|---|
| `Vb > Vv` | contextual | 22 / 20 |
| `Vd > Vð` | contextual | 43 / 43 |
| `Vg > Vɣ` | contextual | 30 / 27 |

### [[ɣ], [ŋ] vocalized before [l], [r], [m], [n]](https://eldamo.org/content/words/word-363878661.html)

- порядок 01000
- общая формула `{iea}{ɣŋ}{lrmn}|{ou}{ɣŋ}{lrmn} > {iea}i{lrmn}|{ou}u{lrmn}`
- раньше, чем: short [i], [u] became [e], [o] preceding final [a]; [ou] became [au]; [ei] (sometimes) became [ai] in final syllables; [ai] became [oe] or [ae]; [nm] became [nw]
- позже, чем: voiced stops became spirants after vowels
- вариант правила [[ɣ] vocalized before [l], [r], [m], [n]](https://eldamo.org/content/words/word-539122737.html)

| подформула | вид | примеры |
|---|---|---|
| `aɣl > ail` | literal | 1 / 1 |
| `aɣr > air` | literal | 2 / 2 |
| `aŋm > aim` | literal | 5 / 5 |
| `aŋn > ain` | literal | 4 / 4 |
| `eŋm > eim` | literal | 2 / 2 |
| `eŋn > ein` | literal | 2 / 2 |
| `iŋn > īn` | literal | 1 / 1 |
| `oŋm > oum` | literal | 1 / 1 |
| `uɣl > ūl` | literal | 1 / 1 |
| `uŋn > ūn` | literal | 3 / 3 |

### [short [i], [u] became [e], [o] preceding final [a]](https://eldamo.org/content/words/word-1867193695.html)

- порядок 01100
- общая формула `-{ĭŭ}{C|CC}a > -{eo}{C|CC}a`
- раньше, чем: short [u] often became [o]; [x], [ɸ] vocalized between a vowel and [s], [θ]; short final vowels vanished; [h] vanished after vowels; [lð] became [ll] or [lt]; [mb], [nd] became [mm], [nn]; [œ] became [e]; initial [θl] sometimes became [fl]; final [i] intruded into preceding syllable
- позже, чем: [ɣ], [ŋ] vocalized before [l], [r], [m], [n]
- вариант правила [short [i], [u] became [e], [o] preceding final [a]](https://eldamo.org/content/words/word-1593810649.html)

| подформула | вид | примеры |
|---|---|---|
| `ĭC+Ca > eC+Ca` | contextual | 1 / 0 |
| `-ĭCa > -eCa` | contextual | 21 / 21 |
| `-ĭCCa > -eCCa` | contextual | 23 / 23 |
| `-ŭCa > -oCa` | contextual | 2 / 2 |
| `-ŭCCa > -oCCa` | contextual | 40 / 40 |

### [[x], [ɸ] vocalized between a vowel and [s], [θ]](https://eldamo.org/content/words/word-297940333.html)

- порядок 01200
- общая формула `{iea}{ɸx}{θs}|{ou}{ɸx}{θs}|juiθ > {iea}i{θs}|{ou}u{θs}|juxθ`
- позже, чем: short [i], [u] became [e], [o] preceding final [a]
- вариант правила [[x], [ɸ] vocalized between a vowel and [θ]](https://eldamo.org/content/words/word-4002924749.html)

| подформула | вид | примеры |
|---|---|---|
| `ixθ > īθ` | literal | 3 / 3 |
| `exθ > eiθ` | literal | 9 / 9 |
| `aɸs > ais` | literal | 2 / 2 |
| `axs > ais` | literal | 4 / 4 |
| `axθ > aiθ` | literal | 6 / 6 |
| `juxθ > juiθ` | literal | 2 / 2 |
| `oxθ > ouθ` | literal | 2 / 2 |
| `oxs > ous` | literal | 1 / 1 |
| `oɸs > ous` | literal | 1 / 1 |
| `uxθ > ūθ` | literal | 3 / 3 |

### [[ɸ], [β] became [f], [v]](https://eldamo.org/content/words/word-2995333959.html)

- порядок 01300
- общая формула `ɸ|β > f|v`
- раньше, чем: [ou] became [au]; [mb], [nd] became [mm], [nn]; [œ] became [e]
- вариант правила [[ɸ], [β] became [f], [v]](https://eldamo.org/content/words/word-890563133.html)

| подформула | вид | примеры |
|---|---|---|
| `ɸ > f` | literal | 60 / 58 |
| `β > v` | literal | — |

### [medial [j] became [i]](https://eldamo.org/content/words/word-1126685261.html)

- порядок 01400
- раньше, чем: short [a], [o], [u] became [e], [œ], [y] preceding [i]
- вариант правила [medial [j] became [i]](https://eldamo.org/content/words/word-1679623085.html)

| подформула | вид | примеры |
|---|---|---|
| `CjV > CiV` | contextual | 53 / 49 |

### [short [u] often became [o]](https://eldamo.org/content/words/word-1228910977.html)

- порядок 01500
- общая формула `ŭ|uC{uwv}|u{mnŋ} > o|uC{uwv}|u{mnŋ}`
- раньше, чем: short [a], [o], [u] became [e], [œ], [y] preceding [i]; [h] vanished after vowels
- позже, чем: short [i], [u] became [e], [o] preceding final [a]
- вариант правила [short [u] often became [o]](https://eldamo.org/content/words/word-2740073851.html)

| подформула | вид | примеры |
|---|---|---|
| `ŭ > o` | literal | 22 / 22 |
| `uCu > uCu` | contextual | 10 / 0 |
| `uCw > uCw` | contextual | 1 / 0 |
| `uCv > uCv` | contextual | — |
| `um > um` | identity | 7 / 0 |
| `un > un` | identity | 3 / 0 |
| `uŋ > uŋ` | identity | — |

### [short [e], [o] became [i], [u] in syllable before final [i]](https://eldamo.org/content/words/word-1113919391.html)

- порядок 01600
- общая формула `-{ĕŏ}{C|CC}i > -{iu}{C|CC}i`
- вариант правила [short [e], [o] became [i], [u] in syllable before final [i]](https://eldamo.org/content/words/word-2646655607.html)

| подформула | вид | примеры |
|---|---|---|
| `-ĕCi > -iCi` | contextual | 13 / 13 |
| `-ĕCCi > -iCCi` | contextual | 2 / 2 |
| `-ŏCi > -uCi` | contextual | 3 / 3 |
| `-ŏCCi > -uCCi` | contextual | 6 / 5 |

### [short [a], [o], [u] became [e], [œ], [y] preceding [i]](https://eldamo.org/content/words/word-1963461937.html)

- порядок 01700
- общая формула `{ĕăŏ}{C|CC}i > {ieœ}{C|CC}i`
- раньше, чем: short vowels vanished before morpheme boundaries; initial [pl] became [bl]; [mb], [nd] became [mm], [nn]; [œ] became [e]
- позже, чем: medial [j] became [i]; short [u] often became [o]
- вариант правила [short [a], [o], [u] became [e], [œ], [y] preceding [i]](https://eldamo.org/content/words/word-3958031275.html)

| подформула | вид | примеры |
|---|---|---|
| `ăCi > eCi` | contextual | 38 / 29 |
| `ăCCi > eCCi` | contextual | 9 / 6 |
| `ăCăCi > eCeCi` | contextual | 18 / 14 |
| `ăCVCi > eCVCi` | contextual | — |
| `ăCŏCi > eCœCi` | contextual | 3 / 1 |
| `ăCŭCi > eCyCi` | contextual | 3 / 0 |
| `ŏCi > œCi` | contextual | 11 / 11 |
| `ŏCŏCi > œCœCi` | contextual | 6 / 6 |
| `ŏCVCi > œCVCi` | contextual | 1 / 0 |
| `yCi > œCi` | contextual | 2 / 2 |
| `ŭCi > yCi` | contextual | 2 / 2 |
| `ŭCŭCi > yCyCi` | contextual | 1 / 0 |
| `ŭCCi > yCCi` | contextual | 5 / 4 |

### [[nm] became [nw]](https://eldamo.org/content/words/word-3703611571.html)

- порядок 01800
- раньше, чем: final [w] usually became [u]
- позже, чем: [ɣ], [ŋ] vocalized before [l], [r], [m], [n]
- вариант правила [[nm], [ŋm] became [nw], [ŋw]](https://eldamo.org/content/words/word-3258926163.html)

| подформула | вид | примеры |
|---|---|---|
| `nm > nw` | literal | 3 / 3 |

### [[ou] became [au]](https://eldamo.org/content/words/word-2902864717.html)

- порядок 01900
- раньше, чем: [tl], [dl] became [kl], [gl]; non-initial [m] usually became [v]; short final vowels vanished
- позже, чем: [ɣ], [ŋ] vocalized before [l], [r], [m], [n]; [ǭ] became [ou]; [ɸ], [β] became [f], [v]
- вариант правила [[ou] became [au]](https://eldamo.org/content/words/word-2476983755.html)

| подформула | вид | примеры |
|---|---|---|
| `ou > au` | literal | 86 / 85 |

### [[n] assimilated to following labial](https://eldamo.org/content/words/word-3231141875.html)

- порядок 02000
- общая формула `n+{mb} > m+{mb}`
- раньше, чем: short final vowels vanished; [mm] shortened
- вариант правила [[n] assimilated to following labial](https://eldamo.org/content/words/word-1126284559.html)

| подформула | вид | примеры |
|---|---|---|
| `n+m > m+m` | contextual | 1 / 0 |
| `n+b > m+b` | contextual | 1 / 0 |

### [short final vowels vanished](https://eldamo.org/content/words/word-1490765151.html)

- порядок 02100
- общая формула `-S{ĕăŏ} > -Sø`
- раньше, чем: short vowels generally lengthened in monosyllables; [h] vanished after vowels; [tl], [dl] became [kl], [gl]; short vowels vanished before morpheme boundaries; final [mf], [nθ], [ŋx], [lθ] became [mp], [nt], [ŋk], [lt]; final [ɣ] became [a] after a consonant; [ɣ] otherwise vanished; [w], [v] vanished after [u]; [lð] became [ll] or [lt]; [mb], [nd] became [mm], [nn]; [ls], [rs] became [lθ], [ss]; [œ] became [e]; final [l], [r] usually became syllabic; final [w] usually became [u]; [io] became [ui], [eo]; final [vn] sometimes became [von]; initial [θl] sometimes became [fl]
- позже, чем: [n] assimilated to following labial; [ou] became [au]; final nasals vanished after vowels; short [i], [u] became [e], [o] preceding final [a]
- вариант правила [short final vowels vanished](https://eldamo.org/content/words/word-813787869.html)

| подформула | вид | примеры |
|---|---|---|
| `-Sĕ > -Sø` | contextual | 270 / 264 |
| `-Să > -Sø` | contextual | 402 / 388 |
| `-Sŏ > -Sø` | contextual | 108 / 105 |

### [final [i] intruded into preceding syllable](https://eldamo.org/content/words/word-3166734935.html)

- порядок 02200
- общая формула `-VCi > -ViC`
- раньше, чем: [œ] became [e]
- позже, чем: short [i], [u] became [e], [o] preceding final [a]
- вариант правила [final [i] intruded into preceding syllable](https://eldamo.org/content/words/word-2399289739.html)

| подформула | вид | примеры |
|---|---|---|
| `-iCi > -iC` | contextual | 27 / 25 |
| `-ĕCi > -eiC` | contextual | 37 / 33 |
| `-yCi > -yC` | contextual | 3 / 3 |
| `-ūCi > -uiC` | contextual | 1 / 1 |
| `-auCi > -uiC` | contextual | 6 / 6 |
| `-œCi > -œiC` | contextual | 13 / 13 |
| `-ŭCi > -uiC` | contextual | — |

### [initial [r-], [l-] were unvoiced](https://eldamo.org/content/words/word-876815979.html)

- порядок 02300
- общая формула `{lr}- > {l̥r̥}-`
- раньше, чем: [ei] (sometimes) became [ai] in final syllables; [mb], [nd] became [mm], [nn]; [œ] became [e]
- вариант правила [initial [s] unvoiced following consonants](https://eldamo.org/content/words/word-3923357111.html)

| подформула | вид | примеры |
|---|---|---|
| `l- > l̥-` | literal | 59 / 59 |
| `r- > r̥-` | literal | 57 / 57 |

### [voiceless stops voiced after vowels](https://eldamo.org/content/words/word-2951504533.html)

- порядок 02400
- общая формула `V{ptk} > V{bdg}`
- раньше, чем: [ei] (sometimes) became [ai] in final syllables; short vowels vanished before morpheme boundaries; initial [pl] became [bl]; final [l], [r] usually became syllabic; [ei] sometimes became [e] in unstressed final syllables
- вариант правила [voiceless stops voiced after vowels](https://eldamo.org/content/words/word-2240258959.html)

| подформула | вид | примеры |
|---|---|---|
| `Vp > Vb` | contextual | 23 / 22 |
| `Vt > Vd` | contextual | 82 / 80 |
| `Vk > Vg` | contextual | 63 / 63 |

### [short vowels generally lengthened in monosyllables](https://eldamo.org/content/words/word-3587226727.html)

- порядок 02500
- общая формула `C*V̆C > C*V̄C`
- позже, чем: short final vowels vanished
- вариант правила [short vowels generally lengthened in monosyllables](https://eldamo.org/content/words/word-1053424933.html)

| подформула | вид | примеры |
|---|---|---|
| `C*ĭC > C*īC` | contextual | 12 / 11 |
| `C*ĕC > C*ēC` | contextual | 7 / 7 |
| `C*ăC > C*āC` | contextual | 16 / 16 |
| `C*ŏC > C*ōC` | contextual | 11 / 11 |
| `C*ŭC > C*ūC` | contextual | 1 / 1 |
| `C*yC > C*ȳC` | contextual | 3 / 3 |

### [final [ɣ] became [a] after a consonant](https://eldamo.org/content/words/word-3999248211.html)

- порядок 02600
- общая формула `-C{vɣ}|-Cɣi > -C{ua}|-Cī`
- раньше, чем: [ɣ] otherwise vanished
- позже, чем: short final vowels vanished
- вариант правила [final [ɣ] became [a] after a consonant](https://eldamo.org/content/words/word-916418731.html)

| подформула | вид | примеры |
|---|---|---|
| `-Cɣ > -Ca` | contextual | 5 / 5 |
| `-Cɣi > -Cī` | contextual | 1 / 1 |

### [[ɣ] became [i] between sonants and vowels](https://eldamo.org/content/words/word-2340007385.html)

- порядок 02700
- общая формула `{lr}ɣV > {lr}iV`
- раньше, чем: [ɣ] otherwise vanished
- позже, чем: voiced stops became spirants after liquids
- вариант правила [[ɣ] became [i] between sonants and vowels](https://eldamo.org/content/words/word-2139740021.html)

| подформула | вид | примеры |
|---|---|---|
| `lɣV > liV` | contextual | 1 / 1 |
| `rɣV > riV` | contextual | 2 / 2 |
| `ðɣV > ðiV` | contextual | — |
| `lɣi > li` | literal | — |
| `lɣy > ly` | literal | 1 / 1 |
| `lɣu > lu` | literal | 1 / 1 |

### [[ɣ] otherwise vanished](https://eldamo.org/content/words/word-1058893297.html)

- порядок 02800
- позже, чем: [ɣ] became [i] between sonants and vowels; final [ɣ] became [a] after a consonant; short final vowels vanished
- вариант правила [[ɣ] otherwise vanished](https://eldamo.org/content/words/word-4164672875.html)

| подформула | вид | примеры |
|---|---|---|
| `ɣ > ø` | loss | 26 / 22 |

### [[h] vanished after vowels](https://eldamo.org/content/words/word-2979061283.html)

- порядок 02900
- раньше, чем: short vowels vanished before morpheme boundaries; final [i], [u] generally vanished; [mb], [nd] became [mm], [nn]; final [ll], [nn], [ss] shortened in polysyllables
- позже, чем: short [i], [u] became [e], [o] preceding final [a]; short [u] often became [o]; short final vowels vanished
- вариант правила [[h] vanished after vowels](https://eldamo.org/content/words/word-875184187.html)

| подформула | вид | примеры |
|---|---|---|
| `Vh > Vø` | contextual | 19 / 17 |

### [final [i], [u] generally vanished](https://eldamo.org/content/words/word-2264369305.html)

- порядок 03000
- общая формула `-S{ĭŭ} > -Sø`
- позже, чем: [h] vanished after vowels
- вариант правила [final [i], [u] generally vanished](https://eldamo.org/content/words/word-1815401039.html)

| подформула | вид | примеры |
|---|---|---|
| `-Sĭ > -Sø` | contextual | 13 / 13 |
| `-Sŭ > -Sø` | contextual | 2 / 2 |
| `-uCu > -uCu` | contextual | 3 / 0 |
| `-Sī > -Sĭ` | contextual | 1 / 1 |

### [short vowels vanished before morpheme boundaries](https://eldamo.org/content/words/word-3230272819.html)

- порядок 03100
- общая формула `C{ĭĕăŏŭ}+C > Cø+C`
- раньше, чем: [ð] vanished before nasals; long vowels shortened before clusters
- позже, чем: [h] vanished after vowels; short [a], [o], [u] became [e], [œ], [y] preceding [i]; short final vowels vanished; voiceless stops voiced after vowels
- вариант правила [short vowels vanished before morpheme boundaries](https://eldamo.org/content/words/word-2749565259.html)

| подформула | вид | примеры |
|---|---|---|
| `Cĭ+C > Cø+C` | contextual | 3 / 0 |
| `Cĕ+C > Cø+C` | contextual | 5 / 0 |
| `Că+C > Cø+C` | contextual | 6 / 0 |
| `Cŏ+C > Cø+C` | contextual | 4 / 0 |

### [[ai] became [oe] or [ae]](https://eldamo.org/content/words/word-3173115217.html)

- порядок 03200
- общая формула `ai > oe|ae`
- раньше, чем: final [v] became [w] after [ae], [oe], and sometimes [i]; non-initial [m] usually became [v]; initial [θl] sometimes became [fl]; [ei] (sometimes) became [ai] in final syllables
- позже, чем: [ɣ], [ŋ] vocalized before [l], [r], [m], [n]
- вариант правила [[ai], [oi] became [ae], [oe]](https://eldamo.org/content/words/word-941153689.html)

| подформула | вид | примеры |
|---|---|---|
| `ai > oe` | literal | 19 / 19 |
| `ai > ae` | literal | 54 / 54 |
| `ę̄ > ae` | literal | 1 / 1 |

### [[nr] became [ðr]](https://eldamo.org/content/words/word-1531755313.html)

- порядок 03300
- раньше, чем: middle consonants frequently vanished in clusters
- вариант правила [[nr] became [ðr]](https://eldamo.org/content/words/word-1105959911.html)

| подформула | вид | примеры |
|---|---|---|
| `nr > ðr` | literal | 4 / 4 |

### [[ei] (sometimes) became [ai] in final syllables](https://eldamo.org/content/words/word-3775120039.html)

- порядок 03400
- позже, чем: [ai] became [oe] or [ae]; [ɣ], [ŋ] vocalized before [l], [r], [m], [n]; voiceless stops voiced after vowels; initial [r-], [l-] were unvoiced
- вариант правила [later [ei] became [ai] in final syllables](https://eldamo.org/content/words/word-1660291111.html)

| подформула | вид | примеры |
|---|---|---|
| `ei > ai` | literal | 8 / 8 |

### [initial [pl] became [bl]](https://eldamo.org/content/words/word-4244802075.html)

- порядок 03500
- позже, чем: short [a], [o], [u] became [e], [œ], [y] preceding [i]; voiceless stops voiced after vowels

| подформула | вид | примеры |
|---|---|---|
| `pl- > bl-` | literal | 1 / 1 |

### [[ls], [rs] became [lθ], [ss]](https://eldamo.org/content/words/word-720515691.html)

- порядок 03600
- общая формула `ls|rs > lθ|ss`
- позже, чем: short final vowels vanished
- вариант правила [[ls], [rs] became [lθ], [ss]](https://eldamo.org/content/words/word-298324969.html)

| подформула | вид | примеры |
|---|---|---|
| `rs > ss` | literal | 3 / 3 |
| `ls > lθ` | literal | 2 / 2 |

### [final [mf], [nθ], [ŋx], [lθ] became [mp], [nt], [ŋk], [lt]](https://eldamo.org/content/words/word-1735735423.html)

- порядок 03700
- общая формула `-{mf|nθ|ŋx|lθ} > -{mp|nt|ŋk|lt}`
- раньше, чем: nasals vanished before spirantal clusters
- позже, чем: short final vowels vanished
- вариант правила [final [mf], [nθ], [ŋx], [lθ] became [mp], [nt], [ŋk], [lt]](https://eldamo.org/content/words/word-1531741019.html)

| подформула | вид | примеры |
|---|---|---|
| `-mf > -mp` | literal | 5 / 5 |
| `-nθ > -nt` | literal | 16 / 16 |
| `-ŋx > -ŋk` | literal | 9 / 9 |
| `-lθ > -lt` | literal | 3 / 3 |

### [nasals vanished before spirantal clusters](https://eldamo.org/content/words/word-4006467547.html)

- порядок 03800
- общая формула `{mnŋ}{fθxs}{lr} > ø{fθxs}{lr}`
- раньше, чем: middle consonants frequently vanished in clusters; final [l], [r] usually became syllabic; medial [s] became [θ] before [l], [r]
- позже, чем: final [mf], [nθ], [ŋx], [lθ] became [mp], [nt], [ŋk], [lt]
- вариант правила [nasals vanished before spirantal clusters](https://eldamo.org/content/words/word-1856165973.html)

| подформула | вид | примеры |
|---|---|---|
| `mf{lr} > øf{lr}` | contextual | 1 / 1 |
| `nθ{lr} > øθ{lr}` | contextual | 2 / 2 |
| `ns{lr} > øs{lr}` | contextual | 2 / 2 |
| `ŋx{lr} > øx{lr}` | contextual | 1 / 1 |

### [[ð] vanished before nasals](https://eldamo.org/content/words/word-471170683.html)

- порядок 03900
- общая формула `ð{mnŋ} > ø{mnŋ}`
- раньше, чем: middle consonants frequently vanished in clusters
- позже, чем: short vowels vanished before morpheme boundaries
- вариант правила [[ð] vanished before nasals at morpheme boundaries](https://eldamo.org/content/words/word-3841960279.html)

| подформула | вид | примеры |
|---|---|---|
| `ðm > m` | literal | 1 / 1 |
| `ðn > n` | literal | 1 / 1 |
| `ðŋ > ŋ` | literal | — |

### [voiced spirants restopped after nasals](https://eldamo.org/content/words/word-1497309901.html)

- порядок 04000
- общая формула `-{mnŋ}{vðɣ}- > -{mnŋ}{bdg}-`
- вариант правила [voiced spirants restopped after nasals](https://eldamo.org/content/words/word-3123278727.html)

### [nasals vanished before morpheme boundaries](https://eldamo.org/content/words/word-113588545.html)

- порядок 04100
- общая формула `-n·{fθxsmnŋl}- > -ø·{fθxsmnŋl}-`
- вариант правила [nasals vanished before morpheme boundaries](https://eldamo.org/content/words/word-3282356701.html)

| подформула | вид | примеры |
|---|---|---|
| `nf > øf` | contextual | 1 / 1 |

### [medial [mf], [nθ], [ŋx] became [mm], [nn], [ŋg]](https://eldamo.org/content/words/word-2733695233.html)

- порядок 04200
- общая формула `-{mf|nθ|ŋx}- > -{mm|nn|ŋg}-`
- вариант правила [medial [mf], [nθ], [ŋx], [lθ] became [mm], [nn], [ŋg], [ll]](https://eldamo.org/content/words/word-2996915415.html)

| подформула | вид | примеры |
|---|---|---|
| `-mf- > -mm-` | literal | 4 / 4 |
| `-nθ- > -nn-` | literal | 12 / 12 |
| `-ŋx- > -ŋg-` | literal | 6 / 6 |

### [voiceless nasals were usually voiced](https://eldamo.org/content/words/word-4024445463.html)

- порядок 04300
- общая формула `m̥|n̥ > m|n`
- вариант правила [voiceless nasals were voiced](https://eldamo.org/content/words/word-725943271.html)

| подформула | вид | примеры |
|---|---|---|
| `m̥ > m` | literal | 5 / 4 |
| `n̥ > n` | literal | 5 / 5 |

### [initial [x-] became [h-]](https://eldamo.org/content/words/word-1195324115.html)

- порядок 04400
- общая формула `x-|x{lr}- > h-|{l̥r̥}-`
- раньше, чем: [mb], [nd] became [mm], [nn]
- позже, чем: initial [s] vanished before spirants; voiceless [j̊], [w̥] became [x], [xw]
- вариант правила [initial [x-] became [h-]](https://eldamo.org/content/words/word-4287595571.html)

| подформула | вид | примеры |
|---|---|---|
| `x- > h-` | literal | 72 / 71 |
| `xl- > l̥-` | literal | — |
| `xr- > r̥-` | literal | 1 / 1 |

### [long vowels shortened before clusters](https://eldamo.org/content/words/word-368632267.html)

- порядок 04500
- общая формула `V̄CC > V̆CC`
- позже, чем: short vowels vanished before morpheme boundaries
- вариант правила [long vowels shortened before clusters](https://eldamo.org/content/words/word-2083930569.html)

| подформула | вид | примеры |
|---|---|---|
| `īCC > ĭCC` | contextual | — |
| `ūCC > ŭCC` | contextual | — |

### [[ī], [ū] often shortened in polysyllables](https://eldamo.org/content/words/word-2795592857.html)

- порядок 04600
- общая формула `ī|ū > ĭ|ŭ`
- вариант правила [[ī], [ū] often shortened in polysyllables](https://eldamo.org/content/words/word-302560565.html)

| подформула | вид | примеры |
|---|---|---|
| `ī > ĭ` | literal | 11 / 11 |
| `ū > ŭ` | literal | 7 / 7 |

### [[au], [ae] became [o], [e] in polysyllables](https://eldamo.org/content/words/word-497173381.html)

- порядок 04700
- общая формула `ˌau|ˌae > o|e`
- вариант правила [[au], [ae] became [o], [e] in polysyllables](https://eldamo.org/content/words/word-567222053.html)

| подформула | вид | примеры |
|---|---|---|
| `ˌau > o` | literal | 21 / 21 |
| `ˌae > e` | literal | 1 / 1 |

### [middle consonants frequently vanished in clusters](https://eldamo.org/content/words/word-1537236535.html)

- порядок 04800
- раньше, чем: medial [s] became [θ] before [l], [r]
- позже, чем: [ð] vanished before nasals; [nr] became [ðr]; nasals vanished before spirantal clusters
- вариант правила [middle consonants frequently vanished in clusters](https://eldamo.org/content/words/word-3868328117.html)

| подформула | вид | примеры |
|---|---|---|
| `CCC > CC` | contextual | 8 / 8 |

### [medial [s] became [θ] before [l], [r]](https://eldamo.org/content/words/word-2266682021.html)

- порядок 04900
- общая формула `Vs{lr} > Vθ{lr}`
- раньше, чем: [mb], [nd] became [mm], [nn]
- позже, чем: middle consonants frequently vanished in clusters; nasals vanished before spirantal clusters
- вариант правила [medial [s] became [θ] before [l], [r]](https://eldamo.org/content/words/word-3736793827.html)

| подформула | вид | примеры |
|---|---|---|
| `Vsl > Vθl` | contextual | 1 / 1 |
| `Vsr > Vθr` | contextual | 4 / 4 |

### [[wo] became [o]](https://eldamo.org/content/words/word-3719761789.html)

- порядок 05000
- вариант правила [[wo] became [o]](https://eldamo.org/content/words/word-586391091.html)

| подформула | вид | примеры |
|---|---|---|
| `wo > o` | literal | 1 / 1 |

### [[lð] became [ll] or [lt]](https://eldamo.org/content/words/word-3316520435.html)

- порядок 05100
- общая формула `lð|-lð > ll|-lt`
- раньше, чем: [mb], [nd] became [mm], [nn]
- позже, чем: short [i], [u] became [e], [o] preceding final [a]; short final vowels vanished; voiced stops became spirants after liquids
- вариант правила [[lð] became [ll]](https://eldamo.org/content/words/word-226282629.html)

| подформула | вид | примеры |
|---|---|---|
| `lð > ll` | literal | 10 / 10 |
| `-lð > -lt` | literal | 2 / 2 |

### [[nl] became [ll]](https://eldamo.org/content/words/word-3185726471.html)

- порядок 05200
- вариант правила [[nl] became [ll]](https://eldamo.org/content/words/word-2759811879.html)

| подформула | вид | примеры |
|---|---|---|
| `nl > ll` | literal | — |

### [non-initial [m] usually became [v]](https://eldamo.org/content/words/word-3030431535.html)

- порядок 05300
- общая формула `Xm|m{mbp} > Xv|m{mbp}`
- раньше, чем: [w], [v] vanished after [u]; final [l], [r] usually became syllabic; [io] became [ui], [eo]; final [vn] sometimes became [von]; [mm] shortened
- позже, чем: [ai] became [oe] or [ae]; [ou] became [au]
- вариант правила [non-initial [m] usually became [v]](https://eldamo.org/content/words/word-1951379117.html)

| подформула | вид | примеры |
|---|---|---|
| `Vm > Vv` | contextual | 55 / 55 |
| `lm > lv` | literal | 13 / 13 |
| `rm > rv` | literal | 8 / 8 |
| `mm > mm` | identity | 5 / 0 |
| `mb > mb` | identity | 36 / 0 |
| `mp > mp` | identity | 5 / 0 |

### [final [v] became [w] after [ae], [oe], and sometimes [i]](https://eldamo.org/content/words/word-1696736419.html)

- порядок 05400
- общая формула `-{ae|i}v > -{ae|i}w`
- позже, чем: [ai] became [oe] or [ae]
- вариант правила [final [v] became [w] after [ae], [oe], and sometimes [i]](https://eldamo.org/content/words/word-3909760699.html)

| подформула | вид | примеры |
|---|---|---|
| `-iv > -iw` | literal | 3 / 1 |
| `-aev > -aew` | literal | 10 / 10 |

### [[w], [v] vanished after [u]](https://eldamo.org/content/words/word-297230625.html)

- порядок 05500
- общая формула `u{vw}|ui{vw} > u|ui`
- раньше, чем: [mb], [nd] became [mm], [nn]
- позже, чем: non-initial [m] usually became [v]; short final vowels vanished
- вариант правила [final [w], [v] vanished after [u]](https://eldamo.org/content/words/word-70600889.html)

| подформула | вид | примеры |
|---|---|---|
| `uv > u` | literal | 20 / 13 |
| `uw > u` | literal | — |
| `uiv > ui` | literal | 4 / 4 |
| `uiw > ui` | literal | 2 / 2 |
| `-ovC > -ouC` | contextual | 1 / 1 |

### [[mb], [nd] became [mm], [nn]](https://eldamo.org/content/words/word-1317326183.html)

- порядок 05600
- общая формула `mb|nd > mm|nn`
- раньше, чем: [mm] shortened; final [ll], [nn], [ss] shortened in polysyllables; [œ] became [e]
- позже, чем: [h] vanished after vowels; [lð] became [ll] or [lt]; [ɸ], [β] became [f], [v]; [w], [v] vanished after [u]; initial [s] vanished before spirants; initial [w] became [gw]; initial [x-] became [h-]; initial nasals vanished before stops; voiceless [j̊], [w̥] became [x], [xw]; medial [s] became [θ] before [l], [r]; short [a], [o], [u] became [e], [œ], [y] preceding [i]; short [i], [u] became [e], [o] preceding final [a]; short final vowels vanished; voiced stops became spirants after vowels; initial [r-], [l-] were unvoiced
- вариант правила [[mb], [nd] became [mm], [nn]](https://eldamo.org/content/words/word-868023175.html)

| подформула | вид | примеры |
|---|---|---|
| `mb > mm` | literal | 37 / 37 |
| `nd > nn` | literal | 79 / 79 |

### [[œ] became [e]](https://eldamo.org/content/words/word-1006118073.html)

- порядок 05700
- раньше, чем: [ei] sometimes became [e] in unstressed final syllables; final [ll], [nn], [ss] shortened in polysyllables
- позже, чем: [mb], [nd] became [mm], [nn]; [ɸ], [β] became [f], [v]; final [i] intruded into preceding syllable; initial nasals vanished before stops; short [a], [o], [u] became [e], [œ], [y] preceding [i]; short [i], [u] became [e], [o] preceding final [a]; short final vowels vanished; initial [r-], [l-] were unvoiced
- вариант правила [[œ] became [e]](https://eldamo.org/content/words/word-1838610927.html)

| подформула | вид | примеры |
|---|---|---|
| `œ > e` | literal | 21 / 21 |

### [final [ll], [nn], [ss] shortened in polysyllables](https://eldamo.org/content/words/word-2559778861.html)

- порядок 05800
- общая формула `-SS{ll|nn|ss} > -SS{l|n|s}`
- раньше, чем: [mm] shortened
- позже, чем: [h] vanished after vowels; [mb], [nd] became [mm], [nn]; [œ] became [e]
- вариант правила [final [ll], [nn], [ss] shortened in polysyllables](https://eldamo.org/content/words/word-1742178057.html)

| подформула | вид | примеры |
|---|---|---|
| `-SSll > -SSl` | contextual | 4 / 4 |
| `-SSnn > -SSn` | contextual | 30 / 30 |
| `-SSss > -SSs` | contextual | 22 / 21 |

### [final and initial [ŋg] became [ŋ]](https://eldamo.org/content/words/word-4053547951.html)

- порядок 05900
- общая формула `ŋg-|-ŋg > ŋ-|-ŋ`
- вариант правила [final and initial [ŋg] became [ŋ]](https://eldamo.org/content/words/word-311523279.html)

| подформула | вид | примеры |
|---|---|---|
| `ŋg- > ŋ-` | literal | — |
| `-ŋg > -ŋ` | literal | 11 / 11 |

### [[mm] shortened](https://eldamo.org/content/words/word-2855637749.html)

- порядок 06000
- раньше, чем: final [l], [r] usually became syllabic
- позже, чем: [mb], [nd] became [mm], [nn]; [n] assimilated to following labial; final [ll], [nn], [ss] shortened in polysyllables; non-initial [m] usually became [v]
- вариант правила [[mm] shortened](https://eldamo.org/content/words/word-3689144303.html)

| подформула | вид | примеры |
|---|---|---|
| `mm > m` | literal | 33 / 33 |

### [long voiceless spirants shortened](https://eldamo.org/content/words/word-2631001607.html)

- порядок 06100
- общая формула `ff|θθ|xx > f|θ|x`
- вариант правила [long voiceless spirants shortened](https://eldamo.org/content/words/word-1206014597.html)

| подформула | вид | примеры |
|---|---|---|
| `ff > f` | literal | 2 / 2 |
| `θθ > θ` | literal | 40 / 39 |
| `xx > x` | literal | 5 / 5 |

### [final [l], [r] usually became syllabic](https://eldamo.org/content/words/word-257168135.html)

- порядок 06200
- общая формула `-C{lr} > -Co{lr}`
- позже, чем: [mm] shortened; initial nasals vanished before stops; nasals vanished before spirantal clusters; non-initial [m] usually became [v]; short final vowels vanished; voiced stops became spirants after vowels; voiceless stops voiced after vowels
- вариант правила [final [l], [r] usually became syllabic](https://eldamo.org/content/words/word-1942165347.html)

| подформула | вид | примеры |
|---|---|---|
| `-Cl > -Col` | contextual | 4 / 4 |
| `-Cr > -Cor` | contextual | 14 / 14 |
| `-iCr > -iCer` | contextual | 1 / 1 |

### [final [vn] sometimes became [von]](https://eldamo.org/content/words/word-198304083.html)

- порядок 06300
- позже, чем: non-initial [m] usually became [v]; short final vowels vanished
- вариант правила [final [vn] sometimes became [von]](https://eldamo.org/content/words/word-2569469231.html)

| подформула | вид | примеры |
|---|---|---|
| `-vn > -von` | literal | 2 / 2 |

### [final [w] usually became [u]](https://eldamo.org/content/words/word-1104843109.html)

- порядок 06400
- общая формула `-Cw|-aw > -Cu|-au`
- позже, чем: [nm] became [nw]; short final vowels vanished
- вариант правила [final [w] usually became [u]](https://eldamo.org/content/words/word-798091205.html)

| подформула | вид | примеры |
|---|---|---|
| `-Cw > -Cu` | contextual | 22 / 22 |
| `-aw > -au` | literal | 2 / 2 |

### [[io] became [ui], [eo]](https://eldamo.org/content/words/word-1158299479.html)

- порядок 06500
- позже, чем: non-initial [m] usually became [v]; short final vowels vanished

| подформула | вид | примеры |
|---|---|---|
| `io > ui` | literal | 2 / 1 |

### [final [rr] became [r]](https://eldamo.org/content/words/word-701237681.html)

- порядок 06600
- вариант правила [final [rr] became [r]](https://eldamo.org/content/words/word-1254294665.html)

| подформула | вид | примеры |
|---|---|---|
| `-rr > -r` | literal | 1 / 1 |

### [long [i] shortened before [w]](https://eldamo.org/content/words/word-1006714287.html)

- порядок 06700
- раньше, чем: initial [θl] sometimes became [fl]

| подформула | вид | примеры |
|---|---|---|
| `īw > iw` | literal | 2 / 2 |

### [[tl], [dl] became [kl], [gl]](https://eldamo.org/content/words/word-2165755085.html)

- порядок 06800
- общая формула `{td}l > {kg}l`
- позже, чем: [ou] became [au]; short final vowels vanished

| подформула | вид | примеры |
|---|---|---|
| `tl > kl` | literal | 1 / 1 |
| `dl > gl` | literal | 11 / 8 |

### [initial [θl] sometimes became [fl]](https://eldamo.org/content/words/word-2640707457.html)

- порядок 06900
- позже, чем: [ai] became [oe] or [ae]; long [i] shortened before [w]; short [i], [u] became [e], [o] preceding final [a]; short final vowels vanished

| подформула | вид | примеры |
|---|---|---|
| `θl- > fl-` | literal | 3 / 3 |

### [[ei] sometimes became [e] in unstressed final syllables](https://eldamo.org/content/words/word-3414024931.html)

- порядок 07000
- общая формула `-SeiC > -SeC`
- позже, чем: [œ] became [e]; voiceless stops voiced after vowels

| подформула | вид | примеры |
|---|---|---|
| `-SeiC > -SeC` | contextual | 14 / 13 |
| `-SeiC > -SiC` | contextual | 1 / 1 |

### [[sk], [sp] usually became [sg], [sb]](https://eldamo.org/content/words/word-2755591529.html)

- порядок 07100
- вариант правила [[sk], [sp] usually became [sg], [sb]](https://eldamo.org/content/words/word-1759587217.html)

| подформула | вид | примеры |
|---|---|---|
| `sk > sg` | literal | 3 / 3 |

### [final [-ui] became [-y]](https://eldamo.org/content/words/word-702774181.html)

- порядок 07200
- вариант правила [final [-wi] became [-y]](https://eldamo.org/content/words/word-677308549.html)

| подформула | вид | примеры |
|---|---|---|
| `-ui > -y` | literal | 4 / 4 |

### [voiced spirants unvoiced before voiceless spirants](https://eldamo.org/content/words/word-3892722985.html)

- порядок 07300
- общая формула `{vð}{hx} > {fθ}`
- вариант правила [voiced spirants unvoiced before voiceless spirants](https://eldamo.org/content/words/word-132402625.html)

| подформула | вид | примеры |
|---|---|---|
| `vh > f` | literal | 1 / 1 |
| `ðh > θ` | literal | — |

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

## G. Gnomish (ранняя концепция)

### [palatal consonants became velars](https://eldamo.org/content/words/word-2205165111.html)

- порядок 00100
- общая формула `{tdθzn}ʲ > {kgxðŋ}`
- вариант правила [[j] was lost after initial velars](https://eldamo.org/content/words/word-4025342543.html)

| подформула | вид | примеры |
|---|---|---|
| `θʲ > x` | literal | 1 / 1 |
| `tʲ > k` | literal | 4 / 4 |
| `dʲ > g` | literal | 4 / 4 |
| `nʲ > ŋ` | literal | — |

### [[xʷ] became [f]](https://eldamo.org/content/words/word-3323934825.html)

- порядок 00200

| подформула | вид | примеры |
|---|---|---|
| `xʷ > f` | literal | 5 / 5 |

### [initial voiced spirants became stops](https://eldamo.org/content/words/word-2523049185.html)

- порядок 00300
- общая формула `{βðɣ}- > {bdg}-`

| подформула | вид | примеры |
|---|---|---|
| `β- > b-` | literal | 20 / 20 |
| `ð- > d-` | literal | — |
| `ɣ- > g-` | literal | 8 / 8 |

### [[ɸ], [β] became [f], [v]](https://eldamo.org/content/words/word-4218663817.html)

- порядок 00400
- общая формула `β|ɸ > v|f`
- вариант правила [[ɸ], [β] became [f], [v]](https://eldamo.org/content/words/word-2995333959.html)

| подформула | вид | примеры |
|---|---|---|
| `ɸ > f` | literal | 15 / 15 |
| `β > v` | literal | 12 / 12 |

### [non-initial [kʷ] become [p]](https://eldamo.org/content/words/word-1365625999.html)

- порядок 00500
- вариант правила [2565789453](https://eldamo.org/content/words/word-2565789453.html)

| подформула | вид | примеры |
|---|---|---|
| `Xkʷ > Xp` | contextual | 2 / 2 |

### [[ŋ] became [ŋg]](https://eldamo.org/content/words/word-2869972293.html)

- порядок 00600
- вариант правила [initial and intervocalic [ŋ] vanished](https://eldamo.org/content/words/word-552653835.html)

| подформула | вид | примеры |
|---|---|---|
| `ŋ > ŋg` | literal | 14 / 4 |

### [initial [w] became [gw]](https://eldamo.org/content/words/word-3358436645.html)

- порядок 00700
- раньше, чем: unstressed [wa] became [wo]
- вариант правила [400710869](https://eldamo.org/content/words/word-400710869.html)

| подформула | вид | примеры |
|---|---|---|
| `w- > gʷ-` | literal | 13 / 13 |

### [intervocalic [w] became [v]](https://eldamo.org/content/words/word-2741496655.html)

- порядок 00800
- раньше, чем: short final vowels vanished

| подформула | вид | примеры |
|---|---|---|
| `VwV > VvV` | contextual | 2 / 2 |

### [unstressed initial syllables reduced to favored clusters](https://eldamo.org/content/words/word-1096657061.html)

- порядок 00900
- общая формула `{ptkɸθxbdgmn}V₁{rl}V́₁- > {ptkɸθxbdgmn}ø{rl}V́₁-`
- вариант правила [unstressed initial syllables reduced to favored clusters](https://eldamo.org/content/words/word-341640763.html)

| подформула | вид | примеры |
|---|---|---|
| `bala- > bla-` | literal | 2 / 2 |
| `boro- > bro-` | literal | 1 / 1 |
| `folo- > flo-` | literal | 1 / 1 |
| `kala- > kla-` | literal | 1 / 1 |
| `kere- > kre-` | literal | 2 / 2 |
| `kirí- > krí-` | literal | 4 / 4 |
| `koro- > kro-` | literal | 1 / 1 |
| `gǝro- > gro-` | literal | 1 / 1 |
| `nere- > nre-` | literal | 1 / 1 |
| `noro- > nro-` | literal | 3 / 3 |
| `teli- > tli-` | literal | 1 / 1 |
| `telu- > tlu-` | literal | 1 / 1 |

### [[ī], [ū] became [ai], [au]](https://eldamo.org/content/words/word-1815156341.html)

- порядок 01000
- общая формула `ī|ū|ū{pbfvm} > ai|au|ū{pbfvm}`

| подформула | вид | примеры |
|---|---|---|
| `ī > ai` | literal | 8 / 8 |
| `ū > au` | literal | 5 / 5 |
| `ū{pbfvm} > ū{pbfvm}` | contextual | — |

### [[ē], [ō] became [ī], [ū]](https://eldamo.org/content/words/word-1277969137.html)

- порядок 01100
- общая формула `ē|ō > ī|ū`
- раньше, чем: [ll] became [l] lengthening preceding stressed vowel
- вариант правила [[ē], [ō] became [ī], [ū]](https://eldamo.org/content/words/word-390078853.html)

| подформула | вид | примеры |
|---|---|---|
| `ē > ī` | literal | 7 / 7 |
| `ō > ū` | literal | 2 / 2 |

### [initial [ŋgʷ] became [gʷ]](https://eldamo.org/content/words/word-1371815731.html)

- порядок 01200
- вариант правила [initial nasals vanished before stops](https://eldamo.org/content/words/word-956128961.html)

| подформула | вид | примеры |
|---|---|---|
| `ŋgʷ- > gʷ-` | literal | 13 / 13 |

### [[ā] became [ō]](https://eldamo.org/content/words/word-3140771935.html)

- порядок 01300
- общая формула `ā > ō`
- раньше, чем: [ll] became [l] lengthening preceding stressed vowel
- вариант правила [[ā], [au] became [ǭ]](https://eldamo.org/content/words/word-2790556075.html)

| подформула | вид | примеры |
|---|---|---|
| `ā > ō` | literal | 7 / 7 |

### [unstressed [au], [ai] became [ō], [ē]](https://eldamo.org/content/words/word-3579735133.html)

- порядок 01400
- общая формула `ˌau|ˌai > ō|ē`

| подформула | вид | примеры |
|---|---|---|
| `ˌau > ō` | literal | — |
| `ˌai > ē` | literal | 2 / 1 |

### [[eu], [iu] became [io] or [iu]](https://eldamo.org/content/words/word-1598541361.html)

- порядок 01500
- общая формула `{eu|iu} > io|iu`
- вариант правила [2838612897](https://eldamo.org/content/words/word-2838612897.html)

| подформула | вид | примеры |
|---|---|---|
| `eu > io` | literal | 1 / 1 |
| `iu > io` | literal | 4 / 4 |
| `eu > iu` | literal | — |

### [[ei], [ou] became [ē], [ō]](https://eldamo.org/content/words/word-1053983129.html)

- порядок 01600
- общая формула `ei|ou > ē|ō`
- раньше, чем: [oi] became [ui]
- вариант правила [1880600739](https://eldamo.org/content/words/word-1880600739.html)

| подформула | вид | примеры |
|---|---|---|
| `ei > ē` | literal | 2 / 2 |
| `ou > ō` | literal | 13 / 11 |

### [[ao] became [o]](https://eldamo.org/content/words/word-2507211565.html)

- порядок 01800
- общая формула `ao > o`

| подформула | вид | примеры |
|---|---|---|
| `ao > o` | literal | 1 / 1 |

### [unstressed [wa] became [wo]](https://eldamo.org/content/words/word-2099337057.html)

- порядок 01900
- общая формула `{wˌa|wo} > o`
- позже, чем: initial [w] became [gw]
- вариант правила [stressed [wŏ] became [wa]](https://eldamo.org/content/words/word-1415948757.html)

| подформула | вид | примеры |
|---|---|---|
| `wˌa > wo` | literal | 2 / 0 |

### [unstressed [ui] became [wi]](https://eldamo.org/content/words/word-150094523.html)

- порядок 02000

| подформула | вид | примеры |
|---|---|---|
| `ˌui > wi` | literal | — |

### [syllabic consonants developed vowels](https://eldamo.org/content/words/word-1924948145.html)

- порядок 02100
- общая формула `ḷ|ṛ|ṇ > Vl|Vr|Vn`

| подформула | вид | примеры |
|---|---|---|
| `bḷ- > bli-` | literal | 1 / 1 |
| `gḷ- > gli-` | literal | — |
| `kḷ- > kli-` | literal | — |
| `nḷ- > nli-` | literal | 1 / 1 |
| `mḷ- > mli-` | literal | — |
| `tḷ- > tli-` | literal | 1 / 1 |
| `bṛ- > bri-` | literal | 1 / 1 |
| `gṛ- > gri-` | literal | 3 / 3 |
| `nṛ- > nri-` | literal | 3 / 3 |
| `mṛ- > mri-` | literal | 2 / 2 |
| `tṛ- > tri-` | literal | 1 / 1 |
| `-ḷ > -li` | literal | 1 / 1 |
| `Cʷṛ > Cʷur` | contextual | 3 / 0 |
| `ḷm > ulm` | literal | 1 / 1 |
| `ḹ > al` | literal | 8 / 8 |
| `ḷ > il` | literal | 1 / 1 |
| `ṝ > ar` | literal | 9 / 9 |

### [syllabic nasals became [in] or [an]](https://eldamo.org/content/words/word-3923587781.html)

- порядок 02200
- общая формула `ṇ|ṇ̄ > in|an`
- вариант правила [initial syllabic [m], [n], [ŋ] became [am], [an], [aŋ]](https://eldamo.org/content/words/word-1642455461.html)

| подформула | вид | примеры |
|---|---|---|
| `ṇ > in` | literal | 3 / 3 |
| `ṇ̄ > an` | literal | 7 / 7 |

### [initial [j] usually became [g]](https://eldamo.org/content/words/word-712894237.html)

- порядок 02300
- общая формула `j-|ji- > g-|i-`
- вариант правила [[j] vanished before [i], [ui]](https://eldamo.org/content/words/word-4029245039.html)

| подформула | вид | примеры |
|---|---|---|
| `j- > g-` | literal | 17 / 15 |
| `ji- > i-` | literal | 1 / 1 |

### [[e] becomes [i] before stressed [i]](https://eldamo.org/content/words/word-1312401427.html)

- порядок 02400

| подформула | вид | примеры |
|---|---|---|
| `eCí > iCi` | contextual | 3 / 3 |

### [[wo] became [o]](https://eldamo.org/content/words/word-2946990975.html)

- порядок 02500
- вариант правила [[wo] became [o]](https://eldamo.org/content/words/word-3719761789.html)

| подформула | вид | примеры |
|---|---|---|
| `wo > o` | literal | — |

### [labialized velars became velars before [o], [u]](https://eldamo.org/content/words/word-3460441403.html)

- порядок 02600
- общая формула `Cʷu|Cʷo > Cu|Co`
- вариант правила [[wo] became [o]](https://eldamo.org/content/words/word-3719761789.html)

| подформула | вид | примеры |
|---|---|---|
| `gʷo > go` | literal | 4 / 2 |
| `gʷu > gu` | literal | 3 / 2 |
| `kʷo > ko` | literal | — |
| `kʷu > ku` | literal | 1 / 1 |

### [short final vowels vanished](https://eldamo.org/content/words/word-634661439.html)

- порядок 02700
- общая формула `-S{ĭĕăŏŭ} > -Sø`
- позже, чем: intervocalic [w] became [v]
- вариант правила [short final vowels vanished](https://eldamo.org/content/words/word-1490765151.html)

| подформула | вид | примеры |
|---|---|---|
| `-Sĭ > -Sø` | contextual | 6 / 6 |
| `-Sĕ > -Sø` | contextual | 27 / 24 |
| `-Să > -Sø` | contextual | 42 / 42 |
| `-Sŏ > -Sø` | contextual | 8 / 8 |
| `-Sŭ > -Sø` | contextual | 7 / 7 |

### [final [n] sometimes became syllabic](https://eldamo.org/content/words/word-1436029253.html)

- порядок 02800
- общая формула `-C{n} > -Co{n}`
- вариант правила [final [vn] sometimes became [von]](https://eldamo.org/content/words/word-198304083.html)

| подформула | вид | примеры |
|---|---|---|
| `-Cn > -Con` | contextual | 1 / 1 |

### [long final vowels were shortened](https://eldamo.org/content/words/word-3801855289.html)

- порядок 02900
- общая формула `-S{īēǣāōū} > -S{ĭĭăăăŭ}`
- вариант правила [long final vowels were shortened](https://eldamo.org/content/words/word-1410098833.html)

| подформула | вид | примеры |
|---|---|---|
| `-Sī > -Sĭ` | contextual | 10 / 10 |
| `-Sē > -Sĭ` | contextual | 2 / 1 |
| `-Sǣ > -Să` | contextual | 3 / 1 |
| `-Sā > -Să` | contextual | 18 / 17 |
| `-Sō > -Să` | contextual | 2 / 2 |
| `-Sū > -Sŭ` | contextual | 5 / 5 |

### [unstressed long vowels shortened](https://eldamo.org/content/words/word-344365373.html)

- порядок 03000
- общая формула `ˌV̄ > V̆`

| подформула | вид | примеры |
|---|---|---|
| `ˌV̄ > V̆` | contextual | 4 / 4 |

### [initial [sj] became [x]](https://eldamo.org/content/words/word-2688788155.html)

- порядок 03100
- раньше, чем: initial [x-] became [h-]

| подформула | вид | примеры |
|---|---|---|
| `sj- > x-` | literal | 3 / 3 |

### [initial [x-] became [h-]](https://eldamo.org/content/words/word-501264925.html)

- порядок 03200
- позже, чем: initial [sj] became [x]
- вариант правила [initial [x-] became [h-]](https://eldamo.org/content/words/word-1195324115.html)

| подформула | вид | примеры |
|---|---|---|
| `x- > h-` | literal | 19 / 18 |

### [initial [n], [m] became [d], [b] before [l], [r]](https://eldamo.org/content/words/word-1360745545.html)

- порядок 03300
- общая формула `{mn}{lr}- > {bd}{lr}-`
- раньше, чем: [tl], [dl], [ðl] became [kl], [gl]
- вариант правила [initial [ml], [mr] became [bl], [br]](https://eldamo.org/content/words/word-1353747713.html)

| подформула | вид | примеры |
|---|---|---|
| `nl- > dl-` | literal | 1 / 1 |
| `nr- > ndr-` | literal | 7 / 7 |
| `ml- > mbl-` | literal | 1 / 1 |
| `mr- > mbr-` | literal | 2 / 2 |

### [[θ], [ð] became [s] before [p], [t], [k], [b] and [s]](https://eldamo.org/content/words/word-976451235.html)

- порядок 03400
- общая формула `{θð}{ptkbs} > s{ptkbs}`

| подформула | вид | примеры |
|---|---|---|
| `ðk > sk` | literal | 1 / 1 |
| `ðs > ss` | literal | 1 / 1 |
| `ðt > st` | literal | 3 / 2 |
| `θk > sk` | literal | 3 / 3 |
| `θs > ss` | literal | 1 / 1 |
| `θt > st` | literal | 1 / 1 |

### [voiced stop plus [h] became voiceless spirant](https://eldamo.org/content/words/word-259168593.html)

- порядок 03500
- общая формула `{bdg}h > {fθx}ø`

| подформула | вид | примеры |
|---|---|---|
| `bh > f` | literal | — |
| `dh > θ` | literal | 1 / 1 |
| `gh > x` | literal | — |

### [voiceless stops spirantalized after many consonants](https://eldamo.org/content/words/word-473550387.html)

- порядок 03600
- общая формула `{lrmnŋ}{ptk}|{ptk}{fθx}|ɣt > {lrmnŋ]}{fθx}|{fθx}{fθx}|ɣð`
- вариант правила [voiceless stops aspirated after consonants except [s]](https://eldamo.org/content/words/word-1775884631.html)

| подформула | вид | примеры |
|---|---|---|
| `lp > lf` | literal | 2 / 2 |
| `lt > lθ` | literal | 6 / 6 |
| `lk > lx` | literal | 4 / 4 |
| `rp > rf` | literal | — |
| `rt > rθ` | literal | 1 / 1 |
| `rk > rx` | literal | 1 / 1 |
| `mp > mf` | literal | — |
| `nt > nθ` | literal | 11 / 11 |
| `ŋk > ŋx` | literal | 1 / 1 |
| `pp > ff` | literal | — |
| `pt > pθ` | literal | 2 / 2 |
| `-pt > -fθ` | literal | 1 / 1 |
| `tt > θθ` | literal | 7 / 7 |
| `kt > kθ` | literal | 4 / 3 |
| `-kt > -xθ` | literal | 4 / 1 |
| `xt > xθ` | literal | 4 / 4 |
| `kk > xx` | literal | 3 / 3 |
| `ɣt > ɣθ` | literal | 1 / 1 |
| `ɣt > ɣð` | literal | 1 / 1 |
| `gð > ɣð` | literal | — |
| `kð > ɣð` | literal | 1 / 1 |
| `vt > vθ` | literal | 1 / 1 |

### [[ts] became [s] after long vowel](https://eldamo.org/content/words/word-1209928251.html)

- порядок 03700
- общая формула `VVts > VVs`
- раньше, чем: [p], [t], [k] usually spirantalized with following [s]
- вариант правила [[p], [t], [k] spirantalized before [s]](https://eldamo.org/content/words/word-1682758275.html)

| подформула | вид | примеры |
|---|---|---|
| `VVts > VVs` | contextual | 1 / 0 |
| `wets > wess` | literal | 1 / 0 |

### [[p], [t], [k] usually spirantalized with following [s]](https://eldamo.org/content/words/word-1497090471.html)

- порядок 03800
- общая формула `{ptk}s > {fθx}ø`
- позже, чем: [ts] became [s] after long vowel
- вариант правила [[p], [t], [k] spirantalized before [s]](https://eldamo.org/content/words/word-1682758275.html)

| подформула | вид | примеры |
|---|---|---|
| `ps > f` | literal | — |
| `ts > θ` | literal | 1 / 1 |
| `ks > x` | literal | 1 / 0 |
| `ks > xs` | literal | — |

### [[x], [ɣ] sometimes became [i]](https://eldamo.org/content/words/word-272028599.html)

- порядок 03900
- общая формула `{xɣ} > i`
- раньше, чем: final voiceless spirants restopped after consonants
- вариант правила [[x], [ɸ] vocalized between a vowel and [s], [θ]](https://eldamo.org/content/words/word-297940333.html)

| подформула | вид | примеры |
|---|---|---|
| `axC > aiC` | contextual | 1 / 1 |
| `exC > eiC` | contextual | 8 / 8 |
| `oxC > oiC` | contextual | 3 / 3 |
| `-ax > -ai` | literal | 1 / 1 |
| `aɣC > aiC` | contextual | 4 / 4 |
| `eɣC > eiC` | contextual | 1 / 1 |
| `uɣC > uiC` | contextual | 1 / 1 |
| `-aɣ > -ai` | literal | 1 / 1 |
| `-uɣ > -ui` | literal | 1 / 1 |

### [[oi] became [ui]](https://eldamo.org/content/words/word-1684892745.html)

- порядок 04000
- общая формула `oi > ui`
- позже, чем: [ei], [ou] became [ē], [ō]
- вариант правила [2638900527](https://eldamo.org/content/words/word-2638900527.html)

| подформула | вид | примеры |
|---|---|---|
| `oi > ui` | literal | 9 / 9 |

### [[f], [v] sometimes became [u]](https://eldamo.org/content/words/word-3096214821.html)

- порядок 04100
- общая формула `{fv} > u`
- раньше, чем: final voiceless spirants restopped after consonants
- вариант правила [[x], [ɸ] vocalized between a vowel and [s], [θ]](https://eldamo.org/content/words/word-297940333.html)

| подформула | вид | примеры |
|---|---|---|
| `afθ > auθ` | literal | 1 / 1 |
| `avk > auk` | literal | 2 / 2 |
| `avm > aum` | literal | 1 / 0 |
| `avs > aus` | literal | 4 / 4 |
| `avθ > auθ` | literal | 1 / 1 |

### [later [ei] became [ai]](https://eldamo.org/content/words/word-3272158349.html)

- порядок 04200
- вариант правила [[ei] (sometimes) became [ai] in final syllables](https://eldamo.org/content/words/word-3775120039.html)

| подформула | вид | примеры |
|---|---|---|
| `ei > ai` | literal | 9 / 9 |

### [final voiceless spirants restopped after consonants](https://eldamo.org/content/words/word-3441987869.html)

- порядок 04300
- общая формула `-C{fθx} > -C{ptk}`
- раньше, чем: [ð] became [θ] finally or before a consonant
- позже, чем: [f], [v] sometimes became [u]; [x], [ɣ] sometimes became [i]
- вариант правила [final [mf], [nθ], [ŋx], [lθ] became [mp], [nt], [ŋk], [lt]](https://eldamo.org/content/words/word-1735735423.html)

| подформула | вид | примеры |
|---|---|---|
| `-Cf > -Cp` | contextual | — |
| `-Cθ > -Ct` | contextual | 14 / 14 |
| `-Cx > -Ck` | contextual | 4 / 3 |
| `-Cf > -Cf` | contextual | — |
| `-Cθ > -Cθ` | contextual | — |
| `-Cx > -Cx` | contextual | 1 / 0 |

### [[nð] became [nd]](https://eldamo.org/content/words/word-738701133.html)

- порядок 04400

| подформула | вид | примеры |
|---|---|---|
| `nð > nd` | literal | 6 / 6 |

### [[nx] became [nθ]](https://eldamo.org/content/words/word-2274919337.html)

- порядок 04500

| подформула | вид | примеры |
|---|---|---|
| `nx > nθ` | literal | 1 / 1 |

### [[mβ] became [mb]](https://eldamo.org/content/words/word-1610556241.html)

- порядок 04600
- раньше, чем: [nd] generally became [nn], while [mb] became [m] finally
- вариант правила [[mb], [nd] became [mm], [nn]](https://eldamo.org/content/words/word-1317326183.html)

| подформула | вид | примеры |
|---|---|---|
| `mβ > mb` | literal | 1 / 1 |

### [[nd] generally became [nn], while [mb] became [m] finally](https://eldamo.org/content/words/word-2845062117.html)

- порядок 04700
- общая формула `n{dð}|-mb > nn|m`
- позже, чем: [mβ] became [mb]
- вариант правила [[mb], [nd] became [mm], [nn]](https://eldamo.org/content/words/word-1317326183.html)

| подформула | вид | примеры |
|---|---|---|
| `nd > nn` | literal | 12 / 11 |
| `nd > nd` | identity | 1 / 0 |
| `-mb > -m` | literal | 3 / 3 |

### [[ld] became [ll]](https://eldamo.org/content/words/word-931729579.html)

- порядок 04800
- раньше, чем: [ll] became [l] lengthening preceding stressed vowel; [lð] became [ld] medially, [l] finally
- вариант правила [[lð] became [ll] or [lt]](https://eldamo.org/content/words/word-3316520435.html)

| подформула | вид | примеры |
|---|---|---|
| `ld > ll` | literal | 7 / 7 |

### [[ll] became [l] lengthening preceding stressed vowel](https://eldamo.org/content/words/word-711485671.html)

- порядок 04900
- общая формула `ll|V́ll > l|V̄l`
- позже, чем: [ē], [ō] became [ī], [ū]; [ld] became [ll]; [ā] became [ō]
- вариант правила [final [ll], [nn], [ss] shortened in polysyllables](https://eldamo.org/content/words/word-2559778861.html)

| подформула | вид | примеры |
|---|---|---|
| `ll > l` | literal | 1 / 1 |
| `áll > āl` | literal | 3 / 3 |
| `óll > ōl` | literal | 1 / 1 |

### [final [nn], [ss] shortened in polysyllables](https://eldamo.org/content/words/word-2881686067.html)

- порядок 05000
- общая формула `-SS{nn|ss} > -SS{n|s}`
- вариант правила [final [ll], [nn], [ss] shortened in polysyllables](https://eldamo.org/content/words/word-2559778861.html)

| подформула | вид | примеры |
|---|---|---|
| `-SSnn > -SSn` | contextual | 3 / 2 |
| `-SSss > -SSs` | contextual | 1 / 1 |

### [[a], [u] became [o] in final unstressed closed syllable](https://eldamo.org/content/words/word-1152095659.html)

- порядок 05100
- общая формула `-ˌ{au}C > -oC`
- вариант правила [short [u] often became [o]](https://eldamo.org/content/words/word-1228910977.html)

| подформула | вид | примеры |
|---|---|---|
| `-ˌaC > -oC` | contextual | 7 / 6 |
| `-ˌuC > -oC` | contextual | 4 / 3 |

### [[lð] became [ld] medially, [l] finally](https://eldamo.org/content/words/word-3105939935.html)

- порядок 05200
- общая формула `lð|-lð > ld|-l`
- позже, чем: [ld] became [ll]
- вариант правила [[lð] became [ll] or [lt]](https://eldamo.org/content/words/word-3316520435.html)

| подформула | вид | примеры |
|---|---|---|
| `lð > ld` | literal | 1 / 1 |
| `-lð > -l` | literal | 2 / 2 |
| `rð > rd` | literal | — |

### [[tl], [dl], [ðl] became [kl], [gl]](https://eldamo.org/content/words/word-3113057765.html)

- порядок 05300
- общая формула `tl|{dð}l > kl|gl`
- раньше, чем: voiceless stops mostly voiced after vowels
- позже, чем: initial [n], [m] became [d], [b] before [l], [r]
- вариант правила [[tl], [dl] became [kl], [gl]](https://eldamo.org/content/words/word-2165755085.html)

| подформула | вид | примеры |
|---|---|---|
| `dl > gl` | literal | 2 / 2 |
| `ðl > gl` | literal | 3 / 2 |
| `tl > kl` | literal | 3 / 3 |

### [voiced stops became spirants after vowels](https://eldamo.org/content/words/word-3492748191.html)

- порядок 05400
- общая формула `V{bdg} > V{vðɣ}`
- вариант правила [1901523613](https://eldamo.org/content/words/word-1901523613.html)

| подформула | вид | примеры |
|---|---|---|
| `Vb > Vv` | contextual | — |
| `Vd > Vð` | contextual | 1 / 1 |
| `Vg > Vɣ` | contextual | 2 / 2 |

### [voiceless stops mostly voiced after vowels](https://eldamo.org/content/words/word-1463657717.html)

- порядок 05500
- общая формула `V{ptk}|{pk}θ > V{bdg}|{pk}θ`
- позже, чем: [tl], [dl], [ðl] became [kl], [gl]
- вариант правила [3477429555](https://eldamo.org/content/words/word-3477429555.html)

| подформула | вид | примеры |
|---|---|---|
| `Vp > Vb` | contextual | 9 / 9 |
| `Vt > Vd` | contextual | 17 / 16 |
| `Vk > Vg` | contextual | 15 / 14 |
| `pθ > pθ` | identity | 2 / 0 |
| `kθ > kθ` | identity | 3 / 0 |

### [intervocalic [x], [ɣ] vanished](https://eldamo.org/content/words/word-4134163671.html)

- порядок 05600
- общая формула `V{xɣ}V > VøV`
- вариант правила [[ɣ] otherwise vanished](https://eldamo.org/content/words/word-1058893297.html)

| подформула | вид | примеры |
|---|---|---|
| `VxV > VøV` | contextual | 1 / 1 |
| `VɣV > VøV` | contextual | 4 / 3 |

### [long voiceless spirants shortened](https://eldamo.org/content/words/word-4228274355.html)

- порядок 05700
- общая формула `ff|θθ|xx > f|θ|x`
- вариант правила [long voiceless spirants shortened](https://eldamo.org/content/words/word-2631001607.html)

| подформула | вид | примеры |
|---|---|---|
| `ff > f` | literal | — |
| `θθ > θ` | literal | 8 / 8 |
| `xx > x` | literal | 3 / 3 |

### [[s] became [θ] before [l], [r], [w]](https://eldamo.org/content/words/word-3455596725.html)

- порядок 05800
- общая формула `s{rlw} > θ{rlw}`
- раньше, чем: initial [θ] sometimes became [f] before [l], [r], [w]
- вариант правила [medial [s] became [θ] before [l], [r]](https://eldamo.org/content/words/word-2266682021.html)

| подформула | вид | примеры |
|---|---|---|
| `sl > θl` | literal | 2 / 2 |
| `sr > θr` | literal | — |
| `sw > θw` | literal | — |
| `tl > θl` | literal | 1 / 1 |

### [initial [θ] sometimes became [f] before [l], [r], [w]](https://eldamo.org/content/words/word-4288301617.html)

- порядок 05900
- общая формула `θ{rlw}- > f{rlw}-`
- позже, чем: [s] became [θ] before [l], [r], [w]
- вариант правила [initial [θl] sometimes became [fl]](https://eldamo.org/content/words/word-2640707457.html)

| подформула | вид | примеры |
|---|---|---|
| `θl- > fl-` | literal | — |
| `θr- > fr-` | literal | — |
| `θw- > fw-` | literal | — |

### [[sβ] became [θw]](https://eldamo.org/content/words/word-963622237.html)

- порядок 06000

| подформула | вид | примеры |
|---|---|---|
| `sβ > θw` | literal | — |

### [[sm], [sf] became [f]](https://eldamo.org/content/words/word-1586615947.html)

- порядок 06100
- общая формула `sm|sf > f`

| подформула | вид | примеры |
|---|---|---|
| `sm > f` | literal | 2 / 2 |
| `sf > f` | literal | 1 / 1 |

### [final [θ] sometimes became [s]](https://eldamo.org/content/words/word-49608021.html)

- порядок 06200
- раньше, чем: [ð] became [θ] finally or before a consonant

| подформула | вид | примеры |
|---|---|---|
| `-θ > -s` | literal | 1 / 1 |

### [[ð] became [θ] finally or before a consonant](https://eldamo.org/content/words/word-3786037189.html)

- порядок 06300
- общая формула `-ð|ðC > -θ|θC`
- позже, чем: final voiceless spirants restopped after consonants; final [θ] sometimes became [s]

| подформула | вид | примеры |
|---|---|---|
| `-ð > -θ` | literal | 7 / 7 |
| `ðC > θC` | contextual | 1 / 1 |

### [initial nasals vanished before stops](https://eldamo.org/content/words/word-2825088365.html)

- порядок 06400
- общая формула `{mb|nd|ŋg}- > {bdg}-`
- вариант правила [initial nasals vanished before stops](https://eldamo.org/content/words/word-956128961.html)

| подформула | вид | примеры |
|---|---|---|
| `mb- > b-` | literal | 7 / 7 |
| `nd- > d-` | literal | 14 / 14 |
| `ŋg- > g-` | literal | 4 / 4 |

### [initial [l], [r] sometimes strengthened to [gl], [gr]](https://eldamo.org/content/words/word-3606177509.html)

- порядок 06500
- общая формула `{lr}- > g{lr}-`

| подформула | вид | примеры |
|---|---|---|
| `l- > gl-` | literal | 2 / 2 |
| `r- > gr-` | literal | — |

### [final [nw], [lw], [tw] became [m], [lb], [du]](https://eldamo.org/content/words/word-1704662033.html)

- порядок 06600

| подформула | вид | примеры |
|---|---|---|
| `-lw > -lb` | literal | 2 / 2 |

### [final [nw] became [m]](https://eldamo.org/content/words/word-4173802635.html)

- порядок 06700

| подформула | вид | примеры |
|---|---|---|
| `-nw > -m` | literal | 4 / 4 |

### [final [w] usually became [u]](https://eldamo.org/content/words/word-1139075853.html)

- порядок 06800
- вариант правила [final [w] usually became [u]](https://eldamo.org/content/words/word-1104843109.html)

| подформула | вид | примеры |
|---|---|---|
| `-Cw > -Cu` | contextual | 1 / 1 |

### [[ae] became [ai]](https://eldamo.org/content/words/word-3505973729.html)

- порядок 06900
- вариант правила [[ai] became [oe] or [ae]](https://eldamo.org/content/words/word-3173115217.html)

| подформула | вид | примеры |
|---|---|---|
| `ae > ai` | literal | 2 / 2 |

## Цепочки с оценками A и B

### A — засвидетельствована в одной деривации

- рання. `tt → θθ → θ` (G., G.) — 7 дерив.
- рання. `nð → nd → nn` (G., G.) — 4 дерив.
- рання. `ŋ → ŋg → g` (G., G.) — 4 дерив.
- рання. `kk → xx → x` (G., G.) — 3 дерив.
- рання. `sj → x → h` (G., G.) — 3 дерив.
- рання. `ld → ll → l` (G., G.) — 1 дерив.
- рання. `mβ → mb → m` (G., G.) — 1 дерив.
- рання. `nl → dl → gl` (G., G.) — 1 дерив.
- рання. `θʲ → x → h` (G., G.) — 1 дерив.
- поздн. `ā → ǭ → au` (OS., S.) — 65 дерив.
- поздн. `pʰ → ɸ → f` (OS., S.) — 49 дерив.
- поздн. `ǭ → au → o` (S., S.) — 34 дерив.
- поздн. `ā → ǭ → au → o` (OS., S., S.) — 34 дерив.
- поздн. `mb → mm → m` (S., S.) — 26 дерив.
- поздн. `kʰ → x → h` (OS., S.) — 21 дерив.
- поздн. `ttʰ → θθ → θ` (OS., S.) — 18 дерив.
- поздн. `kt → ktʰ → xθ` (OS., OS.) — 17 дерив.
- поздн. `tt → ttʰ → θθ` (OS., OS.) — 16 дерив.
- поздн. `tt → ttʰ → θθ → θ` (OS., OS., S.) — 16 дерив.
- поздн. `eu → iu → ȳ` (OS., S.) — 8 дерив.
- поздн. `ld → lð → ll` (S., S.) — 8 дерив.
- поздн. `ǭi → oi → oe` (OS., S.) — 7 дерив.
- поздн. `sp → sɸ → ɸ` (OS., S.) — 5 дерив.
- поздн. `st → sθ → θ` (OS., S.) — 5 дерив.
- поздн. `sɸ → ɸ → f` (S., S.) — 5 дерив.
- поздн. `sp → sɸ → ɸ → f` (OS., S., S.) — 5 дерив.
- поздн. `pp → ppʰ → ɸɸ` (OS., OS.) — 4 дерив.
- поздн. `gt → kt → ktʰ` (✶, OS.) — 3 дерив.
- поздн. `j̊ → x → h` (S., S.) — 3 дерив.
- поздн. `kk → kkʰ → xx` (OS., OS.) — 3 дерив.
- поздн. `kkʰ → xx → x` (OS., S.) — 3 дерив.
- поздн. `sj → j̊ → x` (OS., S.) — 3 дерив.
- поздн. `ŋkw → mp → mpʰ` (AT., OS.) — 3 дерив.
- поздн. `gt → kt → ktʰ → xθ` (✶, OS., OS.) — 3 дерив.
- поздн. `kk → kkʰ → xx → x` (OS., OS., S.) — 3 дерив.
- поздн. `sj → j̊ → x → h` (OS., S., S.) — 3 дерив.
- поздн. `sj → xʲ → ix` (OS., S.) — 2 дерив.
- поздн. `tk → kk → kkʰ` (✶, OS.) — 2 дерив.
- поздн. `tp → pp → ppʰ` (✶, OS.) — 2 дерив.
- поздн. `ts → θθ → θ` (OS., S.) — 2 дерив.
- поздн. `ðm → ðv → ðw` (S., S.) — 2 дерив.
- поздн. `ŋgw → mb → b` (AT., S.) — 2 дерив.
- поздн. `tk → kk → kkʰ → xx` (✶, OS., OS.) — 2 дерив.
- поздн. `tp → pp → ppʰ → ɸɸ` (✶, OS., OS.) — 2 дерив.
- поздн. `ad → ā → ǭ` (OS., OS.) — 1 дерив.
- поздн. `ai → ae → e` (S., S.) — 1 дерив.
- поздн. `km → mk → ŋk` (✶, ✶) — 1 дерив.
- поздн. `ks → xx → x` (OS., S.) — 1 дерив.
- поздн. `kʰj → kʰ → x` (OS., OS.) — 1 дерив.
- поздн. `mt → nt → ntʰ` (✶, OS.) — 1 дерив.
- поздн. `ov → ou → au` (S., S.) — 1 дерив.
- поздн. `pt → ptʰ → ɸθ` (OS., OS.) — 1 дерив.
- поздн. `sn → n̥ → n` (OS., S.) — 1 дерив.
- поздн. `ō → ū → u` (S., S.) — 1 дерив.
- поздн. `ad → ā → ǭ → au` (OS., OS., S.) — 1 дерив.
- поздн. `kʰj → kʰ → x → h` (OS., OS., S.) — 1 дерив.
- средн. `ǭ → ou → au` (N., N.) — 75 дерив.
- средн. `kʰ → x → h` (ON., N.) — 50 дерив.
- средн. `ā → ǭ → ou` (ON., N.) — 37 дерив.
- средн. `ā → ǭ → ou → au` (ON., N., N.) — 37 дерив.
- средн. `pʰ → ɸ → f` (ON., N.) — 33 дерив.
- средн. `mb → mm → m` (N., N.) — 30 дерив.
- средн. `tt → ttʰ → θθ` (ON., ON.) — 26 дерив.
- средн. `ttʰ → θθ → θ` (ON., N.) — 26 дерив.
- средн. `kt → ktʰ → xθ` (ON., ON.) — 23 дерив.
- средн. `tt → ttʰ → θθ → θ` (ON., ON., N.) — 23 дерив.
- средн. `au → ǭ → ou` (ON., N.) — 20 дерив.
- средн. `ou → au → o` (N., N.) — 19 дерив.
- средн. `ǭ → ou → au → o` (N., N., N.) — 18 дерив.
- средн. `sx → x → h` (N., N.) — 12 дерив.
- средн. `sɸ → ɸ → f` (N., N.) — 11 дерив.
- средн. `ld → lð → ll` (N., N.) — 10 дерив.
- средн. `st → sθ → θ` (ON., N.) — 8 дерив.
- средн. `ts → θθ → θ` (ON., N.) — 8 дерив.
- средн. `sk → sx → x` (ON., N.) — 7 дерив.
- средн. `sp → sɸ → ɸ` (ON., N.) — 7 дерив.
- средн. `ē → ī → i` (ON., N.) — 7 дерив.
- средн. `sk → sx → x → h` (ON., N., N.) — 7 дерив.
- средн. `sp → sɸ → ɸ → f` (ON., N., N.) — 7 дерив.
- средн. `ŋgw → mb → mm` (ON., N.) — 6 дерив.
- средн. `j̊ → x → h` (N., N.) — 5 дерив.
- средн. `kk → kkʰ → xx` (ON., ON.) — 5 дерив.
- средн. `kkʰ → xx → x` (ON., N.) — 5 дерив.
- средн. `sn → n̥ → n` (ON., N.) — 5 дерив.
- средн. `kk → kkʰ → xx → x` (ON., ON., N.) — 5 дерив.
- средн. `ŋgw → mb → mm → m` (ON., N., N.) — 5 дерив.
- средн. `kʰj → kʰ → x` (ON., ON.) — 4 дерив.
- средн. `sj → j̊ → x` (ON., N.) — 4 дерив.
- средн. `sw → w̥ → xw` (ON., N.) — 4 дерив.
- средн. `ŋkw → mp → mpʰ` (ON., ON.) — 4 дерив.
- средн. `ŋw → ŋgw → mb` (ᴹ✶, ON.) — 4 дерив.
- средн. `sj → j̊ → x → h` (ON., N., N.) — 4 дерив.
- средн. `ad → ā → ǭ` (ON., ON.) — 3 дерив.
- средн. `km → gm → ŋm` (ON., ON.) — 3 дерив.
- средн. `ŋgw → mb → b` (ON., N.) — 3 дерив.
- средн. `ō → ū → u` (ON., N.) — 3 дерив.
- средн. `kʰj → kʰ → x → h` (ON., ON., N.) — 3 дерив.
- средн. `ŋw → ŋgw → mb → mm` (ᴹ✶, ON., N.) — 3 дерив.
- средн. `dm → nm → nw` (ON., N.) — 2 дерив.
- средн. `ld → lð → lt` (N., N.) — 2 дерив.
- средн. `pp → ppʰ → ɸɸ` (ON., ON.) — 2 дерив.
- средн. `tk → kk → kkʰ` (ᴹ✶, ON.) — 2 дерив.
- средн. `tn → dn → nn` (ON., ON.) — 2 дерив.
- средн. `ǣ → ai → ae` (ON., N.) — 2 дерив.
- средн. `ɣn → gn → ŋn` (ON., ON.) — 2 дерив.
- средн. `tk → kk → kkʰ → xx` (ᴹ✶, ON., ON.) — 2 дерив.
- средн. `ai → ae → e` (N., N.) — 1 дерив.
- средн. `ds → ts → θθ` (ᴹ✶, ON.) — 1 дерив.
- средн. `ei → ī → i` (ON., N.) — 1 дерив.
- средн. `eu → io → ui` (ON., N.) — 1 дерив.
- средн. `gt → kt → ktʰ` (ᴹ✶, ON.) — 1 дерив.
- средн. `ht → tt → ttʰ` (ON., ON.) — 1 дерив.
- средн. `kn → gn → ŋn` (ON., ON.) — 1 дерив.
- средн. `kʰs → ks → xs` (ᴹ✶, ON.) — 1 дерив.
- средн. `mt → nt → ntʰ` (ᴹ✶, ON.) — 1 дерив.
- средн. `pn → bn → mn` (ON., ON.) — 1 дерив.
- средн. `skj → sk → sx` (ON., ON.) — 1 дерив.
- средн. `sl → θl → fl` (ON., N.) — 1 дерив.
- средн. `sm → mm → m` (ON., N.) — 1 дерив.
- средн. `sm → m̥ → m` (ON., N.) — 1 дерив.
- средн. `tm → dm → nm` (ON., ON.) — 1 дерив.
- средн. `tp → pp → ppʰ` (ᴹ✶, ON.) — 1 дерив.
- средн. `tʰn → ttʰ → θθ` (ON., ON.) — 1 дерив.
- средн. `ŋj → ŋgj → ŋg` (ᴹ✶, ON.) — 1 дерив.
- средн. `ǣ → ai → oe` (ON., N.) — 1 дерив.
- средн. `ɣm → gm → ŋm` (ON., ON.) — 1 дерив.
- средн. `ɣs → hs → ss` (ᴹ✶, ᴹ✶) — 1 дерив.
- средн. `ds → ts → θθ → θ` (ᴹ✶, ON., N.) — 1 дерив.
- средн. `gt → kt → ktʰ → xθ` (ᴹ✶, ON., ON.) — 1 дерив.
- средн. `ht → tt → ttʰ → θθ` (ON., ON., ON.) — 1 дерив.
- средн. `tm → dm → nm → nw` (ON., ON., N.) — 1 дерив.
- средн. `tp → pp → ppʰ → ɸɸ` (ᴹ✶, ON., ON.) — 1 дерив.

### B — шаги засвидетельствованы, порядок подтверждён

- рання. `dh → θ → s` (G., G.)
- рання. `gt → kt → kθ` (ᴱ✶, G.)
- рання. `gt → kt → xθ` (ᴱ✶, G.)
- рання. `ll → l → gl` (G., G.)
- рання. `md → nd → d` (ᴱ✶, G.)
- рання. `md → nd → nn` (ᴱ✶, G.)
- рання. `mt → nt → nθ` (ᴱ✶, G.)
- рання. `mβ → mb → b` (G., G.)
- рання. `nb → mb → b` (ᴱ✶, G.)
- рання. `nb → mb → m` (ᴱ✶, G.)
- рання. `nk → ŋk → ŋx` (ᴱ✶, G.)
- рання. `nð → nd → d` (G., G.)
- рання. `ts → θ → s` (G., G.)
- рання. `ī → ai → ē` (G., G.)
- рання. `θθ → θ → s` (G., G.)
- рання. `ld → ll → l → gl` (G., G., G.)
- рання. `tt → θθ → θ → s` (G., G., G.)
- поздн. `awa → au → o` (S., S.)
- поздн. `bm → mb → b` (✶, S.)
- поздн. `bm → mb → mm` (✶, S.)
- поздн. `bt → pt → ptʰ` (✶, OS.)
- поздн. `dn → nd → d` (✶, S.)
- поздн. `dn → nd → nn` (✶, S.)
- поздн. `ei → ī → i` (OS., S.)
- поздн. `kd → kt → ktʰ` (✶, OS.)
- поздн. `kʰk → kkʰ → xx` (✶, OS.)
- поздн. `kʰt → ktʰ → xθ` (✶, OS.)
- поздн. `md → nd → d` (✶, S.)
- поздн. `md → nd → nn` (✶, S.)
- поздн. `mk → ŋk → ŋkʰ` (✶, OS.)
- поздн. `nb → mb → b` (✶, S.)
- поздн. `nb → mb → mm` (✶, S.)
- поздн. `nk → ŋk → ŋkʰ` (✶, OS.)
- поздн. `np → mp → mpʰ` (✶, OS.)
- поздн. `ou → ū → u` (OS., S.)
- поздн. `sd → st → sθ` (✶, OS.)
- поздн. `sg → zg → ðɣ` (✶, S.)
- поздн. `w → u → o` (✶, S.)
- поздн. `wa → wo → o` (✶, S.)
- поздн. `ē → ī → i` (S., S.)
- поздн. `ŋ → ɣ → ø` (✶, S.)
- поздн. `ŋgw → mb → mm` (AT., S.)
- поздн. `ŋw → ŋgw → mb` (✶, AT.)
- поздн. `ŋŋ → ŋg → g` (✶, S.)
- поздн. `ŋŋ → ŋg → ŋ` (✶, S.)
- поздн. `bm → mb → mm → m` (✶, S., S.)
- поздн. `bt → pt → ptʰ → ɸθ` (✶, OS., OS.)
- поздн. `kd → kt → ktʰ → xθ` (✶, OS., OS.)
- поздн. `kʰk → kkʰ → xx → x` (✶, OS., S.)
- поздн. `nb → mb → mm → m` (✶, S., S.)
- поздн. `sd → st → sθ → θ` (✶, OS., S.)
- поздн. `ŋgw → mb → mm → m` (AT., S., S.)
- поздн. `ŋw → ŋgw → mb → mm` (✶, AT., S.)
- средн. `ai → ę̄ → ae` (ON., N.)
- средн. `dn → nd → d` (ᴹ✶, N.)
- средн. `dn → nd → nn` (ᴹ✶, N.)
- средн. `eu → ū → u` (ON., N.)
- средн. `io → ui → y` (N., N.)
- средн. `iu → ū → u` (ON., N.)
- средн. `jui → ui → y` (ON., N.)
- средн. `ls → lθ → lt` (N., N.)
- средн. `md → nd → d` (ᴹ✶, N.)
- средн. `md → nd → nn` (ᴹ✶, N.)
- средн. `mf → mm → m` (N., N.)
- средн. `nb → mb → b` (ᴹ✶, N.)
- средн. `nb → mb → mm` (ᴹ✶, N.)
- средн. `nk → ŋk → ŋkʰ` (ᴹ✶, ON.)
- средн. `np → mp → mpʰ` (ᴹ✶, ON.)
- средн. `oi → ui → y` (ON., N.)
- средн. `sg → zg → ig` (ᴹ✶, ON.)
- средн. `skj → sk → sg` (ON., N.)
- средн. `tk → kt → ktʰ` (ᴹ✶, ON.)
- средн. `tʰs → ts → θθ` (ᴹ✶, ON.)
- средн. `tʰt → ttʰ → θθ` (ᴹ✶, ON.)
- средн. `uiv → ui → y` (N., N.)
- средн. `uiw → ui → y` (N., N.)
- средн. `wu → u → o` (ON., N.)
- средн. `ę̄ → ae → e` (N., N.)
- средн. `ŋ → ɣ → ø` (ᴹ✶, ON.)
- средн. `ŋgj → ŋg → g` (ON., N.)
- средн. `ŋgj → ŋg → ŋ` (ON., N.)
- средн. `ŋŋ → ŋg → g` (ᴹ✶, N.)
- средн. `ŋŋ → ŋg → ŋ` (ᴹ✶, N.)
- средн. `ŋɣ → ŋg → g` (ᴹ✶, N.)
- средн. `ŋɣ → ŋg → ŋ` (ᴹ✶, N.)
- средн. `ǣ → ai → ę̄` (ON., ON.)
- средн. `ǭi → ui → y` (ON., N.)
- средн. `ad → ā → ǭ → ou` (ON., ON., N.)
- средн. `ai → ę̄ → ae → e` (ON., N., N.)
- средн. `eu → io → ui → y` (ON., N., N.)
- средн. `nb → mb → mm → m` (ᴹ✶, N., N.)
- средн. `skj → sk → sx → x` (ON., ON., N.)
- средн. `tk → kt → ktʰ → xθ` (ᴹ✶, ON., ON.)
- средн. `tʰn → ttʰ → θθ → θ` (ON., ON., N.)
- средн. `tʰs → ts → θθ → θ` (ᴹ✶, ON., N.)
- средн. `tʰt → ttʰ → θθ → θ` (ᴹ✶, ON., N.)
- средн. `ǣ → ai → ae → e` (ON., N., N.)
- средн. `ǣ → ai → ę̄ → ae` (ON., ON., N.)
