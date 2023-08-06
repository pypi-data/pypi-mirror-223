from setuptools import setup, find_packages

deps = [
    'imageio',
    'scikit_image',
    'matplotlib',
    'munch',
    'tfpnp',
    'cvxpy',
    'torchlights',
    'tensorboardX',
    'termcolor',
    'proximal',
    'opencv-python'
]

setup(
    name='dprox',
    description='A domain-specific language and compiler that transforms optimization problems into differentiable proximal solvers.',
    url='https://github.com/princeton-computational-imaging/Delta-Prox',
    author='Zeqiang Lai',
    author_email='laizeqiang@outlook.com',
    packages=find_packages(),
    version='0.2',
    include_package_data=True,
    install_requires=deps,
)
