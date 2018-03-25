#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

from colorama import Fore, Back, Style
import speech_recognition as sr
import sys
import argparse
import logging as log
import types

GCP = Fore.BLUE + "GCP" + Style.RESET_ALL


def deep_fried_error_message(self, msg):
    self.critical(Back.WHITE + Fore.RED + msg + Style.RESET_ALL)


def SafeTrek():
    print('Catchphrase has been detected by GCP, contacting SafeTrek API...')


# TODO make this asynchronous
def handleAudio(audio):
    try:
        result = r.recognize_google_cloud(
            audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS)
        log.info(GCP + ": " + result)
        if args.catch_phrase in result:
            SafeTrek()
    except sr.UnknownValueError:
        log.warn(GCP + " couldn't tell what you are saying.")


ap = argparse.ArgumentParser(
    description="Uses GCP Speech API to detect \"catchphrases\" to invoke a SafeTrek action.")
ap.add_argument("-v", "--verbose", action="store_true",
                help="Print extra debugging messages to stderr")
ap.add_argument("--gcp", type=str, dest="gcp_key", default="private/pervalert-ef8bf59d2f9b.json",
                help="location of the Google Cloud Platform JSON key")
ap.add_argument("-p", "--phrase", type=str, dest="catch_phrase", default="help me",
                help="set the trigger catch phrase (default: \"help me\")")  # TODO allow this to be defined multiple times?
ap.add_argument("--no-report", dest="no_report", action="store_true",
                help="skip report to front-end website on trigger")
args = ap.parse_args()
log.basicConfig(
    format="[ %(asctime)-24s] %(levelname)-8s -- %(message)s", level=log.INFO)
log.deepFry = types.MethodType(deep_fried_error_message, log)
if not args.verbose:
    log.getLogger(__name__).setLevel(log.ERROR)

# recognize speech using Google Cloud Speech
try:
    with open(args.gcp_key) as private_file:
        GOOGLE_CLOUD_SPEECH_CREDENTIALS = private_file.read()
        log.info(Style.DIM + args.gcp_key + " imported as GCI key." +
                 Style.RESET_ALL)
except Exception as e:
    print(e)
    log.deepFry("could not read " + args.gcp_key)
    sys.exit(1)

mp = sr.Microphone()
r = sr.Recognizer()

with mp as microphone:
    print("Don't talk right now... r.adjust_for_ambient_noise")
    r.adjust_for_ambient_noise(microphone)

while True:
    with mp as microphone:
        log.info("Listening for danger...")
        # TODO async
        handleAudio(r.listen(source=microphone,
                             timeout=10, phrase_time_limit=3))
