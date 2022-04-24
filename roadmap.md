

Ver 1 – Simply works

x Can inefficiently create a photo_mosaic (NO PREMATURE OPTIMIZATION!)

Ver 2 – Plug & Play

x Allow pickle ingress for tiles instead of converting cropped images each time.

x Generalize program so it can be used for non-fruit-related purposes.

x Add sample image folder for plug-and-play Github code.

Ver 3 – Benchmarking & Testing

- (Easy) Add environment info to quit_error https://stackoverflow.com/questions/4906977/how-do-i-access-environment-variables-in-python

- Add testing cases using pytest

- Testing using pytest https://docs.pytest.org/en/7.1.x/ 
Also consider pytest-html for html reports
$ pip install pytest-html
$ pytest –-html=report.html

-- Test using big datasets
-- Test using small datasets

- Add Codecov https://about.codecov.io/sign-up/

- Add dependabot

- Automate regression testing via CI (Jenkins, Buddy), also automatically generate dependencies list.

Ver 4 - Algo Optimization

- Optimize efficiency of find_mosaic_tile algorithm. (Currently loops through EVERY image for EVERY TILE to find the closest match.)

Ver 5 - Ease Of Use

- Create simple GUI https://realpython.com/python-gui-tkinter/

- Implement command-line flags: https://typer.tiangolo.com/ (same developer as FastAPI)

- Create pipenv https://pipenv.pypa.io/en/latest/ for easy install
