# Algoritmo di correzione per il motore di ricerca Searchify
# Confronto le parole della query con un dizionario e uso la distanza di edit
# (Levenshtein + scambio di due lettere vicine) per suggerire la correzione.

dizionario = [
    "rapporto", "vendite", "acquisti", "fattura", "fatture", "budget", "cliente",
    "clienti", "dipendente", "dipendenti", "documento", "documenti", "report",
    "contratto", "contratti", "riunione", "riunioni", "progetto", "progetti",
    "scadenza", "scadenze", "archivio", "inventario", "magazzino", "ordine",
    "ordini", "pagamento", "pagamenti", "bilancio", "contabilita", "risorse",
    "umane", "formazione", "marketing", "strategia", "analisi", "trimestrale",
    "annuale", "mensile", "presentazione", "verbale", "protocollo", "fornitore",
    "fornitori", "preventivo", "offerta", "catalogo", "prodotto", "prodotti",
    "servizio", "servizi", "qualita", "sicurezza", "privacy", "manuale",
    "procedura", "sede", "filiale", "fatturato", "obiettivo", "piano", "2023",
]


def calcola_distanza(a, b):
    # Distanza di Levenshtein: quante modifiche servono per passare da a a b
    # (inserire, cancellare o sostituire una lettera).
    # Aggiungo anche lo scambio di due caratteri consecutivi, perché
    # è un errore di battitura molto comune (es. "clineti" -> "clienti").
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(n + 1):
        dp[i][0] = i
    for j in range(m + 1):
        dp[0][j] = j

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            costo = 0 if a[i - 1] == b[j - 1] else 1
            canc = dp[i - 1][j] + 1
            ins = dp[i][j - 1] + 1
            sost = dp[i - 1][j - 1] + costo
            dp[i][j] = min(canc, ins, sost)

            if i > 1 and j > 1 and a[i - 1] == b[j - 2] and a[i - 2] == b[j - 1]:
                scambia = dp[i - 2][j - 2] + 1
                if scambia < dp[i][j]:
                    dp[i][j] = scambia

    return dp[n][m]


def suggest_correction(query, dictionary):
    # Se la query è già tutta nel dizionario la restituisco così com'è.
    # Altrimenti correggo solo le parole sbagliate, una per una.
    if query.strip() == "":
        return query

    parole = query.split()
    diz_low = [d.lower() for d in dictionary]

    valida = True
    for p in parole:
        # non prendo in considerazione i numeri (es. l'anno 2023), non sono parole da dizionario
        if p.lower() not in diz_low and not p.isdigit():
            valida = False
            break
    if valida:
        return query

    corrette = []
    for p in parole:
        if p.isdigit() or p.lower() in diz_low:
            corrette.append(p)
            continue

        # cerco la parola più simile nel dizionario
        migliore = p
        dmin = 99
        p_low = p.lower()
        for d in dictionary:
            nd = calcola_distanza(p_low, d.lower())
            if nd < dmin:
                migliore = d
                dmin = nd

        # se è troppo diversa non la forzo: probabilmente non è un refuso
        soglia = 2
        if dmin > soglia:
            corrette.append(p)
        else:
            corrette.append(migliore)

    return " ".join(corrette)


# blocco codice per testare la correzione delle query
if __name__ == "__main__":
    test = [
        ("raporto", "rapporto"),
        ("venditte", "vendite"),
        ("clineti", "clienti"),
        ("fattuba", "fattura"),
        ("rapporto", "rapporto"),
        ("raporto vendite 2023", "rapporto vendite 2023"),
        ("budget annuale 2023", "budget annuale 2023"),
        ("documneto", "documento"),
        ("progeto", "progetto"),
        ("contrtatto", "contratto"),
        ("BILANCIO", "BILANCIO"),
        ("verbale riunion progeto", "verbale riunione progetto"),
        ("xyz", "xyz"),
    ]

    print("Test correzione query")
    print("---------------------")
    ok = 0
    for q, atteso in test:
        out = suggest_correction(q, dizionario)
        esito = "OK" if out == atteso else "ERRORE"
        if esito == "OK":
            ok += 1
        print(q, "->", out, esito)

    print("---------------------")
    print("corretti:", ok, "su", len(test))
