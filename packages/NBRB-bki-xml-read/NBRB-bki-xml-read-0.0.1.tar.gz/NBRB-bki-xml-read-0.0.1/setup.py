from setuptools import setup

description='Collection of tools for reading bki.xml files provided by National Bank of the Republic of Belarus. Find out more on https://www.nbrb.by/today/creditregistry/instructions.'

setup(
    name='NBRB-bki-xml-read',
    version='0.0.1',
    description=description,
    packages=['NBRB_bki_xml_read'],
    author_email='kobfedsur@gmail.com',
    zip_safe=False,
    install_requires=["xmltodict"],
 )