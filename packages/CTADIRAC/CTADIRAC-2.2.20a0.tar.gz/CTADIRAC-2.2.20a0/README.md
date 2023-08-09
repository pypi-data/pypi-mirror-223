# CTADIRAC project

* CTADIRAC is a customized version of the DIRAC interware. As of today, it allows an easy and optimized access to Grid resources (mainly EGI) available to the CTA Virtual Organization (vo.cta.in2p3.fr). When CTAO DPPS will be setup, CTADIRAC will serve as the Computing Ressource and Worflow Management System.
* CTADIRAC specific documentation can be found at:
 https://redmine.cta-observatory.org/projects/cta_dirac/wiki/CTA-DIRAC_Users_Guide.
* [Wiki](https://gitlab.cta-observatory.org/cta-computing/dpps/CTADIRAC/-/wikis/)

# Release informations:

* Get `CTADIRAC` on `Pypi`: https://pypi.org/project/CTADIRAC/

# Deploying CTADIRAC

See the [dedicated documentation](docs/install_CTADIRAC.md).

CTADIRAC Helm charts: https://gitlab.cta-observatory.org/cta-computing/dpps/workload/CTADIRAC-charts
CTADIRAC fleet deployment on a Kubernetes cluster: https://gitlab.cta-observatory.org/cta-computing/dpps/workload/ctadirac-deployment

# Repositories and images:

* Install `CTADIRAC`:

```
pip install CTADIRAC
```

* Get `CTADIRAC` client `docker` image:

```
docker pull gitlab.cta-observatory.org:5555/cta-computing/dpps/ctadirac/dirac-client:latest
```

# Contribute to CTADIRAC:

* To contribute to CTADIRAC, please check out the full DIRAC developers guide at:
  http://dirac.readthedocs.io/en/integration/DeveloperGuide/index.html

* Fork CTADIRAC project

* Use [pre-commit](https://pre-commit.com/):

On Debian:
```bash
apt install pre-commit
```
On Mac:
```bash
brew install pre-commit
```
```bash
cd CTADIRAC
pre-commit install
```

# Contact Information
* Luisa Arrabito <arrabito@in2p3.fr>
