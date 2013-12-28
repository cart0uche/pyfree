#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


setup(

    # le nom de votre bibliothèque, tel qu'il apparaitre sur pypi
    name='pyfree',

    # la version du code
    version="0.0.1",

    # Liste les packages à insérer dans la distribution
    packages=find_packages(),

    # nom
    author="cart0uche",

    # Une description courte
    description="Unofficial API that implements access to Freebox Server Révolution (http://dev.freebox.fr/sdk/os/)",

    # Une description longue, sera affichée pour présenter la lib
    # Généralement on dump le README ici
    long_description=open('README.md').read(),

    # Vous pouvez rajouter une liste de dépendances pour votre lib
    # et même préciser une version. A l'installation, Python essayera de
    # les télécharger et les installer.
    install_requires=['requests'],

    # Active la prise en compte du fichier MANIFEST.in
    include_package_data=True,

    # Une url qui pointe vers la page officielle
    url='https://github.com/cart0uche/pyfree',

    # Il est d'usage de mettre quelques metadata à propos de sa lib
    # Pour que les robots puissent facilement la classer.
    # La liste des marqueurs autorisées est longue, alors je vous
    # l'ai mise sur 0bin: http://is.gd/AajTjj
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 1 - Planning",
        "License :: OSI Approved",
        "Natural Language :: French",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2.7",
        "Topic :: Communications",
    ],

    # A fournir uniquement si votre licence n'est pas listée dans "classifiers"
    # ce qui est notre cas
    license="WTFPL",
)
