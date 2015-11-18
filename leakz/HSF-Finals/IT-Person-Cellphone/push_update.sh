#!/bin/bash
adb push creds.txt /sdcard/
adb shell "rm /sdcard/Download/XMarksTheSpot.apk"
adb push apks/XMarksTheSpot.apk /sdcard/Download/
adb install apks/XMarksTheSpot.apk
