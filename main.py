import os
import Constants
import Model
import Tools
users = []
users += Model.Contestant.get_data(os.path.join(Constants.RES_FOLDER, Constants.DB_CERT))
users += Model.Organizer.get_data()
users += Model.Volunteer.get_data()
users += Model.Company.get_data()
users += Model.Guest.get_data()

# Tools.create_dir(Constants.OUT_FOLDER)
# Tools.empty_dir(Constants.OUT_FOLDER)

for u in users:
	u.generate_card()
	# u.show()
	u.save()