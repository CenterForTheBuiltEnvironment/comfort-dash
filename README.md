<!-- PROJECT LOGO -->
<br />
<div align="center">

[//]: # (  <a href="https://github.com/Environmental-Measurement-Unit-Systems/dashboard/blob/main/assets/media/emu_logo_white.png">)
[//]: # (    <img src="assets/media/emu_logo_white.png" alt="Logo" width="80">)
[//]: # (  </a>)

<h3 align="center">CBE Thermal Comfort Tool</h3>

  <p align="center">
    This is the official repository for the CBE Thermal Comfort Tool
    <br />
    <br />
    <a href="https://dashboard-b7zdid2ocq-ts.a.run.app/">View Demo</a>
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
python -m pytest tests/test_login.py --base-url http://0.0.0.0:9090
python -m pytest --numprocesses 3 --base-url http://0.0.0.0:9090
gcloud builds submit --project=emu-systems --substitutions=_REPO_NAME="comfort-tool-v2-test"
gcloud builds submit --project=emu-systems --substitutions=_REPO_NAME="comfort-tool-v2"
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

Project Link: [Environmental-Measurement-Unit-Systems/dashboard](https://github.com/Environmental-Measurement-Unit-Systems/dashboard)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Contributors

* [Federico Tartarini]()

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Teams & responsibilities
|  Task                 |  Team                        | Responsibilites                                     | 
|-----------------------|------------------------------|-----------------------------------------------------|
|  **Admin**            | Member 1 or Revolving        |  Meetings (Invitations, Notetaking), Communication  |
|  **Front-End**        | Member 1, Member 2           |  Front-End design and Dash implementation           |
|  **Data Management**  | Member 1, Member 2           |  Manage use of data within app                      |
|  **Visuals**          | Member 1, Member 2           |  Develop plots for main UI                          |
|  **Back-End**         | Member 1, Member 2, Member 3 |  Develop app back-end                               |



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/Environmental-Measurement-Unit-Systems/dashboard.svg?style=for-the-badge
[contributors-url]: https://github.com/Environmental-Measurement-Unit-Systems/dashboard/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Environmental-Measurement-Unit-Systems/dashboard.svg?style=for-the-badge
[forks-url]: https://github.com/Environmental-Measurement-Unit-Systems/dashboard/network/members
[stars-shield]: https://img.shields.io/github/stars/Environmental-Measurement-Unit-Systems/dashboard.svg?style=for-the-badge
[stars-url]: https://github.com/Environmental-Measurement-Unit-Systems/dashboard/stargazers
[issues-shield]: https://img.shields.io/github/issues/Environmental-Measurement-Unit-Systems/dashboard.svg?style=for-the-badge
[issues-url]: https://github.com/Environmental-Measurement-Unit-Systems/dashboard/issues
[license-shield]: https://img.shields.io/github/license/Environmental-Measurement-Unit-Systems/dashboard.svg?style=for-the-badge
[license-url]: https://github.com/Environmental-Measurement-Unit-Systems/dashboard/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: images/screenshot.png
[Python.org]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/




