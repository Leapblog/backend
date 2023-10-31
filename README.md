<h1 align="center">Leapblog - Backend</h1>

<div align="center">
  <img src="https://cdn.snishant.com.np/r/leapblog.png" alt="Leapblog Logo" width="400">
</div>

---

<div align="center">
  <img
    alt="GitHub repo size"
    src="https://img.shields.io/github/repo-size/Seven-Musketeers/backend?color=FFB001&logo=github&style=for-the-badge&logoColor=00CB5B"
  />
  <img
    alt="GitHub forks"
    src="https://img.shields.io/github/forks/Seven-Musketeers/backend?color=FFB001&logo=github&style=for-the-badge&logoColor=00CB5B"
  />
  <img
    alt="GitHub Repo stars"
    src="https://img.shields.io/github/stars/Seven-Musketeers/backend?color=FFB001&logo=github&style=for-the-badge&logoColor=00CB5B"
  />
  <img
    alt="Last commit"
    src="https://img.shields.io/github/last-commit/Seven-Musketeers/backend?color=FFB001&logo=git&logoColor=00CB5B&style=for-the-badge"
  />
  <img
    alt="Commit activity"
    src="https://img.shields.io/github/commit-activity/m/Seven-Musketeers/backend?color=FFB001&logo=git&logoColor=00CB5B&style=for-the-badge"
  />
</div>

## Running Locally

**Clone the project**

```bash
  git clone https://github.com/Seven-Musketeers/backend
```

**Go to the project directory**

```bash
  cd backend
```

**Install dependencies**

We need poetry to install the dependencies and manage them. Refer to this [link](https://python-poetry.org/docs/) on how to install poetry.

After the installation, we need to activate the virtual environment. Run this command to activate it.

```bash
poetry shell
```

Then finally install all the dependencies using this command.

```bash
  poetry install
```

**Environment File Setup**

Rename the `.env.example` file to `.env` to setup the environment file.

**Setup Database**

To setup the database, we need docker-compose. You can refer to [this](https://docs.docker.com/compose/install/) to install `docker-compose` on your system. If you already have postgres installed on your system, make sure to disable it first before running the command below.

After the installation of docker and docker-compose you can run this command to setup the database

```bash
docker-compose up -d
```

This will start the database up in the background.

**Run Migrations**
Before starting the project for the first time we need to make migrations and run the migrate command to sync our database with the latest changes.

First, make the migration files using this command:

```bash
python manage.py makemigrations
```

Then, migrate the database using the migrations files by running this command:

```bash
python manage.py migrate
```

**Starting the Project**
After all the initial setup, we're now ready to start the project up. Run this command to start the project:

```bash
python manage.py runserver
```
