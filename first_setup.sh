#!/bin/bash

# Look out for conflicts between git and cmssw
if [ ! -f ${CMSSW_BASE}/src/.git/HEAD ];
then
    echo "You seem to be on Ingrid and CMSSW area appears not to be set up correctly. Check README carefully."
    echo
    return 1
fi
cd ${CMSSW_BASE}/src/cp3_llbb/Calculators42HDM
# configure the origin repository
GITHUBUSERNAME=`git config user.github`
GITHUBUSERREMOTE=`git remote -v | grep upstream | awk '{print $2}' | head -n 1 | cut -d / -f 2`
git remote add origin git@github.com:${GITHUBUSERNAME}/${GITHUBUSERREMOTE}

# Add the remaining forks
git remote add OlivierBondu https://github.com/OlivierBondu/Calculators42HDM.git
git remote add AlexandreMertens https://github.com/AlexandreMertens/Calculators42HDM.git
git remote add KhawlaJaffel git@github.com:kjaffel/Calculators42HDM.git
