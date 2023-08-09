# say11

Utility to use eleven lab's streaming to in the command line

## Installation

You'll need to install mpv on Mac via Brew

```sh
brew install mpv
```

Then to install the library 

```sh
pip install say11
```

## Usage 

To use this you can use two methods, weither pipe into stdin 

```sh
cat text.txt | say11 -v Nicole 
echo "hello there everyone!" | say11 -v Nicole 
```

or by using the normal arugment

```sh
say11 -t "Hello everyone!" -v Nicole
```