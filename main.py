import Config
import Model
import Tools
from PIL import Image
import os

users = []
# users += Model.Contestant.get_data()
# users += Model.Organizer.get_data()
# users += Model.Volunteer.get_data()
# users += Model.Company.get_data()
# users += Model.Guest.get_data()
# users += Model.Assistant.get_data()

Tools.create_dir(Config.OUT_PATH)
Tools.empty_dir(Config.OUT_PATH)


#create 4 cars on each type
users=[]
for i in range(4):
    users.append(Model.Colaborator())
    users.append(Model.Organizer())
    users.append(Model.Volunteer())
    users.append(Model.Expositor())
    
for u in users:
	u.generate_card()
	u.save()
# 	break


