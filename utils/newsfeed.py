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

def get_sample_bill_ids(sample_size=10):
	url = f"{API_BASE}/Bills?Take={sample_size}&SortOrder=DateUpdatedDescending"

	bill_ids = []
	bills = requests.get(url).json()
	for bill in bills['items']:
		bill_ids.append(bill['billId'])

	return bill_ids

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
			num_amendments = self.details['num_amendments']

			if num_amendments == 1:
				event_str = f"was amended"
			else:
				event_str = f"was amended {num_amendments} times"
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

	for bill_id in get_sample_bill_ids(5):
		
		bill = get_bill(bill_id)

		# the API only allows querying amendments by bill stage, so follow the history
		# of the bill in order to get all the relevant stages

		bill_stages = []
		all_sitting_dates = []

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

			if len(sitting_dates) > 0:
				# create an event to note that the bill moved stages at a certain point
				# use the earliest sitting date for each stage
				details = {
					'new_stage': stage['description']
				}
				events.append(NewsfeedEvent(bill_id, bill['shortTitle'], 'stage_change', min(sitting_dates), details))

				amendments = get_amendments(bill_id, bill_stage_id)
				if amendments['totalResults'] > 0:
					events.append(NewsfeedEvent(bill_id, bill['shortTitle'], 'amendment', min(sitting_dates), { 'num_amendments': amendments['totalResults'] }))


		# create an event for the bill introduction
		# use the earliest date from all the sittings as the introduction date
		events.append(NewsfeedEvent(bill_id, bill['shortTitle'], 'introduction', min(all_sitting_dates)))

	events.sort(key=lambda event: event.time, reverse=True)
	return events
