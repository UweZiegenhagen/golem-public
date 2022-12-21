def berechne_jaehrliche_Annuitaet(kreditsumme, zinssatz, tilgung):
    """ Berechnet die _jährliche_ Annuität.
        Jährliche_Rate = (nominalzins in proz + tilgungssatz in proz) * Kreditsumme
        Quelle: https://de.wikipedia.org/wiki/Annuit%C3%A4tendarlehen
    """ 

    return round((zinssatz + tilgung) * kreditsumme, 2)


def tilgungsplan(kreditsumme, zinssatz, tilgung, jahre):
    """
    Erstellt den Tilgungsplan und gibt ihn aus    
    """

    annuitaet = berechne_jaehrliche_Annuitaet(kreditsumme, zinssatz, tilgung)
    print(f'{annuitaet=}\n')
    # Am Anfang entspricht die Restschuld der Kreditsumme
    restschuld = kreditsumme
    
    for jahr in range(1, jahre+1):
        zinsen = restschuld * zinssatz
        tilgung = restschuld if restschuld <= annuitaet else annuitaet - zinsen    
        rate = zinsen + tilgung

        restschuld = restschuld - tilgung
        print(f'Jahr {jahr}: {rate=:.2f} : {zinsen=:.2f} : {tilgung=:.2f} : {restschuld=:.2f}')
 
    
tilgungsplan(120000, 0.1, 0.25, 4)
    
