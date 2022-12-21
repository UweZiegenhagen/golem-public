import pandas as pd

def berechne_monatliche_Annuitaet(kreditsumme, zinssatz, tilgung):
    """ Berechnet die _monatliche_ Annuität.
        Jährliche_Rate = (nominalzins + tilgungssatz) * Kreditsumme
        Monatliche_Rate = Jährliche_Rate / 12
    """ 
    return round(kreditsumme * (zinssatz + tilgung) / 12, 2)


def tilgungsplan(kreditsumme, zinssatz, tilgung, monate, sondertilgung):
    """
    Erstellt den Tilgungsplan als Excel
    """

    tilgplan = pd.DataFrame(columns=['Monat', 'Rate', 'Zinsen', 'Tilgung', 
                                  'Sondertilgung', 'Restschuld'])
    annuitaet = berechne_monatliche_Annuitaet(kreditsumme, zinssatz, tilgung)
    print(f'{annuitaet=}\n')
    # Am Anfang entspricht die Restschuld der Kreditsumme
    restschuld = kreditsumme
    
    for monat in range(1, monate+1):
        zinsen = restschuld * (zinssatz / 12 )
        tilgung = restschuld if restschuld < annuitaet else annuitaet - zinsen    
        rate = zinsen + tilgung
        restschuld = restschuld - tilgung
        
        wert_sondertilgung = 0.0
        
        # Sondertilgung berücksichtigen im Dezember
        if monat % 12 == 0 and restschuld > sondertilgung:
            restschuld = restschuld - sondertilgung
            wert_sondertilgung = sondertilgung
        elif monat % 12 == 0 and restschuld <= sondertilgung:
            wert_sondertilgung = restschuld
            restschuld = 0        
       
        
        zeile = pd.DataFrame([{'Monat':monat, 'Rate':rate, 'Zinsen':zinsen,
                               'Tilgung':tilgung, 'Sondertilgung': wert_sondertilgung,  
                               'Restschuld':restschuld}])
        
        tilgplan = pd.concat([tilgplan, zeile])

    tilgplan['Jahr'] = ((tilgplan['Monat'] - 1 ) // 12 ) + 1
    tilgplan=tilgplan.set_index(['Monat'])
    return tilgplan


tilgungsplan_mit_sondertilgung = tilgungsplan(45000, 0.0245, 0.04, 120, 2500)
tilgungsplan_ohne_sondertilgung = tilgungsplan(45000, 0.0245, 0.04, 250, 0)

zinsen_mit_Sondertilgung = round(tilgungsplan_mit_sondertilgung["Zinsen"].sum(),2)
zinsen_ohne_Sondertilgung = round(tilgungsplan_ohne_sondertilgung["Zinsen"].sum(),2)

print( f'{zinsen_mit_Sondertilgung} EUR Gesamtzinsen\n')
print( f'{zinsen_ohne_Sondertilgung} EUR Gesamtzinsen\n')

print( f'{round(zinsen_ohne_Sondertilgung - zinsen_mit_Sondertilgung,2)} EUR Zinsersparnis\n')


tilgungsplan_mit_sondertilgung.to_excel('tilgungsplan_mit_sondertilgung.xlsx')
tilgungsplan_ohne_sondertilgung.to_excel('tilgungsplan_ohne_sondertilgung.xlsx')
