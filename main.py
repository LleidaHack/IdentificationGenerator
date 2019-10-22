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

users = Model.Voluntari.get_data()
# users = Model.Concursant.get_data(os.path.join(Constants.RES_FOLDER,Constants.DB_CERT)) + Model.Organitzador.get_data() + Model.Voluntari.get_data() + Model.Empresa.get_data()
# users = Model.Concursant.get_data(os.path.join(Constants.RES_FOLDER,Constants.DB_CERT))
for u in users:
	u.generate_card()
	u.show()
	u.save()
	break