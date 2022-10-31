# Sampling-Studio

- [Sampling-Reconstruction-Signals](#sampling-reconstruction-signals)
  - [Task Info.](#task-info.)
  - [Features](#features)
  - [Demos](#demos)
    - [Reconstruction Demo](#reconstruction-demo)
    - [Composer Demo](#composer-demo)
  - [Run-App](#run-app)

## Task Info. 
- This course is about _Digital Signal Processing_ for Third-year of department of medical Engineering, first semester on **25th Oct.2022**
- Members who participated in the work of this project:
  | Names           | Section | Bench Number |
  | --------------- | ------- | ------------ |
  | Amr Muhammed    |    2    |      7       |
  | Abdelrahman Ali |    1    |     55       |
  | Ereny Eleya     |    1    |     19       |
  | Kareman yasser  |    2    |     9        |
## Description
   This is a web app for sampling, reconstruction and composing signals
## Features
- Developing an illustrator for the signal recovery that shows Nyquist rate.
- Highlight the sampled points on top of the original signal.
- Change the sampling frequency via a slider that range from 1 to 10 fmax (normalized freqency) or from 1 to 800 HZ
- Reconstruct/recover the signal from the sampled points.
- Adding noise to the signal by SNR to see the effect of noise on the sampling and recovery of the signal
- Composing signals together via the add button and removing selected signals from the sum of signals  illustrating the results on the graph
- After making a synthetic signal then moving it to the main illustrator graph to start the sampling/recovery process.
## Demos
1. Generating, samoling and recovering a signal using normalized frequency

![This is an image](https://github.com/Amrmohamed090/DSP_task1_19/blob/main/Screenshot%20(197).png)

2. Uploading, sampling and recovering a signal 

![This is an image](https://github.com/Amrmohamed090/DSP_task1_19/blob/main/Screenshot%20(199).png)

3. Sampling a signal by frequency 
![This is an image](https://github.com/Amrmohamed090/DSP_task1_19/blob/main/Screenshot%20(200).png)

4. Adding noise to the signal 
![This is an image](https://github.com/Amrmohamed090/DSP_task1_19/blob/main/Screenshot%20(201).png)

### Composer Demo 
![Composer](GIFs/composing.gif)

### Reconstruction Demo 
![Sampler](GIFs/sampling.gif)

## Run-App
1. **_install project dependencies_**
```sh
pip install -r requirements.txt
```
2. **_Run the application_**
```sh
python main.py
