from invoke import task

@task(aliases=("cl",))
def clear_notebooks(c):
    c.run("jupyter nbconvert --clear-output notebooks/*.ipynb")
