<img src="assets/heimdall.jpg" alt="Heimdall" width="230px">

# heimdall-python
In Norse mythology, Heimdall has incredibly acute senses, particularly his sight and hearing. He can perceive nearly all that occurs within the Nine Realms, allowing him to detect the presence of individuals, even across great distances. Our agents are also great at sensing exceptions and obtaining stack traces from everywhere in the system.

# Build 
Since we use C extensions, the whl files built are specific to the platform it is built on. There are 2 sections here: local build and build to publish.  
`Local build` (usually during development) talks about steps to locally build the whl file specific to the platform / architecture your system is on.  
`Build to publish` talks about how you can build whl files for all python versions for manylinux distributions.
## Local build
### Pre-reqs
1. Install `pyenv` to manage multiple python versions.
```
# Install basic system things
sudo apt-get install libbz2-dev libncurses-dev libreadline-dev openssl libssl-dev libffi-dev

# Install pyenv
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc

# Install python
pyenv install 3.8
pyenv global 3.8
```

2. Basic build tools
```
sudo apt-get -y -q --no-install-recommends install \
     curl ca-certificates gcc build-essential cmake \
     python3 python3-dev python3-setuptools
```

### Steps
These steps build a release `dist/ctrlb_heimdall-1.0.0-cp310-cp310-linux_x86_64.whl`  (for python 3.10)  

1. Select the python version you are interested in.
```
pyenv global 3.10
```

2. Create `virtual environment` and install package dependencies.
```
python -m venv venv3.10
source venv3.10/bin/activate
pip install -r requirements.txt
```

3. Build dependencies first. `Google python cloud debugger` uses `glog` and `gflags` libraries, so those are built first.
```
./pre-build.sh
```

4. Use setup tools to build `Google python cloud debugger` from source code (only supported on Linux) and our `heimdall` agent.
```
./build_tools/build_local.sh
```
## Build to publish
The whl files built in above step cannot be put on Pypi. Read more about this problem [here](https://github.com/pypa/manylinux). That is why we use `manylinux` docker image to build.

```
docker pull quay.io/pypa/manylinux2010_x86_64

sudo ./clean-full.sh

docker run --rm -e PLAT=manylinux2010_x86_64 -v `pwd`:/heimdall-python quay.io/pypa/manylinux2010_x86_64 /heimdall-python/build_tools/build_wheels.sh

twine upload dist/* --verbose
```
## Clean
```
chmod +x clean.sh
sudo ./clean.sh
```


## Release
Find the latest release [here](https://github.com/ctrlb-hq/heimdall-python/releases/latest/download/heimdall_python-0.1.0-cp310-cp310-linux_x86_64.whl)

## Debug
```
./build_tools/build_local.sh && pip install dist/ctrlb_heimdall-1.0.0-cp310-cp310-linux_x86_64.whl --force-reinstall
```








