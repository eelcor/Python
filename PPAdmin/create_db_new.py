# -*- coding: utf-8 -*-
"""
Created on Sat May 31 22:47:21 2014

@author: Eelco
"""

from app import db
from app import model
import datetime

db.create_all()
eelco = model.Gebruiker('eelco.rouw','cacivaysda')
marije = model.Gebruiker('marije.assink','Leiden79')
db.session.add(eelco)
db.session.add(marije)
db.session.commit()

testclient = model.Client(voornaam='Test', tussenvoegsel='', achternaam='Client')
testclient2 = model.Client(voornaam='Test2', tussenvoegsel='', achternaam='Client')
db.session.add(testclient)
db.session.add(testclient2)
db.session.commit()

eelco_pers = model.Client(voornaam=u'Eelco', tussenvoegsel=u'',achternaam=u'Rouw')
marije_pers = model.Client(voornaam=u'Marije José Willemijn', tussenvoegsel=u'', achternaam=u'Assink')
db.session.add(eelco_pers)
db.session.add(marije_pers)
db.session.commit()

wim = model.Verzorger(voornaam='Wim', tussenvoegsel='', achternaam='Rouw')
ida = model.Verzorger(voornaam='Ida', tussenvoegsel='', achternaam='Rouw-Runia')
eelco_pers.verzorgers.append(wim)
eelco_pers.verzorgers.append(ida)
db.session.add(eelco_pers)
db.session.commit()

eelco.profielen.append(eelco_pers)
marije.profielen.append(marije_pers)
db.session.add(eelco)
db.session.add(marije)
db.session.commit()

an = model.Annotatie('Test','Dit is een test')
a2 = model.Annotatie('Test 2','Dit is een tweede test')
marije_pers.annotaties.append(an)
marije_pers.annotaties.append(a2)
db.session.add(marije_pers)
db.session.commit()