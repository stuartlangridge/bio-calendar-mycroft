"""
List tech events happening in Birmingham over the next few days.
Uses the back end published for the Alexa Flash Briefing.
"""
from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import LOG
import requests
from requests import RequestException

FEED_URL = "https://birminghamio-alexa.surge.sh/bio.json"

class BirminghamIOSkill(MycroftSkill):
    def __init__(self):
        super(BirminghamIOSkill, self).__init__(name="BirminghamIOSkill")
        self.stop_requested = False

    @intent_handler(IntentBuilder("").require("Birmingham").require("TechEvents"))
    def handle_tech_events_intent(self, message):
        self.stop_requested = False
        try:
            r = requests.get(FEED_URL)
            events = r.json()
            if events:
                self.speak_dialog("from.the.calendar")
                for event in events:
                    if self.stop_requested: break
                    self.speak_dialog("meeting", data={"meeting": event.get("mainText", "An unknown meeting")})
            else:
                self.speak_dialog("no.events")
        except:
            self.speak_dialog("error")

    def stop(self):
        self.stop_requested = True
        return False

# The "create_skill()" method is used to create an instance of the skill.
# Note that it's outside the class itself.
def create_skill():
    return BirminghamIOSkill()
