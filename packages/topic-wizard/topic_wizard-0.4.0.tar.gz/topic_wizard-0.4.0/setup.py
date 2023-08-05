# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['topicwizard',
 'topicwizard.blueprints',
 'topicwizard.compatibility',
 'topicwizard.components',
 'topicwizard.components.documents',
 'topicwizard.components.groups',
 'topicwizard.components.topics',
 'topicwizard.components.words',
 'topicwizard.figures',
 'topicwizard.plots',
 'topicwizard.prepare']

package_data = \
{'': ['*'], 'topicwizard': ['assets/*']}

install_requires = \
['dash-extensions>=0.1.10,<0.2.0',
 'dash-iconify>=0.1.2,<0.2.0',
 'dash-mantine-components>=0.11.1,<0.12.0',
 'dash>=2.7.1,<2.8.0',
 'joblib>=1.2.0,<1.3.0',
 'numpy>=1.22.0',
 'pandas>=1.5.2,<1.6.0',
 'scikit-learn>=1.2.0,<1.3.0',
 'scipy>=1.8.0',
 'umap-learn>=0.5.3',
 'wordcloud>=1.8.2.2,<1.9.0.0']

setup_kwargs = {
    'name': 'topic-wizard',
    'version': '0.4.0',
    'description': 'Pretty and opinionated topic model visualization in Python.',
    'long_description': '<img align="left" width="82" height="82" src="assets/logo.svg">\n\n# topicwizard\n\n<br>\n\nPretty and opinionated topic model visualization in Python.\n\n[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/x-tabdeveloping/topic-wizard/blob/main/examples/basic_usage.ipynb)\n[![PyPI version](https://badge.fury.io/py/topic-wizard.svg)](https://pypi.org/project/topic-wizard/)\n[![pip downloads](https://img.shields.io/pypi/dm/topic-wizard.svg)](https://pypi.org/project/topic-wizard/)\n[![python version](https://img.shields.io/badge/Python-%3E=3.8-blue)](https://github.com/centre-for-humanities-computing/tweetopic)\n[![Code style: black](https://img.shields.io/badge/Code%20Style-Black-black)](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html)\n<br>\n\n\n\nhttps://user-images.githubusercontent.com/13087737/234209888-0d20ede9-2ea1-4d6e-b69b-71b863287cc9.mp4\n\n## New in version 0.4.0 🌟 🌟\n\n- Introduced topic pipelines that make it easier and safer to use topic models in downstream tasks and interpretation.\n\n## New in version 0.3.1 🌟 🌟\n\n- You can now investigate relations of pre-existing labels to your topics and words :mag:\n\n## New in version 0.3.0 🌟 \n\n - Exclude pages, that are not needed :bird:\n - Self-contained interactive figures :gift:\n - Topic name inference is now default behavior and is done implicitly.\n\n\n## Features\n\n-   Investigate complex relations between topics, words, documents and groups/genres/labels\n-   Sklearn, Gensim and BERTopic compatible :nut_and_bolt:\n-   Highly interactive web app\n-   Interactive and composable Plotly figures\n-   Automatically infer topic names, oooor...\n-   Name topics manually\n-   Easy deployment :earth_africa:\n\n## Installation\n\nInstall from PyPI:\n\n```bash\npip install topic-wizard\n```\n\n## Usage ([documentation](https://x-tabdeveloping.github.io/topic-wizard/))\n\n### Step 0:\n\nHave a corpus ready for analysis, in this example I am going to use 20 newgroups from scikit-learn.\n\n```python\nfrom sklearn.datasets import fetch_20newsgroups\n\nnewsgroups = fetch_20newsgroups(subset="all")\ncorpus = newsgroups.data\n\n# Sklearn gives the labels back as integers, we have to map them back to\n# the actual textual label.\ngroup_labels = [newsgroups.target_names[label] for label in newsgroups.target]\n```\n\n### Step 1:\n\nTrain a scikit-learn compatible topic model.\n(If you want to use non-scikit-learn topic models, check [compatibility](https://x-tabdeveloping.github.io/topic-wizard/usage.compatibility.html))\n\n```python\nfrom sklearn.decomposition import NMF\nfrom sklearn.feature_extraction.text import CountVectorizer\nfrom sklearn.pipeline import make_pipeline\n\n# Create topic pipeline\npipeline = make_pipeline(\n    CountVectorizer(stop_words="english", min_df=10),\n    NMF(n_components=30),\n)\n\n# Then fit it on the given texts\npipeline.fit(corpus)\n```\n\nFrom version 0.4.0 you can also use TopicPipelines, which are almost functionally identical but come with a set of built-in conveniences and\nsafeties.\n\n```python\nfrom topicwizard.pipeline import make_topic_pipeline\n\npipeline = make_topic_pipeline(\n    CountVectorizer(stop_words="english", min_df=10),\n    NMF(n_components=30),\n)\n```\n\n### Step 2a:\n\nVisualize with the topicwizard webapp :bulb:\n\n```python\nimport topicwizard\n\ntopicwizard.visualize(corpus, pipeline=pipeline)\n```\n\nFrom version 0.3.0 you can also disable pages you do not wish to display thereby sparing a lot of time for yourself:\n\n```python\n# A large corpus takes a looong time to compute 2D projections for so\n# so you can speed up preprocessing by disabling it alltogether.\ntopicwizard.visualize(corpus, pipeline=pipeline, exclude_pages=["documents"])\n```\n\n\n![topics screenshot](assets/screenshot_topics.png)\n![words screenshot](assets/screenshot_words.png)\n![words screenshot](assets/screenshot_words_zoomed.png)\n![documents screenshot](assets/screenshot_documents.png)\n\nFrom version 0.3.1 you can investigate groups/labels by passing them along to the webapp.\n\n```python\ntopicwizard.visualize(corpus, pipeline=pipeline, group_labels=group_labels)\n```\n\n![groups screenshot](docs/_static/screenshot_groups.png)\n\nOoooor...\n\n### Step 2b:\n\nProduce high quality self-contained HTML plots and create your own dashboards/reports :strawberry:\n\n### Map of words\n\n```python\nfrom topicwizard.figures import word_map\n\nword_map(corpus, pipeline=pipeline)\n```\n\n![word map screenshot](assets/word_map.png)\n\n### Timelines of topic distributions\n\n```python\nfrom topicwizard.figures import document_topic_timeline\n\ndocument_topic_timeline(\n    "Joe Biden takes over presidential office from Donald Trump.",\n    pipeline=pipeline,\n)\n```\n![document timeline](assets/document_topic_timeline.png)\n\n### Wordclouds of your topics :cloud:\n\n```python\nfrom topicwizard.figures import topic_wordclouds\n\ntopic_wordclouds(corpus, pipeline=pipeline)\n```\n\n![wordclouds](assets/topic_wordclouds.png)\n\n#### And much more... ([documentation](https://x-tabdeveloping.github.io/topic-wizard/))\n',
    'author': 'Márton Kardos',
    'author_email': 'power.up1163@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0',
}


setup(**setup_kwargs)
