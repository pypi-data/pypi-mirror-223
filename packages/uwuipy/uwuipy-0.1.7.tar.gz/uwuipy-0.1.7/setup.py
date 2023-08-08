# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['uwuipy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'uwuipy',
    'version': '0.1.7',
    'description': 'Allows the easy implementation of uwuifying words for applications like Discord bots and websites',
    'long_description': '# uwuipy\n`uwuipy` is an advanced uwuifier for Python, designed to transform regular text into a playful and expressive "uwu" style. This whimsical modification of text is often used in online communities for humorous or emotive communication.\n\nWhether you\'re looking to add a fun twist to a chat application or simply want to explore text manipulation in a lighthearted manner, `uwuipy` offers an easy-to-use interface with customizable options to create unique text transformations.\n\nThe library provides control over various aspects of the uwuification process, including stuttering, facial expressions, actions, and exclamations. Whether you want subtle changes or dramatic transformations, `uwuipy` allows you to find the perfect balance through adjustable parameters.\n\n## Key Features:\n- Ease of Use: Quickly integrate `uwuipy` into your projects with a simple API.\n- Customizable: Tailor the uwuification process to your needs with adjustable parameters.\n- CLI Support: Use the tool directly from the command line or integrate it into Python applications.\n- Entertainment: A unique way to engage users with lively and animated text transformations.\n\n## Requirements\n* Python 3.10 or higher\n\n## Install\nTo install just use PyPI `pip install uwuipy`\n\n## Usage\n### As a library\nIntegrate `uwuipy` into your Python application to transform ordinary text into playful uwu-styled expressions. Here\'s a basic example of how to use it:\n```python\nfrom uwuipy import uwuipy\n\nuwu = uwuipy()\nprint(uwu.uwuify(input()))\n```\n\n#### Constructor parameters\nThe `uwuipy` constructor allows fine-tuning of the uwuification process through the following parameters:\n\n- `seed`: An integer seed for the random number generator. Defaults to current time if - not provided.\n- `stutterchance`: Probability of stuttering a word (0 to 1.0), default 0.1.\n- `facechance`: Probability of adding a face (0 to 1.0), default 0.05.\n- `actionchance`: Probability of adding an action (0 to 1.0), default 0.075.\n- `exclamationchance`: Probability of adding exclamations (0 to 1.0), default 1.\n- `nsfw_actions`: Enables more explicit actions if set to true; default is false.\n\n#### Customized Example:\nAdjust the parameters to create a customized uwuification process:\n```python\nfrom uwuipy import uwuipy\n\nuwu = uwuipy(None, 0.3, 0.3, 0.3, 1, False)\nprint(uwu.uwuify(input()))\n```\n\nThis can produce output like:\n```\nThe quick brown fox jumps over the lazy dog\nThe quick b-b-b-bwown (・\\`ω\\´・) ***screeches*** fox jumps uvw t-t-t-the OwO wazy dog\n```\n\n#### Time-Based Seeding:\nUtilize time-based seeding for unique transformations:\n```python\nfrom datetime import datetime\nfrom uwuipy import uwuipy\n\nmessage = "Hello this is a message posted in 2017."\nseed = datetime(2017, 11, 28, 23, 55, 59, 342380).timestamp()\nuwu = uwuipy(seed)\nprint(uwu.uwuify(message))\n```\nThis method only uses the `uwuify()` function, accepting a string and returning an uwuified string based on the constructor parameters.\n\n### Directly in the terminal\n#### CLI\nUse `uwuipy` directly from the command line for quick uwuification:\n```bash\npython3 -m uwuipy The quick brown fox jumps over the lazy dog\n```\nOutput:\n```bash\nThe quick b-b-b-bwown (・\\`ω\\´・) ***screeches*** fox jumps uvw t-t-t-the OwO wazy dog\n```\n\n#### REPL\nREPL Mode:\n```bash\npython3 -m uwuipy \n>>> The quick brown fox jumps over the lazy dog\nThe quick b-b-b-bwown (・\\`ω\\´・) ***screeches*** fox jumps uvw t-t-t-the OwO wazy dog\n```\n\n#### Help\nCommand Line Help:\n```bash\npython3 -m uwuipy --help\n```\n\n## Contributing and Licence\nFeel free contribute to the [GitHub repo](https://github.com/Cuprum77/uwuipy) of the project.\n\nLicenced under [MIT](https://github.com/Cuprum77/uwuipy/blob/main/LICENSE)\n',
    'author': 'Cuprum77',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
