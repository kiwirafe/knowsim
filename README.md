# KnowSim

#### KnowSim, Know Your Simlarity
#### Text Similarity Calculator
#### Cossine, Simhash, Minhash Similarity Calculator

[![Pypi Version](https://img.shields.io/pypi/v/knowsim?label=Pypi%20Version)](https://img.shields.io/pypi/v/knowsim)
[![Downloads](https://pepy.tech/badge/knowsim)](https://pepy.tech/project/knowsim)
[![Pypi and Github License](https://img.shields.io/pypi/l/knowsim?label=Pypi%20and%20Github%20License)](https://img.shields.io/github/license/kiwirafe/knowsim)
[![Language](https://img.shields.io/github/languages/top/kiwirafe/knowsim)](https://github.com/kiwirafe/knowsim)

The advantages of Knowsim are:

  - Focus on text similarity comparison
  - Cosine similarity and Simhash + Minhash algorithms are used
  - 100% Python language
  - Automatic TFIDF filtering
  - TF and IDF can be calculated separately
  - List and file are supported
  - Support multiple file similarity comparison
  - Efficient and quick
  - Easy to install
  - 100% open source
  - Long term maintenance and update

### Download and install
PIP installation:
```sh
$ pip3 install knowsim
```

### Usage method
#### Calculate text similarity
##### Cosine similarity
```py
import knowsim as ks
ks.cossim(Input1, Input2)
```
##### Simhash & Minhash similarity
```py
import knowsim as ks
# Simhash
ks.simhash(Input1, Input2)
# Minhash
ks.minhash(Input1, Input2)
```
  - When calculating the text similarity, it is automatically filtered by TFIDF
  - Input1 - the first input value, which can be the address of a file or a list
  - Input2 - the second input value, which can be the address of a file or a list

##### Calculate TF, IDF, TFIDF
```py
import knowsim as ks
ks.GetTF(Input)
ks.GetIDF(Input)
ks.GetTFIDF(Input)
```
  - Input - input value, which can be the address of a file or a list
  - Input type for calculating text similarity
  - At present, two types of acquaintance are supported: file and list file


### MIT License
Copyright (c) [2020] [Kiwirafe]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
