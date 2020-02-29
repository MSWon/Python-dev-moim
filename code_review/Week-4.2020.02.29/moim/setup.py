import os
from setuptools import setup

def get_about():
    about = {}
    with open("./moim/about.py","r") as f:
        exec(f.read(), about)
    return about

def get_requires():
    result = []
    with open("./requirements.txt", "r") as f:
        for package_name in f:
            result.append(package_name)
    return result

about = get_about()

setup(
    name='moim',                            # 모듈명
    version=about['__version__'],                        # 버전
    author=about['__author__'],                    # 저자
    description=about['__description__'],   # 설명
    packages=['moim'],
    python_requires='>=3.6.0',
    install_requires=get_requires(),        # 패키지 설치를 위한 요구사항 패키지들
    entry_points={
        # moim이라는 명령어를 실행하면
        # moim모듈 main.py에서 main함수를 실행한다는 의미
        "console_scripts" : ["moim=moim.main:main"]
    },
    include_package_data=True,
    zip_safe=False,
)