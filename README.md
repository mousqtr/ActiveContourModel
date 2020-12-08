# ActiveContourModel

This project shows the implementation of one of the active contour segmentation methods, the "snakes" method. This method is based on the minimization of two energies: the internal energy related to the shape of the snake and the external energy dependent on the image. 

## Usage
### Clone the project
```
clone https://github.com/mousqtr/ActiveContourModel.git
```
### Create and activate the virtual environment 
```
python -m venv venv
venv\Scripts\activate.bat
```
### Install the libraries 
```
pip install -r requirements.txt
```
### Run the program
```
python snake.py filename
```
### Examples
```
python snake.py images/goutte.png
python snake.py images/finger.png
```
