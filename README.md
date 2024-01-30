# IntPlanOpt
Integrated planning &amp; optimization tool

This tool provides a platform for integrated planning and optimization using optimization algorithms. 
Initially demonstrated with the example of meeting scheduling, 
the project's long-term goal is to advance into a comprehensive optimization system, 
operable across various domains and adaptable to the maximum likelihood principle.

## 1. Git
All activities can be found at the link below.

&rarr; [Project activity](https://github.com/rkvcode/Int-Plan-Opt/activity?ref=main)

## 2. UML
The project includes several UML diagrams. 
- &rarr; [Activity diagram](https://github.com/rkvcode/Int-Plan-Opt/blob/main/topics_answered/uml_diagrams/activity_uml.png)
- &rarr; [Components diagram](https://github.com/rkvcode/Int-Plan-Opt/blob/main/topics_answered/uml_diagrams/components_uml.png)
- &rarr; [Class diagram](https://github.com/rkvcode/Int-Plan-Opt/blob/main/topics_answered/uml_diagrams/classes_uml.png)

## 3. Requirements engineering
Requirements were made using 2 different tools: Notion and Xebrio (6 in each)
- &rarr; [Xebrio requirements](https://github.com/rkvcode/Int-Plan-Opt/blob/main/topics_answered/requirements/Xebrio-requirements.pdf)
- &rarr; [Notion requirements](https://apricot-hoodie-e6c.notion.site/Int-Plan-Opt-Requirements-db94b6b337bc49af901fe1ab803ab5f8?pvs=25)

## 4. Analysis
Analysis was carried out in a separate word document. However, pdf version is also available.
- &rarr; [Word document](https://github.com/rkvcode/Int-Plan-Opt/blob/main/topics_answered/analysis/Analysis.docx)
- &rarr; [PDF document](https://github.com/rkvcode/Int-Plan-Opt/blob/main/topics_answered/analysis/analysis.pdf)

## 5. DDD
For the Domain-Driven Development the event storming was carried out. Then, domains were drawn out of it and two chars created:
- &rarr; [Event storming + Core Domain chart](https://github.com/rkvcode/Int-Plan-Opt/blob/main/topics_answered/DDD/Event_storming_diagram.png)
- &rarr; [Domain relation](https://github.com/rkvcode/Int-Plan-Opt/blob/main/topics_answered/DDD/Domain%20relations.png)

## 6. Metrics
After connecting SonarCloud the results were the following:
- Reliability: 3 Bugs
- Security: 0 Vulnerabilities
- Maintainability: 10 Code Smells
- Security Review: 3 Security Hotspots
- Duplications: 0.0% Duplications

The issues were corrected (where possible). New metrics:
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=rkvcode_Int-Plan-Opt&metric=bugs)](https://sonarcloud.io/summary/new_code?id=rkvcode_Int-Plan-Opt)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=rkvcode_Int-Plan-Opt&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=rkvcode_Int-Plan-Opt)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=rkvcode_Int-Plan-Opt&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=rkvcode_Int-Plan-Opt)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=rkvcode_Int-Plan-Opt&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=rkvcode_Int-Plan-Opt)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=rkvcode_Int-Plan-Opt&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=rkvcode_Int-Plan-Opt)
[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=rkvcode_Int-Plan-Opt&metric=sqale_index)](https://sonarcloud.io/summary/new_code?id=rkvcode_Int-Plan-Opt)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=rkvcode_Int-Plan-Opt&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=rkvcode_Int-Plan-Opt)

## 7. Clean Code Development
&rarr; [Parameter and return types](https://github.com/rkvcode/Int-Plan-Opt/blob/main/solution.py#L64)

&rarr; [Docstrings](https://github.com/rkvcode/Int-Plan-Opt/blob/main/solution.py#L85)

&rarr; [Explanatory variable names](https://github.com/rkvcode/Int-Plan-Opt/blob/main/service_management.py#L17)

&rarr; [Throw exception with context](https://github.com/rkvcode/Int-Plan-Opt/blob/main/service_management.py#L33)

&rarr; [One assert per test](https://github.com/rkvcode/Int-Plan-Opt/blob/6a9e69276e1d7c3b5afd857ae5c7bb80a0bb5ddf/tests/test_input_management.py#L95C5-L95C11)

CCD sheet can be found here: 
&rarr; [CCD Sheet](https://github.com/rkvcode/Int-Plan-Opt/blob/main/topics_answered/CCD/sheet.pdf)


## 8. Build Management
Docker acts as a build management system in this project with the help of
docker-compose plugin. The program can be deployed using single command:

docker compose up -d --build

&rarr; [Dockerfile](https://github.com/rkvcode/Int-Plan-Opt/blob/main/Dockerfile)

&rarr; [docker-compose.yml](https://github.com/rkvcode/Int-Plan-Opt/blob/main/docker-compose.yml)

&rarr; [.dockerignore](https://github.com/rkvcode/Int-Plan-Opt/blob/main/.dockerignore)

CICD was implemented with github Action feature using docker image

&rarr; [Actions](https://github.com/rkvcode/Int-Plan-Opt/blob/main/.github/workflows/docker-image.yml)

## 9. Unit tests
Total 16 tests written with pytest.

&rarr; [Here](https://github.com/rkvcode/Int-Plan-Opt/blob/main/tests/test_config_management.py)

&rarr; [And here](https://github.com/rkvcode/Int-Plan-Opt/blob/main/tests/test_input_management.py)


## 10. IDE
I use Pycharm for about 4 years now as a main developer tool. It covers most of my requirements.
What I like most about it is:
- Support of multiple languages
- Internal jupyter support (much better than jupterlab)
- Remote development feature
- Possibility to connect ot databases
- Development and services feature
- Diagrams feature

and much more.

Favourite shortcuts:
- ctrl+c, ctrl+v :)
- ctrl+f
- ctrl+r
- shift+tab
- ctrl+/ - comment-uncomment
- alt+enter - show actions if there is a warning
- ctrl+enter - execute in console

## 11. Functional Programming
- [only final data structures](https://github.com/rkvcode/Int-Plan-Opt/blob/main/optimizing.py#L107)
- [(mostly) side-effect-free functions](https://github.com/rkvcode/Int-Plan-Opt/blob/main/service_management.py#L40)
- [the use of higher-order functions/functions as parameters and return values](https://github.com/rkvcode/Int-Plan-Opt/blob/main/optimizing.py#L81)
- [use closures / anonymous functions](https://github.com/rkvcode/Int-Plan-Opt/blob/main/configuration/fitness_function.py#L21)
