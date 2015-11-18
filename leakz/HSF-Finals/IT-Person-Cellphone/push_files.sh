#!/bin/bash

# Setup

FILES=Apps/*
for f in $FILES
do
    echo "Processing apk: $f"
    adb push $f /sdcard/Download/
    adb install $f
done

FILES=Photos/*
for f in $FILES
do
    echo "Processing picture: $f"
    adb push $f /sdcard/Pictures/
done

adb push Contacts/00001.vcf /sdcard/
adb push wallet.txt /sdcard/

