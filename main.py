import os
import Constants
import Model

users = []
users += Model.Contestant.get_data(os.path.join(Constants.RES_FOLDER, Constants.DB_CERT))
users += Model.Organizer.get_data()
users += Model.Volunteer.get_data()
users += Model.Company.get_data()
users += Model.Guest.get_data()

for u in users:
	u.generate_card()
	# u.show()
	u.save()