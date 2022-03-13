import json
import requests
from dateutil import parser as date_parser

API_BASE = 'https://bills-api.parliament.uk/api/v1'
BILL_IDS = ['2836', '2822', '1838', '2620', '2731']

def get_bill(bill_id):
	url = f"{API_BASE}/Bills/{bill_id}"
	return requests.get(url).json()

def get_stages(bill_id):
	url = f"{API_BASE}/Bills/{bill_id}/Stages"
	return requests.get(url).json()

def get_amendments(bill_id, stage_id):
	url = f"{API_BASE}/Bills/{bill_id}/Stages/{stage_id}/Amendments"
	return requests.get(url).json()

def get_amendment(amendment_id, stage_id, bill_id):
	url = f"{API_BASE}/Bills/{bill_id}/Stages/{stage_id}/Amendments/{amendment_id}"
	return requests.get(url).json()


"""

Get all introductions of new bills or amendments to existing ones where:

- bill id matches a subscribed bill id
- category tag matches a subscribed category

Consider these introductions/amendments as 'events' 

"""

class NewsfeedEvent():

	def __init__(self, bill_id, bill_title, event_type, time, details={}):
		self.bill_id = bill_id
		self.bill_title = bill_title

		if event_type not in ['introduction', 'amendment', 'stage_change']:
			raise f"{event_type} is not a recognized event type"
		else:
			self.event_type = event_type

		self.time = time
		self.details = details

	def output(self):
		if self.event_type == 'introduction':
			event_str = 'was introduced'
		elif self.event_type == 'amendment':
			event_str = 'was amended'
		elif self.event_type == 'stage_change':
			if self.details['new_stage'] == 'Royal Assent':
				event_str = 'received Royal Assent'
			else:
				event_str = f"moved to {self.details['new_stage']}"
		else:
			raise f"Unexepcted event type {self.event_type}"

		return f"{self.bill_title} {event_str} on {self.time.strftime('%d %b %Y')}"

def newsfeed(use_subscriptions=False):
	events = []

	# if narrowing to a set of bills the user has specified interest in,
	# use their subsriptions
	# else just look at all the bills that are available
	# (for now, just do the latter)

	for bill_id in BILL_IDS:
		
		bill = get_bill(bill_id)

		# get amendments and create event for each
		bill_stages = []
		all_sitting_dates = []

		# amendments are only given by bill stage in the API, so follow the history of the
		# bill in order to get all the relevant stages
		stages = get_stages(bill_id)
		for stage in stages['items']:
			sittings = stage['stageSittings']

			sitting_dates = []

			for sitting in sittings:
				bill_stage_id = sitting['billStageId']

				if bill_stage_id not in bill_stages:
					bill_stages.append(bill_stage_id)

				sitting_date = date_parser.parse(sitting['date'])
				sitting_dates.append(sitting_date)
				all_sitting_dates.append(sitting_date)

			# create an event to note that the bill moved stages at a certain point
			# use the earliest sitting date for each stage
			details = {
				'new_stage': stage['description']
			}
			events.append(NewsfeedEvent(bill_id, bill['shortTitle'], 'stage_change', min(sitting_dates), details))

		# create an event for the bill introduction
		# use the earliest date from all the sittings as the introduction date
		events.append(NewsfeedEvent(bill_id, bill['shortTitle'], 'introduction', min(all_sitting_dates)))

			

		# mark amendments
		"""
		for bill_stage in bill_stages:
			amendments = get_amendments(bill_id, stage)

			for amendment in amendments['items']:
				amendment_date = 
				event = NewsFeedEvent(bill_id, bill['short_title'], 'amendment', amendment_date)

				events.append(event)
		"""

	# sort the events with the newest first
	events.sort(key=lambda event: event.time, reverse=True)
	return events





"""

For each event, show the:

- Id/title of the bill
- Short description of the event
- Link to view the details

"""