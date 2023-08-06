from setuptools import setup, find_packages

setup(
    name="django_redis_session",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "django>=3.0",
        "redis>=3.5",
    ],
    author="Ömer Alkın",
    author_email="omeralkin7@gmail.com",
    description="A Django session backend with Redis storage",
    license="MIT",
    keywords="django redis session",
)
