# -*- coding: utf-8 -*-
import dbmodel
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine('sqlite:///testdb.sqlite',connect_args={'check_same_thread':False})
Session = sessionmaker(bind=engine)
session = Session()

eelco = dbmodel.Client(Voornaam='Eelco', Achternaam='Rouw')
marije = dbmodel.Behandelaar(Voornaam='Marije',Achternaam='Assink')
elske = dbmodel.Behandelaar(Voornaam='Elske',Achternaam='Algra')
wim = dbmodel.Verzorger(Voornaam='Wim',Achternaam='Rouw')
ida = dbmodel.Verzorger(Voornaam='Ida',Achternaam='Rouw-Runia')
eelco.verzorgers.append(wim)
eelco.verzorgers.append(ida)
eelco.behandelaars.append(marije)
eelco.behandelaars.append(elske)
session.add(eelco)
session.commit()
