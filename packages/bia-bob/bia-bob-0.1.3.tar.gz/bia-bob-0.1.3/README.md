# bia-bob

BIA Bob is a Jupyter-based assistant for interacting with image data and for working on Bio-image Analysis tasks.
It is based on [LangChain](https://python.langchain.com/docs/get_started/introduction.html) and [OpenAI's API](https://openai.com/blog/openai-api). You need an openai API account to use it.

Trailer:

![img.png](https://github.com/haesleinhuepf/bia-bob/raw/main/docs/images/bia_bob_trailer.gif)

Note: Bob is currently in an early alpha stage. It is not very smart yet. Feedback is very welcome!

## Usage

Detailed examples of how to interact with Bob are given in these notebooks:
* [Basic usage](https://github.com/haesleinhuepf/bia-bob/blob/main/demo/basic_demo.ipynb)
* [Accessing variables](https://github.com/haesleinhuepf/bia-bob/blob/main/demo/globals.ipynb)
* [Image Filtering](https://github.com/haesleinhuepf/bia-bob/blob/main/demo/image_filtering.ipynb)
* [Browsing folders](https://github.com/haesleinhuepf/bia-bob/blob/main/demo/browsing_folders.ipynb)
* [Interactive image stack viewing](https://github.com/haesleinhuepf/bia-bob/blob/main/demo/interactive_stackview.ipynb)

You can initialize Bob like this:
```
from bia_bob import bob
```

In case you want it to be aware of all your variables, call this addtionally:
```
bob.initialize(globals())
```

Afterwards, you can ask Bob questions like this:
```
%bob Load blobs.tif and show it
```

Or like this:
```
%%bob
Please load the image blobs.tif,
segment bright objects in it, 
count them and 
show the segmentation result.
```


You can also ask Bob about available tools:
```
%bob list tools
```

## Example gallery

![img.png](https://github.com/haesleinhuepf/bia-bob/raw/main/docs/images/load_and_show.png)

![img_1.png](https://github.com/haesleinhuepf/bia-bob/raw/main/docs/images/slice.png)

![img.png](https://github.com/haesleinhuepf/bia-bob/raw/main/docs/images/chain_workflows.png)

![img.png](https://github.com/haesleinhuepf/bia-bob/raw/main/docs/images/count_blobs.png)

![img.png](https://github.com/haesleinhuepf/bia-bob/raw/main/docs/images/edge_detection.png)

## Known issues

If you want to ask Bob a question, you need to put a space before the `?`.

```
What do you know about blobs.gif ?
```

## Installation

```
pip install bia-bob
```


## Issues

If you encounter any problems or want to provide feedback or suggestions, please create a thread on [image.sc](https://image.sc) along with a detailed description and tag [@haesleinhuepf].





