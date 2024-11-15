import Config
# import Model
from models.assistant import Assistant
from models.company import Company
from models.contestant import Contestant
from models.guest import Guest
from models.mentor import Mentor
from models.organizer import Organizer
from models.volunteer import Volunteer
import tools
from PIL import Image
import os

users = []
users += Contestant.get_data()
# users += Organizer.get_data()
# users += Volunteer.get_data()
# users += Mentor.get_data()
# users += Company.get_data()
# users += Guest.get_data()
# users += Assistant.get_data()

tools.create_dir(Config.OUT_PATH)
tools.empty_dir(Config.OUT_PATH)

i = 0
for u in users:
	u.generate_card()
	u.save()
	i+=1
	if Config.TEST:
		if i == 10:
			break

print('Generated ' + str(i) + ' cards')