#!/usr/bin/env python3
# coding = utf-8
#
# Copyright 2016 Steven Knoblich
#  Licensed to PSF under a Contributor Agreement.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied. See the License for the specific language governing
# permissions and limitations under the License.

import os

import ipaddr


def query_yes_no(question, default):
    valid = {"yes": True, "y": True, "ye": True, "j": True, "ja": True, "no": False, "n": False, "nein": False}
    if default is None:
        prompt = " [j/N] "
    elif default == "yes":
        prompt = " [J/n] "
    elif default == "no":
        prompt = " [j/N] "
    else:
        raise ValueError("Wrong answer: \"%s\"" % default)
    while True:
        print("%s%s" % (question, prompt))
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            print("[ERROR] Please answer with \"Yes / y\" or \"No / n\".")


def main():
    if os.path.exists("addresses.txt"):
        if not query_yes_no("[?] A file with IP addresses already exists. May I delete the file?", "yes"):
            print("[!] The file has to be deleted. I'm out!")
            exit(1)
        else:
            os.remove("addresses.txt")
    file = open("addresses.txt", "w+")
    subnet = input("[?] Which subnet should I calculate?\n> ")

    try:
        network = ipaddr.IPNetwork(subnet)
    except ValueError:
        print("[ERROR] The subnet is incorrect. I'm out!")
        exit(1)

    index = input("[?] How many IP addresses should I calculate? [max. %s]\n> " % network.numhosts)

    try:
        index = int(index)
    except ValueError:
        print("[ERROR] Your entry is incorrect. I'm out!")
        exit(1)

    if index > network.numhosts:
        print(
            "[!] You've entered a number which is bigger than the biggest possible number. I only will calculate %s addresses." % network.numhosts)

    print(
        "[INFO] The IPv%s subnet will be calculated. I also put the result in the file \"addresses.txt\". Please wait!" % network.version)

    calculated = 0

    for host in network.iterhosts():
        if calculated == index:
            break
        file.write(host.compressed)
        file.write("\n")
        calculated += 1

    print("[INFO] The subnet has been calculated an put into the file.")
    file.close()


if __name__ == '__main__':
    main()
