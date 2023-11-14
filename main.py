import Config
import Model
import Tools
from PIL import Image
import os

users = []
users += Model.Contestant.get_data()
# users += Model.Organizer.get_data()
# users += Model.Volunteer.get_data()
# users += Model.Mentor.get_data()
# users += Model.Company.get_data()
# users += Model.Guest.get_data()
# users += Model.Assistant.get_data()

Tools.create_dir(Config.OUT_PATH)
Tools.empty_dir(Config.OUT_PATH)

i = 0
for u in users:
	u.generate_card()
	u.save()
	i+=1
	if i == 10:
		break

print('Generated ' + str(i) + ' cards')