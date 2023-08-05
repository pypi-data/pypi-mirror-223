# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['databeakers']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.24.0,<0.25.0',
 'networkx>=3.1,<4.0',
 'pydantic>=2.0.2,<3.0.0',
 'rich>=13.4.2,<14.0.0',
 'scrapelib>=2.1.0,<3.0.0',
 'structlog>=23.1.0,<24.0.0',
 'typer>=0.9.0,<0.10.0']

entry_points = \
{'console_scripts': ['bkr = beakers.cli:app']}

setup_kwargs = {
    'name': 'databeakers',
    'version': '0.1.0',
    'description': '',
    'long_description': '# beakers\n\nbeakers is an experimental lightweight declarative ETL framework for Python\n\nRight now this is an experiment to explore some ideas around ETL.\n\nIt is still very experimental with no stability guarantees. \nIf you\'re interested in poking around, thoughts and feedback are welcome, please reach out before contributing code though as a lot is still in flux.\n\n## (Intended) Features\n\n- [x] Declarative ETL graph comprised of Python functions & Pydantic models\n- [x] Developer-friendly CLI for running processes\n- [x] Synchronous mode for ease of debugging or simple pipelines\n- [x] Data checkpoints stored in local database for intermediate caching & resuming interrupted runs\n- [ ] Asynchronous task execution\n- [ ] Support for multiple backends (sqlite, postgres, etc)\n- [ ] Robust error handling, including retries\n\n## Guiding Principles\n\n* **Lightweight** - Writing a single python file should be enough to get started. It should be as easy to use as a script in that sense.\n* **Data-centric** - Looking at the definition should make it clear what data exists at what step. \n* **Modern Python** - Take full advantage of recent additions to Python, including type hints, `asyncio`, and libraries like `pydantic`.\n* **Developer Experience** - The focus should be on the developer experience, a nice CLI, helpful error messages.\n\n## Anti-Principles\n\nUnlike most tools in this space, this is not a complete "enterprise grade" ETL solution.\n\nIt isn\'t a perfect analogy by any means but beakers strives to be to `luigi` what `flask` is to `Django`. \nIf you are building your entire business around ETL, it makes sense to invest in the infrastructure & tooling to make that work.\nMaybe structuring your code around beakers will make it easier to migrate to one of those tools than if you had written a bespoke script.\nPlus, beakers is Python, so you can always start by running it from within a bigger framework.\n\n## Concepts\n\nLike most ETL tools, beakers is built around a directed acyclic graph (DAG).\n\nThe nodes on this graph are known as "beakers", and the edges are often called "transforms".\n\n(Note: These names aren\'t final, suggestions welcome.)\n\n### Beakers\n\nEach node in the graph is called a "beaker". A beaker is a container for some data.\n\nEach beaker has a name and a type.\nThe name is used to refer to the beaker elsewhere in the graph.\nThe type, represented by a `pydantic` model, defines the structure of the data. By leveraging `pydantic` we get a lot of nice features for free, like validation and serialization.\n\n### Transform\n\nEdges in the graph represent dataflow between beakers. Each edge has a concept of a "source beaker" and a "destination beaker".\n\n These come in two main flavors:\n\n* **Transforms** - A transform places new data in the destination beaker based on data already in the source beaker.\nAn example of this might be a transform that takes a list of URLs and downloads the HTML for each one, placing the results in a new beaker.\n\n* **Filter** - A filter can be used to stop the flow of data from one beaker to another based on some criteria.\n\n### Seed\n\nA concept somewhat unique to beakers is the "seed". A seed is a function that returns initial data for a beaker.\n\nThis is useful for things like starting the graph with a list of URLs to scrape, or a list of images to process.\n\nA beaker can have any number of seeds, for example one might have a short list of URLs to use for testing, and another that reads from a database.',
    'author': 'James Turk',
    'author_email': 'dev@jamesturk.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
