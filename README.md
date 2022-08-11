# Sunalyzer

![Python checks](https://github.com/VanKurt/Sunalyzer/actions/workflows/python.yml/badge.svg)
![Docker build](https://github.com/VanKurt/Sunalyzer/actions/workflows/docker.yml/badge.svg)

Sunalyzer is a free and open source solar monitoring system. It collects relevant data from your inverter/smart meter and stores them safely in a data base. A modern and beautiful web frontend allows you to visualize the data on any device. Sunalyzer can easily be self hosted on a Raspberry Pi or a NAS by using Docker. No cloud is required, all your data stays under your control.

![Bilby Stampede](doc/screenshot.png)

## Supported Languages

Currently Sunalyzer provides an **English** and a **German** user interface. The language can be changed on the fly via the user interface.

## Supported Devices

Sunalyzer provides integrations for the following device types (inverters/smart meters):
* Fronius (Symo/Gen24)
* Dummy device (for testing purposes)

Contributions for the support of additional devices are welcome. Please feel free to creach out or submit a pull request.


## Installation instructions

Sunalyzer comes as a self contained and easy to set up Docker container. Thus it can be run on various different platforms. Detailled installation instructions for the Raspberry Pi and Synology DiskStation NAS systems are provided below.

### General Docker Container Configuration

Todo

### Installation Guide: Synology NAS

Todo

### Installation Guide: Raspberry Pi

Todo

## Configuration

Todo

## Deveopment Environment

Sunalyzer is currently being developed using the following tools and libraries:
* **Operating system**: Manjaro Linux
* **Development Environment**: Visual Studio Code
* **Programming languages**: Python 3.10, JavaScript, HTML
* **Database**: SQlite
* **Frameworks**: Bootstrap, Chart.js
* **DevOps**: pylint, htmlhint, ESlint
* **Deployment**: Docker
