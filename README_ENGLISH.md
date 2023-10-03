# PC2I - Platform
Platform and API code repository for supervision management promoted by the PC2I project.

#### :pushpin: For now, only accessible on _localhost_

---

## :warning: Prerequisites
> Before you begin, make sure the following tools are installed on your machine
- [Git](https://git-scm.com/downloads)
- [Python](https://python.org/downloads)

## :fire: How to contribute
To contribute code or suggestions for improvements/corrections to the PC2I project platform, access the file [CONTRIBUTING.md](./docs/CONTRIBUTING_ENGLISH.md).

If you have any questions or are curious about collaborative work with Git and GitHub, please contact one of the repository members.

## :compass: Installation Guide
> With the tools properly installed, run the following commands in the terminal (bash, powershell, cmd...)

### 1. Clone the repository
```bash
git clone https://github.com/lead-ifal/pc2i-platform.git
```

### 2. Enter the project folder
```bash
cd pc2i-platform
```

### 3. Create the Flask virtual environment
```bash
# Linux and MacOS
python -m venv venv
```

```bash
# Windows
py -3 -m venv venv
```

### 4. Activate the virtual environment
```bash
# Linux and MacOS
. venv/bin/activate
```

```bash
# Windows
venv\Scripts\activate
```

### 5. Install dependencies
```bash
# Linux, MacOS and Windows
pip install -r requirements.txt
```

### 6. Create the environment variables file
Access the file [MONGO_CONFIG.md](./docs/MONGO_CONFIG_ENGLISH.md) and get the database URL.

Using the bank's URL, create a copy of the file [`.env.example`](./.env.example) with the name of `.env`.

In the file `.env`, put the bank URL after `MONGO_URI=(here)`.

### 7. Run the application
```bash
# Linux, MacOS and Windows
python __init__.py
```

In the terminal, something like this will appear:

```bash
* Serving Flask app 'app' (lazy loading)
* Environment: production
  WARNING: This is a development server. Do not use it in a production deployment.
  Use a production WSGI server instead.
* Debug mode: on
* Running on all addresses.
  WARNING: This is a development server. Do not use it in a production deployment.
* Running on http://192.168.1.110:1026/ (Press CTRL+C to quit)
* Restarting with stat
* Debugger is active!
* Debugger PIN: 103-964-359
```

The platform will be running at the specified URL (e.g., `http://192.168.1.110:1026/`)

## :fire: Platform/API testing
Access the route `/api/docs` in the browser to access via [Swagger](https://swagger.io/tools/swagger-ui/) or install an HTTP client such as [Postman](https://postman.com/downloads/), and get the API routes by accessing [this documentation](https://documenter.getpostman.com/view/21952024/UzQypiBw).
