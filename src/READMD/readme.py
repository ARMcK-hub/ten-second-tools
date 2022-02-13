from abc import ABC, abstractmethod
from typing import Optional

from src.READMD.config import Repository, User


class ReadMe(ABC):
    host_name: str

    def write(self, repo: Repository, output: str) -> None:
        write_file = (
            f"/workspaces/TenSecondTools/src/READMD/output/README_{repo.name}.md"
        )
        with open(write_file, "w+") as wf:
            wf.write(output)

    def to_md(self, repo: Repository) -> None:
        output = self.build(repo)
        self.write(repo, output)

    @abstractmethod
    def build(self, repo: Repository) -> str:
        raise NotImplementedError


class GitHubReadMe(ReadMe):
    host_name = "github"
    shields_uri = "https://img.shields.io/github"

    def __init__(self, user: User) -> None:
        self.user = user
        self._repo: Optional[Repository] = None

    def reset(self) -> None:
        self._repo = None

    def build(self, repo: Repository) -> str:
        self._repo = repo

        build_ops = [
            self.header,
            self.shields,
            self.logo,
            self.toc,
            self.about,
            self.license,
            self.contact,
            self.acknowledgements,
            self.shield_def,
        ]
        output = "".join([op() for op in build_ops])

        self.reset()

        return output

    def header(self) -> str:
        return f"""
<!--
README Template Author: otheneildrew
Template Source: https://github.com/othneildrew/Best-README-Template
Version Author: {self.user.yourName}
-->"""

    def shields(self) -> str:
        return f"""
<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
![GitHub last commit]({self.shields_uri}/last-commit/{self.user.accountName}/{self._repo.name})
[![MIT License][license-shield]][license-url]
![GitHub top language]({self.shields_uri}/languages/top/{self.user.accountName}/{self._repo.name})
![GitHub repo size]({self.shields_uri}/repo-size/{self.user.accountName}/{self._repo.name})
"""

    def logo(self) -> str:
        return f"""
<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="{self._repo.link}">
    <img src="{self._repo.image}" alt="Logo" width="100" height="100">
  </a>

  <h3 align="center">{self._repo.title}</h3>

  <p align="center">
    {self._repo.description}
    <br />
    <a href="{self._repo.link}" target="_blank"><strong> >> Visit Demo >> </strong></a>
    <br />
    <a href="https://github.com/{self.user.accountName}/{self._repo.name}/issues">Report Bug</a>
    -
    <a href="https://github.com/{self.user.accountName}/{self._repo.name}/issues">Request Feature</a>
  </p>
</p>
"""

    def toc(self) -> str:
        return """
<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [License](#license)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)
"""

    def about(self) -> str:
        return (
            f"""
<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]]({self._repo.image})

{self._repo.body}

Here's why {self._repo.title} is important:"""
            + "\n".join([f"* {f}" for f in self._repo.features])
            + """
### Built With
"""
            + "\n".join(
                [f"* [{t['name']}]({t['link']})" for t in self._repo.technologies]
            )
        )

    def license(self) -> str:
        return """
<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information."""

    def contact(self) -> str:
        return f"""
<!-- CONTACT -->
## Contact

<img src="{self.user.portrait}" width=200>
<h3>{self.user.yourName}</h3>

[![GitHub][github-shield]][github-url]
[![LinkedIn][linkedin-shield]][linkedin-url]
[![Email][email-shield]][email-url]
"""

    def acknowledgements(self) -> str:
        return """
<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
""" + "\n".join(
            [f"* [{a['name']}]({a['link']})" for a in self._repo.acknowledgements]
        )

    def shield_def(self) -> str:
        return f"""
<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

<!-- Stock -->
[license-url]: https://github.com/{self.user.accountName}/{self._repo.name}/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/{self.user.linkedInAccount}/
[email-shield]: https://img.shields.io/badge/-Email-black.svg?style=flat&colorB=555
[email-url]: mailto:{self.user.email}
[github-shield]: https://img.shields.io/badge/-GitHub-black.svg?style=flat&colorB=555
[github-url]: https://github.com/{self.user.accountName}
[languages-shield]: https://img.shields.io/badge/-GitHub-black.svg?style=flat&colorB=555


<!-- Project Dynamic -->
[license-shield]: https://img.shields.io/github/license/{self.user.accountName}/{self._repo.name}.svg?style=flat
[contributors-shield]: https://img.shields.io/github/contributors/{self.user.accountName}/{self._repo.name}.svg?style=flat
[contributors-url]: https://github.com/{self.user.accountName}/{self._repo.name}/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/{self.user.accountName}/{self._repo.name}.svg?style=flat
[forks-url]: https://github.com/{self.user.accountName}/{self._repo.name}/network/members
[stars-shield]: https://img.shields.io/github/stars/{self.user.accountName}/{self._repo.name}.svg?style=flat
[stars-url]: https://github.com/{self.user.accountName}/{self._repo.name}/stargazers
[issues-shield]: https://img.shields.io/github/issues/{self.user.accountName}/{self._repo.name}.svg?style=flat
[issues-url]: https://github.com/{self.user.accountName}/{self._repo.name}/issues
[product-screenshot]: {self._repo.image}"""
