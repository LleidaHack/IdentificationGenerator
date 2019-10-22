import os
import Constants
import Model

"""
def save(users,file_name):
	cards=[]
	pdf = FPDF()
	i=9
	for u in users:
		if(i==9):
			pdf.add_page('L')
			i=0
		pdf.image(u+'.png',100,100*i+1,100,100)
		i+=1
	pdf.output(file_name+'.pdf', "F")
"""
users=[]
# users += Model.Contestant.get_data(os.path.join(Constants.RES_FOLDER, Constants.DB_CERT))
# users += Model.Organizer.get_data()
# users += Model.Volunteer.get_data()
users += Model.Company.get_data()
# users += Model.Guest.get_data()
for u in users:
	u.generate_card()
	u.show()
	u.save()
	break
