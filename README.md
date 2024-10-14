<!-- PROJECT LOGO -->
<br />
<div align="center">

  <a href="https://github.com/CenterForTheBuiltEnvironment/comfort-dash/blob/main/assets/media/CBE-logo-2018.png">
    <img src="assets/media/CBE-logo-2018.png" alt="Logo" width="80">
  </a>

<h3 align="center">CBE Thermal Comfort Tool</h3>

  <p align="center">
    This is the official repository for the CBE Thermal Comfort Tool
    <br />
    <br />
    <a href="https://comfort-tool-v2-test-6ncu37myea-uc.a.run.app/">View Demo</a>
    ·
    <a href="https://github.com/CenterForTheBuiltEnvironment/comfort-dash/issues/new">Report Bug</a>
    ·
    <a href="https://github.com/CenterForTheBuiltEnvironment/comfort-dash/issues/new">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This is the official repository for the CBE Thermal Comfort Tool. 
The CBE Thermal Comfort Tool is a web application to calculate and visualize thermal comfort indices.

- [Original CBE Comfort Tool Repository](https://github.com/CenterForTheBuiltEnvironment/comfort_tool)
- [Project Miro Board](https://miro.com/app/board/uXjVKpPJvxE=/?share_link_id=841990080046)
- [CBE Tool Template Repository](https://github.com/CenterForTheBuiltEnvironment/cbe-tool-template)

[//]: # ([![Product Name Screen Shot][product-screenshot]]&#40;https://example.com&#41;)

[//]: # (Here's a blank template to get started: To avoid retyping too much info. Do a search and replace with your text editor for the following: `Environmental-Measurement-Unit-Systems`, `dashboard`, `twitter_handle`, `linkedin_username`, `email_client`, `email`, `project_title`, `project_description`)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

[![Python][Python.org]][Python-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.
Clone the repository and run the following commands:

```bash
pipenv install
pipenv shell
python app.py
```

Then you can run the application using the following command:

```bash
python app.py
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/CenterForTheBuiltEnvironment/comfort-dash/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`) using [commit conventions](https://www.conventionalcommits.org/en/v1.0.0/).
4. Bump the version `bump-my-version bump patch`
5. Push to the Branch (`git push origin feature/AmazingFeature`)
6. Open a Pull Request

### Test the application

I wrote some tests with playwright to make sure the application is displaying properly.
All the tests are located in the `tests` folder.

In order to run the tests, you need to have the application running locally.

```bash
python app.py
``` 

You will also need to install the playwright dependencies, [more info here](https://playwright.dev/python/docs/intro):

```bash
playwright install
```

#### Test generation

Detailed guide on how to generate tests can be found [here](https://playwright.dev/python/docs/codegen)

```
playwright codegen http://localhost:9090
```

If you want to generate tests for a specific device, you can run the following command:

```
playwright codegen --device="iPhone 13" http://localhost:9090
```

### Deploy the application

The application is deployed automatically using a GitHub action.
If you want to deploy the application manually, you can run the following command:

```
gcloud components update
pipenv requirements > requirements.txt
pipenv requirements --dev > dev-requirements.txt
gcloud config set account federicotartarini@gmail.com
python -m pytest tests/test_public_urls.py --base-url http://0.0.0.0:9090
python -m pytest --numprocesses 3 --base-url http://0.0.0.0:9090
python -m pytest --numprocesses 3 --base-url https://comfort-tool-v2-test-6ncu37myea-uc.a.run.app
gcloud builds submit --project=comfort-327718 --substitutions=_REPO_NAME="comfort-tool-v2-test"
gcloud builds submit --project=comfort-327718 --substitutions=_REPO_NAME="comfort-tool-v2"
```

### Kill application running locally

```
lsof -i :9090
kill -9 <PID>
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Federico Tartarini - federicotartarini@gmail.com

Project Link: [CenterForTheBuiltEnvironment/comfort-dash](https://github.com/CenterForTheBuiltEnvironment/comfort-dash)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Contributors

* [Federico Tartarini]()

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Teams & responsibilities
|  Group   |  Task                 |  Team                                            | Main focus                                           | 
|----------|-----------------------|--------------------------------------------------|------------------------------------------------------|
|  -       |  **Admin**            | Revolving, weekly                                |  Meetings & communication (e.g. notes, agenda)       |
|  A       |  **Front-End**        | Ruixin Wu, Jiaming Zheng, Xuhui Wang, Zhou Tong  |  Front-End design and Dash implementation            |
|  A       |  **Visuals**          | Jiadong Zhang, Yan Zhang                         |  Develop plots for main UI                           |
|  B       |  **Data Management**  | Shiyi Shen, Haozhen Li                           |  Manage use of data within app                       |
|  B       |  **Back-End**         | Yinyan Liu, Junan Lu, Jinjia Bai, Chao Jiang     |  Develop app back-end                                |
|  -       |  **Testing**          | Haozhen Li                                       |  Writing tests for the app                           |



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/CenterForTheBuiltEnvironment/comfort-dash.svg?style=for-the-badge
[contributors-url]: https://github.com/CenterForTheBuiltEnvironment/comfort-dash/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/CenterForTheBuiltEnvironment/comfort-dash.svg?style=for-the-badge
[forks-url]: https://github.com/CenterForTheBuiltEnvironment/comfort-dash/network/members
[stars-shield]: https://img.shields.io/github/stars/CenterForTheBuiltEnvironment/comfort-dash.svg?style=for-the-badge
[stars-url]: https://github.com/CenterForTheBuiltEnvironment/comfort-dash/stargazers
[issues-shield]: https://img.shields.io/github/issues/CenterForTheBuiltEnvironment/comfort-dash.svg?style=for-the-badge
[issues-url]: https://github.com/CenterForTheBuiltEnvironment/comfort-dash/issues
[license-shield]: https://img.shields.io/github/license/CenterForTheBuiltEnvironment/comfort-dash.svg?style=for-the-badge
[license-url]: https://github.com/CenterForTheBuiltEnvironment/comfort-dash/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/federico-tartarini/
[product-screenshot]: images/screenshot.png
[Python.org]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/




