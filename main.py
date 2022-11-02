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
for i in range(10):
    c.generate_card()
    c.card.save(os.path.join(Config.OUT_PATH, 'card' + str(i) + '.png'))
# for u in users:
# 	u.generate_card()
# 	u.save()
# 	break


