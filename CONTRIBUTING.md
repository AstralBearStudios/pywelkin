# Contributing Guidelines

️⚠ **Warning: The Contributing Guidelines is a WIP. This project is in its early stages and does not have any code. Please wait to raise pull requests, and stay tuned for updates.**

Thank you for making a contribution to Welkin. This document explains the steps to have your changes reviewed, tested, and merged. If you have any questions about this document or contributing in general, see: TBD.

Before you request a merge request, please see the: TBD
TODO: Determine Full Contributing Guidelines

## Installing
- Setup a python virtual environment using your favorite tool.
  - Current python version: 3.12.
- Make sure to git clone from the main branch
- You can either use 
- To install a specific package ...
  - *Warning:* pywelkin is a [namespace package](), which means it contains its own packages.
    To run the tests, make sure that ALL




## Testing

## Static Type Checking (mypy)


## Style


## Security
See SECURITY.md for our full security policy. In short, if you find a vulnerability, please report it to the lead developer(s) and *do not* make it public. This ensures we have adequate time to release a patch and not advertise an exploit.
  - After we complete a patch, we will announce the past vulnerability publicly.

## Copyright and Licensing
- You may apply a license that is compatible with the license(s) in the specific subpackage:
  - core, cli: Apache-2.0-WITH-LLVM-exception (permissive),
  - gui, android, ios, desktop: LGPL-3.0-or-later (copyleft).
- Whenever you create a file for the project, you automatically retain ownership of the copyright. This means you *do not* need to add copyright information at the top of the file; you only need the license. 
  - Our version control system (currently git) will keep track of your contribution, and they will be publicly available on GitHub.
  - If you would like to include a copyright notice, see the format below.
- All licenses (and copyrights) should be written in the SPDX style. See the [REUSE specification](https://reuse.software/spec/) for a guide. Note that we are only partially compliant and are focusing on licenses. 
  - We run the python package [reuse](https://github.com/fsfe/reuse-tool) to make sure licenses are correct.
  
