e-models
========


Suite of tools to assist in the build of extraction models with scrapy spiders

Installation:

```
$ pip install e-models
```

## scrapyutils module


scrapyutils module provides two classes, one for extending `scrapy.http.TextResponse` and another for
extending `scrapy.loader.ItemLoader`. The extensions provide methods that:

1. Allow to extract item data in the text (markdown) domain instead of the html source domain.
2. The main purpose of this approach is the generation of datasets suitable for training transformer models for text extraction (aka extractive question answering, EQA)
3. As a secondary objective, it provides an alternative approach to xpath and css selectors for extraction of data from the html source, that may be more suitable and readable for humans.
4. In many situations, and specially when there is not an id or a class to spot accurately the text, the expresion in terms of regular expressions in the domain of markdown is usually much simpler.

Usage:

Instead of subclass your item loaders from `scrapy.loader.ItemLoader`, use `emodels.scrapyutils.ExtractItemLoader`. This action will not affect the working of itemloaders and will enable the properties just
described above. In addition, in order to save the collected extraction data, it is required to set the environment variable `EMODELS_SAVE_EXTRACT_ITEMS` to 1. The collected
extraction data will be stored at `<user home folder>/.datasets/items/<item class name>/<sequence number>.jl.gz`. The base folder `<user home folder>/.datasets` is the default one. You can
customize it via the environment variable `EMODELS_DIR`.

So, in order to maintain a clean dataset well ordered, only enable extract items saving when you are sure you have the correct extraction selectors. Then run locally:

```
EMODELS_SAVE_EXTRACT_ITEMS=1 scrapy crawl myspider
```

In addition, in order to have your dataset well ordered, you should choose the same item class name for same item schema, even accross multiple projects. And avoid to repeat it among items with different
schema. However, in general you will use extraction data from all classes of items at same time in order to train a transformer model, as this is the way how transformers learn to generalize. At
the end you will have a transformer model that is suited to extract any kind of item, as they are trained not to extract "data from x item" but instead to recognize and extract based on fields.
So, even if you didn't train the transformer to extract a specific item class, it will do great if you trained it to extract its fields, if it already learned to extract same fields from
other item classes. You only need to ask the correct question. For example, given an html page as a context, you can ask the model: `which is the phone number?`. You don't need to specify
which kind of data (a business? a person? an organization?) you expect to find there.

(WIP...)
