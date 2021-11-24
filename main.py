import Config
import Model
import Tools
from PIL import Image

users = []
users += Model.Contestant.get_data()
users += Model.Organizer.get_data()
users += Model.Volunteer.get_data()
users += Model.Company.get_data()
users += Model.Guest.get_data()
users += Model.Assistant.get_data()

Tools.create_dir(Config.OUT_PATH)
Tools.empty_dir(Config.OUT_PATH)

# self.card.paste(image, Card.QR_POS)
# a4im = Image.new('RGB',
                #  (595, 842),   # A4 at 72dpi
                #  (255, 255, 255))  # White
# x,y=0,0
# i=0
for u in users:
	u.generate_card()
	# a4im.paste(u.card, (x,y))
	# i+=1
	# x+=u.card.width
	# if(i==2):
		# i=0
		# y+=u.card.height
		# x=0
	u.save()
# a4im.save("cards.pdf")

	# break