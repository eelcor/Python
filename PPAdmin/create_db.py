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
beheerder = model.Autorisatie('beheerder')
db.session.add(eelco)
db.session.add(marije)
db.session.add(beheerder)
db.session.commit()
eelco_mat = model.Autorisatiematrix()
eelco_mat.gebruiker_id = eelco.id
eelco_mat.autorisatie_id = beheerder.id
marije_mat = model.Autorisatiematrix()
marije_mat.gebruiker_id = marije.id
marije_mat.autorisatie_id = beheerder.id
db.session.add(eelco_mat)
db.session.add(marije_mat)
db.session.commit()
testclient = model.Persoon('Test','','Client')
testclient2 = model.Persoon('Test2','','Client')
db.session.add(testclient)
db.session.add(testclient2)
db.session.commit()
post1 = model.Journaalitem('Dit is een test van een rapportage',datetime.datetime.now())
post2 = model.Journaalitem('Dit is ook een test van een rapportage',datetime.datetime.now())
post1.client_id = testclient.id
post1.auteur_id = marije.id
post2.client_id = testclient2.id
post2.auteur_id = eelco.id
db.session.add(post1)
db.session.add(post2)
db.session.commit()
eelco_pers = model.Persoon(u'Eelco', u' ',u'Rouw')
marije_pers = model.Persoon(u'Marije José Willemijn',u' ',u'Assink')
db.session.add(eelco_pers)
db.session.add(marije_pers)
db.session.commit()
eelco_user = model.Gebruikermatrix()
marije_user = model.Gebruikermatrix()
eelco_user.gebruiker_id = eelco.id
eelco_user.persoon_id = eelco_pers.id
marije_user.gebruiker_id = marije.id
marije_user.persoon_id = marije_pers.id
db.session.add(eelco_user)
db.session.add(marije_user)
db.session.commit()

