# Data Mining Project

We make SIR model with python from [COVID-19 Italy dataset](https://github.com/pcm-dpc/COVID-19).

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install required packages.

```bash
pip install numpy
pip install matplotlib
pip install scipy
pip install beautifulsoup4
pip install requests
```

Python version used :

```python
python --version
Python 3.6.8
```

## Usage

### Brief Summary

There are 3 main file in the root directory.

1. Scrapper `scrapper.py`
   Is used to download automatically the data from the github. Here is the github [link](https://github.com/pcm-dpc/COVID-19/tree/master)
2. Cleaner `cleaner.py`
   Is used to clean the downloaded data and save the new data in `dataset/dataframe.csv`
3. Runner `runner.py`
   Is used to run the SIR model and compare it to the `dataset/dataframe.csv` so that we can get the accuracy of the model.

### How to run

First, thing first. Install all the requirement. And then, run the `scrapper.py` like this :

```python
python scrapper.py
```

Wait untill all the data is downloaded into the `./dataset/` folder. After that, the second thing we must do is clean the data :

```python
python cleaner.py
```

After the data has been cleaned. We can continue to run the runner file :

```python
python runner.py
```

We can see in stdout about the details. And also, remember that the value of constant.TIME must be equal to the number of row in dataframe. Unless you dont want to plot the real data result.

### Model Detail

There are two models that we provide :

1. SIR (Susceptible, Infected, Recovered/Removed)
2. SEIRD (Susceptible, Exposed, Infected, Recovered, Death)

You can find both model file python in `./model/` directory

## Contributing

This is a university project, i already have a team. Please dont ask me to make you contributor or something.

## References

- [https://www.statista.com/statistics/270473/age-distribution-in-italy/](https://www.statista.com/statistics/270473/age-distribution-in-italy/)
- [https://www.statista.com/statistics/1106372/coronavirus-death-rate-by-age-group-italy/](https://www.statista.com/statistics/1106372/coronavirus-death-rate-by-age-group-italy/)
- [https://www.worldometers.info/coronavirus/coronavirus-incubation-period/](https://www.worldometers.info/coronavirus/coronavirus-incubation-period/)
- [https://scipython.com/book/chapter-8-scipy/additional-examples/the-sir-epidemic-model/](https://scipython.com/book/chapter-8-scipy/additional-examples/the-sir-epidemic-model/)
- [https://towardsdatascience.com/infectious-disease-modelling-beyond-the-basic-sir-model-216369c584c4](https://towardsdatascience.com/infectious-disease-modelling-beyond-the-basic-sir-model-216369c584c4)
- [https://en.wikipedia.org/wiki/Basic_reproduction_number](https://en.wikipedia.org/wiki/Basic_reproduction_number)

## License

[MIT](https://choosealicense.com/licenses/mit/)
