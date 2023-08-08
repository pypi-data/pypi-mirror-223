# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['whyqd',
 'whyqd.config',
 'whyqd.core',
 'whyqd.crosswalk',
 'whyqd.crosswalk.actions',
 'whyqd.crosswalk.base',
 'whyqd.crud',
 'whyqd.dtypes',
 'whyqd.models',
 'whyqd.parsers']

package_data = \
{'': ['*']}

install_requires = \
['modin>=0.20.1,<0.21.0',
 'numpy>=1.21.1,<2.0.0',
 'openpyxl>=3.0.7,<4.0.0',
 'pandas>=1.5.2,<2.0.0',
 'pyarrow>=11.0.0,<12.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'python-dotenv>=1.0.0,<2.0.0',
 'randomname>=0.2.1,<0.3.0',
 'ray>=2.2.0,<3.0.0',
 'setuptools>=67.7.2',
 'tabulate>=0.8.9,<0.9.0',
 'xlrd>=2.0.1,<3.0.0']

setup_kwargs = {
    'name': 'whyqd',
    'version': '1.0.3',
    'description': 'data wrangling simplicity, complete audit transparency, and at speed',
    'long_description': '# whyqd: simplicity, transparency, speed\n\n[![Documentation Status](https://readthedocs.org/projects/whyqd/badge/?version=latest)](docs/en/latest/?badge=latest)\n[![Build Status](https://travis-ci.com/whythawk/whyqd.svg?branch=master)](https://travis-ci.com/whythawk/whyqd.svg?branch=master)\n[![DOI](https://zenodo.org/badge/239159569.svg)](https://zenodo.org/badge/latestdoi/239159569)\n\n## What is it?\n\n> More research, less wrangling\n\n[**whyqd**](https://whyqd.com) (/wɪkɪd/) is a curatorial toolkit intended to produce well-structured and predictable \ndata for research analysis.\n\nIt provides an intuitive method for creating schema-to-schema crosswalks for restructuring messy data to conform to a \nstandardised metadata schema. It supports rapid and continuous transformation of messy data using a simple series of \nsteps. Once complete, you can import wrangled data into more complex analytical or database systems.\n\n**whyqd** plays well with your existing Python-based data-analytical tools. It uses [Ray](https://www.ray.io/) and \n[Modin](https://modin.readthedocs.io/) as a drop-in replacement for [Pandas](https://pandas.pydata.org/) to support \nprocessing of large datasets, and [Pydantic](https://pydantic-docs.helpmanual.io/) for data models. \n\nEach definition is saved as [JSON Schema-compliant](https://json-schema.org/) file. This permits others to read and \nscrutinise your approach, validate your methodology, or even use your crosswalks to import and transform data in \nproduction.\n\nOnce complete, a transform file can be shared, along with your input data, and anyone can import and validate your \ncrosswalk to verify that your output data is the product of these inputs.\n\n## Why use it?\n\n**whyqd** allows you to get to work without requiring you to achieve buy-in from anyone or change your existing code.\n\nIf you don\'t want to spend days or weeks slogging through data when all you want to do is test whether your source \ndata are even useful. If you already have a workflow and established software which includes Python and pandas, and \ndon\'t want to change your code every time your source data changes.\n\nIf you want to go from a [Cthulhu dataset](https://whyqd.readthedocs.io/en/latest/tutorials/tutorial3) like this:\n\n![UNDP Human Development Index 2007-2008: a beautiful example of messy data.](docs/images/undp-hdi-2007-8.jpg)\n*UNDP Human Development Index 2007-2008: a beautiful example of messy data.*\n\nTo this:\n\n|    | country_name           | indicator_name   | reference   |   year |   values |\n|:---|:-----------------------|:-----------------|:------------|:-------|:---------|\n|  0 | Hong Kong, China (SAR) | HDI rank         | e           |   2008 |       21 |\n|  1 | Singapore              | HDI rank         | nan         |   2008 |       25 |\n|  2 | Korea (Republic of)    | HDI rank         | nan         |   2008 |       26 |\n|  3 | Cyprus                 | HDI rank         | nan         |   2008 |       28 |\n|  4 | Brunei Darussalam      | HDI rank         | nan         |   2008 |       30 |\n|  5 | Barbados               | HDI rank         | e,g,f       |   2008 |       31 |\n\nWith a readable set of scripts to ensure that your process can be audited and repeated:\n\n```python\nschema_scripts = [\n    f"UNITE > \'reference\' < {REFERENCE_COLUMNS}",\n    "RENAME > \'country_name\' < [\'Country\']",\n    "PIVOT_LONGER > [\'indicator_name\', \'values\'] < [\'HDI rank\', \'HDI Category\', \'Human poverty index (HPI-1) - Rank;;2008\', \'Human poverty index (HPI-1) - Value (%);;2008\', \'Probability at birth of not surviving to age 40 (% of cohort);;2000-05\', \'Adult illiteracy rate (% aged 15 and older);;1995-2005\', \'Population not using an improved water source (%);;2004\', \'Children under weight for age (% under age 5);;1996-2005\', \'Population below income poverty line (%) - $1 a day;;1990-2005\', \'Population below income poverty line (%) - $2 a day;;1990-2005\', \'Population below income poverty line (%) - National poverty line;;1990-2004\', \'HPI-1 rank minus income poverty rank;;2008\']",\n    "SEPARATE > [\'indicator_name\', \'year\'] < \';;\'::[\'indicator_name\']",\n    "DEBLANK",\n    "DEDUPE",\n]\n```\n\nThen **whyqd** may be for you.\n\n## How does it work?\n\n> Crosswalks are mappings of the relationships between fields defined in different metadata \n> [schemas](https://whyqd.readthedocs.io/en/latest/strategies/schema). Ideally, these are one-to-one, where a field in \n> one has an exact match in the other. In practice, it\'s more complicated than that.\n\nYour workflow is:\n\n1. Define a single destination schema,\n2. Derive a source schema from a data source,\n3. Review your source data structure,\n4. Develop a crosswalk to define the relationship between source and destination,\n5. Transform and validate your outputs,\n6. Share your output data, transform definitions, and a citation.\n\nIt starts like this:\n\n```python\nimport whyqd as qd\n```\n\n[Install](https://whyqd.readthedocs.io/en/latest/installation) and then read the [quickstart](https://whyqd.readthedocs.io/en/latest/quickstart).\n\nThere are three worked tutorials to guide you through three typical scenarios:\n\n- [Aligning multiple disparate data sources to a single schema](https://whyqd.readthedocs.io/en/latest/tutorials/tutorial1)\n- [Pivoting wide-format data into archival long-format](https://whyqd.readthedocs.io/en/latest/tutorials/tutorial2)\n- [Wrangling Cthulhu data without losing your mind](https://whyqd.readthedocs.io/en/latest/tutorials/tutorial3)\n\n## Installation\n\nYou\'ll need at least Python 3.8, then install with your favourite package manager:\n\n```bash\npip install whyqd\n```\n\nTo derive a source schema from tabular data, import from `DATASOURCE_PATH`, define its `MIMETYPE`, and derive a schema:\n\n```python\nimport whyqd as qd\n\ndatasource = qd.DataSourceDefinition()\ndatasource.derive_model(source=DATASOURCE_PATH, mimetype=MIMETYPE)\nschema_source = qd.SchemaDefinition()\nschema_source.derive_model(data=datasource.get)\nschema_source.fields.set_categories(name=CATEGORY_FIELD, \n                                    terms=datasource.get_data())\nschema_source.save()\n```\n\n[Get started...](https://whyqd.readthedocs.io/en/latest/quickstart)\n\n## Changelog\n\nThe version history can be found in the [changelog](https://whyqd.readthedocs.io/en/latest/changelog).\n\n## Background and funding\n\n**whyqd** was created to serve a continuous data wrangling process, including collaboration on more complex messy \nsources, ensuring the integrity of the source data, and producing a complete audit trail from data imported to our \ndatabase, back to source. You can see the product of that at [openLocal.uk](https://openlocal.uk).\n\n**whyqd** [received initial funding](https://eoscfuture-grants.eu/meet-the-grantees/implementation-no-code-method-schema-schema-data-transformations-interoperability)\nfrom the European Union\'s Horizon 2020 research and innovation programme under grant agreement No 101017536. Technical \ndevelopment support is from [EOSC Future](https://eoscfuture.eu/) through the \n[RDA Open Call mechanism](https://eoscfuture-grants.eu/provider/research-data-alliance), based on evaluations of \nexternal, independent experts.\n\nThe \'backronym\' for **whyqd** /wɪkɪd/ is *Whythawk Quantitative Data*, [Whythawk](https://whythawk.com)\nis an open data science and open research technical consultancy.\n\n## Licence\n\nThe [**whyqd** Python distribution](https://github.com/whythawk/whyqd) is licensed under the terms of the \n[BSD 3-Clause license](https://github.com/whythawk/whyqd/blob/master/LICENSE). All documentation is released under \n[Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/). **whyqd** tradenames and \nmarks are copyright [Whythawk](https://whythawk.com).\n',
    'author': 'Gavin Chait',
    'author_email': 'gchait@whythawk.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://whyqd.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<4.0',
}


setup(**setup_kwargs)
