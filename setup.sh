#!/bin/bash

inventory=${INVENTORY:-inventory}

ansible-playbook -i ${inventory} site.yml $@
