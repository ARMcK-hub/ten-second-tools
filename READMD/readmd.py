import pandas as pd

repo_df = pd.read_csv("repos.csv")

for repo in repo_df.index:
    input_dict = {}
    for index, item in enumerate(repo_df.iloc[repo]):
        input_dict[repo_df.columns[index]] = item
    
    if input_dict['README Complete'] == 'n':
    
        md_file = f"{input_dict['repo']}_README.md"
        print(md_file)
        
        with open(md_file, 'w') as f:
            f.write(f'''
<!-- 
README Template Author: otheneildrew
Template Source: https://github.com/othneildrew/Best-README-Template
Version Author: Drew McKinney
 -->





<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
![GitHub last commit](https://img.shields.io/github/last-commit/ARMcK-hub/{input_dict['repo']})
[![MIT License][license-shield]][license-url]
![GitHub top language](https://img.shields.io/github/languages/top/ARMcK-hub/{input_dict['repo']})
![GitHub repo size](https://img.shields.io/github/repo-size/ARMcK-hub/{input_dict['repo']})
![Website](https://img.shields.io/website?down_color=lightgrey&down_message=offline&up_color=blue&up_message=online&url=https%3A%2F%2Fwestendfinancial.herokuapp.com%2F)

<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="{input_dict['head_img_url']}">
    <img src="{input_dict['head_img_src']}" alt="Logo" width="100" height="100">
  </a>

  <h3 align="center">{input_dict['head_title']}</h3>

  <p align="center">
    {input_dict['head_description']}
    <br />
    <a href="{input_dict['head_img_url']}" target="_blank"><strong> >> Visit Demo >> </strong></a>
    <br />
    <a href="https://github.com/ARMcK-hub/{input_dict['repo']}/issues">Report Bug</a>
    -
    <a href="https://github.com/ARMcK-hub/{input_dict['repo']}/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [License](#license)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]]({input_dict['head_img_url']})

{input_dict['body_description']}

Here's why {input_dict['head_title']} is important:
{input_dict['important_factors']}


### Built With
{input_dict['built_with']}


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

<img src="https://avatars3.githubusercontent.com/u/57081049?s=460&u=1260bc893922a063a29f437d8565e4b970fe45ca&v=4" width=200>
<h3>Drew McKinney</h3>

[![GitHub][github-shield]][github-url]
[![LinkedIn][linkedin-shield]][linkedin-url]
[![Email][email-shield]][email-url]



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
{input_dict['acknowledgements']}



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

<!-- Stock -->
[license-url]: https://github.com/ARMcK-hub/West-End-Financial/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/drew-mckinney/
[email-shield]: https://img.shields.io/badge/-Email-black.svg?style=flat&colorB=555
[email-url]: mailto:andrewryanmckinney@gmail.com
[github-shield]: https://img.shields.io/badge/-GitHub-black.svg?style=flat&colorB=555
[github-url]: https://github.com/ARMcK-hub
[languages-shield]: https://img.shields.io/badge/-GitHub-black.svg?style=flat&colorB=555


<!-- Project Dynamic -->
[license-shield]: https://img.shields.io/github/license/ARMcK-hub/{input_dict['repo']}.svg?style=flat
[contributors-shield]: https://img.shields.io/github/contributors/ARMcK-hub/{input_dict['repo']}.svg?style=flat
[contributors-url]: https://github.com/ARMcK-hub/{input_dict['repo']}/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/ARMcK-hub/{input_dict['repo']}.svg?style=flat
[forks-url]: https://github.com/ARMcK-hub/{input_dict['repo']}/network/members
[stars-shield]: https://img.shields.io/github/stars/ARMcK-hub/{input_dict['repo']}.svg?style=flat
[stars-url]: https://github.com/ARMcK-hub/{input_dict['repo']}/stargazers
[issues-shield]: https://img.shields.io/github/issues/ARMcK-hub/{input_dict['repo']}.svg?style=flat
[issues-url]: https://github.com/ARMcK-hub/{input_dict['repo']}/issues
[product-screenshot]: {input_dict['product_screenshot']}

''')