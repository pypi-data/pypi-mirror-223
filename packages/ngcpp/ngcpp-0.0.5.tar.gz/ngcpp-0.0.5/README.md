# Install

```shell
pip install ngcpp
sudo apt install fzf # iteractive fuzzy finder

# if apt installed fzf does not work or give strange behavior
git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
~/.fzf/install
```

# Feature

## cluster `ngc_cluster --help`

* `ngc_cluster usage --help`: List user usage
* `ngc_cluster hang --help`: List your all hanging jobs
* `ngc_cluster list --help`: List your jobs in one cluster
* `ngc_cluster alias --help`: List all available cluster aliases

## job `ngc_job --help`

* `ngc_job kill --help`: kill your jobs interactively
* `ngc_job result --help`: download results for your jobs interactively
* `ngc_job bash --help`: exec bash for one selected job~(support autoresuming)
