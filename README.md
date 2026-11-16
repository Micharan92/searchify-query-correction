# Searchify - correzione automatica delle query di ricerca

Correttore ortografico per un motore di ricerca aziendale. Se un utente scrive `raporto vendite 2023`, il sistema restituisce `rapporto vendite 2023` e la ricerca non va a vuoto.

Implementato in Python, senza librerie esterne: la distanza di edit è scritta da zero.

## Il problema

Searchify indicizza documenti interni (report, fatture, verbali, contratti). Una lettera fuori posto - una `p` mancante, due caratteri invertiti, una consonante doppia - produce zero risultati. L’utente non ha sbagliato l’intento, ha sbagliato la battitura. Il motore deve accorgersene prima di cercare.

## Cosa fa

La funzione `suggest_correction(query, dictionary)` confronta ogni parola della query con un dizionario di termini aziendali e, se serve, la sostituisce con la voce più vicina.

| Query digitata | Query corretta |
| --- | --- |
| `raporto` | `rapporto` |
| `clineti` | `clienti` |
| `fattuba` | `fattura` |
| `raporto vendite 2023` | `rapporto vendite 2023` |
| `verbale riunion progeto` | `verbale riunione progetto` |
| `budget annuale 2023` | `budget annuale 2023` |
| `BILANCIO` | `BILANCIO` |
| `xyz` | `xyz` |

Le ultime tre righe sono volute. Una query già valida resta invariata, il maiuscolo di una parola esatta viene conservato, e un termine troppo lontano dal dizionario non viene forzato.

## Come funziona

1. La query viene spezzata in parole. I numeri (anni, codici) restano così come sono.
2. Se ogni parola è già nel dizionario, la query torna indietro identica.
3. Per ogni refuso si calcola la distanza di edit verso tutte le voci del dizionario.
4. Vince la parola con distanza minima, ma solo se la distanza è al massimo 2. Oltre quella soglia la parola originale viene lasciata stare: correggere a tutti i costi introduce errori nuovi.

La distanza è una Levenshtein con un’operazione in più: lo scambio di due lettere vicine costa 1, come un singolo errore. `clineti` → `clienti` e `documneto` → `documento` sono refusi frequenti, e trattarli come due sostituzioni separate li allontanerebbe dalla parola giusta.

Operazioni considerate:

- inserimento di un carattere
- cancellazione di un carattere
- sostituzione di un carattere
- scambio di due caratteri consecutivi

Il dizionario contiene oltre 60 termini del dominio (fatture, contratti, magazzino, bilancio, scadenze) e sta nel codice, così l’algoritmo è eseguibile senza dipendenze.

## Scelte di progetto

- **Soglia a 2.** Un refuso vero è quasi sempre una o due operazioni. `xyz` non diventa `sede` solo perché è la voce meno lontana.
- **Confronto case-insensitive, output fedele all’input.** `BILANCIO` combacia con `bilancio` e viene restituito com’è stato scritto. La forma del dizionario entra in gioco solo quando c’è davvero una correzione.
- **Query intere, non parole isolate.** Si corregge token per token, così `raporto vendite 2023` sistema solo `raporto` e lascia intatti anno e parole già corrette.
- **Nessuna libreria per la distanza.** La matrice di programmazione dinamica è nel file, leggibile e modificabile.

## Esecuzione

Serve Python 3. Nessun `pip install`.

```bash
python correzione_motore_di_ricerca.py
```

Lo script lancia 13 casi: refusi singoli, scambi di lettere, query multi-parola, query già corrette, maiuscole e termini fuori dizionario. In console compare l’esito di ciascuno e il totale dei corretti.

## File

| File | Contenuto |
| --- | --- |
| `correzione_motore_di_ricerca.py` | Dizionario, distanza di edit, `suggest_correction`, test |

## Stack

Python 3 · libreria standard · distanza di Damerau-Levenshtein implementata a mano
