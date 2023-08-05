#
# Copyright (c) 2023 Airbyte, Inc., all rights reserved.
#


from setuptools import find_packages, setup

MAIN_REQUIREMENTS = ["airbyte-cdk", "stripe==2.56.0", "pendulum==2.1.2"]

TEST_REQUIREMENTS = [
    "pytest~=6.1",
    "requests-mock",
    "requests_mock~=1.8",
    "connector-acceptance-test",
]

setup(
    description="Source implementation for Stripe.",
    packages=find_packages(),
    install_requires=MAIN_REQUIREMENTS,
    package_data={"": ["*.json", "*.yaml", "schemas/*.json", "schemas/shared/*.json"]},
    extras_require={
        "tests": TEST_REQUIREMENTS,
    },
)
