# Project Musti Backend

Api voor het ophalen van de musti data.

Run de applicatie via `python -m uvicorn main:app` dit zorgt ervoor dat de FastApi start. Om de 60 seconden zal het programma checken of er nieuwe files beschikbaar zijn. Indien deze er zijn zal hij alles inladen en een model trainen.

OPGEPAST: Bij het uploaden van nieuwe files volg je steeds het juiste bestandsysteem (namen van folders). Anders zal het programma niet correct trainen.

### Beschrijving model
- Snelste om te trainen
- Hoogste accuracy

### Beschrijving hyperparameters:
- Gevonden met HalvingGridSearchCV

- Het aantal estimators 185 is gekozen als het middeste getal uit een kleine range die optimaal bleek te zijn uit de HalvingGridSearchCV-testen.

- Het aantal max_features 11 gaf het beste resultaat bij 185 estimators

- De overige hyperparameters bleken weinig positief effect te hebben. Eventueel met veel tijd zou het mogelijk zijn om deze voor iedere hyperparameter perfect juist te stellen, maar door de exponentiele natuur van het testen zou dit enkele dagen kunnen innemen. Daarom hebben we het gehouden bij de parameters die het meeste invloed bleken te hebben.

### Interessante vaststellingen
- Ookal zou het gelijkstellen van de klassen betere resultaten moeten geven, is dit hier niet het geval. Dit is hoogstwaarschijnlijk het gevolg van onvoldoende trainingsdata in 1 van de klassen.

- Ondanks een gelijke random_state, viel het op dat de resultaten van de HalvingGridSearchCV varieren per test. Hierdoor kunnen we wel een 'optimale range' van hyperparameters vinden, maar voor parameters als 'n_estimators' kon het geen perfect aantal estimators vinden