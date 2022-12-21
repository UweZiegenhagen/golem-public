def berechne_jaehrliche_Annuitaet(kreditsumme, zinssatz, tilgung):
    """ Berechnet die _jährliche_ Annuität.
        Jährliche_Rate = (nominalzins + tilgungssatz) * Kreditsumme
        Quelle: https://de.wikipedia.org/wiki/Annuit%C3%A4tendarlehen
    """

    return round((zinssatz + tilgung) * kreditsumme, 2)

def tilgungsplan(kreditsumme, zinssatz, tilgung, jahre):

    annuitaet = berechne_jaehrliche_Annuitaet(kreditsumme, zinssatz, tilgung)
    print(f'{annuitaet=}\n')
    # Am Anfang entspricht die Restschuld der Kreditsumme
    restschuld = kreditsumme
    
    for j in range(1, jahre+1):
        zinsen = restschuld * zinssatz
        tilgung = restschuld if restschuld < annuitaet else annuitaet - zinsen    
        rate = zinsen + tilgung

        restschuld = restschuld - tilgung
        print(f'{rate:.2f} & {zinsen:.2f} & {tilgung:.2f}')
 
    
tilgungsplan(120000, 0.1, 0.25, 5)
    
