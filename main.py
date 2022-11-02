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
c=Model.Company('Laura Haro Escoi', 'Lleidahack')
t=40
h=40
for i in range(4):
    c.generate_card(t=t, h=h)
    c.card.save(os.path.join(Config.OUT_PATH, 'card' + str(i) + '.png'))
    
# for u in users:
# 	u.generate_card()
# 	u.save()
# 	break


